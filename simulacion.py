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

#CONTROL
print("Inserte cant lavados en mins")
INTERVALO_LAVADOS = int(input()) # 30 o 60
print("Inserte cant tazas totales en unidades")
TAZAS_TOTALES = int(input()) # 10 o 15

#ESTADO
TAZAS_SUCIAS = 0
TAZAS_DISPONIBLES = TAZAS_TOTALES

#RESULTADO
LAVADOS_INNECESARIOS = 0
LAVADOS_FORZOSOS  = 0
RETIRADOS = 0

#OTROS
PEDIDOS_TOTALES = 0
HV = 5000000

#TEF
TPPC = 0 # 9:00 # tiempo prox pedido cliente
TPTS = 0 # 9:00 # tiempo prox taza sucia
TPL = INTERVALO_LAVADOS # 9:00 # tiempo prox lavado

#TIEMPOS
T = 0 # 9:00
TF  = 60 * 3  # 12:00


def procesar_sgte_lavado():
    global TPL, TAZAS_SUCIAS, LAVADOS_INNECESARIOS, TAZAS_DISPONIBLES, INTERVALO_LAVADOS
    T = TPL
    TPL = T + INTERVALO_LAVADOS
    print("\033[4;35m"+ "LAVADO TS={ts}, TD={td} hora: {hora}".format(ts = TAZAS_SUCIAS, td = TAZAS_DISPONIBLES, hora= get_hora(T)))
    if(TAZAS_SUCIAS > 0):
        TAZAS_DISPONIBLES = TAZAS_DISPONIBLES + TAZAS_SUCIAS
        TAZAS_SUCIAS = 0
    else: 
        LAVADOS_INNECESARIOS = LAVADOS_INNECESARIOS + 1

        
def procesar_sgte_taza_sucia():
    global TAZAS_SUCIAS, TPTS
    T = TPTS
    TPTS = T + get_tiempo_consumo()
    print("\033[4;32mEntrega de taza sucia")
    TAZAS_SUCIAS = TAZAS_SUCIAS + 1 

def procesar_sgte_pedido():
    global TPPC, TAZAS_SUCIAS, TAZAS_DISPONIBLES, T, RETIRADOS, PEDIDOS_TOTALES, LAVADOS_FORZOSOS
    T = TPPC
    TPPC =  T + get_intervalo_pedidos()
    if(TAZAS_DISPONIBLES > 0):
        TAZAS_DISPONIBLES = TAZAS_DISPONIBLES - 1
    else:
        if(TAZAS_SUCIAS > 0): #lavo
            LAVADOS_FORZOSOS = LAVADOS_FORZOSOS + 1 
            TAZAS_DISPONIBLES = TAZAS_SUCIAS - 1
            TAZAS_SUCIAS = 0 
        else: 
            RETIRADOS = RETIRADOS + 1 
    PEDIDOS_TOTALES = PEDIDOS_TOTALES + 1
    print("Cliente nro:{nro} hora: {hora}".format(nro = PEDIDOS_TOTALES,hora= get_hora(T)))
 


# -------------------- INICIO SIMULACION ------------------------------------

while(T <= TF):
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

PLI = (LAVADOS_INNECESARIOS/PEDIDOS_TOTALES) * 100
PLF = (LAVADOS_FORZOSOS/PEDIDOS_TOTALES) * 100
PR = (RETIRADOS/PEDIDOS_TOTALES) * 100

print("")
print("--------------------SUMMARY-------------------")
print("")
       
print("Con tazas totales:", TAZAS_TOTALES)
print("y intervalo lavados:", INTERVALO_LAVADOS)
print("Promedio lavados innecesarios(PLI) ", PLI, " esta mal calculado deberia hacerse contra lavados totales")
print("Promedio lavado Forzosos (PLF) ", PLF, " esta mal calculado deberia hacerse contra lavados totales")
print("Promedio retirado (RT) ", PR)
    
    





# f = Fitter(df_arrivals_in_mins, distributions=['gamma', 'rayleigh', 'uniform'])
# print(f.fit())
# print(f.summary())
# print(f.get_best())
# print(f.get)