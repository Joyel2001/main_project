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



def index(request):

    return render(request,'index.html')

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
                return redirect('hello_admin')
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
    return render(request, 'profile.html', context)




#add event
from django.shortcuts import render, redirect
from .models import Event
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required


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

@login_required
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

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, event_id=event_id, user=request.user)
    event.delete()
    return redirect('event_details_view')





def registration_confirmation(request):
    return render(request, 'event/registration_confirmation.html')


 




# addbinfor home
from django.contrib import messages
from .models import Bin

def add_bin(request):
    if request.method == 'POST':
        bin_id = request.POST['bin_id']
        title = request.POST['title']
        size = request.POST['size']
        capacity = request.POST['capacity']
        description = request.POST['description']
        image = request.FILES.get('image')  # Get the uploaded image

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
def bin_order(request):
    bins = Bin.objects.all()
    context = {'bins': bins}
    return render(request, 'bin/binorder.html', context)

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

@login_required




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
        booking_id = f"{bin_size_to_code.get(bin_size, 'u')}{count + 1}"

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
        return redirect('bin_order')

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

def event_booking(request, event_id=None):
    event = None

    if event_id:
        # If 'event_id' is provided, fetch the event using the correct field name
        event = get_object_or_404(Event, event_id=event_id)

    if request.method == 'POST':
        # Handle the form submission here
        attendees = int(request.POST.get('attendees', 0))  # Convert input to an integer
        max_participants = event.max_participants  # Get the maximum participants from the event

        if event:
            if max_participants <= 0:
                # Booking is closed if max_participants is zero or negative
                messages.error(request, 'Booking is closed for this event.')
                return redirect('event_booking', event_id=event.event_id)  # Use event.event_id

            try:
                if attendees <= max_participants:
                    # Generate a unique booking ID using uuid
                    booking_id = uuid.uuid4().hex

                    booking = EventBooking.objects.create(
                        booking_id=booking_id,
                        user=request.user,  # Assuming you have user authentication
                        event=event,
                        attendees=attendees
                    )
                    # Deduct the number of attendees from the maximum participants
                    event.max_participants -= attendees
                    event.save()

                    messages.success(request, 'Booking successfully created.')
                    return redirect('event_booking', event_id=event.event_id)  # Use event.event_id
                else:
                    messages.error(request, 'Number of attendees exceeds maximum participants.')
                    return redirect('event_booking', event_id=event.event_id)  # Use event.event_id

            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
                return redirect('event_booking', event_id=event.event_id)  # Use event.event_id

    return render(request, 'event/bookingeventform.html', {'event': event})




# editprofile
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
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
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def reset_password(request):
    if request.method == "POST":
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match. Please try again.")
        else:
            user = request.user
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Update the session with the new password
            messages.success(request, "Password reset successful!")

            # Redirect to the user's profile page or any other desired page
            return redirect('user_profile_view')  # Change 'user_profile' to your actual profile page URL name

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
from django.shortcuts import render
from .models import BinBooking
from django.contrib.auth.models import User

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

    return render(request, 'bin/bin_details.html', context)


# admin_list_user
# userlist/views.py
from django.contrib.auth.models import User
from django.shortcuts import render

def user_list(request):
    users = User.objects.all()
    return render(request, 'admin/userlist.html', {'users': users})


#edit_user_details_by admin
# views.py
# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User

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

        user.save()
        return redirect('user_list')  # Redirect back to the user list page

    return render(request, 'admin/edituser.html', {'user': user})



