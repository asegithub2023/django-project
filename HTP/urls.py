
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from baseapp.views import ChangePasswordView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('baseapp.urls')),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
    
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




