from django.shortcuts import render
from django.views.decorators.cache import cache_page

from portal import fb_updates
from portal.models import SubtitleFile

def welcome_page(request):
  return render(request, 'pages/welcome_page.html')

def about_me(request):
  return render(request, 'pages/about_me.html')

def subs_download(request):
  return render(request, 'pages/subtitles_page.html')

@cache_page(60 * 15)
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

def updates(request):
  access_token = fb_updates.get_access_token()
  target_date = fb_updates.get_target_date()

  fb_group_infos = []
  for id in fb_updates.FB_GROUPS:
    npost = fb_updates.get_fb_group_posts_number(target_date, id, access_token)
    fb_group_infos.append(fb_updates.FbGroup(fb_updates.FB_GROUPS[id], id, npost))

  return render(request, 'pages/updates.html', {'fb_group_infos': fb_group_infos, 'target_date': target_date})

