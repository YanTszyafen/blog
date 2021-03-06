import os
from django.db import IntegrityError
import urllib
from urllib.parse import urlparse
from urllib.request import urlopen
from PIL import Image
from io import BytesIO
from django.core.files import File
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from home.models import ArticleCategory, Article
from django.http.response import HttpResponseNotFound
from django.core.paginator import Paginator, EmptyPage
from home.thefilmblog import get_article,get_detail,URL
from users.models import User
from django.http.response import HttpResponseBadRequest
import logging
logger = logging.getLogger('django')

def get_blogs():
    categories = ArticleCategory.objects.all()
    for cat_id in range(1,4):
        url = URL[int(cat_id)]
        blogs = get_article(url)
        category = ArticleCategory.objects.get(id=cat_id)
        for blog in blogs:
            detail_url = blog["url"]
            detail = get_detail(detail_url)
            author = User.objects.get(username="thefilmblog")
            title = str(blog.get("title"))
            avatar_url = blog.get("avatar")
            avatar = urlparse(avatar_url).path.split('/')[-1]
            path, header = urllib.request.urlretrieve(avatar_url, "./media/" + avatar)
            content = str(detail[0].get("content"))
            created = detail[0].get("created")
            y = int(created[0:4])
            m = int(created[5:7])
            d = int(created[8:10])
            H = int(created[11:13])
            M = int(created[14:16])
            S = int(created[17:19])
            import datetime
            # 2019-01-29T14:08:00+00:00
            created_ = datetime.datetime(y, m, d, H, M, S)
            try:
                filmblog = Article.objects.get_or_create(
                    avatar=avatar,
                    title=title,
                    category=category,
                    defaults={"author": author, "content": content, "created": created_}
                )
            except:
                IntegrityError

# Create your views here.
class IndexView(View):
    def get(self,request):
        get_blogs()
        #1. Receive info of category
        categories = ArticleCategory.objects.all()
        # 2. Get the category id clicked by user
        cat_id = request.GET.get('cat_id',1)
        # 3. Query category by the category id
        try:
            category = ArticleCategory.objects.get(id=cat_id)
        except ArticleCategory.DoesNotExist:
            return HttpResponseNotFound('No such category!')

        # 4. Get paging parameters
        page_num = request.GET.get('page_num', 1)
        page_size = request.GET.get('page_size', 6)

        # 5. Query article data by the info of paging
        articles = Article.objects.filter(category=category)
        # 6. Create Paginator

        paginator = Paginator(articles,page_size)
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


from home.models import Comment
class DetailView(View):
    def get(self,request):
        #1. Receive article id
        id = request.GET.get('id')
        # 4. Get paging parameters
        page_size = request.GET.get('page_size', 6)
        print(page_size)
        page_num = request.GET.get('page_num', 1)
        print(page_num)
        # 3. Query category data
        categories = ArticleCategory.objects.all()
        # 2. Query article data by id
        try:
            article = Article.objects.get(id=id)
        except Article.DoesNotExist:
            return render(request,'404.html')
        else:
            article.total_views += 1
            article.save()

        # Query the top 10 article data
        hot_articles = Article.objects.order_by('-total_views')[:9]

        # 5. Query comment data by the info of paging
        comments = Comment.objects.filter(article=article).order_by('-created')

        total_count = comments.count()
        # 6. Create Paginator
        paginator = Paginator(comments,page_size)
        # 7. Paging
        try:
            page_comments = paginator.page(page_num)
        except EmptyPage:
            return HttpResponseNotFound('Empty Page!')
        print(paginator.page(1))
        # print(paginator.page(2))
        # print(paginator.page(3))
        total_page = paginator.num_pages

        # 8. Translate data to templates
        context = {
            'categories':categories,
            'category':article.category,
            'article':article,
            'hot_articles':hot_articles,
            'total_count':total_count,
            'comments':page_comments,
            'page_size':page_size,
            'total_page':total_page,
            'page_num':page_num
        }
        return render(request,'detail.html',context=context)

    def post(self,request):
        #1. Receive user info
        user = request.user
        # 2. Check user is logged in or not
        if user and user.is_authenticated:
            # 3. Logged in users can post form data
            #     3.1 Receive comment data
            id = request.POST.get('id')
            content = request.POST.get('content')
            #     3.2 Check the article is exist or not
            try:
                article = Article.objects.get(id=id)
            except Article.DoesNotExist:
                return HttpResponseNotFound('No such article!')
            #     3.3 Save comment data
            Comment.objects.create(
                content=content,
                article=article,
                user=user
            )
            #     3.4 Modify the number of comments on the article
            article.comments_count += 1
            article.save()

            path = reverse('home:detail')+'?id={}'.format(article.id)
            return redirect(path)
        else:
            # 4. Not logged in users will jump to the login page
            return redirect(reverse('users:login'))