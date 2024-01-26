from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.cache import never_cache
# Create your views here.
#  cumunity forum post section 
# main/views.py
from django.shortcuts import render, redirect
from .models import Post
from django.contrib.auth.decorators import login_required


def post_content(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        
        # Retrieve content from the regular text area
        content = request.POST.get('content')

        # Handling the uploaded image
        image = request.FILES.get('image', None)

        # Create a new Post instance and save it to the database
        new_post = Post(title=title, content=content, image=image, user=request.user)
        new_post.save()

        return redirect('forum_home')  # Change 'forum_home' to the appropriate URL

    return render(request, 'main/forum/newpost.html')







# display post


# main/views.py
# views.py
from django.shortcuts import render
from .models import Post

def all_posts(request):
    # Retrieve all posts and posts shared by the currently logged-in user
    all_posts = Post.objects.all()
    
    if request.user.is_authenticated:
        user_posts = Post.objects.filter(user=request.user)
    else:
        user_posts = None

    return render(request, 'main/forum/post_detail.html', {'all_posts': all_posts, 'user_posts': user_posts})



# elaborated post details
# views.py
# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Comment

from .models import Post, Comment

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post)

    if request.method == 'POST':
        # Assuming you have a form with the id 'addCommentForm'
        content = request.POST.get('content')
        user = request.user  # Assuming you have a user associated with the comment

        # Create a new comment instance
        comment = Comment(post=post, content=content, user=user)
        comment.save()

        # Add a success message
        messages.success(request, 'Your comment has been saved successfully!')

        # Redirect to the same page
        return redirect('post_detail', post_id=post_id)

    context = {
        'post': post,
        'comments': comments,  # Pass the comments to the template
    }

    return render(request, 'main/forum/elaborated.html', context)









# post comments
# views.py

# from django.http import JsonResponse

# def add_comment(request, post_id):
#     post = get_object_or_404(Post, pk=post_id)

#     if request.method == 'POST' and request.is_ajax():
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.user = request.user
#             comment.save()

#             # Assuming you have a template for a single comment (_comment.html)
#             comment_html = render_to_string('_comment.html', {'comment': comment}, request=request)

#             return JsonResponse({
#                 'comment_html': comment_html,
#                 'comments_count': post.comments.count(),
#             })

#     return JsonResponse({'error': 'Invalid request'}, status=400)




from django.shortcuts import render

def login2_page(request):
    return render(request, 'main/login/login2.html')



# company register view 

# views.py
# views.py
from django.shortcuts import render, redirect
from .models import CompanyRegistration

def register_company(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        owners_shareholders_names = request.POST.get('owners_shareholders_names')
        vat_registration_number = request.POST.get('vat_registration_number')
        business_address = request.POST.get('business_address')
        email_address = request.POST.get('email_address')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        business_license_document = request.FILES.get('business_license_document')

        # Check if password and confirm_password match
        if password != confirm_password:
            # Handle password mismatch error
            return render(request, 'register_company.html', {'error': 'Password and Confirm Password do not match'})

        # Check if the email address is already registered
        if CompanyRegistration.objects.filter(email_address=email_address).exists():
            # Handle email address already registered error
            return render(request, 'register_company.html', {'error': 'Email Address is already registered'})

        # Create a new CompanyRegistration instance and save it to the database
        new_company = CompanyRegistration(
            company_name=company_name,
            owners_shareholders_names=owners_shareholders_names,
            vat_registration_number=vat_registration_number,
            business_address=business_address,
            email_address=email_address,
            password=password,
            business_license_document=business_license_document
        )
        new_company.save()

        return redirect('success_page')  # Redirect to a success page

    return render(request, 'main/company/register_company.html')



# seller_registertion
# views.py
from django.shortcuts import render, redirect
from .models import Company

def signup_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        company_name = request.POST.get('company_name')
        gstin = request.POST.get('gstin')
        document = request.FILES.get('document')
        password = request.POST.get('password')

        # Create a new Company instance and save it to the database
        new_company = Company(name=name, email=email, company_name=company_name, gstin=gstin, document=document, password=password)
        new_company.save()

        return render(request, 'main/seller/seller_registeration.html', {'success_message': 'Registration successful!'})

    return render(request, 'main/seller/seller_registeration.html')





# microproject/main/views.py

from django.shortcuts import render
from .models import Post  # Import your Post model or adjust accordingly

def forum_index(request):
    posts = Post.objects.all()  # Adjust this query based on your model structure
    return render(request, 'main/forum/index.html', {'posts': posts})
