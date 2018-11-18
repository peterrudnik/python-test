# -*- coding: utf-8 -*-
'''
Created on 16.06.2018

@author: prudnik
'''

import PyICU


def test1():
    s = ""
    value = 1
    print (f'The value is {value}.')


#----------------------------------------------------------------------------- #
def isThai(chr):
    cVal = ord(chr)
    if(cVal >= 3584 and cVal <= 3711):
        return True
    return False

def warp(txt):
    print (txt)
    bd = PyICU.BreakIterator.createWordInstance(PyICU.Locale("th"))
    bd.setText(txt)
    lastPos = bd.first()
    retTxt = ""
    try:
        while(1):
            currentPos = bd.next()
            retTxt += txt[lastPos:currentPos]
            #Only thai language evaluated
            if(isThai(txt[currentPos-1])):
                if(currentPos < len(txt)):
                    if(isThai(txt[currentPos])):
                        #This is dummy word seperator   
                        retTxt += "|"
            lastPos = currentPos
    except StopIteration:
        pass
        #retTxt = retTxt[:-1]
    return retTxt

def test2():
    text = u"à¸›à¸§à¸”à¸«à¸±à¸§à¸„à¸‡à¸ˆà¸°à¹€à¸›à¹‡à¸™à¸­à¸²à¸�à¸²à¸£à¸—à¸µà¹ˆà¸¡à¸™à¸¸à¸©à¸¢à¹Œà¸£à¸¹à¹‰à¸ªà¸¶à¸�à¸šà¹ˆà¸­à¸¢à¸—à¸µà¹ˆà¸ªà¸¸à¸”à¹ƒà¸™à¸šà¸£à¸£à¸”à¸²à¸­à¸²à¸�à¸²à¸£à¸—à¸±à¹‰à¸‡à¸«à¸¥à¸²à¸¢à¹€à¸žà¸£à¸²à¸°à¸«à¸±à¸§à¸­à¸¢à¸¹à¹ˆà¹ƒà¸�à¸¥à¹‰à¸ªà¸¡à¸­à¸‡à¸­à¸±à¸™à¹€à¸›à¹‡à¸™à¸—à¸µà¹ˆà¸£à¸±à¸šà¸£à¸¹à¹‰ à¸—à¸µà¹ˆà¸ˆà¸£à¸´à¸‡à¸­à¸²à¸�à¸²à¸£à¸­à¸·à¹ˆà¸™à¹† à¸¡à¸±à¸™à¸�à¹‡à¸„à¸‡à¸ˆà¸°à¸¡à¸µà¸¡à¸²à¸�à¹€à¸«à¸¡à¸·à¸­à¸™à¸�à¸±à¸™ à¹€à¸Šà¹ˆà¸™ à¸›à¸§à¸”à¹�à¸‚à¹‰à¸‡ à¸›à¸§à¸”à¸‚à¸² à¸›à¸§à¸”à¸™à¸´à¹‰à¸§à¹€à¸—à¹‰à¸² à¹�à¸•à¹ˆà¹€à¸™à¸·à¹ˆà¸­à¸‡à¸ˆà¸²à¸�à¸¡à¸±à¸™à¸­à¸¢à¸¹à¹ˆà¹„à¸�à¸¥à¸—à¸µà¹ˆà¸£à¸±à¸šà¸£à¸¹à¹‰ à¸ˆà¸¶à¸‡à¹„à¸¡à¹ˆà¸„à¹ˆà¸­à¸¢à¸„à¸³à¸™à¸¶à¸‡à¸–à¸¶à¸‡ à¸›à¸§à¸”à¸«à¸±à¸§à¹€à¸�à¸·à¸­à¸šà¸—à¸±à¹‰à¸‡à¸«à¸¡à¸”à¹€à¸�à¸´à¸”à¸ˆà¸²à¸�à¸­à¸²à¸�à¸²à¸£à¹€à¸„à¸£à¸µà¸¢à¸” à¹€à¸Šà¹ˆà¸™ à¸­à¸”à¸™à¸­à¸™ à¸—à¸³à¸‡à¸²à¸™à¹ƒà¸Šà¹‰à¸„à¸§à¸²à¸¡à¸„à¸´à¸”à¸¡à¸²à¸� à¸¡à¸µà¸­à¸²à¸£à¸¡à¸“à¹Œ à¹€à¸Šà¹ˆà¸™ à¸£à¸–à¸•à¸´à¸” à¸§à¸´à¸•à¸�à¸�à¸±à¸‡à¸§à¸¥ à¹‚à¸�à¸£à¸˜ à¹€à¸�à¸¥à¸µà¸¢à¸”"

    tokens = warp(text.replace(' ',''))
    print (tokens)


def test3():
    locale = PyICU.Locale('pt_BR')
    name = locale.getDisplayName()
    print (name)

def test4():
    pass

def test5():
    pass

def test6():  
    pass

def test7():  
    pass

def test8():  
    pass

def test9():  
    pass

def test10():  
    pass

#--------------------------------------------------------------------------------------------------------------------------------------------
# Controlling Functions
# -------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    #test1()
    #test2()
    test3()

