'''
Created on 31 Jan 2017

@author: rudnikp
'''

from __future__ import print_function
from threading import current_thread 
from datetime import datetime, timedelta
import xlrd
import numpy as np   
import lxml.etree as ET
import lxml.builder
import glob
import os
import Spielwiese.XMLImportInterface
 
 
 
 
def validateXml():
    '''
    @summary: converts N2EX price excel sheet to xml
    @version: 27.10.2017
    @author: rundikp
    @note: 
    '''
    #filePath = "C:/_Data/data/development/projects/N2EX/Copy of auction-prices17.xml"
    #filePath = "I:/Data/Source Data/N2EX/Copy of auction-prices17.xml"
    #filePath = "C:/_Data/data/development/projects/N2EX/w3schoolstest.xml"
    #filePath = "C:/_Data/data/development/projects/N2EX/Copy of auction-prices17.xml"
    filePath = "I:\Data\Source Data\Seffaflik Epias\RealTimeGeneration/RealTimeGeneration-01012015-31122015.xml"
    filePath = "E:/Development/projects/workspace local/PythonTestProject/Validation/ICIS_Xml_Interface_Power_Test.xml"
    #filePathValidator = "C:/_Data/data/development/projects/N2EX/ICIS_Xml_Interface_Power.xsd"
    filePathValidator = "C:/_Data/data/development/projects/ICIS XML Interface/ICIS_Xml_Interface_Power.xsd"
    filePathValidator = "I:/Data/Validation/ICIS_Xml_Interface_Power.xsd"
    filePathValidator = "E:/Development/projects/workspace local/PythonTestProject/Validation/ICIS_Xml_Interface_Power_Test.xsd"
    #filePathValidator = "C:/_Data/data/development/projects/ICIS XML Interface/w3schoolstest.xsd"
    #logger.setPrintLines(False)

    try:
        '''
        xmlschema_doc = ET.parse(filePathValidator)
        xmlschema = ET.XMLSchema(xmlschema_doc)       
        xmlFile = ET.parse(filePath)
        b = xmlschema.validate(xmlFile)
        if (b == False):
            log = xmlschema.error_log
            logger.info(str(log))
        logger.info("result of validation: {b}\n".format(b = b))
        '''
        Spielwiese.XMLImportInterface.validateXMLPower(filePath)
        print("result of validation for {f} : ok\n".format(f = filePath))
        
    except (OSError, IOError) as e: # file not found
        print(str(e))
        raise e
    except Exception as e:
        print(str(e))
 
 

if __name__ == "__main__":
    validateXml()
    
    
    

