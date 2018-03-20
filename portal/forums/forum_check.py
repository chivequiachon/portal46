from portal.forums.forum_check_strategy import ForumCheckStrategy


class ForumCheck(object):
    def __init__(self, forum_check_strategy, forum_name, forum_url, date, forum_cookie_ref_idx):
        self.forum_check_strategy = forum_check_strategy
        self.forum_name = forum_name
        self.forum_url = forum_url
        self.forum_posts = None
        self.forum_posts_n = 0
        self.date = date
        self.forum_cookie_ref_idx = forum_cookie_ref_idx

    def check_updates(self):
        requested_page = self.forum_check_strategy.request_page()
        self.forum_posts = self.forum_check_strategy.scrape(requested_page)
        self.forum_posts_n = len(self.forum_posts)

