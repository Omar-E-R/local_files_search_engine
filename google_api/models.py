from django.db import models


# Create your models here.
class Index(models.Model):
    words = models.CharField(max_length=25)
    documents = models.CharField(max_length=50)
    occurrences = models.IntegerField(editable=False)

    def __str__(self):
        return self.words
