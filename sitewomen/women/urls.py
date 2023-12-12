from django.urls import path, register_converter
from women import views, converters
from women.views import page_not_found

register_converter(converters.FourDigitYearConverter, 'year4')


urlpatterns = [
    path('', views.WomenHome.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('auth/', views.login, name='login'),
    path('post/<slug:post_slug>/', views.show_post, name='show_post'),
    path('category/<slug:cat_slug>/', views.show_category, name='category'),
    path('tag/<slug:tag_slug>/', views.show_tag_postlist, name='tag'),
    path('add_post/', views.AddPage.as_view(), name='add_post')
]

handler404 = page_not_found
