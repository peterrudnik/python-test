'''
Created on 13 Jan 2017

@author: rudnikp
'''

filePath = 'I:/PersonalFolders/MVarli/tuerkeiWetterDaten/'
fileInput = '2015.csv'
fileOutput = '2015-selected-data 2.csv'

def doit():
    fOut = open(filePath + fileOutput,'w')
    with open(filePath + fileInput) as fIn:
        for line in fIn:
            #print (line)
            if (line.startswith('TUM00017130')):
                fOut.write(line)      
            
    fIn.close()        
    fOut.close() 
    print ("finished")       


if __name__ == '__main__':
    doit()