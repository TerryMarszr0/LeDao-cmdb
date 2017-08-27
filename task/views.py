from django.shortcuts import render

# Create your views here.

from celery import  Celery



broker = 'redis://10.1.20.111:6379'
backend = 'redis://10.1.20.111:6379/0'

app = Celery( broker=broker, backend=backend)

@app.task
def add(x,y):
    return x+y


add.delay(2,8)







