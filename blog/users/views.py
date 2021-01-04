from django.shortcuts import render

# Create your views here.

from django.views import View

#Register view
class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

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
        #   uuid is the key, the image content is the value, and we also need to set an actual effect
        redis_conn = get_redis_connection('default')
        #key -> uuid
        #seconds -> Expired seconds (300s)
        #value -> text
        redis_conn.setex('img:%s'%uuid, 300, text)
        # 5. Return image binary
        return HttpResponse(image,content_type='image/jpeg')