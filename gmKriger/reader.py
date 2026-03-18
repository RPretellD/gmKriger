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
    
	cwd = os.path.dirname(os.path.abspath(__file__))

	with open(os.path.join(cwd,'data','{}.json'.format(earthquake)), 'r') as f:
		data = json.load(f)

	stlat = data['wer'][gmim.lower()]['lat']
	stlon = data['wer'][gmim.lower()]['lon']
	stval = data['wer'][gmim]
	elat  = data['hypocenter']['hypo_lat']
	elon  = data['hypocenter']['hypo_lon']
	sill  = data['sill'][gmim]
	eta   = data['eta'][gmim]

	if model.lower() == 'realizations':
		Nmodel = 1000
		LE     = data['rho_rea'][gmim]['le']
		gammaE = data['rho_rea'][gmim]['ge']
		LA     = data['rho_rea'][gmim]['la']

	elif model.lower() == 'map':
		Nmodel = 1
		LE     = data['rho_map'][gmim]['le']
		gammaE = data['rho_map'][gmim]['ge']
		LA     = data['rho_map'][gmim]['la']

	else:
		raise NotImplementedError('gmKriger does not currently support this "model" option.')

	params = [*data['hypocenter'].values()]
	region = data['region']
	if region not in ['california','china','italy','japan','taiwan','turkey']:
		region = 'global'
	if earthquake in ['2023 M7.8 Pazarcik', '2023 M7.7 Kahramanmaras', '2023 M6.8 Nurdagi', '2023 M6.3 Yayladagi']:
		region = 'global'
	eparams = sum([[earthquake],[data['M']],params,[data['tectonic']], [region]],[])
	event   = Event(*eparams)
	
	fparams = [*data['fault'].values()]
	fparams = make_array(fparams)
	fault   = Fault(*fparams)

	return stlat,stlon,stval,elat,elon,event,fault,sill,eta,Nmodel,LE,gammaE,LA
