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
    text = u"ปวดหัวคงจะเป็นอาการที่มนุษย์รู้สึกบ่อยที่สุดในบรรดาอาการทั้งหลายเพราะหัวอยู่ใกล้สมองอันเป็นที่รับรู้ ที่จริงอาการอื่นๆ มันก็คงจะมีมากเหมือนกัน เช่น ปวดแข้ง ปวดขา ปวดนิ้วเท้า แต่เนื่องจากมันอยู่ไกลที่รับรู้ จึงไม่ค่อยคำนึงถึง ปวดหัวเกือบทั้งหมดเกิดจากอาการเครียด เช่น อดนอน ทำงานใช้ความคิดมาก มีอารมณ์ เช่น รถติด วิตกกังวล โกรธ เกลียด"

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


#--------------------------------------------------------------------------------------------------------------------------------------------
# Controlling Functions
# -------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    #test1()
    #test2()
    test3()

