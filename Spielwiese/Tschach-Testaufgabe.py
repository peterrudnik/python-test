'''
Created on 22 Dec 2016

@author: rudnikp
'''

#--------------------------------------------------------------------------------
#  Testaufgabe der Firma ICIS Tschach Solutions GmbH
#  Karlsruhe
#  
#  Autor: Peter Rudnik
#         17.09.2016
#
#  Beschreibung: Es sollen Daten eines Webservices heruntergeladen werden 
#                http://utilitytool.casc.eu/CascUtilityWebService.asmx?op=GetLTNForAPeriod 
#                und in einem CSV format abgespeichert werden
#                like so:
#                "sourceID;utcTimeStamp;locTimeStamp;value
#                1;2015-10-23 22:00:00;2015-10-24 00:00:00;0
#                2;2015-10-23 22:00:00;2015-10-24 00:00:00;000"  
#
#                Naehere Beschreibung zu moeglichen Protokollen und Formaten der Abfrage befinden sich auf der oben angegebenen Webseite:
#                im Prinzip SOAP oder direkt HTTP.
#                Das Ergebnis in XML wird geparst und als csv abgespeichert.
#                Es handelt sich um zeitabhaengige Daten, es muss eine Konvertierung zwischen lokaler Zeit und UTC erfolgen.            
#                Sprache ist Python 2.7 
#                Achtung: Bei den mitgelieferten Sample Daten das Datum: Die Umstellung auf die Winterzeit 2015 war am 25. Oktober 
#
# Stand:         -Es gibt noch Fragen zu den Zeitangaben: welche Zeitangaben (UTC oder lokal CET) verlangt die Webseite und was gibt sie zurueck ?
#                 Von den Angaben scheint es CET zu sein, dass dann uebersetz wird nach UTC
#                 Die mitgelieferte Musterausgabe scheint dann lokale Zeitangaben zu enthalten: Auch 1 Tag lang aber um zwei Stunden zeitvesetzt. Stimmt das?
#                - data validation: seems to be the same data as yields a query through the web site's form, but still look kind of repetitive    
#                - execption handling: necessary? if it is a one off the probable not
#                - better use python 3.x because of better utf-8 support (see comments below)   
#                - Zeitumstellung: bei den Sample Daten hat man einen Datensatz mehr 25 statt 24 wegen der zusaetzlichen Stunde, 2016 erst am 30.10, 
#                  muss aber trotzdem beruecksichtigt werden                
# Issues:            
#                 If we are on a date, when time is reset due to daylight saving time, we need to handle this.
#                 In this case an AmbiguousTimeError is raised: but we still don't know if an hour is added or taken away.
#                 The exception is also raised at the beginning of that day, not accounting for the exact hour of the switch,
#                 but this issue can be dealt with by doing a local Date - UTC data - local date conversion
#                 We handle 2 cases:
#                 1. the case when an hour is added: that would be around October in CET e.g 25.10.2015
#                 2. the case when a hour is lost that would be around March in CET e.g 29.03.2015
#                 for other dates it does not seem to matter
# -------------------------------------------------------------------
# packages
# -------------------------------------------------------------------
import requests
from datetime import datetime, timedelta
import csv, pytz
import xml.etree.ElementTree as ET 
from io import StringIO
from pprint import pprint


# -------------------------------------------------------------------
# definitions
# -------------------------------------------------------------------
    
dateFrom    = "2016-09-13" 
#dateFrom    = "2015-10-25"
#dateFrom    = "2015-03-29" 
dateTo      = dateFrom
timeZone    = pytz.timezone('CET')
utc_timeZone = pytz.timezone('UTC')

# prepare for date time
datefmtIN = '%Y-%m-%dT%H:%M:%S'
datefmtOUT = '%Y-%m-%d %H:%M:%S'
    
fileName    = 'casc_LTN_%(dateFrom)s.csv' % {'dateFrom':dateFrom}
fileNameRawResponseData    = 'casc_LTN_%(dateFrom)s.xml' % {'dateFrom':dateFrom}
#filePath    = "c:\\temp\\"
filePath    = "P:\\temp\\"
#filePath    = "e:\\Development\\projects\\python\\tschach_testaufgabe\\data\\"

    
columnNames = ['sourceID', 'utcTimeStamp', 'locTimeStamp', 'value']
sourceIDs   = {'BEFR':  1, 'BENL':  2, 
               'DEATFR':3, 'DEATNL':4, 
               'FRBE':  5, 'FRDEAT':6, 
               'NLBE':  7, 'NLDEAT':8, 
               }
    
host        = 'utilitytool.casc.eu'
baseURL     = '/CascUtilityWebService.asmx'


# getUTC(ld,tz)
# rationale: a naive or non naive local date is converted to an utc dat, 
# given the timezone string, if the local date is non naive, the time zone string is ignored
# With a naive local date there can be exceptions, when a date time is specified that does not exist or is ambiguous
# like in this example:  
# CET                       UTC
# 27.03.16      0.00        26.03.16        23.00
# 27.03.16      1.00        27.03.16        00.00
# 27.03.16      2.00        27.03.16        01.00   .NonExistentTimeError
# 27.03.16      3.00        27.03.16        01.00
# 27.03.16      4.00        27.03.16        02.00
# 27.03.16      5.00        27.03.16        03.00
# 27.03.16      6.00        27.03.16        04.00
#
# 30.10.16      0.00        29.10.16        22.00
# 30.10.16      1.00        29.10.16        23.00
# 30.10.16      2.00        30.10.16        00.00   .AmbiguousTimeError
# 30.10.16      3.00        30.10.16        02.00
# 30.10.16      4.00        30.10.16        03.00
# 30.10.16      5.00        30.10.16        04.00
# 30.10.16      6.00        30.10.16        05.00
#
# The procedure is to ignore such invalid dates and move to a valid date by adding hours to the local date util
# there is no exeption. From suchd a date a valid conversion to utc can be performed. 
# The hours forwarded when searching for a valid date are then inversed using the utc date 
def getUTC(localDateIn,strTimeZone):
    localDate = localDateIn
    hoursForwarded = 0
    if (localDateIn.tzinfo== None):
        timeZone    = pytz.timezone(strTimeZone)
        foundOkDate = False
        while foundOkDate == False:
            try:       
                localDate = timeZone.localize(localDate,is_dst=None) 
                #Documentation: If you pass None as the is_dst flag to localize(), pytz will refuse to guess and raise exceptions 
                #               if you try to build ambiguous or non-existent times.
            except pytz.exceptions.AmbiguousTimeError:
                #localDate = timeZone.localize(localDateIn,is_dst=True) 
                #print "dst={dst}".format(dst=timeZone.dst(localDateIn,is_dst=True)) # gives the dst = 1h usually
                #print("utc offset: {0} ;dst={1} ".format(timeZone.utcoffset(localDate, is_dst=True),timeZone.dst(localDate, is_dst=True)))
                #print('pytz.exceptions.AmbiguousTimeError: %s' % localDate)
                hoursForwarded += 1
                localDate = localDateIn + timedelta(hours=hoursForwarded)
                continue
            except pytz.exceptions.NonExistentTimeError:
                #localDate = timeZone.localize(localDateIn,is_dst=False) # we don't change anything
                #print "dst={dst}".format(dst=timeZone.dst(localDateIn,is_dst=True)) # gives the dst = 1h usually
                #print("utc offset: {0} ;dst={1} ".format(timeZone.utcoffset(localDate, is_dst=True),timeZone.dst(localDate, is_dst=True)))
                #print('pytz.exceptions.NonExistentTimeError: %s' % localDate)
                hoursForwarded += 1
                localDate = localDateIn + timedelta(hours=hoursForwarded)
                continue
            foundOkDate = True 
                       
    #create the utc date 
    utc_date = localDate.astimezone(pytz.timezone('UTC'))
    if (hoursForwarded>0):
        utc_date -= timedelta(hours = hoursForwarded)   
    return utc_date
    #print "CET: {0} ;dst={1} ".format(localDate.strftime(datefmtOUT),localDate.dst())      


# -------------------------------------------------------------------
# request data from site
# -------------------------------------------------------------------
#url="http://utilitytool.casc.eu/CascUtilityWebService.asmx?op=GetLTNForAPeriod"
#url="http://utilitytool.casc.eu/CascUtilityWebService.asmx"
url= "http://{0}{1}".format(host,baseURL)
#headers = {'content-type': 'application/soap+xml'}
body = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetLTNForAPeriod xmlns="http://tempuri.org/">
      <dateFrom>%s</dateFrom>
      <dateTo>%s</dateTo>
    </GetLTNForAPeriod>
  </soap:Body>
</soap:Envelope>""" % (dateFrom , dateTo )
headers = {'content-type': 'text/xml', 'charset': 'utf-8', 'content-length': 'body.length' }

response = requests.post(url,data=body,headers=headers)
#print response.content   
fileHandle = open(filePath + fileNameRawResponseData, 'w')
#file.write( response.content.replace("<","\n<"))
fileHandle.write( response.content)
fileHandle.close()


# -------------------------------------------------------------------
# parse the xml response and write csv while parsing
# -------------------------------------------------------------------
# parse
root = ET.fromstring(response.content)

# print the xml namespace definitions: not used
#response_unicode = unicode(response.content, "utf-8")
response_str = response.content.decode("utf-8", "strict")
my_namespaces = dict([
   node for _, node in ET.iterparse(
      StringIO(response_str), events=['start-ns']
      )
])
pprint(my_namespaces)

#sort dict sourceIDs by value: returns a list of lists with two elements each  
#like so:  ((BEFR',  1), (BENL , 2) .....   
sorted_sourceIDs = [x for x in sourceIDs.iteritems()]
sorted_sourceIDs.sort(key=lambda x: x[1]) # sort by value 
#test
#for ID in sorted_sourceIDs:
#    print("0:{0}  1:{1}".format(ID[0],ID[1]))
#    print ID 

#open a csv file:  note: should use utf-8: but as there are no non ascii characters I don't bother
#                        for writing utf-8 is best to use python 3.x: with open('output_file_name', 'w', newline='', encoding='utf-8') as csv_file: 
#                        here we could be using something like: u = unicode(s, "utf-8")      
with open(filePath + fileName, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(columnNames)
    
    # if we are on a date, when time is reset due to daylight saving time, we need to handle this
    # see Issues
    handle_time_switch = False
    delta_hours = 0 
    #do the parsing and write csv
    for el in root.findall('.//{http://tempuri.org/}LtnData'):
        elDate = el.find('{http://tempuri.org/}Date')
        elHour = el.find('{http://tempuri.org/}Hour')
        hour = int(elHour.text)
        
        # parse time data
        # the rationale is a follows: first we try to create a UTC date from the local date
        # then hadling the daylightt saving time switch dates
        # in the end we convert the UTC back to local in order to get the right adjusted time for switch dates 
        # string parse time
        locBaseDate = datetime.strptime(elDate.text,datefmtIN)
        utcBaseDate = getUTC(locBaseDate,timeZone.zone)  
        
        # the data contain hours 1, 2, 3 , this is converting them to start from 0 
        utc_date = utcBaseDate + timedelta(hours=hour-1) 
        
        # reconverting UTC back to the lokal time as recommended by the pytz       
        loc_date = timeZone.normalize(utc_date)
        
        for ID in sorted_sourceIDs:
            vvv = el.find("{http://tempuri.org/}%s" % ID[0])
            value = vvv.text
            print("{0}({4});{1};{2};{3}".format(ID[1],utc_date.strftime(datefmtOUT),loc_date.strftime(datefmtOUT),value,ID[0]))
            writer.writerow([ID[1],utc_date.strftime(datefmtOUT),loc_date.strftime(datefmtOUT),value])
   
print("end")    
