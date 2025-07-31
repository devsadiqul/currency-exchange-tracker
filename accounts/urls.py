from django.urls import path
from .views import *


# Register your urls here.
urlpatterns = [
    path('api/login/', LoginView.as_view(), name='login'),
]
