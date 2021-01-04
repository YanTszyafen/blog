#Perform view routing of users sub-applications
from django.urls import path
from users.views import RegisterView, ImageCodeView
urlpatterns = [
    #The first parameter of path: routing
    #The second parameter of path: view function name
    path('register/',RegisterView.as_view(), name='register'),

    #Image verification code routing
    path('imagecode/', ImageCodeView.as_view(), name='imagecode'),
]