from django.contrib import admin
from.models import State,Relationship,Gender
# Register your models here.
admin.site.register(Gender)
admin.site.register(Relationship)
admin.site.register(State)