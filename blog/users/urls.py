#Perform view routing of users sub-applications
from django.urls import path
from users.views import RegisterView, ImageCodeView, LoginView, LogoutView, ForgetPasswordView, UserCenterView
urlpatterns = [
    #The first parameter of path: routing
    #The second parameter of path: view function name
    path('register/',RegisterView.as_view(), name='register'),

    #Image verification code routing
    path('imagecode/', ImageCodeView.as_view(), name='imagecode'),

    path('login/',LoginView.as_view(),name='login'),

    path('logout/', LogoutView.as_view(), name='logout'),

    path('forgetpassword/', ForgetPasswordView.as_view(), name='forgetpassword'),

    path('center/', UserCenterView.as_view(), name='center'),
]