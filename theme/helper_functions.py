from django.http import Http404
from django.shortcuts import get_object_or_404, get_list_or_404
from django.utils.translation import get_language
from django.core.paginator import Paginator
from django.db.models import Q
from blog.models import Category, CategoryContent, Post, PostCategory, PostContent
from .models import Theme, Page, ThemePage, Menu, MenuItem, MenuItemContent
from .models import PageTextContent, PageCategory, PageCategoryContent, PageMenuContent, PageMenu
from .models import PageImage, PageImageContent, PageLink, PageLinkContent
from .models import SiteSetting
from .forms import CommentForm


def get_active_theme():
    themes = get_list_or_404(Theme, is_active=True)
    return themes[0]


def get_page(theme, slug):
    page = Page.objects.filter(slug=slug, theme_page__theme=theme).first()
    if not page:
        raise Http404('Page not found')
    return page


def get_page_texts(page):
    lang = get_language()
    texts = page.page_texts.all()
    text_val = {}
    for text in texts:
        values = PageTextContent.objects.filter(page_text=text, language=lang)
        for value in values:
            key = value.page_text.variable
            val = value.text_value
            text_val[key] = val
    return text_val


def get_page_links(page):
    lang = get_language()
    links = page.page_links.all()
    link_val = {}
    for link in links:
        page_link_contents = PageLinkContent.objects.filter(
            page_link=link, language=lang)
        for page_link_content in page_link_contents:
            key = page_link_content.page_link.link_variable
            val = page_link_content.link_value
            link_val[key] = val
    return link_val


def get_page_images(page):
    lang = get_language()
    images = page.page_images.all()
    img_vals = {}
    for image in images:
        values = image.page_images.filter(language=lang)
        for value in values:
            key = image.image_variable
            val = value.image_value.file.url if value.image_value else None
            img_vals[key] = val
    return img_vals


def get_category_posts(cat, count, page_num=1):
    count = 1000 if count == 0 else count
    lang = get_language()
    all_posts = PostContent.objects.filter(
        post__category=cat, lang=lang, status='PUBLISH').order_by('-id')
    paginator = Paginator(all_posts, count)
    try:
        post_list = paginator.page(page_num)
    except:
        post_list = paginator.page(1)
    return post_list


def get_page_cats(page, page_num):
    lang = get_language()
    cats = page.page_categories.all()
    cat_vals = {}
    for cat in cats:
        values = PageCategoryContent.objects.filter(
            page_category=cat, language=lang)
        for value in values:
            key = value.page_category.category_variable
            count = value.page_category.count
            val = value.category_content
            cat_vals[key] = get_category_posts(val, count, page_num)
    return cat_vals


def get_page_menus(page):
    page_menus = page.menus.all()
    menu_vars = {}
    for page_menu in page_menus:
        key = page_menu.menu_variable
        val = get_menu_from_var(page_menu)
        menu_vars[key] = val
    return menu_vars


def get_page_post(page, slug):
    if not slug:
        return None
    if page.page_type == 'custom':
        return {'content': get_post_content(page.post)}
    # page_posts = page.page_posts.all()
    # post_vars = {'post': get_post_content(post)}
    # for page_post in page_posts:
    #     key = page_post.post_variable
    #     val = get_post_by_slug(slug)
    #     post_vars[key] = val
    #     post_vars[key] = {'post': val,
    #                       'comments': val.post.comments.filter(confirmed=True)}
    # return post_vars
    post = get_post_by_slug(slug)
    return {
        'content': post,
        'comments': post.post.comments.filter(confirmed=True) if post else None}
    


def get_menu_from_var(menu):
    lang = get_language()
    menus = PageMenuContent.objects.filter(language=lang, page_menu=menu)
    if not menus:
        return None
    menu = menus[0].menu_content
    if menu:
        return create_menu_context(menu)
    return []


def create_menu_context(menu):
    menu_context = []
    for item in menu.items.all().order_by('order'):
        if item.parent == None:
            menu_context.append(get_item(item))
    return menu_context


def get_item(item):
    lang = get_language()
    obj = {}
    url = get_item_url(item)

    sub_items = item.subitems.all().order_by('order')
    childs = []
    if sub_items:
        for child in sub_items:
            childs.append(get_item(child))
    content = item.contents.filter(language=lang)
    content = url if not content else content[0]
    obj['childs'] = childs
    obj['title'] = content
    obj['url'] = url
    if item.subitems.all():
        obj['items'] = []
        for subitem in item.subitems.all():
            obj['items'].append(get_item(subitem))
    return obj


def get_item_url(item):
    return item.url


def get_page_variables(page, page_num=None, slug=None):
    base_variables = get_page_variables(
        page.base, page_num) if page.base else None
    variables = {}
    variables['cats'] = get_page_cats(page, page_num)
    variables['texts'] = get_page_texts(page)
    variables['links'] = get_page_links(page)
    variables['menus'] = get_page_menus(page)
    variables['post'] = get_page_post(page, slug)
    variables['images'] = get_page_images(page)

    all_variables = combine_variables(variables, base_variables)
    return all_variables


def get_search_result(query=''):
    lang = get_language()
    items = PostContent.objects.filter(title__icontains=query, lang=lang)
    count = items.count()
    results = {
        'q': query,
        'items': items,
        'count': count
    }
    return results


def get_post_by_slug(slug):
    post = Post.objects.filter(slug=slug).first()
    if not post:
        return None
    return get_post_content(post)

def get_post_content(post):
    lang = get_language()
    content = PostContent.objects.filter(lang=lang, post=post).first()
    return content


def get_site_settings():
    setting = SiteSetting.objects.get_or_create()[0]
    return {
        'title': setting.site_title,
        'sub_title': setting.site_subtitle,
        'primary_light_color': setting.primary_light_color,
        'primary_bold_color': setting.primary_bold_color,
        'primary_dark_color': setting.primary_dark_color,
        'accend_light_color': setting.accend_light_color,
        'accend_bold_color': setting.accend_bold_color,
        'accend_dark_color': setting.accend_dark_color,
    }

def get_theme_settings():
    return {}

def combine_variables(variables, base_variables):
    site_settings = get_site_settings()
    theme_settings = get_theme_settings()
    if base_variables:
        return {
            'vars': variables,
            'base': base_variables,
            'settings': site_settings,
            'theme': theme_settings,
        }
    return {
        'vars': variables,
        'settings': site_settings,
        'theme': theme_settings,
    }
