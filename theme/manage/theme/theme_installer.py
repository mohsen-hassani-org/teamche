import os
import json
import shutil
import zipfile
from django.utils.translation import ugettext as _
from django.core.files.base import File as DjangoFile
from django.conf import settings
from theme.models import Theme, ThemePage
from theme.models import PageCategory, PageCategoryContent
from theme.models import PageMenu, PageMenuContent
from theme.models import PagePost, PagePostContent
from theme.models import PageText, PageTextContent
from theme.models import PageLink, PageLinkContent
from theme.models import PageImage, PageImageContent
from theme.models import Page
from file.models import File


def install_theme(file):
    if file.size > (20 * 1024 * 1024):  # 20MB
        return _('حجم فایل مورد نظر باید کمتر از 10 مگابایت باشد')
    if not zipfile.is_zipfile(file):
        return _('فایل مورد نظر باید با فرمت zip باشد')

    theme_name = file.name[:-4]
    cwd = os.getcwd()
    theme_template_path = '{cwd}/theme/templates/themes/{theme}'.format(
        cwd=cwd, theme=theme_name)
    theme_static_path = '{cwd}/static/theme/themes/{theme}'.format(
        cwd=cwd, theme=theme_name)
    if os.path.exists(theme_template_path) or os.path.exists(theme_static_path):
        return _('پوسته‌ای با این نام وجود دارد')
    with zipfile.ZipFile(file, mode='r') as zipped_theme:
        zipped_theme.extractall(
            'theme/templates/themes/{0}'.format(theme_name))
    shutil.move('{cwd}/theme/templates/themes/{theme}/{theme}'.format(
        cwd=cwd, theme=theme_name), theme_static_path)
    generate_db_records(
        cwd + '/theme/templates/themes/{0}/theme_info.json'.format(theme_name))


def generate_db_records(path):
    theme_json = None
    with open(path, mode='r') as file:
        theme_json = json.load(file)
    theme_info = theme_json['info']
    theme_pages = theme_json['theme']['pages']
    theme_init_pages = theme_json['theme']['initial_pages']

    theme = create_theme(theme_info)
    create_theme_pages(theme, theme_pages)
    create_theme_initial_pages(theme, theme_pages, theme_init_pages)
    set_custompage_pagetype_to_null()# set all custom pages page_type to null


def set_custompage_pagetype_to_null():
    pages = Page.objects.filter(page_type='custom')
    updated_pages = []
    for page in pages:
        page.theme_page = None
        updated_pages.append(page)
    Page.objects.bulk_update(updated_pages)


def create_theme(theme_info):
    theme = Theme(name=theme_info['name'],
                  website=theme_info['site'],
                  author_name=theme_info['author'],
                  author_email=theme_info['email'],
                  desc=theme_info['desc'],
                  image='theme/themes/{0}/{1}'.format(theme_info['name'], theme_info['image']))
    theme.save()
    return theme


def create_theme_pages(theme, theme_pages):
    for theme_page in theme_pages.keys():
        name = theme_page
        file = theme_pages[name]['file']
        page_type = theme_pages[name]['type']
        page = ThemePage(theme=theme, page_name=name,
                         file_name=file, page_type=page_type)
        page.save()


def create_theme_initial_pages(theme, theme_pages, theme_init_pages):
    for init_page in theme_init_pages:
        page = init_page['page']
        theme_page = get_theme_page(theme, page)
        if theme_page == None:
            continue
        base = get_page(theme, init_page['base'])
        slug = init_page['slug']
        page = Page(base=base, page_type='system',
                    slug=slug, theme_page=theme_page)
        page.save()
        create_text_variables(
            theme, page, theme_pages[page.slug]['variables']['text'])
        create_link_variables(
            theme, page, theme_pages[page.slug]['variables']['link'])
        create_menu_variables(
            theme, page, theme_pages[page.slug]['variables']['menu'])
        create_post_variables(
            theme, page, theme_pages[page.slug]['variables']['post'])
        create_image_variables(
            theme, page, theme_pages[page.slug]['variables']['image'])
        create_category_variables(
            theme, page, theme_pages[page.slug]['variables']['category'])


def get_theme_page(theme, page):
    theme_page = ThemePage.objects.filter(theme=theme, page_name=page)
    if not theme_page:
        return None
    return theme_page[0]


def get_page(theme_page, slug):
    page = Page.objects.filter(theme_page__theme=theme_page, slug=slug)
    if not page:
        return None
    return page[0]


def create_text_variables(theme, page, variables):
    bulk_objects = []
    bulk_contents = []
    default_values = {}

    for variable in variables:
        var = variable['name']
        text_var = PageText(page=page, variable=var)
        bulk_objects.append(text_var)
        default_values[variable['name']] = variable['default']
    PageText.objects.bulk_create(bulk_objects)

    page_text_vars = PageText.objects.filter(page=page)
    for variable in page_text_vars:
        value = default_values[variable.variable]
        for lang in settings.LANGUAGES:
            cont = PageTextContent(
                language=lang[0], page_text=variable, text_value=value)
            bulk_contents.append(cont)
    PageTextContent.objects.bulk_create(bulk_contents)


def create_menu_variables(theme, page, variables):
    menus = []
    for variable in variables:
        menu = PageMenu(page=page, menu_variable=variable)
        menus.append(menu)
    PageMenu.objects.bulk_create(menus)


def create_post_variables(theme, page, variables):
    posts = []
    for variable in variables:
        post = PagePost(page=page, post_variable=variable)
        posts.append(post)
    PagePost.objects.bulk_create(posts)


def create_category_variables(theme, page, variables):
    cats = []
    for variable in variables:
        cat = PageCategory(
            page=page, category_variable=variable['name'], count=variable['count'])
        cats.append(cat)
    PageCategory.objects.bulk_create(cats)


def create_link_variables(theme, page, variables):
    links = []
    bulk_link_variables = []
    bulk_link_contents = []
    default_values = {} 
    for variable in variables:
        link = PageLink(page=page, link_variable=variable['name'])
        bulk_link_variables.append(link)
        default_values[variable['name']] = variable['default']
    PageLink.objects.bulk_create(bulk_link_variables)
    page_links = PageLink.objects.filter(page=page)

    for page_link in page_links:
        content = default_values[page_link.link_variable]
        for lang in settings.LANGUAGES:
            link_content = PageLinkContent(language=lang[0], page_link=page_link, link_value=content)
            bulk_link_contents.append(link_content)
    PageLinkContent.objects.bulk_create(bulk_link_contents)



def create_image_variables(theme, page, variables):
    images = []
    bulk_images = []
    bulk_content = []
    default_vals = {}
    for variable in variables:
        img = PageImage(page=page, image_variable=variable['name'])
        bulk_images.append(img)
        default_vals[variable['name']] = variable['default']
    PageImage.objects.bulk_create(bulk_images)
    page_images = PageImage.objects.filter(page=page)

    cwd = os.getcwd()
    for page_image in page_images:
        relative_path = default_vals[page_image.image_variable]
        path = '{cwd}/static/theme/themes/{theme}/{relative_path}'.format(
            cwd=cwd, theme=theme.name, relative_path=relative_path)
        with open(path, mode='rb') as base_file:
            django_file = DjangoFile(base_file)
            img = File()
            img.file.save(relative_path, django_file)
        for lang in settings.LANGUAGES:
            content = PageImageContent(
                language=lang[0], page_image=page_image, image_value=img)
            bulk_content.append(content)
    PageImageContent.objects.bulk_create(bulk_content)

    # Create Page Variables
    # cat_vars = theme_pages[name]['variables']['category']
    # # img_vars = theme_pages[name]['variables']['image']
    # mnu_vars = theme_pages[name]['variables']['menu']
    # txt_vars =
    # # lnk_vars = theme_pages[name]['variables']['link']
    # for cat in cat_vars:
    #     page_cat = PageCategory(page=page, category_variable=cat)
    # for menu in mnu_vars:
    #     page_menu = PageMenu(page=page, menu_variable=menu)
    #     page_menu.save()
    # for text in txt_vars.keys():
    #     page_text = PageText(page=page, variable=text)
    #     page_text.save()
