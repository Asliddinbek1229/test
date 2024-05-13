from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Category, News
from .forms import ContactUsForm, NewsCreatedForm, CommentForm
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView, DetailView
from config.custom_permissions import OnlyLoggedSuperUser


# Create your views here.


@login_required(login_url='login')
def homePageView(request):
    categories = Category.objects.all()
    news_list = News.published.all().order_by('-publish_time')[:5]
    mahalliy_news = News.published.filter(category__name="MAHALLIY").order_by('-publish_time')[:5]
    xorij_news = News.published.filter(category__name="XORIJ").order_by('-publish_time')[:5]
    sport_news = News.published.filter(category__name="SPORT").order_by('-publish_time')[:5]
    texnologiya_news = News.published.filter(category__name="TEXNOLOGIYA").order_by('-publish_time')[:5]
    context = {
        'categories': categories,
        'news_list': news_list,
        'mahalliy_news': mahalliy_news,
        'xorij_news': xorij_news,
        'sport_news': sport_news,
        'texnologiya_news': texnologiya_news
    }
    return render(request, 'news/home.html', context)


# class HomePageView(ListView):
#     model = News
#     template_name = 'news/home.html'
#     context_object_name = 'news'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['categories'] = Category.objects.all()
#         context['news_list'] = News.published.all().order_by('-publish_time')
#         context['local_one'] = News.published.filter(category__name="MAHALLIY").order_by('-publish_time')[0]
#         context['local_news'] = News.published.all().filter(category__name="MAHALLIY").order_by('-publish_time')[1:6]
#         return context


def news_detail(request, slug):
    news = get_object_or_404(News, slug=slug)
    comments = news.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.news = news
            new_comment.save()
            comment_form = CommentForm()

    else:
        comment_form = CommentForm()
    context = {
        'news': news,
        'comments': comments,
        'news_comment': new_comment,
        'comment_form': comment_form
    }
    return render(request, 'news/news_detail.html', context)

# def contactPageView(request):
#     form = ContactUsForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         form.save()
#         return HttpResponse("<h1>Biz bilan bog'langaningiz uchun rahmat</h1>")
#     context = {
#         'form': form
#     }
#     return render(request, 'news/contact.html', context=context)


class ContactPageView(TemplateView):
    template_name = 'news/contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactUsForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = ContactUsForm(request.POST)
        if request.method == "POST" and form.is_valid():
            form.save()
            return HttpResponse("<h1>Biz bilan bog'langaningiz uchun rahmat</h1>")

        context = {
            'form': form
        }
        return render(request, self.template_name, context)


class LocalPageView(ListView):
    model = News
    template_name = 'news_page/local.html'
    context_object_name = 'mahalliy_yangiliklar'

    def get_queryset(self):
        news = News.objects.all().filter(category__name="MAHALLIY")
        return news


class XorijPageView(ListView):
    model = News
    template_name = 'news_page/xorij.html'
    context_object_name = 'xorij_yangiliklar'

    def get_queryset(self):
        news = News.objects.all().filter(category__name="XORIJ")
        return news


class TexnoPageView(ListView):
    model = News
    template_name = 'news_page/texnology.html'
    context_object_name = 'texnologiya_yangiliklar'

    def get_queryset(self):
        news = News.objects.all().filter(category__name="TEXNOLOGIYA")
        return news


class SportPageView(ListView):
    model = News
    template_name = 'news_page/sport.html'
    context_object_name = 'sport_yangiliklar'

    def get_queryset(self):
        news = News.objects.all().filter(category__name="SPORT")
        return news


class NewsUpdateView(OnlyLoggedSuperUser ,UpdateView):
    model = News
    fields = (
        'title',
        'body',
        'image',
        'category',
        'status',
    )
    template_name = 'CRUD/news_update.html'


class NewsDeleteView(OnlyLoggedSuperUser ,DeleteView):
    model = News
    template_name = 'CRUD/news_delete.html'
    success_url = reverse_lazy('home')


class NewsCreateView(LoginRequiredMixin, UserPassesTestMixin ,CreateView):
    model = News
    form_class = NewsCreatedForm
    template_name = 'CRUD/news_create.html'
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_superuser


def errorPageView(request):
    return render(request, 'news/404.html', context=None)


@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def admin_page(request):
    admin_user = User.objects.filter(is_superuser=True)

    context = {
        'admin_user': admin_user
    }
    return render(request, 'pages/admin_page.html', context)


@login_required(login_url='login')
def comment_view(request, slug):
    comment = News.objects.get(slug=slug)
    if request.method == 'POST':
        pass


class SearchView(ListView):
    model = News
    template_name = 'news/search_results.html'
    context_object_name = 'barcha_yangiliklar'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )

