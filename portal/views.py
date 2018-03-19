from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string

from portal import fb_updates, stage48_updates, onehallyu_updates, endecoder, updates_tracker
from portal.blog_check import BlogCheck
from portal.ikuchancheeks_updates import IkuchancheeksCheckStrategy
from portal.conjyak_updates import ConjyakCheckStrategy
from portal.depressingsubs_updates import DepressingSubsCheckStrategy
from portal.models import SubtitleFile, Credential, FbPage

import datetime
import json


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


def forum_updates_fetch(request):
  ret = "None"
  if request.is_ajax():
    ## Get Stage48 Updates
    s48_credential = Credential.objects.filter(forum__contains='stage48')
    s48_username = endecoder.decode(s48_credential[0].username)
    s48_password = endecoder.decode(s48_credential[0].password)
  
    s48_alerts_page = stage48_updates.get_alerts_page(s48_username, s48_password)
    s48_alerts = stage48_updates.get_alerts(s48_alerts_page)
    s48_alerts_n = len(s48_alerts)

    ## Get OneHallyu Updates
    #onehallyu_auth_key = settings.ONEHALLYU_AUTH_KEY
    #onehallyu_credential = Credential.objects.filter(forum__contains='onehallyu')
    #onehallyu_username = endecoder.decode(onehallyu_credential[0].username)
    #onehallyu_password = endecoder.decode(onehallyu_credential[0].password)
    # 
    #onehallyu_notifs_page = onehallyu_updates.get_notifications_page(onehallyu_auth_key, onehallyu_username, onehallyu_password)
    #onehallyu_notifs = onehallyu_updates.get_notifications(onehallyu_notifs_page)
    #onehallyu_notifs_n = len(onehallyu_notifs)
   
    data = {
      'stage48_alerts': s48_alerts,
      'stage48_alerts_n': s48_alerts_n,
      #'onehallyu_notifs': onehallyu_notifs,
      #'onehallyu_notifs_n': onehallyu_notifs_n,
    }
 
    ret = render_to_string('pages/forum_updates_section.html', data)
  return HttpResponse(ret)


def update_cookie(request):
  ret = HttpResponse("None")
  if request.is_ajax():
    if request.method == 'POST':
      # Retrieve json data from request body
      json_data = json.loads(request.body.decode('utf-8'))
      which_cookie = json_data['which']

      # Determine which cookie to create/update
      cookie_name = None
      if which_cookie == 'fb':
        cookie_name = 'fb-cookie'
      elif which_cookie == 'blog':
        cookie_name = 'blog-cookie'

      cookie_ref_idx = int(json_data['cookie_ref_idx'])
      post_count = json_data['post_count']

      cookie_vals = request.COOKIES[cookie_name].split('|')

      # Pad 0s to string digit if needed
      cookie_vals[cookie_ref_idx] = post_count.zfill(2)
      new_cookie_val = "|".join(cookie_vals)

      ret = HttpResponse("OK")

      # Set cookie with 3 days expiry
      max_age = 3 * 24 * 60 * 60
      expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
      ret.set_cookie(cookie_name, new_cookie_val, max_age=max_age, expires=expires)
    
  return ret


def fb_updates_fetch(request):
  ret = HttpResponse("None")
  if request.is_ajax():
    ## Get Facebook Updates
    access_token = fb_updates.get_access_token(settings.FB_CLIENT_ID, settings.FB_CLIENT_SECRET)
    target_date = fb_updates.get_target_date()

    fb_pages = FbPage.objects.all()
    fb_group_infos = []
    for fb_page in fb_pages:
      fb_posts = fb_updates.get_fb_group_posts(target_date, fb_page.page_id, access_token)
      npost = len(fb_posts)
      fb_group_infos.append(fb_updates.FbGroup(fb_page.name, fb_page.page_id, fb_posts, fb_page.img_url, npost, fb_page.cookie_ref_idx))

    ## Check cookies
    groups_n = len(fb_pages) 

    # generate default cookie value
    default_val = '|'.join(["00" for i in range(groups_n)])

    # check cookie existence
    cookie_name = 'fb-cookie'
    set_new_empty_cookie = True
    val = default_val
    if cookie_name in request.COOKIES:
        val = request.COOKIES[cookie_name]
        if len(val) == len(default_val):
            set_new_empty_cookie = False
            val = default_val

    # show unread
    cookie = request.COOKIES.get(cookie_name, val)
    grp_ids_with_updates = updates_tracker.check_cookie_fb(cookie, fb_group_infos)

    data = {
      'fb_group_infos': fb_group_infos,
      'fb_target_date': target_date,
      'fb_updated_grp_ids': grp_ids_with_updates,
    }

    ret = HttpResponse(render_to_string('pages/fb_updates_section.html', data))

    if set_new_empty_cookie:
        ret.set_cookie(cookie_name, default_val)
    
  return ret


def blog_updates_fetch(request):
  ret = HttpResponse("None")
  if request.is_ajax():
    ## Get blog updates
    blogs = []

    # Ikuchancheeks
    now = datetime.datetime.now()
    ikuchancheeks_check_strategy = IkuchancheeksCheckStrategy(now.year, now.month)
    ikuchancheeks_check = BlogCheck(ikuchancheeks_check_strategy, "Ikuchancheeks", "https://ikuchancheeks.blogspot.co.id/", "{}/{}".format(now.year, now.month), 0)
    ikuchancheeks_check.check_updates()
    blogs.append(ikuchancheeks_check)

    # Conjyak
    conjyak_check_strategy = ConjyakCheckStrategy(now.year, now.month)
    conjyak_check = BlogCheck(conjyak_check_strategy, "Conjyak", "https://conjyak.wordpress.com/", "{}/{}".format(now.year, now.month), 1)
    conjyak_check.check_updates()
    blogs.append(conjyak_check)

    # DepressingSubs
    depressingsubs_check_strategy = DepressingSubsCheckStrategy(now.year, now.month)
    depressingsubs_check = BlogCheck(depressingsubs_check_strategy, "DepressingSubs", "http://depressingsubs.com/", "{}/{}".format(now.year, now.month), 2)
    depressingsubs_check.check_updates()
    blogs.append(depressingsubs_check)

    ## Check cookies
    blogs_n = len(blogs) 

    # generate default cookie value
    default_val = '|'.join(["00" for i in range(blogs_n)])

    # check cookie existence
    cookie_name = 'blog-cookie'
    set_new_empty_cookie = True
    val = default_val
    if cookie_name in request.COOKIES:
        val = request.COOKIES[cookie_name]
        if len(val) == len(default_val):
            set_new_empty_cookie = False
            val = default_val

    # show unread
    cookie = request.COOKIES.get(cookie_name, val)
    blog_ids_with_updates = updates_tracker.check_cookie_blog(cookie, blogs)

    data = {
      'blog_updates': blogs,
      'updated_blogs': blog_ids_with_updates,
    }

    ret = HttpResponse(render_to_string('pages/blog_updates_section.html', data))

    if set_new_empty_cookie:
        ret.set_cookie(cookie_name, default_val)


  return ret


def updates(request):
  return render(request, 'pages/updates.html', {})

