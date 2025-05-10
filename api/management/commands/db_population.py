import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import lorem_ipsum
from api.models import CustomUser, Product, Order, OrderItem

class Command(BaseCommand):
    help = 'Creates application data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')
        
        # get or create superuser
        user = CustomUser.objects.filter(username='admin').first()
        if not user:
            user = CustomUser.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='test'
            )
            self.stdout.write(self.style.SUCCESS('Superuser created'))

        # create products
        products = [
            Product(name="A Scanner Darkly", description=lorem_ipsum.paragraph(), price=Decimal('12.99'), stock=4),
            Product(name="Coffee Machine", description=lorem_ipsum.paragraph(), price=Decimal('70.99'), stock=6),
            Product(name="Velvet Underground & Nico", description=lorem_ipsum.paragraph(), price=Decimal('15.99'), stock=11),
            Product(name="Enter the Wu-Tang (36 Chambers)", description=lorem_ipsum.paragraph(), price=Decimal('17.99'), stock=2),
            Product(name="Digital Camera", description=lorem_ipsum.paragraph(), price=Decimal('350.99'), stock=4),
            Product(name="Watch", description=lorem_ipsum.paragraph(), price=Decimal('500.05'), stock=0),
        ]

        # create products & re-fetch from DB
        Product.objects.bulk_create(products)
        self.stdout.write(self.style.SUCCESS(f'Created {len(products)} products'))
        
        products = Product.objects.all()

        # create dummy orders
        for i in range(3):
            order = Order.objects.create(user=user)
            for product in random.sample(list(products), 2):
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=random.randint(1,3)
                )
            self.stdout.write(self.style.SUCCESS(f'Created order {i+1}'))

        self.stdout.write(self.style.SUCCESS('Sample data creation completed!'))