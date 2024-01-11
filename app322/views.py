from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.cache import never_cache
# Create your views here.
#  cumunity forum post section 
# main/views.py
from django.shortcuts import render, redirect
from .models import Post
# @login_required(login_url='loginn')
def post_content(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        # Handling the uploaded image
        image = request.FILES.get('image', None)

        # Create a new Post instance and save it to the database
        new_post = Post(title=title, content=content, image=image)
        new_post.save()

        return redirect('forum_home')  # Change 'forum_home' to the appropriate URL

    return render(request, 'main/forum/newpost.html')
  # Render the form page for GET requests



# display post


# main/views.py
# views.py
from django.shortcuts import render
from .models import Post

def all_posts(request):
    posts = Post.objects.all()
    return render(request, 'main/forum/post_detail.html', {'posts': posts})


# elaborated post details
# views.py
from django.shortcuts import render, get_object_or_404
from .models import Post

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'main/forum/elaborated.html', {'post': post})




