from django.urls import path

from .views import homePageView, ContactPageView, errorPageView, news_detail, \
    LocalPageView, XorijPageView, TexnoPageView, SportPageView, \
    NewsUpdateView, NewsDeleteView, NewsCreateView, admin_page, SearchView


urlpatterns = [
    path('', homePageView, name='home'),
    path('news/contact/', ContactPageView.as_view(), name='contact'),
    path('news/detail/<slug:slug>/', news_detail, name='news_detail'),
    path('news/update/<slug:slug>/', NewsUpdateView.as_view(), name='news_edit'),
    path('news/delete/<slug:slug>/', NewsDeleteView.as_view(), name='news_delete'),
    path('news/create/', NewsCreateView.as_view(), name='news_create'),
    path('news/error/', errorPageView, name='error_404'),
    path('local-news/', LocalPageView.as_view(), name='local_news_page'),
    path('foreign-news/', XorijPageView.as_view(), name='xorij_news_page'),
    path('texnology-news/', TexnoPageView.as_view(), name='texnology_news_page'),
    path('sport-news/', SportPageView.as_view(), name='sport_news_page'),
    path('adminpage/', admin_page, name='admin_page'),
    path('search/results/', SearchView.as_view(), name='search_results'),
]