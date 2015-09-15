import csv 
import codecs

def namelist(filename, splitter):
    filetext = open(filename, 'r')
    names = []
    for line in filetext:
        #print line
        item = line.strip().split(splitter)
        if len(item[0].split()) > 1: #exclude single names; address inverted names when producing initial text files
            names += item
        #print '\n'
    return list(set(names))
        
female_names = namelist('female_names.txt', ',')
#print female_names
remove_names = namelist('remove_names.txt', ',') #note that this can include corporate names and other false positives
#print remove_names

print str(len(female_names)) + ' female names'

def write_file(yes_list, filename):
        
    outfile = open(filename, 'wb')
    outfile.write('\r\n'.join(yes_list))
    
    print str(len(yes_list)) + ' names written to file: ' + filename
    print "Caveat: Obviously we don't know for sure who in this list is actually *actually* female-identified."

def remove_values_from_list(yes_list, no_list):
   return [value.strip() for value in yes_list if value.strip() not in no_list]

actually_female_names = remove_values_from_list(female_names, remove_names)

print str(len(female_names)-len(actually_female_names)) + ' names removed. \n'

write_file(actually_female_names, 'potentially_actually_female_names.txt')
