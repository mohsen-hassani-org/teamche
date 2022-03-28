from django.contrib.auth import get_user_model
from django_filters import FilterSet, ModelChoiceFilter
from cfd.models import PTAAnalysis, Signal, ClassicAnalysis
User = get_user_model()

class SignalFilter(FilterSet):
    class Meta:
        model = Signal
        fields = {
            'signal_datetime': ['lt', 'gt'],
            'result_datetime': ['lt', 'gt'],
            'user': ['exact'],
            'asset': ['exact'],
            'signal_type': ['exact'],
        }

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None, team_id=None):
        super().__init__(data, queryset, request=request, prefix=prefix)
        self.form.fields['user'].queryset = User.objects.filter(teams__id=team_id)

class ClassicAnalysisFilter(FilterSet):
    class Meta:
        model = ClassicAnalysis
        fields = {
            'title': ['icontains'],
            'user': ['exact'],
        }

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None, team_id=None):
        super().__init__(data, queryset, request=request, prefix=prefix)
        self.form.fields['user'].queryset = User.objects.filter(teams__id=team_id)


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

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None, team_id=None):
        super().__init__(data, queryset, request=request, prefix=prefix)
        self.form.fields['user'].queryset = User.objects.filter(teams__id=team_id)
