from datetime import datetime, timedelta
from functools import reduce
from django import db
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.contrib.auth import get_user_model
from jalali_date import date2jalali
from dmo.models import DmoDay, Dmo


User = get_user_model()


class TodoListManager(models.Manager):
    def get_todo_list(self, user, date):
        todo_list, _ = self.get_or_create(user=user, date=date)
        self._attach_dmo_items(todo_list)
        return todo_list

    def _attach_dmo_items(self, todo_list):
        date = date2jalali(todo_list.date)
        user_dmos = Dmo.objects.filter(user=todo_list.user, year=date.year, month=date.month)
        for dmo in user_dmos:
            if todo_list.items.filter(title=dmo.goal).exists():
                continue
            todo_list.items.create(title=dmo.goal)


    def move_lists_to_today(self):
        today = datetime.now()
        self.update(date=today)

    def move_lists_to_date(self, date):
        self.update(date=date)
        

class TodoListItemManager(models.Manager):
    def move_tasks_to_today_list(self):
        users = self.values('todo_list__user')
        if len(users) > 1:
            raise Exception('Multiple users found.')
        user = users[0]['todo_list__user']
        today_list = TodoList.objects.get_today(user)
        self.update(todo_list=today_list)

    def add_item(self, title, desc, user, date=None, stauts=None):
        if not date:
            date = datetime.now()
        if not status:
            status = TodoList.Statuses.PENDING
        todo_list = TodoList.objects.get_todo_list(user, date)
        self.create(todo_list=todo_list, title=title, desceription=desc, status=status)
        


class TodoList(models.Model):
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر',
                             related_name='todo_lists')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخرین ویرایش')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده در')
    objects = TodoListManager()

    class Meta:
        verbose_name = 'Todo لیست'
        verbose_name_plural = 'Todo لیست'
        unique_together = ('date', 'user', )

    def __str__(self):
        return f'{self.user} - {self.date}'

    def move_list_to_date(self, to_date, commit=True):
        self.date = to_date
        if commit:
            self.save()

    
    
class TodoListItem(models.Model):

    class Statuses(models.IntegerChoices):
        PENDING = 0, 'در انتظار انجام'
        DONE = 100, 'انجام شد'
        NOT_DONE = 200, 'انجام نشد'

    todo_list = models.ForeignKey(TodoList, verbose_name='Todo', related_name='items',
                                  on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='عنوان')
    desc = models.TextField(verbose_name='توضیحات', blank=True)
    status = models.IntegerField(verbose_name='وضعیت', choices=Statuses.choices,
                                 default=Statuses.PENDING)
    dmo_day = models.OneToOneField(DmoDay, on_delete=models.CASCADE, verbose_name='دمو',
                                   related_name='todo_list_item', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخرین ویرایش')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده در')
    objects = TodoListItemManager()

    class Meta:
        verbose_name = 'آیتم Todo لیست'
        verbose_name_plural = 'آیتم Todo لیست'

    def __str__(self):
        return self.title

    def change_status(self, status: Statuses, commit=True):
        self.status = status
        if commit:
            self.save()

    def done_task(self, commit=True):
        self.status = self.Statuses.DONE
        jalali_date = date2jalali(self.todo_list.date)
        dmo = Dmo.objects.filter(user=self.todo_list.user, goal=self.title,
                                 year=jalali_date.year, month=jalali_date.month
                                ).first()
        if dmo:
            dmo.complete(jalali_date.day, done=True)
        if commit:
            self.save()
            
    def undone_task(self, commit=True):
        self.end_datetime = datetime.now()
        self.status = self.Statuses.NOT_DONE
        jalali_date = date2jalali(self.todo_list.date)
        dmo = Dmo.objects.filter(user=self.todo_list.user, goal=self.title,
                                 year=jalali_date.year, month=jalali_date.month
                                ).first()
        if dmo:
            dmo.complete(jalali_date.day, done=False)
        if commit:
            self.save()

    def start_task(self):
        if self.time_tracks.filter(end_datetime__isnull=True).exists():
            raise Exception('Task is already started.')
        TodoListItemTimeTrack.objects.create(
            item=self,
            start_datetime=datetime.now(),
            end_datetime=None
        )

    def finish_task(self):
        now = datetime.now()
        self.time_tracks.filter(end_datetime=None).update(end_datetime=now)

    def toggle_start_stop(self):
        started_tracks = self.time_tracks.filter(end_datetime__isnull=True)
        if started_tracks.exists():
            started_tracks.update(end_datetime=datetime.now())
            return
        TodoListItemTimeTrack.objects.create(
            item=self,
            start_datetime=datetime.now(),
            end_datetime=None
        )

    def get_total_time_seconds(self):
        # db aggrigation doesn't work for some databases, so it's safer to use python
        time_tracks = self.time_tracks.filter(end_datetime__isnull=False).values('start_datetime', 'end_datetime')
        durations = [time['end_datetime'] - time['start_datetime'] for time in time_tracks]
        return reduce(lambda a, b: a+b, durations, timedelta(seconds=0)).seconds

    def get_last_ongoing_time_track(self):
        return self.time_tracks.filter(end_datetime__isnull=True).last()



class TodoListItemTimeTrack(models.Model):
    item = models.ForeignKey(TodoListItem, on_delete=models.CASCADE, verbose_name='آیتم',
                             related_name='time_tracks')
    start_datetime = models.DateTimeField(verbose_name='شروع', null=True, blank=True)
    end_datetime = models.DateTimeField(verbose_name='پایان', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخرین ویرایش')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده در')

    class Meta:
        verbose_name = 'Todo لیست زمان'
        verbose_name_plural = 'Todo لیست زمان'

    def __str__(self):
        return f'{self.item}'
