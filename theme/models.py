from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from blog import models as blog_models
from file import models as file_models
from theme.fields import ColorField

# Create your models here.

class SiteSetting(models.Model):
    class Meta:
        verbose_name = _('تنظیمات سایت')
        verbose_name_plural = _('تنظیمات سایت')
    def __str__(self):
        return _('تنظیمات سایت')
    site_title = models.CharField(max_length=200, verbose_name=_('عنوان سایت'), default='TeamChe')
    site_subtitle = models.CharField(max_length=500, verbose_name=_('زیرعنوان سایت'), default='Team Management System')
    home_page = models.CharField(max_length=100, verbose_name=_('صفحه اصلی سایت'), null=True, blank=True)
    
    primary_light_color = ColorField(null=True, blank=True, verbose_name=_('رنگ اصلی'))
    primary_bold_color = ColorField(null=True, blank=True, verbose_name=_('رنگ اصلی پررنگ'))
    primary_dark_color = ColorField(null=True, blank=True, verbose_name=_('رنگ اصلی تیره'))
    accend_light_color = ColorField(null=True, blank=True, verbose_name=_('رنگ فرعی'))
    accend_bold_color = ColorField(null=True, blank=True, verbose_name=_('رنگ فرعی پررنگ'))
    accend_dark_color = ColorField(null=True, blank=True, verbose_name=_('رنگ فرعی تیره'))


class Theme(models.Model):
    class Meta:
        verbose_name = _('پوسته')
        verbose_name_plural = _('پوسته‌ها')

    def __str__(self):
        return self.name
    name = models.CharField(max_length=100, verbose_name=_('نام'))
    website = models.URLField(verbose_name=_('سایت'), null=True, blank=True)
    author_name = models.CharField(
        max_length=200, verbose_name=_('توسعه دهنده'))
    author_email = models.EmailField(verbose_name=_(
        'ایمیل توسعه دهنده'), null=True, blank=True)
    desc = models.CharField(max_length=500, null=True,
                            blank=True, verbose_name=_('توضیحات'))
    image = models.CharField(null=True, blank=True,
                             max_length=50, verbose_name=_('تصویر'))
    is_active = models.BooleanField(default=False, verbose_name=_('فعال'))


class ThemePage(models.Model):
    class Meta:
        verbose_name = _('صفحه پوسته')
        verbose_name_plural = _('صفحات پوسته')

    def __str__(self):
        return '{theme}: {page}'.format(theme=self.theme, page=self.page_name)
    page_types = [('base', _('پایه')), ('blog', _('بلاگ')), ('post', _(
        'پست')), ('search', _('جستجو')), ('cat', _('دسته‌بندی')), ('custom', _('سفارشی'))]
    theme = models.ForeignKey(
        Theme, on_delete=models.CASCADE, related_name='pages', verbose_name=_('پوسته'))
    page_name = models.CharField(max_length=50, verbose_name=_('نام صفحه'))
    file_name = models.CharField(
        max_length=100, verbose_name=_('نام فایل صفحه'))
    page_type = models.CharField(
        max_length=50, choices=page_types, verbose_name=_('نوع صفحه'))

class Menu(models.Model):
    class Meta:
        verbose_name = _('منو')
        verbose_name_plural = _('منوها')

    def __str__(self):
        return self.name
    name = models.CharField(max_length=100, verbose_name=_('نام منو'))

class MenuItem(models.Model):
    class Meta:
        verbose_name = _('آیتم منو')
        verbose_name_plural = _('آیتم‌های منو')

    def __str__(self):
        return '{url}'.format(menu=self.menu, url=self.url)
    menu = models.ForeignKey(
        Menu, on_delete=models.CASCADE, related_name='items', verbose_name=_('منو'))
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               related_name='subitems', verbose_name=_('آیتم والد'))
    url = models.CharField(max_length=50, verbose_name=_('آدرس'))
    order = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('موقعیت'))

class MenuItemContent(models.Model):
    class Meta:
        verbose_name = _('محتوای آیتم')
        verbose_name_plural = _('محتواهای آیتم')

    def __str__(self):
        return '{0}'.format(self.title)

    menu_item = models.ForeignKey(
        MenuItem, on_delete=models.CASCADE, related_name='contents', verbose_name=_('آیتم منو'))
    language = models.CharField(
        max_length=10, choices=settings.LANGUAGES, verbose_name=_('زبان'))
    title = models.CharField(max_length=50, verbose_name=_('عنوان'))
    # image = models.ImageField(upload_to='theme/menu/contents', max_length=100, verbose_name=_('تصویر'), null=True, blank=True)
    desc = models.CharField(max_length=200, null=True,
                            blank=True, verbose_name=_('توضیحات'))

class Page(models.Model):
    # TODO: Need improvement
    class Meta:
        verbose_name = _('صفحه')
        verbose_name_plural = _('صفحات')

    def __str__(self):
        return '{0}: {1}'.format(self.slug, self.theme_page)
    theme_page = models.ForeignKey(ThemePage, on_delete=models.SET_NULL,limit_choices_to={'theme__is_active': True},
                                   related_name='pages', verbose_name=_('صفحه پوسته'), null=True, blank=True)
    slug = models.SlugField(verbose_name=_(
        'نشانی (slug)'), null=True, blank=True)
    page_type = models.CharField(max_length=10, choices=[('system', _(
        'سیستمی')), ('custom', _('شخصی'))], verbose_name=_('نوع صفحه'), default='custom')
    base = models.ForeignKey('self', related_name='base_page', limit_choices_to={'theme_page__theme__is_active': True},
                             on_delete=models.SET_NULL, null=True, blank=True)
    post = models.ForeignKey(blog_models.Post, on_delete=models.CASCADE, related_name='pages', null=True, blank=True, verbose_name=_('پست'))

class PageText(models.Model):
    class Meta:
        verbose_name = _('متغیر متن صفحه')
        verbose_name_plural = _('متغیرهای متن صفحه')

    def __str__(self):
        return '{0}.{1}'.format(self.page, self.variable)
    page = models.ForeignKey(Page, on_delete=models.CASCADE,
                             related_name='page_texts', verbose_name=_('صفحه'))
    variable = models.CharField(max_length=100, verbose_name=_('نام متغیر'))

class PageTextContent(models.Model):
    class Meta:
        verbose_name = _('محتوای متغیر متن')
        verbose_name_plural = _('محتوای متغیرهای متن')

    def __str__(self):
        return '{0}({1}): {2}'.format(self.page_text, self.language, self.text_value[:50])
    page_text = models.ForeignKey(
        PageText, on_delete=models.CASCADE, related_name='contents', verbose_name=_('متغیر متنی'))
    text_value = models.CharField(
        max_length=500, verbose_name=_('محتوای متنی'), null=True, blank=True)
    language = models.CharField(
        max_length=10, choices=settings.LANGUAGES, verbose_name=_('زبان'))

class PageLink(models.Model):
    class Meta:
        verbose_name = _('متغیر لینک صفحه')
        verbose_name_plural = _('متغیرهای لینک صفحه')

    def __str__(self):
        return '{0}.{1}'.format(self.page, self.link_variable)
    page = models.ForeignKey(Page, on_delete=models.CASCADE,
                             related_name='page_links', verbose_name=_('صفحه'))
    link_variable = models.CharField(
        max_length=100, verbose_name=_('نام متغیر'))

class PageLinkContent(models.Model):
    class Meta:
        verbose_name = _('محتوای متغیر لینک')
        verbose_name_plural = _('محتوای متغیرهای لینک')

    def __str__(self):
        return '{0}({1}): {2}'.format(self.page_link, self.language, self.link_value[:50])
    page_link = models.ForeignKey(
        PageLink, on_delete=models.CASCADE, related_name='contents', verbose_name=_('متغیر لینک'))
    link_value = models.CharField(
        max_length=500, verbose_name=_('محتوای لینک'), null=True, blank=True)
    language = models.CharField(
        max_length=10, choices=settings.LANGUAGES, verbose_name=_('زبان'))

class PageImage(models.Model):
    class Meta:
        verbose_name = _('متغیر تصویر صفحه')
        verbose_name_plural = _('متغیر‌های تصویر صفحه')

    def __str__(self):
        return '{page}: {var}'.format(page=self.page, var=self.image_variable)
    page = models.ForeignKey(Page, on_delete=models.CASCADE,
                             related_name='page_images', verbose_name=_('صفحه'))
    image_variable = models.CharField(
        max_length=100, verbose_name=_('نام متغیر'))

class PageImageContent(models.Model):
    class Meta:
        verbose_name = _('محتوای متغیر تصویر')
        verbose_name_plural = _('محتوا‌های متغیر تصویر')

    def __str__(self):
        return '{var}: {val} {lang}'.format(var=self.page_image, val=self.image_value, lang=self.language)
    page_image = models.ForeignKey(
        PageImage, on_delete=models.CASCADE, related_name='page_images', verbose_name=_('متغیر تصویر'))
    image_value = models.ForeignKey(file_models.File, on_delete=models.CASCADE,
                                    related_name='image_values', verbose_name=_('تصویر'), null=True, blank=True)
    language = models.CharField(
        max_length=10, choices=settings.LANGUAGES, verbose_name=_('زبان'))

class PagePost(models.Model):
    class Meta:
        verbose_name = _('متغیر پست صفحه')
        verbose_name_plural = _('متغیرهای پست صفحه')

    def __str__(self):
        return '{0}.{1}'.format(self.page, self.post_variable)
    page = models.ForeignKey(Page, on_delete=models.CASCADE,
                             related_name='page_posts', verbose_name=_('صفحه'))
    post_variable = models.CharField(
        max_length=100, verbose_name=_('نام متغیر پست'))

class PagePostContent(models.Model):
    class Meta:
        verbose_name = _('محتوای متغیر پست')
        verbose_name_plural = _('محتوای متغیرهای پست')

    def __str__(self):
        return '{0}({1}): {2}'.format(self.page_post, self.language, self.post_content)
    page_post = models.ForeignKey(
        PagePost, on_delete=models.CASCADE, related_name='contents', verbose_name=_('متغیر پست'))
    post_content = models.ForeignKey(
        blog_models.Post, on_delete=models.CASCADE, verbose_name=_('پست'), null=True, blank=True,)
    language = models.CharField(
        max_length=10, choices=settings.LANGUAGES, verbose_name=_('زبان'))

class PageCategory(models.Model):
    class Meta:
        verbose_name = _('متغیر دسته‌بندی صفحه')
        verbose_name_plural = _('متغیرهای دسته‌بندی صفحه')

    def __str__(self):
        return '{0}.{1}'.format(self.page, self.category_variable)
    page = models.ForeignKey(Page, on_delete=models.CASCADE,
                             related_name='page_categories', verbose_name=_('صفحه'))
    category_variable = models.CharField(
        max_length=100, verbose_name=_('نام متغیر دسته‌بندی'))
    count = models.PositiveSmallIntegerField(
        default=10, verbose_name=_('تعداد پست'))

class PageCategoryContent(models.Model):
    class Meta:
        verbose_name = _('محتوای متغیر دسته‌بندی')
        verbose_name_plural = _('محتوای متغیرهای دسته‌بندی')

    def __str__(self):
        return '{0}({1}): {2}'.format(self.page_category, self.language, self.category_content)
    page_category = models.ForeignKey(
        PageCategory, on_delete=models.CASCADE, related_name='contents', verbose_name=_('متغیر دسته‌بندی'))
    category_content = models.ForeignKey(
        blog_models.Category, on_delete=models.CASCADE, verbose_name=_('دسته‌بندی'), null=True, blank=True,)
    language = models.CharField(
        max_length=10, choices=settings.LANGUAGES, verbose_name=_('زبان'))

class PageMenu(models.Model):
    class Meta:
        verbose_name = _('متغیر منو صفحه')
        verbose_name_plural = _('متغیرهای منو صفحه')

    def __str__(self):
        return '{0} - {1}'.format(self.page, self.menu_variable)
    page = models.ForeignKey(
        Page, on_delete=models.CASCADE, related_name='menus', verbose_name=_('صفحه'))
    menu_variable = models.CharField(
        max_length=50, verbose_name=_('متغیر منو'))

class PageMenuContent(models.Model):
    class Meta:
        verbose_name = _('محتوای متغیر منو')
        verbose_name_plural = _('محتوای متغیرهای منو')

    def __str__(self):
        return '{0} {1}({2})'.format(self.page_menu, self.menu_content, self.language)
    page_menu = models.ForeignKey(
        PageMenu, on_delete=models.CASCADE, related_name='menu_contents', verbose_name=_('متغیر منو'))
    menu_content = models.ForeignKey(
        Menu, on_delete=models.CASCADE, verbose_name=_('منو'), null=True, blank=True)
    language = models.CharField(
        max_length=10, choices=settings.LANGUAGES, verbose_name=_('زبان'))

