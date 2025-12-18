from django.db import models
from django.contrib.auth.models import User
from Categories.models import Category
# Create your models here.


class TransactionType(models.TextChoices):
    PAYMENT = 'Payment', 'payment'
    SALARY = 'Salary', 'salary'


class TransactionStatus(models.TextChoices):
    COMPLETED = 'Completed', 'completed'
    CANCELLED = 'Cancelled', 'cancelled'

class Transaction(models.Model):
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(
        Category,on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions'
    )
    type = models.CharField(max_length=7, choices=TransactionType.choices, default=TransactionType.PAYMENT)
    status = models.CharField(max_length=9, choices=TransactionStatus.choices, default=TransactionStatus.COMPLETED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}-{abs(self.amount)}-{self.currency}'