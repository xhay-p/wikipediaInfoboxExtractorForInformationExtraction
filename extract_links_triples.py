import re
import sys
import pickle
from dump import *

def get_link_tuples_list(infobox):
	links = list()
	try:
		if infobox != 'NA':
			for entry in infobox:
				#preprocessing entry also.
				#remove \n| from string
				entry = re.sub(r"\n\|",r"|vi",entry)
				#remove text between <ref>....</ref>
				entry = re.sub(r"<ref>.*?</ref>",r"",entry)
				entry = re.sub(r"<ref.*?>",r"",entry)
				#take out raw string of entry for processing
				raw_string = infobox[entry]
				#remove \n| from string
				raw_string = re.sub(r"\n\|",r"|vi",raw_string)
				if (len(raw_string)) != 0 and raw_string[-1] == '|':
					raw_string = raw_string[:-1]
				#remove text between <ref>....</ref>
				raw_string = re.sub(r"<ref>.*?</ref>",r"",raw_string)
				raw_string = re.sub(r"<ref.*?>",r"",raw_string)
				#remove additional comments
				if "<br" not in raw_string:
					raw_string = re.sub(r"<.*?>",r"",raw_string)
				# collect all links enclosed in [[]] and append in links (list)
				links_in_entry = re.findall(r"\[\[.*?\]\]",raw_string)
				if links_in_entry != []:
					links.append((entry,links_in_entry))
				#set processed string as new value for entry key
				processed_string = raw_string
				infobox[entry] = processed_string
	except:
		pass			
	
	return links

def clean_links(link):
	#print(link)
	lst = link[1]
	targets = list()
	for i in range(len(lst)):
		lst[i] = lst[i].replace("\n\|","")
		lst[i] = lst[i].replace("vi","")
		if (len(lst[i])) != 0 and lst[i][-1] == '|':
			lst[i] = lst[i][:-1]
			#print(lst[i])
		
		if "<br" in lst[i]:
			lst[i] = re.sub(r"<.*?>",r"",lst[i])

		lst[i] = re.findall(r"\[.*?\]",lst[i])

		for k in range(len(lst[i])):
			a = lst[i][k].find('|')
			lst[i][k]=lst[i][k][:a]
			lst[i][k] = re.sub('[\[\]]+',' ',lst[i][k])
			lst[i][k]=lst[i][k].strip()
			#print(lst[i][k])
			targets.append(lst[i][k])

	#print(targets)	
	#print("---------------------------------------------------------")
	return link[0], targets

def get_triples_list(e1, listOfLinks):
	r_list = list()
	t_list = list()
	for link in listOfLinks:
		r, e2_list = clean_links(link)
		r_list.append(r)
		for e2 in e2_list:
			t_list.append((e1, r, e2))
	return r_list, t_list

if __name__ == '__main__':
	links_dict = dict()
	infoboxDictionary = sys.argv[1]
	infoboxes = pickle.load(open(infoboxDictionary, "rb"))
	for key, val in infoboxes.items():
		links_dict[key] = dict()
		links_dict[key]['id'] = val['id']
		temp = get_link_tuples_list(val['infobox'])
		links_dict[key]['rels'], links_dict[key]['triples'] = get_triples_list(key, temp)
		#if len(links_dict[key]['rels']):
			#print(links_dict[key]['triples'])

	dump_dictionary("linksRelsTriples.pickle", links_dict)