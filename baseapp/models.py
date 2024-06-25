from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
import re
from django.core.validators import RegexValidator
from django.db import models


# Define the validator for alphabetic characters
alphabet_validator = RegexValidator(
    regex=r'^[a-zA-Z\s]*$',
    message='Only alphabet characters are allowed!'
)

class User(AbstractUser):
    first_name = models.CharField(max_length=50,validators=[alphabet_validator])
    last_name = models.CharField(max_length=50,validators=[alphabet_validator])
    email = models.EmailField(unique=True, null=False)
    username = models.CharField(unique=True, max_length=20)

    is_student = models.BooleanField(default=False)
    is_tutor = models.BooleanField(default=False)
    profile_photo = models.ImageField(upload_to='profile_photos/', default='default.jpg')
    
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class Day(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Tutor(User):
    experience = models.TextField(max_length=255)
    self_description = models.TextField(max_length=255)
    skills = models.CharField(max_length=50)
    subjects = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    education_level = models.CharField(max_length=50)
    available_days = models.ManyToManyField(Day)
    expected_fee = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    sex = models.CharField(max_length=10)
    
    class Meta:
        verbose_name = "Tutor"
        verbose_name_plural = "Tutors"


class Student(User):
    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"



# Define the validator for alphabetic characters
alphabet_validator = RegexValidator(
    regex=r'^[a-zA-Z\s]*$',
    message='Only alphabet characters are allowed!'
)

class Request(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    tutor = models.ForeignKey('Tutor', on_delete=models.CASCADE)
    status_choices = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='pending', null=False)
    request_date = models.DateTimeField(auto_now_add=True)
    city = models.CharField(max_length=100, validators=[alphabet_validator])  
    address = models.CharField(max_length=255)  
    subjects = models.CharField(max_length=100, validators=[alphabet_validator])  
    language_spoken = models.CharField(max_length=100, validators=[alphabet_validator])
    request_details = models.TextField(max_length=255, null=True, blank=True)  
    frequency_choices = [(i, str(i)) for i in range(1, 8)]
    frequency = models.IntegerField(choices=frequency_choices, null=True, blank=True)  
   


def validate_review_text(value):
    if not re.match(r'^[A-Za-z\s.!,]*$', value):
        raise ValidationError('Review text can only contain alphabets, spaces, periods, and exclamation marks.')
    if len(value) > 255:
        raise ValidationError('Review text should not exceed 255 characters.')

class Rating(models.Model):
    rating_value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    student = models.ForeignKey('Student', on_delete=models.SET_NULL, null=True)
    tutor = models.ForeignKey('Tutor', on_delete=models.CASCADE)
    review_text = models.TextField(validators=[validate_review_text])
    date_created = models.DateTimeField(auto_now_add=True)
    request = models.ForeignKey(Request, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"


#Forum model
class Category(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

class Topic(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Reply(models.Model):
    content = models.TextField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    #each reply can have a parent reply, allowing for replies to replies.
    parent_reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
         return self.content[:50]  # Display first 50 characters of post content


class ContactUs(models.Model):
    full_name = models.CharField(max_length=100)  
    email = models.EmailField(unique=True, null=False) 
    subject = models.CharField(max_length=50)
    message = models.TextField()
    
    def __str__(self):
        return self.subject
 