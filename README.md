# Information Extarction from Wikipedia Infobox
## Using the extracted information for generated Knowledge Graph for Person, Organization, and Location entities

canonicalXXXXXXX.csv ----->  list infobox relations mapped to their canonical names.

infoboxes_list.py -----> list of infobox template for Person, Organization and Location.

convertInfoboxToDictionary.py -----> support file for extract_all.py, file converts extracted infobox test into a dictionary where, 									key : information type
									value : information value

getCompleteInfobox.py -----> helper file for extract_all.py and convertInfoboxToDictionary.py

dump.py -----> helper file to dump pickle dictionary and dictionary into csv file.

extract_all.py -----> extract all required information from a wikipedia xml dump.
input : wikipedia xml dump
output : dictionary :: 
	1. all.pickle
		key - title
		value - dictionary with following keys: id(value : wikipedia id), fine_type(entity)(value : infobox template type), coarse_type(entity)(value : person or organization or location), man_relation(value : list of canonicalized relation name, selected from the ones manually chosen(canonicalXXXXXXX.csv)), link_relation(value : list of relation names, where the other value is also linked to a wikipedia page) 
	2. triples.pickle
		key - title
		value - list of relation triples based on link_relations
	3. reirects.pickle
		key - title
		value - redirect page title

extract_entity_type.py -----> helper file for extract_all.py
								returns coarse_type and fine_type from infobox dictionary

extract_manual_relations.py -----> helper file for extract_all.py
								returns list of canonicalized relation name from infobox dictionary

extract_links_triples.py -----> helper file for extract_all.py
								returns list of linked relation name and list of linked relation tuples from infobox dictionary

To run,
(Works only for Python3)
```
python3 extract_all.py {location of wikipedia xml dump}
```
