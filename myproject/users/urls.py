from django.urls import path
from users.views import records_list, record_detail, register_user, update_user


urlpatterns = [
    path('records/', records_list, name='records_list'),
    path('records/<int:pk>/', record_detail, name='record_detail'),
    path('register/', register_user, name='register'),
    path('users/<int:pk>/', update_user, name='update-user')
]