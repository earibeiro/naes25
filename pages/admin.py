from django.contrib import admin
from .models import State, City, Person, Company

admin.site.register(State)
admin.site.register(City)
admin.site.register(Person)
admin.site.register(Company)
