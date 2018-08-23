from django.shortcuts import render, redirect
from django.core.cache import cache
from django.contrib import auth
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_data, get_7_days_hot_data
from blog.models import Blog
from django.urls import reverse


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)
    today_hot_data = get_today_hot_data(blog_content_type)
    yesterday_hot_data = get_yesterday_hot_data(blog_content_type)
    
    # 获取7天热门博客的缓存数据
    hot_data_for_7_days = cache.get('hot_data_for_7_days')
    if hot_data_for_7_days is None:
        hot_data_for_7_days = get_7_days_hot_data(blog_content_type)
        cache.set('hot_data_for_7_days', hot_data_for_7_days, 20)
        print('calc')
    else:
        print('use cache')

    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['today_hot_data'] = today_hot_data
    context['yesterday_hot_data'] = yesterday_hot_data
    context['hot_data_for_7_days'] = hot_data_for_7_days
    return render(request, 'home.html', context)

def login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(request, username=username, password=password)
    # referer = request.META.get('HTTP_REFERER', '/') # 获取请求时网址，登录成功后返回
    referer = request.META.get('HTTP_REFERER', reverse('home')) #别名找到链接
    if user is not None:
        auth.login(request, user)
        return redirect(referer)
    else:
        return render(request, 'error.html', {'message': '用户名或密码错误'})