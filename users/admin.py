from django.contrib import admin
from .models import Score, Flag, SubmittedFlag

admin.site.register(Score)
admin.site.register(Flag)
admin.site.register(SubmittedFlag)
