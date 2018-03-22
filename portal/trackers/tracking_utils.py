from ..fb import fb_updates
from ..blogs import blog_check


def check_cookie(request, groups_n, cookie_name):
    # generate default cookie value
    default_val = '|'.join(["00" for i in range(groups_n)])

    # check cookie existence
    set_new_empty_cookie = True
    val = default_val
    if cookie_name in request.COOKIES:
        val = request.COOKIES[cookie_name]
        if len(val) == len(default_val):
            set_new_empty_cookie = False
            val = default_val

    return val, set_new_empty_cookie



def track_updated_fb_pages(cookie, fb_pages):
    # format: info_post_count1|info_post_count2|info_post_count3|......
    cookie_values = cookie.split('|')
    updated_fb_page_ids = []
    for cookie_val, fb_page in zip(cookie_values, fb_pages):
        int_val = int(cookie_val)
        if int_val != fb_page.post_count:
            updated_fb_page_ids.append(fb_page.page_id)

    return updated_fb_page_ids


def track_updated_blogs(cookie, blogs):
    # format: info_post_count1|info_post_count2|info_post_count3|......
    cookie_values = cookie.split('|')
    updated_blogs = []
    for cookie_val, blog in zip(cookie_values, blogs):
        int_val = int(cookie_val)
        if int_val != blog.blog_posts_n:
            updated_blogs.append(blog.blog_name)

