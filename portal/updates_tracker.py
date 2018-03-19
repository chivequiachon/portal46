from portal import fb_updates

def check_cookie_fb(cookie, fb_group_infos):
    # format: info_post_count1|info_post_count2|info_post_count3|......
    cookie_values = cookie.split('|')
    updated_fb_grps_ids = []
    for cookie_val, fb_grp_info in zip(cookie_values, fb_group_infos):
        int_val = int(cookie_val)
        if int_val < fb_grp_info.post_count:
            updated_fb_grps_ids.append(fb_grp_info.id)

    return updated_fb_grps_ids


def check_cookie_blog(cookie, blogs):
    # format: info_post_count1|info_post_count2|info_post_count3|......
    cookie_values = cookie.split('|')
    updated_blogs = []
    for cookie_val, blog in zip(cookie_values, blogs):
        int_val = int(cookie_val)
        if int_val < blog.blog_posts_n:
            updated_blogs.append(blog.blog_name)

    return updated_blogs

