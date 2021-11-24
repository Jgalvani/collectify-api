from django.contrib import admin

from .models import CarHasColor, Color, Car, User


# Register your models here.
admin.site.register(User)
admin.site.register(Car)
admin.site.register(Color)
admin.site.register(CarHasColor)
