from django.shortcuts import render
from django.views import View
from home.models import ArticleCategory, Article
from django.http.response import HttpResponseNotFound
# Create your views here.
class IndexView(View):
    def get(self,request):
        """
        1. Receive info of category
        2. Get the category id clicked by user
        3. Query category by the category id
        4. Get paging parameters
        5. Query article data by the info of paging
        6. Create Paginator
        7. Paging
        8. Translate data to templates
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
        #4. Get paging parameters
        page_num = request.GET.get('page_num',1)
        page_size = request.GET.get('page_size',6)
        # 5. Query article data by the info of paging
        articles = Article.objects.filter(category=category)
        # 6. Create Paginator
        from django.core.paginator import Paginator, EmptyPage
        paginator = Paginator(articles,per_page=page_size)
        # 7. Paging
        try:
            page_articles = paginator.page(page_num)
        except EmptyPage:
            return HttpResponseNotFound('Empty Page!')
        #total page
        total_page = paginator.num_pages
        # 8. Translate data to templates
        context = {
            'categories':categories,
            'category':category,
            'articles':page_articles,
            'page_size':page_size,
            'total_page':total_page,
            'page_num':page_num
        }

        return render(request,'index.html',context=context)


class DetailView(View):
    def get(self,request):
        """
        1. Receive article id
        2. Query article data by id
        3. Query category data
        4. Translate data to templates
        :param request:
        :return:
        """
        #1. Receive article id
        id = request.GET.get('id')
        # 2. Query article data by id
        try:
            article = Article.objects.get(id=id)
        except Article.DoesNotExist:
            return render(request,'404.html')
        # 3. Query category data
        categories = ArticleCategory.objects.all()
        # 4. Translate data to templates
        context = {
            'categories':categories,
            'category':article.category,
            'article':article
        }
        return render(request,'detail.html',context=context)