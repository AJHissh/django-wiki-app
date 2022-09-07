from django.contrib import admin

# Register your models here.

from .models import Entries



# Register your models here.

class EntriesAdmin(admin.ModelAdmin):
    list_display = ("id" , "title", "text")



admin.site.register(Entries, EntriesAdmin)

