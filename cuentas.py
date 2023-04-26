import re
import datetime

# Toma uno o varios nombres de alumnos y una lista de strings encabezados por nombres. Borra los strings que comienzan con los nombres ingresados y devuelve un string.
def borrar(lista, *strings):
    lista = lista.copy()
    for i in strings:
        for j in lista:
            if re.search(i+" [^\d]", j):
                lista.remove(j)
    textonuevo = ""
    for i in lista:
        textonuevo += i + "\n"
    return textonuevo

# Toma el nombre del alumno, la lista con strings encabezados por nombres, el str que se quiere agregar en alguno de ellos y tiene una flag para cuando hay que agregar plata a favor.
def agregar(lista, string, agr, fav=False, mod=False):
    textonuevo = ""
    encontrado = 0

    for entrada in lista:
        if not re.search(string+" [^\d]", entrada):
            textonuevo = textonuevo + entrada + "\n"
            continue

        if not fav:
            if not mod:
                entrada = entrada + " " + agr
                encontrado = 1
                textonuevo = textonuevo + entrada + "\n"
                continue
            entrada = re.sub(f" \$\d+\s\d+/{mod}","",entrada)
            if not re.search("\$", entrada): 
                encontrado = 1
                continue
            textonuevo = textonuevo + entrada + "\n"
            encontrado = 1
            continue

        pos = re.search("[a-zA-ZáéíóúÁÉÍÓÚ]*\s*[a-zA-ZáéíóúÁÉÍÓÚ]*\s*\d*",entrada)
        busc = re.search('\(\+\$(\d+)\)',entrada)

        if not busc:
            sep = pos.span()[1]+1
            agr += " "

            if not pos.group(0)[-1].isdigit():
                sep -= 1
            entrada = entrada[:sep]+agr+entrada[sep:]
            encontrado = 1
            textonuevo = textonuevo + entrada + "\n"
            continue

        credprev = int(busc.group(1))
        agr = int(re.search('\d+',agr).group(0))
        agr = str(agr + credprev)
        entrada = re.sub("\(\+\$\d+\)","(+$"+agr+")",entrada)
        textonuevo = textonuevo + entrada + "\n"
        encontrado = 1

    if encontrado == 0:
        textonuevo = string + " " + agr + "\n" + textonuevo

    return textonuevo

# Toma el valor de diccionario de un alumno y arma un string con fecha de clase-> plata, plata a favor y total.
def cuenta_alumno(v, mes=""):
    cuenta = ""
    total_mes = 0
# los valores del diccionario tienen la forma {"Alumno":[[(fecha, plata), (fecha, plata),...], deuda total, crédito]
    for c in range(len(v[0])):
        fecha = v[0][c][0]
        plata = v[0][c][1]
        if mes:
            if not f"/{mes}" in fecha: continue
            total_mes += plata
                      
        cuenta += f"clase del {fecha:5} --> $ {plata}\n"
        
    if v[2] != 0:
        cuenta += f"plata a favor: ${v[2]}"

    if mes:
        cuenta += f"\nTotal: ${total_mes-v[2]}"
    else:
        cuenta += f"\nTotal: ${v[1]-v[2]}"
    
    return cuenta


    

#crea el diccionario con alumnos y los datos de sus clases.
def crear_diccionario (fh):
    texto =  fh.read().rstrip()
    lista = texto.split("\n") #lista con strings -> "alumno dinero a favor/en contra fechas".
    d = {}

    if texto == "":
        return (d,"","")

    for string in lista:
        nombre = re.findall("(\w+\s*[0-9]*)\s?",string)[0].rstrip() #nombre del alumno como único elem de la lista.

        if " $" in string:
            plata = list(map(int,re.findall("[^+]\$([0-9]+)",string))) #lista dinero en int
            fecha = re.findall("([0-9]+/[0-9]+)\s?",string) #lista con uno o más fechas en str
            f_p = list(zip(fecha,plata)) #lista de tuplas de fecha y plata correspondiente
        else:
            plata = []
            f_p = []

        plata_f = list(map(int,re.findall("\(\+\$([0-9]+)\)",string))) #lista dinero a favor en int

        if plata_f == []:
            plata_f = [0] #si no hay plata a favor, ingresa 0 en la lista para poder hacer la cuenta.

        d[nombre] = [f_p,sum(plata),sum(plata_f)] #diccionario-> {"nombre alumno": [[tuplas],int, int]}

    return (d,texto,lista)

def main():

    buscar = " "

    while buscar != "fin":
        with open("D:\\code\\laburo\\cuentas.txt","r",encoding="utf-8") as fh:
            d, texto, minotalst = crear_diccionario(fh)
#comienzo del programa para el usuario.
        buscar = input("Opciones:\n'lista' | 'dic' | 'check' | nombre del alumno | 'fin':\n")

        if len(buscar) == 0: buscar = "fin"

        if buscar == "fin" : continue

        buscar = buscar.capitalize()
        check = False

        match (buscar):
#imprime el listado de alumnos con clases--> su valor, deuda y crédito. Embellecido para enviar por Whatsapp.
            case ("Lista"):
                cuenta = ""
                total = 0
                print ("")

                for k, v in d.items():
                    cuenta = k + ":\n"
                    cuenta = cuenta + cuenta_alumno(v)
                    print(cuenta + "\n\n")

                    if v[1] < v[2]: continue # si plata a favor > plata adeudada, no lo suma al total
                    total += v[1]-v[2]

                print ("\ntotal final: $"+str(total)+"\n")
                continue

#imprime los nombres de alumnos que deben dinero, sin detalle.
            case ('Dic'):
                print("")
                for k in d.keys():
                    print (k)
                print ("\n")
                continue

#busca alumnos con balance $0 y ofrece eliminarlos.
            case ('Check'):
                check = True
                aux = []

                for k,v in d.items():
                    if v[1] == v[2]:
                        bal_cero = input (f'El balance de {k} es $0, eliminar?[s|n]\n')

                        if bal_cero == "": bal_cero = "n"

                        if bal_cero[0].lower() == "s":
                            aux.append(k)

                    b = tuple(aux)

                textonuevo = borrar(minotalst,*b)
                if len(aux) == 0:
                    print("nada...\n")
                opt = "s"

#búsqueda inteligente en el diccionario.
        if not buscar in d.keys() and not check:
            posiblesnombres = []

            for nombre in d.keys():
                if buscar in nombre:
                    posiblesnombres.append(nombre)

            if posiblesnombres != []:
                count = 1

                for x in posiblesnombres:
                    print (str(count) + ") " + x)
                    count += 1
                nombre = buscar
                buscar = input("número del alumno | [a]gregar | enter para terminar\n")

                if len(buscar) == 0: buscar = "n"

                if buscar == "a":
                    opt = buscar
                    buscar = nombre

                else:
                    try:
                        buscar = int(buscar)
                        buscar = posiblesnombres[buscar-1].capitalize()
                        print (buscar)
                    except:
                        continue

            else:
                print ("\nEl nombre no se encuentra en el diccionario")
                opt = input("[a]gregar alumno a la lista | [n]o agregar alumno\n")

#si encuentra el nombre del alumno, ofrece eliminarlo o agregar clases
        if buscar in d.keys() and not check:
            mes = input("\nIngresar mes o enter para mostrar todos:\n")
            if mes.isnumeric():
                print("\n"+cuenta_alumno(d[buscar],mes=mes))
            else:
                print("\n"+cuenta_alumno(d[buscar]))

            opt = input("\n[e]liminar entrada | [a]gregar clase | [m]odificar: | [n]ada\n")

            if len(opt) == 0:
                opt = "n"
            else:
                opt = opt[0].lower()

            if opt == "e":

                while opt != "s" and opt != "n":
                    opt = input("Seguro?[s|n]")

#en caso de querer agregar una entrada, ya sea a un alumno existente o ingresándolo por primera vez.
        if opt == "a":
            alumno = buscar
            dicplata = {"a":3600, "b":5400, "c":7200, "d":2700, "e":4000, "f":5400, "g":2700, "h": 4500, "s":800, "n":0}

            try:
                fav = False
                precred = input("plata a favor[s|n]:\n")

                if precred == "": precred = "n"

                precred = precred[0].lower()

                if precred == "s" : fav = True

                plata = input("[a] 1h | [b] 1h30m | [c] 2h | [d] gr 1h | [e] gr 1h30m | [f] gr 2h | [g] 45m | [h] gr3 2h | [p]ersonalizado\n")

                if plata == "p":
                    plata = int(input("$: "))
                else:
                    plata = dicplata[plata] #busca el valor de la clase seleccionada

                extra = input("extra sábado [s|n]")

                if extra == "": extra = "n"

                extra = extra[0].lower()
                extra = dicplata[extra]
                plata = str(plata+extra)
                cambiar_fecha = input("cambiar fecha[s|n]")
                if cambiar_fecha.lower() == "s":
                    día = input("número día: ")
                    mes = input("número mes: ")
                    fecha = día+"/"+mes
                else:
                    fecha = str(datetime.datetime.now().day)+"/"+str(datetime.datetime.now().month) # fecha actual


                if fav:
                    agr = "(+$" + plata + ")"
                else:
                    agr = f"${plata} {fecha}" # el dinero a agregar y la fecha correspondiente a la clase.

            except:
                print("tocaste mal, va de nuevo")
                opt = "n"
                continue

            textonuevo = agregar(minotalst, alumno, agr, fav=fav)

#en caso de querer borrar una entrada completa.
        if opt == "s" and not check:
            elim = buscar
            textonuevo = borrar (minotalst, elim)

        if opt == "m":
            alumno = buscar
            try:
                mod = int(input("mes a eliminar: "))
                textonuevo = agregar(minotalst, alumno, "", mod=mod)
                opt = "a"
            except:
                print("tocaste mal, va de nuevo")
                opt = "n"
                continue

#hace un backup
        if (opt == "s" or opt == "a") and (not check or len(aux)>0):
            fecha_c = datetime.datetime.now()
            día = fecha_c.day
            mes = fecha_c.month
            año = fecha_c.year
            hora = fecha_c.strftime("%H:%M")
            fecha = str(día)+"/"+str(mes) + " " + hora

            nota = open("D:\\code\\laburo\\cuentas.txt", "w",encoding="utf-8")
            nota.write(textonuevo)
            nota.close()

            nota_backup = open("D:\\code\\laburo\\cuentas_backup.txt","r",encoding="utf-8")
            nota_backup_texto = nota_backup.read()

            lista_limpieza = re.split("\n\n\n",nota_backup_texto)
            if lista_limpieza:
                fechas_mod = []
                for modif in lista_limpieza:
                    if modif == "": continue
                    d_mod = int(re.search ("\d+", modif).group(0))
                    m_mod = int(re.search ("/(\d+)", modif).group(1))
                    fecha_mod = datetime.datetime(año, m_mod, d_mod)
                    delta = fecha_c - fecha_mod
                    if delta > datetime.timedelta(10): continue #borra entradas más antiguas que 10 días.
                    fechas_mod.append(modif)
                nota_backup_texto = "\n\n\n".join(fechas_mod)

            nota_backup.close()
            nota_backup = open("D:\\code\\laburo\\cuentas_backup.txt","w",encoding="utf-8")
            nota_backup.write(f"previo al cambio del {fecha}:\n\n{texto}\n\n\n{nota_backup_texto}")
            nota_backup.close()

            with open("D:\\code\\laburo\\cuentas.txt", "r",encoding="utf-8") as nota:
                nuevo_dic,texto,compara = crear_diccionario(nota)
                if opt == "a":
                    if not alumno in nuevo_dic.keys():
                        print("Alumno borrado\n")
                    else:
                        print("\n--------------------------------------------------")
                        print(f"{alumno}:\n" + cuenta_alumno(nuevo_dic[alumno]))
                        print("--------------------------------------------------")
                if compara != minotalst:
                    print("\nSe guardaron los cambios.\n")
                else:
                    print("Hubo un error en la escritura.")

if __name__ == "__main__":
    main()
