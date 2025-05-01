from . import views
from django.urls import path


app_name = 'blog'

urlpatterns = [
    path("", views.PostListView.as_view(), name='display_blogs'),
    path("blog/<int:year>/<int:month>/<int:day>/<slug:slug>", views.blog_detail, name='blog_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment' )
]