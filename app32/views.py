from datetime import datetime, timedelta
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
from django.views.decorators.cache import never_cache



def index(request):
    # Retrieve the message from the Message model (assuming you want to display the latest message)
    latest_message = Message.objects.latest('id')
    
    # Retrieve the list of bins from the Bin model
    bins = Bin.objects.all()
    
    return render(request, 'index.html', {'latest_message': latest_message, 'bins': bins})

def resetpass(request):
    return render(request,'resetpass.html')

# profile new page view
def profilee(request):
    return render(request,'profile2.html')


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
from django.http import JsonResponse

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

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import UserProfile

@never_cache
@login_required(login_url='loginn')
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
@never_cache
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
@never_cache
@login_required(login_url='loginn')
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
@never_cache
@login_required(login_url='loginn')
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

@never_cache
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

@never_cache
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
@never_cache
@login_required(login_url='loginn')
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
@never_cache
@login_required(login_url='loginn')
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
@never_cache
@login_required(login_url='loginn')
def bin_order(request):
    bins = Bin.objects.all()
    context = {'bins': bins}
    return render(request, 'bin/binorder.html', context)



@never_cache
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
from .models import SuperCoin
from .models import SuperCoin

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Bin, BinBooking, SuperCoin
from django.contrib.auth.models import User


@never_cache
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

        if bin:
            # Deduct 1 bin from the selected bin
            bin.number_of_bins -= 1
            bin.save()

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

            # Add super coins based on the bin size booked
            super_coins, created = SuperCoin.objects.get_or_create(user=user)
            if created:
                # If a new SuperCoin instance is created, set initial coins based on bin size
                if bin_size == 'Large Size':
                    super_coins.coins = 50
                elif bin_size == 'Medium Size':
                    super_coins.coins = 20
                elif bin_size == 'Small Size':
                    super_coins.coins = 10
                super_coins.save()

            else:
                # If the SuperCoin instance already exists, add coins based on bin size
                if bin_size == 'Large Size':
                    super_coins.coins += 50
                elif bin_size == 'Medium Size':
                    super_coins.coins += 20
                elif bin_size == 'Small Size':
                    super_coins.coins += 10
                super_coins.save()

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
@never_cache
@login_required(login_url='loginn')
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
@never_cache
@login_required(login_url='loginn')
def edit_profile(request):
    if request.method == "POST":
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')
        new_address = request.POST.get('address', '')  # Provide a default value
        new_mobile_number = request.POST.get('mobile_number')

        if User.objects.filter(username=new_username).exclude(id=request.user.id).exists():
            messages.error(request, "Username already exists")
        elif User.objects.filter(email=new_email).exclude(id=request.user.id).exists():
            messages.error(request, "Email already exists")
        else:
            user = request.user
            user.username = new_username
            user.email = new_email
            user.save()

            user_profile, created = UserProfile.objects.get_or_create(user=user)
            user_profile.address = new_address
            user_profile.mobile_number = new_mobile_number
            user_profile.save()

            messages.success(request, "Profile updated successfully!", extra_tags='edit-profile')

            # Redirect to the user's profile view
            return redirect('user_profile_view')

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

@never_cache
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
@never_cache
@login_required(login_url='loginn')
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
@never_cache
@login_required(login_url='loginn')
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
@never_cache
@login_required(login_url='loginn')
def user_list(request):
    users = User.objects.all()
    return render(request, 'admin/userlist.html', {'users': users})


#edit_user_details_by admin

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages
@never_cache
@login_required(login_url='loginn')
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
@never_cache
@login_required(login_url='loginn')
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
@never_cache
@login_required(login_url='loginn')
def bin_list(request):
    bins = Bin.objects.all()
    context = {'bins': bins}
    return render(request, 'admin/bin_list.html', context)


# admin_binbooking_details
from django.shortcuts import render
from .models import BinBooking
@never_cache
@login_required(login_url='loginn')
def bin_booking_list(request):
    bin_bookings = BinBooking.objects.all()
    context = {'bin_bookings': bin_bookings}
    return render(request, 'admin/bin_booking_list.html', context)



# binststus
# views.py
# views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import BinBooking, BookedBinStatus
@never_cache
@login_required(login_url='loginn')
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
@never_cache
@login_required(login_url='loginn')
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
@never_cache
@login_required(login_url='loginn')
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
@never_cache
@login_required(login_url='loginn')
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
@never_cache
@login_required(login_url='loginn')
def delete_waste_collection(request, waste_collection_id):
    waste_collection = get_object_or_404(WasteCollection, id=waste_collection_id)

    if request.method == 'POST':
        waste_collection.delete()
        return redirect('collection_detail', user_id=waste_collection.booking.user.id)

    return HttpResponse(status=405)






    




# waste_colection_message
from django.shortcuts import render
from .models import WasteCollection, BinBooking
from django.contrib.auth.decorators import login_required

@never_cache
@login_required(login_url='loginn')
def collection_detail(request, user_id):
    # Get the WasteCollection records related to the user
    waste_collections = WasteCollection.objects.filter(booking__user__id=user_id)

    return render(request, 'admin/bin_collection_message.html', {'waste_collections': waste_collections})


#pay,ent 
from django.shortcuts import render, redirect  # Import the redirect function
from django.conf import settings
from django.urls import reverse

# Create a Razorpay client

def subscription_plans(request):
    
      

    # Render the template with the context
    return render(request, 'payment/subscription_plans.html')



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
from django.urls import reverse
from .models import BinEvent, BinBookingEvent
from django.utils import timezone
from django.http import HttpResponse
@never_cache
@login_required(login_url='loginn')
def save_bin_booking_event(request):
    bins = BinEvent.objects.all()

    if request.method == 'POST':
        event_date_time = request.POST.get('event_date_time')
        event_location = request.POST.get('event_location')
        delivery_time = request.POST.get('delivery_time')
        number_of_bins_needed = int(request.POST.get('number_of_bins_needed'))
        selected_bin_id = request.POST.get('bin')

        selected_bin_event = BinEvent.objects.get(bin_id=selected_bin_id)

        if selected_bin_event.number_of_bins >= number_of_bins_needed:
            pickup_time = request.POST.get('pickup_time')
            
            if not pickup_time:
                # If pickup_time is not provided, set it to the current time
                pickup_time = timezone.now()
            
            bin_booking_event = BinBookingEvent(
                bin=selected_bin_event,
                event_date_time=event_date_time,
                event_location=event_location,
                delivery_time=delivery_time,
                pickup_time=pickup_time,
                number_of_bins_needed=number_of_bins_needed,
            )
            bin_booking_event.save()

            selected_bin_event.number_of_bins -= number_of_bins_needed
            selected_bin_event.save()

            # Calculate the amount based on the bin size
            if selected_bin_event.size == 'small':
                amount = 160
            elif selected_bin_event.size == 'medium':
                amount = 180
            elif selected_bin_event.size == 'large':
                amount = 200
            else:
                amount = 0  # Handle other cases as needed

            # Make sure the amount is at least 100 (1 INR)
            if amount < 100:
                amount = 100  # Set it to 1 INR

            # Redirect to the paymentform view with the amount as a query parameter
            return redirect(reverse('paymentform') + f'?amount={amount}')

        else:
            error_message = "Not enough bins available for booking."
            return render(request, 'bin/error_page.html', {'error_message': error_message})

    return render(request, 'bin/bin_booking_event_form.html', {'bins': bins})










# admin/bin_booking_events.html

from django.shortcuts import render
from .models import BinBookingEvent
@never_cache
@login_required(login_url='loginn')
def display_bin_booking_events(request):
    # Retrieve all BinBookingEvent objects from the database
    bin_booking_events = BinBookingEvent.objects.all()

    # Pass the data to the template for rendering
    context = {'bin_booking_events': bin_booking_events}
    return render(request, 'admin/bin_booking_events.html', context)







from django.shortcuts import render
from django.db.models import Q
from .models import BookedBinStatus
@never_cache
@login_required(login_url='loginn')
def bins_with_low_fill_level(request):
    # Query for bins with fill level less than or equal to 20 or fill level is null
    low_fill_bins = BookedBinStatus.objects.filter(Q(fill_level__lte=0) | Q(fill_level__isnull=True))

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




# seminar


from django.shortcuts import render

def open_url(request):
    return render(request, 'admin\seminar\seminar.html')




# feedback
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from .models import Feedback  # Import the Feedback model

@never_cache
@login_required(login_url='loginn')
def submit_feedback(request, user_id):
    # Use user_id to identify the user, for example:
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        # Handle the case where the user does not exist
        return HttpResponseNotFound("User not found")
    
    if request.method == 'POST':
        star_rating = request.POST.get('star_rating')
        message = request.POST.get('message')
        
        # Create and save the Feedback instance
        feedback_instance = Feedback(user=user, star_rating=star_rating, message=message)
        feedback_instance.save()
        messages.info(request, f'Added to Cart')
        
        # Redirect to a thank you page or display a success message
        return redirect('index')
    
    return render(request, 'feedback/feedback.html', {'user': user})





# payment sucess
from django.shortcuts import render
@never_cache
@login_required(login_url='loginn')
def payment_success(request):
    return render(request, 'paymentsuccess.html')



#payment for home bin booking 
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
import razorpay

razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def paymentform(request: HttpRequest):
    currency = 'INR'
    amount = int(request.GET.get("amount")) * 100  # Rs. 200

    razorpay_order = razorpay_client.order.create(dict(amount=amount, currency=currency, payment_capture='0'))
    razorpay_order_id = razorpay_order['id']
    callback_url = '/paymenthandler/'
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount / 100
    context['currency'] = currency
    context['callback_url'] = callback_url

    return render(request, 'payment/payment_form.html', context=context)

from django.conf import settings
@csrf_exempt
@login_required  
def paymenthandler(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            client = razorpay.Client(auth=('rzp_test_Ul5agYuKOPazq3', 'lhozVEM1VKK2RmUmLIJg0i9C'))
            payment = client.payment.fetch(payment_id)
            payment_amount = payment['amount']
            result = razorpay_client.utility.verify_payment_signature(params_dict)

            if result is not None:
                authenticated_user = request.user
                user_profile = UserProfile.objects.get(user=authenticated_user)
                
            
                amount = 200 if payment_amount == 20000 else (400 if payment_amount == 40000 else 60000)

                # Set the subscription duration based on the plan
                if amount == 200:
                    user_profile.subscription_duration = 1  # 1 month
                elif amount == 400:
                    user_profile.subscription_duration = 6  # 6 months
                elif amount == 60000:
                    user_profile.subscription_duration = 12  # 12 months



                # Calculate the subscription expiration date
                current_date = datetime.now().date()
                expiration_date = current_date + timedelta(days=30 * user_profile.subscription_duration)  # Assuming 30 days per month
                user_profile.subscription_expiration = expiration_date

                # Set the user as subscribed
                user_profile.subscribed = True
                user_profile.save()

                username = authenticated_user.username

                # Your code for sending a successful subscription email
                

                return render(request, 'paymentsuccess.html')
            else:
                return render(request, 'home.html')
        except Exception as e:
            return render(request, 'home.html', {'error_message': str(e)})
    else:
        return render(request, 'paymentsuccess.html')
    
# payemnt to db

       
    




# feedback_list_html
# views.py

from django.shortcuts import render
from .models import Feedback
@never_cache
@login_required(login_url='loginn')
def feedback_lists(request):
    feedback_entries = Feedback.objects.all()  # Retrieve all feedback entries
    return render(request, 'admin/feedback_display/feedback_list.html', {'feedback_entries': feedback_entries})





# event_ bin _boooking _ payment _details
@never_cache
@login_required(login_url='loginn')
def payment_details(request, amount_to_pay):
    return render(request, 'payment_details.html', {'amount_to_pay': amount_to_pay})




# edit bin details
from django.shortcuts import render, get_object_or_404, redirect
from .models import BinBooking
@never_cache
@login_required(login_url='loginn')
def edit_booking_details(request, booking_id):
    booking = get_object_or_404(BinBooking, booking_id=booking_id)
    
    if request.method == 'POST':
        # Handle form submission and update the details in the database
        collection_day = request.POST.get('collection_day')
        house_number = request.POST.get('house_number')
        landmark = request.POST.get('landmark')
        
        # Update the booking details in the database
        booking.collection_period = collection_day
        booking.house_number = house_number
        booking.landmark = landmark
        booking.save()
        
        # Redirect to a success page or back to the bin details page
        return redirect('bin_details', user_id=booking.user.pk)
    
    context = {
        'booking': booking,
    }
    
    return render(request, 'admin\edit_booking_details.html', context)


from django.shortcuts import render

# def user_profile_view(request):
#     return render(request, 'profile2.html')



# waste_classifier/views.py

from django.shortcuts import render

def contact_info(request):
    return render(request, 'contact.html')



# subscrtion_details 
from django.shortcuts import render
from .models import UserProfile  # Import your UserProfile model
@never_cache
@login_required(login_url='loginn')
def user_sub_details(request):
    user_profiles = UserProfile.objects.all()  # Retrieve all user profiles
    return render(request, 'admin\subscription.html', {'user_profiles': user_profiles})





# views.py

from django.http import JsonResponse
from .models import Feedback
from .serializers import FeedbackSerializer

def feedback_list(request):
    feedback = Feedback.objects.all()
    serializer = FeedbackSerializer(feedback, many=True)
    return JsonResponse(serializer.data, safe=False)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile
from .serializers import UserProfileSerializer

class UserProfileAPIView(APIView):
    def get(self, request):
        profiles = UserProfile.objects.all()
        serializer = UserProfileSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    



# views.py
from rest_framework import generics
from .models import EventBooking
from .serializers import EventBookingSerializer

class EventBookingList(generics.ListAPIView):
    queryset = EventBooking.objects.all()
    serializer_class = EventBookingSerializer


# views.py

# views.py

from django.shortcuts import render
from django.http import JsonResponse
from .models import UserProfile

def all_users_detail(request):
    # Retrieve all user profiles
    profiles = UserProfile.objects.all()
    # Create a list to store user details
    users_data = []
    # Iterate through each user profile and construct a dictionary with user details
    for profile in profiles:
        user_data = {
            'username': profile.user.username,
            'email': profile.user.email,
            'address': profile.address,
            'mobile_number': profile.mobile_number,
            'subscribed': profile.subscribed,
            'subscription_expiration': profile.subscription_expiration,
            'subscription_duration': profile.subscription_duration
        }
        users_data.append(user_data)
    # Return the list of user data as JSON response
    return JsonResponse(users_data, safe=False)





# views.py

from django.shortcuts import render
from django.http import JsonResponse
from .models import EventBooking

def event_booking_detail(request):
    bookings = EventBooking.objects.all()
    booking_data = []
    for booking in bookings:
        booking_data.append({
            'booking_id': booking.booking_id,
            'user': booking.user.username,
            'event': booking.event.name,
            'attendees': booking.attendees
        })
    return JsonResponse(booking_data, safe=False)



# views.py

from django.shortcuts import render
from django.http import JsonResponse
from .models import UserProfile

def user_profiles(request):
    profiles = UserProfile.objects.all()
    profile_data = []
    for profile in profiles:
        profile_data.append({
            'username': profile.user.username,
            'subscribed': profile.subscribed,
            'subscription_expiration': profile.subscription_expiration,
            'subscription_duration': profile.subscription_duration
        })
    return JsonResponse(profile_data, safe=False)




# views.py

# views.py

from django.shortcuts import render
from django.http import JsonResponse
from .models import BinBooking

def bin_booking_detail(request):
    bookings = BinBooking.objects.all()
    booking_data = []
    for booking in bookings:
        booking_data.append({
            'user': booking.user.username,
            'bin': booking.bin.bin_name,  # Modify this line
            'house_number': booking.house_number,
            'landmark': booking.landmark,
            'pin_code': booking.pin_code,
            'bin_size': booking.bin_size,
            'bin_capacity': booking.bin_capacity,
            'collection_period': booking.collection_period,
            'booking_id': booking.booking_id
        })
    return JsonResponse(booking_data, safe=False)


