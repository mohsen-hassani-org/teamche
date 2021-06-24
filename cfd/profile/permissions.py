from django.core.exceptions import PermissionDenied

def team_leader_permission(user, team):
    if not user.is_superuser:
        if team and not user == team.leader:
            raise PermissionDenied

def team_registration_permission(user, team):
    if not user.is_superuser:
        if team and not user == team.leader:
            if user not in team.users.all():
                raise PermissionDenied