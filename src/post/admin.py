from django.contrib.admin.filters import (ChoicesFieldListFilter,
                                          DateFieldListFilter)

from models import Post
from post.forms import (PageChangeFormAdmin, PageCreationFormAdmin,
                        PostChangeFormAdmin, PostCreationFormAdmin)
from post.models import Page
from utility.admin import AdminChangeMixin, register_model_admin


class PostAdmin(AdminChangeMixin):
    change_form = PostChangeFormAdmin
    add_form = PostCreationFormAdmin
    change_own_field = "author__id"
    change_own_owner_field = "id"
    
    add_form_template = "admin/add_files_form.html"
    
    icon = '<i class="material-icons">description</i>'

    list_display = ('short_name', 'author', 'fileLink', 'location', 'date', 'slug',)
    list_filter = (
        ('date', DateFieldListFilter),
        ('author__status', ChoicesFieldListFilter)
    )
    readonly_fields = ['fileLink', 'author', 'location']

    fieldsets = ()
    change_fieldsets = (
        ('File', {'fields': ('name', 'author', ('file', 'location'))}),
    )
    
    add_fieldsets = (
        ('File', {'fields': ('name', 'file')}),
    )
    
    search_fields = ('author__first_name', 'author__last_name', 'name', 'date', 'slug',)

    ordering = ['date']
    filter_horizontal = ()
      
    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            self.fieldsets = self.add_fieldsets
            form = self.add_form
            form.current_user = request.user
            return form
        else:
            self.fieldsets = self.change_fieldsets
            return self.change_form
          

class PageAdmin(AdminChangeMixin):
    change_form = PageChangeFormAdmin
    add_form = PageCreationFormAdmin
    change_own_field = "author__id"
    change_own_owner_field = "id"
    
    icon = '<i class="material-icons">description</i>'

    list_display = ('name', 'author', 'fileLink', 'date', 'slug',)
    list_filter = (
        ('date', DateFieldListFilter),
    )
    readonly_fields = ['fileLink', 'author']

    fieldsets = ()
    change_fieldsets = (
        ('Page', {'fields': ('name', 'author')}),
        ('Page content', {'fields': ('text', 'file')})
    )
    
    add_fieldsets = (
        ('Page', {'fields': ('name',)}),
        ('Page content', {'fields': ('text', 'file')})
    )
    
    search_fields = ('author__first_name', 'author__last_name', 'name', 'date', 'slug',)

    ordering = ['date']
    filter_horizontal = ()
      
    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            self.fieldsets = self.add_fieldsets
            form = self.add_form
            form.current_user = request.user
            return form
        else:
            self.fieldsets = self.change_fieldsets
            form = self.change_form
            form.text_initial = obj.text
            return form
    
    pass
    
register_model_admin(Post, PostAdmin)
register_model_admin(Page, PageAdmin)
