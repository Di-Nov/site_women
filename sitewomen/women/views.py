import uuid

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView

from women.forms import AddPostForm, UploadFileForm
from women.models import WomenModel, Category, TagPost
from women.utils import DataMixin


class WomenHome(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return WomenModel.published.all().select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title='Главная страница')


class ShowPost(DataMixin, DetailView):
    template_name = 'women/post.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'

    def get_object(self, queryset=None):
        return get_object_or_404(WomenModel.published, slug=self.kwargs[self.slug_url_kwarg])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)


def page_not_found(request, exception):
    return HttpResponseNotFound('Хахаха... Страница не найдена, что ты будешь делать, человеческий детеныш')


class WomenCategory(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False # флаг разрешения отображения страницы с пустым списком записей (для класса ListView)

    def get_queryset(self):
        return WomenModel.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context, title='Категория - ' + cat.name, cat_selected=cat.id)


class TagPostList(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return WomenModel.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тег: ' + tag.tag, cat_selected=None)


class UpdatePage(LoginRequiredMixin, DataMixin, UpdateView): # LoginRequiredMixin - Закрывает старницу для неавторизованного user,
    form_class = AddPostForm
    model = WomenModel
    # fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'women/add_post.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'
    login_url = reverse_lazy('user:login') # перенаправлят на login_url. приоритет выше чем у LOGIN_URL в настройках

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    '''метод form_valid() уже реализован внутри класса CreateView'''

    template_name = 'women/add_post.html'
    form_class = AddPostForm
    success_url = reverse_lazy('home')
    title_page = 'Добавление статьи'
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)

def handle_uploaded_file(f):
    """Функция используется для чтения файла который загружаем, его наименования и сохранении по заданому пути"""

    name = f.name
    ext = ''
    if '.' in name:
        ext = name[name.rindex('.'):]
        name = name[:name.rindex('.')]
    suffix = str(uuid.uuid4())
    with open(f"uploads/{name}_{suffix}{ext}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@login_required(login_url=reverse_lazy('users:login')) # Закрывает старницу для неавторизованного user, перенаправлят на login_url определяет URL-адрес. приоритет выше чем у LOGIN_URL в настройках
def about(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(form.cleaned_data['file'])
    else:
        form = UploadFileForm()

    return render(request, 'women/about.html',
                  context={'title': 'О сайте', 'form': form})


class FeedBack(DataMixin, TemplateView):
    template_name = 'women/feedback.html'
    title_page = 'Обратная связь'
