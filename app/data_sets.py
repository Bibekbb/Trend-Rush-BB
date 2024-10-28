
from django.core.management.base import BaseCommand
import pandas as pd
from app.models import Product

class Command(BaseCommand):
    help = 'Load dataset to the database'

    def handle(self, *args, **options):
        dataset_path = 'datasetsknn.csv'
        df = pd.read_csv('datasetsknn.csv')

        for _, row in df.iterrows():
            Product.objects.create(
                name=row['Product Name'],
                price=row['Price'],
                category=row['Category'],
                brand=row['Brand'],
            )
