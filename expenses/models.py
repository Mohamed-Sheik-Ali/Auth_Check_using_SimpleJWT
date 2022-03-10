from django.db import models
from SimpApp.models import MyUser
# Create your models here.


class Expense(models.Model):

    CATEGORY_OPTIONS = [
        ('ONLINE_SERVICES', 'ONLINE_SERVICES'),
        ('TRAVEL', 'TRAVEL'),
        ('FOOD', 'FOOD'),
        ('RENT', 'RENT'),
        ('OTHERS', 'OTHERS'),
    ]

    category = models.CharField(choices=CATEGORY_OPTIONS, max_length=255)

    amount = models.DecimalField(
        max_digits=10, decimal_places=2, max_length=255)

    description = models.TextField()

    owner = models.ForeignKey(to=MyUser, on_delete=models.CASCADE)

    date = models.DateField(null=False, blank=False)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return str(self.owner)+'\'s expenses.'
