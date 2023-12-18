""" Ground motion Kriger: Core
"""

import numpy as np
import gmms
from gmms import get_fault_URC
from gmms import get_representative_fault
from gmms import get_faulting_style
from gmms import get_distances_cy
from .helpers import make_array
import pygmm

__author__ = 'A. Renmin Pretell Ductram'


class Site:
	
	def __init__(self, latitude, longitude, Vs30=None, Z1p0=None, Z2p5=None):
		self.Nsites    = len(latitude)
		self.latitude  = latitude
		self.longitude = longitude
		self.IM_mu  = np.full(self.Nsites, np.nan)
		self.IM_phi = np.full(self.Nsites, np.nan)
		self.IM_tau = np.full(self.Nsites, np.nan)

		if Vs30 is not None:
			self.Vs30 = Vs30

		if Z1p0 is None and Vs30 is not None:
			self.Z1p0 = np.exp((-7.15/4)*np.log((self.Vs30**4+571**4)/(1360**4+571**4))) # BSSA14
		else:
			self.Z1p0 = Z1p0

		if Z2p5 is None and Vs30 is not None:
			self.Z2p5 = np.exp(7.089-1.144*np.log(self.Vs30)) # CB13
		else:
			self.Z2p5 = Z2p5
	
	def get_distances(self,fault):
		params = [*fault]
		params = sum([[self.latitude.tolist(),self.longitude.tolist()],params],[])
		params = make_array(params)
		self.Rjb, self.Rrup, self.Rx = get_distances_cy(*params)

	def get_gmim(self, event, fault, gmim, flag_CAVgm=None, flag_PSV=None):
		self.gmim   = gmim
		if flag_CAVgm is None:
			self.flag_CAVgm = 1
		if flag_PSV is None:
			self.flag_PSV = 1
		
		if gmim.lower() == 'pga':
			self.gmim_tag = 0
		elif gmim.lower() == 'pgv':
			self.gmim_tag = 1
		elif gmim.lower() == 'ia':
			self.gmim_tag = 2
		elif gmim.lower() == 'cav':
			self.gmim_tag = 3
		elif gmim.lower() == 'cavdp':
			self.gmim_tag = 4
		elif gmim.lower() == 'psa(0.3)':
			self.gmim_tag = 5
		elif gmim.lower() == 'psa(0.6)':
			self.gmim_tag = 6
		elif gmim.lower() == 'psa(1.0)':
			self.gmim_tag = 7

		IM_mu  = np.zeros(self.Nsites)
		IM_phi = np.zeros(self.Nsites)
		IM_tau = np.zeros(self.Nsites)
		
		if self.gmim_tag == 0:
			if event.tectonic.lower() == 'crustal':
				for i in range(self.Nsites):
					scenario = pygmm.Scenario(mag=event.M,depth_1_0=self.Z1p0[i],dist_jb=self.Rjb[i],v_s30=self.Vs30[i],mechanism=fault.fmech,region=event.region)
					gmm_estimate = pygmm.BooreStewartSeyhanAtkinson2014(scenario)
					IM_mu[i]  = np.log(gmm_estimate.pga)
					IM_phi[i] = gmm_estimate._phi[0]
					IM_tau[i] = gmm_estimate._tau[0]
			else:
				print('No ground motion models currently implemented for {} events.'.format(event.tectonic))
				return

		elif self.gmim_tag == 1:
			if event.tectonic.lower() == 'crustal':
				for i in range(self.Nsites):
					scenario = pygmm.Scenario(mag=event.M,depth_1_0=self.Z1p0[i],dist_jb=self.Rjb[i],v_s30=self.Vs30[i],mechanism=fault.fmech,region=event.region)
					gmm_estimate = pygmm.BooreStewartSeyhanAtkinson2014(scenario)
					IM_mu[i]  = np.log(gmm_estimate.pgv)
					IM_phi[i] = gmm_estimate._phi[-1]
					IM_tau[i] = gmm_estimate._tau[-1]
			else:
				print('No ground motion models currently implemented for {} events.'.format(event.tectonic))
				return
		
		elif self.gmim_tag in [5,6,7]:
			T = float(gmim[4:7])
			periods = pygmm.model.load_data_file('boore_stewart_seyhan_atkinson-2014.csv', 2).period
			boo_IM  = periods==T
				
			for i in range(self.Nsites):
				scenario = pygmm.Scenario(mag=event.M,depth_1_0=self.Z1p0[i],dist_jb=self.Rjb[i],v_s30=self.Vs30[i],mechanism=fault.fmech,region=event.region)
				gmm_estimate = pygmm.BooreStewartSeyhanAtkinson2014(scenario)
				IM_mu[i]  = np.log(gmm_estimate.spec_accels[boo_IM[2:]][0])
				IM_phi[i] = gmm_estimate._phi[boo_IM][0]
				IM_tau[i] = gmm_estimate._tau[boo_IM][0]

		elif self.gmim_tag == 2:
			if event.tectonic.lower() == 'crustal' and event.region.lower() != 'japan':
				[IM_mu,IM_phi,IM_tau] = gmms.CampbellBozorgnia2019.CampbellBozorgnia2019_cy(0,event.M,fault.rwidth,fault.rdip,fault.rZtor,event.hyp_Z,self.Rjb,self.Rrup,self.Rx,self.Vs30,self.Z2p5,fault.fnm,fault.frv,event.region)
			else:
				[IM_mu,IM_phi,IM_tau] = gmms.FoulserPiggottGoda2015.FoulserPiggottGoda2015_cy(0,event.M,event.hyp_lat,event.hyp_lon,event.hyp_Z,self.Rrup,self.Vs30,event.fins,event.fint,fault.fnm,fault.frv)

		elif self.gmim_tag == 3:
			if event.tectonic.lower() == 'crustal' and event.region.lower() != 'japan':
				[IM_mu,IM_phi,IM_tau] = gmms.CampbellBozorgnia2019.CampbellBozorgnia2019_cy(1,event.M,fault.rwidth,fault.rdip,fault.rZtor,event.hyp_Z,self.Rjb,self.Rrup,self.Rx,self.Vs30,self.Z2p5,fault.fnm,fault.frv,event.region)
			else:
				[IM_mu,IM_phi,IM_tau] = gmms.FoulserPiggottGoda2015.FoulserPiggottGoda2015_cy(1,event.M,event.hyp_lat,event.hyp_lon,event.hyp_Z,self.Rrup,self.Vs30,event.fins,event.fint,fault.fnm,fault.frv)

		elif self.gmim_tag == 4:
			if event.tectonic.lower() == 'crustal':
				[IM_mu,IM_phi,IM_tau] = gmms.CampbellBozorgnia2011.CampbellBozorgnia2011_cy(event.M,fault.rdip,fault.rZtor,self.Rjb,self.Rrup,self.Rx,self.Vs30,self.Z1p0,self.Z2p5,fault.fnm,fault.frv,self.flag_CAVgm,self.flag_PSV)
			else:
				print('No ground motion models currently implemented for {} events.'.format(event.tectonic))
				return

		self.IM_mu  = IM_mu
		self.IM_phi = IM_phi
		self.IM_tau = IM_tau


class Event:

	def __init__(self,name,M, hyp_lat, hyp_lon, hyp_Z, tectonic, region):
		self.name     = name
		self.M        = M
		self.hyp_lat  = hyp_lat
		self.hyp_lon  = hyp_lon
		self.hyp_Z    = hyp_Z
		self.tectonic = tectonic
		self.region   = region

		if self.tectonic.lower() == 'interface':
			self.fins = 0
			self.fint = 1
		elif self.tectonic.lower() == 'intraslab':
			self.fins = 1
			self.fint = 0
		else:
			self.fins = 0
			self.fint = 0


class Fault:

	def __init__(self, length, width, strike, dip, rake, ULC_lat, ULC_lon, Ztor, flag=None):
		self.Nsegm   = len(length)
		self.length  = length
		self.width   = width
		self.strike  = strike
		self.dip     = dip
		self.rake    = rake
		self.ULC_lat = ULC_lat
		self.ULC_lon = ULC_lon
		self.Ztor    = Ztor

	def __iter__(self):
		yield self.ULC_lat.tolist()
		yield self.ULC_lon.tolist()
		yield self.URC_lat.tolist()
		yield self.URC_lon.tolist()
		yield self.width.tolist()
		yield self.length.tolist()
		yield self.dip.tolist()
		yield self.strike.tolist()
		yield self.Ztor.tolist()

	def get_URC(self):
		self.URC_lat, self.URC_lon = get_fault_URC(self.ULC_lat, self.ULC_lon, self.length, self.strike)

	def get_rfault(self):
		self.rrake,self.rwidth,self.rdip,self.rZtor = get_representative_fault(self.rake,self.width,self.length,self.dip,self.Ztor)

	def get_fstyle(self):
		self.fnm,self.frv,self.fmech = get_faulting_style(self.rrake)
