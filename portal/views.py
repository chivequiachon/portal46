import datetime
import json

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page

from . import endecoder, constants
from .fb import fb_updates
from .models import SubtitleFile, Credential, FbPage

from .blogs.blog_check import BlogCheck
from .blogs.ikuchancheeks_updates import IkuchancheeksCheckStrategy
from .blogs.conjyak_updates import ConjyakCheckStrategy
from .blogs.depressingsubs_updates import DepressingSubsCheckStrategy

from .forums.forum_check import ForumCheck
from .forums.stage48_updates import Stage48CheckStrategy

from .trackers import tracking_utils


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

        s48_check_strategy = Stage48CheckStrategy(s48_username, s48_password)
        s48_check = ForumCheck(s48_check_strategy, "Stage48", constants.STAGE48_URL, "today", 0)
        s48_check.check_updates()
     
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
            'stage48_updates': s48_check,
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
                cookie_name = constants.FB_COOKIE_NAME
            elif which_cookie == 'blog':
                cookie_name = constants.BLOG_COOKIE_NAME

            cookie_ref_idx = int(json_data['cookie_ref_idx'])
            post_count = json_data['post_count']

            cookie_vals = request.COOKIES[cookie_name].split('|')

            # Pad 0s to string digit if needed
            cookie_vals[cookie_ref_idx] = post_count.zfill(2)
            new_cookie_val = "|".join(cookie_vals)

            ret = HttpResponse("OK")

            # Set cookie with 3 days expiry
            max_age = constants.COOKIE_EXPIRY
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
        for i in range(len(fb_pages)):
            fb_pages[i].retrieve_posts(access_token, target_date) 
        
        ## Check cookies
        groups_n = len(fb_pages) 

        # check cookie existence
        cookie_name = constants.FB_COOKIE_NAME
        val, set_new_empty_cookie = tracking_utils.check_cookie(request, groups_n, cookie_name)

        # show unread
        cookie = request.COOKIES.get(cookie_name, val)
        page_ids_with_updates = tracking_utils.track_updated_fb_pages(cookie, fb_pages)

        data = {
            'fb_pages': fb_pages,
            'fb_target_date': target_date,
            'fb_updated_page_ids': page_ids_with_updates,
        }

        ret = HttpResponse(render_to_string('pages/fb_updates_section.html', data))

        if set_new_empty_cookie:
            ret.set_cookie(cookie_name, val)
      
    return ret

def blog_updates_fetch(request):
    ret = HttpResponse("None")
    if request.is_ajax():
        ## Get blog updates
        blogs = []


        # Ikuchancheeks
        now = datetime.datetime.now()
        since_date_format = "{}/{}".format(now.year, now.month)
        ikuchancheeks_check_strategy = IkuchancheeksCheckStrategy(now.year, now.month)
        ikuchancheeks_check = (
            BlogCheck(ikuchancheeks_check_strategy, "Ikuchancheeks", constants.IKUCHANCHEEKS_URL, since_date_format, constants.IKUCHANCHEEKS_COOKIE_REF_IDX)
        )
        ikuchancheeks_check.check_updates()
        blogs.append(ikuchancheeks_check)

        # Conjyak
        conjyak_check_strategy = ConjyakCheckStrategy(now.year, now.month)
        conjyak_check = BlogCheck(conjyak_check_strategy, "Conjyak", constants.CONJYAK_URL, since_date_format, constants.CONJYAK_COOKIE_REF_IDX)
        conjyak_check.check_updates()
        blogs.append(conjyak_check)

        # DepressingSubs
        depressingsubs_check_strategy = DepressingSubsCheckStrategy(now.year, now.month)
        depressingsubs_check = (
            BlogCheck(depressingsubs_check_strategy, "DepressingSubs", constants.DEPRESSINGSUBS_URL, since_date_format, constants.DEPRESSINGSUBS_COOKIE_REF_IDX)
        )
        depressingsubs_check.check_updates()
        blogs.append(depressingsubs_check)

        ## Check cookies
        blogs_n = len(blogs) 

        # check cookie existence
        cookie_name = constants.BLOG_COOKIE_NAME
        val, set_new_empty_cookie = tracking_utils.check_cookie(request, blogs_n, cookie_name)

        # show unread
        cookie = request.COOKIES.get(cookie_name, val)
        blog_ids_with_updates = tracking_utils.track_updated_blogs(cookie, blogs)

        data = {
            'blog_updates': blogs,
            'updated_blogs': blog_ids_with_updates,
        }

        ret = HttpResponse(render_to_string('pages/blog_updates_section.html', data))

        if set_new_empty_cookie:
            ret.set_cookie(cookie_name, val)

    return ret

def updates(request):
    return render(request, 'pages/updates.html', {})

