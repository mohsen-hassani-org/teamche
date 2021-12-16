import requests
from django.conf import settings
from django.utils.translation import ugettext as _


def get_discord_url():
    assert hasattr(settings, 'DISCORD_WEBHOOK_URL'), _(
        'DISCORD_WEBHOOK_URL not set. You should either set it in your settings.py or '
        'pass it as parameter to Discord __init__ method.'
    )
    return settings.DISCORD_WEBHOOK_URL


class Discord:
    def __init__(self, discord_url=get_discord_url, bot_name='Discord Bot'):
        self.discord_url = discord_url
        self.bot_name = bot_name

    def send_message(self, message):
        headers = { "Content-Type": "application/json" }
        data = {'content': message, 'username': self.bot_name}
        requests.post(self.discord_url, json=data, headers=headers)
        
