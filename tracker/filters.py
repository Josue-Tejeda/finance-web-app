import django_filters
from django import forms
from tracker.data import TRANSACTION_TYPE_CHOICES
from tracker.models import Transaction, Category


class TransactionFilter(django_filters.FilterSet):
    transaction_type = django_filters.ChoiceFilter(
        choices=TRANSACTION_TYPE_CHOICES,
        field_name='type',
        lookup_expr='iexact',
        empty_label='Any'
    )
    
    start_date = django_filters.DateFilter(
        field_name='date',
        lookup_expr='gte',
        label='Date From',
        widget=forms.DateInput(attrs={'type':'date'})
    )
    
    end_date = django_filters.DateFilter(
        field_name='date',
        lookup_expr='lte',
        label='Date To',
        widget=forms.DateInput(attrs={'type':'date'})
    )
    
    category = django_filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        label='Categories',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'daisy-checkbox-accent'}),
    )
    
    class Meta:
        model = Transaction
        fields = ('transaction_type', 'start_date', 'end_date', 'category')
        