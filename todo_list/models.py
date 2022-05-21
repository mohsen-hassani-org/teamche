from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class TodoListManager(models.Manager):
    def get_today(self, user):
        today = datetime.now()
        return self.get_or_create(user=user, date=today)

    def get_todo_list(self, user, date):
        return self.filter(user=user, date=date)

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
    desc = models.TextField(verbose_name='توضیحات')
    status = models.IntegerField(verbose_name='وضعیت', choices=Statuses.choices,
                                 default=Statuses.PENDING)
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

    def undone_task(self, commit=True):
        self.end_datetime = datetime.now()
        self.status = self.Statuses.NOT_DONE
        if commit:
            self.save()


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

    def start_task(self, commit=True):
        self.start_datetime = datetime.now()
        if commit:
            self.save()

    def finish_task(self, commit=True):
        self.end_datetime = datetime.now()
        if commit:
            self.save()