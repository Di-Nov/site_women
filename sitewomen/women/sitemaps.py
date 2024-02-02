from django.contrib.sitemaps import Sitemap

from women.models import Women, Category


class PostSitemap(Sitemap):
    priority = 0.9
    changefreq = 'monthly'

    def items(self):
        return Women.published.all()

    def lastmod(self, obj):
        return obj.time_update

class CategorySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8

    def items(self):
        return Category.objects.all()