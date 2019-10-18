# Information Extarction from Wikipedia Infobox
Using the extracted information for generating Knowledge Graph for Person, Organization, and Location entities

### Important Files

1. canonicalXXXXXXX.csv ----->  list infobox relations mapped to their canonical names.

2. infoboxes_list.py -----> list of infobox template for Person, Organization and Location.

3. convertInfoboxToDictionary.py -----> support file for extract_all.py, file converts extracted infobox test into a dictionary where, 									key : information type
									value : information value

4. getCompleteInfobox.py -----> helper file for extract_all.py and convertInfoboxToDictionary.py

5. dump.py -----> helper file to dump pickle dictionary and dictionary into csv file.

6. extract_all.py -----> extract all required information from a wikipedia xml dump. <br>
	input : wikipedia xml dump <br>
	output : dictionary :: 
	1. all.pickle <br>
		key - title <br>
		value - dictionary with following keys: id(value : wikipedia id), fine_type(entity)(value : infobox template type), coarse_type(entity)(value : person or organization or location), man_relation(value : list of canonicalized relation name, selected from the ones manually chosen(canonicalXXXXXXX.csv)), link_relation(value : list of relation names, where the other value is also linked to a wikipedia page) <br>
	2. triples.pickle <br>
		key - title <br>
		value - list of relation triples based on link_relations <br>
	3. reirects.pickle <br>
		key - title <br>
		value - redirect page title <br>

5. extract_entity_type.py -----> helper file for extract_all.py
								returns coarse_type and fine_type from infobox dictionary

6. extract_manual_relations.py -----> helper file for extract_all.py
								returns list of canonicalized relation name from infobox dictionary

7. extract_links_triples.py -----> helper file for extract_all.py
								returns list of linked relation name and list of linked relation tuples from infobox dictionary

### Requirements
1. Python3

### Execute

```
python3 extract_all.py {location of wikipedia xml dump}
```
