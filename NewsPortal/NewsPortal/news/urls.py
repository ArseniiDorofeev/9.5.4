from allauth.account.views import SignupView
from allauth.socialaccount.providers.oauth.urls import default_urlpatterns
from allauth.socialaccount.providers.oauth2.views import (OAuth2View, OAuth2CallbackView)
from django.contrib.auth import views as auth_views
from django.urls import path, include

from . import views

urlpatterns = [
    path('news/', views.news_list, name='news_list'),
    path('news/<int:news_id>/', views.news_detail, name='news_detail'),
    path('news/search/', views.news_search, name='news_search'),
    path('news/create/', views.NewsCreateView.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', views.NewsUpdateView.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', views.NewsDeleteView.as_view(), name='news_delete'),

    path('articles/create/', views.ArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', views.ArticleUpdateView.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', views.ArticleDeleteView.as_view(), name='article_delete'),
    path('accounts/', include('allauth.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/signup/', SignupView.as_view(), name='account_signup'),
    path('accounts/google/login/', OAuth2View.as_view(), name='google_login'),
    path('accounts/google/login/callback/', OAuth2CallbackView.as_view(), name='google_callback'),
    path('request_author_status/', views.request_author_status, name='request_author_status'),
    path('author_requests/', views.author_request_list, name='author_request_list'),
    path('author_request/approve/<int:request_id>/', views.approve_author_request, name='approve_author_request'),
    path('author_request/reject/<int:request_id>/', views.reject_author_request, name='reject_author_request'),
path('subscribe/<int:category_id>/', views.subscribe_to_category, name='subscribe_to_category'),
    path('unsubscribe/<int:category_id>/', views.unsubscribe_from_category, name='unsubscribe_from_category'),
]
urlpatterns += default_urlpatterns('allauth.socialaccount.providers.oauth2.views')