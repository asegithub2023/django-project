from django.urls import path
from django.contrib.auth import views as auth_views 
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('how_it_works', views.how_it_works, name='howitworks'),
    path('accounts/login/', views.login_view, name = 'login'),
    path('logout/', views.logout_view, name = 'logout'),
    path('choose_account_type/', views.choose_account_type, name='choose_account_type'),
    path('tutor-registration/', views.tutor_registration, name='tutor_registration'),
    path('student-registration/', views.student_registration, name='student_registration'),
    # path('student_detail/', views.student_detail, name='student_detail'),
    # path('tutor_detail/', views.tutor_detail, name='tutor_detail'),
    path('tutor_dashboard/tutor_profile_update/', views.tutor_profile_update, name='tutor_profile_update'),
    path('student_dashboard/student_profile_update/', views.student_profile_update, name='student_profile_update'),
    path('search/', views.search_tutors, name='search_tutors'),
    path('tutor_profile/<int:tutor_id>/', views.tutor_profile, name='tutor_profile'),
    path('all_tutors/', views.all_tutors, name='all_tutors'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('tutor_dashboard/', views.tutor_dashboard, name='tutor_dashboard'),
    path('tutor/<int:tutor_id>/add-rating/', views.add_rating, name='add_rating'),
    path('rating/<int:rating_id>/edit/', views.edit_rating, name='edit_rating'),
    path('rating/<int:rating_id>/delete/', views.delete_rating, name='delete_rating'),
    path('send-request/<int:tutor_id>/', views.send_request, name='send_request'),
    path('student_dashboard/view_response/', views.view_response, name='view_response'),
    path('tutor_dashboard/view-requests/', views.view_requests, name='view_requests'),
    path('take-action/<int:request_id>/', views.take_action, name='take_action'),
    path('delete-request/<int:request_id>/', views.delete_request, name='delete_request'),
    path('delete-request-tutor/<int:request_id>/', views.delete_request_tutor, name='delete_request_tutor'),
    path('contact/', views.index, name='index'),
      # Forum URL patterns...
      path('forum', views.front_page, name='front_page'),
      path('topics/<int:topic_id>/', views.topic_detail, name='topic_detail'),
      path('category/<int:category_id>/create_topic/', views.create_topic, name='create_topic'),
      path('category/<int:category_id>/', views.category_topics, name='category_topics'),
      path('topic/<int:topic_id>/reply/', views.reply_to_topic, name='reply_to_topic'),


      path('topic/<int:topic_id>/delete/', views.delete_topic, name='delete_topic'),
      path('topic/<int:topic_id>/edit/', views.edit_topic, name='edit_topic'),

          
      
path('topic/<int:topic_id>/reply/<int:reply_id>/delete/', views.delete_reply, name='delete_reply'),
path('topic/<int:topic_id>/reply/<int:reply_id>/edit/', views.edit_reply, name='edit_reply'),
path('topic/<int:topic_id>/reply/<int:reply_id>/', views.reply_to_reply, name='reply_to_reply'),

#password_reset_urls
path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),

path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),

path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),

path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),





path('token' , views.token_send , name="token_send"),
path('verify/<auth_token>' , views.verify , name="verify"),
path('error' , views.error_page , name="error"),


]
