from django.contrib import admin
from .models import Page, PageText, PageTextContent
from .models import Theme, ThemePage, PageCategory, PageCategoryContent
from .models import PageMenu, PageMenuContent, Menu, MenuItem, MenuItemContent
from .models import PagePost, PagePostContent, PageImage, PageImageContent
from .models import PageLink, PageLinkContent
from .models import SiteSetting

# Register your models here.
admin.site.register(SiteSetting)
admin.site.register(Theme)
admin.site.register(ThemePage)
admin.site.register(Page)
admin.site.register(PageText)
admin.site.register(PageTextContent)
admin.site.register(PageLink)
admin.site.register(PageLinkContent)
admin.site.register(PageImage)
admin.site.register(PageImageContent)
admin.site.register(PageCategory)
admin.site.register(PageCategoryContent)
admin.site.register(PageMenu)
admin.site.register(PageMenuContent)
admin.site.register(PagePost)
admin.site.register(PagePostContent)
admin.site.register(Menu)
admin.site.register(MenuItem)
admin.site.register(MenuItemContent)