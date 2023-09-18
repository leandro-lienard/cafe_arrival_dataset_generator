from datetime import datetime, timedelta
import random


# ----------------------------------------------------------------------------------------------------- #
#simulacion de un dia abre de 8 a 20
# horario pico 9:30-11:00 y 16:30-19:00 

def calculate_mins_to_next_arrival_normal():
    return random.randint(0, 25)

def calculate_mins_to_next_arrival_hr_pico():
    return random.randint(0, 7)

def is_between(date_to_compare, begin, end):
    return (date_to_compare >= begin) & (date_to_compare < end)

def is_hr_pico(comparing_date):
    return (is_between(comparing_date, INICIO_HR_PICO_1, FIN_HR_PICO_1)) or (is_between(comparing_date, INICIO_HR_PICO_2, FIN_HR_PICO_2))

def calculate_mins_to_next_arrival(actual):
    if(is_hr_pico(actual)):
        return calculate_mins_to_next_arrival_hr_pico()
    else:
        return calculate_mins_to_next_arrival_normal()
    
NRO_PERSONAS = 100
INICIO = datetime(2023, 9, 14, 8, 0, 0)
FIN = datetime(2023, 9, 14, 20, 0, 0)

INICIO_HR_PICO_1 = datetime(2023, 9, 14, 9, 30, 0) # 9:30
FIN_HR_PICO_1 = datetime(2023, 9, 14, 11, 0, 0) # 11:00
INICIO_HR_PICO_2 = datetime(2023, 9, 14, 16, 30, 0) # 16:30
FIN_HR_PICO_2 = datetime(2023, 9, 14, 19, 0, 0)     # 19:00 

print(INICIO.strftime('%H:%M:%S'))

i = 0
actual_time = INICIO
while(actual_time <  FIN):
    i = i + 1
    mins_to_next_arrival = calculate_mins_to_next_arrival(actual = actual_time)

    actual_time = actual_time + timedelta(minutes=mins_to_next_arrival)
    print( actual_time.strftime('%H:%M:%S')) #, "hr_pico: ", is_hr_pico(actual_time))

print("totales: ", i)



