from django.shortcuts import redirect, render, get_object_or_404
from django.http import Http404
from django.forms import modelformset_factory
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from theme.manage.page.forms import PageTextContentNoLanguageForm, PageTextContentSingleLanguageForm
from theme.manage.page.forms import PageImageContentNoLanguageForm, PageImageContentSingleLanguageForm
from theme.manage.page.forms import PageLinkContentNoLanguageForm, PageLinkContentSingleLanguageForm
from theme.manage.page.forms import PageMenuContentNoLanguageForm, PageMenuContentSingleLanguageForm
from theme.manage.page.forms import PageCatContentNoLanguageForm, PageCatContentSingleLanguageForm
from theme.models import Page, Theme, ThemePage
from theme.models import PageCategory, PageImage, PageLink, PageMenu, PagePost, PageText
from theme.models import PageCategoryContent, PageImageContent, PageLinkContent, PageMenuContent, PagePostContent, PageTextContent
from theme.gvars import GENERIC_MODEL_FORM, GENERIC_MODEL_LIST

def theme_pages(request, theme_id):
    theme = get_object_or_404(Theme, id=theme_id)
    pages = Page.objects.filter(theme_page__theme=theme, page_type='system')
    context = {
        'page_title': _('صفحات پوسته'),
        'page_subtitle': theme.name,
        'items': pages,
        'fields': ['slug', 'theme_page', 'base',],
        'headers': [_('اسلاگ'), _('قالب صفحه'), _('صفحه پایه')],
        'action_buttons': [
            {
                'title': _('متن‌ها'),
                'url_name': 'theme_manage_pagetextvars_list',
                'arg1_field': 'id',
            },
            {
                'title': _('تصاویر'),
                'url_name': 'theme_manage_pageimagevars_list',
                'arg1_field': 'id',
            },
            {
                'title': _('لینک‌ها'),
                'url_name': 'theme_manage_pagelinkvars_list',
                'arg1_field': 'id',
            },
            {
                'title': _('منوها'),
                'url_name': 'theme_manage_pagemenuvars_list',
                'arg1_field': 'id',
            },
            {
                'title': _('دسته‌بندی‌ها'),
                'url_name': 'theme_manage_pagecatvars_list',
                'arg1_field': 'id',
            },
        ],
        'footer_buttons': [
            {
                'title': _('بازگشت'),
                'url_name': 'theme_manage_theme_list',
            }
        ]
    }
    return render(request, GENERIC_MODEL_LIST, context)




def page_textvars_list(request, page_id):
    page = get_object_or_404(Page, id=page_id)
    text_vars = page.page_texts.all()
    items = []
    for var in text_vars:
        obj = {}
        obj['id'] = var.id
        obj['var_name'] = var.variable
        for lang in settings.LANGUAGES:
            content, created = PageTextContent.objects.get_or_create(language=lang[0], page_text=var)
            obj['{lang}'.format(lang=lang[0])] = content.text_value
        items.append(obj)
    fields = ['var_name']
    fields += [lang[0] for lang in settings.LANGUAGES]
    headers = [_('نام متغیر')]
    headers += [lang[0] for lang in settings.LANGUAGES]
    context = {
        'items': items,
        'fields': fields,
        'headers': headers,
        'page_title': _('متغیرهای متن صفحه'),
        'page_subtitle': page.slug,
        'action_buttons': [
            {
                'title': _('ویرایش محتوای هر زبان'),
                'url_name': 'theme_manage_pagetextvars_contentedit_each',
                'arg1_field': 'id'
            },
            {
                'title': _('ویرایش محتوای همه زبان‌ها'),
                'url_name': 'theme_manage_pagetextvars_contentedit_all',
                'arg1_field': 'id'
            },
        ],
        'footer_buttons': [
            {
                'title': _('بازگشت'),
                'url_name': 'theme_manage_page_list',
                'url_arg1': page.theme_page.theme.id,
            },
        ]
    }
    return render(request, GENERIC_MODEL_LIST, context)
def page_imagevars_list(request, page_id):
    page = get_object_or_404(Page, id=page_id)
    image_vars = page.page_images.all()
    items = []
    for var in image_vars:
        obj = {}
        obj['id'] = var.id
        obj['var_name'] = var.image_variable
        for lang in settings.LANGUAGES:
            content, created = PageImageContent.objects.get_or_create(language=lang[0], page_image=var)
            obj['{lang}'.format(lang=lang[0])] = content.image_value
        items.append(obj)
    fields = ['var_name']
    fields += [lang[0] for lang in settings.LANGUAGES]
    headers = [_('نام متغیر')]
    headers += [lang[0] for lang in settings.LANGUAGES]
    context = {
        'items': items,
        'fields': fields,
        'headers': headers,
        'page_title': _('متغیرهای تصویر صفحه'),
        'page_subtitle': page.slug,
        'action_buttons': [
            {
                'title': _('ویرایش محتوای هر زبان'),
                'url_name': 'theme_manage_pageimagevars_contentedit_each',
                'arg1_field': 'id'
            },
            {
                'title': _('ویرایش محتوای همه زبان‌ها'),
                'url_name': 'theme_manage_pageimagevars_contentedit_all',
                'arg1_field': 'id'
            },
        ],
        'footer_buttons': [
            {
                'title': _('بازگشت'),
                'url_name': 'theme_manage_page_list',
                'url_arg1': page.theme_page.theme.id,
            },
        ]
    }
    return render(request, GENERIC_MODEL_LIST, context)
def page_linkvars_list(request, page_id):
    page = get_object_or_404(Page, id=page_id)
    link_vars = page.page_links.all()
    items = []
    for var in link_vars:
        obj = {}
        obj['id'] = var.id
        obj['var_name'] = var.link_variable
        for lang in settings.LANGUAGES:
            content, created = PageLinkContent.objects.get_or_create(language=lang[0], page_link=var)
            obj['{lang}'.format(lang=lang[0])] = content.link_value
        items.append(obj)
    fields = ['var_name']
    fields += [lang[0] for lang in settings.LANGUAGES]
    headers = [_('نام متغیر')]
    headers += [lang[0] for lang in settings.LANGUAGES]
    context = {
        'items': items,
        'fields': fields,
        'headers': headers,
        'page_title': _('متغیرهای لینک صفحه'),
        'page_subtitle': page.slug,
        'action_buttons': [
            {
                'title': _('ویرایش محتوای هر زبان'),
                'url_name': 'theme_manage_pagelinkvars_contentedit_each',
                'arg1_field': 'id'
            },
            {
                'title': _('ویرایش محتوای همه زبان‌ها'),
                'url_name': 'theme_manage_pagelinkvars_contentedit_all',
                'arg1_field': 'id'
            },
        ],
        'footer_buttons': [
            {
                'title': _('بازگشت'),
                'url_name': 'theme_manage_page_list',
                'url_arg1': page.theme_page.theme.id,
            },
        ]
    }
    return render(request, GENERIC_MODEL_LIST, context)
def page_menuvars_list(request, page_id):
    page = get_object_or_404(Page, id=page_id)
    menu_vars = page.menus.all()
    items = []
    for var in menu_vars:
        obj = {}
        obj['id'] = var.id
        obj['var_name'] = var.menu_variable
        for lang in settings.LANGUAGES:
            content, created = PageMenuContent.objects.get_or_create(language=lang[0], page_menu=var)
            obj['{lang}'.format(lang=lang[0])] = content.menu_content
        items.append(obj)
    fields = ['var_name']
    fields += [lang[0] for lang in settings.LANGUAGES]
    headers = [_('نام متغیر')]
    headers += [lang[0] for lang in settings.LANGUAGES]
    context = {
        'items': items,
        'fields': fields,
        'headers': headers,
        'page_title': _('متغیرهای منوی صفحه'),
        'page_subtitle': page.slug,
        'action_buttons': [
            {
                'title': _('ویرایش محتوای هر زبان'),
                'url_name': 'theme_manage_pagemenuvars_contentedit_each',
                'arg1_field': 'id'
            },
            {
                'title': _('ویرایش محتوای همه زبان‌ها'),
                'url_name': 'theme_manage_pagemenuvars_contentedit_all',
                'arg1_field': 'id'
            },
        ],
        'footer_buttons': [
            {
                'title': _('بازگشت'),
                'url_name': 'theme_manage_page_list',
                'url_arg1': page.theme_page.theme.id,
            },
        ]
    }
    return render(request, GENERIC_MODEL_LIST, context)
def page_catvars_list(request, page_id):
    page = get_object_or_404(Page, id=page_id)
    cat_vars = page.page_categories.all()
    items = []
    for var in cat_vars:
        obj = {}
        obj['id'] = var.id
        obj['var_name'] = var.category_variable
        for lang in settings.LANGUAGES:
            content, created = PageCategoryContent.objects.get_or_create(language=lang[0], page_category=var)
            obj['{lang}'.format(lang=lang[0])] = content.category_content
        items.append(obj)
    fields = ['var_name']
    fields += [lang[0] for lang in settings.LANGUAGES]
    headers = [_('نام متغیر')]
    headers += [lang[0] for lang in settings.LANGUAGES]
    context = {
        'items': items,
        'fields': fields,
        'headers': headers,
        'page_title': _('متغیرهای دسته‌بندی صفحه'),
        'page_subtitle': page.slug,
        'action_buttons': [
            {
                'title': _('ویرایش محتوای هر زبان'),
                'url_name': 'theme_manage_pagecatvars_contentedit_each',
                'arg1_field': 'id'
            },
            {
                'title': _('ویرایش محتوای همه زبان‌ها'),
                'url_name': 'theme_manage_pagecatvars_contentedit_all',
                'arg1_field': 'id'
            },
        ],
        'footer_buttons': [
            {
                'title': _('بازگشت'),
                'url_name': 'theme_manage_page_list',
                'url_arg1': page.theme_page.theme.id,
            },
        ]
    }
    return render(request, GENERIC_MODEL_LIST, context)






def page_textvars_editcontent_each(request, textvar_id):
    textvar = get_object_or_404(PageText, id=textvar_id)

    TextContentFormSet = modelformset_factory(PageTextContent, form=PageTextContentSingleLanguageForm, extra=0, max_num=3)
    if request.method == 'POST':
        formset = TextContentFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('theme_manage_pagetextvars_list', page_id=textvar.page.id)
    else:
        for lang in settings.LANGUAGES:
            content, created = PageTextContent.objects.get_or_create(language=lang[0], page_text=textvar, defaults={'text_value': ' '})
        formset = TextContentFormSet(queryset=textvar.contents.all())
    context = {
        'page_title': _('ویرایش محتوای هر زبان'),
        'page_subtitle': textvar.variable,
        'formset': formset,
        'form_submit_url_name': 'theme_manage_pagetextvars_contentedit_each',
        'form_submit_url_arg1': textvar_id,
        'form_cancel_url_name': 'theme_manage_pagetextvars_list',
        'form_cancel_url_arg1': textvar.page.id,
    }
    return render(request, GENERIC_MODEL_FORM, context)
def page_imagevars_editcontent_each(request, imagevar_id):
    var = get_object_or_404(PageImage, id=imagevar_id)

    ContentFormSet = modelformset_factory(PageImageContent, form=PageImageContentSingleLanguageForm, extra=0, max_num=3)
    if request.method == 'POST':
        formset = ContentFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('theme_manage_pageimagevars_list', page_id=var.page.id)
    else:
        for lang in settings.LANGUAGES:
            content, created = PageImageContent.objects.get_or_create(language=lang[0], page_image=var)
        formset = ContentFormSet(queryset=var.page_images.all())
    context = {
        'page_title': _('ویرایش محتوای هر زبان'),
        'page_subtitle': var.image_variable,
        'formset': formset,
        'form_submit_url_name': 'theme_manage_pageimagevars_contentedit_each',
        'form_submit_url_arg1': imagevar_id,
        'form_cancel_url_name': 'theme_manage_pageimagevars_list',
        'form_cancel_url_arg1': var.page.id,
    }
    return render(request, GENERIC_MODEL_FORM, context)
def page_linkvars_editcontent_each(request, var_id):
    var = get_object_or_404(PageLink, id=var_id)

    ContentFormSet = modelformset_factory(PageLinkContent, form=PageLinkContentSingleLanguageForm, extra=0, max_num=3)
    if request.method == 'POST':
        formset = ContentFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('theme_manage_pagelinkvars_list', page_id=var.page.id)
    else:
        for lang in settings.LANGUAGES:
            content, created = PageLinkContent.objects.get_or_create(language=lang[0], page_link=var)
        formset = ContentFormSet(queryset=var.contents.all())
    context = {
        'page_title': _('ویرایش محتوای هر زبان'),
        'page_subtitle': var.link_variable,
        'formset': formset,
        'form_submit_url_name': 'theme_manage_pagelinkvars_contentedit_each',
        'form_submit_url_arg1': var_id,
        'form_cancel_url_name': 'theme_manage_pagelinkvars_list',
        'form_cancel_url_arg1': var.page.id,
    }
    return render(request, GENERIC_MODEL_FORM, context)
def page_menuvars_editcontent_each(request, var_id):
    var = get_object_or_404(PageMenu, id=var_id)

    ContentFormSet = modelformset_factory(PageMenuContent, form=PageMenuContentSingleLanguageForm, extra=0, max_num=3)
    if request.method == 'POST':
        formset = ContentFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('theme_manage_pagemenuvars_list', page_id=var.page.id)
    else:
        for lang in settings.LANGUAGES:
            content, created = PageMenuContent.objects.get_or_create(language=lang[0], page_menu=var)
        formset = ContentFormSet(queryset=var.menu_contents.all())
    context = {
        'page_title': _('ویرایش محتوای هر زبان'),
        'page_subtitle': var.menu_variable,
        'formset': formset,
        'form_submit_url_name': 'theme_manage_pagemenuvars_contentedit_each',
        'form_submit_url_arg1': var_id,
        'form_cancel_url_name': 'theme_manage_pagemenuvars_list',
        'form_cancel_url_arg1': var.page.id,
    }
    return render(request, GENERIC_MODEL_FORM, context)
def page_catvars_editcontent_each(request, var_id):
    var = get_object_or_404(PageCategory, id=var_id)

    ContentFormSet = modelformset_factory(PageCategoryContent, form=PageCatContentSingleLanguageForm, extra=0, max_num=3)
    if request.method == 'POST':
        formset = ContentFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('theme_manage_pagecatvars_list', page_id=var.page.id)
    else:
        for lang in settings.LANGUAGES:
            content, created = PageCategoryContent.objects.get_or_create(language=lang[0], page_category=var)
        formset = ContentFormSet(queryset=var.contents.all())
    context = {
        'page_title': _('ویرایش محتوای هر زبان'),
        'page_subtitle': var.category_content,
        'formset': formset,
        'form_submit_url_name': 'theme_manage_pagecatvars_contentedit_each',
        'form_submit_url_arg1': var_id,
        'form_cancel_url_name': 'theme_manage_pagecatvars_list',
        'form_cancel_url_arg1': var.page.id,
    }
    return render(request, GENERIC_MODEL_FORM, context)





def page_textvars_editcontent_all(request, textvar_id):
    textvar = get_object_or_404(PageText, id=textvar_id)
    if request.method == 'POST':
        form = PageTextContentNoLanguageForm(request.POST)
        if form.is_valid():
            for lang in settings.LANGUAGES:
                content, created = PageTextContent.objects.get_or_create(language=lang[0], page_text=textvar, defaults={'text_value': ' '})
                content.text_value = form.cleaned_data.get('text_value')
                content.save()
            return redirect('theme_manage_pagetextvars_list', page_id=textvar.page.id)
    else:
        form = PageTextContentNoLanguageForm()
    context = {
        'page_title': _('ویرایش محتوای همه زبان‌ها'),
        'page_subtitle': textvar.variable,
        'forms': [form],
        'form_submit_url_name': 'theme_manage_pagetextvars_contentedit_all',
        'form_submit_url_arg1': textvar_id,
        'form_cancel_url_name': 'theme_manage_pagetextvars_list',
        'form_cancel_url_arg1': textvar.page.id,
    }
    return render(request, GENERIC_MODEL_FORM, context)
def page_imagevars_editcontent_all(request, imagevar_id):
    var = get_object_or_404(PageImage, id=imagevar_id)
    if request.method == 'POST':
        form = PageImageContentNoLanguageForm(request.POST)
        if form.is_valid():
            for lang in settings.LANGUAGES:
                content, created = PageImageContent.objects.get_or_create(language=lang[0], page_image=var )
                content.image_value = form.cleaned_data.get('image_value')
                content.save()
            return redirect('theme_manage_pageimagevars_list', page_id=var.page.id)
    else:
        form = PageImageContentNoLanguageForm()
    context = {
        'page_title': _('ویرایش محتوای همه زبان‌ها'),
        'page_subtitle': var.image_variable,
        'forms': [form],
        'form_submit_url_name': 'theme_manage_pageimagevars_contentedit_all',
        'form_submit_url_arg1': imagevar_id,
        'form_cancel_url_name': 'theme_manage_pageimagevars_list',
        'form_cancel_url_arg1': var.page.id,
    }
    return render(request, GENERIC_MODEL_FORM, context)
def page_linkvars_editcontent_all(request, var_id):
    var = get_object_or_404(PageLink, id=var_id)
    if request.method == 'POST':
        form = PageLinkContentNoLanguageForm(request.POST)
        if form.is_valid():
            for lang in settings.LANGUAGES:
                content, created = PageLinkContent.objects.get_or_create(language=lang[0], page_link=var)
                content.link_value = form.cleaned_data.get('link_value')
                content.save()
            return redirect('theme_manage_pagelinkvars_list', page_id=var.page.id)
    else:
        form = PageLinkContentNoLanguageForm()
    context = {
        'page_title': _('ویرایش محتوای همه زبان‌ها'),
        'page_subtitle': var.link_variable,
        'forms': [form],
        'form_submit_url_name': 'theme_manage_pagelinkvars_contentedit_all',
        'form_submit_url_arg1': var_id,
        'form_cancel_url_name': 'theme_manage_pagelinkvars_list',
        'form_cancel_url_arg1': var.page.id,
    }
    return render(request, GENERIC_MODEL_FORM, context)
def page_menuvars_editcontent_all(request, var_id):
    var = get_object_or_404(PageMenu, id=var_id)
    if request.method == 'POST':
        form = PageMenuContentNoLanguageForm(request.POST)
        if form.is_valid():
            for lang in settings.LANGUAGES:
                content, created = PageMenuContent.objects.get_or_create(language=lang[0], page_menu=var)
                content.menu_content = form.cleaned_data.get('menu_content')
                content.save()
            return redirect('theme_manage_pagemenuvars_list', page_id=var.page.id)
    else:
        form = PageMenuContentNoLanguageForm()
    context = {
        'page_title': _('ویرایش محتوای همه زبان‌ها'),
        'page_subtitle': var.menu_variable,
        'forms': [form],
        'form_submit_url_name': 'theme_manage_pagemenuvars_contentedit_all',
        'form_submit_url_arg1': var_id,
        'form_cancel_url_name': 'theme_manage_pagemenuvars_list',
        'form_cancel_url_arg1': var.page.id,
    }
    return render(request, GENERIC_MODEL_FORM, context)
def page_catvars_editcontent_all(request, var_id):
    var = get_object_or_404(PageCategory, id=var_id)
    if request.method == 'POST':
        form = PageCatContentNoLanguageForm(request.POST)
        if form.is_valid():
            for lang in settings.LANGUAGES:
                content, created = PageCategoryContent.objects.get_or_create(language=lang[0], page_category=var)
                content.category_content = form.cleaned_data.get('category_content')
                content.save()
            return redirect('theme_manage_pagecatvars_list', page_id=var.page.id)
    else:
        form = PageCatContentNoLanguageForm()
    context = {
        'page_title': _('ویرایش محتوای همه زبان‌ها'),
        'page_subtitle': var.category_variable,
        'forms': [form],
        'form_submit_url_name': 'theme_manage_pagecatvars_contentedit_all',
        'form_submit_url_arg1': var_id,
        'form_cancel_url_name': 'theme_manage_pagecatvars_list',
        'form_cancel_url_arg1': var.page.id,
    }
    return render(request, GENERIC_MODEL_FORM, context)



