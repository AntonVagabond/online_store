from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from customers.models.customers import Customer
from customers.models.profile import Profile


class ProfileAdmin(admin.StackedInline):
    model = Profile
    fields = ('photo',)


@admin.register(Customer)
class CustomerAdmin(UserAdmin):
    change_user_password_template = None
    fieldsets = (
        (None,
         {'fields': ('phone_number', 'email', 'username')}),
        (_('Личная информация'),
         {'fields': ('first_name', 'last_name',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser',
                       'groups', 'user_permissions',)
        }),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'password1', 'password2',),
        }),
    )
    list_display = ('id', 'full_name', 'email', 'phone_number',)

    list_display_links = ('id', 'full_name',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('first_name', 'last_name', 'id', 'email', 'phone_number',)
    ordering = ('-id',)
    filter_horizontal = ('groups', 'user_permissions',)
    readonly_fields = ('last_login',)

    inlines = (ProfileAdmin,)
