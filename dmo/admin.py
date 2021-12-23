from django.contrib import admin
from dmo.models import Dmo, DmoDay, Microaction, Setting

# Register your models here.
admin.site.register(Dmo)
admin.site.register(DmoDay)
admin.site.register(Setting)
admin.site.register(Microaction)
