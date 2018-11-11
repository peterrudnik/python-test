'''
Created on 10 Jan 2017

@author: rudnikp
@note  demonstrating late binding, virtual functions
'''
import test


localPath               = "I:/Data/Source Data/ENTSOE.eu"


# --------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------
class ClassGeneralXMLImporter(object):
    '''
    classdocs
    '''
    def __init__(self, params):
        '''
        Constructor
        '''
        pass
    
    def getLocalPath(self):
        return None
    
    
    def do_import(self):
        ''' 
            @summary: 
            @requires: thread has to have a runTimeController instance, no special requirements for runTimeController
            @return: (optional)
            @author:
            @version: 
        '''
        print("path is %30s" % (self.getLocalPath(),))


# --------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------
class ClassDerivedXMLImporter(ClassGeneralXMLImporter):
    '''
    classdocs
    '''
    def __init__(self, params):
        '''
        Constructor
        '''
        pass
    
    def getLocalPath(self):
        return localPath


    #def do_import(self):
    #    print("path = " + self.getLocalPath())


def test1():
    importer = ClassDerivedXMLImporter(None)
    importer.do_import()

# --------------------------------------------------------------------------------------------------------------------------------------------
# super
# --------------------------------------------------------------------------------------------------------------------------------------------
class Base(object):
    def __init__(self):
        print("Base init'ed")

class ChildA(Base):
    def __init__(self):
        print("ChildA init'ed")
        Base.__init__(self)

class ChildB(Base):
    def __init__(self):
        print("ChildB init'ed")
        super(ChildB, self).__init__()
        
        
class UserDependency(Base):
    def __init__(self):
        print("UserDependency init'ed")
        super(UserDependency, self).__init__()
        
class UserA(ChildA, UserDependency):
    def __init__(self):
        print("UserA init'ed")
        super(UserA, self).__init__()

class UserB(ChildB, UserDependency):
    def __init__(self):
        print("UserB init'ed")
        super(UserB, self).__init__()                


def test2():
    a = UserA()
    print ('----------------------------------' )
    b = UserB()


class CustomBaseError():
    '''
        @summary: BaseClass for all project related error classes
        @param *args:list, list of the parameters passed in
        @author: SchmittM
        @version: 05.05.2017
    '''
    def __init__(self, *args):
        '''convert input args to list of strings - return ErrorObject'''
        print(self.object)
        self.args = [str(a) for a in args] if not isinstance(object, str) else [args]

    def __str__(self):
        '''return concatenated string (\n) of arguments'''
        args = [a.replace("\\\\", '\\') for a in self.args]
        return "\n".join(args)

    def __repr__(self, *args, **kwargs):  # @UnusedVariable
        '''representation of class - return string stating className and list of arguments'''
        return self.__class__.__name__ + '(' + self.__str__() + ')'


def test3():
    '''
    s = test
    print(object)
    if not isinstance(object, str):
        print("yes")
    else:
        print("no")    
    '''
    #a = CustomBaseError("a", 1)
    #dir()
#===============================================================================
# 
#===============================================================================
if __name__ == "__main__":
    #test1()
    #test2()      
    test3()