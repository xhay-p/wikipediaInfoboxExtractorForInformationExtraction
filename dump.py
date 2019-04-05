import csv
import pickle

def dump_dictionary(fileName, dictionaryName):
	print("dumping  "+fileName)
	with open(fileName, 'wb') as handle:
		pickle.dump(dictionaryName, handle, protocol=pickle.HIGHEST_PROTOCOL)

def dump_dictionary_csv(fileName, dictionaryName):
	with open(fileName, "w+") as csv_file:
		writer = csv.writer(csv_file)
		for key, val in dictionaryName.items():
			writer.writerow([key, val])