'''
Created on 1 Feb 2017

@author: rudnikp
@note: This module provides XML Schema validation. It provides a header when creating new xml files. This is required when there is a need to create xml files from client data.
       The module provides also functions to validate against the XML Schema which is defined is xsd files (see below). If there is a need to extned the interface definition, 
       this should be done in the xsd files 
'''
import lxml.etree as ET
import lxml.builder


xsi = 'http://www.w3.org/2001/XMLSchema-instance'  # this string must conform with the one used in the xsd file, otherwise there will be an error during validation, which looks like this:
                                                   #  attribute {http://www.host.org/2001/XMLSchema-instance}schemaLocation: The attribute {http://www.host.org/2001/XMLSchema-instance}schemaLocation is not allowed.,)                 
xsdSchemaPower = 'ICIS_Xml_Interface_Power.xsd'
xmlnsPower = 'https://analytics.icis.com/power'
#filePathValidatorPower = "I:/Data/Validation/ICIS_Xml_Interface_Power.xsd"
filePathValidatorPower = "E:/Development/projects/workspace local/PythonTestProject/Validation/ICIS_Xml_Interface_Power_Test.xsd"


def xmlTagRootPower():
    return "power_data"
def xmlTagProductionData():
    return "production_data" 
def xmlTagProductionDataset():
    return "production_dataset" 
def xmlTagProductionDatapoint():
    return "production_datapoint" 
def xmlTagProductionDatapointValue():
    return "production" 
def xmlTagPriceData():
    return "price_data" 
def xmlTagPriceDataset():
    return "price_dataset" 
def xmlTagPriceDatapoint():
    return "price_datapoint" 

def xmlTagDate():
    return "date" 
def xmlTagTime():
    return "time" 
def xmlTagUoM():
    return "uom" 
def xmlTagPrice():
    return "price" 


# source id
def xmlTagArea():
    return "area" 
def xmlTagPublisher():
    return "publisher" 
def xmlTagInstantValue():
    return "instantValue" 
def xmlTagTimeInterval():
    return "timeInterval" 
def xmlTagFuelType():
    return "fuelType" 
def xmlTagBlockType():
    return "blockType" 
def xmlTagAuctionType():
    return "auctionType" 

def dateFormat():
    return '%Y-%m-%d'
def timeFormat():
    return '%H:%M:%S'

# fueltypes
def xmlTagBattery():
    return "battery" 
def xmlTagBiomass():
    return "biomass" 
def xmlTagCoal():
    return "coal" 
def xmlTagCoalderivedgas():
    return "coal-derived-gas" 
def xmlTagCoke():
    return "coke" 
def xmlTagFossil():
    return "fossil" 
def xmlTagGas():
    return "gas" 
def xmlTagGeothermal():
    return "geothermal" 
def xmlTagHydro():
    return "hydro" 
def xmlTagLignite():
    return "lignite" 
def xmlTagMarine():
    return "marine" 
def xmlTagNaphtha():
    return "naphtha" 
def xmlTagNuclear():
    return "nuclear" 
def xmlTagOil():
    return "oil" 
def xmlTagOther():
    return "other" 
def xmlTagOtherrenewables():
    return "other_renewables" 
def xmlTagPeat():
    return "peat" 
def xmlTagPumpedandseasonalstorage():
    return "pumped-and-seasonal-storage" 
def xmlTagPumpedstorage():
    return "pumped-storage" 
def xmlTagPv():
    return "pv" 
def xmlTagPvestimated():
    return "PV-estimated" 
def xmlTagPvmeasured():
    return "PV-measured" 
def xmlTagRenewables():
    return "renewables" 
def xmlTagRunofriver():
    return "run-of-the-river" 
def xmlTagSeasonalstorage():
    return "seasonal-storage" 
def xmlTagSolar():
    return "solar" 
def xmlTagSolarthermal():
    return "solar-thermal" 
def xmlTagX():
    return "steam" 
def xmlTagTotal():
    return "total" 
def xmlTagWaste():
    return "waste" 
def xmlTagWind():
    return "wind" 
def xmlTagWindoffshore():
    return "wind-offshore" 
def xmlTagWindonshore():
    return "wind-onshore" 
def xmlTagWood():
    return "wood"



# --------------------------------------------------------------------------------------------------------------------------------------------
# XML Schema functions
# --------------------------------------------------------------------------------------------------------------------------------------------
def getRoot(include_schema = True):
    if include_schema == True:
        return get_xml_root_with_power_xmlschema()
    else:    
        xmlRoot = ET.Element(xmlTagRootPower())



def get_xml_root_with_power_xmlschema():
    ''' 
        @summary: gets a xml header including an XML Schema validator for power
                  it has the from mentioned in the @return 
        @requires: the XML Schema file filePathValidatorPower (see above)
        @return: "<power_data xmlns:xsi="http://www.host.org/2001/XMLSchema-instance" xmlns="https://analytics.icis.com/power" xsi:schemaLocation="https://analytics.icis.com/power ICIS_Xml_Interface_Power.xsd">"
        @author: Peter Rudnik
        @version: 1.0
    '''
    schemaLocation = xmlnsPower + ' ' + xsdSchemaPower
    E = lxml.builder.ElementMaker(
        nsmap={
            None: xmlnsPower,
            'xsi': xsi})
    ROOT = E.power_data
    files = ()
    xmlRoot = ROOT(*files)
    xmlRoot.attrib['{{{pre}}}schemaLocation'.format(pre=xsi)] = schemaLocation
    return xmlRoot
 
def validateXMLPower(filePath):
    ''' 
        @summary: validates a xml file if  it complies with the XML Schema file filePathValidatorPower (see above)
                throws an exception if the file does not comply and gives a description of the problem
        @requires: the XML Schema file "I:/Data/Validation/ICIS_Xml_Interface_Power.xsd"
        @return: 
        @author: Peter Rudnik
        @version: 1.0
    '''
    try: 
        xmlschema_doc = ET.parse(filePathValidatorPower)
        xmlschema = ET.XMLSchema(xmlschema_doc)       
        xmlFile = ET.parse(filePath)
        b = xmlschema.validate(xmlFile)
        if (b == False):
            log = xmlschema.error_log
            raise Exception(str(log))
    except Exception as e:
        raise e        

