'''
Created on 18.12.2016

@author: prudnik
'''

import json

json_text = '''{"employees":[{"firstName":"John", "lastName":"Doe"},{"firstName":"Anna", "lastName":"Smith"},{"firstName":"Peter", "lastName":"Jones"}]}'''

def runProgram():
    try:
        obj = json.loads(json_text)
        employees = obj['employees']
        for employee in employees:
            print(employee['firstName'])
            print(employee['lastName'])
                #print(employee)
        #    print
        print(repr(obj))
    except Exception as e:
        pass    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    runProgram()
