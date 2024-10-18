from django.contrib import admin

from .models import Read, Transmitter, StatusLog


admin.site.register(Read)
admin.site.register(Transmitter)
admin.site.register(StatusLog)



