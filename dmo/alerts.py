import imgkit
from django.contrib.auth import base_user
from discord.interfaces import Discord
from discord_webhook import DiscordWebhook, DiscordEmbed, webhook
from dmo.profile.utils import dmo_last_days

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
        summary = dmo_day.dmo.get_summary_as_table()
        image_file = DiscordAlert._build_image(summary)

        webhook.add_embed(embed)
        webhook.add_file(file=image_file, filename=f'summary{dmo_day.dmo.goal}.png')
        response = webhook.execute()

    @staticmethod
    def _build_new_dmo_embed(dmo: Dmo):
        base_url = 'http://iprpars.ir'
        dmo_user = dmo.user.profile.display_name
        user_avatar = f'{base_url}{dmo.user.profile.avatar.url}' if dmo.user.profile.avatar else ''
        embed = DiscordEmbed(
            title="یک DMO جدید!", description=f'همین الان {dmo_user} یک DMO جدید ثبت کرد', color=dmo.color.replace('#', ''),
        )
        embed.set_author(
            name=dmo_user,
            url="https://panel.robin-traders.ir/",
            icon_url=user_avatar,
        )
        embed.add_embed_field(name="هدف", value=dmo.goal, inline=False)
        embed.add_embed_field(name="ماه", value=dmo.month)
        embed.add_embed_field(name="سال", value=dmo.year)
        
        return embed

        
    @staticmethod
    def _build_fill_dmo_embed(dmo_day):
        ''' Create an image from dmo table and send it with description '''
        base_url = 'http://iprpars.ir'
        dmo_user = dmo_day.dmo.user.profile.display_name
        user_avatar = f'{base_url}{dmo_day.dmo.user.profile.avatar.url}' if dmo_day.dmo.user.profile.avatar else ''
        status = 'مثبت' if dmo_day.done else 'منفی'
        color = '00ff00' if dmo_day.done else 'ff0000'
        goal = dmo_day.dmo.goal
        day = dmo_day.day
        description = f'{dmo_user} روز {day}ام DMO "{goal}" خودش رو {status} بست'
        embed = DiscordEmbed(
            title=f'تیک {status} DMO', description=description, color=color,
        )
        embed.set_author(
            name=dmo_user,
            url=user_avatar,
            icon_url=user_avatar,
        )
        embed.add_embed_field(name="روز", value=dmo_day.day, inline=True)
        embed.add_embed_field(name="هدف DMO", value=dmo_day.dmo.goal, inline=True)
        if dmo_day.comment:
            embed.add_embed_field(name="توضیحات", value=dmo_day.comment, inline=False)
        return embed

    @staticmethod
    def _build_image(summary):
        options = {'crop-w': '350', 'xvfb': ''}
        body = '''
        <html>
            <head>
                <style>
                body {margin: 0px;}
                .dmo_summary .green {background-color: limegreen;}
                .dmo_summary .red {background-color: indianred;}
                .dmo_summary {border: 1px solid #18252d;width: 100%;max-width: 350px;margin: 0px; border-collapse: collapse}
                .dmo_summary tr td {border: 1px solid #18252d;color: #222;height: 15px;max-width: 25px;width: 10%;text-align: center;}
                </style>
            </head>
            <body>
        '''
        body += '''
            {summary}
            </body>
        </html>
        '''.format(summary=summary)
        image = imgkit.from_string(body, False, options=options)
        return image