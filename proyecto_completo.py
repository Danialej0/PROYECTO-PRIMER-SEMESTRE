# LIBRERIAS NECESARIAS

import unicodedata

import csv

from colorama import Fore, Style # pip install colorama

import matplotlib.pyplot as plt # pip install matplotlib


#-------------------BIENVENIDA-------------------

def centrar_texto(mensaje, ancho):
    espacios = (ancho - len(mensaje)) // 2
    return " " * espacios + mensaje

def centrar(texto, ancho):
    print(centrar_texto(texto, ancho))

def divider(ancho):
    print(Fore.CYAN + "-" * ancho)
    print(Style.RESET_ALL)

def mensaje_bienvenida():
    ancho = 50
    divider(ancho)
    centrar(Fore.CYAN + "¡Bienvenidos a EduFinder!", ancho)
    divider(ancho)
    print(Style.RESET_ALL) # Resetaura el color

def mensaje_graficas():
    ancho = 50
    divider(ancho)
    centrar(Fore.CYAN + "¡Seccion grafica!", ancho)
    divider(ancho)
    print(Style.RESET_ALL) # Resetaura el color

def mensaje_graficas_icfes():
    ancho = 50
    divider(ancho)
    centrar(Fore.CYAN + "¡Seccion puntaje pruebas icfes!", ancho)
    divider(ancho)
    print(Style.RESET_ALL) # Resetaura el color
    


mensaje_bienvenida()



#-------------------FILTROS-------------------


import csv
import unicodedata
from colorama import Fore, Style

def solicitar_discapacidad():
    while True:
        espacio_discapacitados = input("¿Necesitas que el colegio tenga espacio para discapacitados? (sí/no) " + '\n')
        if espacio_discapacitados.lower() in ['si', 'sí', 'no']:
            return espacio_discapacitados
        else:
            print("Por favor, ingresa 'sí' o 'no'.")

def solicitar_tipo_zona():
    while True:
        tipo_zona = input("¿Buscas un colegio en zona rural o urbana? " + '\n')
        if tipo_zona.lower() in ['rural', 'urbana']:
            return tipo_zona
        else:
            print("Por favor, ingresa 'rural' o 'urbana'.")
def solicitar_jornada():
    while True:
        jornada = input("¿Qué jornada buscas? (mañana/nocturna/completa) " + '\n') 
        if jornada:
            return jornada
        else:
            print("Por favor, ingresa 'mañana', 'nocturna' o 'completa'.")

def solicitar_estrato():
    while True:
        estrato = input("Ingrese el estrato que desea que sea el colegio (1/2/3/4): " + '\n')
        if estrato in ['1', '2', '3', '4']:
            return estrato
        else:
            print("Por favor, ingresa '1', '2', '3' o '4'.")

def solicitar_idioma():
    while True:
        idioma = input("¿Qué idioma buscas? " + '\n')
        if idioma:  
            return idioma
        else:
            print("Por favor, ingresa un idioma.")

def solicitar_localidades():
    while True:
        localidades = input("¿En qué localidad buscas el colegio? " + '\n')
        if localidades: 
            return localidades
        else:
            print("Por favor, ingresa una localidad." + '\n')

def solicitar_filtros():
    espacio_discapacitados = solicitar_discapacidad()
    tipo_zona = solicitar_tipo_zona()
    estrato = solicitar_estrato()
    idioma = solicitar_idioma()
    localidades = solicitar_localidades()
    jornada = solicitar_jornada()
    
    return espacio_discapacitados, tipo_zona, estrato, idioma, localidades, jornada
    
def solicitar_filtros_con_validacion():
    while True:
        try:
            return solicitar_filtros()
        except Exception as e:
            print(f"Ocurrió un error al solicitar los filtros: {e}")
            print("Por favor, inténtalo de nuevo.")

def normalizar_texto(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    ).upper()

def es_coincidencia(row, espacio_discapacitados, tipo_zona, estrato, idioma, localidades, localidades_bogota, jornada):
    if row['idiomas'] == '':
        row['idiomas'] = 'ESPAÑOL'
    idiomas = row['idiomas'].split(",")
    idiomas = [normalizar_texto(idioma.strip()) for idioma in idiomas]
    if '' in idiomas:
        idiomas.remove('')
        idiomas.append('ESPAÑOL')
    jornadas = row['jornadas'].split(",")
    jornadas = [normalizar_texto(jornada.strip()) for jornada in jornadas]
    

    idioma_normalizado = normalizar_texto(idioma)
    localidad_normalizada = normalizar_texto(localidades)
    jornada_normalizada = normalizar_texto(jornada)
    
    localidad_colegio_normalizada = normalizar_texto(row['localidad'])
    localidades_bogota_normalizadas = [normalizar_texto(localidad) for localidad in localidades_bogota]
    if idioma_normalizado not in idiomas:
        return False
    if localidad_colegio_normalizada not in localidades_bogota_normalizadas:
        return False   
    if localidad_normalizada not in localidad_colegio_normalizada:
        return False   
    if (espacio_discapacitados.lower() == 'sí' and row['discapacidades'] == '') or (espacio_discapacitados.lower() == 'no' and row['discapacidades'] != ''):
        return False   
    if estrato != row['estrato_Socio_Economico']:
        return False       
    if tipo_zona.lower() != row['zona'].lower():
        return False
    if jornada_normalizada not in jornadas:
        return False
    
    return True
    
espacio_discapacitados, tipo_zona, estrato, idioma, localidades, jornada = solicitar_filtros_con_validacion()
localidades_bogota = ['Usaquén', 'Chapinero', 'Santa Fe', 'San Cristóbal', 'Usme', 'Tunjuelito', 'Bosa', 'Kennedy', 'Fontibón', 'Engativá', 'Suba', 'Barrios Unidos', 'Teusaquillo', 'Los Mártires', 'Antonio Nariño', 'Puente Aranda', 'La Candelaria', 'Rafael Uribe Uribe', 'Ciudad Bolívar', 'Sumapaz']

with open('datos.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    colegios_encontrados = False
    for row in reader:
        if es_coincidencia(row, espacio_discapacitados, tipo_zona, estrato, idioma, localidades, localidades_bogota, jornada):
            colegios_encontrados = True
            print(f"\n{Fore.RED}Colegio:{Style.RESET_ALL} {row['nombreestablecimiento']}\n{Fore.RED}Correo electrónico:{Style.RESET_ALL} {row['correo_Electronico']}\n{Fore.RED}Teléfono:{Style.RESET_ALL} {row['telefono']}\n{Fore.RED}Discapacidad:{Style.RESET_ALL} {row['discapacidades']}\n{Fore.RED}Estrato{Style.RESET_ALL}: {row['estrato_Socio_Economico']}\n{Fore.RED}Idioma:{Style.RESET_ALL} {', '.join(row['idiomas'].split(','))}\n{Fore.RED}Zona:{Style.RESET_ALL} {row['zona']}\n{Fore.RED}Localidad:{Style.RESET_ALL} {row['localidad']}{Style.RESET_ALL}\n{Fore.RED}Jornada:{Style.RESET_ALL} {row['jornadas']}\n")
            print('-' * 50 + '\n')
    if not colegios_encontrados:
        print('\n')
        print(Fore.YELLOW + "No se encontraron colegios que coincidan con los filtros proporcionados." + Style.RESET_ALL)
        print('\n')
    



#-------------------GRAFICAS SOBRE COLGIOS-------------------

mensaje_graficas()

# FUNCION PARA DEFINIR SI VER O NO LAS GRAFICAS

def obtener_respuesta():
    respuesta = input("Por favor, responda con 'sí' o 'no'. para ver las gráficas de información general, según lo que desee." + '\n')
    if respuesta.lower() in ['si', 'sí']:
        return True
    else:
        return False
    
si_no_pregunta = obtener_respuesta()

# SEPARAR LOS DATOS DE LOS COLEGIOS PARA GRAFICARLOS

colegios_discapacitados = []
colegios_no_discapacitados = []
jornadas_manana = []
jornadas_completa = []
jornadas_nocturna = []

estrato_1 = []
estrato_2 = []
estrato_3 = []
estrato_4 = []

ingles = []
otro = []

urbana = []
rural = []



with open('datos.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row['discapacidades'] != '':
            colegios_discapacitados.append(row['nombreestablecimiento'])
        else:
            colegios_no_discapacitados.append(row['nombreestablecimiento'])
        if row['jornadas'] == 'MAÑANA':
            jornadas_manana.append(row['nombreestablecimiento'])
        elif row['jornadas'] == 'COMPLETA':
            jornadas_completa.append(row['nombreestablecimiento'])
        elif row['jornadas'] == 'NOCTURNA':
            jornadas_nocturna.append(row['nombreestablecimiento'])
        if row['estrato_Socio_Economico'] == '1':
            estrato_1.append(row['nombreestablecimiento'])
        elif row['estrato_Socio_Economico'] == '2':
            estrato_2.append(row['nombreestablecimiento'])
        elif row['estrato_Socio_Economico'] == '3':
            estrato_3.append(row['nombreestablecimiento'])
        elif row['estrato_Socio_Economico'] == '4':
            estrato_4.append(row['nombreestablecimiento'])
        if row['idiomas'] == 'INGLES' or row['idiomas'] == 'INGLÉS':
            ingles.append(row['nombreestablecimiento'])
        elif row['idiomas'] == 'FRANCES, ALEMAN' or row['idiomas'] == 'FRANCÉS, ALEMÁN' or row['idiomas'] == 'ALEMAN, FRANCES' or row['idiomas'] == 'ALEMÁN, FRANCÉS' or row['idiomas'] == 'FRANCES' or row['idiomas'] == 'FRANCÉS' or row['idiomas'] == 'ALEMAN' or row['idiomas'] == 'ALEMÁN':
            otro.append(row['nombreestablecimiento'])
        if row['zona'] == 'URBANA':
            urbana.append(row['nombreestablecimiento'])
        elif row['zona'] == 'RURAL':
            rural.append(row['nombreestablecimiento'])

    if si_no_pregunta:
        plt.bar(['Discapacitados', 'No discapacitados'], [len(colegios_discapacitados), len(colegios_no_discapacitados)])
        plt.title('Colegios con espacio para discapacitados')
        plt.xlabel('Discapacidades')
        plt.ylabel('Cantidad de colegios')
        plt.show()

        plt.bar(['Mañana', 'Completa', 'Nocturna'], [len(jornadas_manana), len(jornadas_completa), len(jornadas_nocturna)])
        plt.title('Jornadas de los colegios')
        plt.xlabel('Jornadas')
        plt.ylabel('Cantidad de colegios')
        plt.show()

        plt.bar(['Estrato 1', 'Estrato 2', 'Estrato 3', 'Estrato 4'], [len(estrato_1), len(estrato_2), len(estrato_3), len(estrato_4)])
        plt.title('Estratos de los colegios')
        plt.xlabel('Estratos')
        plt.ylabel('Cantidad de colegios')
        plt.show()

        plt.bar(['Ingles', 'Otros'], [len(ingles), len(otro)])
        plt.title('Idiomas de los colegios')
        plt.xlabel('Idiomas')
        plt.ylabel('Cantidad de colegios')
        plt.show()

        plt.bar(['Urbana', 'Rural'], [len(urbana), len(rural)])
        plt.title('Zonas de los colegios')
        plt.xlabel('Zonas')
        plt.ylabel('Cantidad de colegios')
        plt.show()
    
    else:
        print("No se mostrarán las gráficas de información general. Pasaremos a la siguiente sección.")
    

print('\n')

#-------------------PUNTAJES-------------------

mensaje_graficas_icfes()


# FUNCION PARA REVISAR LA OPCION DEL USUARIO PARA DARLE LAS GRAFICAS DE LOS COLEGIOS SEGÚN EL ICFES
def obtener_opcion():
    op = input("Digite '1': Promedio de 201 a 250. '2': Promedio de 251 a 300. '3': Promedio de 301 a 350. '4': Promedio de 351 a 400: ")
    if op in ['1', '2', '3', '4']:
        return int(op)
    print("Por favor, ingrese una opción válida.")
    return obtener_opcion()


colegios_seleccionados = [] #Array para meter todos los colegios que cumplen con la condición que haya digitado el usuario anteriormente
op = obtener_opcion()

with open('PUNTAJES_BOGOTA.csv', 'r', encoding='latin-1') as reader:
    colegios = []
    for line in reader:
        #ESTOS SI SE PUEDEN MANTENER EN STRING
        campos = line.split(";")
        nombre = campos[0]
        localidad = campos[1]
        calendario = campos[2]
        naturaleza = campos[3]

        # CONVIERTO A ENTEROS LAS COLUMNAS QUE TIENEN LO DE LOS PROMEDIOS DE CADA COMPONENTE DEL ICFES
        if campos[4]:
            lectura = int(campos[4])
        else:
            lectura = 0 #Toca igualar a cero porque hay algunas celdas en el excel que están vacías

        if campos[5]:
            matematicas = int(campos[5])
        else:
            matematicas = 0

        if campos[6]:
            sociales = int(campos[6])
        else:
            sociales = 0

        if campos[7]:
            ciencias = int(campos[7])
        else:
            ciencias = 0

        if campos[8]:
            ingles = int(campos[8])
        else:
            ingles = 0

        if campos[9]:
            total = int(campos[9])
        else:
            total = 0

        #Agrego a la lista de seleccionados
        if op == 1:
          if  total>=201 and total<=250:
            colegios_seleccionados.append((nombre, localidad, calendario, naturaleza, lectura, matematicas, sociales, ciencias, ingles, total))

        elif op == 2:
          if total>=251 and total<=300:
            colegios_seleccionados.append((nombre, localidad, calendario, naturaleza, lectura, matematicas, sociales, ciencias, ingles, total))

        elif op == 3:
          if total>=301 and total<=251:
            colegios_seleccionados.append((nombre, localidad, calendario, naturaleza, lectura, matematicas, sociales, ciencias, ingles, total))

        elif op == 4:
          if total>=351 and total<=400:
            colegios_seleccionados.append((nombre, localidad, calendario, naturaleza, lectura, matematicas, sociales, ciencias, ingles, total))

#GRÁFICAS
for colegio in colegios_seleccionados:
    nombre, localidad, calendario, naturaleza, lectura, matematicas, sociales, ciencias, ingles, total = colegio
    categorias = ['Lectura', 'Matemáticas', 'Sociales', 'Ciencias', 'Inglés']
    valores = [lectura, matematicas, sociales, ciencias, ingles]
    plt.bar(categorias, valores)#No pude para que fuera cada barra de diferente color
    plt.title(f'Puntajes para total en el rango seleccionado: \n Colegio: {nombre} \n Localidad: {localidad} \n Calendario: {calendario} \n Naturaleza: {naturaleza} \n')
    plt.xlabel('Materias')
    plt.ylabel('Puntajes')
    plt.show()