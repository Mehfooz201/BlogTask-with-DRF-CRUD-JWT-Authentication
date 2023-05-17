
from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import BlogPostList, BlogPostDetail, RegistrationAPIView


urlpatterns = [

    path('auth/register/', RegistrationAPIView.as_view(), name='signup'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/refresh-token/', TokenRefreshView.as_view(), name='refreshtoken'),
    
    path('api/blogposts/', BlogPostList.as_view(), name='blogpost_list'),
    path('api/blogposts/<int:pk>/', BlogPostDetail.as_view(), name='blogpost_detail'),


    path('', views.home),
    path('search/', views.searchBar, name='search'),


    path('signup/', views.user_signup, name='signup'),
    path('signin/', views.user_login, name='signin'),
    path('logout/', views.user_logout, name='logout'),



    path('addpost/', views.addPost, name='addpost'),
    path('singlepost/<int:id>/', views.singlePost, name='singlepost'),
    path('updatepost/<int:id>/', views.updatePost, name='updatepost'),
    path('deletepost/<int:id>/', views.deletePost, name='deletepost'),

]
