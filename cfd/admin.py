from django.contrib import admin
from cfd.models import Signal, PTAAnalysis, ClassicAnalysis
# Register your models here.
admin.site.register(Signal)
admin.site.register(PTAAnalysis)
admin.site.register(ClassicAnalysis)
