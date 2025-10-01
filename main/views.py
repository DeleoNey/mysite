from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView # for CBV

from .models import Post
from .forms import PostForm
# from django.shortcuts import render, get_object_or_404 # for FBV


'''CBV - Class Based Views'''
class PostListView(ListView):
    model = Post
    template_name = 'main/site/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']


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

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(post.get_absolute_url())
    else:
        form = PostForm()
    return render(request,
                  'main/site/post_form.html',
                  {'form': form, 'title': "Create Post"}
                  )


@login_required
def post_update(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if post.author != request.user:
        return redirect(post.get_absolute_url())

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect(post.get_absolute_url())
    else:
        form = PostForm(instance=post)

    return render(request, 'main/site/post_form.html',
                  {'form': form, 'title': "Update Post"})


@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if post.author != request.user:
        return redirect(post.get_absolute_url())

    if request.method == 'POST':
        post.delete()
        return redirect('main:post-list')
    return render(request, 'main/site/post_confirm_delete.html',
                  {'post': post})