# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Módulo de logging - modo desarollo
#------------------------------------------------------------
# pelisalacarta
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
# Creado por: Jesús (tvalacarta@gmail.com)
# Licencia: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#------------------------------------------------------------
# Historial de cambios:
#------------------------------------------------------------

def clean_string(s):
    if not s:
        return ''
    validchars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890."
    stripped = ''.join(c for c in s if c in validchars)
    return stripped;

def info(texto):
    print clean_string(texto)

def debug(texto):
    print clean_string(texto)

def error(texto):
    print clean_string(texto)
