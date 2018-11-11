'''
Created on 26 Jan 2017

@author: rudnikp
'''
from __future__ import print_function
from General.ErrorInCode import ErrorInCode
from General.DBConnector import getValuesFromTable, runQuery, insertCheckedValuesIntoTable#, insertValuesIntoTable
from General.RunTimeController import RunTimeController 
from General.CustomThread import CustomThread
from General.DateConverter import formatDateTimeInLocalTimeToUTC
from Power.General.DatabasePreProcessingFunctions import  _getSourceIDSpotPricesActual, _getSourceIDVolumeActual, actualSpotPriceTable, actualVolumesTableData
from threading import current_thread 
from datetime import datetime, timedelta
import xlrd
import numpy as np   
import lxml.etree as ET
import lxml.builder
import glob
import os
from General.Databases import getDatabase, SYNCED, UNSYNCED
import General.DBTableNames as dbtables
import DownloaderAndImporter.Importer._GeneralImportClasses 
 


downloadFilesTable          = 'tblin_web_downloadedfiles'
dayinformationTable         = 'tblgn_dayinformation'
#tableOutEXAAprices          = "tblin_exaa_spotprices"
#tableOutEXAAvolumes         = "tblin_exaa_volumes"
#tableOutEXAA15minItraday    = "tblin_exaa_spotprices_quarterhourly"

localPathEXAA               = "I:/Data/Source Data/EXAA/Historical_EXAA_Spotprices/latest/"
publisher                   = 'N2EX'
timezoneName                = "Europe/Berlin"

#localPath = "c:/_Data/data/temp/"
localPath = "I:/Data/Source Data/N2EX"

datefmtOUT = '%Y-%m-%d %H:%M:%S'
datefmtOUT1 = '%d.%m.%Y'
datefmtOUT2 = '%H:%M'
qty_format = "{:.2f}"

logger = None

include_xsd = True
xsi = 'http://www.w3.org/2001/XMLSchema-instance'
xsdSchema = 'ICIS_Xml_Interface_Power.xsd'


PRINT_TO_SCREEN = 1   # 0 = no printing; 1 = Level 1 printing, 2 = Level 2 printing (more detail) etc  
PRINT_TO_FILE = True # because of Turkish character that are not diplayed in the Python console corretly
WRITE_TO_XMLFILE = True
WRITE_TO_CSVFILE = True
WRITE_TO_DB = True
WRITE_TO_LOGGER = False
WRITE_NULL_VALUE_RECORDS = True
PRINT_PROGRESS = False
STOPP_AFTER_N_RECORDS = 0  # 0 means no stopp, e.g. 10 means stopp after 10 records


def convertN2EXData():
    '''
    @summary: converts N2EX price excel sheet to xml
    @version: 27.10.2017
    @author: rundikp
    @note: 
            UK time change 2017
            March 27:  0, 1, 3, 4, 5, ....23  = 23 hours
            Oct 29:    0, 1, 2, 2, 3, ....23  = 25 hours 
            

    '''
    
    filePath = "C:/_Data/data/development/projects/N2EX/Copy of auction-prices17.xls"
    bRet = False
    runTimeController = current_thread().getRunTimeController()
    logger = runTimeController.logger.getLogger()

    try:
        # queryDict contains relevant variables for the queries
            # open excel file once for all imports
        excelFile = xlrd.open_workbook(filePath)
        
        filePathOut = os.path.splitext(filePath)[0] + ".xml"
        #fileNameOutExt = os.path.splitext(fileName[0])[1]
        for sheetName in excelFile.sheet_names(): 
            # use different importers for the different data (volume/spot price)
            price_sheet  = excelFile.sheet_by_name(sheetName)
             
            timeInterval    = 'hourly'
            if price_sheet.ncols > 0 and price_sheet.nrows >0: 
                #importExaaPrices(excelSheet, timeInterval)
                print ("cols={c} rows={r}".format(c=price_sheet.ncols,r=price_sheet.nrows))
                #xlRow       = price_sheet.row_values(rowx)
                if include_xsd == True:
                    xmlRoot = DownloaderAndImporter.Importer._GeneralImportClasses.get_xml_root_with_schema()
                    '''
                    E = lxml.builder.ElementMaker(nsmap={'xsi': xsi})
                    ROOT = E.power_data
                    files = ()
                    xmlRoot = ROOT(*files)
                    xmlRoot.attrib['{{{pre}}}schemaLocation'.format(pre=xsi)] = xsdSchema
                    '''
                else:    
                    xmlRoot = ET.Element("power_data")
                for rowx in xrange(6, price_sheet.nrows):
                    xlRow       = price_sheet.row_values(rowx)
                    if price_sheet.cell_type(rowx,0) != xlrd.XL_CELL_EMPTY and price_sheet.cell_type(rowx,1) != xlrd.XL_CELL_EMPTY:
                    #print(xlRow)
                        try:
                            #convert excel datetime to datetime 
                            dttuple = xlrd.xldate_as_tuple(xlRow[0], 0)#
                            baseDate = datetime(*dttuple)
                            print (datetime.strftime(baseDate,datefmtOUT), end = ',')
                            #print ("rowx={r}len={l}".format(r=rowx,l=xlRow[0]))
                            h = -1
                            for colx in xrange(1, 26):
                                if price_sheet.cell_type(rowx,colx) != xlrd.XL_CELL_EMPTY:
                                    #if colx == 5 and price_sheet.cell_type(rowx,3) == xlrd.XL_CELL_EMPTY and price_sheet.cell_type(rowx,4) == xlrd.XL_CELL_EMPTY:
                                    #    h -= 1
                                    #elif colx >= 5 and price_sheet.cell_type(rowx,3) == xlrd.XL_CELL_EMPTY and price_sheet.cell_type(rowx,4) == xlrd.XL_CELL_EMPTY:
                                    #elif colx >= 5:  
                                    
                                    if colx != 4:
                                        h += 1
                                    
                                    
                                    xmlEl = ET.SubElement(xmlRoot, "price-dataset")
                                    curDate = baseDate + timedelta(hours=h)
                                    xmlDate = ET.SubElement(xmlEl, "date").text = curDate.strftime(datefmtOUT1) 
                                    xmlHour = ET.SubElement(xmlEl, "hour").text = curDate.strftime(datefmtOUT2)
                                    f = float(xlRow[colx])
                                    xmlPrice = ET.SubElement(xmlEl, "price").text = qty_format.format(f)
                                    
                                #if (xlRow[colx] == None or xlRow[colx].strip() in ["","-"] ):
                                #if (xlRow[colx] == xlrd.XL_CELL_EMPTY):
                                #if xlRow.cell_type(colx)== xlrd.XL_CELL_EMPTY:
                                #price_sheet.cell_type(r, c) 
                                
                                #if price_sheet.cell_type(rowx,colx)== xlrd.XL_CELL_EMPTY:
                                #    print('None',end = ',')
                                #else:
                                #    
                                    print(xlRow[colx],end = ',')
                                else:
                                    print('None',end = ',')
                                    if colx == 3:
                                        h += 1    
                            print(' ', end = '\n')
                        except Exception as e:
                            print(str(e))  
                
                tree = ET.ElementTree(xmlRoot)                
                if WRITE_TO_XMLFILE == True:
                    tree.write(filePathOut,encoding = "UTF-8",xml_declaration=True, pretty_print=True) 
                bRet = True    
    except (OSError, IOError) as e: # file not found
        logger.error(str(e))
        raise e
    except ErrorInCode as exc:
        raise  ErrorInCode(str(exc.args), "Calling Module: N2EXConverter", "Calling Function: N2EXConverter")
    except Exception as exc:
        errorInCode = ErrorInCode("Module: ExaaImporter", "Function:importExaaData", "Error: " + str(exc.args), "Time: " + str (datetime.now()))
        logger.error(errorInCode)
        raise errorInCode
    return bRet
 
 
def startExcelParser():
    '''
    debugMode = True    
    displayLogsOnConsole = True 
    insertLogsIntoDatabase = True
    # ex ante - planned energy        
    runTimeController = RunTimeController("dev_test", debugMode, insertLogsIntoDatabase, displayLogsOnConsole )
    #args = {file: "C:/_Data/data/development/projects/N2EX/Copy of auction-prices17.xls"}
    f = "C:/_Data/data/development/projects/N2EX/Copy of auction-prices17.xls"
    t1 = CustomThread(runTimeController = runTimeController, target = convertN2EXData(), args = ())
    t1.start()
    t1.join()  
    '''
    debugMode = True
    displayLogsOnConsole = True
    insertLogsIntoDatabase = True 
        
    runTimeController1 = RunTimeController("dev_excel_parser", debugMode, insertLogsIntoDatabase, displayLogsOnConsole)
    t1 = CustomThread(runTimeController = runTimeController1, target = convertN2EXData ,  args=())
    t1.start()  
    t1.join()  


def test():
    '''
    @note: see http://stackoverflow.com/questions/15369329/python-adding-xml-schema-attributes-with-lxml
    '''
    dbchangelog = 'http://www.host.org/xml/ns/dbchangelog'
    xsi = 'http://www.host.org/2001/XMLSchema-instance'
    E = lxml.builder.ElementMaker(
        nsmap={
            None: dbchangelog,
            'xsi': xsi})
    
    ROOT = E.databaseChangeLog
    DOC = E.include
    
    # grab all the xml files
    files = [DOC(file=f) for f in glob.glob("*.xml")]
    
    the_doc = ROOT(*files)
    the_doc.attrib['{{{pre}}}schemaLocation'.format(pre=xsi)] = 'www.host.org/xml/ns/dbchangelog'
    
    xmlEl = ET.SubElement(the_doc, "price-dataset")
    print(ET.tostring(the_doc,
                      pretty_print=True, xml_declaration=True, encoding='utf-8'))

def test2():
    E = lxml.builder.ElementMaker(nsmap={'xsi': xsi})
    ROOT = E.power_data
    #DOC = E.include
    #files = [DOC(file=f) for f in glob.glob("*.xml")]
    files = ()
    #the_doc = ROOT(*files)
    xmlRoot = ROOT(*files)
    xmlRoot.attrib['{{{pre}}}schemaLocation'.format(pre=xsi)] = xsdSchema
    xmlEl = ET.SubElement(xmlRoot, "price-dataset")
    print(ET.tostring(xmlRoot,pretty_print=True, xml_declaration=True, encoding='utf-8'))
    
def test3():
    xmlns = 'https://analytics.icis.com/power'
    xsi = 'http://www.w3.org/2001/XMLSchema-instance'
    schemaLocation = xmlns + ' ' + xsdSchema
    E = lxml.builder.ElementMaker(
        nsmap={
            None: xmlns,
            'xsi': xsi})
    ROOT = E.power_data
    files = ()
    xmlRoot = ROOT(*files)
    xmlRoot.attrib['{{{pre}}}schemaLocation'.format(pre=xsi)] = schemaLocation
    xmlEl = ET.SubElement(xmlRoot, "price-dataset")
    print(ET.tostring(xmlRoot,pretty_print=True, xml_declaration=True, encoding='utf-8'))
    
    
if __name__ == "__main__":
    startExcelParser()
    #test2()
    #test3()
