def BuscarInformacion(clave,donde):
    informacion = ""
    donde = donde.lower()
    if clave == "nombre":
        informacion = donde[:donde.find("-")-1]
    if clave =="banco":
        informacion = donde[donde.find("-")+2:donde.find(",",donde.find("-"))]
    if clave == "facturacion":
        if "rd$" in donde[donde.find("renovacion",0,donde.find("beneficios:")):donde.find(",", donde.find("renovacion",0,donde.find("beneficios:")))] or "gratis" in donde[donde.find("renovacion"):donde.find(",", donde.find("renovacion",0,donde.find("beneficios:")))]:
            if donde.count("usd") + donde.count("us$") >= 3 and ("usd$|-" not in donde) or donde.count("usd") >= 2 and ("usd|-" not in donde):
                informacion = "doble saldo"
            else:
                informacion = "pesos"
        else:
            informacion = "dolares"
    if clave == "tasa_de_interes_en_rd":
        informacion = donde[:donde.find("beneficios:")]
        if "rd$" in donde[donde.find("renovacion",0,donde.find("beneficios:")):donde.find(",", donde.find("renovacion",0,donde.find("beneficios:")))] or "gratis" in donde[donde.find("renovacion"):donde.find(",", donde.find("renovacion",0,donde.find("beneficios:")))]:
            informacion = informacion.split(",")
            for e in informacion:
                if (("tasa" in e or "cargo" in e) and "financiamiento" in e) or (("tasa" in e or "cargo" in e) and "interes" in e) or ("interes" in e and "financiamiento" in e):
                    if "rd$" in e or "usd$" in e:
                        if "rd$" in e:
                            informacion = e
                            break
                    else:
                        informacion = e
                        break

            if type(informacion) != list:
                informacion = informacion[informacion.find("|")+1:]
                if "/" in informacion or "-" in informacion:
                    informacion = informacion[:informacion.find("%")+1]
            else:
                informacion = "n/a"
        else:
            informacion = "n/a"

    if clave == "tasa_de_interes_en_us":
        informacion = donde[:donde.find("beneficios:")]
        informacion = informacion.split(",")
        if ("rd$" in donde[donde.find("renovacion",0,donde.find("beneficios:")):donde.find(",", donde.find("renovacion",0,donde.find("beneficios:")))] or "gratis" in donde[donde.find("renovacion"):donde.find(",", donde.find("renovacion",0,donde.find("beneficios:")))]) and donde.count("usd") + donde.count("us$") < 2:
            informacion = "n/a"
        else:
            for e in informacion:
                if (("tasa" in e or "cargo" in e) and "financiamiento" in e) or (("tasa" in e or "cargo" in e) and "interes" in e) or ("interes" in e and "financiamiento" in e):
                    if "rd$" in e or "usd$" in e:
                        if "usd$" in e:
                            informacion = e
                            break
                    else:
                        informacion = e
                        break
            if type(informacion) != list:
                informacion = informacion[informacion.find("|")+1:]
                if "/usd$" in informacion and informacion.find("%", informacion.find("/usd$")+1) != -1:
                    informacion = informacion.split("/")[1]
                elif "-" in informacion and informacion.find("%", informacion.find("-")+1) != -1:
                    informacion = informacion.split("-")[1]
                else:
                    if not "a" in informacion and not "m" in informacion:
                        informacion = informacion[:informacion.find("%")+1]
            else:
                informacion = "rd$0"
            
       
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
                if "emision" in e and "adicional" not in e:
                    informacion = e
                    break
            if type(informacion) == list:
                informacion = "n/a"
            else:
                for e in informacion2:
                    if "principal" in e and "emisión" in e and ("grat" in e or "cost" in e) and not "primer año" in e:
                        benefit = True
                        break
                informacion = informacion[informacion.find("|")+1:]
                if informacion == "gratis" or benefit == True:
                    informacion = "rd$0"
        if "emision_internacional" in donde:
            internacional = donde[donde.find("emision_internacional"):donde.find(",", donde.find("emision_internacional"))]
            if "/" in internacional:
                internacional = internacional.split("/")[0]
            informacion += "/" + internacional

    if clave == "renovacion_anual":
        informacion = donde[:donde.find("beneficios:")]
        informacion = informacion.split(",")
        mensual = False
        for e in informacion:
            if "renovacion" in e or "reposición" in e or "mantenimiento anual" in e or ("cargo" in e and "membresía" in e):
                informacion = e
                if "mensual" in informacion:
                    mensual = True
                break
        if type(informacion) == list:
            informacion = "n/a"
        else:
            informacion = informacion[informacion.find("|")+1:]
            if informacion == "gratis":
                informacion = "rd$0"
            if mensual == True:
                informacion = informacion + " (mensual)"
    if clave == "seguro_robo_o_perdida":
        informacion = donde[:donde.find("beneficios:")]
        informacion = informacion.split(",")
        for e in informacion:
            if (("seguro" in e or "cargo" in e or "protección" in e or "reposición" in e) and ("pérdida" in e or "rob" in e or "protección" in e) and ("plástico" not in e and "reemplazo" not in e)):
                informacion = e
        if type(informacion) == list:
            informacion = "n/a"
        else:
            informacion = informacion[informacion.find("|")+1:]
    if clave == "avance_de_efectivo":
        informacion = donde[:donde.find("beneficios:")]
        informacion = informacion.split(",")
        for e in informacion:
            if ("avance" in e and "efectivo" in e) or ("retiro" in e and "cajero" in e and "autom" in e ) or ("retiro" in e and "efectivo" in e):
                informacion = e
                break
        if type(informacion) == list:
            informacion = "n/a"
        else:
            informacion = informacion[informacion.find("|")+1:informacion.find("%")+1]
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