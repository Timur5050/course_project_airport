from django.contrib import admin

from hangar.models import Flight, Airplane, User, Ticket, Order

admin.site.register(Flight)
admin.site.register(Airplane)
admin.site.register(User)
admin.site.register(Ticket)
admin.site.register(Order)
