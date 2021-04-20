from cfd.models import ClassicAnalysis

def classic_analysis_signal_count(analysis):
    if not analysis:
        return None
    nature = 0
    sell = 0
    buy = 0

    # Major
    if analysis.major_trend_signal == ClassicAnalysis.SignalTypes.BUY:
        buy += 1
    elif analysis.major_trend_signal == ClassicAnalysis.SignalTypes.SELL:
        sell += 1
    else:
        nature += 1

    # Intermediate
    if analysis.intermediate_trend_signal == ClassicAnalysis.SignalTypes.BUY:
        buy += 1
    elif analysis.intermediate_trend_signal == ClassicAnalysis.SignalTypes.SELL:
        sell += 1
    else:
        nature += 1
    
    # Pattern
    if analysis.pattern_signal == ClassicAnalysis.SignalTypes.BUY:
        buy += 1
    elif analysis.pattern_signal == ClassicAnalysis.SignalTypes.SELL:
        sell += 1
    else:
        nature += 1

    # Moving
    if analysis.moving_signal == ClassicAnalysis.SignalTypes.BUY:
        buy += 1
    elif analysis.moving_signal == ClassicAnalysis.SignalTypes.SELL:
        sell += 1
    else:
        nature += 1

    # pivot
    if analysis.pivot_signal == ClassicAnalysis.SignalTypes.BUY:
        buy += 1
    elif analysis.pivot_signal == ClassicAnalysis.SignalTypes.SELL:
        sell += 1
    else:
        nature += 1

    # fibo
    if analysis.fibo_signal == ClassicAnalysis.SignalTypes.BUY:
        buy += 1
    elif analysis.fibo_signal == ClassicAnalysis.SignalTypes.SELL:
        sell += 1
    else:
        nature += 1

    # time_divergent 
    if analysis.time_divergent_signal == ClassicAnalysis.SignalTypes.BUY:
        buy += 1
    elif analysis.time_divergent_signal == ClassicAnalysis.SignalTypes.SELL:
        sell += 1
    else:
        nature += 1

    # eliot 
    if analysis.eliot_signal == ClassicAnalysis.SignalTypes.BUY:
        buy += 1
    elif analysis.eliot_signal == ClassicAnalysis.SignalTypes.SELL:
        sell += 1
    else:
        nature += 1

    # candle
    if analysis.candle_signal == ClassicAnalysis.SignalTypes.BUY:
        buy += 1
    elif analysis.candle_signal == ClassicAnalysis.SignalTypes.SELL:
        sell += 1
    else:
        nature += 1

    # rsi
    if analysis.rsi_signal == ClassicAnalysis.SignalTypes.BUY:
        buy += 1
    elif analysis.rsi_signal == ClassicAnalysis.SignalTypes.SELL:
        sell += 1
    else:
        nature += 1

    # momentum
    if analysis.momentum_signal == ClassicAnalysis.SignalTypes.BUY:
        buy += 1
    elif analysis.momentum_signal == ClassicAnalysis.SignalTypes.SELL:
        sell += 1
    else:
        nature += 1

    # macd
    if analysis.macd_signal == ClassicAnalysis.SignalTypes.BUY:
        buy += 1
    elif analysis.macd_signal == ClassicAnalysis.SignalTypes.SELL:
        sell += 1
    else:
        nature += 1

    # stochastic
    if analysis.stochastic_signal == ClassicAnalysis.SignalTypes.BUY:
        buy += 1
    elif analysis.stochastic_signal == ClassicAnalysis.SignalTypes.SELL:
        sell += 1
    else:
        nature += 1

    # atr
    if analysis.atr_signal == ClassicAnalysis.SignalTypes.BUY:
        buy += 1
    elif analysis.atr_signal == ClassicAnalysis.SignalTypes.SELL:
        sell += 1
    else:
        nature += 1

    # atx
    if analysis.atx_signal == ClassicAnalysis.SignalTypes.BUY:
        buy += 1
    elif analysis.atx_signal == ClassicAnalysis.SignalTypes.SELL:
        sell += 1
    else:
        nature += 1

    return {
        'buy': buy,
        'sell': sell,
        'nature': nature,
    }
