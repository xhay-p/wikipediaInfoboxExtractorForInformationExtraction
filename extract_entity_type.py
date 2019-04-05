import pickle
import sys
import csv
from infoboxes_list import *
from dump import *


def get_coarse_type(f_type):
	if f_type != None:
		if f_type in Person_infoboxes:
			return 'Person'
		elif f_type in Location_infoboxes:
			return 'Location'
		elif f_type in Organization_infoboxes:
			return 'Organization'
		#elif f_type in Miscllaneous_infoboxes:
			#return 'Misc'
		else:
			return None

def get_fine_type(infobox):
	try:
		if infobox['Infobox'] == 'musical artist':
			if infobox['background'] == 'group_or_band':
				return 'musical group or band'
			else:
				return infobox['Infobox']	
		else:
			return infobox['Infobox']
	except Exception as e:
		return None

coarse_count = dict()
fine_count = dict()

if __name__ == '__main__':
	entitype_dict = dict()
	infoboxDictionary = sys.argv[1]
	infoboxes = pickle.load(open(infoboxDictionary, "rb"))
	for key, val in infoboxes.items():
		entitype_dict[key] = dict()
		entitype_dict[key]['id'] = val['id']
		fine = get_fine_type(val['infobox'])
		entitype_dict[key]['fine'] = fine
		coarse = get_coarse_type(fine)
		entitype_dict[key]['coarse'] = coarse
		if coarse != None:
			#print(key, fine, coarse)
			if fine not in fine_count:
				fine_count[fine] = 1
			else:
				fine_count[fine] += 1
			if coarse not in coarse_count:
				coarse_count[coarse] = 1
			else:
				coarse_count[coarse] += 1


	dump_dictionary('entity_types.pickle', entitype_dict)
	
	dump_dictionary_csv("fineTypeStats.csv", fine_count)
	dump_dictionary_csv("coarseTypeStats.csv", coarse_count)
	