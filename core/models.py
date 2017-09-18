from django.db import models
from django.contrib.auth.models import User


class SavedPlot(models.Model):
    class Meta:
        verbose_name = 'Saved Plot'
        verbose_name_plural = 'Saved Plots'

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150)
    user = models.ForeignKey(User)
    plots = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{0}'.format(self.name)

    def __repr__(self):
        return self.__str__()
