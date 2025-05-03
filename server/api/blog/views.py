from django.shortcuts import render, redirect
from .models import *
from django.core.paginator import Paginator #(FOR CBV, you dont need it)
# Create your views here.
from django.views.generic import View
from .forms import EmailPostForm, CommentForm, BlogSearch
from django.core.mail import send_mail

class PostListView(View):

    def get(self, request):
        
        blogs = Post.objects.filter(status='PB').order_by('-publish')

        paginator = Paginator(blogs, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)


        context_list = []
        for blog in page_obj:
            temp_dict = {}
            temp_dict['blog'] = blog
            temp_dict['tag'] = blog.tags.values('tag_name')
            context_list.append(temp_dict)
        
        
        return render(request, 'blog/index.html', {
            'blogs':context_list,
            'page_obj':page_obj
        })
    
       
         
        
        
            



def blog_detail(request, slug, year, month, day):
    
    blog = Post.objects.get(slug = slug, publish__year = year, publish__month = month, publish__day = day)
    comments = Comments.objects.filter(post = blog)
    tags = blog.tags.values('tag_name')
   
    # recommendations

    post_to_recommend = []
    for tag in tags:
        print(tag['tag_name'])
        tag_to_search = Tags.objects.get(tag_name = tag['tag_name'])
        
        recommended_post = Post.objects.filter(tags = tag_to_search)

        post_to_recommend += list(recommended_post)     
       


    
    post_to_recommend = [post for post in post_to_recommend if post.id != blog.id]
    

    latest_blogs = [post for post in Post.objects.all() if post.id != blog.id]
    latest_blogs = latest_blogs[:5]


    print(post_to_recommend)
    content = {
        'blog':blog,
        'comments':comments,
        'tags' : tags,
        'recommendations' : post_to_recommend,
        'latest_blogs' : latest_blogs
    }#values() return list of dictionary.

    return render(request, 'blog/blog.html', content)    

def post_share(request, post_id):
    # Receive the post to share

    post = Post.objects.get(id = post_id)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = f"{cd['name']} ({cd['email']}) recommends you read {post.title}"
            
            message = f"Read this cool stuff {post.title} : {post_url}"
            
            send_mail(
                subject = subject,
                message = message,
                from_email = None,
                recipient_list = [cd['to']]
            )
            sent = True
    else:
        form = EmailPostForm()
    
    return render(
        request,
        'blog/share.html',
        {
            'post':post,
            'form':form,
            'sent':sent
        }
    )
        
    
def post_comment(request, post_id):

    post = Post.objects.get(id = post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            print(type(form))
            cd = form.cleaned_data
            print(type(cd))
            comment = Comments(post = post, email = cd['email'], body = cd['body'])
            comment.save()
            return redirect('blog:blog_detail', slug=post.slug, year=post.publish.year, month=post.publish.month, day=post.publish.day)

            

    else:
        form = CommentForm()


    return render(request, 'blog/comments.html',{
        'form' : form
    })