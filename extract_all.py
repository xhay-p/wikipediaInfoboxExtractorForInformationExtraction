import xml.etree.ElementTree as etree
import codecs
import csv
import time
import os
import re
import sys
import json
import pickle

from convertInfoboxToDictionary import *
from getCompleteInfobox import *
from extract_links_triples import *
from extract_manual_relations import *
from extract_entity_type import *


# Nicely formatted time string
def hms_string(sec_elapsed):
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = sec_elapsed % 60
    return "{}:{:>02}:{:>05.2f}".format(h, m, s)



def strip_tag_name(t):
    t = elem.tag
    idx = k = t.rfind("}")
    if idx != -1:
        t = t[idx + 1:]
    return t



#function to add entries entries into wiki_dict
wiki_dict = dict()
def add_to_wiki_dict(title,item_name,item_val):
    wiki_dict[title][item_name] = item_val

#function to add triples to triples_dict
triple_dict = dict()
def add_to_triples_dict(title,item_name,item_val):
    triple_dict[title][item_name] = item_val

#mapping for redirect page with it's original page
redirect_dict = dict()

pathWikiXML = sys.argv[1]


totalCount = 0
title = None
start_time = time.time()

for event, elem in etree.iterparse(pathWikiXML, events=('start', 'end')):
    tname = strip_tag_name(elem.tag)
    if event == 'start':
        if tname == 'page':
            title = ''
            id = -1
            redirect = ''
            inrevision = False
            ns = 0
        elif tname == 'revision':
            # Do not pick up on revision id's
            inrevision = True
    else:
        if tname == 'title':
            title = elem.text
        elif tname == 'id' and not inrevision:
            id = int(elem.text)
        elif tname == 'redirect':
            redirect = elem.attrib['title']
        elif tname == 'ns':
            ns = int(elem.text)
        elif tname == 'text':
            raw_text = elem.text
            if type(raw_text) == str:
                #Search for start position of '{{Infobox'
                raw_text = raw_text.replace("infobox","Infobox")
                start_tags = ["{{Infobox"]
                for tag in start_tags:
                    start_info = raw_text.find(tag)
                    if start_info != -1:
                        break
                if start_info != -1:
                    #take text starting from infobox
                    text = raw_text[start_info:]
                    #call function to get complete infobox from raw_text 
                    infobox_raw, length = parenthesis_match(text)
                    #call function to convert infobox text to dictionary
                    #print("############TITLE=" + title + "#############")
                    infobox = convert_to_dict(infobox_raw)
                else : 
                    infobox = None
                    infobox_raw = None
        # writing starts after xml parser finds start of new page
        elif tname == 'page':
            totalCount += 1
#           print(id, title, redirect)
            if totalCount%10000 == 0:
                print(totalCount)
            
            #redirects and original page dictionary
            if len(redirect) > 0:
                redirect_dict[title] = redirect.replace(' ', '_')
#                print(title, redirect_dict[title])
            wiki_dict[title] = dict()
            triple_dict[title] = dict()
            #adds id to dictionary
            add_to_wiki_dict(title, 'id', id)
            add_to_triples_dict(title, 'id', id)
            #adds infobox dictionary to dictionary
            #add_to_wiki_dict(title, 'infobox', infobox)
            #extracts fine type of entity
            f_type = get_fine_type(infobox)
            #adds f_type to dictionary
            add_to_wiki_dict(title, 'fine_type', f_type)
            #extracts coarse type of entity
            c_type = get_coarse_type(f_type)
            #adds c_type to dictionary
            add_to_wiki_dict(title, 'coarse_type', c_type)
            add_to_triples_dict(title, 'coarse_type', c_type)
            #extracts relations
            rel_lst = get_relations_list(infobox, c_type)
            #adds manually extracted relations list to dictionary
            add_to_wiki_dict(title, 'man_relations', rel_lst)
            
            linked_tuple_list = get_link_tuples_list(infobox)
            #adds links to dictionary
            #add_to_wiki_dict(title, 'links', linked_tuple_list)
            #extracts linked relation list and also extracts tuples and save them
            link_rel_lst, triple_list = get_triples_list(title, linked_tuple_list) 
            #adds manually extracted relations list to dictionary
            add_to_wiki_dict(title, 'link_relations', link_rel_lst)
            add_to_triples_dict(title, 'triples', triple_list)
#            print(id, title, f_type, c_type, rel_lst)
        elem.clear()
print("Dumping Infobox Dictionary............")
dump_dictionary('all.pickle', wiki_dict)
print("Dumping triples Dictionary............")
dump_dictionary('triples.pickle', triple_dict)
print("Dumping redirects Dictionary..........")
dump_dictionary('redirects.pickle', redirect_dict)


elapsed_time = time.time() - start_time
print("Total pages: {:,}".format(totalCount))
print("Time taken:{:.2f}".format(elapsed_time))
