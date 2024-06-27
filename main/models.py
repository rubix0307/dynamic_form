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


class Activity(models.Model):
    name = models.CharField(max_length=255)

class Specialization(models.Model):
    name = models.CharField(max_length=255)
    activity = models.ForeignKey('Activity', on_delete=models.CASCADE, related_name='specialization')


class PriceDataManager(models.Manager):
    def get_package_with_children(self, pk):
        package = self.get(pk=pk)
        package.values_list = self._get_children(package)
        package.total_value = package.get_total_value()
        return package

    def _get_children(self, parent):
        children = parent.values.all()
        for child in children:
            child.values_list = self._get_children(child)
        return children

class PlaceType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'<{self.__class__.__name__} ({self.id})>: {self.name}'

    def __repr__(self):
        return self.__str__()

class PriceData(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_start_value = models.BooleanField(null=True, blank=True)
    parent = models.ForeignKey('self', related_name='values', on_delete=models.CASCADE, null=True, blank=True)
    place_type = models.ForeignKey(PlaceType, on_delete=models.CASCADE, null=True, blank=True)
    has_free_amount = models.IntegerField(null=True, blank=True)

    objects = PriceDataManager()

    def __str__(self):
        return f'<{self.__class__.__name__} ({self.id})>: {self.name}'

    def __repr__(self):
        return self.__str__()

    def get_total_value(self):
        if self.value is not None:
            return self.value
        else:
            total_value = sum(child.get_total_value() for child in self.values.all())
            return total_value

    class Meta:
        db_table = 'price_data'