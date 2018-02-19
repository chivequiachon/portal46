from django.shortcuts import render
from django.views.decorators.cache import cache_page

from portal import fb_updates, stage48_updates, onehallyu_updates
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
  ## Get Facebook Updates
  access_token = fb_updates.get_access_token()
  target_date = fb_updates.get_target_date()

  fb_group_infos = []
  for id in fb_updates.FB_GROUPS:
    fb_posts = fb_updates.get_fb_group_posts(target_date, id, access_token)
    npost = len(fb_posts)
    fb_group_infos.append(fb_updates.FbGroup(fb_updates.FB_GROUPS[id], id, fb_posts, npost))
    
  ## Get Stage48 Updates
  s48_alerts_page = stage48_updates.get_alerts_page("chivequiachon@gmail.com", "GatewAy1011")
  s48_alerts = stage48_updates.get_alerts(s48_alerts_page)
  s48_alerts_n = len(s48_alerts)
  
  ## Get OneHallyu Updates
  login_data = {'auth_key': '880ea6a14ea49e853634fbdc5015a024', 'ips_username': 'Chubo', 'ips_password': 'GatewAy1011'}
  onehallyu_notifs_page = onehallyu_updates.get_notifications_page(login_data['auth_key'], login_data['ips_username'], login_data['ips_password'])
  onehallyu_notifs = onehallyu_updates.get_notifications(onehallyu_notifs_page)
  onehallyu_notifs_n = len(onehallyu_notifs)
  

  return render(request, 'pages/updates.html', {'fb_group_infos': fb_group_infos, 'fb_target_date': target_date, 'stage48_alerts': s48_alerts, 'stage48_alerts_n': s48_alerts_n, 'onehallyu_notifs': onehallyu_notifs, 'onehallyu_notifs_n': onehallyu_notifs_n})

