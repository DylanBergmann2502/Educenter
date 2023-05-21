from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import MyUserCreationForm, MyUserChangeForm
from .models import Major, Teacher
from .models import MyUser


class MyUserAdmin(UserAdmin):
    add_form = MyUserCreationForm
    form = MyUserChangeForm
    model = MyUser
    list_display = ("email","is_superuser", "is_staff","is_teacher","is_student")
    list_filter = ("email", "is_staff","is_teacher")
    fieldsets = (
        (None, {"fields": ("email","full_name", "phone", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_teacher", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "full_name", "phone", "is_teacher","is_staff","password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(MyUser, MyUserAdmin)


admin.site.register(Major)
admin.site.register(Teacher)
