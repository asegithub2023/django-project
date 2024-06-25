from django.contrib import admin
from .models import User, Tutor, Student, Day,Rating, Request,ContactUs,Category, Topic, Reply#, Post

# Register the models
admin.site.register(User)
admin.site.register(Tutor)
admin.site.register(Student)
admin.site.register(Day)
admin.site.register(Rating)
admin.site.register(Request)
admin.site.register(ContactUs)


#Forum model
admin.site.register(Category)
admin.site.register(Topic)
admin.site.register(Reply)

