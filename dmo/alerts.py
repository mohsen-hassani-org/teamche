from django.contrib.auth import base_user
from discord.interfaces import Discord
from discord_webhook import DiscordWebhook, DiscordEmbed, webhook

from dmo.models import Dmo, DmoDay

class DiscordAlert(Discord):
    @staticmethod
    def send_new_dmo_alert(dmo):
        webhook = DiscordWebhook(url=dmo.team.dmo_settings.discord_webhook, username=dmo.team.name)
        embed = DiscordAlert._build_new_dmo_embed(dmo)
        webhook.add_embed(embed)
        response = webhook.execute()

        
    @staticmethod
    def send_fill_dmo_alert(dmo_day):
        webhook = DiscordWebhook(url=dmo_day.dmo.team.dmo_settings.discord_webhook, username=dmo_day.dmo.team.name)
        embed = DiscordAlert._build_fill_dmo_embed(dmo_day)
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
        embed.add_embed_field(name="هدف", value=dmo.goal, inline=False)
        embed.add_embed_field(name="ماه", value=dmo.month)
        embed.add_embed_field(name="سال", value=dmo.year)
        
        return embed

        
    @staticmethod
    def _build_fill_dmo_embed(dmo_day):
        ''' Create an image from dmo table and send it with description '''
        base_url = 'https://iprpars.ir'
        dmo_user = dmo_day.dmo.user.profile.display_name
        status = 'مثبت' if dmo_day.done else 'منفی'
        color = '00ff00' if dmo_day.done else 'ff0000'
        goal = dmo_day.dmo.goal
        embed = DiscordEmbed(
            title=f'تیک {status}', description=f'{dmo_user} DMO {goal} خودش رو {status} بست', color=color,
        )
        embed.set_author(
            name=dmo_user,
            url="https://panel.robin-traders.ir/",
            icon_url=f'{base_url}{dmo_day.dmo.user.profile.avatar.url}',
        )
        
        return embed

       