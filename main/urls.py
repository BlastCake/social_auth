from django.urls import path
from .views import SocialAuth, UserPage, log_out

urlpatterns = [
    path('', SocialAuth.as_view(), name='authorize_url'),
    path('user_detail/', UserPage.as_view(), name='user_detail_url'),
    path('logout/', log_out, name='log_out_url')
]