from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Profile, TutorProfile, StudentProfile, InstituteProfile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"
    fk_name = "user"


class CustomUserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "get_user_type",
    )
    list_select_related = ("profile",)

    @admin.display(description="User Type", ordering="profile__user_type")
    def get_user_type(self, obj):
        try:
            return obj.profile.get_user_type_display()
        except Profile.DoesNotExist:
            return "-"


# Re-register UserAdmin with the inline
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "user_type", "user_firstname", "user_lastname", "date_joined")
    list_filter = ("user_type", "date_joined")
    search_fields = ("user__username", "user__email", "user_firstname", "user_lastname", "user_cedulaid")
    raw_id_fields = ("user",)


@admin.register(TutorProfile)
class TutorProfileAdmin(admin.ModelAdmin):
    list_display = ("profile", "is_verified")
    list_filter = ("is_verified",)
    search_fields = (
        "profile__user__username",
        "profile__user_firstname",
        "profile__user_lastname",
    )
    raw_id_fields = ("profile",)


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("profile", "grade_level")
    list_filter = ("grade_level",)
    search_fields = (
        "profile__user__username",
        "profile__user_firstname",
        "profile__user_lastname",
    )
    raw_id_fields = ("profile",)


@admin.register(InstituteProfile)
class InstituteProfileAdmin(admin.ModelAdmin):
    list_display = ("profile", "institute_name", "owner_fullname", "is_verified")
    list_filter = ("is_verified",)
    search_fields = (
        "institute_name",
        "owner_fullname",
        "profile__user__username",
    )
    raw_id_fields = ("profile",)
