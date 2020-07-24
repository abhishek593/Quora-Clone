from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .forms import QuoraUserCreationForm, QuoraUserChangeForm

from .models import QuoraUser, UserFollowing


class QuoraUserAdmin(BaseUserAdmin):
    form = QuoraUserChangeForm
    add_form = QuoraUserCreationForm

    list_display = ('email', 'username', 'first_name', 'is_admin')
    list_filter = ('is_admin',)

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password', 'description')}),
        ('Personal info', {'fields': ('date_of_birth', 'first_name', 'last_name',)}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'date_of_birth', 'password1', 'password2'),
        }),
    )
    search_fields = ('username', 'email',)
    ordering = ('email', 'username')
    filter_horizontal = ()


admin.site.register(QuoraUser, QuoraUserAdmin)
admin.site.register(UserFollowing)
admin.site.unregister(Group)
