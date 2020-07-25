from django.urls import path
from comment import views

app_name = 'comment'
urlpatterns = [
    #发表评论
    path('post-comment/<int:article_id>/', views.post_comment, name='post_comment'),
    path('comment-delete/<int:article_id>/<int:comment_id>/', views.comment_delete, name='comment_delete'),
    path('post-comment/<int:article_id>/<int:parent_comment_id>', views.post_comment, name='comment_reply'),
]