# -*- coding: utf-8 -*-
import os
import sys
import webapp2
import jinja2
import urllib2
import urllib
from google.appengine.ext import db
from google.appengine.api import memcache
import time
import json
from google.appengine.api import urlfetch
import logging

urlfetch.set_default_fetch_deadline(45)
tarjetas = {'bdiplazacentralgold':1862,'bdiplazacentralclasica':1861,'bdiplazacentrallocal':1860,'bdibmcargogold':1864,'bdibmcargolocal':2085,'bdifundapec':1867,'bdibmcargoclasica':2084,'ademiclasica': 1791, 'vimencablackgold': 6024, 'scotiabankgold': [1775, 1776], 'scotiabankaadvantageplatinum': 1782, 'popularalmacenesiberia': 1696, 'bancamericaclasica': 2017, 'popularplatinumlocal': [1691, 1690], 'banaciplatinum': 16, 'progresointernacional': [1756, 1753], 'bhdleonmipais': 1736, 'alnapgold': 1678, 'popularmileageplus': 1704, 'scotiabankvisa': 1774, 'popularccnplus': 1703, 'apapclasicainternacional': 1766, 'bdianthonysplatinum': 1871, 'bdisignature': 1858, 'bhdleongoldpremia': 1929, 'scotiabankinfinite': 1783, 'progresoamericanexpress': 1748, 'banreservasmultimoneda': [1710, 1711], 'progresoplatinum': 1760, 'ademigoldinternacional': 1793, 'caribeplatinum': 1847, 'bhdleonclasicalocal': 1725, 'federalplatinum': 1851, 'apapstandardinternacional': 1762, 'banreservasplatinumuniverse': 1718, 'bdiplatinum': 2075, 'alnapconfiaentilocal': 4153, 'alnapconfiaentiinternacional': 4228, 'vimencaplatinum': 1814, 'bhdleonsiremasoro': 1743, 'popularplatinuminternacional': [1922, 1923], 'banreservasclasica': 1712, 'banescoclasicainternacional': 1806, 'promericalamaplazos': 1820, 'bancamericasignature': 2021, 'apapgold': 1767, 'bhdleonblackmujer': 1735, 'apapfamiliar': 1769, 'lopezdeharoclasica': 1829, 'ademiempresarialinternacional': 92, 'promericagold': 1828, 'bancamericaplatinum': 2019, 'scotiabankorange': 1785, 'bancamericagold': 2018, 'scotiabankaadvantage': 1779, 'caribeecard': 1932, 'bhdleonclasicainternacional': 1727, 'vimencaclasicalocal': 1812, 'bhdleoninfinite': 1732, 'popularmbsignaturecard': 1695, 'acapvisaclasicalocal': 1770, 'banescoplatinum': [2087, 1807], 'bhdleongold': [1730, 1729], 'bhdleongoldmlb': 1738, 'banacistandar': 116, 'acapvisagold': 1772, 'popularfcbescola': 1694, 'populargoldinternacional': [1920, 1921], 'vimencagold': 1813, 'bhdleonbeisbolinvernal': 1737, 'banescogold': 1809, 'banreservasgoldmultimoneda': 1716, 'banacigold': 130, 'banaciempresarial': 132, 'bhdleonplatinummujer': 1734, 'ademiclasicainternacional': 1792, 'lopezdeharoclubnaco': 1833, 'lopezdeharoclubhemingway': 1834, 'popularcaminantesporlavida': 1699, 'bdisignaturebmcargo': 1863, 'popularsegurosuniversal': 1702, 'banescostandard': 2083, 'bdilocal': 1855, 'bhdleonclasicapremia': 1928, 'bdicrediplan': 152, 'santacruzclasica': 1786, 'alnapunaselocal': 1680, 'alnapclasicalocal': 1676, 'banreservasplatinum': 1717, 'promericaplatinum': 1826, 'popularclasicainternacional': [1918, 1919], 'caribeclasicainternacional': 1842, 'popularsuperpolasirena': 1700, 'lopezdeharogoldsgym': 1835, 'promericaspiritgold': 1816, 'alnapunionlocal': 1682, 'scotiabankmastercard': 1773, 'ademiempresarialplus': 1797, 'ademihipermercadosole': 1794, 'alnapcompramas': 4247, 'apapplatinum': [1764, 1768], 'alnapunioninternacional': 1683, 'banacicombustible': 80, 'bdianthonysclasica': 1869, 'banreservasstandard': 1713, 'scotiabankaadvantagegold': [1780, 1781], 'alnapclasicainternacional': 1677, 'ademiempresariallocal': 1796, 'acapvisaclasicainternacional': 1771, 'bhdleonstandardlocal': 1726, 'scotiabankplatinum': [1777, 1778], 'progresoamericanexpresssumaccn': 1930, 'apapgoldinternacional': 1763, 'popularblackinternacional': 1924, 'santacruzcecomsa': 1790, 'bdianthonysgold': 1870, 'bhdleongoldmujer': 1733, 'alnapunaseinternacional': 1681, 'federalgold': 1850, 'banescooro': 2088, 'lopezdeharoplatinum': 1831, 'bdiclasica': 1856, 'scotiabankpricesmartdiamond': 1931, 'federalclasica': 1849, 'bdigold': 1857, 'popularprestige': 1689, 'promericaspiritplatinum': 1815, 'lopezdeharogold': 1830, 'lopezdeharocasadeespana': 1832, 'popularikeafamily': 1698, 'caribeelite': 1846, 'banescoinfinite': 1808, 'popularclasicalocal': [1684, 1685], 'progresogold': [1757, 1754], 'progresolocal': [1755, 1752], 'banreservasinfinite': 1719, 'santacruzplatinum': 1788, 'vimencaclasicainternacional': 6023, 'scotiabankbravo': 1784, 'promericaplatinumpremium': 1821, 'caribeclasicalocal': 1840, 'bhdleonstandardinternacional': 1728, 'apapstandardlocal': 1761, 'santacruzinfinite': 1789, 'alnapconfiamaslocal': 1679, 'popularblacklocal': 1692, 'santacruzgold': 1787, 'popularorbit': 1688, 'bhdleonlacadena': 1742, 'promericainfinite': 1824, 'progresotheplatinumcard': 1750, 'vimencagoldpagatodo': 137, 'promericamisuper': 1817, 'progresoamericanexpresscasadecampoplatinum': 1751, 'banaciblack': 140, 'caribeoro': 1848, 'popularjetblue': 1705, 'apapclasicalocal': 1765, 'progresoamericanexpressgold': 1749, 'bhdleonplatinum': 1731, 'banreservasgold': [1714, 1715], 'populargoldlocal': [1686, 1687]}
empresas = ['bm cargo',"plaza central","lidom","mlb","la sirena","vimenca", "american airlines", "pricesmart", "orange", "bravo", "cecomsa", "plaza lama", "carrefour", "spirit", "utesa", "anthony's", "san miguel", " mbe ", "mb cargo", "unase", u"unión", "vega real", u"olé", "ccn", "gold's gym", "club hemingway", "club naco", u"casa de españa", "jetblue", "united", "seguros universal", "grupo ramos", "caminantes por la vida", "ikea", "almacenes iberia", "mercedes benz", "fcbescola"]
aerolineas = ["delta airlines", "pawa dominicana", "dominican wings", "copa airlines", "united airlines", "avianca", "spirit", "american airlines", "air century", "venezolana", "southwest airlines", "seaborne", "jetblue", "air europa", "lan airline", "general air services", "helidosa", "aerointer", "airberlin", "aircanada","tropical aero servicios", "aserca airlines", "air france"]

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)
                                       
class Handler(webapp2.RequestHandler):
    def write(self,*a,**kw):
        self.response.write(*a,**kw)
    def render_str(self,template,**params):
        y = jinja_env.get_template(template)
        return y.render(params)
    def render(self,template,**kw):
        self.write(self.render_str(template,**kw))

class InformacionTarjetas(db.Model):
    nombre = db.StringProperty(required=True)
    contenido = db.TextProperty(required=True)

class Tarjeta_ID(db.Model):
    nombre_tarjeta = db.StringProperty(required=True)
    numeros_tarjeta = db.ListProperty(item_type=int,required=True)

class Global_Instituciones(db.Model):
    empresas = db.ListProperty(item_type=str,required=True)
    aerolineas = db.ListProperty(item_type=str,required=True)





def fetch(info):
    info = info[info.find("<div id='contenido'>")+len("<div id='contenido'>"):info.find("</div>", info.find("<div id='contenido'>")+1)]
    return info

def guardarTarjeta(name,check):
    done = False
    info = urllib2.urlopen('http://pocket-wikix.appspot.com/'+name).read().decode("utf-8")
    if len(info) > 0:
        done = True
    if check==True:
        return done
    if done == True:
        informacion = InformacionTarjetas(
            contenido=fetch(info),
            nombre = name )
        informacion.put()
        memcache.set(informacion.nombre,informacion)

def sacar_entero(cadena):
    if type(cadena) == float or type(cadena) == int:
        return int(cadena)
    else:
        for e in cadena:
            if e.isdigit() == False and e != ".":
                cadena = cadena.replace(e,"")
        return int(float(cadena))
def convertir_float(cadena):
    for e in cadena:
        if e.isdigit() == False and e != ".":
            cadena = cadena.replace(e,"")
    if cadena == "":
        return 0
    return float(cadena)

def mayusculiza(cadena):
    cadena = cadena.split()
    estring = ""
    for e in cadena:
        estring += " " + e.replace(e[0],e[0].upper())
    return estring[1:]

def Compara_tarjetas(info,info2,update):
    cache = memcache.get(str(info["id"]))
    if cache == None or update == True:
        el_ayudante = info2
        el_real = {}
        la_comparacion = {}
        for e in info:
            el_real[e] = info[e]

        #ADAPTANDO LAS CARACTERISTICAS PARA HACER MAS FACIL LA COMPARACION
    #Facturacion

        el_real["facturacion"] =  mayusculiza(el_ayudante["facturacion"])

    #Dias de vencimiento despues del corte
        if el_ayudante["dias_de_vencimiento"] == "no encontrado":
            el_real["diasDeVencimientoDespuesDelCorte"] = ""
        else:
            el_real["diasDeVencimientoDespuesDelCorte"] = sacar_entero(el_ayudante["dias_de_vencimiento"])

    #Tasa de interes
        if el_real["tasaDeInteresAnualEnPesos"] != "":
            propiedad_sin_verificar = el_real["tasaDeInteresAnualEnPesos"]
            propiedad_verificada = el_ayudante["tasa_de_interes_en_rd"]
            if propiedad_verificada != "n/a":
                propiedad_verificada = sacar_entero(convertir_float(propiedad_verificada))
                if propiedad_sin_verificar != propiedad_verificada:
                    el_real["tasaDeInteresAnualEnPesos"] = propiedad_verificada
            else:
                el_real["tasaDeInteresAnualEnPesos"] = 0
    #Nivel de ingreso no se toma en cuenta
        if el_real["nivelDeIngreso"] != "":
            propiedad_sin_verificar = el_real["nivelDeIngreso"]
            propiedad_verificada = el_ayudante["ingreso_minimo"]
            if propiedad_verificada != "no encontrado":
                propiedad_verificada = sacar_entero(propiedad_verificada)
                if str(propiedad_verificada) not in propiedad_sin_verificar:
                    el_real["nivelDeIngreso"] = str(propiedad_verificada)
            else:
                el_real["nivelDeIngreso"] = ""
    #Tasa de interes en dolares
        propiedad_verificada = el_ayudante["tasa_de_interes_en_us"]
        propiedad_sin_verificar = el_real["tasaDeInteresAnualEnDolares"]
        if propiedad_verificada != "n/a":
            propiedad_verificada = sacar_entero(convertir_float(propiedad_verificada))
            if propiedad_verificada != propiedad_sin_verificar:
                el_real["tasaDeInteresAnualEnDolares"] = propiedad_verificada
        else:
            el_real["tasaDeInteresAnualEnDolares"] = 0


    #CARGO POR EMISION
        if "rd$" in el_ayudante["cargo_por_emision"] and "usd" in el_ayudante["cargo_por_emision"]:
            dos_valores = []
            splitters = ["/","-","o","+"]
            for e in splitters:
                if el_ayudante["cargo_por_emision"].count(e) > 0:
                    dos_valores = el_ayudante["cargo_por_emision"].split(e)
                    break
            if "rd$" in dos_valores[0] and "usd" in dos_valores[1]:
                emision_en_pesos = sacar_entero(dos_valores[0])
                emision_en_dolares = sacar_entero(dos_valores[1])
            elif "usd" in dos_valores[0] and "rd$" in dos_valores[1]:
                emision_en_dolares = sacar_entero(dos_valores[0])
                emision_en_pesos = sacar_entero(dos_valores[1])
            el_real["cargoPorEmisionEnPesos"] = emision_en_pesos
            el_real["cargoPorEmisionEnDolares"] = emision_en_dolares

        elif "rd$" in el_ayudante["cargo_por_emision"]:
            emision_en_pesos = sacar_entero(el_ayudante["cargo_por_emision"])
            el_real["cargoPorEmisionEnPesos"] = emision_en_pesos
            el_real["cargoPorEmisionEnDolares"] = 0
        elif "usd" in el_ayudante["cargo_por_emision"]:
            emision_en_dolares = sacar_entero(el_ayudante["cargo_por_emision"])
            el_real["cargoPorEmisionEnPesos"] = 0
            el_real["cargoPorEmisionEnDolares"] = sacar_entero(el_ayudante["cargo_por_emision"])
        else:
            el_real["cargoPorEmisionEnPesos"] = ""
            el_real["cargoPorEmisionEnDolares"] = ""

    #CARGO POR RENOVACION
        if "rd$" in el_ayudante["renovacion_anual"] and "usd" in el_ayudante["renovacion_anual"]:
            dos_valores = []
            splitters = ["/","-","o","+"]
            for e in splitters:
                if el_ayudante["renovacion_anual"].count(e) > 0:
                    dos_valores = el_ayudante["renovacion_anual"].split(e)
                    break
            if "rd$" in dos_valores[0] and "usd" in dos_valores[1]:
                renovacion_en_pesos = sacar_entero(dos_valores[0])
                renovacion_en_dolares = sacar_entero(dos_valores[1])
            elif "usd" in dos_valores[0] and "rd$" in dos_valores[1]:
                renovacion_en_dolares = dos_valores[0]
                renovacion_en_pesos = dos_valores[1]
            el_real["renovacionAnualEnPesos"] = renovacion_en_pesos
            el_real["renovacionAnualEnDolares"] = renovacion_en_dolares

        elif "rd$" in el_ayudante["renovacion_anual"]:
            renovacion_en_pesos = sacar_entero(el_ayudante["renovacion_anual"])
            el_real["renovacionAnualEnPesos"] = renovacion_en_pesos
            el_real["renovacionAnualEnDolares"] = 0
        elif "usd" in el_ayudante["renovacion_anual"]:
            renovacion_en_dolares = sacar_entero(el_ayudante["renovacion_anual"])
            el_real["renovacionAnualEnPesos"] = 0
            el_real["renovacionAnualEnDolares"] = sacar_entero(el_ayudante["renovacion_anual"])
        else:
            el_real["renovacionAnualEnPesos"] = ""
            el_real["renovacionAnualEnDolares"] = ""

                    ##FIJO O VARIABLE## 
        if "%" in el_ayudante["cargo_por_sobregiro"]:
            el_real["cargoPorSobregiro"] = "Porcentaje"
        else:
            el_real["cargoPorSobregiro"] = "Fijo"

        if "%" in el_ayudante["cargo_por_mora"]:
            el_real["cargoPorMora"] = "Porcentaje"
        else:
            el_real["cargoPorMora"] = "Fijo"
    #SEGURO PROTECCION
        if "rd$" in el_ayudante["seguro_robo_o_perdida"] and "usd" in el_ayudante["seguro_robo_o_perdida"]:
            dos_valores = []
            splitters = ["/","-","o","+"]
            for e in splitters:
                if el_ayudante["seguro_robo_o_perdida"].count(e) > 0:
                    dos_valores = el_ayudante["seguro_robo_o_perdida"].split(e)
                    break
            if "rd$" in dos_valores[0] and "usd" in dos_valores[1]:
                proteccion_en_pesos = sacar_entero(dos_valores[0])
                proteccion_en_dolares = sacar_entero(dos_valores[1])
            elif "usd" in dos_valores[0] and "rd$" in dos_valores[1]:
                proteccion_en_dolares = dos_valores[0]
                proteccion_en_pesos = dos_valores[1]
            el_real["seguroDeProteccionEnPesos"] = proteccion_en_pesos
            el_real["seguroDeProteccionEnDolares"] = proteccion_en_dolares

        elif "rd$" in el_ayudante["seguro_robo_o_perdida"]:
            proteccion_en_pesos = sacar_entero(el_ayudante["seguro_robo_o_perdida"])
            el_real["seguroDeProteccionEnPesos"] = proteccion_en_pesos
            el_real["seguroDeProteccionEnDolares"] = 0
        elif "usd" in el_ayudante["seguro_robo_o_perdida"]:
            proteccion_en_dolares = sacar_entero(el_ayudante["seguro_robo_o_perdida"])
            el_real["seguroDeProteccionEnPesos"] = 0
            el_real["seguroDeProteccionEnDolares"] = sacar_entero(el_ayudante["seguro_robo_o_perdida"])
        else:
            el_real["seguroDeProteccionEnPesos"] = ""
            el_real["seguroDeProteccionEnDolares"] = ""

    #CARGO POR SOBREGIRO
        if "rd$" in el_ayudante["cargo_por_sobregiro"] and "usd" in el_ayudante["cargo_por_sobregiro"]:
            dos_valores = []
            splitters = ["/","-","o","+", "y"]
            for e in splitters:
                if el_ayudante["cargo_por_sobregiro"].count(e) > 0:
                    dos_valores = el_ayudante["cargo_por_sobregiro"].split(e)
                    break

            if "rd$" in dos_valores[0] and "usd" in dos_valores[1]:
                sobregiro_en_pesos = dos_valores[0]
                sobregiro_en_dolares = dos_valores[1]
            elif "usd" in dos_valores[0] and "rd$" in dos_valores[1]:
                sobregiro_en_pesos = dos_valores[1]
                sobregiro_en_dolares = dos_valores[0]

            if el_real["cargoPorSobregiro"] != "Porcentaje":
                el_real["cargoPorSobregiroFijoEnPesos"] = sacar_entero(sobregiro_en_pesos)
                el_real["cargoPorSobregiroFijoEnDolares"] = sacar_entero(sobregiro_en_dolares)
            else:
                el_real["cargoPorSobregiroVariableEnPesos"] = convertir_float(sobregiro_en_pesos)
                el_real["cargoPorSobregiroVariableEnDolares"] = convertir_float(sobregiro_en_dolares)
                el_real["cargoPorSobregiroFijoEnPesos"] = 0
                el_real["cargoPorSobregiroFijoEnDolares"] = 0


        elif "rd$" in el_ayudante["cargo_por_sobregiro"]:
            sobregiro_en_pesos = el_ayudante["cargo_por_sobregiro"]
            if el_real["cargoPorSobregiro"] != "Porcentaje":
                el_real["cargoPorSobregiroFijoEnPesos"] = sacar_entero(sobregiro_en_pesos)
                el_real["cargoPorSobregiroFijoEnDolares"] = 0
            else:
                el_real["cargoPorSobregiroVariableEnPesos"] = convertir_float(sobregiro_en_pesos)
                el_real["cargoPorSobregiroVariableEnDolares"] = 0
                el_real["cargoPorSobregiroFijoEnPesos"] = 0
                el_real["cargoPorSobregiroFijoEnDolares"] = 0

        elif "%" in el_ayudante["cargo_por_sobregiro"] and "rd$" not in el_ayudante["cargo_por_sobregiro"] and "usd" not in el_ayudante["cargo_por_sobregiro"]:
            sobregiro_en_pesos = el_ayudante["cargo_por_sobregiro"]
            if el_real["cargoPorSobregiro"] != "Porcentaje":
                el_real["cargoPorSobregiroFijoEnPesos"] = sacar_entero(sobregiro_en_pesos)
                el_real["cargoPorSobregiroFijoEnDolares"] = 0
            else:
                el_real["cargoPorSobregiroVariableEnPesos"] = convertir_float(sobregiro_en_pesos)
                el_real["cargoPorSobregiroVariableEnDolares"] = 0
                el_real["cargoPorSobregiroFijoEnPesos"] = 0
                el_real["cargoPorSobregiroFijoEnDolares"] = 0

        elif "usd" in el_ayudante["cargo_por_sobregiro"]:
            sobregiro_en_dolares = el_ayudante["cargo_por_sobregiro"]
            if el_real["cargoPorSobregiro"] != "Porcentaje":
                el_real["cargoPorSobregiroFijoEnPesos"] = 0
                el_real["cargoPorSobregiroFijoEnDolares"] = sacar_entero(sobregiro_en_dolares)
            else:
                el_real["cargoPorSobregiroVariableEnPesos"] = 0
                el_real["cargoPorSobregiroVariableEnDolares"] = convertir_float(sobregiro_en_dolares)
                el_real["cargoPorSobregiroFijoEnPesos"] = 0
                el_real["cargoPorSobregiroFijoEnDolares"] = 0
        else:
            el_real["cargoPorSobregiroVariableEnPesos"] = ""
            el_real["cargoPorSobregiroVariableEnDolares"] = ""
            el_real["cargoPorSobregiroFijoEnPesos"] = ""
            el_real["cargoPorSobregiroFijoEnDolares"] = ""

    #CARGO POR MORA
        if "rd$" in el_ayudante["cargo_por_mora"] and "usd" in el_ayudante["cargo_por_mora"]:
            dos_valores = []
            splitters = ["/","-","o","+", "y"]
            for e in splitters:
                if el_ayudante["cargo_por_mora"].count(e) > 0:
                    dos_valores = el_ayudante["cargo_por_mora"].split(e)
                    break
                
            if "rd$" in dos_valores[0] and "usd" in dos_valores[1]:
                mora_en_pesos = dos_valores[0]
                mora_en_dolares = dos_valores[1]
            elif "usd" in dos_valores[0] and "rd$" in dos_valores[1]:
                mora_en_pesos = dos_valores[1]
                mora_en_dolares = dos_valores[0]

            if el_real["cargoPorMora"] != "Porcentaje":
                el_real["cargoPorMoraFijoEnPesos"] = sacar_entero(mora_en_pesos)
                el_real["cargoPorMoraFijoEnDolares"] = sacar_entero(mora_en_dolares)
            else:
                el_real["cargoPorMoraVariableEnPesos"] = convertir_float(mora_en_pesos)
                el_real["cargoPorMoraVariableEnDolares"] = convertir_float(mora_en_dolares)
                el_real["cargoPorMoraFijoEnPesos"] = 0
                el_real["cargoPorMoraFijoEnDolares"] = 0


        elif "rd$" in el_ayudante["cargo_por_mora"]:
            mora_en_pesos = el_ayudante["cargo_por_mora"]
            if el_real["cargoPorMora"] != "Porcentaje":
                el_real["cargoPorMoraFijoEnPesos"] = sacar_entero(mora_en_pesos)
                el_real["cargoPorMoraFijoEnDolares"] = 0
            else:
                el_real["cargoPorMoraVariableEnPesos"] = convertir_float(mora_en_pesos)
                el_real["cargoPorMoraVariableEnDolares"] = 0
                el_real["cargoPorMoraFijoEnPesos"] = 0
                el_real["cargoPorMoraFijoEnDolares"] = 0


        elif "usd" in el_ayudante["cargo_por_mora"]:
            mora_en_dolares = el_ayudante["cargo_por_mora"]
            if el_real["cargoPorMora"] != "Porcentaje":
                el_real["cargoPorMoraFijoEnPesos"] = 0
                el_real["cargoPorMoraFijoEnDolares"] = sacar_entero(mora_en_dolares)
            else:
                el_real["cargoPorMoraVariableEnPesos"] = 0
                el_real["cargoPorMoraVariableEnDolares"] = convertir_float(sobregiro_en_dolares)
                el_real["cargoPorMoraFijoEnPesos"] = 0
                el_real["cargoPorMoraFijoEnDolares"] = 0
        else:
            el_real["cargoPorMoraVariableEnPesos"] = ""
            el_real["cargoPorMoraVariableEnDolares"] = ""
            el_real["cargoPorMoraFijoEnPesos"] = ""
            el_real["cargoPorMoraFijoEnDolares"] = ""

        avance_efectivo = el_ayudante["avance_de_efectivo"]
        dos_valores = []
        if avance_efectivo != "n/a":
            splitters = ["/","-","o","+"]
            for e in splitters:
                if avance_efectivo.count(e) > 0:
                    dos_valores = avance_efectivo.split(e)
                    break
            if dos_valores == []:
                el_real["avanceDeEfectivo"] = convertir_float(avance_efectivo)
            else:
                el_real["avanceDeEfectivo"] = convertir_float(dos_valores[0])
        else:
            el_real["avanceDeEfectivo"] = ""



    #Recompensas
        if el_ayudante["plan_de_lealtad"] != "no encontrado":
            lealtad_rexi = info["unidadDeRecompensa"].lower() if info["unidadDeRecompensa"] != None else ""
            lealtad_publica = el_ayudante["plan_de_lealtad"].lower()

            if (lealtad_rexi in lealtad_publica) or (lealtad_publica in lealtad_rexi) or (lealtad_rexi == lealtad_publica):
                el_real["unidadDeRecompensa"] = info["unidadDeRecompensa"]
            else:
                el_real["unidadDeRecompensa"] = mayusculiza(lealtad_publica)
            if el_ayudante["recompensa"] == "no encontrado":
                propiedades = ["consumoMinimoParaGenerarUnidad","monedaDelConsumoMinimo","unidadesGeneradasPorConsumoMinimo","establecimientosQueGeneranUnidadesExtra", "establecimientos"]
                for e in propiedades:
                    el_real[e] = ""

        else:
            propiedades = ["unidadDeRecompensa","consumoMinimoParaGenerarUnidad","monedaDelConsumoMinimo","unidadesGeneradasPorConsumoMinimo","establecimientosQueGeneranUnidadesExtra", "establecimientos"]
            for e in propiedades:
                el_real[e] = ""

        this_three = ["minimoDeUnidadesParaCanje", "valorEnPesosDelCanjeMinimo","mesesDeVigencia","bonoDeUnidadesPorEmision","montoDelBono"]
        for e in this_three:
            el_real[e] = ""
            
        el_real["pagoDeMembresia"] = True if el_ayudante["pago_de_membresia"] == "si" else False
        el_real["vencimientoDeUnidades"] = True if el_ayudante["vencimiento_de_unidades"] == "si" else False


    #descuentos
        el_real["descuentosOcacionales"] = True if el_ayudante["catalogo_de_descuentos_ocasionales"] == "si" else False
        el_real["catalogoDeDescuentosOcacionales"] = ""

        descuentos_especificos_publica = el_ayudante["descuento_en_comercios_especificos"]
        descuentos_especificos_rexi = info["comerciosEnEspecifico"]
        descuento_maximo = el_ayudante["descuento_maximo_en_comercios"]

        if descuentos_especificos_publica != "no":
            descuentos_especificos_publica = mayusculiza(descuentos_especificos_publica)
            el_real["descuentoEnComerciosEspecificos"] = True
            el_real["comerciosEnEspecifico"] = descuentos_especificos_publica
            el_real["descuentoMaximoEnComercios"] = sacar_entero(descuento_maximo) if descuento_maximo != "no encontrado" else 0

            
        else:
            el_real["descuentoEnComerciosEspecificos"] = False
            el_real["comerciosEnEspecifico"] = "No"
            el_real["descuentoMaximoEnComercios"] = 0
            el_real["alcanceDelDescuento"] = ""


        tipo_comercio = el_ayudante["descuentos_por_tipo_de_comercio"] 

        el_real["descuentosPorTipoDeComercio"] = True if tipo_comercio != "n/a"  else False
        el_real["tiposDeComercios"] = "No" if el_real["descuentosPorTipoDeComercio"] == False else mayusculiza(tipo_comercio)
        el_real["descuentoMaximoPorTipoDeComercio"] = 0 if el_real["descuentosPorTipoDeComercio"] == False else info["descuentoMaximoPorTipoDeComercio"]

        el_real["historialDeCreditoMinimoOReducido"] = ""

    #primera tarjeta
        el_real["enfoqueExclusivoParaJovenes"] = ""
        el_real["programaParaIniciarElCredito"] = ""

        el_real["lineaAereaVinculada"] = "" if el_ayudante["linea_aerea_vinculada"] == "ninguna" else mayusculiza(el_ayudante["linea_aerea_vinculada"])
        el_real["accesoASalasVIPEnAeropuertos"] = False if el_ayudante["priority_pass"] == "no" else True
        el_real["beforeBoarding"] = False if el_ayudante["before_boarding"] == "dato no encontrado" else True
        el_real["serviciosDeAsistenciaDeViajes"] = False if el_ayudante["servicios_de_asistencia_de_viajes"] == "dato no encontrado" else True
        el_real["serviciosDeAsistenciaPersonalConcierge"] = False if el_ayudante["servicios_de_asistencia_personal"] == "no encontrado" else True
        el_real["seguroDeAccidenteEnViajes"] = False if el_ayudante["seguro_en_accidentes_de_viaje"] == "no encontrado" else True
        el_real["seguroDeAccidenteEnDestinoDeViaje"] = False if el_ayudante["seguro_en_accidentes_en_destino_de_viaje"] == "no encontrado" else True
        el_real["seguroDeAutosAlquilados"] = False if el_ayudante["seguro_de_autos_alquilados"] == "no encontrado" else True
        el_real["seguroContraDemoraDeEquipaje"] = False if el_ayudante["seguro_contra_demora_de_equipaje"] == "no" else True
        el_real["seguroContraPerdidaDeEquipaje"] = False if el_ayudante["seguro_contra_perdida_de_equipaje"] == "no" else True
        el_real["seguroContraDemoraDeViaje"] = False if el_ayudante["seguro_contra_demora_de_viaje"] == "no" else True
        el_real["seguroContraCancelacionDeViaje"] = False if el_ayudante["seguro_contra_cancelacion_de_viaje"] == "no" else True
        el_real["seguroContraPerdidaDeConexion"] = False if el_ayudante["seguro_contra_perdida_de_conexion"] == "no" else True
        el_real["servicioDeEmergenciaMedicaInternacional"] = False if el_ayudante["emergencia_medica_internacional"] == "no encontrado" else True
        el_real["proteccionDeCompras"] = False if el_ayudante["proteccion_de_compras"] == "no" else True
        el_real["proteccionDePrecios"] = False if el_ayudante["proteccion_de_precios"] == "no" else True
        el_real["adelantoDeEfectivoDeEmergencia"] = False if el_ayudante["adelanto_efectivo_emergencia"] == "no encontrado" else True
        el_real["proteccionRoboEnCajeros"] = ""

    #Negocios
        
        el_real["enfoqueEmpresarialYoPYMEs"] = True if el_ayudante["enfoque_empresas"] == "si" else False
        el_real["herramientaParaControlDeGastos"] = ""
        el_real["servicioDeAsistenciaANegocios"] = ""
        el_real["nombreDelServicio"] = ""

    #Credito Diferido

        el_real["creditoDiferidoDisponible"] = True if el_ayudante["credito_diferido"] != "dato no encontrado" else False
        el_real["restringidoAUnEstablecimientoEspecifico"] = ""
        el_real["establecimientosPermitidos"] == "" if el_ayudante["establecimientos_permitidos"] == "dato no encontrado" else info[e]
        el_real["montoMinimoDeCompra"] = ""
        el_real["minimoDeCuotasPermitidas"] = "" if el_ayudante["minimo_de_cuotas_permitidas"] == "no encontrado" else sacar_entero(el_ayudante["minimo_de_cuotas_permitidas"])
        el_real["maximoDeCuotasPermitidas"] = "" if el_ayudante["cantidad_de_cuotas_permitidas"] == "no encontrado" else sacar_entero(el_ayudante["cantidad_de_cuotas_permitidas"])
        el_real["tasaDeInteresAnualDelCreditoDiferido"] = "" if el_ayudante["tasa_de_interes_del_credito_diferido"] == "dato no encontrado" else sacar_entero(el_ayudante["tasa_de_interes_del_credito_diferido"])
        el_real["requiereUnPlasticoAdicional"] = False if el_ayudante["utiliza_tarjeta_separada"] == "no encontrado" else True
        el_real["porcentajeDisponibleSobreElLimitePrincipal"] = 0 if el_ayudante["porcentaje_sobre_limite"] == "no encontrado" else sacar_entero(el_ayudante["porcentaje_sobre_limite"])
        el_real["permiteAvanceDeEfectivo"] = ""
        el_real["comisionPorAvanceDeEfectivo"] = ""
        el_real["permiteDepositoEnGarantia"] = False if el_ayudante["permite_garantia"] == "no encontrado" else True

    #Recuperacion del credito
        nones = ["programaDeEducacionFinanciera", "programaParaRecuperacionDelCredito", "nombreDelProgramaDeRecuperacionDelCredito", "nombreDelProgramaDeEducacionFinanciera"]
        for e in nones:
            el_real[e] = ""

    #Afinidad
        el_real["marcaCompartidaConUnaInstitucionOEmpresa"] = True if el_ayudante["institucion_o_empresa"] != "no encontrado" else False
        el_real["nombreDeLaInstitucionOEmpresa"] = "" if el_real["marcaCompartidaConUnaInstitucionOEmpresa"] == False else info["nombreDeLaInstitucionOEmpresa"]
        el_real["beneficioOValorAgregadoPorAfinidad"] = ""
        el_real["beneficioOValorAgregado"] = ""

    #Combustible
        el_real["destinadaExclusivamenteALaCompraDeCombustibles"] = True if el_ayudante["destinada_combustible"] == "si" else False



















        




        #COMPARACION
        for e in info:
            if el_real[e] == info[e]:
                la_comparacion[e] = "OK"
            if el_real[e] != info[e]:
                la_comparacion[e] = "Diferente"
            if el_real[e] == "" and info[e] != "":
                la_comparacion[e] = "No encontrado"
            if el_real[e] != "" and info[e] == "":
                la_comparacion[e] = "No registrado"
            if (el_real[e] == 0 and info[e]) == "" or (el_real[e] == "" and info[e] == 0) or (el_real[e] == "" and (info[e] == "" or info[e] == None or info[e] == "No")):
                la_comparacion[e] = "No aplica"

        memcache.set(str(info["id"]),[info,el_real,la_comparacion])
        cache = memcache.get(str(info["id"]))


        
    return cache


def BuscarInformacion(clave,donde):
    informacion = ""
    donde = donde.lower()
    if clave == "nombre":
        informacion = donde[:donde.find("-")-1]
    if clave =="banco":
        informacion = donde[donde.find("-")+2:donde.find(",",donde.find("-"))]
    if clave == "facturacion":
        if donde.count("usd") >= 2 and donde.count("rd$") == 0:
            informacion = "dolares"
        elif donde.count("rd$") >= 2 and donde.count("usd") == 0:
            informacion = "pesos"
        elif donde.count("usd") >= 1 and donde.count("rd$") >= 1:
            informacion = "doble saldo"
        else:
            informacion = "pesos"

        
    if clave == "tasa_de_interes_en_rd":
        informacion = donde[:donde.find("beneficios:")]
        informacion = informacion.split(",")
        for e in informacion:
            if (("tasa" in e or "cargo" in e) and "financiamiento" in e) or (("tasa" in e or "cargo" in e) and "interes" in e) or ("interes" in e and "financiamiento" in e):
                if "rd" in e or "usd" in e:
                    if "rd" in e:
                        informacion = e
                        break
                else:
                    informacion = e
                    break

        if type(informacion) != list:
            informacion = informacion[informacion.find("|")+1:]
            informacion_old = informacion
            splitters = ["/","-","+", "o"]
            for e in splitters:
                if informacion.count(e) > 0:
                    informacion = informacion.split(e)
                    break
            if type(informacion) != list:
                informacion = informacion_old
            else:
                informacion = informacion[1] if "rd" in informacion[1] else informacion[0]
        else:
            informacion = "n/a"

    if clave == "tasa_de_interes_en_us":
        informacion = donde[:donde.find("beneficios:")]
        informacion = informacion.split(",")
        for e in informacion:
            if (("tasa" in e or "cargo" in e) and "financiamiento" in e) or (("tasa" in e or "cargo" in e) and "interes" in e) or ("interes" in e and "financiamiento" in e):
                if "rd" in e or "usd" in e:
                    if "usd" in e:
                        informacion = e
                        break
                else:
                    informacion = e
                    break
        if type(informacion) != list and donde.count("usd") >= 1:
            informacion = informacion[informacion.find("|")+1:]
            informacion_old = informacion
            splitters = ["/","-","+", "o"]
            for e in splitters:
                if informacion.count(e) > 0:
                    informacion = informacion.split(e)
                    break
            if type(informacion) != list:
                informacion = informacion_old
            else:
                informacion = informacion[1] if "usd" in informacion[1] else informacion[0]
        else:
            informacion = "usd$0"
        
       
    if clave == "cargo_por_emision":
        informacion = donde[:donde.find("beneficios:")]
        informacion = informacion.split(",")
        informacion2 = donde[donde.find("beneficios:"):donde.find("||")]
        informacion2 = informacion2.split(".")
        benefit = False
        if "emision|" not in donde:
            informacion = "rd$0"
        else:
            for e in informacion:
                if "emision|" in e and "adicional" not in e:
                    informacion = e
                    break
            if type(informacion) == list:
                informacion = "n/a"
            else:
                for e in informacion2:
                    if "adicional" not in e and u"emisión" in e and ("grat" in e or "cost" in e) and not u"primer año" in e:
                        benefit = True
                        break
                informacion = informacion[informacion.find("|")+1:]
                if "gratis" in informacion or benefit == True:
                    informacion = "rd$0"

        if "emision_internacional" in donde:
            internacional = donde[donde.find("emision_internacional")+len("emision_internacional")+1:donde.find(",", donde.find("emision_internacional"))]
            if "/" in internacional:
                internacional = internacional.split("/")[0]
            informacion += "/" + internacional

    if clave == "renovacion_anual":
        informacion = donde[:donde.find("beneficios:")]
        informacion = informacion.split(",")
        informacion2 = None
        mensual = False
        for e in informacion:
            if "renovacion|" in e:
                informacion = e
                if "mensual" in informacion:
                    mensual = True
            if "renovacion_internacional|" in e:
                informacion2 = e

        if type(informacion) == list:
            informacion = "n/a"
        else:
            informacion = informacion[informacion.find("|")+1:]
            if informacion == "gratis":
                informacion = "rd$0"
            if mensual == True:
                informacion = informacion + " (mensual)"
            if informacion2 != None:
                informacion2 = informacion2[informacion2.find("|")+1:]
                if "/" in informacion2:
                    informacion2 = informacion2.split("/")
                    informacion = informacion + "/" + informacion2[0]
                else:
                    informacion = informacion + "/" + informacion2


    if clave == "seguro_robo_o_perdida":
        informacion = donde[:donde.find("beneficios:")]
        informacion = informacion.split(",")
        for e in informacion:
            if (("seguro" in e or "cargo" in e or "proteccion" in e or "reposicion" in e) and ("perdida" in e or "rob" in e or "proteccion" in e) and ("plastico" not in e and "reemplazo" not in e)):
                informacion = e
        if type(informacion) == list:
            informacion = "n/a"
        else:
            informacion = informacion[informacion.find("|")+1:]
    if clave == "avance_de_efectivo":
        informacion = donde[:donde.find("beneficios:")]
        informacion = informacion.split(",")
        for e in informacion:
            if ("avance" in e and "efectivo" in e):
                informacion = e
                break
        if type(informacion) == list:
            informacion = "n/a"
        else:
            informacion = informacion[informacion.find("|")+1:]
    if clave == "cargo_por_sobregiro":
        informacion = donde[:donde.find("beneficios:")]
        informacion = informacion.split(",")
        for e in informacion:
            if "sobregiro" in e:
                informacion = e
                break
        if type(informacion) == list:
            informacion = "no encontrado"
        else:
            informacion = informacion[informacion.find("|")+1:].replace("m","").replace("a","")
    if clave == "cargo_por_mora":
        informacion = donde[:donde.find("beneficios:")]
        informacion = informacion.split(",")
        for e in informacion:
            if "mora" in e:
                informacion = e
                break
        if type(informacion) == list:
            informacion = "n/a"
        else:
            informacion = informacion[informacion.find("|")+1:].replace("m","").replace("a","")
    if clave == "pago_de_membresia":
        if "bancam" in donde or "caribe" in donde or "santa cruz" in donde:
            informacion = "si"
        else:
            informacion = "no"

    if clave == "seguro_de_autos_alquilados":
        informacion = donde[donde.find("beneficios:"):donde.find("||")]
        informacion = informacion.split(".")
        for e in informacion:
            if ("seguro" in e and ("auto" or u"vehículo") in e and "alquil" in e) or (("auto" in e or u"vehículo" in e) and "alquil" in e): 
                informacion = e
                break
        if type(informacion) == list:
            informacion = "no encontrado"
        else:
            informacion = "si"

    if clave == "seguro_en_accidentes_de_viaje":
        informacion = donde[donde.find("beneficios:"):donde.find("||")]
        informacion = informacion.split(".")
        for e in informacion:
            if ("seguro" in e and "accidente" in e and "viaje" in e) or ("accidente" in e and "viaje" in e) or ("seguro" in e and "accidente" in e) and " nacional" not in e:
                informacion = e
                break
        if type(informacion) == list:
            informacion = "no encontrado"
        else:
            informacion = "si"
    if clave == "seguro_en_accidentes_en_destino_de_viaje":
        informacion = donde[donde.find("beneficios:"):donde.find("||")]
        informacion = informacion.split(".")
        for e in informacion:
            if ("seguro" in e and "accidente" in e and "destino" in e and "viaje" in e) or ("destino" in e and "accidente" in e and "viaje" in e):
                informacion = e
                break
        if type(informacion) == list:
            informacion = "no encontrado"
        else:
            informacion = "si"

    if clave == "seguro_contra_demora_de_equipaje":
        informacion = donde[donde.find("beneficios:"):donde.find("||")]
        if informacion.count(u"•") != 0:
            informacion = informacion.split(u"•")
        else:
            informacion = informacion.split(".")
        for e in informacion:
            if ("seguro" in e and "demora" in e and "equip" in e) or ("demora" in e and "equip" in e):
                informacion = e
                break
        if type(informacion) == list:
            informacion = "no"
        else:
            informacion = "si"

    if clave == "seguro_contra_perdida_de_equipaje":
        informacion = donde[donde.find("beneficios:"):donde.find("||")]
        informacion = informacion.split(".")
        for e in informacion:
            if ("seguro" in e and u"pérdida" in e and "equipaje" in e) or ((u"pérdida" in e or "extrav" in e) and "equip" in e):
                informacion = e
                break
        if type(informacion) == list:
            informacion = "no"
        else:
            informacion = "si"

    if clave == "seguro_contra_demora_de_viaje":
        informacion = donde[donde.find("beneficios:"):donde.find("||")]
        informacion = informacion.split(".")
        for e in informacion:
            if ("seguro" in e and "demora" in e and ("viaje" in e or "vuelo" in e)) or ("demora" in e and ("viaje" in e or "vuelo" in e)):
                informacion = e
                break
        if type(informacion) == list:
            informacion = "no"
        else:
            informacion = "si"


    if clave == "seguro_contra_cancelacion_de_viaje":
        informacion = donde[donde.find("beneficios:"):donde.find("||")]
        informacion = informacion.split(".")
        for e in informacion:
            if ("seguro" in e and u"cancela" in e and ("viaje" in e or "vuelo" in e)) or (u"cancela" in e and ("viaje" in e or "vuelo" in e)):
                informacion = e
                break
        if type(informacion) == list:
            informacion = "no"
        else:
            informacion = "si"

    if clave == "seguro_contra_perdida_de_conexion":
        informacion = donde[donde.find("beneficios:"):donde.find("||")]
        informacion = informacion.split(".")
        for e in informacion:
            if ("seguro" in e and u"pérdida" in e and "conex" in e) or (u"pérdida" in e and "conex" in e):
                informacion = e
                break
        if type(informacion) == list:
            informacion = "no"
        else:
            informacion = "si"

    if clave == "emergencia_medica_internacional":
        informacion = donde[donde.find("beneficios:"):donde.find("||")]
        informacion = informacion.split(".")
        for e in informacion:
            if "emergencia" in e and u"médic" in e and ("internacional" in e or "internacional" not in e) and " nacional" not in e:
                informacion = e
                break
        if type(informacion) == list:
            informacion = "no encontrado"
        else:
            informacion = "si"
    if clave == "proteccion_de_compras":
        informacion = donde[donde.find("beneficios:"):donde.find("||")]
        informacion = informacion.split(".")
        for e in informacion:
            if "protecc" in e and "compra" in e:
                informacion = e
                break
        if type(informacion) == list:
            informacion = "no"
        else:
            informacion = "si"
    if clave == "proteccion_de_precios":
        informacion = donde[donde.find("beneficios:"):donde.find("||")]
        informacion = informacion.split(".")
        for e in informacion:
            if "protecc" in e and "precio" in e:
                informacion = e
                break
        if type(informacion) == list:
            informacion = "no"
        else:
            informacion = "si"
    if clave == "descuento_en_comercios_especificos":
        beneficios = donde[donde.find("beneficios:"):donde.find("||")]
        if (("descuento" in beneficios) or ("reembolso" in beneficios) or "ahorr" in beneficios or u"devolución" in donde) and "%" in beneficios:
            if "bm cargo" in donde:
                informacion = "bm cargo"
            elif "anthony's" in donde:
                informacion = "anthony's"
            elif "unase" in donde:
                informacion = "supermercados unase"
            elif u"hipermercados olé" in donde:
                informacion = u"hipermercados olé"
            elif u"unión local" in donde or u"unión internacional" in donde:
                informacion = u"farmacias unión" 
            elif "gold's gym" in donde:
                informacion = "gold's gym"
            elif "club hemingway" in donde:
                informacion = "club hemingway"
            elif "club naco" in donde:
                informacion = "club naco"
            elif u"casa de españa" in donde:
                informacion = u"casa de españa"
            elif "pricesmart" in donde:
                informacion = "clubes pricesmart"
            elif "bravo" in donde:
                informacion = "supermercados bravo"
            elif "ikea" in donde:
                informacion = "ikea"
            elif "almacenes iberia" in donde:
                informacion = "almacenes iberia"
            elif "autozama" in donde:
                informacion = "autozama"
            elif "la cadena" in donde:
                informacion = "supermercados la cadena"
            elif "plaza lama" in donde:
                informacion = "plaza lama"
            elif "skybox" in donde:
                informacion = "skybox"
            elif "nelly rent a car" in donde:
                informacion = "nelly rent a car"
            elif "la sirena" in donde and "pola " in donde:
                informacion = "la sirena y supermercados pola"
            elif "la sirena" in donde:
                informacion = "la sirena"
            
            else:
                informacion = "no"
        else:
            informacion = "no"
    if clave == "descuentos_por_tipo_de_comercio":
        beneficios = donde[donde.find("beneficios:"):donde.find("||")]
        if (("descuento" in beneficios) or ("reembolso" in beneficios) or "ahorr" in beneficios or u"devolución" in donde) and "%" in beneficios:
            if "la sirena" in donde or ("la sirena" in donde and "pola " in donde) or "nelly rent a car" in donde or "skybox" in donde or "plaza lama" in donde or "la cadena" in donde or "autozama" in donde or "almacenes iberia" in donde or "ikea" in donde or "bravo" in donde or "anthony's" in donde or "unase" in donde or u"hipermercados olé" in donde or (u"unión local" in donde or u"unión internacional" in donde) or "gold's gym" in donde or "club hemingway" in donde or "club naco" in donde or u"casa de españa" in donde or "pricesmart" in donde or "plaza central" in donde:
                informacion = "no"
            else:
                if "estadios" in donde:
                    informacion = "estadios de beisbol"
                elif "farmacias" in donde and "restaurantes" in donde:
                    informacion = "farmacias y restaurantes"
                elif "farmacias" in donde:
                    informacion = "farmacias"
                elif "servicio priority" in donde:
                    informacion = "servicio priority"

    if clave == "alcance_del_descuento":
        beneficios = donde[donde.find("beneficios:"):donde.find("||")]
        if (("descuento" in beneficios) or ("reembolso" in beneficios) or "ahorr" in beneficios or u"devolución" in donde) and "%" in beneficios:
            informacion = "si"
        else:
            informacion = "n/a"

    if clave == "descuento_maximo_en_comercios":
        if "descuento" in donde or "ahorr" or u"devolución" in donde:
            informacion = donde[donde.find("beneficios:"):donde.find("||")]
            informacion = informacion.split(".")
            maximo = ""
            for e in informacion:
                if "%" in e and ("descuento" in e or "ahorr" in e or "reembolso" in e or u"devolución" in e):
                    informacion = e
                    maximo =  maximo + informacion
            if type(informacion) != list:
                for letter in maximo:
                    if not letter.isdigit() and letter != "%":
                        maximo = maximo.replace(letter,"")
                maximo = maximo[:maximo.rfind("%")].split("%")
                maximo_lista = []
                for e in maximo:
                    maximo_lista.append(eval(e))
                informacion = str(max(maximo_lista))+"%"

            else:
                informacion = "no encontrado"
        else:
            informacion = "no encontrado"
    if clave == "plan_de_lealtad":
        if ("punto" in donde or "puntos" in donde) and "bhd" not in donde and "banesco" not in donde and "banreservas" not in donde and "promerica" not in donde and "membership reward" not in donde and "trueblue" not in donde and "pola " not in donde and "caribe" not in donde and not "bmcargopuntos" in donde:
            informacion = "puntos"
        elif "abonapunto" in donde:
            informacion = "abonapunto"
        elif "punto verde banesco" in donde or "puntos verdes banesco" in donde:
            informacion = "punto verde banesco"
        elif "puntos banreservas" in donde:
            informacion = "punto banreservas"
        elif "milla " in donde or "millas " in donde  and "free spirit" not in donde and "mileageplus" not in donde:
            informacion = "milla"
        elif "punto promerica" in donde or "puntos promerica" in donde:
            informacion = "punto promerica"
        elif "millas free spirit" in donde or "milla free spirit" in donde:
            informacion = "milla free spirit"
        elif "soles" in donde or " sol " in donde:
            informacion = "soles"
        elif "pesos caribe" in donde or "peso caribe" in donde:
            informacion = "pesos caribe"
        elif "facilito" in donde:
            informacion = "facilitos"
        elif "puntos reales" in donde or "punto real" in donde:
            informacion = "puntos reales"
        elif "bono" in donde:
            informacion = "bonos"
        elif "llave" in donde:
            informacion = "llaves"
        elif "membership reward" in donde:
            informacion = "membership reward point"
        elif "escudo" in donde:
            informacion = "escudos"
        elif "cerito" in donde:
            informacion = "ceritos"
        elif "trueblue" in donde:
            informacion = "trueblue"
        elif "pola punto" in donde:
            informacion = "pola puntos"
        elif u"punto siremás" in donde:
            informacion = u"punto siremás"
        elif "pasos" in donde:
            informacion = "pasos"
        elif "estrella" in donde:
            informacion = "estrellas"
        elif "punto" in donde and "promerica" in donde:
            informacion = "puntos promerica"
        elif "manos " in donde or "manos," in donde:
            informacion = "manos"
        else:
            informacion = "no encontrado"

    if clave == "vencimiento_de_unidades":
        if ("punto" in donde or "abonapunto" in donde or "milla " in donde or "bono" in donde or "llave" in donde or "estrella" in donde or "pasos" in donde or "manos" in donde or "soles" in donde or "sol " in donde):
            if ("unidades no vencen" in donde):
                informacion = "no"
            else: 
                informacion = "si"
        else:
            informacion = "no"


 

    if clave == "servicios_de_asistencia_personal":
        informacion = donde[donde.find("beneficios:"):donde.find("||")]
        informacion = informacion.split(".")
        for e in informacion:
            if ("asisten" in e and "personal" in e) or ("servicio" in e and "personal" in e) or ("concierge" in e):
                informacion = e
                break
        if type(informacion) == list:
            informacion = "no encontrado"
        else:
            informacion = "si"

    if clave =="permite_garantia":
        informacion = donde[donde.find("beneficios:"):donde.find("||")]
        informacion = informacion.split(".")
        for e in informacion:
            if u"garant" in e or (u"garant" in e and "extend" in e) or ("permite" in e and u"garant" in e):
                informacion = e
                break
        if type(informacion) == list:
            informacion = "no encontrado"
        else:
            informacion = "si"
    if clave == "utiliza_tarjeta_separada":
        informacion = ["tarjetas principales","tarjetas adicionales", "tarjeta adicional", "tarjeta principal", u"tarjeta de crédito adicional", u"tarjetas de crédito adicionales", "dos tarjetas"]
        for e in informacion:
            if e in donde:
                informacion = e
                break
        if type(informacion) == list:
            informacion = "no encontrado"
        else:
            informacion = "si"
    if clave == "priority_pass":
        informacion = donde[donde.find("beneficios:"):donde.find("||")]
        informacion = informacion.split(".")
        for e in informacion:
            if ("priority" in e and "pass" in e) or ("acceso" in e and "vip" in e):
                informacion = e
                break
        if type(informacion) == list:
            informacion = "no"
        else:
            informacion = "si"
    if clave == "dias_de_vencimiento":
        informacion = donde[donde.find("beneficios:"):donde.find("||")]
        informacion = informacion.split(".")
        for e in informacion:
            if ((u"después" in e or "luego" in e) and "corte" in e and u" días " in e) or (u" días " in e and "vencimiento" in e):
                informacion = e
        if type(informacion) == list:
            informacion = "no encontrado"
        else:
            informacion = informacion[informacion.find(u" días ")-3:informacion.find(u" días ")]
        

    if clave == "credito_diferido":
        beneficios = donde[donde.find("beneficios:"):donde.find("||")]
        beneficios = beneficios.split(".")
        for e in beneficios:
            if (u"línea" in e and "efectivo" in e) or (u"crédito" in e and "diferido" in e) or (("efectivo" in e) and (u"límite" in e or "limite" in e) or ("exced" in e and u"límite" in e)and ("%" in e)) or (("cuotas" in e and "meses" in e) or ("financia" in e and "meses" in e) or (u"límite" in e and "cuotas" in e)):
                beneficios = e
                break
        if type(beneficios) == list:
            informacion = "dato no encontrado"
        else:
            informacion = "si"
    if clave == "tasa_de_interes_del_credito_diferido":
        informacion = donde[:donde.find("beneficios:")]
        informacion = informacion.split(",")
        for e in informacion:
            if (u"línea" in e and "efectivo" in e) or (u"crédito" in e and "diferido" in e):
                informacion = e
                break
        if type(informacion) == list:
            informacion = "dato no encontrado"
        else:
            informacion = informacion[informacion.find("|")+1:]
    if clave == "recompensa":
        informacion = donde[donde.find("beneficios:"):donde.find("||")]
        if informacion.count("-") > 2:
            informacion = informacion.split("-")
        else:
            informacion = informacion.split(".")

        procede = False
        for e in informacion:
            if "programa de lealtad" in e or "programa de puntos" in e or "plan de lealtad" in e or ("por cada rd$" in e or "por cada peso" in e or u"por cada dólar" in e) or ("cada" in e and "consum" in e) or ("cada " in e and "rd$" in e):
                procede = True
        if procede == True:
            for e in informacion:
                if ((("por" in e and "cada" in e) or ("cada" in e and "consum" in e)) and ("rd$" in e or "%" in e) or ("por cada rd$" in e or "por cada peso" in e or u"por cada dólar" in e)) or "program" in e and "acumul" in e or ("cada" in e and "rd$" in e):
                    informacion = e
            if type(informacion) == list:
                informacion = "no encontrado"
        else:
            informacion = "no encontrado"
    if clave == "ingreso_minimo":
        informacion = donde[:donde.find("beneficios")]
        informacion = informacion.split(",")
        for e in informacion:
            if "ingreso" in e and u"mínimo" in e:
                informacion = e
                break
        if type(informacion) == list:
            informacion = "no encontrado"
        else:
            informacion = informacion[informacion.find("|")+1:]

    if clave == "linea_aerea_vinculada":
        aerolineas = db.GqlQuery("select * from Global_Instituciones").fetch(1)[0].aerolineas
        informacion = []
        for airline in aerolineas:
            if airline in donde:
                informacion = airline
        if type(informacion) == list:
            informacion = "ninguna"
        

    if clave == "before_boarding":
        informacion = donde[donde.find("beneficios:"):donde.find("||")]
        informacion = informacion.split(".")
        for e in informacion:
            if u"before boarding" in e or "salas vip" in e or "sala vip" in e:
                informacion = e
        if type(informacion) == list:
            informacion = "dato no encontrado"
        else:
            informacion = "si"
        

    if clave == "comercios_que_generan_unidades_extra":
        informacion = donde[donde.find("beneficios:"):donde.find("||")]
        informacion = informacion.split(".")
        puntos = ""
        for e in informacion:
            if "por compras" in e and ("punto" in e or "restaurant" in e or "trueblue" in e or ("la sirena" in e and "pola " in e) and ":" not in e):
                if "trueblue" in e:
                    informacion = "jetblue"
                elif "la sirena" in e and "pola " in e:
                    informacion = "la sinera y supermercados pola"
                elif "restaurantes" in e:
                    informacion = "restaurantes"
                else:
                    puntos = puntos + e
                    informacion = puntos
        if type(informacion) == list:
            informacion = "dato no encontrado"

    if clave == "servicios_de_asistencia_de_viajes":
        informacion = donde[donde.find("beneficios:"):donde.find("||")]
        informacion = informacion.split(".")
        for e in informacion:
            if "asistencia de viaje" in e or "asistente de viaje" in e or "asistencia en viaje" in e or "asistente en viaje" in e or "asistencia previa al viaje" in e:
                informacion = "si"
                break
        if type(informacion) == list:
            informacion = "dato no encontrado"

    if clave == "catalogo_de_descuentos_ocasionales":
        beneficios = donde[donde.find("beneficios:"):donde.find("||")]
        if "anthony's" in donde and not "bdi" in donde:
            informacion = "no"
        elif u"hipermercados olé" in donde:
            informacion = "no"
        elif "gold's gym" in donde and not "lopez de haro" in donde:
            informacion = "no"
        elif "club hemingway" in donde:
            informacion = "no"
        elif "club naco" in donde:
            informacion = "no"
        elif u"casa de españa" in donde:
            informacion = "no"
        elif "pricesmart" in donde:
            informacion = "no"
        elif "bravo" in donde:
            informacion = "no"
        elif "ikea" in donde:
            informacion = "no"
        elif "almacenes iberia" in donde:
            informacion = "no"
        elif "autozama" in donde:
            informacion = "no"
        elif "la cadena" in donde:
            informacion = "no"
        elif (("descuento" in beneficios) or ("reembolso" in beneficios) or ("ahorr" in beneficios) or u"devolución" in beneficios) and "%" not in beneficios or ("popular" in donde or "bdi" in donde or "alnap" in donde or "lopez de haro"):
                informacion = "si"
        else:
            informacion = "no"
    if clave == "alcance_del_descuento":
        beneficios = donde[donde.find("beneficios:"):donde.find("||")]
        if (("descuento" in beneficios) or ("reembolso" in beneficios) or "ahorr" in beneficios or u"devolución" in donde) and "%" in beneficios:
            informacion = "si"
        else:
            informacion = "n/a"
    if clave == "institucion_o_empresa":
        empresas = db.GqlQuery("select * from Global_Instituciones").fetch(1)[0].empresas
        informacion = []
        for e in empresas:
            if e in donde:
                informacion = e
                break
        if type(informacion) == list:
            informacion = "no encontrado"
        else:
            if e == "san miguel" and e not in donde[:donde.find(u"emisión")]:
                informacion = "no encontrado"
    if clave == "porcentaje_sobre_limite":
        informacion = donde[donde.find("beneficios:"):donde.find("||")]
        if informacion.count(".") > informacion.count("-"):
            informacion = informacion.split(".")
        elif informacion.count("-") > informacion.count("."):
            informacion = informacion.split(".")
        else:
            informacion = informacion.split(",")
        for e in informacion:
            if (("efectivo" in e) and (u"límite" in e or "limite" in e) or ("exced" in e and u"límite" in e)) and ("%" in e) or (("retiro" in e and "efectivo" in e) and "%" in e):
                informacion = e

        if type(informacion) == list:
            informacion = "no encontrado"
        else:
            for e in informacion:
                if e.isdigit() == False:
                    informacion = informacion.replace(e,"")
            informacion += "%"
    if clave == "adelanto_efectivo_emergencia":
        informacion = donde[donde.find("beneficios:"):donde.find("||")]
        if informacion.count(".") > informacion.count("-"):
            informacion = informacion.split(".")
        elif informacion.count("-") > informacion.count("."):
            informacion = informacion.split(".")
        else:
            informacion = informacion.split(",")
        for e in informacion:
            if ("emergencia" in e and "efectivo" in e):
                informacion = e

        if type(informacion) == list:
            informacion = "no encontrado"
        else:
            informacion = "si"
    if clave == "enfoque_empresas":
        if "empresa" in donde:
            informacion = "si"
        else:
            informacion = "no"

    if clave == "cantidad_de_cuotas_permitidas":
        informacion = donde[donde.find("beneficios:"):donde.find("||")]
        if informacion.count(".") > informacion.count("-"):
            informacion = informacion.split(".")
        elif informacion.count("-") > informacion.count("."):
            informacion = informacion.split(".")
        else:
            informacion = informacion.split(",")
        for e in informacion:
            if ("cuotas" in e and "meses" in e) or ("financia" in e and "meses" in e) or (u"límite" in e and "cuotas" in e):
                informacion = e
        lista_cuotas = []
        if type(informacion) == list:
            informacion = "no encontrado"
        else:
            informacion = informacion.split()
            for e in informacion:
                if e.isdigit() == True: 
                    lista_cuotas.append(eval(e))
            informacion = str(max(lista_cuotas))
    if clave == "minimo_de_cuotas_permitidas":
        informacion = donde[donde.find("beneficios:"):donde.find("||")]
        if informacion.count(".") > informacion.count("-"):
            informacion = informacion.split(".")
        elif informacion.count("-") > informacion.count("."):
            informacion = informacion.split(".")
        else:
            informacion = informacion.split(",")
        for e in informacion:
            if ("cuotas" in e and "meses" in e) or ("financia" in e and "meses" in e) or (u"límite" in e and "cuotas" in e):
                informacion = e
                break
        lista_cuotas = []
        if type(informacion) == list:
            informacion = "no encontrado"
        else:
            informacion = informacion.split()
            for e in informacion:
                if e.isdigit() == True: 
                    lista_cuotas.append(eval(e))
            informacion = str(min(lista_cuotas))
    if clave == "establecimientos_permitidos":
        informacion = donde[donde.find("beneficios:"):donde.find("||")]
        informacion = informacion.split(".")
        if "plaza lama" in donde:
            informacion = "plaza lama"
        else:      
            for e in informacion:
                if "establecimiento" in e and "afiliado" in e and "descuento" in e and "%" in e:
                    informacion = e
            if type(informacion) == list:
                informacion = "dato no encontrado"
            else:
                informacion = "si"
    if clave == "beneficio_valor_agregado":
        if "club de ventajas ikea" in donde:
            informacion = "club de ventajas ikea"
        elif "autozama" in donde:
            informacion = "priority pass en taller"
        else:
            informacion = "no encontrado"

    if clave == "destinada_combustible":
        informacion = "si" if "combustible" in donde or "fleet" in donde else "no"



        

    #no se como pueden aparecer

    if clave == "minimo_unidades_para_canje":
        informacion = "dato no encontrado"

   

    if clave == "bono_unidades_de_emision":
        informacion = "dato no encontrado"

    
    

    if clave == "monto_minimo_de_compra":
        informacion = "dato no encontrado"

    if clave == "programa_recuperacion_de_credito":
        informacion = "dato no encontrado"

    if clave == "programa_educacion_financiera":
        informacion = "dato no encontrado"

    if clave == "programa_iniciar_credito":
        informacion = "dato no encontrado"

    if clave == "servicio_de_asistencia_a_negocios":
        informacion = "dato no encontrado"












    if type(informacion) != list:
        if len(informacion) < 1:
            return "n/a"
        elif len(informacion) > 1500:
            return "si, tiene demasiadas recompensas."
        else:
            return informacion.replace('\n',"").replace("beneficios:", "")
    else:
        return informacion


def maniobrarComoPro(damelo_papi):
    el_papi = {
        "nombre": "",
        "banco": "",
        "ingreso_minimo": "",
        "facturacion": "",
        "dias_de_vencimiento": "",
        "tasa_de_interes_en_rd": "",
        "tasa_de_interes_en_us": "",
        "cargo_por_emision": "",
        "renovacion_anual": "",
        "seguro_robo_o_perdida": "",
        "cargo_por_sobregiro": "",
        "cargo_por_mora": "",
        "avance_de_efectivo": "",
        "plan_de_lealtad": "",
        "recompensa": "",
        "bono_unidades_de_emision": "",
        "comercios_que_generan_unidades_extra": "",
        "minimo_unidades_para_canje":"",
        "vencimiento_de_unidades": "",
        "pago_de_membresia": "",
        "descuento_en_comercios_especificos": "",
        "alcance_del_descuento": "",
        "descuento_maximo_en_comercios": "",
        "descuentos_por_tipo_de_comercio": "",
        "catalogo_de_descuentos_ocasionales": "",
        "credito_diferido": "",
        "adelanto_efectivo_emergencia": "",
        "enfoque_empresas": "",
        "utiliza_tarjeta_separada": "",
        "establecimientos_permitidos": "",
        "monto_minimo_de_compra": "",
        "cantidad_de_cuotas_permitidas": "",
        "minimo_de_cuotas_permitidas": "",
        "tasa_de_interes_del_credito_diferido": "",
        "linea_aerea_vinculada": "",
        "priority_pass": "",
        "before_boarding": "",
        "servicios_de_asistencia_de_viajes": "",
        "servicios_de_asistencia_personal": "",
        "seguro_en_accidentes_de_viaje": "",
        "seguro_en_accidentes_en_destino_de_viaje": "",
        "seguro_de_autos_alquilados": "",
        "seguro_contra_demora_de_equipaje": "",
        "seguro_contra_perdida_de_equipaje": "",
        "seguro_contra_demora_de_viaje": "",
        "seguro_contra_cancelacion_de_viaje": "",
        "seguro_contra_perdida_de_conexion":"",
        "emergencia_medica_internacional": "",
        "proteccion_de_compras": "",
        "proteccion_de_precios": "",
        "permite_garantia": "",
        "programa_recuperacion_de_credito": "",
        "programa_educacion_financiera": "",
        "programa_iniciar_credito": "",
        "servicio_de_asistencia_a_negocios": "",
        "institucion_o_empresa": "",
        "beneficio_valor_agregado": "",
        "destinada_combustible": "",
        "porcentaje_sobre_limite": ""
    }
    for e in el_papi:
        el_papi[e] = BuscarInformacion(e,damelo_papi)
    return json.dumps(el_papi)

def rexi_info(id_tarjeta,update):
    info = memcache.get("rexi_"+str(id_tarjeta))
    if info == None or update == True:
        data = urllib.urlencode({"id":id_tarjeta})
        req = urllib.urlopen("https://dev-rexi.azurewebsites.net/umbraco/Surface/CreditCard/GetCCByIdorName", data)
        memcache.set("rexi_"+str(id_tarjeta), req.read().decode('utf-8'))
        info = memcache.get("rexi_"+str(id_tarjeta))
    return json.dumps(info)

class Principal(Handler):
    def get(self):
        self.render("rexi.html")

def chequea_banco(lixt,update):
    lixta = []
    for e in lixt:
        tarjeta = db.GqlQuery("select * from Tarjeta_ID where nombre_tarjeta='%s'" %e).fetch(1)[0]
        logging.error(tarjeta)
        if tarjeta.numeros_tarjeta[1] == 0:
            info = json.loads(rexi_info(tarjeta.numeros_tarjeta[0],update))
        else:
            info = json.loads(rexi_info(tarjeta.numeros_tarjeta,update))
        if "status" not in info:
            lixta.append(e)
    return len(lixta)
class VerificadorHandler(Handler):
    def get(self):
        if not self.request.get("banco") and self.request.get("id"):
            encontrada,rexi,verification=[],[],[]
            id_tarjeta = self.request.get_all("id")
            update = True if self.request.get("update") == "1" else False
            error = False
            tarjetas = db.GqlQuery("select * from Tarjeta_ID").fetch(500)
            for idt in id_tarjeta:
                if idt.isdigit() == False:
                    error = True
                    break       
                info = json.loads(rexi_info(idt,update))
                info2 = None
                for e in tarjetas:
                    if e.numeros_tarjeta[1] == int(idt) or e.numeros_tarjeta[0] == int(idt):
                        info2 = memcache.get(e.nombre_tarjeta)
                        if info2 == None or update == True:
                            guardarTarjeta(e.nombre_tarjeta,check=False)
                            time.sleep(1)
                            info2 = memcache.get(e.nombre_tarjeta)
                        break

                if info2 != None:
                    info2_viejo = info2
                    info2 = memcache.get("local_"+str(idt))
                    if info2 == None or update == True:
                        memcache.set("local_"+str(idt),json.loads(maniobrarComoPro(info2_viejo.contenido)))
                        info2 = memcache.get("local_"+str(idt))

                    if len(info) != 2:
                        info = json.loads(info)
                        encontrada.append(json.dumps(Compara_tarjetas(info,info2,update)[1]))
                        rexi.append(json.dumps(Compara_tarjetas(info,info2,update)[0]))
                        verification.append(json.dumps(Compara_tarjetas(info,info2,update)[2]))

                else:
                    error = True
            if error != True:
                time.sleep(1)
                self.render("rexi.html",encontrada=str(encontrada), rexi=str(rexi), verification=str(verification))
            else:
                self.write(u"<h1>Errores encontrados</h1><br><h3>Posibles errores:</h3><br><ul><li>ID Incorrecto(s)</li><li>Servidor QA Caido</li><li>Información mal extraida</li></ul>")
        elif self.request.get("banco"):
            banco = self.request.get("banco")
            credit_cards= []
            error = False
            id_tarjeta = []
            encontrada,rexi,verification=[],[],[]
            tarjetas = db.GqlQuery("select * from Tarjeta_ID").fetch(500)
            update = True if self.request.get("update") == "1" else False
            for e in tarjetas:
                if banco in e.nombre_tarjeta:
                    credit_cards.append(e.nombre_tarjeta)
            if credit_cards == []:
                self.write("<h1>Este banco no existe</h1>")
            elif chequea_banco(credit_cards,update) == 0:
                self.write("<h1>Este banco no tiene tarjetas publicadas</h1>")
            else:
                for nombre in credit_cards:
                    for e in tarjetas:
                        if e.nombre_tarjeta == nombre:
                            id_tarjeta.append(e.numeros_tarjeta[0])
                            id_tarjeta.append(e.numeros_tarjeta[1])
                
                for idt in id_tarjeta:

                    info = json.loads(rexi_info(idt,update))
                    info2 = None
                    for e in tarjetas:
                        if e.numeros_tarjeta[1] == int(idt) or e.numeros_tarjeta[0] == int(idt):
                            info2 = memcache.get(e.nombre_tarjeta)
                            if info2 == None or update == True:
                                guardarTarjeta(e.nombre_tarjeta,check=False)
                                time.sleep(1)
                                info2 = memcache.get(e.nombre_tarjeta)
                            break

                    if info2 != None:
                        info2_viejo = info2
                        info2 = memcache.get("local_"+str(idt))
                        if info2 == None or update == True:
                            memcache.set("local_"+str(idt),json.loads(maniobrarComoPro(info2_viejo.contenido)))
                            info2 = memcache.get("local_"+str(idt))
                            
                        if "id" in info:
                            info = json.loads(info)
                            encontrada.append(json.dumps(Compara_tarjetas(info,info2,update)[1]))
                            rexi.append(json.dumps(Compara_tarjetas(info,info2,update)[0]))
                            verification.append(json.dumps(Compara_tarjetas(info,info2,update)[2]))

                    else:
                        error = True
                if error != True:
                    time.sleep(1)
                    self.render("rexi.html",encontrada=str(encontrada), rexi=str(rexi), verification=str(verification))
                else:
                    self.write("<h1>Errores encontrados</h1><br><h3>Posibles errores:</h3><br><ul><li>ID Incorrecto(s)</li><li>Servidor QA Caido</li><li>Información mal extraida</li></ul>")
        else:
            self.write("<h1>Error 9999999</h1>")


class MainHandler(Handler):
    def get(self,card):
        info = None
        informacion = memcache.get(card)
        verification = None
        update = True if self.request.get("update") == "1" else False
        if informacion == None or update == True:
            if informacion == None:
                if guardarTarjeta(card,check=True) == True:
                    pass
                else:
                    guardarTarjeta(card,check=False)
                    informacion = memcache.get(card)
                    if informacion != None:
                        info = maniobrarComoPro(informacion.contenido)

            elif update == True:
                informacion = memcache.get(card)
                memcache.delete(card)
                informacion.contenido = fetch(urllib2.urlopen('http://pocket-wikix.appspot.com/'+card).read().decode("utf-8"))
                informacion.put()
                time.sleep(1)
                memcache.set(card,informacion)
                info = maniobrarComoPro(memcache.get(card).contenido)
        else:
            info = maniobrarComoPro(memcache.get(card).contenido)





        if not self.request.get("test"):
            time.sleep(1)
            verification = tarjetas = db.GqlQuery("select * from Tarjeta_ID where nombre_tarjeta='"+card+"'").fetch(1)
            update_request = "&update=1" if update == True else ""
            if verification != []:
                if verification[0].numeros_tarjeta[1] != 0:
                    ids = "id="+str(verification[0].numeros_tarjeta[0])+"&id="+str(verification[0].numeros_tarjeta[1])

                    self.redirect("/_verificar?"+ids+update_request)
                else:
                    self.redirect("/_verificar?id="+str(verification[0].numeros_tarjeta[0])+update_request)
            else:
                self.write("<h1>Nombre incorrecto</h1>")
        else:
            self.render("rexi.html",info=info)

def add_card(card,Id,check):
    search = db.GqlQuery("select * from Tarjeta_ID where nombre_tarjeta='"+card+"'").fetch(1)
    if search == []:
        if check != True:
            card = Tarjeta_ID(nombre_tarjeta=card,numeros_tarjeta=Id)
            card.put()
        else:
            return search
    else:
        return search




class AgregarTarjeta(Handler):
    def get(self):
        self.render('newcard.html')
    def post(self):
        nombre = self.request.get("nombre_tarjeta")
        Id = self.request.get("id_tarjeta")
        Id2 = self.request.get("id_tarjeta2") if self.request.get("id_tarjeta2") != "" else "0"
        if len(rexi_info(int(Id),False)) == 2 or Id2 != "0" and len(rexi_info(int(Id2),False)) == 2:
            self.render('newcard.html')
        elif Id.isdigit() == False or Id2.isdigit() == False:
            self.render("newcard.html")
        elif add_card(nombre,[int(Id),int(Id2)],True) != []:
            search = db.GqlQuery("select * from Tarjeta_ID where nombre_tarjeta='"+nombre+"'").fetch(1)[0]
            search.numeros_tarjeta = [int(Id),int(Id2)]
            search.put()
            self.redirect('/_addcard')
        else:
            add_card(nombre,[int(Id),int(Id2)],False)
        self.redirect('/_addcard')

class Create_Backup(Handler):
    def get(self):
        for e in tarjetas:
            if type(tarjetas[e]) != list:
                add_card(e,[tarjetas[e],0],False)
            else:
                add_card(e,tarjetas[e],False)
        empresas_backup = Global_Instituciones(empresas=empresas,aerolineas=aerolineas)
        empresas_backup.put()
        self.redirect('/')

def add_empresa_aerolinea(nombre,emp_aer):
    search = db.GqlQuery("select * from Global_Instituciones").fetch(1)
    if emp_aer == "aerolinea" and search != []:
        if nombre not in search[0].aerolineas:
            search[0].aerolineas.append(nombre)
            search[0].put()
    if emp_aer == "empresa" and search != []:
        if nombre not in search[0].empresas:
            search[0].empresas.append(nombre)
            search[0].put()

class Add_Emp(Handler):
    def get(self):
        self.render("addEmp.html")
    def post(self):
        empresa = self.request.get("emp_aer2")
        aerolinea = self.request.get("emp_aer1")
        nombre = self.request.get("name")
        if empresa and aerolinea and nombre:
            add_empresa_aerolinea(nombre,"aerolinea")
            add_empresa_aerolinea(nombre,"empresa")
        elif empresa and nombre:
            add_empresa_aerolinea(nombre,"empresa")
        elif aerolinea and nombre:
            add_empresa_aerolinea(nombre,"aerolinea")
        
        self.redirect("/_addEmp")


app = webapp2.WSGIApplication([
    ('/'+'([a-z]+)', MainHandler),
    ("/", Principal),
    ("/_verificar", VerificadorHandler),
    ("/_addcard", AgregarTarjeta),
    ("/_backup", Create_Backup),
    ("/_addEmp", Add_Emp)
], debug=True)
