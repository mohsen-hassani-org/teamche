from django_filters import FilterSet
from cfd.models import PTAAnalysis, Signal, ClassicAnalysis

class SignalFilter(FilterSet):
    class Meta:
        model = Signal
        fields = {
            'signal_datetime': ['lt', 'gt'],
            'result_datetime': ['lt', 'gt'],
            'user': ['exact'],
            'asset': ['exact'],
        }

class ClassicAnalysisFilter(FilterSet):
    class Meta:
        model = ClassicAnalysis
        fields = {
            'title': ['icontains'],
            'user': ['exact'],
        }


class PTAAnalysisFilter(FilterSet):
    class Meta:
        model = PTAAnalysis
        fields = {
            'user': ['exact'],
            'any_news': ['exact'],
            'chart_move': ['exact'],
            'impulsive_direction': ['exact'],
            'pattern': ['exact'],
            'candle_pressure': ['exact'],
            'scenario': ['exact'],
            'entrance': ['exact'],
            'datetime': ['lt', 'gt'],
        }
