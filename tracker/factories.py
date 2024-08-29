from django.utils import timezone
import factory
from tracker.data import TRANSACTION_TYPE_CHOICES
from tracker.models import Category, Transaction, User

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)
        
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.Sequence(lambda n: 'user%d' % n)
    
    
class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model= Category
        django_get_or_create = ('name',)
    
    name = factory.Iterator(
        ['Bills', 'Housing', 'Salary', 'Food', 'Social']
    )
    

class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model= Transaction
        
    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
    amount = 5
    date = factory.Faker(
        'date_between',
        start_date=timezone.now().replace(hour=15, minute=45, second=0),
        end_date=timezone.now().date()
    )
    type = factory.Iterator(
        [
            x[0] for x in TRANSACTION_TYPE_CHOICES
        ]
    )