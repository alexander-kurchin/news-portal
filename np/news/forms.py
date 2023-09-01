from django import forms
from .models import Category, Post


class PostForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(label='Категория',
                                              queryset=Category.objects.all(),
                                              widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
                                              )
    title = forms.CharField(label='Заголовок',
                            widget=forms.TextInput(attrs={'class': 'form-control'}),
                            )
    text = forms.Field(label='Текст',
                       widget=forms.Textarea(attrs={'class': 'form-control'}),
                       )

    class Meta:
        model = Post
        fields = ['category', 'title', 'text']
