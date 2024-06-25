from django.test import TestCase

# Create your tests here.
import pytest
from django.core.exceptions import ValidationError
from myapp.models import User, Tutor, Student, Request, Rating, validate_review_text

@pytest.mark.django_db
def test_user_creation():
    user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
    assert user.username == 'testuser'
    assert user.email == 'test@example.com'
    assert user.is_student == False
    assert user.is_tutor == False

@pytest.mark.django_db
def test_tutor_creation():
    tutor = Tutor.objects.create_user(username='tutoruser', email='tutor@example.com', password='password123', is_tutor=True)
    assert tutor.username == 'tutoruser'
    assert tutor.email == 'tutor@example.com'
    assert tutor.is_tutor == True

@pytest.mark.django_db
def test_request_creation():
    student = Student.objects.create_user(username='studentuser', email='student@example.com', password='password123', is_student=True)
    tutor = Tutor.objects.create_user(username='tutoruser', email='tutor@example.com', password='password123', is_tutor=True)
    request = Request.objects.create(student=student, tutor=tutor, city='Test City', address='123 Test St', subjects='Math', language_spoken='English')
    assert request.status == 'pending'
    assert request.city == 'Test City'

def test_validate_review_text():
    valid_text = "Great tutor!"
    validate_review_text(valid_text)  # Should not raise an exception

    invalid_text = "Great tutor @$%"
    with pytest.raises(ValidationError):
        validate_review_text(invalid_text)
