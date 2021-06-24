import random
from django.contrib.auth.models import User
from django.db.models import Sum, Count


def single_dataset_chart(qs, x_data_field, y_data_field, chart_type, operation, sum_results=False):
    ''' Chart generator for datasets that contain seprated values '''
    DATASET = qs
    X_DATA_FIELD = x_data_field
    Y_DATA_FIELD = y_data_field
    X_DATA_VALUES = [item[X_DATA_FIELD] for item in DATASET.order_by(X_DATA_FIELD).values(X_DATA_FIELD).distinct()]
    OPERATION = operation
    SUM_RESULTS = sum_results
    dataset = {}
    dataset['label'] = 'Data'
    dataset['data'] = []
    prev_res = 0
    for obj in X_DATA_VALUES:
        filter_key = {X_DATA_FIELD:obj}
        data = DATASET.filter(**filter_key).aggregate(res=OPERATION(Y_DATA_FIELD))
        data = data.get('res', 0)
        data = prev_res + data if SUM_RESULTS else data
        prev_res = data
        dataset['data'].append(data)
    if chart_type == 'pie':
        dataset['color'] = [random_color() for color in range(len(X_DATA_VALUES))]
    else:
        dataset['color'] = [random_color()]
    return {'labels':X_DATA_VALUES,'datasets': [dataset], 'type': chart_type}


def multi_dataset_chart(qs, x_data_field, y_data_field, dataset_field, chart_type, operation, sum_results=False):
    ''' Chart generator for datasets that contain seprated values '''
    DATASET = qs
    X_DATA_FIELD = x_data_field
    Y_DATA_FIELD = y_data_field
    X_DATA_VALUES = [item[X_DATA_FIELD] for item in DATASET.order_by(X_DATA_FIELD).values(X_DATA_FIELD).distinct()]
    OPERATION = operation
    DATASET_FIELD = dataset_field
    DATASET_VALUES = [item[DATASET_FIELD] for item in DATASET.order_by(DATASET_FIELD).values(DATASET_FIELD).distinct()]
    SUM_RESULTS = sum_results

    datasets = []
    for obj in X_DATA_VALUES:
        object_data = []
        for dataset_obj in DATASET_VALUES:
            filter_key = {X_DATA_FIELD:obj, DATASET_FIELD: dataset_obj}
            data = DATASET.filter(**filter_key).aggregate(res=OPERATION(Y_DATA_FIELD))
            data = data.get('res', 0)
            data = prev_res + data if SUM_RESULTS else data
            prev_res = data
            object_data.append(data)
        if chart_type == 'pie':
            color = [random_color() for color in range(len(X_DATA_VALUES))]
        else:
            color = [random_color()]
        datasets.append({'label': obj, 'data': object_data, 'color': color})

    return {
        'labels': DATASET_VALUES,
        'datasets': datasets,
        'type': chart_type,
    }













def random_color():
    r = random.choice(range(256))
    g = random.choice(range(256))
    b = random.choice(range(256))
    return f'rgba({r}, {g}, {b}, 0.7)'

