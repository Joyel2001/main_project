from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import views as auth_views
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from .models import Message



def index(request):
    # Retrieve the message from the Message model (assuming you want to display the latest message)
    latest_message = Message.objects.latest('id')
    
    # Retrieve the list of bins from the Bin model
    bins = Bin.objects.all()
    
    return render(request, 'index.html', {'latest_message': latest_message, 'bins': bins})

def resetpass(request):
    return render(request,'resetpass.html')


# def showevents(request):
#     return render(request,'showsevents.html')

def eventbook(request):
    return render(request,'eventbook.html')


# login
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def loginn(request):
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
            return render(request, 'Login.html')
    else:
        return render(request, 'login.html')


# register
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import UserProfile
from django.contrib import messages

def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user_role = request.POST.get('user_role', 'customer')  # Get user role or default to 'customer'

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, "register.html", {'username': username})
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return render(request, "register.html", {'email': email})
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.is_staff = user_role == 'staff'  # Set the user as staff based on the role
            user.save()
            UserProfile.objects.create(user=user, address="")
            messages.success(request, "Registration successful! Please log in.")
            return redirect('loginn')
    else:
        return render(request, "register.html")


def check_email_exists(request):
    email = request.GET.get('email')
    data = {'exists': User.objects.filter(email=email).exists()}
    return JsonResponse(data)
def check_username_exists(request):
    username = request.GET.get('username')
    data = {'exists': User.objects.filter(username=username).exists()}
    return JsonResponse(data)

# logout
def loggout(request):
    print('Logged Out')
    logout(request)
    return redirect('index')


 
    


    


#userprofile
from django.shortcuts import render
from .models import UserProfile

def user_profile_view(request):
    profile = UserProfile.objects.get(user=request.user)
    
    context = {
        'profile': profile,
    }
    return render(request, 'profile/profile.html', context)




#add event
from django.shortcuts import render, redirect
from .models import Event
from django.contrib.auth.decorators import login_required
from django.contrib import messages
@login_required(login_url='loginn')


def addevent(request):
    message = None
    success_message = None

    if request.method == "POST":
        # Get form data
        category = request.POST.get('category')
        name = request.POST.get('name')
        description = request.POST.get('description')
        date = request.POST.get('date')
        time = request.POST.get('time')
        location = request.POST.get('location')
        image = request.FILES.get('image')
        max_participants = request.POST.get('max_participants')  # Get max participants value from the form

        # Generate event_id
        category_prefix = {
            'category1': 'e',
            'category2': 'w',
            'category3': 'x',
            'category4': 'c',
            'category5': 'h',
            # Add more category prefixes as needed
        }.get(category, 'u')
        existing_event_ids = Event.objects.filter(category=category).values_list('event_id', flat=True)
        event_id = f"{category_prefix}{len(existing_event_ids) + 1}"

        # Create the event object and save it
        new_event = Event(
            event_id=event_id,
            user=request.user,
            name=name,
            description=description,
            date=date,
            time=time,
            location=location,
            category=category,
            image=image,
            max_participants=max_participants  # Assign max_participants value to the model field
        )
        new_event.save()

        success_message = 'Event added successfully.'
        messages.success(request, success_message)
        return redirect('event_details_view')

    return render(request, 'event/addevent.html', {'message': message, 'success_message': success_message})











from django.shortcuts import render
from .models import Event  # Import your Event model

from django.shortcuts import render
from .models import Event

def show_events(request, category=None):
    if category:
        # Filter events by category if a category is provided
        events = Event.objects.filter(category=category)
    else:
        # If no category is provided, get all events
        events = Event.objects.all()

    context = {
        'events': events,
    }

    if not events:
        context['no_events_message'] = "No upcoming events at the moment."

    return render(request, 'event/showsevents.html', context)




#event_editing_page

def event_details_view(request):
    events = Event.objects.all()  
    context = {
        'events': events,  
    }
   
    return render(request, 'event/eventdetails.html', context)



# edit_event
from django.shortcuts import render, redirect, get_object_or_404
from .models import Event
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url='loginn')
def edit_event(request, event_id):
    event = get_object_or_404(Event, event_id=event_id, user=request.user)

    if request.method == "POST":
        # Update event information based on the form data
        event.name = request.POST.get('name')
        event.description = request.POST.get('description')
        event.date = request.POST.get('date')
        event.time = request.POST.get('time')
        event.location = request.POST.get('location')

        # Check if a new image was provided and update it if necessary
        new_image = request.FILES.get('image')
        if new_image:
            event.image = new_image

        # Save the updated event
        event.save()
        messages.success(request, 'Event updated successfully.')
        return redirect('event_details_view')

    return render(request, 'event/edit_event.html', {'event': event})



# deleteevent
from django.shortcuts import redirect, get_object_or_404
from .models import Event
from django.contrib.auth.decorators import login_required

@login_required(login_url='loginn')
def delete_event(request, event_id):
    event = get_object_or_404(Event, event_id=event_id)
    event.delete()
    return redirect('event_details_view')






def registration_confirmation(request):
    return render(request, 'event/registration_confirmation.html')


 




# addbinfor home
from django.contrib import messages
from .models import Bin

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError

import logging  # Import the logging module

# Add this at the top of your views.py
logger = logging.getLogger(__name__)

# Inside your add_bin view
from django.db import IntegrityError
from django.contrib import messages

def add_bin(request):
    if request.method == 'POST':
        bin_id = request.POST['bin_id']
        title = request.POST['title']
        size = request.POST['size']
        capacity = request.POST['capacity']
        description = request.POST['description']
        image = request.FILES.get('image')  # Get the uploaded image

        try:
            new_bin = Bin(
                bin_id=bin_id,
                title=title,
                size=size,
                capacity=capacity,
                description=description,
                image=image
            )
            new_bin.save()
            messages.success(request, 'Bin details added successfully.')
        except IntegrityError:
            messages.error(request, 'An error occurred while saving the bin details.')
        
        return redirect('add_bin')  # Redirect to the form after adding

    return render(request, 'bin/addbin.html')



# addbinfor home
from django.contrib import messages
from .models import BinEvent

def add_bin_event(request):
    if request.method == 'POST':
        bin_id = request.POST['bin_id']
        title = request.POST['title']
        size = request.POST['size']
        capacity = request.POST['capacity']
        description = request.POST['description']
        image = request.FILES.get('image')  # Get the uploaded image

        new_bin = BinEvent(
            bin_id=bin_id,
            title=title,
            size=size,
            capacity=capacity,
            description=description,
            image=image
        )
        new_bin.save()

        messages.success(request, 'Bin details added successfully.')
        return redirect('add_bin_event')  # Redirect to the form after adding

    return render(request, 'bin/addbinevent.html')

# showbin
@login_required(login_url='loginn')
def bin_order(request):
    bins = Bin.objects.all()
    context = {'bins': bins}
    return render(request, 'bin/binorder.html', context)



@login_required(login_url='loginn')
def bin_order_event(request):
    binss = BinEvent.objects.all()
    context = {'binss': binss}
    return render(request, 'bin/binorderevent.html', context)

def hello_admin(request):
    return render (request,'admin/dashboard.html')




from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Bin, BinBooking  # Import your Bin and BinBooking models
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Bin
from django.shortcuts import render, HttpResponse, redirect
from .models import Bin, BinBooking
from django.contrib import messages
from django.db.models import Count

@login_required(login_url='loginn')




def orderforhome(request):
    if request.method == 'POST':
        user = request.user  # Get the current logged-in user

        house_number = request.POST['houseNumber']
        landmark = request.POST['landmark']  # Added landmark field
        pin_code = request.POST['pin']
        bin_details = request.POST['binDetails'].split(' - ')
        bin_size = bin_details[0]
        bin_capacity = bin_details[1]
        collection_period = request.POST['collectionPeriod']  # Added collection_period field

        try:
            bin = Bin.objects.get(size=bin_size, capacity=bin_capacity)
        except Bin.DoesNotExist:
            bin = None

        # Get the count of existing bookings for the given bin size
        count = BinBooking.objects.filter(bin_size=bin_size).count()
        
        # Map bin size to its corresponding code
        bin_size_to_code = {
            'Large Size': 'l',
            'Small Size': 's',
            'Medium Size': 'm',
            # Add more mappings as needed
        }
        
        # Generate the booking ID
        code = bin_size_to_code.get(bin_size, 'u')
        booking_id = f"{code}{count + 1}"

        # Create and save the BinBooking instance with the logged-in user
        booking = BinBooking(
            user=user,
            bin=bin,
            house_number=house_number,
            landmark=landmark,  # Added landmark field
            pin_code=pin_code,
            bin_size=bin_size,
            bin_capacity=bin_capacity,
            collection_period=collection_period,  # Added collection_period field
            booking_id=booking_id  # Set the generated booking ID
        )
        booking.save()

        messages.success(request, 'Booking saved successfully.', extra_tags='bin message')

        # Redirect to a different URL or view (you can specify your profile page here)
        return redirect('subscription_plans')

    bins = Bin.objects.all()

    context = {
        'bins': bins,
    }

    return render(request, 'bin/orderforhome.html', context)
 





#bookingeventform for booking event

from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, EventBooking
from django.contrib import messages
import uuid  # Import the uuid library

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Event, EventBooking


from django.contrib.messages import constants as messages

from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, EventBooking
import uuid

def event_booking(request, event_id=None):
    event = None

    if event_id:
        event = get_object_or_404(Event, event_id=event_id)

    if request.method == 'POST':
        attendees = int(request.POST.get('attendees', 0))
        max_participants = event.max_participants

        if event:
            if max_participants <= 0:
                booking_status = 'Booking is closed for this event.'
            else:
                # Check if the user has already booked this event
                existing_booking = EventBooking.objects.filter(event=event, user=request.user).first()
                if existing_booking:
                    booking_status = 'You have already booked this event.'
                else:
                    try:
                        if attendees <= max_participants:
                            booking_id = uuid.uuid4().hex

                            booking = EventBooking.objects.create(
                                booking_id=booking_id,
                                user=request.user,
                                event=event,
                                attendees=attendees
                            )
                            event.max_participants -= attendees
                            event.save()

                            booking_status = 'Booking successfully created.'
                        else:
                            booking_status = 'Number of attendees exceeds maximum participants.'
                    except Exception as e:
                        booking_status = f'An error occurred: {str(e)}'

            return render(request, 'event/bookingeventform.html', {'event': event, 'booking_status': booking_status})

    return render(request, 'event/bookingeventform.html', {'event': event})






# editprofile
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url='loginn')
def edit_profile(request):
    if request.method == "POST":
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')
        new_address = request.POST.get('address')
        new_mobile_number = request.POST.get('mobile_number')  # Add this line

        # Check if the new username and email already exist (excluding the current user)
        if User.objects.filter(username=new_username).exclude(id=request.user.id).exists():
            messages.error(request, "Username already exists")
        elif User.objects.filter(email=new_email).exclude(id=request.user.id).exists():
            messages.error(request, "Email already exists")
        else:
            # Update the user's email, username, and phone number
            user = request.user
            user.username = new_username
            user.email = new_email
            user.save()

            # Update the user's address and phone number in the UserProfile
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            user_profile.address = new_address
            user_profile.mobile_number = new_mobile_number  # Set the mobile number
            user_profile.save()

            messages.success(request, "Profile updated successfully!")
            return redirect('user_profile_view')  # Change 'user_profile' to your actual profile page URL name

    return render(request, "profile/edit_profile.html")
#  profile_password_reset
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth import authenticate, login, get_backends
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth import authenticate, login
from django.contrib.auth import get_backends  # Import get_backends

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

@login_required(login_url='loginn')
def reset_password(request):
    if request.method == "POST":
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user

        # Explicitly specify the authentication backend
        auth_user = authenticate(request, username=user.username, password=old_password, backend='django.contrib.auth.backends.ModelBackend')

        if auth_user is not None:
            if new_password != confirm_password:
                request.session['password_change_status'] = 'error'
            else:
                # Set the new password
                user.set_password(new_password)
                user.save()

                # Update the user's session with the new password
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')

                request.session['password_change_status'] = 'success'

                # Redirect to the user's profile page or any other desired page
                return redirect('user_profile_view')  # Change 'user_profile' to your actual profile page URL name
        else:
            request.session['password_change_status'] = 'incorrect_old_password'

    return render(request, "profile/pass_reset.html")




# user_booked_events_to dispaly
from django.shortcuts import render
from .models import EventBooking  

def user_booked_events(request):
    if not request.user.is_authenticated:
        return render(request, 'auth/login.html')

    booked_events = EventBooking.objects.filter(user=request.user)

    context = {
        'booked_events': booked_events,
    }

    return render(request, 'event/user_booked_events.html', context)


# bin_details
# In your app's views.py

def bin_details(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        bookings = BinBooking.objects.filter(user=user)
    except User.DoesNotExist:
        user = None
        bookings = []

    context = {
        'user': user,
        'bookings': bookings,
    }

    return render(request, 'admin/bin_detailsforhome.html', context)






# admin_list_user
# userlist/views.py
from django.contrib.auth.models import User
from django.shortcuts import render

def user_list(request):
    users = User.objects.all()
    return render(request, 'admin/userlist.html', {'users': users})


#edit_user_details_by admin

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages

def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        # Handle form submission and update user details
        user.username = request.POST['username']
        user.email = request.POST['email']

        # Update user role based on the selected role option
        role = request.POST.get('role')
        if role == 'customer':
            user.is_staff = False
            user.is_superuser = False
        elif role == 'staff':
            user.is_staff = True
            user.is_superuser = False
        elif role == 'superuser':
            user.is_staff = True
            user.is_superuser = True

        # Update user status based on the selected status option
        status = request.POST.get('status')
        if status == 'active':
            user.is_active = True
        elif status == 'inactive':
            user.is_active = False

        user.save()
        
        # Add a success message
        # messages.success(request, 'User details updated successfully.')

        # Redirect back to the user list page
        return redirect('user_list')

    return render(request, 'admin/edituser.html', {'user': user})






# admin_event_details
from django.shortcuts import render
from .models import EventBooking, Event

def booking_list(request):
    event_bookings = EventBooking.objects.all()
    events = Event.objects.all()

    selected_event = request.GET.get('event')  # Get the selected event from the query parameters

    if selected_event:
        event_bookings = event_bookings.filter(event__name=selected_event)

    context = {'event_bookings': event_bookings, 'events': events, 'selected_event': selected_event}
    return render(request, 'admin/event_booking_detail.html', context)



# admin_bin_details
from django.shortcuts import render
from .models import Bin

def bin_list(request):
    bins = Bin.objects.all()
    context = {'bins': bins}
    return render(request, 'admin/bin_list.html', context)


# admin_binbooking_details
from django.shortcuts import render
from .models import BinBooking

def bin_booking_list(request):
    bin_bookings = BinBooking.objects.all()
    context = {'bin_bookings': bin_bookings}
    return render(request, 'admin/bin_booking_list.html', context)



# binststus
# views.py
# views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import BinBooking, BookedBinStatus

def update_bin_status(request, booking_id):
    booking = get_object_or_404(BinBooking, booking_id=booking_id)
    
    if request.method == 'POST':
        # Handle form submission here and update the bin status
        fill_level = request.POST.get('fill_level')
        
        # Check if a status entry for the same bin already exists
        booked_bin_status, created = BookedBinStatus.objects.get_or_create(booking=booking)
        
        # Update the fill_level only if it's provided in the form
        if fill_level is not None:
            booked_bin_status.fill_level = fill_level
            booked_bin_status.save()
        
        # Redirect to a success page or back to the bin details page
        return redirect('bin_details', user_id=booking.user.pk)
    
    context = {
        'booking': booking,
    }
    
    return render(request, 'admin/add_status.html', context)











# notification

from django.shortcuts import render

def bin_collection_notification(request):
    return render(request, 'admin/bin_collection_notification.html')

# views.py



from django.shortcuts import render
from .models import BinBooking, User

def booking_chart(request):
    # Query the database to get the booking data
    booking_data = BinBooking.objects.all()
    event_bookings = EventBooking.objects.all()
    # Process the booking data to create the chart dataset for bookings
    booking_labels = []  # Labels for the x-axis (e.g., booking IDs)
    booking_data_points = []  # Data for the y-axis (e.g., counts)
    event_booking_counts = {}
    for booking in booking_data:
        booking_labels.append(booking.booking_id)
        booking_data_points.append(1)  # You can customize this to represent the data you want to display (e.g., counts)

    # Query the database to get the user data
    users = User.objects.all()

    # Process the user data to create the chart dataset for users
    user_labels = []  # Labels for the x-axis (e.g., user usernames)
    user_data_points = []  # Data for the y-axis (e.g., active/inactive)

    for user in users:
        user_labels.append(user.username)  # You can use any user attribute as the label
        user_data_points.append(1 if user.is_active else 0)  # 1 for active, 0 for inactive
    for event_booking in event_bookings:
        category = event_booking.event.category
        if category in event_booking_counts:
            event_booking_counts[category] += 1
        else:
            event_booking_counts[category] = 1

    # Extract category labels and counts
    event_categories = list(event_booking_counts.keys())
    event_counts = list(event_booking_counts.values())
    context = {
        'booking_labels': booking_labels,
        'booking_data': booking_data_points,
        'user_labels': user_labels,
        'user_data': user_data_points,
        'event_categories': event_categories,
        'event_counts': event_counts,
    }

    return render(request, 'admin/chart.html', context)

# BIN_ADMIN_FOR_EVENT_LIST

from django.shortcuts import render
from .models import BinEvent

def bin_list_forevent(request):
    bin_list = BinEvent.objects.all()
    return render(request, 'admin/bin_list_for_events.html', {'bin_list': bin_list})







from django.shortcuts import render

def notification_page(request):
    return render(request, 'notifications/notification_page.html')



from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import WasteCollection
from .models import BinBooking 

def bin_waste_collection(request, booking_id):
    if request.method == 'POST':
        collection_status = request.POST.get('collection_status')
        
        # Set custom status messages based on the selected option
        if collection_status == 'collected':
            status_message = "We are pleased to inform you that your scheduled waste collection has been successfully completed by EcoRecover."
        else:
            status_message = "We are pleased to inform you that your scheduled waste collection has not been completed by EcoRecover."

        # Create a new WasteCollection object with the custom status message
        booking = BinBooking.objects.get(pk=booking_id)
        waste_collection = WasteCollection.objects.create(
            booking=booking,
            collection_status=status_message,  # Store the custom status message
        )

        # Save the object to the database
        waste_collection.save()

        # You can also pass the status_message to the template if needed
        return redirect('bin_booking_list')  # Redirect to bin_booking_list view

    return render(request, 'bin/bin_waste_collecton.html', {'booking_id': booking_id})


# delete_bin_message 
from django.shortcuts import redirect

def delete_waste_collection(request, waste_collection_id):
    waste_collection = get_object_or_404(WasteCollection, id=waste_collection_id)

    if request.method == 'POST':
        waste_collection.delete()
        return redirect('collection_detail', user_id=waste_collection.booking.user.id)

    return HttpResponse(status=405)




# payment
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.db import transaction  # Import transaction
from .models import Payments  # Import the Payments model

# Authorize Razorpay client with API Keys
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

@login_required  # Add this decorator to require authentication
def homepage(request):
    currency = 'INR'
    amount = 20000  # Rs. 200

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(
        amount=amount, currency=currency, payment_capture='0'))

    # Order ID of the newly created order
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'

    # We need to pass these details to the frontend
    context = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount,
        'currency': currency,
        'callback_url': callback_url,
    }

    return render(request, 'payment/subscription_plans.html', context=context)

@csrf_exempt
@login_required
def paymenthandler(request):

    # Only accept POST requests
    if request.method == "POST":
        try:
            # Get the required parameters from the POST request
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # Verify the payment signature
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = 20000  # Rs. 200
                try:
                    # Capture the payment
                    with transaction.atomic():
                        payment = Payments(
                            user=request.user,  # Get the current user
                            payment_id=payment_id,
                            razorpay_order_id=razorpay_order_id,
                            payment_signature=signature,
                            payment_amount=amount,
                            payment_status=True  # Payment is successful
                        )
                        payment.save()

                    # Render a success page on successful capture of payment
                    return render(request, 'bin/orderforhome.html')
                except:
                    # If there is an error while capturing payment
                    return render(request, 'paymentfail.html')
            else:
                # If signature verification fails
                return render(request, 'paymentfail.html')
        except:
            # If the required parameters are not found in POST data
            return HttpResponseBadRequest()
    else:
        # If other than POST request is made
        return HttpResponseBadRequest()





# waste_colection_message
from django.shortcuts import render
from .models import WasteCollection, BinBooking
from django.contrib.auth.decorators import login_required

@login_required
def collection_detail(request, user_id):
    # Get the WasteCollection records related to the user
    waste_collections = WasteCollection.objects.filter(booking__user__id=user_id)

    return render(request, 'admin/bin_collection_message.html', {'waste_collections': waste_collections})


#pay,ent 
from django.shortcuts import render
import razorpay
from django.conf import settings

# Create a Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def subscription_plans(request):
    # Set the currency and amount
    currency = 'INR'
    amount = 20000  # Rs. 200

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(
        amount=amount,
        currency=currency,
        payment_capture='0'
    ))

    # Get the order ID of the newly created order
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'  # Update this URL as needed

    # Prepare context to pass to the frontend
    context = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount,
        'currency': currency,
        'callback_url': callback_url,
    }

    # Render the template with the context
    return render(request, 'payment/subscription_plans.html', context)


# filling_ststus_for _bin

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import BookedBinStatus

@csrf_exempt
def add_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            booking_id = data.get('booking')
            fill_level = data.get('fill_level')

            # Check if a status entry with the same booking_id already exists
            existing_status = BookedBinStatus.objects.filter(booking_id=booking_id).first()

            if existing_status:
                # If it exists, update the fill_level
                existing_status.fill_level = fill_level
                existing_status.save()
            else:
                # If it doesn't exist, create a new BookedBinStatus instance and save it to the database
                status = BookedBinStatus(booking_id=booking_id, fill_level=fill_level)
                status.save()

            return JsonResponse({"message": "Status added or updated successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)




# bin_booking_for_events
from django.shortcuts import render, redirect
from .models import BinEvent, BinBookingEvent

def save_bin_booking_event(request):
    bins = BinEvent.objects.all()

    if request.method == 'POST':
        event_date_time = request.POST.get('event_date_time')
        event_location = request.POST.get('event_location')
        delivery_time = request.POST.get('delivery_time')
        pickup_time = request.POST.get('pickup_time')
        number_of_bins_needed = request.POST.get('number_of_bins_needed')
        selected_bin_id = request.POST.get('bin')  # Get the selected bin_id

        # Query the selected BinEvent based on the selected_bin_id
        selected_bin_event = BinEvent.objects.get(bin_id=selected_bin_id)

        # Create and save a BinBookingEvent instance with the selected BinEvent
        bin_booking_event = BinBookingEvent(
            event_date_time=event_date_time,
            event_location=event_location,
            delivery_time=delivery_time,
            pickup_time=pickup_time,
            number_of_bins_needed=number_of_bins_needed,
            bin=selected_bin_event,  # Assign the selected BinEvent
            # Add other fields as needed
        )
        bin_booking_event.save()

        return redirect('bin_order_event')  # Redirect to a success page or another appropriate URL

    return render(request, 'bin/bin_booking_event_form.html', {'bins': bins})



# admin/bin_booking_events.html

from django.shortcuts import render
from .models import BinBookingEvent

def display_bin_booking_events(request):
    # Retrieve all BinBookingEvent objects from the database
    bin_booking_events = BinBookingEvent.objects.all()

    # Pass the data to the template for rendering
    context = {'bin_booking_events': bin_booking_events}
    return render(request, 'admin/bin_booking_events.html', context)







from django.shortcuts import render
from .models import BookedBinStatus

def bins_with_low_fill_level(request):
    # Query for bins with fill level less than or equal to 40
    low_fill_bins = BookedBinStatus.objects.filter(fill_level__lte=40)

    # Extract user information for these bins
    bin_details = []
    for status in low_fill_bins:
        bin = status.booking.bin
        user_profile = status.booking.user.userprofile
        bin_details.append({
            'booking_id': status.booking.booking_id,
            'username': user_profile.user.username,
            'address': user_profile.address,
            'mobile_number': user_profile.mobile_number,
            'fill_level': status.fill_level,
        })

    context = {'bin_details': bin_details}
    return render(request, 'admin/bins_low_fill_level.html', context)

