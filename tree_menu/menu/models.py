from django.db import models
from django.urls import NoReverseMatch, reverse


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True,related_name= 'children', on_delete=models.CASCADE)
    url = models.CharField(max_length=100)
    url_name = models.CharField(max_length=100,  null=True, blank=True)

    def __str__(self):
        return self.name

    def get_item_url(item):
        if item.url:
            return item.url
        elif item.url_name:
            try:
                return reverse(item.url_name)
            except NoReverseMatch:
                return "#invalid-url"
        return



