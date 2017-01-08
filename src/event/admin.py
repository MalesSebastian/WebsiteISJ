from django.contrib import admin
from models import Event
from view_permission.admin import AdminViewMixin
from django import forms
# Register your models here.

class EventCreationForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'description', 'image', 'time', 'location')

    def save(self, commit=True):
        event = super(EventCreationForm, self).save(commit=False)
        event.author = self.current_user
        if commit:
            event.save()
        return event

class EventAdmin(AdminViewMixin):
    add_form = EventCreationForm
    icon = '<i class="material-icons">room</i>'

    list_display = ('title', 'author', 'location', 'time',)
    readonly_fields = ['author']
    
    search_fields = ('title', 'author__first_name', 'author__last_name', 'location', 'time',)

    ordering = ['time']
    filter_horizontal = ()
    
    change_fieldsets = (
        ('Event Info', {'fields': ('title', 'author', 'description', 'image')}),
        ('Location and Time', {'fields': ('time', 'location')}),
    )
    
    add_fieldsets = (
        ('Event Info', {'fields': ('title', 'description', 'image')}),
        ('Location and Time', {'fields': ('time', 'location')}),
    )
      
    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            self.fieldsets = self.add_fieldsets
            form = self.add_form
            form.current_user = request.user
            return form
        else:
            self.fieldsets = self.change_fieldsets
            return super(EventAdmin, self).get_form(request, obj)
    
    pass
    
admin.site.register(Event, EventAdmin)