from django.views.generic import DetailView, ListView # for CBV
from .models import Post
# from django.shortcuts import render, get_object_or_404 # for FBV


'''CBV - Class Based Views'''
class PostListView(ListView):
    model = Post
    template_name = 'main/site/post_list.html'
    context_object_name = 'posts'
    # ordering = ['-date_posted']


class PostDetailView(DetailView):
    model = Post
    template_name = 'main/site/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


# '''FBV - Function Based Views'''
# def post_list(request):
#     posts = Post.objects.all()
#     return render(request, 'main/site/post_list.html', {'posts': posts})
#
# def post_detail(request, slug):
#     post = get_object_or_404(Post, slug=slug)
#     return render(request, 'main/site/post_detail.html', {'post': post})