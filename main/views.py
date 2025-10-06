from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView # for CBV
from django.views.generic.edit import FormMixin
from django.urls import reverse
from django.utils.text import slugify
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
# from django.shortcuts import render, get_object_or_404 # for FBV


'''CBV - Class Based Views'''
class PostListView(ListView):
    model = Post
    template_name = 'main/site/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']


    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(author__username__icontains=query) |
                Q(author__first_name__icontains=query) |
                Q(author__last_name__icontains=query)
            ).order_by("-created_at")
        return Post.objects.all().order_by("-created_at")

class PostDetailView(FormMixin, DetailView):
    model = Post
    template_name = 'main/site/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('main:post-detail', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.object.comments.all().order_by("-created_at")
        context['form'] = self.get_form()
        return context


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = self.request.user
            comment.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)



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
            if not post.slug:
                post.slug = slugify(post.title)
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
        messages.error(request, 'Ви не можете редагувати цей пост')
        return redirect(post.get_absolute_url())

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пост оновлено')
            return redirect(post.get_absolute_url())
    else:
        form = PostForm(instance=post)

    return render(request, 'main/site/post_form.html',
                  {'form': form, 'post': post, 'title': "Update Post", 'is_edit': True})


@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if post.author != request.user and not request.user.is_superuser:
        messages.error(request, 'Ви не можете видалити цей пост')
        return redirect(post.get_absolute_url())

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Пост успішно видалено')
        return redirect('main:post-list')

    return render(request, 'main/site/post_confirm_delete.html',
                  {'post': post})

@login_required
def post_like(request, slug):
    post = get_object_or_404(Post, slug=slug)
    user_liked = post.likes.filter(id=request.user.id).exists()

    if user_liked:
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'total_likes': post.total_likes(),
        })
    return redirect(post.get_absolute_url())