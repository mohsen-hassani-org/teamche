from datetime import datetime
from jalali_date import date2jalali


def dmo_days_to_data(dmo):
    dmo_days = dmo.days.all().order_by('day')
    procedure = 0
    step = 0
    data = {}
    for dmo_day in dmo_days:
        procedure = procedure + 1 if dmo_day.done else procedure - 1
        step += 1
        if  step == 1 and procedure == -1:
            procedure = 0
        data[dmo_day.day] = procedure
    return data

def month_num_to_str(month):
    if month == 1:
        return 'فروردین'
    if month == 2:
        return 'اردیبهشت'
    if month == 3:
        return 'خرداد'
    if month == 4:
        return 'تیر'
    if month == 5:
        return 'مرداد'
    if month == 6:
        return 'شهریور'
    if month == 7:
        return 'مهر'
    if month == 8:
        return 'آبان'
    if month == 9:
        return 'آذر'
    if month == 10:
        return 'دی'
    if month == 11:
        return 'بهمن'
    if month == 12:
        return 'اسفند'

def dmo_to_chart(dmo):
    pass

def dmo_to_table(dmo_data):
    table = []
    jnow = date2jalali(datetime.now())
    days = jalali_month_length(jnow)
    for i in range(days):
        obj = {}
        for j in range(days):
            # value only apples to row 31 and 32 and should display day num
            value = str(j + 1) if i == days - 1 else ''

            # cell class seprate empty cells which should not display with
            # normal cell which is empty but should be displayed
            cell_class = 'emp' if j < days - i - 1 else 'day'

            obj[j] = {'class': cell_class, 'value': value} 
        table.append(obj)

    for i in range(days):
        obj = {}
        for j in range(days):
            # value only apples to row 31 and 32 and should display day num
            value = str(j + 1) if i == 0 else ''

            # cell class seprate empty cells which should not display with
            # normal cell which is empty but should be displayed
            cell_class = 'emp' if j < i else 'day'

            obj[j] = {'class': cell_class, 'value': value}
        table.append(obj)


    # Append user_data to table
    for item in dmo_data.keys():
        value = dmo_data[item]
        # items are j-indexs or columns and values are i-indexs or rows
        # values should combine with days variable (some values are negetive)
        row_index = days - value
        column_index = item - 1
        
        # this is the row of table that should edit
        row = table[row_index]
        # this is the cell of table that should edit
        cell = row[column_index]
        cell['class'] += ' green'
    return table

def jalali_month_length(date):
    """Number of days in the month of given date.
    :return: number of days in month
    :rtype: int
    """
    if date.month <= 6:
        return 31
    if date.month <= 11:
        return 30
    if date.isleap():
        return 30
    return 29

def dmo_last_days(dmo):
    dmo_data = dmo_days_to_data(dmo)
    jnow = date2jalali(datetime.now())
    today = jnow.day
    classes = []
    tmp = 0
    table = '<table class="dmo_summary"><tr>'
    for i in range(1, today + 1):
        if i in dmo_data.keys():
            if dmo_data[i] > tmp:
                classes.append({'day': i, 'color': 'green'})
            else:
                classes.append({'day': i, 'color': 'red'})
            tmp = dmo_data[i]
        else:
            classes.append({'day': i, 'color': 'gray'})
    classes = classes[-10:]
    for klass in classes:
        table += '<td class="{color}">{day}</td>'.format(color=klass['color'], day=klass['day'])
    table += '</tr></table>'
    return table
