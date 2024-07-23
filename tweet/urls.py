from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.tweet_list, name='tweet_list'),
    path('register/', views.UserSignupView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('search/', views.UserSearchView.as_view(), name='user_search'),
    path('send_request/<int:to_user_id>/', views.SendFriendRequestView.as_view(), name='send_request'),
    path('accept_request/<int:request_id>/', views.AcceptFriendRequestView.as_view(), name='accept_request'),
    path('reject_request/<int:request_id>/', views.RejectFriendRequestView.as_view(), name='reject_request'),
    path('friends/', views.FriendsListView.as_view(), name='friends_list'),
    path('pending_requests/', views.PendingFriendRequestsView.as_view(), name='pending_requests'),
]