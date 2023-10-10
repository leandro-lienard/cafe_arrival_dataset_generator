from datetime import datetime, timedelta
import random
from scipy import stats
import numpy as np
import math
from colorama import init
init(autoreset=True) 


global TPL

# ----------------------------------------------------------------------------------------------------- #
# simulacion de un dia abre de 8 a 20
# horario pico 9:30-11:00 y 16:30-19:00     

#NRO_PERSONAS = 50   
INICIO = datetime(2023, 9, 14, 8, 0, 0)
FIN = datetime(2023, 9, 14, 20, 0, 0)
# 
# INICIO_HR_PICO_1 = datetime(2023, 9, 14, 9, 30, 0) # 9:30
# FIN_HR_PICO_1 = datetime(2023, 9, 14, 11, 0, 0) # 11:00
# INICIO_HR_PICO_2 = datetime(2023, 9, 14, 16, 30, 0) # 16:30
# FIN_HR_PICO_2 = datetime(2023, 9, 14, 19, 0, 0)     # 19:00 



#DATOS
def get_tiempo_consumo():
    return round(stats.beta.ppf(random.random(), 0.8809684438295433, 0.8900744283854006, loc= 24.996392045937338, scale= 15.003607954062664))
    
def get_intervalo_pedidos():
    return round(stats.ncx2.ppf(random.random(), 1.1816142004691113, 2.4431224769406272, loc=-1.2287936235425389e-28, scale=3.8059527763528824))
    
def mins(mins):
    if(mins < 10):
        return '0' + str(mins)
    else:
        return str(mins)
def get_hora(time):
    HORA_INICIO = 9
    return str(math.floor(time / 60) + HORA_INICIO) + ":" + mins(time % 60)

def encontrar_minimo(lista):
  minimo = lista[0]
  for elemento in lista:
    if elemento < minimo:
      minimo = elemento
  return minimo
#CONTROL
print("Inserte intervalo de lavados en mins")
INTERVALO_LAVADOS = int(input()) # 30 o 60
print("Inserte cant tazas totales en unidades")
TAZAS_TOTALES = int(input()) # 10 o 15
# INTERVALO_LAVADOS = 60
# TAZAS_TOTALES  = 5


#ESTADO
TAZAS_SUCIAS = 0
TAZAS_DISPONIBLES = TAZAS_TOTALES

#RESULTADO
LAVADOS_INNECESARIOS = 0
LAVADOS_FORZOSOS  = 0
RETIRADOS = 0

#OTROS
HV = 5000000
PEDIDOS_TOTALES = 0
LAVADOS_TOTALES = 0
#TIEMPOS
T = 0 # 9:00
TF  = 60 * 3  # 12:00

#TEF
TPPC = 0 # 9:00 # tiempo prox pedido cliente
TPTS = HV # 9:00 # tiempo prox taza sucia
TPL = INTERVALO_LAVADOS # 9:00 # tiempo prox lavado


LISTA_TPTS = list()


def procesar_sgte_lavado():
    global TPL, TAZAS_SUCIAS, LAVADOS_INNECESARIOS, TAZAS_DISPONIBLES, INTERVALO_LAVADOS, LAVADOS_TOTALES
    T = TPL
    TPL = T + INTERVALO_LAVADOS
    print("\033[4;34m"+ "TS={ts}, TD={td} LAVADO hora: {hora}".format(ts = TAZAS_SUCIAS, td = TAZAS_DISPONIBLES, hora= get_hora(T)))
    if(TAZAS_SUCIAS > 0):
        TAZAS_DISPONIBLES = TAZAS_DISPONIBLES + TAZAS_SUCIAS
        TAZAS_SUCIAS = 0
    else: 
        LAVADOS_INNECESARIOS = LAVADOS_INNECESARIOS + 1

    LAVADOS_TOTALES = LAVADOS_TOTALES +1 
        
def procesar_sgte_taza_sucia():
    global TAZAS_SUCIAS, LISTA_TPTS, TPTS, TAZAS_DISPONIBLES
    #, TPTS
    T = TPTS
    # TPTS = T + get_tiempo_consumo()
    LISTA_TPTS.remove(TPTS)
    TAZAS_SUCIAS = TAZAS_SUCIAS + 1
    print("\033[4;32mTS={ts}, TD={td} Entrega de taza sucia {time}".format(ts=TAZAS_SUCIAS, td=TAZAS_DISPONIBLES, time = get_hora(T)))
    TPTS = min_or_HV() 

def procesar_sgte_pedido():
    global TPPC, TAZAS_SUCIAS, TAZAS_DISPONIBLES, T, RETIRADOS, PEDIDOS_TOTALES, LAVADOS_FORZOSOS, LISTA_TPTS, LAVADOS_TOTALES 
    T = TPPC
    TPPC =  T + get_intervalo_pedidos()
    PEDIDOS_TOTALES = PEDIDOS_TOTALES + 1
    if(TAZAS_DISPONIBLES > 0):
        TAZAS_DISPONIBLES = TAZAS_DISPONIBLES - 1
    else:
        if(TAZAS_SUCIAS > 0): #lavo
            print("\033[4;33mLAVADO FORZOSO por falta de tazas disponibles {time}".format(time= get_hora(T)))
            LAVADOS_FORZOSOS = LAVADOS_FORZOSOS + 1
            LAVADOS_TOTALES = LAVADOS_TOTALES + 1  
            TAZAS_DISPONIBLES = TAZAS_SUCIAS - 1
            TAZAS_SUCIAS = 0 
        else: 
            print("\033[4;31mRETIRADO por falta de tazas sucias y disponibles")
            RETIRADOS = RETIRADOS + 1 
    LISTA_TPTS.append(T + get_tiempo_consumo())
    print("TS={ts}, TD={td} Cliente nro:{nro} hora: {hora}".format(nro = PEDIDOS_TOTALES,hora= get_hora(T), ts = TAZAS_SUCIAS, td = TAZAS_DISPONIBLES))
 
def min_or_HV():
    global TPTS, LISTA_TPTS, HV
    if(len(LISTA_TPTS) > 0):
        return  min(LISTA_TPTS)
    else: 
        return HV 

# -------------------- INICIO SIMULACION ------------------------------------


while(T <= TF):
    TPTS = min_or_HV()
    if(TPPC <= TPTS):
        if(TPPC <= TPL):
            procesar_sgte_pedido()
        else:
            procesar_sgte_lavado()
    else:
        if(TPL <= TPTS):
            procesar_sgte_lavado()
        else: 
            procesar_sgte_taza_sucia()

PLI = (LAVADOS_INNECESARIOS/LAVADOS_TOTALES) * 100
PLF = (LAVADOS_FORZOSOS/LAVADOS_TOTALES) * 100
PR = (RETIRADOS/PEDIDOS_TOTALES) * 100

print("")
print("--------------------SUMMARY-------------------")
print("")
       
print("Con tazas totales:", TAZAS_TOTALES)
print("y intervalo lavados:", INTERVALO_LAVADOS)
print("Promedio lavados innecesarios(PLI) ", PLI, "%")
print("Promedio lavado Forzosos (PLF) ", PLF,  "%")
print("Promedio retirado (RT) ", PR, "%")
    
    





# f = Fitter(df_arrivals_in_mins, distributions=['gamma', 'rayleigh', 'uniform'])
# print(f.fit())
# print(f.summary())
# print(f.get_best())
# print(f.get)