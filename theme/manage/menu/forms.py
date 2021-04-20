from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import get_language
from theme.models import Menu, MenuItem, MenuItemContent

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ('name', )

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ('url', 'parent', )

class MenuItemReorderForm(forms.Form):
    position = forms.ChoiceField(label=_('انتقال به'),choices=[])
    def __init__(self, *args, **kwargs):
        menu_item = kwargs.pop('menu_item')
        super(MenuItemReorderForm, self).__init__(*args, **kwargs)
        menus = MenuItem.objects.filter(menu=menu_item.menu, parent=menu_item.parent).exclude(id=menu_item.id)
        lang = get_language()
        items = [(menu.id, menu.contents.filter(language=lang).first() or menu.url) for menu in menus]
        self.fields['position'].choices = items


class MenuItemContentForm(forms.ModelForm):
    class Meta:
        model = MenuItemContent
        fields = ('title', 'language')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['language'].disabled = True