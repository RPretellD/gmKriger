""" Ground motion Kriger: Main
"""

import os
import numpy as np
import pandas as pd
import geostats
from .reader import read_data
from .core import Site, GMM_gmIM
from .helpers import make_array, select_backend

__author__ = 'A. Renmin Pretell Ductram'


def get_Kgmim(ID,lat,lon,Vs30,earthquake,model,gmim,backend="Cython"):
	
	"""
	ID: Site name(s)
	lat: Site latitude(s)
	lon: Site longitude(s)
	Vs30: Site Vs30 value(s)
	Earthquake name: See list by using "gmKriger.models()"
	model: Correlation model, either "Realizations", or "MAP" for maximum a-posteriori. 
	gmim: Ground motion intensity measure. See list by using "gmKriger.models()"
	"""
    
	select_backend(backend)
    
	pd.set_option('display.precision', 6)
    
	cwd    = os.path.dirname(os.path.abspath(__file__))
	models = pd.read_csv(os.path.join(cwd,'data','models.csv'))
	gmims  = models.columns[1:]
	gmim   = gmim.lower()

	if gmim not in gmims:
		raise NotImplementedError('gmKriger does not currently support the requested ground motion IM.')

	ind1 = earthquake in models['earthquake'].values
	ind2 = 0

	if ind1:
		ind2 = models[models['earthquake']==earthquake][gmim].values[0]

	if not ind1:
		raise NotImplementedError('No correlation models currently available for {}.'.format(earthquake))

	elif ind1 and ind2 == 0:
		raise NotImplementedError('No {} correlation models currently available for {}'.format(gmim,earthquake))

	else:
		get_label1 = dict(zip(['pga','pgv','cav','ia','psa(0.100)','psa(0.300)','psa(0.600)','psa(1.000)','psa(3.000)','psa(6.000)','psa(10.000)','cavdp'],
							['PGA (g)','PGV (cm/s)','CAV (m/s)','Ia (m/s)','PSA(0.100) (g)','PSA(0.300) (g)','PSA(0.600) (g)','PSA(1.000) (g)','PSA(3.000) (g)','PSA(6.000) (g)','PSA(10.000) (g)','CAVdp (g-s)']))
		get_label2 = dict(zip(['pga','pgv','cav','ia','psa(0.100)','psa(0.300)','psa(0.600)','psa(1.000)','psa(3.000)','psa(6.000)','psa(10.000)','cavdp'],
							['PGA','PGV','CAV','Ia','PSA(0.100)','PSA(0.300)','PSA(0.600)','PSA(1.000)','PSA(3.000)','PSA(6.000)','PSA(10.000)','CAVdp']))
		label1 = get_label1[gmim]
		label2 = get_label2[gmim]

		if isinstance(ID, str):
			ID = [ID]

		[lat,lon,Vs30] = make_array([lat,lon,Vs30])
		if not len(ID)==len(lat)==len(lon)==len(Vs30):
			raise NotImplementedError('Unequal length of input.')
		else:
			Nsites = len(lat)

		# Get data
		[stlat,stlon,stval,elat,elon,event,fault,sill,eta,Nmodel,LE,gE,LA] = read_data(earthquake,gmim,model)

		# Sampling a station
		sco  = pd.DataFrame(zip(lat,lon),columns=['lat','lon'])
		stco = pd.DataFrame(zip(stlat,stlon),columns=['lat','lon'])
		idx  = np.array(sco[sco.isin(stco.to_dict(orient='list')).all(axis=1)].index.tolist())

		# Ground motion
		fault.get_URC()
		fault.get_rfault()
		fault.get_fstyle()

		GMMs_eu = GMM_gmIM(gmim,event)
		gmms    = GMMs_eu.GMMs
		gmm_w   = GMMs_eu.weight
		Ngmms   = GMMs_eu.nGMM

		site = Site(lat, lon, Vs30, Z1p0=None, Z2p5=None)
		site.get_distances(fault)
		site.get_gmim(event, fault, gmim, gmms)
		# print(site.gmmIM_mu)
		# print(site.Vs30_raw)
		# print(site.Vs30)
		# print(site.Z1p0)
		# print(site.Z2p5)
		# Kriging
		out_mu = np.zeros([Ngmms,Nmodel,Nsites])
		out_va = np.zeros([Ngmms,Nmodel,Nsites])

		for i,gmm in enumerate(gmms.keys()):

			for j in range(Nmodel):
				cmodel    = geostats.Model('ea',LE[gmm.lower()][j],gE[gmm.lower()][j],L_A=LA[gmm.lower()][j])
				sampled   = geostats.Site(stlat,stlon,value=stval[gmm.lower()])
				unsampled = geostats.Site(lat,lon)
				Kriger    = geostats.Kriging(sampled,unsampled,sill[gmm.lower()],cmodel,elat,elon)
				out       = Kriger.Krige('ordinary')

				out_mu[i,j,:] = np.array(out.mean)
				out_va[i,j,:] = np.array(out.variance)

			if len(idx) > 0:
				out_va[i,j,:][idx] = 0

		# Ground motion intensity measure
		eta_arr   = np.tile(np.array(list(eta.values())),(site.Nsites, 1))
		gmm_w_arr = np.tile(np.array(list(gmm_w.values())),(site.Nsites, 1))

		K_WER_mean = np.mean(out_mu,axis=1).T
		K_WER_std  = np.sqrt(np.mean(out_va,axis=1)+np.std(out_mu,axis=1)**2).T
		K_IM_mu    = np.exp(site.gmmIM_mu+eta_arr+K_WER_mean)
        
        
		mu_p = np.log(K_IM_mu) * gmm_w_arr
		mu_p = np.sum(mu_p,axis=1)
		mu_p = np.exp(mu_p)

		sigma_p  = (K_WER_std**2)*gmm_w_arr
		sigma_p += (np.log(K_IM_mu)**2-np.log(mu_p[:, None])**2)*gmm_w_arr
		sigma_p  = np.sum(sigma_p,axis=1)
		sigma_p  = sigma_p**0.5

		df_out = pd.DataFrame(zip(ID,lat,lon,mu_p,sigma_p),columns=['Site','Lat (deg)', 'Lon (deg)',label1,'sigma_{} (ln)'.format(label2)])

	return df_out


def models():
	cwd    = os.path.dirname(os.path.abspath(__file__))
	models = pd.read_csv(os.path.join(cwd,'data','models.csv'))
	models.replace(1, 'Yes', inplace=True)
	models.replace(0, 'No', inplace=True)
	return models
