from django.urls import path, include
from rest_framework_jwt.views import (
    obtain_jwt_token, 
    refresh_jwt_token, 
    verify_jwt_token,
)

app_name = 'auth'

urlpatterns = [
    path('jwt/', include([
        path('auth-token/', obtain_jwt_token),
        path('refresh-token/', refresh_jwt_token),
        path('verify-token/', verify_jwt_token),
    ])),    
]
