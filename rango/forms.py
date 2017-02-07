from django import forms
from .models import Page, Category


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Enter the category name")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Category

        fields = ('name', 'views', 'likes')


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Enter the page name")
    url = forms.URLField(max_length=200, help_text="please enter the url of the page")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)


    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url

        return cleaned_data

    class Meta:
        model = Page

        fields = ('title', 'url', 'views')