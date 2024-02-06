from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.cache import never_cache
# Create your views here.
#  cumunity forum post section 
# main/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Post
from django.contrib.auth.decorators import login_required

@login_required
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

        # Display success message
        messages.success(request, 'Post created successfully!')

        return redirect('all_posts')  # Change 'forum_home' to the appropriate URL

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
# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Comment, Like  # Import the Like model

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post)
    likes = Like.objects.filter(post=post, user=request.user)

    if request.method == 'POST':
        content = request.POST.get('content')
        user = request.user
        comment = Comment(post=post, content=content, user=user)
        comment.save()
        messages.success(request, 'Your comment has been saved successfully!')
        return redirect('post_detail', post_id=post_id)

    context = {
        'post': post,
        'comments': comments,
        'likes': likes,  # Pass the likes to the template
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
from django.contrib.auth import get_user_model
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

        # Create a new CompanyRegistration instance
        new_company = CompanyRegistration(
            company_name=company_name,
            owners_shareholders_names=owners_shareholders_names,
            vat_registration_number=vat_registration_number,
            business_address=business_address,
            email_address=email_address,
            business_license_document=business_license_document
        )
        new_company.save()

        # Create a new user instance with the company name as the username
        User = get_user_model()
        new_user = User.objects.create_user(username=company_name, email=email_address, password=password)
        
        return redirect('success_page')  # Redirect to a success page

    return render(request, 'main/company/register_company.html')




# seller_registertion
# views.py
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Seller

def signup_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        company_name = request.POST.get('company_name')
        gstin = request.POST.get('gstin')
        document = request.FILES.get('document')
        password = request.POST.get('password')

        # Check if all required fields are present
        if name and email and company_name and gstin and document and password:
            # Create a new User instance and set is_staff to True
            user = User.objects.create_user(username=name, email=email, password=password)
            user.is_staff = True
            user.save()

            # Create a new Seller instance and link it to the user
            new_seller = Seller.objects.create(user=user, company_name=company_name, gstin=gstin, document=document)
            
            return render(request, 'main/seller/seller_registeration.html', {'success_message': 'Registration successful!'})
        else:
            # If any required field is missing, return an error message or redirect to the registration form
            return render(request, 'main/seller/seller_registeration.html', {'error_message': 'Please fill in all required fields'})

    return render(request, 'main/seller/seller_registeration.html')


# seller_login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login

def seller_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user and user.is_staff:
            login(request, user)
            return redirect('index')  # Replace 'seller_dashboard' with the actual URL for the seller dashboard
        else:
            messages.error(request, 'Invalid login credentials or not a seller account.')

    return render(request, 'main/seller/seller_login.html')





# microproject/main/views.py

from django.shortcuts import render
from .models import Post  # Import your Post model or adjust accordingly

def forum_index(request):
    posts = Post.objects.all()  # Adjust this query based on your model structure
    return render(request, 'main/forum/index.html', {'posts': posts})




# company login
# main/views.py
# views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import CompanyRegistration

def company_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user using the provided CompanyRegistration model
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Login the user
            login(request, user)
            return redirect('company_index')  # Redirect to your desired page after login
        else:
            messages.error(request, 'Invalid login credentials')

    return render(request, 'main/company/company_login.html')




# microproject/views.py index page 

from django.shortcuts import render

def company_index(request):
    # Your view logic here
    return render(request, 'main/company/company_index.html')








# tenderapp/views.py
from django.shortcuts import render, redirect
from .models import Tender
from django.http import HttpResponse

def create_tender(request):
    tmessage = None  # Initialize a variable to store the success message

    if request.method == 'POST':
        title = request.POST.get('title')
        organisation_chain = request.POST.get('organisation_chain')
        tender_type = request.POST.get('tender_type')
        tender_category = request.POST.get('tender_category')
        reference_number = request.POST.get('reference_number')
        closing_date = request.POST.get('closing_date')
        bid_opening_date = request.POST.get('bid_opening_date')
        payment_mode = request.POST.get('payment_mode')

        # Create and save Tender object to the database
        tender = Tender(
            title=title,
            organisation_chain=organisation_chain,
            tender_type=tender_type,
            tender_category=tender_category,
            reference_number=reference_number,
            closing_date=closing_date,
            bid_opening_date=bid_opening_date,
            payment_mode=payment_mode,
        )
        tender.save()

        tmessage = "Tender created successfully!"

    return render(request, 'main/company/create_tender.html', {'message': tmessage})


# from django.shortcuts import render
from django.shortcuts import render
from .models import Tender

def tender_list(request):
    tenders = Tender.objects.all()
    return render(request, 'main/company/tender_list.html', {'tenders': tenders})

# tender_elaborated_list
from django.shortcuts import render, get_object_or_404
from .models import Tender, Waste
from django.shortcuts import render, get_object_or_404
from .models import Tender, Waste

def tender_detail(request, tender_id):
    tender = get_object_or_404(Tender, pk=tender_id)
    waste = Waste.objects.filter(tender=tender).first()  # Fetch the waste object related to the tender
    return render(request, 'main/company/full_tender_details.html', {'tender': tender, 'waste': waste})





# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Tender, CompanyApplyForTender

def registration_page(request, tender_id):
    # Ensure that the tender object exists, or return a 404 page if not found
    tender = get_object_or_404(Tender, id=tender_id)

    # Check if the user is already registered for the tender
    is_registered = CompanyApplyForTender.objects.filter(user=request.user, tender=tender).exists()

    if is_registered:
        # If the user is already registered, return a message
        messsage = 'You are already registered for this tender.'
        return render(request, 'main/company/tender_registeration.html', {'tender': tender, 'messsage': messsage})

    if request.method == 'POST':
        amount = request.POST.get('amount')
        license_number = request.POST.get('license_number')
        nature_of_business = request.POST.get('nature_of_business')
        legal_entity_type = request.POST.get('legal_entity_type')

        # Create CompanyApplyForTender instance
        CompanyApplyForTender.objects.create(
            user=request.user,  # Assuming you have a user associated with the request
            tender=tender,
            amount=amount,
            license_number=license_number,
            nature_of_business=nature_of_business,
            legal_entity_type=legal_entity_type,
        )

        # Add a success message to the context
        successs_message = 'Successfully registered to the tender.'
        return render(request, 'main/company/tender_registeration.html', {'tender': tender, 'successs_message': successs_message})

    # Render the registration_page.html for GET requests
    return render(request, 'main/company/tender_registeration.html', {'tender': tender})



# company profile
from django.shortcuts import render

def companys_profile(request):
    # Add logic to fetch company profile data or perform other operations as needed
    context = {
        # Add context data if necessary
    }
    return render(request, 'main/company/companys_profile.html', context)



# tender application views.py
from django.shortcuts import render, redirect
from .models import CompanyApplyForTender

def display_company_apply_details(request):
    if request.method == 'POST':
        application_id = request.POST.get('application_id')
        action = request.POST.get('action')
        rejection_reason = request.POST.get('rejection_reason')

        application = CompanyApplyForTender.objects.get(id=application_id)

        if action == 'approve':
            # Handle approval logic here
            application.approved = True
            application.save()
        elif action == 'reject':
            # Handle rejection logic here
            application.rejected = True
            application.rejection_reason = rejection_reason
            application.save()

    applications = CompanyApplyForTender.objects.all()
    return render(request, 'main/company/tender_application.html', {'applications': applications})

