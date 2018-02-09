from django.shortcuts import render
from django.http import HttpResponse 

from portal.models import SubtitleFile

def welcome_page(request):
  return render(request, 'pages/welcome_page.html')

def about_me(request):
  return render(request, 'pages/about_me.html')

def subs_download(request):
  return render(request, 'pages/subtitles_page.html')

def subs_list(request):
  subs = None
  subs_type = request.GET.get('subs', 'nogichuu')
  if subs_type == "nogichuu":
    subs = SubtitleFile.objects.filter(subtitle_name__contains='Construction').order_by('subtitle_name')
  elif subs_type == "nogibingo":
    subs = SubtitleFile.objects.filter(subtitle_name__contains='NOGIBINGO').order_by('subtitle_name')
  elif subs_type == "nogiten":
    subs = SubtitleFile.objects.filter(subtitle_name__contains='Nogiten').order_by('subtitle_name')
  return render(request, 'pages/subs_list.html', {'subs':subs})

