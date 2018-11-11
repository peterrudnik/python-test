'''
Created on 01.11.2017

@author: prudnik
'''
from __future__ import print_function
import ConversionFunctions as conv
import sys, os
import pytz
import csv
import re
import collections
from datetime import datetime, timedelta  

#--------------------------------------------------------------------------------------------------------------------------------------------
# Data definitions
# -------------------------------------------------------------------------------------------------------------------------------------------

class UnitLevel():
    All, ProductionUnit, GenerationUnit = range (3)

class EICUnit():
    ''' 
        @summary: base class fro production and power unit :
    '''    
    def __init__(self, **kwargs):

        self._eicCode = None
        if "eicCode" in kwargs:
            self._eicCode = kwargs["eicCode"]
            
        self._eicName = None
        if "eicName" in kwargs:
            self._eicName = kwargs["eicName"]
            
        self._displayName = None
        if "displayName" in kwargs:
            self._displayName = kwargs["displayName"]
        
        self._functionsAs = None     # GenerationUnit, Load            
        if "functionsAs" in kwargs:
            self._functionsAs = kwargs["functionsAs"]
        
        self._area = None
        if "area" in kwargs:
            self._area = kwargs["area"]

        self._pubDate = None
        if "pubDate" in kwargs:
            self._pubDate = kwargs["pubDate"]

        self._fuelType = None
        if "fuelType" in kwargs:
            self._fuelType = kwargs["fuelType"]

        self._max_capacity = None
        if "max_capacity" in kwargs:
            self._max_capacity = kwargs["max_capacity"]
    
        self._publisher = None
        if "publisher" in kwargs:
            self._publisher = kwargs["publisher"]

        self._timeInterval = None
        if "timeInterval" in kwargs:
            self._timeInterval = kwargs["timeInterval"]

        self._timeZone = None
        if "timeZone" in kwargs:
            self._timeZone = kwargs["timeZone"]

    @property
    def eicCode(self):
        return self._eicCode

    @property
    def eicName(self):
        return self._eicName

    @property
    def displayName(self):
        return self._displayName

    @property
    def plantName(self):
        return self._plantName

    @plantName.setter
    def plantName(self,v):
        self._plantName = v

    @property
    def functionsAs(self):
        return self._functionsAs

    @property
    def fuelType(self):
        return self._fuelType

    @property
    def max_capacity(self):
        return self._max_capacity
    
    @property
    def area(self):
        return self._area

    @property
    def publisher(self):
        return self._publisher

    @property
    def timeInterval(self):
        return self._timeInterval

    @property
    def timeZone(self):
        return self._timeZone

    @property
    def pubDate(self):
        return self._pubDate

    def toString(self):
        str_format = "{:>40s}"
        qty_format = "{:8.2f}" 
        s = conv.writeToString("eicCode (gen )=", self.eicCode ,  str_format = "{:>20s}" )
        s += conv.writeToString(", name=", self.displayName ,  str_format = "{:>10s}" )
        s += conv.writeToString(", eic name=", self.eicName ,  str_format = "{:>45s}" )
        s += conv.writeToString(", fuelType=",self._fuelType ,  str_format = "{:>15s}" )
        s += conv.writeToString(", max capacity=",self._max_capacity ,  qty_format = qty_format , str_format = "{:>8s}")
        s += conv.writeToString(", functions as=",self._functionsAs ,  str_format = "{:>20s}" )
        return s

    def toStringAlt(self):
        str_format = "{:>40s}"
        unitName = self.displayName
        s = "Generation Unit: "
        s += conv.writeToString(" area=", self._area ,  str_format = "{:>2s}" )
        s += conv.writeToString(", unitID=", self.eicCode ,  str_format = "{:>20s}" )
        s += conv.writeToString(", fuelType=",self.fuelType ,  str_format = "{:>15s}" )
        s += conv.writeToString(", pub=", self._publisher ,  str_format = "{:>15s}" )
        s += conv.writeToString(", time=", self._timeInterval ,  str_format = "{:>10s}" )
        s += conv.writeToString(", timeZone=", self._timeZone ,  str_format = "{:>3s}" )
        s += conv.writeToString(", unit=", unitName ,  str_format = "{:>10s}" )
        s += conv.writeToString(", plant=", self.plantName ,  str_format = "{:>10s}" )
        return s

 
class EICGenerationUnit(EICUnit):
    ''' 
        @summary: generation unit which has a fueltype:
    '''    
    def __init__(self, **kwargs):
        EICUnit.__init__(self,**kwargs)


class EICProductionUnit(EICUnit):
    ''' 
        @summary: Production unit which has 1 to many Generation Units:
    '''    
    def __init__(self, **kwargs):
        EICUnit.__init__(self,**kwargs)
        self._generationUnitDict = dict()
    
    def addGenerationUnit(self,v):
        if v is not None:
            if v.eicCode != None:
                self._generationUnitDict[v.eicCode] = v

    def getGenerationUnitCount(self):
        return len(self._generationUnitDict)
                
    def getGenerationUnitByIndex(self,indexIn):
        ret = None
        for index, key in enumerate(self._generationUnitDict):
            if index == indexIn:
                ret = self._generationUnitDict[key]
        return ret    
    
    @property
    def max_capacity(self):
        max_capacity = None
        for key, generationUnit in self._generationUnitDict.iteritems():
            if generationUnit:
                if max_capacity is None:
                    max_capacity = generationUnit.max_capacity
                else:    
                    max_capacity += generationUnit.max_capacity
        return max_capacity
    
    def toString(self, unitLevel = UnitLevel.All):
        if self.displayName == "WLNY12":
            pass
        str_format = "{:>40s}"
        qty_format = "{:8.2f}"
        indent_string = ""
        s = "" 
        if unitLevel == UnitLevel.All or  unitLevel == UnitLevel.ProductionUnit:
            indent_string = "    "
            s += conv.writeToString("eicCode (prod)=", self.eicCode ,  str_format = "{:>24s}" )
            s += conv.writeToString(", name=", self.displayName ,  str_format = "{:>10s}" )
            s += conv.writeToString(", eic name=", self.eicName ,  str_format = "{:>45s}" )
            s += conv.writeToString(", fuelType=","" ,  str_format = "{:>15s}" )
            s += conv.writeToString(", max capacity=", self.max_capacity ,  qty_format = qty_format, str_format = "{:>8s}" )
            s += conv.writeToString(", functions as=",self._functionsAs ,  str_format = "{:>20s}" )
            s += conv.writeToString(", number of units=",len(self._generationUnitDict)  )
        if unitLevel == UnitLevel.All or  unitLevel == UnitLevel.GenerationUnit:
            for key, generationUnit in self._generationUnitDict.iteritems():
                if generationUnit:
                    if len(s) > 0:
                        s+= "\n"
                    s += indent_string + generationUnit.toString()
        return s
        #return "eicCode={c:>20}, name ={n:>35},  functions as: {fa:>20} , number of units {ng}".format(c=self.eicCode,n=self.eicName, ng = len(self._generationUnitDict), fa = self._functionsAs)

    def toStringAlt(self, unitLevel = UnitLevel.All):
        plantName = self.displayName
        str_format = "{:>40s}"
        indent_string = ""
        s = "" 
        if unitLevel == UnitLevel.All or  unitLevel == UnitLevel.ProductionUnit:
            indent_string = "    "
            s += "Production Unit: "
            s += conv.writeToString(" area=", self._area ,  str_format = "{:>2s}" )
            s += conv.writeToString(", unitID=", self.eicCode ,  str_format = "{:>20s}" )
            s += conv.writeToString(", fuelType=","" ,  str_format = "{:>15s}" )
            s += conv.writeToString(", pub=", self._publisher ,  str_format = "{:>15s}" )
            s += conv.writeToString(", time=", self._timeInterval ,  str_format = "{:>10s}" )
            s += conv.writeToString(", timeZone=", self._timeZone ,  str_format = "{:>3s}" )
            s += conv.writeToString(", unit=", "" ,  str_format = "{:>10s}" )
            s += conv.writeToString(", plant=", plantName ,  str_format = "{:>10s}" )
        if unitLevel == UnitLevel.All or  unitLevel == UnitLevel.GenerationUnit:
            for key, generationUnit in self._generationUnitDict.iteritems():
                if generationUnit:
                    if len(s) > 0:
                        s+= "\n"
                    s += indent_string + generationUnit.toStringAlt()
        return s


class EICData():
    ''' 
        @summary: holds a list of production units each having 1 to many Generation Units:
    '''    
    def __init__(self):
        self._productionUnitDict = dict()
        self._index = -1
     
    def addProductionUnit(self,v):
        if v is not None:
            if v.eicCode != None:
                self._productionUnitDict[v.eicCode] = v

    def getProductionUnitCount(self):
        return len(self._productionUnitDict)
    
    
    def __iter__(self):
        self._index = -1
        return self

    def next(self):
        ret = None
        if self._index < len(self._productionUnitDict)-1:
            self._index += 1
            for index, key in enumerate(self._productionUnitDict):
                if index == self._index:
                    ret = self._productionUnitDict[key]
                    break
            return ret
        else:
            raise StopIteration    
                
    def getProductionUnitByIndex(self,indexIn):
        ret = None
        for index, key in enumerate(self._productionUnitDict):
            if index == indexIn:
                ret = self._productionUnitDict[key]
        return ret    

    def getProductionUnitByDisplayName(self,name):
        ret = None
        for key, value in self._productionUnitDict.iteritems():
            if value.displayName == name:
                ret = self._productionUnitDict[key]
        return ret

    def toStringOld(self,unitLevel = UnitLevel.All):
        s = ""    
        n1 = self.getProductionUnitCount()
        for i1 in range(n1):
            productionUnit = self.getProductionUnitByIndex(i1)
            if productionUnit:
                if len(s) > 0:
                    s += "\n"
                s += productionUnit.toString(unitLevel)
        return s    
    
    def toString(self,unitLevel = UnitLevel.All):
        s = ""    
        for productionUnit in self:
            if len(s) > 0:
                s += "\n"
            s += productionUnit.toString(unitLevel)
        return s    
    
#--------------------------------------------------------------------------------------------------------------------------------------------
# Main Functions
# -------------------------------------------------------------------------------------------------------------------------------------------

def generateSampleData():
    eicData = EICData()
    for i in range(10):
        displayName = "PU " + str(i)
        eicName = "PU " + str(i)
        eicCode = "PU " + str(i)
        functionsAs = "PU"
        publisher = "ICIS"
        area ="GB"
        timeInterval = "yearly",
        timeZone = "WET", 
        
        pubDate    = datetime(2017, 1, 1)                                
        productionUnit = EICProductionUnit(eicCode=eicCode, 
                                           eicName=eicName, 
                                           displayName=displayName , 
                                           functionsAs=functionsAs, 
                                           area = area, 
                                           publisher = publisher, 
                                           timeInterval = timeInterval,
                                           timeZone=timeZone, 
                                           pubDate = pubDate)
        for i in range(3):
            displayName = "GU " + str(i)
            eicName = "GU " + str(i)
            eicCode = "GU " + str(i)
            functionsAs = "GU"
            fuelType = "nuclear"
            max_capacity = 1000
            generationUnit = EICGenerationUnit(eicCode=eicCode, 
                                               eicName=eicName, 
                                               displayName=displayName , 
                                               functionsAs=functionsAs, 
                                               area = area, 
                                               fuelType=fuelType, 
                                               max_capacity=max_capacity, 
                                               publisher = publisher, 
                                               timeInterval = timeInterval,
                                               timeZone=timeZone, 
                                               pubDate = pubDate)
            productionUnit.addGenerationUnit(generationUnit)
        eicData.addProductionUnit(productionUnit)
    return eicData    

def startEICCodeManualProcedure():
    eicData = generateSampleData()
    print(eicData.toString(UnitLevel.All))
    '''
    s = ""    
    for productionUnit in eicData:
        if len(s) > 0:
            s += "\n"
        s += productionUnit.toString(UnitLevel.All)
    
    print s    
    '''

#--------------------------------------------------------------------------------------------------------------------------------------------
# Controlling Functions
# -------------------------------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    startEICCodeManualProcedure()
    
