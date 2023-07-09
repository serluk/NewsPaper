from django.views.generic import ListView, DetailView,  UpdateView, CreateView, DeleteView
from django.core.paginator import Paginator

from .models import Post, Author
from .forms import PostForm
from .filter import PostFilter


class NewsList(ListView):
    model = Post
    context_object_name = 'news'
    template_name = 'news.html'
    ordering = ['add_time']
    paginate_by = 1


class NewsDetail(DetailView):
    template_name = 'article.html'
    queryset = Post.objects.all()


class PostSearch(ListView):
    model = Post
    template_name = 'post_search.html'
    ordering = ['-add_time']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostCreateView(CreateView):
    template_name = 'post_create.html'
    form_class = PostForm


class UpdatePostView(UpdateView):
    template_name = 'post_create.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'




