# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Parámetros de configuración (mediaserver)
#------------------------------------------------------------
# tvalacarta
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
# Creado por: Jesús (tvalacarta@gmail.com)
# Licencia: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#------------------------------------------------------------

import sys
import os
import re
import ConfigParser

PLATFORM_NAME = "command-line"
PLUGIN_NAME = "descargar"

def get_platform():
    return PLATFORM_NAME

def is_xbmc():
    return False

def get_library_support():
    return False

def get_system_platform():

    # platform.system().lower() es "linux", "sunos", "darwin", "windows"
    import platform
    python_platform_name = platform.system().lower()

    platform = "unknown"
    if python_platform_name=="linux":
        platform = "linux"
    elif python_platform_name=="darwin":
        platform = "osx"
    elif python_platform_name=="windows":
        platform = "windows"

    return platform

def open_settings():
    return None

def get_setting(name):
    return ""
    
def set_setting(name,value):
    return ""

def get_localized_string(code):
    return ""

def get_library_path():
    return None

def get_temp_file(filename):
    return os.path.join(get_data_path(),filename)

def get_data_path():
    return os.getcwd()

def get_runtime_path():
    return os.getcwd()

def get_cookie_data():
    import os
    ficherocookies = os.path.join( get_data_path(), 'cookies.dat' )

    cookiedatafile = open(ficherocookies,'r')
    cookiedata = cookiedatafile.read()
    cookiedatafile.close();

    return cookiedata

print "get_data_path="+get_data_path()
print "get_runtime_path="+get_runtime_path()
