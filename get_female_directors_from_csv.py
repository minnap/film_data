from genderize import Genderize
import pycountry
import csv
import codecs

def gender_lister(people, target_gender='', default_country='', default_language=''):
    gender_list = []
    female_names = []
    male_names = []
    awesome_names = []
    for person in people: # analyzes first name only
        country = ''
        language = ''
        #print person 
        #print type(person)
        if isinstance(person, str):
            name = person
            firstname = person.split(' ')[0]
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
        #print firstname + ', ' + country + ', ' + language
        #result = Genderize().get([firstname], country_id=country, language_id=language)[0]
        result = Genderize().get([unicode(firstname, 'latin1')], country_id=country, language_id=language)[0]
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
        else: # null gender
        #    print "Not sure about " + name
            awesome_names += [name]
            gender_list += [[name, '', 'awesome']]
    
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
        person = {'name':name[0]}
        #person = {unicode(name[0], 'latin1')}
        if name[1]:
            person['country'] = name[1]
        else: 
            person['country'] = ''
        if name[2]:
            person['language'] = name[2]
        else: 
            person['language'] = ''
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
    
    return directors

filename = "directors.csv" # to do: allow user to choose file

csv_file = filename.replace(".", "_genderized.") 
csv_headers = ["name", "probabability", "gender"] # to do: modify headers to reflect target gender or lack thereof

with open(csv_file, 'wb') as output:
    output.write(codecs.BOM_UTF8)
    writer = csv.writer(output, quoting=csv.QUOTE_ALL,quotechar='"')
    #writer.writerows(gender_lister(person_dicter(csv_names(filename)), 'female'))
    writer.writerows(gender_lister(person_dicter(csv_names(filename)))) # to do: incorporate user input for target gender
        
print csv_file, 'has been created'