from django.contrib import admin
from .models import (
    Adventure,
    Inhabitant,
    Factory,
    Fence,
    Song,
    Code,
    Guard,
    Day,
)

admin.site.register(Adventure)
admin.site.register(Inhabitant)
admin.site.register(Factory)
admin.site.register(Fence)
admin.site.register(Song)
admin.site.register(Code)
admin.site.register(Guard)
admin.site.register(Day)
