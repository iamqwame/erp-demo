from django.db import models

class Account(models.Model):
    """
    Represents an account in the chart of accounts, standalone.
    """
    account_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20, unique=True)
    account_type = models.CharField(
        max_length=50,
        choices=[('asset', 'Asset'), ('liability', 'Liability'), ('income', 'Income'), ('expense', 'Expense')]
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


