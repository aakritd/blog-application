from django.shortcuts import render
from .models import *
# Create your views here.


def display_blogs(request):

    blogs = Post.objects.filter(status='PB')
    # print(blogs[0])
    # print(blogs)
    # print(blogs[0]['id'])
    content = {'blogs':blogs}#values() return list of dictionary.
    return render(request, 'blog/index.html', content)


def blog_detail(request, id):

    blog = Post.objects.get(id=id)
    # print(blogs[0])
    # print(blogs)
    # print(blogs[0]['id'])
    content = {'blog':blog}#values() return list of dictionary.
    return render(request, 'blog/blog.html', content)