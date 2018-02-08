from django.shortcuts import render
from django.http import HttpResponse 

from portal.models import SubtitleFile

def welcome_page(request):
  return render(request, 'pages/welcome_page.html')

def about_me(request):
  return render(request, 'pages/about_me.html')

def subs_download(request):
  return render(request, 'pages/subtitles_page.html')

def nogiten_subs_download(request):
  subs = SubtitleFile.objects.filter(subtitle_name__contains='Nogiten').order_by('subtitle_name')
  return render(request, 'pages/nogiten_subs.html', {'subs':subs})

def nogibingo_subs_download(request):
  subs = SubtitleFile.objects.filter(subtitle_name__contains='NOGIBINGO').order_by('subtitle_name')
  return render(request, 'pages/nogibingo_subs.html', {'subs':subs})
