from django.contrib import admin

from .models import Anchor, TagDistance, Read, Transmitter


admin.site.register(Anchor)
admin.site.register(Read)
admin.site.register(Transmitter)

admin.site.register(TagDistance)
