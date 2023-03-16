# Separa, Renombra, Envia SRE
import os # para renombrar
from pdfminer.high_level import extract_text # para leer el texto del pdf
from PyPDF2 import PdfFileWriter, PdfFileReader # para separar
import shutil # para mover

directorio = "ARCHIVOS" # donde esta el archivo con las paginas
directorioDest = input("Digite la direccion donde se encuentran las carpetas: ")
formato = "DETALLECARGOS_800058016_F"
formatoCarpetas = "FACT_800058016_F" 

swt = True
while swt:
    if directorioDest == "":
         directorioDest = input("Digite la direccion donde se encuentran las carpetas: ") #donde estan las carpetas destino 
    else:
        swt = False

print("Buscando carpetas en:", directorioDest,"\n")

#--------------------------------------------------------------------------------------
#aqui separa las paginas del archivo

try:
    f = os.path.join(directorio, "paginas.pdf")
    paginas  = open(f, "rb")
    inputpdf = PdfFileReader(paginas)
except:
    print("No se encontro", f)
    input("Presione ENTER para cerrar")
    os._exit(0)


for i in range(inputpdf.numPages):  
    output = PdfFileWriter()
    output.addPage(inputpdf.getPage(i))
    with open(directorio+"\pagina_%s.pdf" % (i+1), "wb") as outputStream:
        output.write(outputStream)
paginas.close()
os.remove(f)

#---------------------------------------------------------------------------------------
#renombrar cada pagina
j = 1
for archivo in os.listdir(directorio):
    #print(archivo)
    archivoPagina = os.path.join(directorio, archivo) 
    
    if os.path.isfile(archivoPagina): # checking if it is a file  
        #print(file)
        txt = extract_text(archivoPagina)
        #print(txt)
        lineas = txt.split("\n")
        #print(lineas)
        for linea in lineas:
            #print (linea,"---")
            if linea.startswith("F"):
                numeroCarpeta = linea.replace(" ","").lstrip("F") # el numero sin espacio ni F
                cod = linea.split()[0] # F2XX 
                numero = linea.replace(" ","").replace(cod,"")# el numero sin espacio ni F2XX
                #print(numero)
                break
            
        nombreNuevo = directorio+"\\"+formato+numeroCarpeta+".pdf" # agregar ARCHIVOS\\DETALLECARGOS_800058016_F al nombre 
        destino = os.path.join(directorioDest, formatoCarpetas+numeroCarpeta+"//") # direccion dentro de la carpeta donde va el archivo
        
        if os.path.isfile(nombreNuevo): # si ya hay un archivo llamado asi en ARCHIVOS
                nombreNuevo = directorio+"\\"+formato+numeroCarpeta+"_R"+str(j)+".pdf"
                j+=1
                
        os.rename(archivoPagina, nombreNuevo) #renombrar
        
#-----------------------------------------------------------------------------------
# mover a carpetas
        DFnumero = nombreNuevo.lstrip("ARCHIVOS\\").rstrip(".pdf") # solo DETALLECARGOS_800058016_F y el numero

        if os.path.isdir(destino): # si existe la carpeta
            l = 1
            carpeta = True
            if os.path.isfile(destino+nombreNuevo.lstrip("ARCHIVOS\\")): 
                shutil.move(nombreNuevo, destino+DFnumero+"_"+str(l)+".pdf") # mover archivo
                nombreNuevo = DFnumero+"_"+str(l)+".pdf" # variable para imprimir
                l+=1
            else: #si no existe un archivo con ese nombre dentro de la carpeta
                shutil.move(nombreNuevo, destino+DFnumero+".pdf")
                nombreNuevo = DFnumero+".pdf" #Para imprimir
        else: 
            carpeta = False
            
# imprimir los datos
        print(archivo)
        print("NOMBRE NUEVO:",nombreNuevo.split("\\")[-1])
        print("NUMERO:",numero)
        print("DESTINO:", destino)
        if not carpeta:
            print("NO SE ENCONTRO CARPETA DESTINO")
        print("----------")

input("Presione ENTER para cerrar")