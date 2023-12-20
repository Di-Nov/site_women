from django.urls import path, register_converter
from women import views, converters
from women.views import page_not_found

register_converter(converters.FourDigitYearConverter, 'year4')


urlpatterns = [
    path('', views.WomenHome.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.FeedBack.as_view(), name='contact'),
    path('add_post/', views.AddPage.as_view(), name='add_post'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='show_post'),
    path('category/<slug:cat_slug>/', views.WomenCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.TagPostList.as_view(), name='tag'),
    path('edit_post/<int:pk>/', views.UpdatePage.as_view(), name='edit_post')
]

handler404 = page_not_found
