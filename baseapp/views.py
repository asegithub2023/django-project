from django.shortcuts import render, redirect, redirect, get_object_or_404
from django.contrib import messages
from .forms import TutorRegistrationForm, StudentRegistrationForm,StudentProfilePhotoForm, TutorProfilePhotoForm, LoginForm, RatingForm,TopicForm, ReplyForm,RequestForm,RatingForm
from .models import User, Student, Tutor, Rating,Contacts,Request,Contacts,Category, Topic, Reply#, Post 
from .models import *
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django.shortcuts import render
from django.template.defaulttags import register
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.http import HttpResponse
from django.db.models import Count
from django.contrib.auth.decorators import login_required
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Avg
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.

def home(request):
    top_tutors = Tutor.objects.annotate(avg_rating=Avg('rating__rating_value')).order_by('-avg_rating')[:3]
    return render(request, 'base/home.html', {'top_tutors': top_tutors})

def choose_account_type(request):
    return render(request, 'base/choose_account_type.html')

def student_registration(request):
    form = StudentRegistrationForm()
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_student = True
            user.save()

            # Generate and save the authentication token
            token = uuid.uuid4().hex
            user.auth_token = token
            user.save()

            # Send verification email
            send_mail_after_registration(user.email, token)

            # Redirect to a page indicating that the email has been sent
            return redirect('token_send')
    return render(request, 'base/student_registration.html', {'form': form})


def tutor_registration(request):
    form = TutorRegistrationForm()
    if request.method == 'POST':
        form = TutorRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_tutor = True
            user.save()

            # Generate and save the authentication token
            token = uuid.uuid4().hex
            user.auth_token = token
            user.save()

            # Send verification email
            send_mail_after_registration(user.email, token)

            # Redirect to a page indicating that the email has been sent
            return redirect('token_send')
    return render(request, 'base/tutor_registration.html', {'form': form})


def verify(request, auth_token):
    try:
        user = User.objects.get(auth_token=auth_token)

        if user.is_verified:
            messages.success(request, 'Your account is already verified.')
        else:
            user.is_verified = True
            user.save()
            messages.success(request, 'Your account has been verified.')

        return redirect('login')

    except User.DoesNotExist:
        return redirect('error')


def error_page(request):
    return  render(request , 'base/error.html')

def token_send(request):
    return render(request , 'base/token_send.html')

def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi, use this link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )
    
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                if not user.is_verified:
                    messages.error(request, 'Your profile is not verified. Please check your email.')
                    return redirect('login')

                login(request, user)
                messages.info(request, f'Welcome, {username}. You are logged in.')

                # Redirect to appropriate dashboard
                if user.is_student:
                    return redirect('student_dashboard')
                elif user.is_tutor:
                    return redirect('tutor_dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm(request)

    return render(request, 'base/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out!')
    return redirect('home')

@login_required
def all_tutors(request):
    tutors_list = Tutor.objects.all()
    paginator = Paginator(tutors_list, 2)  # Display 2 tutors per page

    page = request.GET.get('page')
    try:
        tutors = paginator.page(page)
    except PageNotAnInteger:
        tutors = paginator.page(1)
    except EmptyPage:
        tutors = paginator.page(paginator.num_pages)

    return render(request, 'base/all_tutors.html', {'tutors': tutors})

@login_required
def student_dashboard(request):
    
    if request.user.is_student:
        student = request.user  # Retrieve the logged-in Student object
        return render(request, 'base/student_dashboard.html', {'student': student})
  
  # Check if the user is a student
    elif not hasattr(request.user, 'student'):
        messages.error(request, 'You are not allowed to allowed to access a student dashboard!')
        return redirect('home')

@login_required
def tutor_dashboard(request):
    if request.user.is_tutor:
        tutor = request.user  # Retrieve the logged-in Tutor object
        return render(request, 'base/tutor_dashboard.html', {'tutor': tutor})
    
    # Check if the user is a tutor
    elif not hasattr(request.user, 'tutor'):
        messages.error(request, 'You are not allowed to allowed to access a tutor dashboard!')
        return redirect('home')

@login_required
def student_profile_update(request):
    # check if the request is post 
    if request.method == 'POST':
        form = StudentProfilePhotoForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            messages.success(request, 'Your profile is updated successfully')
            form.save()
            return redirect('home')
    else:
        form = StudentProfilePhotoForm(instance=request.user)
    return render(request, 'base/student_profile_update.html', {'form': form})   

@login_required
def tutor_profile_update(request):
    try:
        tutor = request.user.tutor
    except Tutor.DoesNotExist:
        # Handle the case where the Tutor instance does not exist
        messages.error(request, 'Tutor profile does not exist.')
        return redirect('home')

    if request.method == 'POST':
        form = TutorProfilePhotoForm(request.POST, request.FILES, instance=tutor)
        if form.is_valid():
            messages.success(request, 'Your profile is updated successfully')
            form.save()
            return redirect('home')
    else:
        form = TutorProfilePhotoForm(instance=tutor)
    return render(request, 'base/tutor_profile_update.html', {'form': form})

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'base/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('login')

@login_required(login_url='login')
def add_rating(request, tutor_id):
    if not hasattr(request.user, 'student'):
        messages.error(request, 'You are not allowed to rate this tutor because you are not a student!')
        return redirect('tutor_profile', tutor_id=tutor_id)

    tutor = get_object_or_404(Tutor, id=tutor_id)

    request_obj = Request.objects.filter(tutor=tutor, student=request.user.student).exclude(status='pending').first()
    if not request_obj or request_obj.status != 'accepted':
        messages.error(request, 'You are not allowed to rate this tutor!')
        return redirect('tutor_profile', tutor_id=tutor_id)

    if Rating.objects.filter(request=request_obj, student=request.user.student).exists():
        messages.error(request, 'You have already rated this tutor for this request.')
        return redirect('tutor_profile', tutor_id=tutor_id)

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.tutor = tutor
            rating.student = request.user.student
            rating.request = request_obj
            rating.save()
            messages.success(request, 'Your rating has been added successfully.')
            return redirect('tutor_profile', tutor_id=tutor_id)
    else:
        form = RatingForm()
    return render(request, 'base/add_rating.html', {'form': form, 'tutor': tutor, 'tutor_id': tutor_id})

@register.filter
def get_range(value):
    return range(value)

@login_required(login_url='login')
def edit_rating(request, rating_id):
    rating = get_object_or_404(Rating, id=rating_id)
    if request.method == 'POST':
        form = RatingForm(request.POST, instance=rating)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your rating has been updated successfully.')
            return redirect('tutor_profile', tutor_id=rating.tutor.id)
    else:
        form = RatingForm(instance=rating)
    return render(request, 'base/edit_rating.html', {'form': form, 'rating': rating})

@login_required(login_url='login')
def delete_rating(request, rating_id):
    rating = get_object_or_404(Rating, id=rating_id)
    if request.method == 'POST':
        rating.delete()
        messages.success(request, 'Your rating has been deleted successfully.')
        return redirect('tutor_profile', tutor_id=rating.tutor.id)
    return render(request, 'base/delete_rating.html', {'rating': rating})

def tutor_profile(request, tutor_id):
    tutor = get_object_or_404(Tutor, id=tutor_id)
    ratings = Rating.objects.filter(tutor=tutor)
    
    avg_rating = ratings.aggregate(avg_rating=Avg('rating_value'))
    
    # Generate a range of numbers based on the average rating
    if avg_rating['avg_rating']:
        avg_rating_range = range(int(avg_rating['avg_rating']))
    else:
        avg_rating_range = None
    
    return render(request, 'base/tutor_profile.html', {'tutor': tutor, 'ratings': ratings, 'avg_rating': avg_rating, 'avg_rating_range': avg_rating_range})

@login_required
def send_request(request, tutor_id):
    if not hasattr(request.user, 'student'):
        messages.error(request, 'You are not allowed to send a request if you are not a student.')
        return redirect('tutor_profile', tutor_id=tutor_id)

    tutor = get_object_or_404(Tutor, id=tutor_id)

    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            request_obj = form.save(commit=False)
            request_obj.student = request.user.student
            request_obj.tutor = tutor
            request_obj.save()
            send_notification_to_tutor(request.user.student, tutor)
            return redirect('student_dashboard')
    else:
        form = RequestForm()

    return render(request, 'base/send_request.html', {'form': form, 'tutor': tutor})

def send_notification_to_tutor(student, tutor):
    tutor_email = tutor.email
    student_full_name = student.get_full_name()
    subject = 'Notification: New Tutoring Request'
    message = render_to_string('base/request_notification_email.html', {
        'student_full_name': student_full_name,
        'tutor_dashboard_link': 'http://127.0.0.1:8000/tutor_dashboard/view-requests/'
    })
    plain_message = strip_tags(message)
    # Dynamically determine sender email address
    from_email = student.email
    send_mail(subject, plain_message, from_email, [tutor_email], html_message=message)

@login_required()
def view_response(request):
      # Check if the user is a student
    if not hasattr(request.user, 'student'):
        messages.error(request, 'You are not allowed to view someone response!')
        return redirect('home')

    student = request.user.student
    requests = Request.objects.filter(student=student)
    return render(request, 'base/view_response.html', {'requests': requests})

@login_required()
def view_requests(request):
      # Check if the user is a tutor
    if not hasattr(request.user, 'tutor'):
        messages.error(request, 'You are not allowed to view someone request!')
        return redirect('home')

    tutor = request.user.tutor
    requests = Request.objects.filter(tutor=tutor)
    return render(request, 'base/view_requests.html', {'requests': requests})

def take_action(request, request_id):
    request_obj = Request.objects.get(id=request_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'accept':
            request_obj.status = 'accepted'
            request_obj.save()
            send_notification_email(request_obj)
        elif action == 'reject':
            request_obj.status = 'rejected'
            request_obj.save()
            send_notification_email(request_obj)
    return redirect('view_requests')

def send_notification_email(request_obj):
    student_email = request_obj.student.email
    tutor_full_name = request_obj.tutor.get_full_name()
    subject = 'Notification: Response to Your Request'
    message = render_to_string('base/notification_email.html', {
        'tutor_full_name': tutor_full_name,
       'student_dashboard_link': 'http://127.0.0.1:8000/student_dashboard/view_response/'

    })
    plain_message = strip_tags(message)
    from_email = request_obj.tutor.email  # Dynamically determine sender email
    send_mail(subject, plain_message, from_email, [student_email], html_message=message)

@login_required
def delete_request(request, request_id):
    request_obj = get_object_or_404(Request, id=request_id)
    
    # Ensure that only the student who sent the request can delete it
    if request.user.is_student and request.user.student == request_obj.student:
        request_obj.delete()
        return redirect('view_response')
    else:
        # Handle unauthorized access or other errors
        return HttpResponseForbidden("You are not authorized to delete this request.")

@login_required
def delete_request_tutor(request, request_id):
    # Retrieve the request object
    request_obj = get_object_or_404(Request, id=request_id)
    
    # Check if the current user is the tutor associated with the request
    if request.user.is_tutor and request.user.tutor == request_obj.tutor:
       
        request_obj.delete()
        return redirect('view_requests')  # Redirect to the tutor's request dashboard
    else:
        # If not authorized, return forbidden response
        return HttpResponseForbidden("You are not authorized to delete this request.")

def search_tutors(request):
    if 'search2' in request.GET:
        query = request.GET['search2']
        tutors = Tutor.objects.filter(
            skills__icontains=query) | Tutor.objects.filter(
            sex__icontains=query) | Tutor.objects.filter(
            location__icontains=query) | Tutor.objects.filter(
            subjects__icontains=query)
        return render(request, 'base/search_results.html', {'tutors': tutors, 'query': query})
    else:
        return render(request, 'home.html')

@login_required
def index(request):
    if request.method == 'POST':
        # Fetching user details from the request
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Save contact with user details
        contact = Contacts.objects.create(
            full_name=full_name,
            email=email,
            subject=subject,
            message=message
        )
        
        # Return response after saving
        return HttpResponse('<h1>Thanks for contacting us!</h1>')

    return render(request, 'base/index.html')

@login_required
def create_topic(request, category_id):
    category = Category.objects.get(id=category_id)
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            creator = request.user
            topic = Topic.objects.create(title=title, content=content, category=category, creator=creator)
            return redirect('front_page')  # Redirect to topic detail page
    else:
        form = TopicForm()
    return render(request, 'base/create_topic.html', {'form': form, 'category': category})

@login_required
def front_page(request):
    categories = Category.objects.all()
    latest_topics = Topic.objects.all().order_by('-created_at')[:5].annotate(num_replies=Count('reply'))
    return render(request, 'base/front_page.html', {'categories': categories, 'latest_topics': latest_topics})

@login_required
def category_topics(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    topics = category.topic_set.all()
    return render(request, 'base/category_topics.html', {'category': category, 'topics': topics})

@login_required
def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    replies = Reply.objects.filter(topic=topic, parent_reply__isnull=True).order_by('-created_at')
    num_replies = Reply.objects.filter(topic=topic).count()
    if request.method == 'POST':
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            content = reply_form.cleaned_data['content']
            reply = Reply.objects.create(content=content, topic=topic, creator=request.user)
            return redirect('topic_detail', topic_id=topic_id)
    else:
        reply_form = ReplyForm()
    return render(request, 'base/topic_detail.html', {'topic': topic, 'replies': replies, 'reply_form': reply_form, 'num_replies': num_replies})

@login_required
def reply_to_topic(request, topic_id, reply_id=None):
    topic = get_object_or_404(Topic, pk=topic_id)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            if reply_id:
                parent_reply = get_object_or_404(Reply, pk=reply_id)
                Reply.objects.create(content=content, topic=topic, creator=request.user, parent_reply=parent_reply)
            else:
                Reply.objects.create(content=content, topic=topic, creator=request.user)
    return redirect('topic_detail', topic_id=topic_id)

@login_required
def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    if request.user == topic.creator:
        topic.delete()
        messages.success(request, 'Topic deleted successfully!')
        return redirect('front_page')  
    else:
        # Handle unauthorized access
        return HttpResponseForbidden()

@login_required
def edit_topic(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    if request.user == topic.creator:
        if request.method == 'POST':
            form = TopicForm(request.POST, instance=topic)
            if form.is_valid():
                form.save()
                return redirect('topic_detail', topic_id=topic_id)  # Redirect to topic detail page
        else:
            form = TopicForm(instance=topic)
        return render(request, 'base/edit_topic.html', {'form': form, 'topic': topic})
    else:
        # Handle unauthorized access
        return HttpResponseForbidden()

@login_required
def delete_reply(request, topic_id, reply_id):
    reply = get_object_or_404(Reply, pk=reply_id)
    if request.user == reply.creator:
        reply.delete()
        messages.success(request, 'Reply deleted successfully gys!')
    return redirect('topic_detail', topic_id=topic_id)

@login_required
def edit_reply(request, topic_id, reply_id):
    reply = get_object_or_404(Reply, pk=reply_id)
    if request.user == reply.creator:
        if request.method == 'POST':
            form = ReplyForm(request.POST, instance=reply)
            if form.is_valid():
                form.save()
                return redirect('topic_detail', topic_id=topic_id)
        else:
            form = ReplyForm(instance=reply)
        return render(request, 'base/edit_reply.html', {'form': form, 'reply': reply})
    else:
        # Handle unauthorized access
        return HttpResponseForbidden()

def how_it_works(request):
    return render(request, 'base/howItworks.html')


@login_required
def reply_to_reply(request, topic_id, reply_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    parent_reply = get_object_or_404(Reply, pk=reply_id)

    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            new_reply = form.save(commit=False)
            new_reply.topic = topic
            new_reply.creator = request.user
            new_reply.parent_reply = parent_reply
            new_reply.save()
            return redirect('topic_detail', topic_id=topic_id)
    else:
        form = ReplyForm()

    return render(request, 'base/reply_to_reply.html', {'form': form, 'parent_reply': parent_reply, 'topic': topic})
