from datetime import  timedelta
from django.utils import timezone
import pytest
from django.urls import reverse

from tracker.models import Category


@pytest.mark.django_db
def test_total_values_appearing_on_list_page(user_transactions, client):
    user = user_transactions[0].user
    client.force_login(user)
    
    income_total = sum(t.amount for t in user_transactions if t.type == 'income')
    expense_total = sum(t.amount for t in user_transactions if t.type == 'expense')
    net = income_total - expense_total
    
    response = client.get(reverse('transactions-list'))
    assert response.context['total_income'] == income_total
    assert response.context['total_expenses'] == expense_total
    assert response.context['net_income'] == net
    
@pytest.mark.django_db
def test_transaction_type_filter(user_transactions, client):
    user = user_transactions[0].user
    client.force_login(user)
    
    #income test
    GET_params = {'transaction_type': 'income'}
    response = client.get(reverse('transactions-list'), GET_params)
    
    qs = response.context['filter'].qs
    
    for transaction in qs:
        assert transaction.type == 'income'
        
    #expense test
    GET_params = {'transaction_type': 'expense'}
    response = client.get(reverse('transactions-list'), GET_params)
    
    qs = response.context['filter'].qs
    
    for transaction in qs:
        assert transaction.type == 'expense'


@pytest.mark.django_db
def test_start_date_filter(user_transactions, client):
    user = user_transactions[0].user
    client.force_login(user)
    
    start_date = timezone.now() - timedelta(days=120)
    
    GET_params = {'start_date': start_date}
    response = client.get(reverse('transactions-list'), GET_params)
    
    qs = response.context['filter'].qs
    
    for transaction in qs:
        assert transaction.date >= start_date
        

@pytest.mark.django_db
def test_end_date_filter(user_transactions, client):
    user = user_transactions[0].user
    client.force_login(user)
    
    end_date = timezone.now().date() - timedelta(days=20)
    
    GET_params = {'end_date': end_date}
    response = client.get(reverse('transactions-list'), GET_params)
    
    qs = response.context['filter'].qs
    
    for transaction in qs:
        assert transaction.date <= end_date
        
        
@pytest.mark.django_db
def test_category_filter(user_transactions, client):
    user = user_transactions[0].user
    client.force_login(user)
    
    category_ids = Category.objects.all()[:2].values_list('id', flat=True)
    GET_params = {'category': category_ids}
    
    response = client.get(reverse('transactions-list'), GET_params)
    
    qs = response.context['filter'].qs
    
    for transaction in qs:
        assert transaction.category.id in category_ids
    