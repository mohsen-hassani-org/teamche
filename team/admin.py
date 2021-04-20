from django.contrib import admin
from team.models import *

# Register your models here.
admin.site.register(Team)
admin.site.register(TeamInvitation)
admin.site.register(Vote)
admin.site.register(VoteChoice)
admin.site.register(UserVote)
admin.site.register(Meeting)
admin.site.register(MeetingSigature)
admin.site.register(Attendance)