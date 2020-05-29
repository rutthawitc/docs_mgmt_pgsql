from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, UserProfile, UserDepartment, UserSection, Documents, DocumentSections, Accepted, Comments, RefDocumentType

# Register your models here.
class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'UserProfile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username','first_name', 'last_name', 'get_role', 'is_staff')
    list_select_related = ('profile', )

    def get_role(self, instance):
        return instance.profile.get_role_display()
    get_role.short_description = 'Role'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


class DocumentsAdmin(admin.ModelAdmin):
    exclude = ('upload_by', 'access_count', 'doc_dept')

    def save_model(self, request, obj, form, change):
        obj.upload_by = request.user.profile
        obj.doc_dept = request.user.profile.dept
        obj.save()

admin.site.register(UserDepartment)
admin.site.register(UserSection)
admin.site.register(UserProfile)
admin.site.register(Documents, DocumentsAdmin)
admin.site.register(Accepted)
admin.site.register(Comments)
admin.site.register(RefDocumentType)

#UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)