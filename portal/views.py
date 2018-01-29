from django.shortcuts import render
from django.http import HttpResponse 

def welcome_page(request):
  return render(request, 'pages/welcome_page.html')
