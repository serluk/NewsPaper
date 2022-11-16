from django.views.generic import ListView, DetailView
from .models import Post


class NewsList(ListView):
    model = Post
    context_object_name = 'news'
    template_name = 'news.html'


class NewsDetail(DetailView):
    model = Post
    template_name = 'article.html'
    context_object_name = 'article'
