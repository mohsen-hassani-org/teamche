from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, reverse, get_object_or_404, get_list_or_404
from django.utils.translation import ugettext as _
from blog.models import Post, PostContent, Comment
from .models import Page, PageText, PageTextContent, Theme, ThemePage, SiteSetting
from .helper_functions import get_active_theme, get_page, get_page_variables, combine_variables, get_post_by_slug, get_search_result
from .forms import CommentForm

# Create your views here.

def admin(request):
    return redirect('/account/profile')

def blog_page(request):
    theme = get_active_theme()
    page = get_page(theme, 'blog')
    page_num = request.GET.get('page', 1)
    context = get_page_variables(page, page_num)
    # a = context['vars']['cats']['posts']
    # di = dir(a)
    template = 'themes/{0}/{1}'.format(theme.name, page.theme_page.file_name)
    return render(request, template, context)

def post_page(request, slug):
    if request.method == "POST" and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            post = get_post_by_slug(slug)
            comment = Comment(post=post.post, body=form.cleaned_data.get('body'), username=request.user)
            comment.save()
            return redirect(reverse('theme_post', kwargs={'slug':slug}) + '?new_comment=done#new_comment')
    theme = get_active_theme()
    page = get_page(theme, 'post')
    context = get_page_variables(page, slug=slug)
    context['form'] = CommentForm()
    template = 'themes/{0}/{1}'.format(theme.name, page.theme_page.file_name)
    return render(request, template, context)

def search_page(request):
    query = request.GET.get('q')
    if not query:
        raise Http404()
    theme = get_active_theme()
    page = get_page(theme, 'search')
    page_num = request.GET.get('page', 1)
    results = get_search_result(query) 

    context = get_page_variables(page, page_num)
    context['search_result'] = results

    template = 'themes/{0}/{1}'.format(theme.name, page.theme_page.file_name)
    return render(request, template, context)


def custom_page(request, slug):
    ''' 
        First look for slugs in themepages, 
        search for pages in custom pages if no themepage found
    '''
    theme = get_active_theme()
    page = get_page(theme, slug)
    if page:
        context = get_page_variables(page, slug=slug)
        template = 'themes/{0}/{1}'.format(theme.name, page.theme_page.file_name)
        return render(request, template, context)
    raise Http404()


def start_page(request):
    setting = SiteSetting.objects.get_or_create()[0]
    slug = 'admin'
    if setting.home_page:
        slug = setting.home_page
    return redirect('theme_custom_page', slug=slug)
