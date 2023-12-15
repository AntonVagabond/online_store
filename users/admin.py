from typing import Union

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe, SafeString
from django.utils.translation import gettext_lazy as _

from users.models.users import User
from users.models.profile import Profile


# region ----------------------------- INLINE ---------------------------------------
class ProfileAdmin(admin.TabularInline):
    """
    Встраиваемая модель профиля для UserAdmin.

    Аттрибуты:
        * `model` (Profile): модель профиля.
        * `fields` (tuple[str]): поля.
        * `readonly_fields` (tuple[str]): поля для чтения.
    """

    model = Profile
    fields = ('photo', 'photo_show')
    readonly_fields = ('photo_show',)

    @admin.display(description='Логотип', ordering='photo')
    def photo_show(self, obj: Profile) -> Union[SafeString, str]:
        if obj.photo:
            return mark_safe(f"<img src='{obj.photo.url}' width='60' />")
        return 'Нет фотографии'


# endregion -------------------------------------------------------------------------


# region -------------------------- MODEL ADMIN -------------------------------------
@admin.register(User)
class UserAdmin(UserAdmin):
    """
    Модель админа пользователя.

    Аттрибуты:
        * `change_user_password_template` (None): изменить шаблон пароля пользователя.
        * `fieldsets` (tuple[tuple[...]]): наборы полей.
        * `add_fieldsets` (tuple[tuple[...]]): добавление наборов полей.
        * `list_display` (tuple[str]): отображение списка.
        * `list_filter` (tuple[str]): фильтр списка.
        * `search_fields` (tuple[str]): поле для поиска.
        * `filter_horizontal` (tuple[str]): горизонтальная фильтрация.
        * `readonly_fields` (tuple[str]): поле для чтения.
        * `inlines` (tuple[ProfileAdmin]): встроенные.
    """
    # region -------------- АТРИБУТЫ МОДЕЛИ АДМИНА ПОЛЬЗОВАТЕЛЯ ---------------------
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
    # endregion ---------------------------------------------------------------------
# endregion -------------------------------------------------------------------------

