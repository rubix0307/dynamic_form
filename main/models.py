from django.db import models

# Create your models here.

class Bank(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'<{self.__class__.__name__}>: {self.name} ({self.id})'

    def __repr__(self):
        return self.__str__()

    class Meta:
        db_table = 'bank'