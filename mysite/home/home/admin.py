from django.contrib import admin
from .models import Job, Comment, Fav
# Register your models here.
admin.site.register(Job)
admin.site.register(Comment)
admin.site.register(Fav)