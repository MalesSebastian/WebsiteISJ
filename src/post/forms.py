import os

from django import forms

from models import Post
from post.models import Page
from tinymce.widgets import TinyMCE, AdminTinyMCE


class CreatePostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['name', 'file']
        widgets = {'name': forms.TextInput(attrs={'required': 'required'})}

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CreatePostForm, self).__init__(*args, **kwargs)

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        max_size = 10000000  # 10 MB
        filename, file_type = os.path.splitext(uploaded_file.name)
        allowed_file_types = [
            '.doc', '.docx', '.docm', '.xls', '.xlsx', '.ppt',
            '.ppt', '.pps', '.zip', '.rar', '.jpg', '.jpeg'
            '.png', '.gif', '.bmp', '.txt', '.tif', '.rtf', '.pdf',
            '.odt', '.ace', '.ods', '.odg'
        ]
        if not(any(file_type in type for type in allowed_file_types)):
            raise forms.ValidationError("Fisierul nu se incadreaza in extensile permise")
        if uploaded_file.size > max_size:
            raise forms.ValidationError("Fisierul trece de dimensiunea maxima de %d" % max_size)

        return uploaded_file


class FilterPostForm(forms.Form):
    time = forms.CharField(max_length=30)
    user_status = forms.IntegerField()
    
class PostCreationFormAdmin(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('name', 'file',)

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        max_size = 10000000  # 10 MB
        filename, file_type = os.path.splitext(uploaded_file.name)
        allowed_file_types = [
            '.doc', '.docx', '.docm', '.xls', '.xlsx', '.ppt',
            '.ppt', '.pps', '.zip', '.rar', '.jpg', '.jpeg'
            '.png', '.gif', '.bmp', '.txt', '.tif', '.rtf', '.pdf',
            '.odt', '.ace', '.ods', '.odg'
        ]
        if not(any(file_type in type for type in allowed_file_types)):
            raise forms.ValidationError("Fisierul nu se incadreaza in extensile permise")
        if uploaded_file.size > max_size:
            raise forms.ValidationError("Fisierul trece de dimensiunea maxima de %d" % max_size)

        return uploaded_file

    def save(self, commit=True):
        uploaded_file = super(PostCreationFormAdmin, self).save(commit=False)
        uploaded_file.author = self.current_user
        if commit:
            uploaded_file.save()
        return uploaded_file


class PostChangeFormAdmin(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('name', 'file')

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        max_size = 10000000  # 10 MB
        filename, file_type = os.path.splitext(uploaded_file.name)
        allowed_file_types = [
            '.doc', '.docx', '.docm', '.xls', '.xlsx', '.ppt',
            '.ppt', '.pps', '.zip', '.rar', '.jpg', '.jpeg'
            '.png', '.gif', '.bmp', '.txt', '.tif', '.rtf', '.pdf',
            '.odt', '.ace', '.ods', '.odg'
        ]
        if not(any(file_type in type for type in allowed_file_types)):
            raise forms.ValidationError("Fisierul nu se incadreaza in extensile permise")
        if uploaded_file.size > max_size:
            raise forms.ValidationError("Fisierul trece de dimensiunea maxima de %d" % max_size)

        return uploaded_file
      
class PageCreationFormAdmin(forms.ModelForm):
    text = forms.CharField(widget=AdminTinyMCE(attrs={'cols': 80, 'rows': 30}), label='')
    class Meta:
        model = Page
        fields = ('name', 'file',)
        
    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        max_size = 10000000  # 10 MB
        filename, file_type = os.path.splitext(uploaded_file.name)
        allowed_file_types = [
            '.doc', '.docx', '.docm', '.xls', '.xlsx', '.ppt',
            '.ppt', '.pps', '.zip', '.rar', '.jpg', '.jpeg'
            '.png', '.gif', '.bmp', '.txt', '.tif', '.rtf', '.pdf',
            '.odt', '.ace', '.ods', '.odg'
        ]
        if not(any(file_type in type for type in allowed_file_types)):
            raise forms.ValidationError("Fisierul nu se incadreaza in extensile permise")
        if uploaded_file.size > max_size:
            raise forms.ValidationError("Fisierul trece de dimensiunea maxima de %d" % max_size)

        return uploaded_file

    def save(self, commit=True):
        uploaded_file = super(PageCreationFormAdmin, self).save(commit=False)
        uploaded_file.author = self.current_user
        uploaded_file.text = self.cleaned_data['text']
        if commit:
            uploaded_file.save()
        return uploaded_file

class PageChangeFormAdmin(forms.ModelForm):
    text = forms.CharField(widget=AdminTinyMCE(attrs={'cols': 80, 'rows': 30}), label='')
    class Meta:
        model = Page
        fields = ('name', 'file')
        
    def __init__(self, *args, **kwargs):
        initial = {
          'text': self.text_initial
        }
        kwargs['initial'] = initial
        super(PageChangeFormAdmin, self).__init__(*args, **kwargs)
        
    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        max_size = 10000000  # 10 MB
        filename, file_type = os.path.splitext(uploaded_file.name)
        allowed_file_types = [
            '.doc', '.docx', '.docm', '.xls', '.xlsx', '.ppt',
            '.ppt', '.pps', '.zip', '.rar', '.jpg', '.jpeg'
            '.png', '.gif', '.bmp', '.txt', '.tif', '.rtf', '.pdf',
            '.odt', '.ace', '.ods', '.odg'
        ]
        if not(any(file_type in type for type in allowed_file_types)):
            raise forms.ValidationError("Fisierul nu se incadreaza in extensile permise")
        if uploaded_file.size > max_size:
            raise forms.ValidationError("Fisierul trece de dimensiunea maxima de %d" % max_size)

        return uploaded_file
      
    def save(self, commit=True):
        uploaded_file = super(PageChangeFormAdmin, self).save(commit=False)
        uploaded_file.text = self.cleaned_data['text']
        if commit:
            uploaded_file.save()
        return uploaded_file