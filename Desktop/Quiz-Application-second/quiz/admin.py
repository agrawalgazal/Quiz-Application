from django.contrib import admin
from .models import Topic,Quiz,Question,UserResponse,Point

# Register your models here.
admin.site.register(Topic)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(UserResponse)
admin.site.register(Point)