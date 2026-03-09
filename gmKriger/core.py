""" Ground motion Kriger: Core
"""

import numpy as np
import pygmm
import gmms
from .helpers import make_array

__author__ = 'A. Renmin Pretell Ductram'


gmms.distancetools.select_backend('Cython')


def set_gmim_tag(gmim):
	
	if gmim.lower() == 'pga':
		gmim_tag = 0
	elif gmim.lower() == 'pgv':
		gmim_tag = 1
	elif gmim.lower() == 'ia':
		gmim_tag = 2
	elif gmim.lower() == 'cav':
		gmim_tag = 3
	elif gmim.lower() == 'cavdp':
		gmim_tag = 4
	elif gmim.lower() == 'psa(0.100)':
		gmim_tag = 5
	elif gmim.lower() == 'psa(0.300)':
		gmim_tag = 6
	elif gmim.lower() == 'psa(0.600)':
		gmim_tag = 7
	elif gmim.lower() == 'psa(1.000)':
		gmim_tag = 8
	elif gmim.lower() == 'psa(3.000)':
		gmim_tag = 9
	elif gmim.lower() == 'psa(6.000)':
		gmim_tag = 10
	elif gmim.lower() == 'psa(10.000)':
		gmim_tag = 11
	else:
		raise NotImplementedError('gmKriger does not currently suppport the requested ground motion IM.')

	return gmim_tag


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
			self.Z1p0 = np.exp((-7.15/4)*np.log((self.Vs30**4+571**4)/(1360**4+571**4)))/1000. # km
		else:
			self.Z1p0 = Z1p0

		if Z2p5 is None and Vs30 is not None:
			self.Z2p5 = np.exp(7.089-1.144*np.log(self.Vs30)) # km
		else:
			self.Z2p5 = Z2p5


	def get_distances(self, fault):
		gmms.distancetools.select_backend('Python')

		params = [*fault]
		params = sum([[self.latitude.tolist(),self.longitude.tolist()],params],[])
		params = make_array(params)
		
		self.Rjb, self.Rrup, self.Rx, self.Ry0 = gmms.distancetools.get_distances(*params)


	def get_gmim(self, event, fault, gmim, gmms, flag_CAVgm=None, flag_PSV=None):
		
		self.gmim     = gmim
		self.gmim_tag = set_gmim_tag(gmim)
		self.Ngmim    = len(gmms.keys())

		IM_mu  = np.zeros([self.Nsites,self.Ngmim])
		IM_phi = np.zeros([self.Nsites,self.Ngmim])
		IM_tau = np.zeros([self.Nsites,self.Ngmim])

		if self.gmim_tag in [0, 1]:
			
			for i in range(self.Nsites):

				scenario = pygmm.Scenario(mag=event.M,v_s30=self.Vs30[i],dist_jb=self.Rjb[i],dist_rup=self.Rrup[i],dist_x=self.Rx[i],dist_y0=self.Ry0[i],
							 depth_1_0=self.Z1p0[i],depth_2_5=self.Z2p5[i],depth_tor=fault.rZtor,on_hanging_wall=(self.Rx[i]>0),
							 dip=fault.rdip,width=fault.rwidth,dist_crjb=False,is_aftershock=False,mechanism=fault.fmech,region=event.region)
				self.scenario = scenario
				
				for j,gmm in enumerate(gmms.keys()):
					gmm_IM = gmms[gmm](scenario)
					
					if self.gmim_tag == 0:
						IM_mu[i,j] = np.log(gmm_IM.pga)
					
					elif self.gmim_tag == 1:
						IM_mu[i,j] = np.log(gmm_IM.pgv)
						
					IM_phi[i,j] = gmm_IM._phi[-1]
					IM_tau[i,j] = gmm_IM._tau[-1]
	
		elif self.gmim_tag == 2:
			
			for j,gmm in enumerate(gmms.keys()):
				if event.tectonic.lower() == 'crustal' and event.region.lower() != 'japan':
					[IM_mu_,IM_phi_,IM_tau_] = gmms[gmm](0,event.M,fault.rwidth,fault.rdip,fault.rZtor,event.hyp_Z,self.Rjb,self.Rrup,self.Rx,self.Vs30,self.Z2p5,fault.fnm,fault.frv,event.region)
				else:
					[IM_mu_,IM_phi_,IM_tau_] = gmms[gmm](0,event.M,event.hyp_lat,event.hyp_lon,event.hyp_Z,self.Rrup,self.Vs30,event.fins,event.fint,fault.fnm,fault.frv)
				
				IM_mu[:,j]  = IM_mu_
				IM_phi[:,j] = IM_phi_
				IM_tau[:,j] = IM_tau_
				
		elif self.gmim_tag == 3:
			
			for j,gmm in enumerate(gmms.keys()):
				if event.tectonic.lower() == 'crustal' and event.region.lower() != 'japan':
					[IM_mu_,IM_phi_,IM_tau_] = gmms[gmm](1,event.M,fault.rwidth,fault.rdip,fault.rZtor,event.hyp_Z,self.Rjb,self.Rrup,self.Rx,self.Vs30,self.Z2p5,fault.fnm,fault.frv,event.region)
				else:
					[IM_mu_,IM_phi_,IM_tau_] = gmms[gmm](1,event.M,event.hyp_lat,event.hyp_lon,event.hyp_Z,self.Rrup,self.Vs30,event.fins,event.fint,fault.fnm,fault.frv)

				IM_mu[:,j]  = IM_mu_
				IM_phi[:,j] = IM_phi_
				IM_tau[:,j] = IM_tau_

		elif self.gmim_tag in [4,5,6,7,8,9,10,11]:
			print('gmKriger does not currently support the requested ground motion IM.')
			return

		self.gmmIM_mu  = IM_mu
		self.gmmIM_phi = IM_phi
		self.gmmIM_tau = IM_tau


class Event:

	def __init__(self, name, M, hyp_lat, hyp_lon, hyp_Z, tectonic, region):
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
		yield self.dip.tolist()
		yield self.strike.tolist()
		yield self.Ztor.tolist()

	def get_URC(self):
		self.URC_lat, self.URC_lon = gmms.faulttools.get_fault_URC(self.ULC_lat, self.ULC_lon, self.length, self.strike)

	def get_rfault(self):
		self.rrake,self.rwidth,self.rdip,self.rZtor = gmms.faulttools.get_representative_fault(self.rake,self.width,self.length,self.dip,self.Ztor)

	def get_fstyle(self):
		self.fnm,self.frv,self.fmech = gmms.faulttools.get_faulting_style(self.rrake)


class GMM_gmIM:

	def __init__(self, gmim, event):
		
		self.gmim     = gmim
		self.gmim_tag = set_gmim_tag(gmim)
		self.region = event.region
		self.tectonic = event.tectonic

		if self.gmim_tag in [0,1,5,6,7,8,9,10,11]:

			if self.tectonic.lower() == 'crustal':
				self.nGMM = 4
				self.GMMs = {
							'ask14':  pygmm.AbrahamsonSilvaKamai2014,
							'bssa14': pygmm.BooreStewartSeyhanAtkinson2014,
							'cb14':   pygmm.CampbellBozorgnia2014,
							'cy14':   pygmm.ChiouYoungs2014,
							}

				self.weight = {
							'ask14':  1/6,
							'bssa14': 1/3,
							'cb14':   1/6,
							'cy14':   1/3,
							}

			elif self.tectonic.lower() == 'interface':

				if self.gmim_tag == 1:
					self.nGMM = 2
					self.GMMs = {}
					raise NotImplementedError('gmKriger does not currently support {} for interface events.'.format(self.gmim))

				else:
					self.nGMM = 3
					self.GMMs = {}
					raise NotImplementedError('gmKriger does not currently support {} for interface events.'.format(self.gmim))

			elif self.tectonic.lower() == 'intraslab':

				if self.gmim_tag == 1:
					self.nGMM = 2
					self.GMMs = {}
					raise NotImplementedError('gmKriger does not currently support {} for intraslab events.'.format(self.gmim))

				elif self.gmim_tag == 0:
					self.nGMM = 3
					self.GMMs = {}
					raise NotImplementedError('gmKriger does not currently support {} for intraslab events.'.format(self.gmim))

			elif self.tectonic.lower() == 'continental':
				self.nGMM   = 1
				self.GMMs   = {}
				self.weight = 1
				raise NotImplementedError('gmKriger does not currently support {} for continental events.'.format(self.gmim))

		elif self.gmim_tag in [2,3]:

			if self.tectonic.lower() == 'crustal' and self.region.lower() != 'japan':
				self.nGMM = 1
				self.GMMs = {
							'cb19': gmms.CampbellBozorgnia2019.CampbellBozorgnia2019,
							}
				self.weight = {
							'cb19': 1,
							}

			else:
				self.nGMM = 1
				self.GMMs = {
							'fpg15': gmms.FoulserPiggottGoda2015.FoulserPiggottGoda2015,
							}
				self.weight = {
							'fpg15': 1,
							}

		elif self.gmim_tag == 4:

			if self.tectonic.lower() == 'crustal' and self.region.lower() != 'japan':
				self.nGMM = 1
				self.GMMs = {
							'cb11': gmms.CampbellBozorgnia2011.CampbellBozorgnia2011,
							}
				self.weight = {
							'cb11': 1,
							}

			else:
				self.nGMM   = 1
				self.GMMs   = {}
				self.weight = 1
				raise NotImplementedError('gmKriger does not currently support {} for non-crustal events.'.format(self.gmim))

