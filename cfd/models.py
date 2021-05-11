from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import SET_NULL
from django.utils.translation import ugettext_lazy  as _
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


# Create your models here.

class Comment(models.Model):
    class Meta:
        verbose_name = _('نظر')
        verbose_name_plural = _('نظرات')
    def __str__(self):
        return f'{self.user} on {self.post}: {self.body}'
    user = models.ForeignKey(User, on_delete=SET_NULL, null=True, verbose_name=_('کاربر'))
    create_on = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ'))
    body = models.CharField(max_length=500, verbose_name=_('متن نظر'))
    public = models.BooleanField(default=True, verbose_name=_('عمومی'))
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    post = GenericForeignKey('content_type', 'object_id')

 
class Asset(models.Model):
    class Meta:
        verbose_name = _('دارایی')
        verbose_name_plural = _('دارایی‌ها')
    def __str__(self):
        return self.name
    name = models.CharField(max_length=10, verbose_name=_('نام دارایی'))

class PTAAnalysis(models.Model):
    class Meta:
        verbose_name = _('آنالیز PTA')
        verbose_name_plural = _('آنالیز‌های PTA')
    class ChartMove(models.TextChoices):
        IMPULSIVE = 'imp', 'Impulsive'
        CORRECTIVE = 'cor', 'Corrective'
    class ImpulsiveDirection(models.TextChoices):
        UP = 'up', _('صعودی')
        DOWN = 'dw', _('نزولی')
    class PTAPattern(models.TextChoices):
        UP_TRIANGLE = 'up_tri', 'مثلث صعودی'
        DW_TRIANGLE = 'dw_tri', 'مثلث نزولی'
        RECTANGLE = 'rct', 'مستطیل'
    class ScenarioTypes(models.TextChoices):
        SCENARIO1 = 'sc1', _('سناریو شماره 1')
        SCENARIO2 = 'sc2', _('سناریو شماره 2')
        SCENARIO3 = 'sc3', _('سناریو شماره 3')
        SCENARIO4 = 'sc4', _('سناریو شماره 4')
        SCENARIO5 = 'sc5', _('سناریو شماره 5')
    def __str__(self):
        return '{user} - date: {date} - time: {time}'.format(user=self.user, date=self.datetime.strftime('%Y/%m/%d'), time=self.datetime.strftime('%H:%M:%S'))
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='pta_analysis', verbose_name=_('کاربر'))
    any_news = models.BooleanField(default=False, verbose_name=_('خبر؟'), help_text=_('در صورتی که در مدت معامله، خبری مرتبط با دارایی وجود دارد این گزینه را تیک بزنید'))
    news_detail = models.TextField(verbose_name=_('جزئیات خبر'), null=True, blank=True, help_text=_('توجه: سی دقیقه قبل و بعد از خبر نباید وارد معامله شوید، اما در صورتی که برای انجام معامله مصر هستید، اطلاعات خبر را اینجا وارد کنید.'))
    chart_move = models.CharField(max_length=3, choices=ChartMove.choices, verbose_name=_('حرکت نمودار'))
    impulsive_direction = models.CharField(max_length=2, choices=ImpulsiveDirection.choices, verbose_name=_('جهت روند'), null=True, blank=True)
    zone_rejects = models.PositiveSmallIntegerField(verbose_name=_('مقاومت ناحیه'), help_text=_('تعداد برخورد و بازگشت قیمت از ناحیه را مشخص کنید '))
    pattern = models.CharField(max_length=8, choices=PTAPattern.choices, null=True, blank=True, verbose_name=_('الگوی نمودار'))
    scenario = models.CharField(max_length=3, choices=ScenarioTypes.choices, verbose_name=_('سناریو'))
    datetime = models.DateTimeField(auto_now=True)
    image_url = models.URLField(max_length=300, null=True, blank=True)
    comments = GenericRelation(Comment)

class ClassicAnalysis(models.Model):
    class Meta:
        verbose_name = _('آنالیز Classic')
        verbose_name_plural = _('آنالیزهای Classic')
    class TrendTypes(models.TextChoices):
        BULLISH = 'bl', _('صعودی')
        BEARISH = 'br', _('نزولی')
        SIDEWAY = 'sd', _('رنج')
    class SignalTypes(models.TextChoices):
        BUY = 'by', _('خرید')
        SELL = 'sl', _('فروش')
        NATURE = 'nt', _('خنثی')
    class TimeFrames(models.TextChoices):
        M5 = '5M'
        M15 = '15M'
        M30 = '30M'
        H1 = '1H'
        H4 = '4H'
        D1 = '1D'
        W1 = '1W'
    class ClassicPatternTypes(models.TextChoices):
        SYMMETRICAL_TRIANGLE = 'sy_tri', _('مثلث متقارن')
        DESCENDING_TRIANGLE = 'ds_tri', _('مثلث نزولی')
        ASCENDING_TRIANGLE = 'as_tri', _('مثلث صعودی')
        DESCENDING_WEDGE = 'ds_wdg', _('کنج نزولی')
        ASCENDING_WEDGE = 'as_wdg', _('کنج صعودی')
        HEAD_AND_SHOULDER = 'hd_sh', _('سر و شانه')
        DOUBLE_TOP = 'do_top', _('دو سقف')
        DOUBLE_BOTTOM = 'do_btm', _('دو کف')
        TRIPLE_TOP = 'tr_top', _('سه سقف')
        TRIPLE_BOTTOM = 'tr_btm', _('سه کف')
        CHANNEL = 'chnl', _('کانال')
        FLAG = 'flag', _('پرچم')
        NOPATTERN = 'none', _('بدون الگو')
    class PivotLines(models.TextChoices):
        NOPIVOT = 'n', _('بدون Pivot')
        DAILY = 'd', _('روزانه')
        WEEKLY = 'w', _('هفتگی')
        MONTHLY = 'm', _('ماهیانه')
    class FiboCorrections(models.TextChoices):
        NO_CORRECTION = 'nc', _('بدون اصلاح')
        C23 = '23', '23.6%'
        C38 = '38', '38.2%'
        C50 = '50', '50%'
        C61 = '61', '61.8%'
        C74 = '74', '74%'
    class FiboTarget(models.TextChoices):
        NO_TARGET = 'nt', _('بدون هدف')
        T127 = '127', '127%'
        T150 = '150', '150%'
        T161 = '161', '161.8%'
        T200 = '200', '200%'
        T261 = '261', '261.8%'
        T423 = '423', '423.6%'
    class EliotWaves(models.TextChoices):
        NO_WAVE = 'nwv', _('بدون موج')
        WAVE1 = 'wv1', _('موج اول')
        WAVE2 = 'wv2', _('موج دوم')
        WAVE3 = 'wv3', _('موج سوم')
        WAVE4 = 'wv4', _('موج چهارم')
        WAVE5 = 'wv5', _('موج پنجم')
        WAVEA = 'wva', _('موج A')
        WAVEB = 'wvb', _('موج B')
        WAVEC = 'wvc', _('موج C')
    def __str__(self):
        return '{title} ({user}) - date: {date} {time}'.format(title=self.title, user=self.user, date=self.datetime.strftime('%Y/%m/%d'), time=self.datetime.strftime('%H:%M:%S'))
    title = models.CharField(max_length=70, default='تحلیل کلاسیک', verbose_name=_('عنوان'))
    desc = models.TextField(null=True, blank=True, verbose_name=_('توضیحات'))
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='classic_analysis', verbose_name=_('کاربر'))
    news = models.TextField(verbose_name=_('اخبار'), null=True, blank=True, help_text=_('توجه: سه دقیقه قبل و بعد از خبر نباید وارد معامله شوید، اما در صورتی که برای انجام معامله مصر هستید، اطلاعات خبر را اینجا وارد کنید.'))
    major_trend = models.CharField(max_length=2, choices=TrendTypes.choices, default=TrendTypes.BULLISH, verbose_name=_('روند اصلی'))
    major_trend_signal = models.CharField(max_length=2, choices=SignalTypes.choices, default=SignalTypes.NATURE, verbose_name=_('سیگنال دریافتی')) 
    major_trend_timeframe = models.CharField(max_length=3, choices=TimeFrames.choices, verbose_name=_('تایم‌فریم'), default=TimeFrames.D1)
    intermediate_trend = models.CharField(max_length=2, choices=TrendTypes.choices, default=TrendTypes.BULLISH, verbose_name=_('روند میان‌مدت'))
    intermediate_trend_signal = models.CharField(max_length=2, choices=SignalTypes.choices, default=SignalTypes.NATURE, verbose_name=_('سیگنال دریافتی')) 
    intermediate_trend_timeframe = models.CharField(max_length=3, choices=TimeFrames.choices, verbose_name=_('تایم‌فریم'), default=TimeFrames.H1)
    eliot = models.CharField(max_length=3, choices=EliotWaves.choices, verbose_name=_('موج‌های الیوت'), default=EliotWaves.NO_WAVE)
    eliot_signal = models.CharField(max_length=2, choices=SignalTypes.choices, default=SignalTypes.NATURE, verbose_name=_('سیگنال دریافتی')) 
    support_resistance1_from = models.DecimalField(max_digits=11, decimal_places=4, null=True, blank=True, verbose_name=_('شروع حمایت و مقاومت اول'))
    support_resistance1_to = models.DecimalField(max_digits=11, decimal_places=4, null=True, blank=True, verbose_name=_('پایان حمایت و مقاومت اول'))
    support_resistance2_from = models.DecimalField(max_digits=11, decimal_places=4, null=True, blank=True, verbose_name=_('شروع حمایت و مقاومت دوم'))
    support_resistance2_to = models.DecimalField(max_digits=11, decimal_places=4, null=True, blank=True, verbose_name=_('پایان حمایت و مقاومت دوم'))
    support_resistance3_from = models.DecimalField(max_digits=11, decimal_places=4, null=True, blank=True, verbose_name=_('شروع حمایت و مقاومت سوم'))
    support_resistance3_to = models.DecimalField(max_digits=11, decimal_places=4, null=True, blank=True, verbose_name=_('پایان حمایت و مقاومت سوم'))
    support_resistance1_timeframe = models.CharField(max_length=3, choices=TimeFrames.choices, verbose_name=_('تایم‌فریم'), default=TimeFrames.H1)
    support_resistance2_timeframe = models.CharField(max_length=3, choices=TimeFrames.choices, verbose_name=_('تایم‌فریم'), default=TimeFrames.H1)
    support_resistance3_timeframe = models.CharField(max_length=3, choices=TimeFrames.choices, verbose_name=_('تایم‌فریم'), default=TimeFrames.H1)
    support_resistance_signal = models.CharField(max_length=2, choices=SignalTypes.choices, default=SignalTypes.NATURE, verbose_name=_('سیگنال دریافتی')) 
    pattern = models.CharField(max_length=8, choices=ClassicPatternTypes.choices, default=ClassicPatternTypes.NOPATTERN, verbose_name=_('الگو'))
    pattern_signal = models.CharField(max_length=2, choices=SignalTypes.choices, default=SignalTypes.NATURE, verbose_name=_('سیگنال دریافتی')) 
    pattern_timeframe = models.CharField(max_length=3, choices=TimeFrames.choices, verbose_name=_('تایم‌فریم'), default=TimeFrames.H1)
    moving = models.TextField(verbose_name=_('میانگین متحرک'), null=True, blank=True)
    moving_signal = models.CharField(max_length=2, choices=SignalTypes.choices, default=SignalTypes.NATURE, verbose_name=_('سیگنال دریافتی')) 
    moving_timeframe = models.CharField(max_length=3, choices=TimeFrames.choices, verbose_name=_('تایم‌فریم'), default=TimeFrames.H1)
    pivot = models.CharField(max_length=1, choices=PivotLines.choices, default=PivotLines.NOPIVOT, verbose_name=_('خطوط Pivot'))
    pivot_signal = models.CharField(max_length=2, choices=SignalTypes.choices, default=SignalTypes.NATURE, verbose_name=_('سیگنال دریافتی')) 
    pivot_timeframe = models.CharField(max_length=3, choices=TimeFrames.choices, verbose_name=_('تایم‌فریم'), default=TimeFrames.H1)
    fibo_correction = models.CharField(max_length=2, choices=FiboCorrections.choices, verbose_name=_('اصلاح فیبوناچی'), default=FiboCorrections.NO_CORRECTION)
    fibo_target = models.CharField(max_length=3, choices=FiboTarget.choices, verbose_name=_('هدف فیبوناچی'), default=FiboTarget.NO_TARGET)
    fibo_signal = models.CharField(max_length=2, choices=SignalTypes.choices, default=SignalTypes.NATURE, verbose_name=_('سیگنال دریافتی')) 
    time_divergent = models.BooleanField(verbose_name=_('واگرایی زمانی'))
    time_divergent_signal = models.CharField(max_length=2, choices=SignalTypes.choices, default=SignalTypes.NATURE, verbose_name=_('سیگنال دریافتی')) 
    time_divergent_timeframe = models.CharField(max_length=3, choices=TimeFrames.choices, verbose_name=_('تایم‌فریم'), default=TimeFrames.H1)
    candle = models.TextField(verbose_name=_('کندل‌شناسی'), null=True, blank=True)
    candle_signal = models.CharField(max_length=2, choices=SignalTypes.choices, default=SignalTypes.NATURE, verbose_name=_('سیگنال دریافتی'))
    candle_timeframe = models.CharField(max_length=3, choices=TimeFrames.choices, verbose_name=_('تایم‌فریم'), default=TimeFrames.H1)
    rsi_oversold = models.BooleanField(verbose_name=_('اشباع فروش'), default=False)
    rsi_overbought = models.BooleanField(verbose_name=_('اشباع خرید'), default=False)
    rsi_divergence = models.BooleanField(verbose_name=_('واگرایی'), default=False)
    rsi_hidden_divergence = models.BooleanField(verbose_name=_('واگرایی مخفی'), default=False)
    rsi_trend_breakout = models.BooleanField(verbose_name=_('شکست خط روند'), default=False)
    rsi_signal = models.CharField(max_length=2, choices=SignalTypes.choices, default=SignalTypes.NATURE, verbose_name=_('سیگنال دریافتی')) 
    rsi_timeframe = models.CharField(max_length=3, choices=TimeFrames.choices, verbose_name=_('تایم‌فریم'), default=TimeFrames.H1)
    momentum_oversold = models.BooleanField(verbose_name=_('اشباع فروش'), default=False)
    momentum_overbought = models.BooleanField(verbose_name=_('اشباع خرید'), default=False)
    momentum_divergence = models.BooleanField(verbose_name=_('واگرایی'), default=False)
    momentum_hidden_divergence = models.BooleanField(verbose_name=_('واگرایی مخفی'), default=False)
    momentum_trend_breakout = models.BooleanField(verbose_name=_('شکست خط روند'), default=False)
    momentum_signal = models.CharField(max_length=2, choices=SignalTypes.choices, default=SignalTypes.NATURE, verbose_name=_('سیگنال دریافتی')) 
    momentum_timeframe = models.CharField(max_length=3, choices=TimeFrames.choices, verbose_name=_('تایم‌فریم'), default=TimeFrames.H1)
    macd_divergence = models.BooleanField(verbose_name=_('واگرایی'), default=False)
    macd_hidden_divergence = models.BooleanField(verbose_name=_('واگرایی مخفی'), default=False)
    macd_signal = models.CharField(max_length=2, choices=SignalTypes.choices, default=SignalTypes.NATURE, verbose_name=_('سیگنال دریافتی')) 
    macd_timeframe = models.CharField(max_length=3, choices=TimeFrames.choices, verbose_name=_('تایم‌فریم'), default=TimeFrames.H1)
    stochastic_oversold = models.BooleanField(verbose_name=_('اشباع فروش'), default=False)
    stochastic_overbought = models.BooleanField(verbose_name=_('اشباع خرید'), default=False)
    stochastic_bullish_breakout = models.BooleanField(verbose_name=_('شکست صعودی '), default=False)
    stochastic_bearish_breakout = models.BooleanField(verbose_name=_('شکست نزولی '), default=False)
    stochastic_signal = models.CharField(max_length=2, choices=SignalTypes.choices, verbose_name=_('سیگنال دریافتی'), null=True, blank=True) 
    stochastic_timeframe = models.CharField(max_length=3, choices=TimeFrames.choices, verbose_name=_('تایم‌فریم'), null=True, blank=True)
    atr = models.TextField(verbose_name=_('ATR'), null=True, blank=True)
    atr_signal = models.CharField(max_length=2, choices=SignalTypes.choices, verbose_name=_('سیگنال دریافتی'), null=True, blank=True) 
    atr_timeframe = models.CharField(max_length=3, choices=TimeFrames.choices, verbose_name=_('تایم‌فریم'), null=True, blank=True)
    atx = models.TextField(verbose_name=_('ATX'), null=True, blank=True)
    atx_signal = models.CharField(max_length=2, choices=SignalTypes.choices, verbose_name=_('سیگنال دریافتی'), null=True, blank=True) 
    atx_timeframe = models.CharField(max_length=3, choices=TimeFrames.choices, verbose_name=_('تایم‌فریم'), null=True, blank=True)
    datetime = models.DateTimeField(auto_now=True)
    image_url = models.URLField(max_length=300, null=True, blank=True, verbose_name=_('URL تصویر'))
    tradingview_url = models.URLField(max_length=300, null=True, blank=True, verbose_name=_('آدرس تحلیل در TradingView'))
    comments = GenericRelation(Comment)

class Signal(models.Model):
    class TradeType(models.TextChoices):
        BUY = 'buy', _('خرید')
        SELL = 'sell', _('فروش')
    class SignalStatus(models.TextChoices):
        RUNNING = 'running', _('در حال اجرا')
        FILLED = 'filled', _('انجام شده')
        CANCELED = 'canceled', _('لغو شده')
    class Meta:
        verbose_name = _('سیگنال')
        verbose_name_plural = _('سیگنال‌ها')
    def __str__(self):
        return 'Signal by {user} on {asset} on {date}'.format(user=self.user, asset=self.asset, date=self.signal_datetime)
    signal_datetime = models.DateTimeField(default=datetime.now, verbose_name=_('تاریخ و زمان'))
    result_datetime = models.DateTimeField(default=datetime.now, verbose_name=_('تاریخ و زمان پایان معامله'))
    canceled_datetime = models.DateTimeField(verbose_name=_('تاریخ و زمان لغو معامله'), null=True, blank=True)
    user = models.ForeignKey(User, related_name='signals', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('کاربر'))
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='signals', verbose_name=_('دارایی'))
    trade_id = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('شناسه Trade'), help_text=_('مشخصه‌ای که با آن بتوان معامله را در پلتفرم‌های معاملاتی پیدا کرد'))
    entry_type = models.CharField(max_length=4, choices=TradeType.choices, default=TradeType.BUY, verbose_name=_('نوع معامله'))
    entry_point1 = models.DecimalField(max_digits=11, decimal_places=4, verbose_name=_('نقطه ورود اول'))
    entry_point2 = models.DecimalField(max_digits=11, decimal_places=4, verbose_name=_('نقطه ورود دوم'), null=True, blank=True)
    stop_loss1 = models.DecimalField(max_digits=11, decimal_places=4, verbose_name=_('حد ضرر اول'))
    stop_loss2 = models.DecimalField(max_digits=11, decimal_places=4, verbose_name=_('حد ضرر دوم'), null=True, blank=True)
    take_profit1 = models.DecimalField(max_digits=11, decimal_places=4, verbose_name=_('حد سود اول'))
    take_profit2 = models.DecimalField(max_digits=11, decimal_places=4, verbose_name=_('حد سود دوم'), null=True, blank=True)
    take_profit3 = models.DecimalField(max_digits=11, decimal_places=4, verbose_name=_('حد سود سوم'), null=True, blank=True)
    risk_reward = models.DecimalField(max_digits=4, decimal_places=2, verbose_name=_('نسبت سود به ضرر'))
    result_pip = models.SmallIntegerField(default=0, verbose_name=_('سود/ضرر نهایی (پیپ)'))
    result_dollar = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name=_('سود/ضرر نهایی (دلار)'))
    lot = models.DecimalField(max_digits=4, decimal_places=2, verbose_name=_('حجم ورود'), null=True, blank=True)
    mistakes = models.TextField(null=True, blank=True, verbose_name=_('اشتباهات معامله'))
    pta_analysis = models.OneToOneField(PTAAnalysis, on_delete=models.SET_NULL, related_name='signal', null=True, blank=True, verbose_name=_('تحلیل PTA'))
    classic_analysis = models.OneToOneField(ClassicAnalysis, on_delete=models.SET_NULL, related_name='signal', null=True, blank=True, verbose_name=_('تحلیل Classic'))
    status = models.CharField(max_length=8, choices=SignalStatus.choices, default=SignalStatus.RUNNING, verbose_name=_('وضعیت'))
    result_image_url = models.URLField(max_length=300, null=True, blank=True, verbose_name=_('تصویر نهایی'))
    comments = GenericRelation(Comment, verbose_name=_('نظرات'))

   