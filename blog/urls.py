from django.urls import path
from . import views

app_name = 'blog'


urlpatterns = [

    path('', views.PostListView.as_view(), name='post_list' ),
    path('detail/<int:pk>', views.PostDetailView.as_view(), name='detail' ),
    path('post/new/', views.PostCreateView.as_view(), name='post_create' ),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_update' ),
    path('post/<int:pk>/remove/', views.PostDeleteView.as_view(), name='post_delete' ),
    path('post/<int:pk>/publish/', views.post_publish, name='post_publish' ),
    path('comment/<int:pk>/approve/', views.comments_approve, name='comment_approve' ),
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment' ),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove' ),
    path('post/drafts/', views.DraftListView.as_view(), name='post_drafts' ),
    path('about', views.AboutView.as_view(), name='about' ),
    
]
