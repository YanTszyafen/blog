from django.shortcuts import render
from django.views import View
from home.models import ArticleCategory
from django.http.response import HttpResponseNotFound
# Create your views here.
class IndexView(View):
    def get(self,request):
        """
        1. Receive info of category
        2. Get the category id clicked by user
        3. Query category by the category id
        4. Translate data to templates
        :param request:
        :return:
        """
        #1. Receive info of category
        categories = ArticleCategory.objects.all()
        # 2. Get the category id clicked by user
        cat_id = request.GET.get('cat_id',1)
        # 3. Query category by the category id
        try:
            category = ArticleCategory.objects.get(id=cat_id)
        except ArticleCategory.DoesNotExist:
            return HttpResponseNotFound('No such category!')
        # 4. Translate data to templates
        context = {
            'categories':categories,
            'category':category
        }

        return render(request,'index.html',context=context)