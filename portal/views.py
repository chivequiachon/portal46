from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.conf import settings

from portal import fb_updates, stage48_updates, onehallyu_updates, endecoder
from portal.blog_check import BlogCheck
from portal.ikuchancheeks_updates import IkuchancheeksCheckStrategy
from portal.conjyak_updates import ConjyakCheckStrategy
from portal.depressingsubs_updates import DepressingSubsCheckStrategy
from portal.models import SubtitleFile, Credential, FbPage

import datetime



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
  access_token = fb_updates.get_access_token(settings.FB_CLIENT_ID, settings.FB_CLIENT_SECRET)
  target_date = fb_updates.get_target_date()

  fb_pages = FbPage.objects.all()
  fb_group_infos = []
  for fb_page in fb_pages:
    fb_posts = fb_updates.get_fb_group_posts(target_date, fb_page.page_id, access_token)
    npost = len(fb_posts)
    fb_group_infos.append(fb_updates.FbGroup(fb_page.name, fb_page.page_id, fb_posts, npost))
    
  ## Get Stage48 Updates
  s48_credential = Credential.objects.filter(forum__contains='stage48')
  s48_username = endecoder.decode(s48_credential[0].username)
  s48_password = endecoder.decode(s48_credential[0].password)
  
  s48_alerts_page = stage48_updates.get_alerts_page(s48_username, s48_password)
  s48_alerts = stage48_updates.get_alerts(s48_alerts_page)
  s48_alerts_n = len(s48_alerts)
  
  ## Get OneHallyu Updates
  onehallyu_auth_key = settings.ONEHALLYU_AUTH_KEY
  onehallyu_credential = Credential.objects.filter(forum__contains='onehallyu')
  onehallyu_username = endecoder.decode(onehallyu_credential[0].username)
  onehallyu_password = endecoder.decode(onehallyu_credential[0].password)
  
  onehallyu_notifs_page = onehallyu_updates.get_notifications_page(onehallyu_auth_key, onehallyu_username, onehallyu_password)
  onehallyu_notifs = onehallyu_updates.get_notifications(onehallyu_notifs_page)
  onehallyu_notifs_n = len(onehallyu_notifs)

  ## Get blog updates
  blogs = []

  # Ikuchancheeks
  now = datetime.datetime.now()
  ikuchancheeks_check_strategy = IkuchancheeksCheckStrategy(now.year, now.month)
  ikuchancheeks_check = BlogCheck(ikuchancheeks_check_strategy, "Ikuchancheeks", "https://ikuchancheeks.blogspot.co.id/", "{}/{}".format(now.year, now.month))
  ikuchancheeks_check.check_updates()
  blogs.append(ikuchancheeks_check)

  # Conjyak
  conjyak_check_strategy = ConjyakCheckStrategy(now.year, now.month)
  conjyak_check = BlogCheck(conjyak_check_strategy, "Conjyak", "https://conjyak.wordpress.com/", "{}/{}".format(now.year, now.month))
  conjyak_check.check_updates()
  blogs.append(conjyak_check)

  # DepressingSubs
  depressingsubs_check_strategy = DepressingSubsCheckStrategy(now.year, now.month)
  depressingsubs_check = BlogCheck(depressingsubs_check_strategy, "DepressingSubs", "http://depressingsubs.com/", "{}/{}".format(now.year, now.month))
  depressingsubs_check.check_updates()
  blogs.append(depressingsubs_check)


  data = {
    'fb_group_infos': fb_group_infos,
    'fb_target_date': target_date,
    'stage48_alerts': s48_alerts,
    'stage48_alerts_n': s48_alerts_n,
    'onehallyu_notifs': onehallyu_notifs,
    'onehallyu_notifs_n': onehallyu_notifs_n,
    'blog_updates': blogs,
  }
    
  return render(request, 'pages/updates.html', data)

