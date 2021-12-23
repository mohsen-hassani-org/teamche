from django.contrib.auth import base_user
from discord.interfaces import Discord
from discord_webhook import DiscordWebhook, DiscordEmbed

from dmo.models import Dmo

class DiscordAlert(Discord):
    @staticmethod
    def send_new_dmo_alert(dmo):
        webhook = DiscordWebhook(url=dmo.team.dmo_settings.discord_webhook, username=dmo.team.name)
        embed = DiscordAlert._build_new_dmo_embed(dmo)
        webhook.add_embed(embed)
        response = webhook.execute()

    @staticmethod
    def _build_new_dmo_embed(dmo: Dmo):
        base_url = 'https://iprpars.ir'
        dmo_user = dmo.user.profile.display_name
        embed = DiscordEmbed(
            title="یک DMO جدید!", description=f'همین الان {dmo_user} یک DMO جدید ثبت کرد', color=dmo.color.replace('#', ''),
        )
        embed.set_author(
            name=dmo_user,
            url="https://panel.robin-traders.ir/",
            icon_url=f'{base_url}{dmo.user.profile.avatar.url}',
        )
        embed.set_timestamp()
        embed.add_embed_field(name="هدف", value=dmo.goal, inline=False)
        embed.add_embed_field(name="ماه", value=dmo.month)
        embed.add_embed_field(name="سال", value=dmo.year)
        
        return embed