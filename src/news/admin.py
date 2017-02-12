from django.contrib import admin

from .models import News
from view_permission.admin import AdminViewMixin
from news.forms import NewsCreationFormAdmin, NewsChangeFormAdmin


class NewsAdmin(AdminViewMixin):    
    change_form = NewsChangeFormAdmin
    add_form = NewsCreationFormAdmin
    
    icon = '<i class="material-icons">rss_feed</i>'

    list_display = ('short_name', 'author', 'fileLink', 'date', 'slug',)
    readonly_fields = ['fileLink', 'author']

    fieldsets = ()
    change_fieldsets = (
        ('Page', {'fields': ('name', 'author', 'date')}),
        ('News content', {'fields': ('text', 'file')})
    )
    
    add_fieldsets = (
        ('Page', {'fields': ('name', 'date')}),
        ('News content', {'fields': ('text', 'file')})
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

admin.site.register(News, NewsAdmin)
