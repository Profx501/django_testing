from django.conf import settings
from django.urls import reverse


def test_home_page(client, news_10):
    urls = reverse('news:home')
    response = client.get(urls)
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, news_10):
    urls = reverse('news:home')
    response = client.get(urls)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_detail_page_contains_form(author_client, news):
    url = reverse('news:detail', args=(news.id,))
    response = author_client.get(url)
    assert 'form' in response.context


def test_detail_page_contains_form_for_user(client, news):
    url = reverse('news:detail', args=(news.id,))
    response = client.get(url)
    assert 'form' not in response.context


def test_comments_order(client, news, commets):
    url = reverse('news:detail', args=(news.id,))
    response = client.get(url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    assert all_comments[0].created < all_comments[1].created
