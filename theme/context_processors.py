from theme import models

def settings_processor(request):
    settings,created = models.SiteSetting.objects.get_or_create()
    return {'settings': settings}