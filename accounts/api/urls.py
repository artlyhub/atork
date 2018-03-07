from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token

from accounts.api.views import (
    AddFollowerAPIView,
    FollowerAPIView,
    ProfileAPIView,
    ProfileImageAPIView,
    ProfileImageDetailsAPIView,
    ProfileDetailsAPIView,
    UserAPIView,
    UserDetailsAPIView,
    UserProfileImageAPIView,
    UserItemAPIView,
    UserLoginAPIView,
)

accounts_api_urlpatterns = [

    # token maker
    url(r'^get-token/', obtain_auth_token),


    # basic user login, info urls
    url(r'^login/$', UserLoginAPIView.as_view(), name='login'),

    url(r'^user/$', UserAPIView.as_view(), name="user"),

    url(r'^user/(?P<username>[\w.@+-]+)/$',
        UserDetailsAPIView.as_view(), name="user-details"),


    # user profile related urls
    url(r'^profile/$', ProfileAPIView.as_view(), name="profile"),

    url(r'^profile/(?P<pk>[\w.@+-]+)/$',
        ProfileDetailsAPIView.as_view(), name="profile-details"),

    url(r'^profile/(?P<pk>[\w.@+-]+)/followers/$',
        FollowerAPIView.as_view(), name="followers"),

    url(r'^profile/(?P<pk>[\w.@+-]+)/items/$',
        UserItemAPIView.as_view(), name="items"),

    url(r'^profile/(?P<pk>[\w.@+-]+)/profile-images/$',
        UserProfileImageAPIView.as_view(), name="profile-images"),

    url(r'^profile-image/$',
        ProfileImageAPIView.as_view(), name="profile-image"),

    url(r'^profile-image/(?P<pk>\d+)/$',
        ProfileImageDetailsAPIView.as_view(), name="profile-image-details"),


    # follow other users
     url(r'^follow/$', AddFollowerAPIView.as_view(), name='follow'),
]
