from django.db import models


class Person(models.Model):
    name = models.CharField('Contact name', max_length=100)

    def __str__(self):
        return self.name
#преобразовывает в строковое представление
    def all_phones_to_string(self):
        return ', '.join([phone.phone for phone in self.phones.all()])


class Phone(models.Model):
    phone = models.CharField('Phone', max_length=50)
    contact = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='phones')

    def __str__(self):
        return self.phone


