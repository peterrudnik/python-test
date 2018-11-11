'''
Created on 25 Jan 2017

@author: rudnikp
'''



def startIt():
    s = '2,400.10'
    try:
        s = s.replace(',', '')
        f = float(s)
        print ("f = {f}".format(f = str(f)))
    except Exception as e:
        print str(e) 
            
    
if __name__ == "__main__":
    startIt()      