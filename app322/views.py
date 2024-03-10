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

@never_cache
@login_required(login_url='loginn')
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
@never_cache
@login_required(login_url='loginn')
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
from django.http import HttpResponseBadRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Comment, Like  # Import the Like model

@never_cache
@login_required(login_url='loginn')
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
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def seller_login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('hello_admin')
        else:
            return redirect('index')

    if request.method == "POST":
        email = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=email, password=password)

        if user is not None:
            login(request, user)
            if user.is_staff or user.is_superuser:
                return redirect('booking_chart')
            else:
                return redirect('index')
        else:
            messages.error(request, "Invalid Login")
            return render(request, 'main\seller\seller_login.html')
    else:
        return render(request, 'main\seller\seller_login.html')





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
@never_cache
@login_required(login_url='company_login')
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

from django.shortcuts import render, redirect, HttpResponse
from .models import CompanyApplyForTender, ApprovedTender, RejectedTender
from django.shortcuts import render, redirect, HttpResponse
from .models import CompanyApplyForTender, ApprovedTender, RejectedTender
from django.shortcuts import render
from .models import CompanyApplyForTender

def display_company_apply_details(request):
    # Fetch all applications
    applications = CompanyApplyForTender.objects.all()
    
    # Render the template with the applications data
    return render(request, 'main/company/tender_application.html', {'applications': applications})




from django.shortcuts import render, redirect, HttpResponse
from .models import CompanyApplyForTender, RejectedTender

def reject_application(request):
    if request.method == 'POST':
        application_id = request.POST.get('application_id')
        rejection_reason = request.POST.get('rejection_reason')
        try:
            application = CompanyApplyForTender.objects.get(id=application_id)
            rejected_tender = RejectedTender.objects.create(registration=application, rejection_reason=rejection_reason)
            # Optionally, you may want to update the application status here.
            application.rejected = True
            application.save()
            return redirect('company_apply_details')  # Redirect to the page showing applications
        except CompanyApplyForTender.DoesNotExist:
            return HttpResponse("Application not found.")
    else:
        return HttpResponse("Invalid request method.")


from django.shortcuts import render, redirect, HttpResponse
from .models import CompanyApplyForTender, ApprovedTender

def approve_application(request):
    if request.method == 'POST':
        application_id = request.POST.get('application_id')
        try:
            application = CompanyApplyForTender.objects.get(id=application_id)
            if not application.approved:
                approved_tender = ApprovedTender.objects.create(registration=application)
                # Optionally, you may want to update the application status here.
                application.approved = True
                application.save()
                return redirect('company_apply_details')  # Redirect to the page showing applications
            else:
                return HttpResponse("Application already approved.")
        except CompanyApplyForTender.DoesNotExist:
            return HttpResponse("Application not found.")
    else:
        return HttpResponse("Invalid request method.")




from django.shortcuts import render
from .models import RejectedTender

def rejected_tender_details(request):
    rejected_tenders = RejectedTender.objects.all()
    return render(request, 'main/company/rejected_tender.html', {'rejected_tenders': rejected_tenders})



# ecomerce_index

from django.shortcuts import render
from django.shortcuts import render
from .models import Product, Subcategory

def ecomerce_index(request):
    products = Product.objects.all()
    subcategories = Subcategory.objects.all()
    return render(request, 'main\ecomerce\ecomerce_index', {'products': products, 'subcategories': subcategories})



# add category and sub 

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Category

def add_category(request):
    if request.method == 'POST':
        # Extract data from the POST request
        name = request.POST['name']
        image = request.FILES['image']
        status = bool(int(request.POST['status']))  # Convert '0' or '1' to boolean
        trending = bool(int(request.POST['trending']))  # Convert '0' or '1' to boolean
        description = request.POST['description']

        # Create a new Category object
        category = Category.objects.create(
            name=name,
            image=image,
            status=status,
            trending=trending,
            description=description
        )

        # Get the ID of the newly created category
        new_category_id = category.id

        # Redirect to a success page or do something else
        return HttpResponse(f'Category added successfully! ID: {new_category_id}')
    else:
        # Retrieve all categories from the database
        categories = Category.objects.all()
        # Render the form template with categories
        return render(request, 'main/products/add_details.html', {'categories': categories})

# add_sub_category
    
from django.shortcuts import render

from django.shortcuts import render
from .models import Category

from django.shortcuts import render, redirect
from .models import Category, Subcategory

def add_subcategory(request):
    if request.method == 'POST':
        category_id = request.POST.get('category')
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        
        category = Category.objects.get(pk=category_id)
        subcategory = Subcategory.objects.create(category=category, name=name, description=description, image=image)
        # Redirect to a success page or homepage
        return redirect('home')  # Change 'home' to the name of your homepage URL pattern
    else:
        categories = Category.objects.all()
        return render(request, 'main/products/sub_category.html', {'categories': categories})






# add_product
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Product, Subcategory

from django.shortcuts import render, redirect
from .models import Product,Subcategory
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from .models import Product

@login_required
def add_product(request):
    if request.method == 'POST':
        subcategory_id = request.POST.get('subcategory')
        name = request.POST.get('name')
        description = request.POST.get('description')
        quantity = request.POST.get('quantity')
        original_price = request.POST.get('original_price')
        selling_price = request.POST.get('selling_price')
        image = request.FILES.get('image')

        # Assuming the user is logged in and you have access to the user object
        user = request.user

        product = Product(subcategory_id=subcategory_id, user=user, name=name, 
                          description=description, quantity=quantity, 
                          original_price=original_price, selling_price=selling_price,
                          product_image=image)
        product.save()

        return render(request, 'main/products/add_product.html', {'message': 'Product added successfully!'})
    elif request.method == 'GET':
        # Fetch subcategories from the database or any other source
        subcategories = Subcategory.objects.all()
          # Or whatever query you use

        products = Product.objects.all()

        # Render the form template with subcategories and products in the context
        return render(request, 'main/products/add_product.html', {'subcategories': subcategories, 'products': products})
    else:
        return HttpResponse('Method not allowed')









# prduct details 
from django.contrib import messages

def product_detail(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return HttpResponseBadRequest("Invalid product ID")

    # Calculate the number of items in the cart
    cart_item_count = 0
    if request.user.is_authenticated:
        cart_item_count = Cart.objects.filter(user=request.user).count()

    response_message = None  # Initialize response message variable

    if request.method == 'POST':
        if request.user.is_authenticated:
            if product.quantity == 0:
                response_message = "Product is out of stock."
            else:
                cart_item, created = Cart.objects.get_or_create(
                    user=request.user,
                    product=product,
                    defaults={'quantity': 1}
                )

                if created:
                    response_message = "Product added to the cart"
                else:
                    response_message = "Product already in the cart"

    return render(request, 'main/ecomerce/product_elaborated.html', {'product': product, 'cart_item_count': cart_item_count, 'response_message': response_message})








# views.py cart irems 

# views.py

from django.shortcuts import render
from .models import Cart

def view_cart(request):
    # Retrieve cart items for the current user
    cart_items = Cart.objects.filter(user=request.user)
    
    # Calculate total number of items and total price
    total_items = sum(item.quantity for item in cart_items)
    total_price = sum(item.product.selling_price * item.quantity for item in cart_items)
    
    return render(request, 'main/ecomerce/cart.html', {'cart_items': cart_items, 'total_items': total_items, 'total_price': total_price})


# views.py

# views.py

from django.http import JsonResponse
from .models import Cart

# views.py

# views.py
# views.py
from django.http import JsonResponse
from .models import Cart

from django.http import JsonResponse
from .models import Cart, Order, OrderItem
from django.db import transaction

@transaction.atomic
def update_quantity(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')

        # Retrieve the cart item
        cart_item = Cart.objects.get(id=item_id)

        # Get the maximum available quantity for the product
        max_available_quantity = cart_item.product.quantity

        # Perform the action (add or remove) if it doesn't exceed the available quantity
        if action == 'add' and cart_item.quantity < max_available_quantity:
            cart_item.quantity += 1
        elif action == 'remove':
            cart_item.quantity -= 1

        # Save the updated quantity
        cart_item.save()

        # Recalculate total items and total price
        cart_items = Cart.objects.filter(user=request.user)
        total_items = sum(item.quantity for item in cart_items)
        total_price = sum(item.product.selling_price * item.quantity for item in cart_items)

        # Prepare response data
        response_data = {
            'quantity': cart_item.quantity,
            'total_items': total_items,
            'total_price': total_price
        }

        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Invalid request method'})

@transaction.atomic
def checkout(request):
    if request.method == 'POST':
        # Retrieve cart items for the current user
        cart_items = Cart.objects.filter(user=request.user)

        # Create an order for the user
        order = Order.objects.create(user=request.user)

        # Create order items for each cart item
        for cart_item in cart_items:
            OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)

        # Clear the cart
        cart_items.delete()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'error': 'Invalid request method'})





# delete item from cart
    # views.py
from django.http import JsonResponse
from .models import Cart

def delete_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        
        # Retrieve the cart item and delete it
        Cart.objects.filter(id=item_id).delete()
        
        return JsonResponse({'success': 'Item deleted successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})




# all_product_details 
from django.shortcuts import render
from django.http import JsonResponse
from .models import Product, Subcategory
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Product
from django.db.models import Q

def all_products(request):
    products = Product.objects.all()
    subcategories = Subcategory.objects.all()
    return render(request, 'main/products/all_products.html', {'products': products, 'subcategories': subcategories})

# views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Wishlist

def add_to_wishlist(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        user = request.user  # Assuming users are authenticated
        wishlist, created = Wishlist.objects.get_or_create(user=user, product=product)
        if created:
            message = 'Product added to wishlist successfully.'
        else:
            message = 'Product already exists in the wishlist.'
        return JsonResponse({'message': message})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
    


# page for wishlist 
    
# views.py
from django.shortcuts import render
from .models import Wishlist

def wishlists(request):
    # Assuming users are authenticated
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'main/products/wishlist.html', {'wishlist_items': wishlist_items})




# seacrch

from django.shortcuts import render
from django.db.models import Q
from .models import Product, Subcategory

def search_products(request):
    query = request.GET.get('search')
    products = Product.objects.filter(name__icontains=query)
    subcategories = Subcategory.objects.all()
    return render(request, 'main/products/all_products.html', {'products': products, 'subcategories': subcategories})



from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Product

def get_products_by_subcategory(request):
    subcategory_id = request.GET.get('subcategory_id')
    if subcategory_id:
        products = Product.objects.filter(subcategory_id=subcategory_id)
    else:
        products = Product.objects.all()
    data = {
        'products': list(products.values())  # Convert queryset to list of dictionaries
    }
    return JsonResponse(data)







# views.py
# authentication/views.py

# from django.http import JsonResponse

# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         # Perform authentication (not implemented here)
#         # You would typically authenticate the user against your database or other authentication backend

#         # Dummy authentication for demonstration
#         if username == 'user' and password == 'password':
#             return JsonResponse({'success': True, 'message': 'Login successful'})
#         else:
#             return JsonResponse({'success': False, 'message': 'Invalid credentials'})

#     return JsonResponse({'success': False, 'message': 'Only POST requests are allowed'})



from django.middleware.csrf import get_token
from django.http import HttpResponse

def csrf_token_view(request):
    token = get_token(request)
    return HttpResponse(token)




from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpRequest
import razorpay
from .models import Cart, Product  # Import the Product model

razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def paymentform1(request: HttpRequest):
    currency = 'INR'
    
    # Get the amount from the GET request and convert it to a float
    amount = float(request.GET.get("amount")) * 100  # Convert to float and then multiply by 100
    
    # Retrieve the cart items for the current user
    cart_items = Cart.objects.filter(user=request.user)
    
    # Calculate total price
    total_price = sum(item.product.selling_price * item.quantity for item in cart_items)
    
    # Deduct quantity from products and create Razorpay order
    for item in cart_items:
        # Retrieve the product
        product = item.product
        # Deduct the quantity from the product
        product.quantity -= item.quantity
        # Save the updated product
        product.save()
    
    # Create Razorpay order
    razorpay_order = razorpay_client.order.create(dict(amount=total_price * 100, currency=currency, payment_capture='0'))
    razorpay_order_id = razorpay_order['id']
    callback_url = '/paymenthandler/'
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = total_price  # Pass total price here
    context['currency'] = currency
    context['callback_url'] = callback_url

    return render(request, 'main/ecomerce/payment.html', context=context)








# from django.http import JsonResponse
from .models import Cart

def delete_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        try:
            cart_item = Cart.objects.get(id=item_id)
            cart_item.delete()
            # Get updated total items and total price
            total_items = Cart.objects.filter(user=request.user).count()
            total_price = sum(item.product.selling_price * item.quantity for item in Cart.objects.filter(user=request.user))
            return JsonResponse({'success': True, 'total_items': total_items, 'total_price': total_price})
        except Cart.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Cart item does not exist'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})




# delattr
    
    # views.py


from django.http import HttpResponseNotAllowed
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt 
def user_loginnn(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True})
        else:
            # Check if user with given email exists
            if email and not User.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'error': 'User with this email does not exist'}, status=400)
            else:
                return JsonResponse({'success': False, 'error': 'Invalid password'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)




# from django.http import JsonResponse
# from app32.models import Feedback
# from django.core.serializers import serialize

# def feedback_list(request):
#     feedback = Feedback.objects.all()
#     data = serialize('json', feedback)
#     return JsonResponse(data, safe=False)




# views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import Cart

def cart_info(request):
    if request.user.is_authenticated:
        cart_item_count = Cart.objects.filter(user=request.user).count()
    else:
        cart_item_count = 0
    return JsonResponse({'cart_item_count': cart_item_count})
