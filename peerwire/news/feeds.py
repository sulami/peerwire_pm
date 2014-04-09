from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from news.models import News

class NewsFeed(Feed):
    title = "Peerwire News"
    link = "/n/"
    description = "All news Peerwire"

    def items(self):
        return News.objects.order_by('-pub_date')[:5]

    def item_title(self, item):
        return item.title

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return reverse('news:newspage', args=[item.pk])
