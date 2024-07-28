from django.db import models

class Space(models.Model):
    space_name = models.CharField(max_length=255)
    space_description = models.TextField(null=True, blank=True)

class Category(models.Model):
    category_name = models.CharField(max_length=255)
    space = models.ForeignKey(Space, on_delete=models.CASCADE)

class Subcategory(models.Model):
    subcategory_name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    parent_subcategory = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

class Url(models.Model):
    name = models.CharField(max_length=255)
    link = models.URLField()
    image = models.URLField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, null=True, blank=True, on_delete=models.CASCADE)
