from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Tutor, Student,User,Rating,Topic,Reply
from django.contrib.auth.forms import AuthenticationForm
from .models import Request

from django.core.validators import RegexValidator
from .models import Request


# Define the validator
alphabet_validator = RegexValidator(
    regex=r'^[a-zA-Z\s]*$',
    message='Only alphabet characters are allowed!'
)
class StudentRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, validators=[alphabet_validator])
    last_name = forms.CharField(max_length=50, validators=[alphabet_validator])

    # fields we want to include and customize in our form
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))

    class Meta(UserCreationForm.Meta):
        model = Student
        fields = [ 'first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class TutorRegistrationForm(UserCreationForm):
      # fields we want to include and customize in our form
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))

    class Meta(UserCreationForm.Meta):
        model = Tutor
        fields = [ 'first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        
 
class TutorProfilePhotoForm(forms.ModelForm):
    profile_photo = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))                         
    class Meta:
        model = Tutor
        fields = ['first_name','last_name', 'username', 'email','subjects','sex','education_level','available_days','location','self_description', 'experience', 'expected_fee','profile_photo']


class StudentProfilePhotoForm(forms.ModelForm):
    profile_photo = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))                         
    class Meta:
        model = Student
        fields = ['first_name','last_name', 'username', 'email', 'profile_photo']


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Email or Username'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Password'})


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating_value', 'review_text']
        widgets = {
            'rating_value': forms.NumberInput(attrs={'type': 'hidden'}),  # Hide numerical rating input
        }
        widgets = {
            'review_text': forms.Textarea(attrs={'class': 'custom-textarea'}),
        }

    def clean_review_text(self):
        review_text = self.cleaned_data.get('review_text')
        if len(review_text) > 255:
            raise forms.ValidationError('Review text should not exceed 255 characters.')
        return review_text
        



# # Define the validator
# alphabet_validator = RegexValidator(
#     regex=r'^[a-zA-Z\s]*$',
#     message='Only alphabet characters are allowed!'
# )

class RequestForm(forms.ModelForm):
    subjects = forms.CharField(validators=[alphabet_validator])
    city = forms.CharField(validators=[alphabet_validator])
    language_spoken = forms.CharField(validators=[alphabet_validator])
    
    class Meta:
        model = Request
        fields = ['subjects', 'city', 'address', 'language_spoken', 'request_details']


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'custom-textarea'})
        }
        

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'content']
       
        widgets = {
            'content': forms.Textarea(attrs={'class': 'custom-textarea'}),
        }

       



#reply_to_reply is not working
#user cannot reply to his own message(remove such functionality)