from django.contrib import admin
from cfd.models import Signal, PTAAnalysis, ClassicAnalysis, Comment
# Register your models here.
admin.site.register(Signal)
admin.site.register(PTAAnalysis)
admin.site.register(ClassicAnalysis)
admin.site.register(Comment)
