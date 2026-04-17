from django.db import models

class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    rating = models.FloatField(null=True, blank=True)
    url = models.URLField()

    def __str__(self):
        return self.title
    
    summary = models.TextField(blank=True, null=True)