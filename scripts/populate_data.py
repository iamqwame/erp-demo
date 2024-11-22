import os
import random
import sys
import django

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.abspath(os.path.join(current_dir, '..')) 
sys.path.append(src_dir) 


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.config.settings.development') 
django.setup()


from src.apps.customers.models import Customer
from src.apps.vendors.models import Vendor
from src.apps.accounts.models import Account


def clear_data():
    """
    Clear old data from the database tables.
    """
    print("Clearing old data...")
    Customer.objects.all().delete()
    Vendor.objects.all().delete()
    Account.objects.all().delete()
    print("Old data cleared successfully.")


def populate_customers(n=10):
    """
    Populate the Customer table with sample data.
    """
    print(f"Creating {n} customers...")
    for i in range(n):
        Customer.objects.create(
            name=f"Customer {i+1}",
            email=f"customer{i+1}@example.com",
            phone=f"555-010{i+1}",
            address=f"Address {i+1}",
            date_of_birth="1990-01-01",  
        )
    print(f"{n} customers created successfully.")


def populate_vendors(n=10):
    """
    Populate the Vendor table with sample data.
    """
    print(f"Creating {n} vendors...")
    for i in range(n):
        Vendor.objects.create(
            name=f"Vendor {i+1}",
            email=f"vendor{i+1}@example.com",
            phone=f"555-020{i+1}",
            address=f"Vendor Address {i+1}",
            contact_person=f"Contact Person {i+1}",
        )
    print(f"{n} vendors created successfully.")


def populate_accounts(n=10):
    """
    Populate the Account table with sample data.
    """
    account_types = ['asset', 'liability', 'income', 'expense']
    print(f"Creating {n} accounts...")
    for i in range(n):
        Account.objects.create(
            name=f"Account {i+1}",
            code=f"A{i+1:04}",  
            account_type=random.choice(account_types),
            description=f"Description for Account {i+1}",
        )
    print(f"{n} accounts created successfully.")


if __name__ == "__main__":
    clear_data()  # Clear old data first
    populate_customers(10000)
    populate_vendors(100000)
    populate_accounts(100000)
    print("Sample data added successfully.")
