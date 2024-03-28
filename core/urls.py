from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('settings', views.settings, name='settings'),
    path('upload', views.upload, name='upload'),
    path('search', views.search, name='search'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('like-post', views.like_post, name='like-post'),
    path('follow', views.follow, name='follow'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
    path('delete_post/<uuid:post_id>', views.delete_post, name='delete_post'),
    path('add_comment/<uuid:post_id>', views.add_comment, name='add_comment'),
    path('api/comments/<uuid:post_id>/', views.get_comments_api, name='get_comments_api'),
]