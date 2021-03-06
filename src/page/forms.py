# Copyright 2017 Adrian-Ioan Garovat, Emanuel Covaci, Sebastian-Valeriu Males
#
# This file is part of WebsiteISJ
#
# WebsiteISJ is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# WebsiteISJ is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WebsiteISJ.   If not, see <http://www.gnu.org/licenses/>.
from django import forms
from page.models import Article
from page.models import SimplePage
from page.models import Category
from tinymce.widgets import AdminTinyMCE
from utility.utility import clean_file


class ArticleCreationFormAdmin(forms.ModelForm):
    text = forms.CharField(widget=AdminTinyMCE(attrs={'cols': 80, 'rows': 30}),
                           label='')
    show_files = True
    show_preview = True
    preview_url = "/preview_news/"

    class Meta:
        model = Article
        fields = ('subcategory', 'name', 'file')

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        error = clean_file(uploaded_file, image=True)
        if error:
            raise forms.ValidationError(error)
        return uploaded_file

    def save(self, commit=True):
        uploaded_file = super(ArticleCreationFormAdmin, self).save(
            commit=False)
        uploaded_file.author = self.current_user
        uploaded_file.text = self.cleaned_data['text']
        if commit:
            uploaded_file.save()
        return uploaded_file


class ArticleChangeFormAdmin(forms.ModelForm):
    text = forms.CharField(widget=AdminTinyMCE(attrs={'cols': 80, 'rows': 30}),
                           label='')
    show_files = True
    show_preview = True
    preview_url = "/preview_news/"

    class Meta:
        model = Article
        fields = ('subcategory', 'name', 'file')

    def __init__(self, *args, **kwargs):
        initial = {
            'text': self.text_initial
        }
        kwargs['initial'] = initial
        super(ArticleChangeFormAdmin, self).__init__(*args, **kwargs)

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        error = clean_file(uploaded_file, image=True)
        if error:
            raise forms.ValidationError(error)
        return uploaded_file

    def save(self, commit=True):
        uploaded_file = super(ArticleChangeFormAdmin, self).save(commit=False)
        uploaded_file.text = self.cleaned_data['text']
        if commit:
            uploaded_file.save()
        return uploaded_file


class SimplePageCreationFormAdmin(forms.ModelForm):
    text = forms.CharField(
        widget=AdminTinyMCE(attrs={'cols': 80, 'rows': 30}),
        label='')
    show_files = True
    show_preview = True
    preview_url = "/preview_news/"

    class Meta:
        model = SimplePage
        fields = ('category', 'name', 'file')

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        error = clean_file(uploaded_file, image=True)
        if error:
            raise forms.ValidationError(error)
        return uploaded_file

    def save(self, commit=True):
        uploaded_file = super(SimplePageCreationFormAdmin, self).save(
            commit=False)
        uploaded_file.author = self.current_user
        uploaded_file.text = self.cleaned_data['text']
        if commit:
            uploaded_file.save()
        return uploaded_file


class SimplePageChangeFormAdmin(forms.ModelForm):
    text = forms.CharField(widget=AdminTinyMCE(attrs={'cols': 80, 'rows': 30}),
                           label='')
    show_files = True
    show_preview = True
    preview_url = "/preview_news/"

    class Meta:
        model = SimplePage
        fields = ('category', 'name', 'file')

    def __init__(self, *args, **kwargs):
        initial = {
            'text': self.text_initial
        }
        kwargs['initial'] = initial
        super(SimplePageChangeFormAdmin, self).__init__(*args, **kwargs)

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        error = clean_file(uploaded_file, image=True)
        if error:
            raise forms.ValidationError(error)
        return uploaded_file

    def save(self, commit=True):
        uploaded_file = super(SimplePageChangeFormAdmin, self).save(
            commit=False)
        uploaded_file.text = self.cleaned_data['text']
        if commit:
            uploaded_file.save()
        return uploaded_file


class CategoryCreationFormAdmin(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('title', 'order')

    def clean_order(self):
        order = self.cleaned_data['order']
        number_of_categories = Category.objects.all().count()
        if order > number_of_categories or order < 1:
            order = number_of_categories + 1
        else:
            try:
                category_to_swap = Category.objects.get(order=order)
                category_to_swap.order = number_of_categories + 1
                category_to_swap.save()
            except Category.DoesNotExist:
                pass
        return order


class CategoryChangeFormAdmin(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('title', 'order')

    def __init__(self, *args, **kwargs):
        initial = {
            'order': self.order_initial
        }
        kwargs['initial'] = initial
        super(CategoryChangeFormAdmin, self).__init__(*args, **kwargs)

    def clean_order(self):
        order = self.cleaned_data['order']
        initial_order = self.order_initial
        number_of_categories = Category.objects.all().count()
        if order > number_of_categories or order < 1:
            order = initial_order
        else:
            try:
                category_to_swap = Category.objects.get(order=order)
                category_to_swap.order = initial_order
                category_to_swap.save()
            except Category.DoesNotExist:
                pass
        return order
