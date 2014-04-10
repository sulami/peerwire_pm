from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

from news.models import News

@cache_page(60 * 15)
@vary_on_headers('Cookie')
def index(request):
    news_list = News.objects.all().order_by('-pub_date')
    paginator = Paginator(news_list, 5)
    page = request.GET.get('p')
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)
    context = {'news': news}
    return render(request, 'news/index.html', context)

@cache_page(60 * 60)
@vary_on_headers('Cookie')
def newspage(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    context = {'news': news}
    return render(request, 'news/newspage.html', context)

