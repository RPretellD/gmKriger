""" Ground motion Kriger: Helpers
"""

import numpy as np

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
