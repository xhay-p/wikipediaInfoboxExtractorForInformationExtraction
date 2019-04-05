import pandas as pd
import sys
import pickle
import csv
from infoboxes_list import *
from dump import *
def load_canonical_rel_dict(filename):
	return pd.read_csv(filename, header=None, index_col=0, squeeze=True).to_dict()

#relation dictionary, where infobox entry is mapped with canonical relation names
person_rel = load_canonical_rel_dict('cannonicalPerson.csv')
location_rel = load_canonical_rel_dict('cannonicalLocation.csv')
organization_rel = load_canonical_rel_dict('cannonicalOrganization.csv')

per_rel_count = dict()
loc_rel_count = dict()
org_rel_count = dict()

def get_relations_list(infobox, coarse=None):
	relations = list()
	try:
		#if infobox['Infobox'] in Person_infoboxes:
		if coarse == 'Person':
			for rel in infobox.keys():
				if rel in person_rel.keys():
					relations.append(person_rel[rel])
					if person_rel[rel] not in per_rel_count:
						per_rel_count[person_rel[rel]] = 1
					else:
						per_rel_count[person_rel[rel]] += 1
		#elif infobox['Infobox'] in Location_infoboxes:
		elif coarse == 'Location':
			for rel in infobox.keys():
				if rel in location_rel.keys():
					relations.append(location_rel[rel])
					if location_rel[rel] not in loc_rel_count:
						loc_rel_count[location_rel[rel]] = 1
					else:
						loc_rel_count[location_rel[rel]] += 1
		#elif infobox['Infobox'] in Organization_infoboxes:
		elif coarse == 'Organization':
			for rel in infobox.keys():
				if rel in organization_rel.keys():
					relations.append(organization_rel[rel])
					if organization_rel[rel] not in org_rel_count:
						org_rel_count[organization_rel[rel]] = 1
					else:
						org_rel_count[organization_rel[rel]] += 1
		return relations
	except:
		return relations
	
if __name__ == '__main__':
	manrel_dict = dict()
	infoboxDictionary = sys.argv[1]
	infoboxes = pickle.load(open(infoboxDictionary, "rb"))
	for key, val in infoboxes.items():
		manrel_dict[key] = get_relations_list(val['infobox'])
		#if len(manrel_dict[key]):
			#print(key, manrel_dict[key])

	dump_dictionary("manual_relations.pickle", manrel_dict)
	
	dump_dictionary_csv("RelationStatsPerson.csv", per_rel_count)
	dump_dictionary_csv("RelationStatsOrganization.csv", org_rel_count)
	dump_dictionary_csv("RelationStatsLocation.csv", loc_rel_count)