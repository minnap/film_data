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

column_headers = prints[0]
initial_columns = max(len(row) for row in prints)
if initial_columns > len(column_headers):
    for number in range(0,(initial_columns - len(column_headers))):
        column_headers.append('')

filmlist = []
for record in prints:
    namelist = []
    for director in record[2].replace(' and ', ', ').replace(' & ', ', ').split(', '): #is there a better option than stringing together .replace?
        if director in names:
            record.append(director)

for record in prints:
    if len(record) > initial_columns: # assumes that any columns beyond the initial columns from csv of prints are because of potentially female names identified
        filmlist += [record]

final_columns = max(len(row) for row in filmlist)
for number in range(0,(final_columns - len(column_headers))):
        column_headers.append('potentially female name')
        
csv_file = 'potential_womens_films.csv'

with open(csv_file, 'wb') as output:
        output.write(codecs.BOM_UTF8)
        writer = csv.writer(output, quoting=csv.QUOTE_ALL,quotechar='"')
        #writer.writerows(gender_lister(person_dicter(csv_names(filename)), 'female'))
        writer.writerows([column_headers])
        writer.writerows(filmlist)
