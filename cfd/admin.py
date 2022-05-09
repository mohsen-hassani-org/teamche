from django.contrib import admin
from cfd.models import (
    Signal, PTAAnalysis, ClassicAnalysis, Comment, VolumeProfileAnalysis
)


admin.site.register(Signal)
admin.site.register(PTAAnalysis)
admin.site.register(ClassicAnalysis)
admin.site.register(Comment)


@admin.register(VolumeProfileAnalysis)
class VolumeProfileAnalysisAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'datetime', 'desc', 'user')
    list_filter = ('user', 'datetime', 'team')
    search_fields = ('id', 'title', 'desc')
