from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from women.models import Women, Category


class MarriedFilter(admin.SimpleListFilter):
    title = "Статус женщин"
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('married', 'Замужем'),
            ('single', 'Не замужем'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'married':
            return queryset.filter(husband__isnull=False)
        elif self.value() == 'single':
            return queryset.filter(husband__isnull=True)



@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):

    list_display = ['id', 'title', 'post_photo', 'time_create', 'is_published', 'cat']
    readonly_fields = ['post_photo']
    list_display_links = ['id', 'title']
    ordering = ['time_create', 'title']
    list_editable = ['is_published']
    list_per_page = 10
    actions = ['make_published', 'make_draft']
    search_fields = ['title__icontains', 'cat__name']
    list_filter = [MarriedFilter, 'cat__name', 'is_published']
    filter_horizontal = ['tags']
    save_on_top = True
    # filter_vertical = ['tags']

    # fields = ['title', 'content', 'slug']
    # exclude = ['tags', 'is_published']
    # readonly_fields = ['slug']
    prepopulated_fields = {'slug': ['title']}



    @admin.display(description='Изображение')
    def post_photo(self, women: Women):
        '''Добавление нового поля в админ-панели'''
        if women.photo:
            return mark_safe(f"<img src='{women.photo.url}' width=50>")
        else:
            return 'Фото нет'

    @admin.action(description='Сменить статус на опубликовано')
    def make_published(self, request, queryset):
        '''Добавление нового действия с выборкой полей в админ-панели'''
        count = queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записи(ей).")

    @admin.action(description='Снять с публикации')
    def make_draft(self, request, queryset):
        '''Добавление нового действия с выборкой полей в админ-панели'''
        count = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(request, f"{count} записи(ей) снято с публикации.", messages.WARNING)

    # @admin.display(description='Количество символов в статье')
    # def brief_info(self, women: WomenModel):
    # '''Добавление нового поля в админ-панели'''
    #     return f'Статья из {len(women.content)} символов'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

