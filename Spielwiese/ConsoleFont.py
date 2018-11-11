'''
Created on 9 Jan 2017

@author: rudnikp
'''
#http://stackoverflow.com/questions/3592673/change-console-font-in-windows

import ctypes

LF_FACESIZE = 32
STD_OUTPUT_HANDLE = -11

class COORD(ctypes.Structure):
    _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

class CONSOLE_FONT_INFOEX(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_ulong),
                ("nFont", ctypes.c_ulong),
                ("dwFontSize", COORD),
                ("FontFamily", ctypes.c_uint),
                ("FontWeight", ctypes.c_uint),
                ("FaceName", ctypes.c_wchar * LF_FACESIZE)]

font = CONSOLE_FONT_INFOEX()
font.cbSize = ctypes.sizeof(CONSOLE_FONT_INFOEX)
font.nFont = 12
font.dwFontSize.X = 11
font.dwFontSize.Y = 18
font.FontFamily = 54
font.FontWeight = 400
font.FaceName = "Lucida Console"

handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE) # probably a python 3.x example
ctypes.windll.kernel32.SetCurrentConsoleFontEx(
        handle, ctypes.c_long(False), ctypes.pointer(font))     

