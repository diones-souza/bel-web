# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 12:38:15 2018

@author: John
"""

from datetime import datetime, timezone,timedelta 

def Now():
    now = datetime.now()
    difference = timedelta(hours=-4)
    timezones = timezone(difference)
    now = now.astimezone(timezones)
    print(now)
    return now

'''
WeekDay serve para saber o dia da semana conforme a classificação feita pela analize 
'''
def WeekDay(temp):
   now = Now()
   day = ('Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo')
   if now.weekday()+temp>6:
       week_day = day[0]
   else:
       week_day = day[now.weekday()+temp]
   return week_day
    
'''
Date serve para saber a data conforme a classificação feita pela analize 
'''
    
def Date(temp):
    now = Now()
    day = now.day+temp
    month = ('','Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro')
    month = month[now.month]
    year = now.year
    date = str(day)+' de '+ str(month)+' de '+ str(year)
    return date
'''
Hours serve para saber a hora atual 
'''
    
def Hours():
    now = Now()
    hours = now.strftime('%H:%M')
    return hours
'''
Shift serve para saber o turno atual que estamos 
'''
    
def Shift():
    now = Now()
    hour = now.hour
    if int(hour)>11 and int(hour)<19:
        shift='boa tarde'
    if int(hour)>18 or int(hour)<5:
        shift='boa noite'
    if int(hour)>5 and int(hour)<12:
        shift='bom dia' 
    return shift

class Treatment:
    
    '''
    ClassifyTreatment faz o tratamento das classificações
    especias como data e hora. adicionando novas possiveis respostas
    '''
    def ClassifyTreatment(class_name,response):
        if class_name=='saudacao':
            response.append(Shift())
        if class_name=='hora':
            response.append('pelo meu relógio, agora são '+Hours())
            response.append('são '+Hours())
            response.append('agora são '+Hours())
            response.append('agora são exatamente '+Hours())
            response.append('são exatamente '+Hours())
        if class_name=='ontem':
            response.append('ontem foi '+WeekDay(-1)+' dia '+Date(-1))
        if class_name=='hoje':
            response.append('hoje é '+WeekDay(0)+' dia '+Date(0))
        if class_name=='amanha':
            response.append('amanha vai ser '+WeekDay(1)+' dia '+Date(1))
     
    
    
