from django.shortcuts import render

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
        # 4. Return the response and jump to the specified page
        #暂时返回注册成功的信息，后期再实现跳转到指定页面
        return HttpResponse('Registration is successful!')



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
