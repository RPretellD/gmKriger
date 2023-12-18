""" Ground motion Kriger: Main
"""

import os
import numpy as np
import pandas as pd
from .reader import read_data
from .core import Site
from .helpers import make_array
import geostats

__author__ = 'A. Renmin Pretell Ductram'


def get_Kgmim(ID,lat,lon,Vs30,earthquake,model,gmim):
	
	"""
	ID: Site name(s)
	lat: Site latitude(s)
	lon: Site longitude(s)
	Vs30: Site Vs30 value(s)
	Earthquake name: See list by using "gmKriger.show()"
	model: Corelation model, either "All", "Realizations", or "MAP"
	gmim: Ground motion intensity measure. See list by using "gmKriger.show()"
	"""
	
	pd.set_option('display.precision', 6)
	
	cwd  = os.path.abspath(__file__).split('gmKriger.py')[0]
	gmim = gmim.lower()
	
	# Check availability
	models = pd.read_csv(os.path.join(cwd,'Data','models.csv'))
	ind1 = earthquake in models['earthquake'].values
	ind2 = 0
	
	if ind1:
		ind2 = models[models['earthquake']==earthquake][gmim].values[0]
	
	if not ind1:
		print('No correlation models currently implemented for {}.'.format(earthquake))
		return
		
	elif ind1 and ind2 == 0:
		print('No {} correlation models for {}'.format(gmim,earthquake))
		return
	
	else:
		
		# Start
		get_label1 = dict(zip(['pga','pgv','cav','ia','psa(0.3)','psa(0.6)','psa(1.0)','cavdp'],
					['PGA (g)','PGV (cm/s)','CAV (m/s)','Ia (m/s)','PSA(0.3) (g)','PSA(0.6) (g)','PSA(1.0) (g)','CAVdp (g/s)']))
		get_label2 = dict(zip(['pga','pgv','cav','ia','psa(0.3)','psa(0.6)','psa(1.0)','cavdp'],
					['PGA','PGV','CAV','Ia','PSA(0.3)','PSA(0.6)','PSA(1.0)','CAVdp']))
		label1 = get_label1[gmim]
		label2 = get_label2[gmim]
		
		# Check input
		if isinstance(ID, str):
			ID = [ID]
		[lat,lon,Vs30] = make_array([lat,lon,Vs30])
		if not len(ID)==len(lat)==len(lon)==len(Vs30):
			print('Unequal length of input.')
			return
		
		# Get data
		[stlat,stlon,stval,elat,elon,event,fault,sill,eta,Nmodel,LE,gammaE,LA] = read_data(earthquake,gmim,model)
		
		# Sampling a station
		sco  = pd.DataFrame(zip(lat,lon),columns=['lat','lon'])
		stco = pd.DataFrame(zip(stlat,stlon),columns=['lat','lon'])
		idx  = np.array(sco[sco.isin(stco.to_dict(orient='list')).all(axis=1)].index.tolist())
		
		# Kriging
		out_mu,out_va = [[],[]]
		for i in range(Nmodel):
			cmodel    = geostats.Model('ea',LE[i],gammaE[i],L_A=LA[i])
			sampled   = geostats.Site(stlat,stlon,value=stval)
			unsampled = geostats.Site(lat,lon)
			Kriger    = geostats.Kriging(sampled,unsampled,sill,cmodel,elat,elon)
			out       = Kriger.Krige('ordinary')
			out_mu.append(out.mean)
			out_va.append(out.variance)
		out_mu = np.array(out_mu)
		out_va = np.array(out_va)
		if len(idx) > 0:
			for i in range(Nmodel):
				out_va[i,:][idx] = 0
			
		# Ground motion
		fault.get_URC()
		fault.get_rfault()
		fault.get_fstyle()
		site = Site(lat, lon, Vs30, Z1p0=None, Z2p5=None)
		site.get_distances(fault)
		site.get_gmim(event, fault, gmim)

		if np.isnan(site.IM_mu[0]):
			return
		
		# Results
		if model.lower() in ['realizations','map']:
			K_WER_mean = np.mean(out_mu,axis=0)
			K_WER_std  = np.sqrt(np.mean(out_va,axis=0)+np.std(out_mu,axis=0)**2)
			K_IM_mu    = np.exp(site.IM_mu+[eta]*site.Nsites+K_WER_mean)
			df_out     = pd.DataFrame(zip(ID,lat,lon,K_IM_mu,K_WER_std),columns=['Site','Lat (deg)', 'Lon (deg)',label1,'sigma_{} (ln)'.format(label2)])

		else:
			K_WER_mean = np.mean(out_mu[:-1,:],axis=0)
			K_IM_mu    = np.exp(site.IM_mu+[eta]*site.Nsites+K_WER_mean)
			K_WER_std  = np.sqrt(np.mean(out_va[:-1,:],axis=0)+np.std(out_mu[:-1,:],axis=0)**2)
			if len(idx) > 0:
				K_WER_std[idx] = 0
			
			K_WER_mean_map = out_mu[-1,:]
			K_IM_mu_map    = np.exp(site.IM_mu+[eta]*site.Nsites+K_WER_mean_map)
			K_WER_std_map  = out_va[-1,:]**0.5
			
			df_out = pd.DataFrame(zip(ID,lat,lon,K_IM_mu_map,K_WER_std_map,K_IM_mu,K_WER_std),
				columns=['Site','Lat (deg)', 'Lon (deg)','{} - MAP'.format(label1),'sigma_{} (ln) - MAP'.format(label2),label1,'sigma_{} (ln)'.format(label2)])
		
		return df_out

def models():
	models = pd.read_csv(os.path.join(os.path.abspath(__file__).split('gmKriger.py')[0],'Data','models.csv'))
	models.replace(1, 'Yes', inplace=True)
	models.replace(0, 'No', inplace=True)
	return models
