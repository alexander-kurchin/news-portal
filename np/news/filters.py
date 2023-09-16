from django import forms
from django_filters import (CharFilter, DateFilter, FilterSet,
                            ModelMultipleChoiceFilter)

from .models import Category, Post


class PostFilterSet(FilterSet):
    title = CharFilter(field_name='title',
                       lookup_expr='icontains',  # TODO: Делает 'contains'
                       label='Название содержит',
                       widget=forms.TextInput(attrs={'class': 'form-control'}),
                       )
    category = ModelMultipleChoiceFilter(field_name='category',
                                         queryset=Category.objects.all(),
                                         label='Категория',
                                         conjoined=True,
                                         widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
                                         )
    after = DateFilter(field_name='created_at',
                       lookup_expr='date__gt',
                       label='Опубликовано после',
                       widget=forms.DateInput(attrs={'type': 'date',  # TODO: Русский формат 'дд-мм-ггг'
                                                     'class': 'form-control'}),
                       )

    class Meta:
        model = Post
        fields = ['title', 'category', 'after']
