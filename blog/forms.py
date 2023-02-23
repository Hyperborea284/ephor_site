from django import forms
from django.db import models
from datetime import datetime

from .models import BlogPost


class BlogPostForm(forms.Form):
    title = forms.CharField()
    slug = forms.SlugField()
    content = forms.CharField(widget=forms.Textarea)
    timestamp = models.DateTimeField(auto_now_add= True)
    updated = models.DateTimeField(auto_now= True)

class BlogPostModelForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'image', 'slug', 'content', 'publish_date', 'barplot_size', 'plot_min_freq', 'reinert_segm', 'reinert_min_freq', 'reinert_k', 'reinert_min_seg']

    def clean_title(self, *args, **kwargs):
        instance = self.instance
        title = self.cleaned_data.get('title')
        qs = BlogPost.objects.filter(title__iexact=title)
        if instance is not None:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise forms.ValidationError("Título já utilizado, por favor escolha outro que seja diferente.")
        return title
