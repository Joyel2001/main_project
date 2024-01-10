from django.shortcuts import render

# Create your views here.
#  cumunity forum post section 
# main/views.py
from django.shortcuts import render, redirect
from .models import Post

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


