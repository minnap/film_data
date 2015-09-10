from genderize import Genderize
import pycountry
import csv
import codecs
from shutil import copyfile

def gender_lister(people, target_gender='', default_country='', default_language=''):
    gender_list = []
    female_names = []
    male_names = []
    awesome_names = []
    for person in people: # analyzes first name only
        
        #print person
        
        country = ''
        language = ''
        #print person 
        #print type(person)
        if isinstance(person, str):
            name = person
            firstname = person.split(' ')[0] # get first name in multi-part name
            country = default_country
            language = default_language
        elif isinstance(person, list):
            name = person[0]
            firstname = person[0].split(' ')[0]
        else:
            name = person['name']
            firstname = person['name'].split(' ')[0] #assume default type is dict
            #if person['country']:
                #country = person['country']
            if len(person['country']) > 2: # if person data includes a country name (longer than a 2-character ISO code)
                try:
                    country = pycountry.languages.get(name=person['country']).alpha2 # get the ISO code
                    # it's possible to use capitalize() here  
                except:
                    pass
            elif len(person['country']) == 2: # if person data includes a country ISO code
                country = person['country']
            if len(person['language']) > 2: # if person data includes a language (longer than a 2-character ISO code)
                try:
                    country = pycountry.countries.get(name=person['language']).iso639_1_code # get the ISO code
                except:
                    pass
            elif len(person['language']) == 2: # if person data includes a country ISO code
                language = person['language']
        # TO DO: figure out why typechecking doesn't seem to work for dicts here
        if '.' in firstname: #weed out initials, which yield false positives
            abbreviated_names += [person.values()]
            #print person
        else:
            result = Genderize().get([unicode(firstname.strip(), 'latin1')], country_id=country, language_id=language)[0]
            # print result
            gender = result['gender']
            if not gender and (country or language): # if country/language paramaters were used, try again without
                # while this may reduce accuracy, it will fetch a larger set of potentially gendered names
                # which is fine for the purposes of our project
                # print 'retrying ' + person['name'] + ' without language or country'
                result = Genderize().get([firstname])[0]
                gender = result['gender']
            if gender:
            #    print name + " is probably " + gender
                gender_list += [[name, result['probability'], gender]]
                if gender == 'female':
                    female_names += [[name, result['probability']]]
                if gender == 'male':
                    male_names += [[name, result['probability']]]
            else: # null gender or low probability
            #    print "Not sure about " + name
                awesome_names += [name]
                gender_list += [[name, '', 'awesome']]
    
    #print abbreviated_names
    
    save_ambiguous_names('test.csv', abbreviated_names)
    
    if target_gender == 'female':
        return female_names
    elif target_gender == 'male':
        return male_names
    elif target_gender == 'awesome':
        return awesome_names
    else:
        return gender_list # returns list of lists

def person_dicter(name_list): # name list should consist of a list of lists, where each list is [name, country, language]
    people = []
    for name in name_list:
        country = ''
        language = ''
        if name[1]:
            country = name[1].strip()
        if name[2]:
            language = name[2].strip()
        if ', ' in name[0] and not ' and ' in name[0]:
            for subname in name[0].split(', '):
                person = {'name':subname.strip(), 'language':language, 'country':country}
                people += [person]
        elif ' and ' in name[0] and not ', ' in name[0]:
            for subname in name[0].split('and'):
                person = {'name':subname.strip(), 'language':language, 'country':country}
                people += [person]
        else:   
            person = {'name':name[0].strip(), 'language':language, 'country':country}
            #person = {unicode(name[0], 'latin1')}
            people += [person]
    
    return people

def csv_names(filename):
    directors = []

    with open(filename, 'rU') as csvfile:
    #with codecs.open(filename,'r','latin1') as csvfile:
        #sniff to find the format
        #fileDialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        #create a CSV reader
        myReader = csv.reader(csvfile, quotechar='"', delimiter = ',')
        #read each row
        for row in myReader:
            directors += [row]
    
    print "At least " + str(len(directors)) + " directors' names are in this file."
    print 'Up to 1000 names can be genderized per day.'
    
    if str(len(directors)) < 1000:
        batch_size_default = str(len(directors))
    else:
        batch_size_default = 1000
    
    batch_size = int(raw_input('How many names do you want to genderize now? ') or batch_size_default) 
    
    truncated_person_list = directors[0:batch_size]
    
    save_leftovers(directors,batch_size)
    
    return truncated_person_list

def save_leftovers(directors, range_start):
    csv_file = filename.replace(".csv", "_leftovers.csv")

    with open(csv_file, 'wb') as output:
        output.write(codecs.BOM_UTF8)
        writer = csv.writer(output, quoting=csv.QUOTE_ALL,quotechar='"')
        #writer.writerows(gender_lister(person_dicter(csv_names(filename)), 'female'))
        writer.writerows(directors[range_start:])
        
    print csv_file, 'has been created. It contains ' + str(len(directors[range_start:])) + ' directors whose names were not processed in this batch.'


def save_ambiguous_names(filename, names):
    
    #write a separate file of abbreviated names

    csv_file = filename.replace(".csv", "_abbreviated_names.csv")

    with open(csv_file, 'wb') as output:
        output.write(codecs.BOM_UTF8)
        writer = csv.writer(output, quoting=csv.QUOTE_ALL,quotechar='"')
        #writer.writerows(gender_lister(person_dicter(csv_names(filename)), 'female'))
        #writer.writerows(gender_lister(person_dicter(csv_names(filename))))
        #writer.writerows([csv_headers])
        writer.writerows(names)
    
    print csv_file + ' has been created. It contains ' + str(len(names)) + ' directors whose ambiguous names were not processed in this batch.' 

#filename = 'directors.csv'

# user options:

target_gender = raw_input('The default output will include all names and their genders. Please enter a binary gender ("male", "female") to get a filtered list of names: ') or ''

filename = raw_input('Enter a filename for processing: ') or 'directors.csv'

csv_file = raw_input('The default output file will be ' + filename.replace(".csv", "_" + target_gender + ".csv") + '; enter a filename to override: ') or filename.replace(".csv", "_" + target_gender + ".csv")

csv_headers = ['name', 'probability']

if target_gender != 'awesome':
        csv_headers += ['gender']

# okay do the thing:
        
gender_list = gender_lister(person_dicter(csv_names(filename)), target_gender)

with open(csv_file, 'wb') as output:
    output.write(codecs.BOM_UTF8)
    writer = csv.writer(output, quoting=csv.QUOTE_ALL,quotechar='"')
    #writer.writerows(gender_lister(person_dicter(csv_names(filename)), 'female'))
    #writer.writerows(gender_lister(person_dicter(csv_names(filename))))
    writer.writerows([csv_headers])
    writer.writerows(gender_list)    

print csv_file, 'has been created. It contains ' + str(len(gender_list)) + ' ' + target_gender + ' directors whose names were processed in this batch.'
