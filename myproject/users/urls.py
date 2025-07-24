from django.urls import path
from users.views import records_list, record_detail, register_user, update_user, auth_by_token, auth_by_password


urlpatterns = [
    path('records/', records_list, name='records_list'),
    path('records/<int:pk>/', record_detail, name='record_detail'),
    path('register/', register_user, name='register'),
    path('users/<int:pk>/', update_user, name='update-user'),
    path('login/', auth_by_token, name='login'),
    path('custom-login/', auth_by_password, name='custom-login'),
]