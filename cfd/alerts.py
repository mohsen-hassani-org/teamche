from discord.interfaces import Discord

class DiscordAlert(Discord):
    @staticmethod
    def send_signal_alert(signal):
        message = DiscordAlert._build_signal_message(signal)
        discord = Discord(discord_url=signal.team.discord_url)
        discord.send_message(message)

    @staticmethod
    def _build_signal_message(signal):
        message = '**New Signal**\n'
        message += 'Pair: {}\n'.format(signal.symbol)
        message += 'By: {}\n'.format(signal.user.username)
        message += 'Entry Point 1: {}\n'.format(signal.entry_point1)
        message += 'Entry Point 2: {}\n'.format(signal.entry_point2)\
                    if signal.entry_point2 else ''
        message += 'Take Profit 1: {}\n'.format(signal.take_profit1)
        message += 'Take Profit 2: {}\n'.format(signal.take_profit2)\
                    if signal.take_profit2 else ''
        message += 'Take Profit 3: {}\n'.format(signal.take_profit3)\
                    if signal.take_profit3 else ''
        message += 'Stop Loss 1: {}\n'.format(signal.stop_loss1)
        message += 'Stop Loss 2: {}\n'.format(signal.stop_loss2)\
                    if signal.stop_loss2 else ''
        message += 'Risk Reward: {}\n'.format(signal.risk_reward)
        message += 'Result pip: {}\n'.format(signal.result_pip)
        message += 'Lot: {}\n'.format(signal.lot)
        message += 'Status: {}\n'.format(signal.status)
        message += 'Time: {}\n'.format(signal.signal_datetime)
        message += 'Entry Type: {}\n'.format(signal.entry_type)
        return message
        
        