from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
# Create your views here.

from django.views import View
from django.http.response import HttpResponseBadRequest
import re
from users.models import User
from django.db import DatabaseError
import logging
logger = logging.getLogger('django')
#Register view
class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')
    def post(self, request):
        """
        1. Receive data
        2. Verify data
            2.1 Determine whether the parameters are complete
            2.2 Verify that the username format is correct
            2.3 Verify that the password format is correct
            2.4 Whether the password and confirm password are the same
            2.5 Verify that the verification code is correct
        3. Save registration information
        4. Return the response and jump to the specified page
        :param request:
        :return:
        """
        #1. Receive data
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        image_code = request.POST.get('imgage_code')
        redis_conn = get_redis_connection('default')
        redis_image_code = redis_conn.get('code')
        # print(image_code)
        # 2. Verify data
        #     2.1 Determine whether the parameters are complete
        if not all([username,password,password2,image_code]):
            return HttpResponseBadRequest('Missing required parameters!')
        #     2.2 Verify that the username format is correct
        if not re.match(r'^[0-9A-Za-z]{4,15}$',username):
            return HttpResponseBadRequest('Please enter 4-15 characters, the username is composed of numbers or letters!')
        #     2.3 Verify that the password format is correct
        if not re.match(r'^[0-9A-Za-z]{8,20}$',password):
            return HttpResponseBadRequest('Please enter 8-20 characters, the password is composed of numbers or letters!')
        #     2.4 Whether the password and confirm password are the same
        if password != password2:
            return HttpResponseBadRequest('The two passwords are inconsistent!')
        #     2.5
        # Determine whether the image verification code exists
        if redis_image_code is None:
            return HttpResponseBadRequest('Image verification code has expired!')
        #If the image verification code has not expired, we can delete the image verification code after we obtain it.
        try:
            redis_conn.delete('code')
        except Exception as e:
            logger.error(e)
        #
        #Compare image verification code, pay attention to the problem of capitalization, and redis data is of type bytes
        if redis_image_code.decode().lower() != image_code.lower():
            return HttpResponseBadRequest('Image verification code error!')
        # 3. Save registration information
        #create_user can use systematic methods to encrypt the password
        try:
            user = User.objects.create_user(username=username, password=password)
        except DatabaseError as e:
            logger.error(e)
            return HttpResponseBadRequest('Registration failed!')

        from django.contrib.auth import login
        login(request,user)

        # 4. Return the response and jump to the specified page
        # return HttpResponse('Registration is successful!')
        #redirect
        #reverse: The route corresponding to the view can be obtained through the namespace:name
        response = redirect(reverse('home:index'))
        #setting for info of cookie to show the info of user in homepage
        response.set_cookie('is_login', True)
        response.set_cookie('username',user.username,max_age=7*24*3600)
        return response



from django.http.response import HttpResponseBadRequest
from libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from django.http import HttpResponse
class ImageCodeView(View):
    def get(self, request):
        """
        1. Receive the uuid passed by the front end
        2. Determine whether uuid is obtained
        3. Generate image verification code (image binary and image content) by calling captcha
        4. Save the image content to redis
            uuid is the key, the image content is the value, and we also need to set an actual effect
        5. Return image binary
        :param request:
        :return:
        """
        # 1. Receive the uuid passed by the front end
        uuid = request.GET.get('uuid')
        # 2. Determine whether uuid is obtained
        if uuid is None:
            return HttpResponseBadRequest('No uuid is passed.')
        # 3. Generate image verification code (image binary and image content) by calling captcha
        text, image = captcha.generate_captcha()
        # 4. Save the image content to redis
        redis_conn = get_redis_connection('default')
        #key -> 'code'
        #seconds -> Expired seconds (300s)
        #value -> text
        redis_conn.set(name = 'code',value=text, ex=120)
        # 5. Return image binary
        return HttpResponse(image,content_type='image/jpeg')


class LoginView(View):

    def get(self,request):

        return render(request,'login.html')

    def post(self,request):
        """
            1. Reception of parameters
            2. Verification of parameters
                2.1 Verification of username
                2.2 Verification of password
            3. User authentication login
            4. Keeping status
            5. Remember me or not
            6. Setting for info of cookie to show the homepage
            7. return response
            :param request:
            :return:
        """
        #1. Reception of parameters
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')

        # 2. Verification of parameters
        #     2.1 Verification of username
        if not re.match(r'^[0-9A-Za-z]{4,15}$', username):
            return HttpResponseBadRequest('Username does not conform to the rules!')
        #     2.2 Verification of password
        if not re.match(r'^[0-9A-Za-z]{8,20}$',password):
            return HttpResponseBadRequest('Password does not conform to the rules!')
        # 3. User authentication login
        # Use the systematic authentication method for authentication.
        # If the username and password are correct, return user, else return None
        from django.contrib.auth import authenticate
        # The default of authentication method is aimed to judge the username for the field username
        user = authenticate(username=username,password=password)
        if user is None:
            return HttpResponseBadRequest('Wrong username or password!')

        # 4. Keeping status
        from django.contrib.auth import login
        login(request, user)

        # 5. Remember me or not
        # 6. Setting for info of cookie to show the homepage

        #redirect to the page based on the next parameter
        next_page = request.GET.get('next')
        if next_page:
            response=redirect(next_page)
        else:
            response = redirect(reverse('home:index'))

        if remember != 'on':#did not remember the info of user
            #after the browser is closed
            request.session.set_expiry(0)
            response.set_cookie('is_login', True)
            response.set_cookie('username',user.username,max_age=14*24*3600)
        else:#remembered the info of user
            request.session.set_expiry(None) #default time is 2 weeks
            response.set_cookie('is_login',True, max_age=14*24*3600)
            response.set_cookie('username',user.username,max_age=14*24*3600)

        # 7. return response
        return response


from django.contrib.auth import logout
class LogoutView(View):
    def get(self,request):
        # 1.delete session data
        logout(request)
        # 2.delete some cookie data
        response = redirect(reverse('home:index'))
        response.delete_cookie('is_login')
        # 3.redirect to the homepage
        return response


class ForgetPasswordView(View):

    def get(self,request):
        return render(request,'forget_password.html')

    def post(self,request):
        """
        1. Receive data
        2. Verify data
            2.1 Determine whether the parameters are complete
            2.2 Verify that the username format is correct
            2.3 Verify that the password format is correct
            2.4 Whether the password and confirm password are the same
            2.5 Verify that the verification code is correct
        3. Query user information based on username
        4. If exists this username, reset the password
        5. else create new user
        6. Redirect to login page
        7. Return response
        :param request:
        :return:
        """
        # 1. Receive data
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        image_code = request.POST.get('imgage_code')
        redis_conn = get_redis_connection('default')
        redis_image_code = redis_conn.get('code')
        # 2. Verify data
        #     2.1 Determine whether the parameters are complete
        if not all([username,password,password2,image_code]):
            return HttpResponseBadRequest('Missing required parameters!')
        #     2.2 Verify that the username format is correct
        if not re.match(r'^[0-9A-Za-z]{4,15}$',username):
            return HttpResponseBadRequest('Please enter 4-15 characters, the username is composed of numbers or letters!')
        #     2.3 Verify that the password format is correct
        if not re.match(r'^[0-9A-Za-z]{8,20}$',password):
            return HttpResponseBadRequest('Please enter 8-20 characters, the password is composed of numbers or letters!')
        #     2.4 Whether the password and confirm password are the same
        if password != password2:
            return HttpResponseBadRequest('The two passwords are inconsistent!')
        #     2.5 Verify that the verification code is correct
        # Determine whether the image verification code exists
        if redis_image_code is None:
            return HttpResponseBadRequest('Image verification code has expired!')
        #If the image verification code has not expired, we can delete the image verification code after we obtain it.
        try:
            redis_conn.delete('code')
        except Exception as e:
            logger.error(e)
        #Compare image verification code, pay attention to the problem of capitalization, and redis data is of type bytes
        if redis_image_code.decode().lower() != image_code.lower():
            return HttpResponseBadRequest('Image verification code error!')
        # 3. Query user information based on username
        try:
            user = User.objects.get(username = username)
        except User.DoesNotExist:
            # 5. else create new user
            try:
                User.objects.create_user(username=username,password=password)
            except Exception:
                return HttpResponseBadRequest('The modification failed, please try again later!')
        else:
            # 4. If exists this username, reset the password
            user.set_password(password)
            user.save()
        # 6. Redirect to login page
        response = redirect(reverse('users:login'))
        # 7. Return response
        return response

from django.contrib.auth.mixins import LoginRequiredMixin
#LoginRequiredMixin: If the user is not logged in, the default redirect will be performed
# The default redirect link is: accounts/login/?next=xxx
class UserCenterView(LoginRequiredMixin, View):

    def get(self,request):
        # get the information of user
        user = request.user
        context = {
            'username': user.username,
            #'mobile': user.mobile,
            'avatar': user.avatar.url if user.avatar else None,
            'user_desc': user.user_desc
        }
        return render(request,'center.html',context=context)

    def post(self, request):
        """
        1. Receive parameters
        2. Save parameters
        3. Refresh the current page (redirect operation)
        4. Return response
        :param request:
        :return:
        """
        user = request.user
        #1. Receive parameters
        username = request.POST.get('username',user.username)
        user_desc = request.POST.get('desc',user.user_desc)
        avatar = request.FILES.get('avatar')
        # 2. Save parameters
        try:
            user.username=username
            user.user_desc=user_desc
            if avatar:
                user.avatar=avatar
            user.save()
        except Exception as e:
            logger.error(e)
            return HttpResponseBadRequest('The modification failed, please try again later!')
        # 3. Refresh the current page (redirect operation)
        response = redirect(reverse('users:center'))
        # 4. Return response
        return response