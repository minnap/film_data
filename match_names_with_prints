import csv 
import codecs

filename = 'female_names.txt'
filetext = open(filename, 'r')
names = []
for line in filetext:
    item = line.strip().split(',')
    names += item
    
filename = 'titles_directors.csv'
prints = []
with open(filename, 'rU') as csvfile:
    #with codecs.open(filename,'r','latin1') as csvfile:
        #sniff to find the format
        #fileDialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        #create a CSV reader
        myReader = csv.reader(csvfile, quotechar='"', delimiter = ',')
        #read each row
        for row in myReader:
            prints += [row]

filmlist = []
for record in prints:
    namelist = []
    for director in record[2].replace(' and ', ', ').split(', '):
    #    print director.split()
        #print director
        if director in names:
            record.append(director)
    #for name in names:
    #   if name in record[2]:
    #       namelist += [name]
    #if len(namelist) > 0 and record not in filmlist:
    #   record += [(', ').join(namelist)]
    #   filmlist += [record]
    #   print record

for record in prints:
    if len(record) > 6: #assumes a 6-column csv to begin with
        filmlist += [record]
        
csv_file = 'potential_womens_films.csv'

with open(csv_file, 'wb') as output:
        output.write(codecs.BOM_UTF8)
        writer = csv.writer(output, quoting=csv.QUOTE_ALL,quotechar='"')
        #writer.writerows(gender_lister(person_dicter(csv_names(filename)), 'female'))
        writer.writerows([['item number', 'original title', 'director(s)', 'language', 'country', 'year', 'potential women']])
        writer.writerows(filmlist)
