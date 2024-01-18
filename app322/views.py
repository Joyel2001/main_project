from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.cache import never_cache
# Create your views here.
#  cumunity forum post section 
# main/views.py
from django.shortcuts import render, redirect
from .models import Post

def post_content(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        
        # Retrieve content from CKEditor
        content = request.POST.get('content')

        # Handling the uploaded image
        image = request.FILES.get('image', None)

        # Create a new Post instance and save it to the database
        new_post = Post(title=title, content=content, image=image)
        new_post.save()

        return redirect('forum_home')  # Change 'forum_home' to the appropriate URL

    return render(request, 'main/forum/newpost.html')





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
# views.py

from django.shortcuts import render, get_object_or_404
from .models import Post, Like, Comment
from django.http import JsonResponse

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    likes = Like.objects.filter(post=post)
    comments = Comment.objects.filter(post=post)

    context = {
        'post': post,
        'likes': likes,
        'comments': comments,
    }

    if request.method == 'POST':
        # Assuming you are sending a POST request when the like button is clicked
        user = request.user  # Get the current user

        # Check if the user has already liked the post
        if not Like.objects.filter(post=post, user=user).exists():
            # If not, create a new Like instance
            like = Like(post=post, user=user)
            like.save()

            # You might want to return a JsonResponse to update the like count in the frontend
            return JsonResponse({'likes_count': post.likes.count()})

        # If the user has already liked the post, you may handle it as needed

    return render(request, 'main/forum/elaborated.html', context)




# post comments
# views.py

from django.shortcuts import render
from .models import Comment

def post_comments(request, post_id):
    post_comments = Comment.objects.filter(post_id=post_id)
    return render(request, 'main/forum/post_comments.html', {'comments': post_comments})



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

