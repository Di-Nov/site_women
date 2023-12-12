import uuid

from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView

from women.forms import AddPostForm, UploadFileForm
from women.models import WomenModel, Category, TagPost

menu = [
    {'title': "Главная страница", 'url_name': 'home'},
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Добавить статью", 'url_name': 'add_post'},
    {'title': "Обратная связь", 'url_name': 'contact'},
    {'title': "Войти", 'url_name': 'login'}
]

class WomenHome(TemplateView):
    template_name = 'women/index.html'
    extra_context = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': WomenModel.published.all().select_related('cat'),
        'cat_selected': 0,
    }

# def index(request):
#     posts = WomenModel.published.all().select_related('cat')
#     categories = Category.objects.all()
#     data = {
#         'title': 'Главная страница',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': 0,
#     }
#     return render(request, 'women/index.html', context=data)


def show_post(request, post_slug):
    post = get_object_or_404(WomenModel, slug=post_slug)
    data = {
        'title': f'{post.title}',
        'menu': menu,
        'post': post,
    }
    return render(request, 'women/post.html', context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound('Хахаха... Страница не найдена, что ты будешь делать, человеческий детеныш')


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    categories = Category.objects.all()
    posts = WomenModel.published.filter(cat_id=category.pk).select_related('cat')
    data = {
        'title': f'Рубрика: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat': category,
        'cats': categories,
    }
    return render(request, 'women/index.html', context=data)


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags_post.filter(is_published=WomenModel.Status.PUBLISHED).select_related('cat')

    data = {
        'title': f'Тег: {tag.tag}',
        'menu': menu,
        'posts': posts,
        "cat_selected": None,
    }
    return render(request, 'women/index.html', context=data)



class AddPage(View):
    def get(self, request):
        form = AddPostForm()
        data = {
                'menu': menu,
                'form': form
            }
        return render (request, 'women/add_post.html', context=data)

    def post(self, request):
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            redirect('home')

# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # fp = WomenModel(file=form.cleaned_data['photo'])
#             # fp.save()
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     data = {
#         'menu': menu,
#         'form': form
#     }
#     return render(request, 'women/add_post.html', context=data)


def handle_uploaded_file(f):
    """Функция используется для чтения файла, его наименовании и сохранении файлов по заданому пути"""
    name = f.name
    ext = ''
    if '.' in name:
        ext = name[name.rindex('.'):]
        name = name[:name.rindex('.')]
    suffix = str(uuid.uuid4())
    with open(f"uploads/{name}_{suffix}{ext}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def about(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(form.cleaned_data['file'])
    else:
        form = UploadFileForm()

    return render(request, 'women/about.html',
                  context={'title': 'О сайте', 'menu': menu, 'form': form})


def contact(request):
    return HttpResponse('<h2>Обратная связь</h2>')


def login(request):
    return HttpResponse('<h2>Войти</h2>')



