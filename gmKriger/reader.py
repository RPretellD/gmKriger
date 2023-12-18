""" Ground motion Kriger: Reader
"""

import os
import numpy as np
import json
from .core import Event
from .core import Fault
from .helpers import make_array

__author__ = 'A. Renmin Pretell Ductram'


def read_data(earthquake,gmim,model):
	
	with open(os.path.join(os.path.abspath(__file__).split('reader.py')[0],'Data','{}.json'.format(earthquake)), 'r') as f:
		data = json.load(f)
	
	stlat = np.array(data['WER']['lat_'+gmim.lower()])
	stlon = np.array(data['WER']['lon_'+gmim.lower()])
	stval = np.array(data['WER'][gmim])
	elat  = data['hypocenter']['hypo_lat']
	elon  = data['hypocenter']['hypo_lon']
	sill  = data['sill'][gmim]
	eta   = data['eta'][gmim]
	
	if model.lower() == 'realizations':
		Nmodel = 1000
		LE     = np.array(data['model']['all'][gmim]['le'])
		gammaE = np.array(data['model']['all'][gmim]['gammae'])
		LA     = np.array(data['model']['all'][gmim]['la'])
	
	elif model.lower() == 'map':
		Nmodel = 1
		LE     = np.array([data['model']['map'][gmim]['le']])
		gammaE = np.array([data['model']['map'][gmim]['gammae']])
		LA     = np.array([data['model']['map'][gmim]['la']])
	
	elif model.lower() == 'all':
		Nmodel = 1001
		LE     = np.array(data['model']['all'][gmim]['le'])
		LE     = np.append(LE,data['model']['map'][gmim]['le'])
		gammaE = np.array(data['model']['all'][gmim]['gammae'])
		gammaE = np.append(gammaE,data['model']['map'][gmim]['gammae'])
		LA     = np.array(data['model']['all'][gmim]['la'])
		LA     = np.append(LA,data['model']['map'][gmim]['la'])

	params = [*data['hypocenter'].values()]
	region = data['region']
	if region not in ['california','china','italy','japan','taiwan','turkey']:
		region = 'global'
	if earthquake in ['2023 M7.8 Pazarcik', '2023 M7.7 Kahramanmaras', '2023 M6.8 Nurdagi', '2023 M6.3 Yayladagi']:
		region = 'global'
	params = sum([[earthquake],[data['M']],params,[data['tectonic']], [region]],[])
	event = Event(*params)

	params = [*data['fault'].values()]
	params = make_array(params)
	fault  = Fault(*params)
	
	return stlat,stlon,stval,elat,elon,event,fault,sill,eta,Nmodel,LE,gammaE,LA
