""" Ground motion Kriger: Helpers
"""

import numpy as np
import geostats
import gmms

__author__ = 'A. Renmin Pretell Ductram'


def make_array(my_list):
	
	vals = []
	for val in zip(my_list):
		if isinstance(val[0],np.ndarray):
			vals.append(val[0])
		elif isinstance(val[0], (int, float)):
			vals.append(np.array([float(val[0])]))
		elif isinstance(val[0], (list, tuple)):
			vals.append(np.array(val[0], dtype=float))
		else:
			vals.append(val[0])
	return vals


def select_backend(backend='python'):   
	geostats.geostats_tools.select_backend(backend)
	geostats.build_Mrho.select_backend(backend)
	gmms.distancetools.select_backend(backend)

def get_backends():
	return	{"geostats_tools": geostats.geostats_tools.get_backend(),
			"build_Mrho": geostats.build_Mrho.get_backend(),
			"gmms_distancetools": gmms.distancetools.get_backend()}