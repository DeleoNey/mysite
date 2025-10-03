from django.urls import path
from .views import PostListView, PostDetailView, post_create, post_update, post_delete

app_name = 'main'

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('post/new/', post_create, name='post-create'),
    path('post/<slug:slug>/update/', post_update, name='post-update'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<slug:slug>/delete/', post_delete, name='post-delete'),

]