from django.shortcuts import render, redirect
from .models import *
from django.core.paginator import Paginator
# Create your views here.
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail

class PostListView(ListView):

    queryset = Post.objects.filter(status = 'PB')
    context_object_name = 'blogs'
    paginate_by = 3
    template_name = 'blog/index.html'


def blog_detail(request, slug, year, month, day):
    post = Post.objects.get(slug = slug, publish__year = year, publish__month = month, publish__day = day)
    print(post)
    comments = Comments.objects.filter(post = post)
    print(comments)
    blog = Post.objects.get(slug = slug, publish__year = year, publish__month = month, publish__day = day)
    print('blog : ',blog)
    
    content = {
        'blog':blog,
        'comments':comments
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