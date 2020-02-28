from django.shortcuts import render,redirect
from django.http import JsonResponse
import platform
import django
import website.static.bel as bel
from datetime import datetime, timedelta 
import website.models as models
import os
from django.db import connection

def Index(request):
    #client_address = request.META['HTTP_X_FORWARDED_FOR']#web
    #client_address = request.META['REMOTE_ADDR']#local
    #information = Information()+'Ip Client '+client_address
    try:
    	if request.method =='GET':
        	os.remove('website/static/website/audio/voice.mp3')
    except Exception:
        print('Arquivo nao encontrado: "website/static/website/voice.mp3"')	
    return render(request,'index.html')

def Ajax(request):
    message = bel.Main.Talk(request.GET.get('text'))
    return JsonResponse({'message': message})

def Remove(request):
    data_classification = models.Base_Classification.objects.filter(id=request.GET.get('id'))
    data_previous = models.Base_Previous.objects.filter(classification=data_classification[0].classification)
    data_response = models.Base_Response.objects.filter(classification=data_classification[0].classification)
    data_next = models.Base_Next.objects.filter(classification=data_classification[0].classification)
    for base_classification in data_classification:
        base_classification.delete()
    for base_previous in data_previous:
        base_previous.delete()
    for base_response in data_response:
        base_response.delete()
    for base_next in data_next:
        base_next.delete()  
    message = 'registro removido'
    return JsonResponse({'message': message})

def Delete(id):
    data_classification = models.Base_Classification.objects.filter(id=id)
    data_previous = models.Base_Previous.objects.filter(classification=data_classification[0].classification)
    data_response = models.Base_Response.objects.filter(classification=data_classification[0].classification)
    data_next = models.Base_Next.objects.filter(classification=data_classification[0].classification)
    for base_classification in data_classification:
        base_classification.delete()
    for base_previous in data_previous:
        base_previous.delete()
    for base_response in data_response:
        base_response.delete()
    for base_next in data_next:
        base_next.delete()

def Insert(request):
    if request.method =='POST':
       base = models.Base_Classification.objects.filter(classification=request.POST.get('classification'))
       if len(base)==0:
           form_classification = models.Base_Classification(classification=request.POST.get('classification'),phrase=request.POST.get('key'))
           form_classification.save() 
       null_previous = models.Base_Previous(classification=request.POST.get('classification'),phrase='')
       null_previous.save()
       for base_previous in request.POST.getlist('previous[]'):
           if(base_previous!=''):
              form_previous = models.Base_Previous(classification=request.POST.get('classification'),phrase=base_previous)
              form_previous.save()
       for base_response in request.POST.getlist('response[]'):
           form_response = models.Base_Response(classification=request.POST.get('classification'),phrase=base_response)
           form_response.save()
       null_next = models.Base_Next(classification=request.POST.get('classification'),phrase='')
       null_next.save()
       for base_next in request.POST.getlist('next[]'):
           if(base_next!=''):
              form_next = models.Base_Next(classification=request.POST.get('classification'),phrase=base_next)
              form_next.save() 
       
       return redirect('/list')
    return render(request,'insert.html')

def Edit(request):
    code = request.GET.get('id')
    form_classification = models.Base_Classification.objects.filter(id=code)
    for data in form_classification:
        form_previous = models.Base_Previous.objects.filter(classification=data.classification)
        form_response = models.Base_Response.objects.filter(classification=data.classification)
        form_next = models.Base_Next.objects.filter(classification=data.classification)
    if request.method =='POST':
      try:
          classification = request.POST.get('search')
          phrase = request.POST.get('key')
          code= request.POST.get('code')
          cursor = connection.cursor()
          cursor.execute("DELETE FROM base_previous  WHERE classification='"+str(classification)+"'")
          cursor.execute("DELETE FROM base_response  WHERE classification='"+str(classification)+"'")
          cursor.execute("DELETE FROM base_next  WHERE classification='"+str(classification)+"'")
          cursor.execute("UPDATE base_classification SET classification='"+str(request.POST.get('classification'))+"', phrase='"+phrase+"' WHERE id='"+code+"'")
          Insert(request)
          return redirect('/list')
      except Exception as e:
          print(str(e))
    context = {'data_classification':form_classification,'data_previous':form_previous,'data_response':form_response,'data_next':form_next}
    return render(request,'edit.html',context)
      

def List(request):
    classification = models.Base_Classification.objects.all()
    context = {'classification':classification}
    return render(request,'list.html',context)

def Information():
    py_version = 'Python '+platform.python_version()
    django_version = 'Django '+django.get_version()
    sytem_version = platform.system()+' '+platform.release()
    processor = platform.processor()
    information = 'America/Campo Grande |'+py_version+' |'+django_version+' |'+sytem_version+' |'+processor+' |'
    return information
  