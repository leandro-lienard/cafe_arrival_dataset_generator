from datetime import datetime, timedelta
import random
import pandas as pd 

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
TIEMPO_CONSUMO = 5  # TODO: USAR RANDOM
INTERVALO_PEDIDOS = 10 # TODO: USAR RANDOM

#CONTROL
INTERVALO_LAVADOS = 30
TAZAS_TOTALES = 15

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
TPPC = datetime(2023, 9, 14, 9, 0, 0) # 9:00 # tiempo prox pedido cliente
TPTS = datetime(2023, 9, 14, 9, 0, 0) # 9:00 # tiempo prox taza sucia
TPL = datetime(2023, 9, 14, 9, 0, 0) # 9:00 # tiempo prox lavado

#TIEMPOS
T = datetime(2023, 9, 14, 9, 0, 0) # 9:00
TF  = datetime(2023, 9, 14, 12, 0, 0) # 12:00


def procesar_sgte_lavado():
    global TPL, TAZAS_SUCIAS, LAVADOS_INNECESARIOS, TAZAS_DISPONIBLES
    T = TPL
    TPL = T + timedelta(minutes=INTERVALO_LAVADOS)
    if(TAZAS_SUCIAS > 0):
        LAVADOS_INNECESARIOS = LAVADOS_INNECESARIOS + 1
    else: 
        TAZAS_DISPONIBLES = TAZAS_DISPONIBLES + TAZAS_SUCIAS
        TAZAS_SUCIAS = 0
        
def procesar_sgte_taza_sucia():
    global TAZAS_SUCIAS, TPTS, TIEMPO_CONSUMO
    T = TPTS
    TPTS = T + timedelta(minutes=TIEMPO_CONSUMO) # TODO: USAR RANDOM TC
    TAZAS_SUCIAS = TAZAS_SUCIAS + 1 

def procesar_sgte_pedido():
    global TPPC, TAZAS_SUCIAS, INTERVALO_PEDIDOS, TAZAS_DISPONIBLES, T, RETIRADOS, PEDIDOS_TOTALES, LAVADOS_FORZOSOS
    T = TPPC
    TPPC =  T + timedelta(minutes=INTERVALO_PEDIDOS) #TODO: USAR RANDOM IP
    if(TAZAS_DISPONIBLES > 0):
        TAZAS_DISPONIBLES = TAZAS_DISPONIBLES - 1
    else:
        if(TAZAS_SUCIAS > 0): #lavo
            LAVADOS_FORZOSOS = LAVADOS_FORZOSOS + 1 
            TAZAS_DISPONIBLES = TAZAS_SUCIAS - 1
            TAZAS_SUCIAS = 0 
        else: 
            RETIRADOS = RETIRADOS + 1 
    PEDIDOS_TOTALES = PEDIDOS_TOTALES +1 


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
print("y intervalo lavados:", INTERVALO_PEDIDOS)
print("Promedio lavados innecesarios(PLI) ", PLI, " esta mal calculado deberia hacerse contra lavados totales")
print("Promedio lavado Forzosos (PLF) ", PLF, " esta mal calculado deberia hacerse contra lavados totales")
print("Promedio retirado (RT) ", PR)
    
    





# f = Fitter(df_arrivals_in_mins, distributions=['gamma', 'rayleigh', 'uniform'])
# print(f.fit())
# print(f.summary())
# print(f.get_best())
# print(f.get)