from portal.blogs.blog_check_strategy import BlogCheckStrategy


class BlogCheck(object):
    def __init__(self, blog_check_strategy, blog_name, blog_url, date, blog_cookie_ref_idx):
        self.blog_check_strategy = blog_check_strategy
        self.blog_name = blog_name
        self.blog_url = blog_url
        self.blog_posts = None
        self.blog_posts_n = 0
        self.date = date
        self.blog_cookie_ref_idx = blog_cookie_ref_idx

    def check_updates(self):
        requested_page = self.blog_check_strategy.request_page()
        self.blog_posts = self.blog_check_strategy.scrape(requested_page)
        self.blog_posts_n = len(self.blog_posts)

