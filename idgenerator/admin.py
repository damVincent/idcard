from django.contrib import admin
from django.utils.html import format_html
from .models import Student, StudentIdentityCard

class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'middle_name', 'last_name', 'date_of_birth', 'student_id', 'issuance_date', 'expiry_date', 'preview_photo', 'preview_logo')

    def preview_photo(self, obj):
        return format_html('<img src="{}" width="50" height="50" />'.format(obj.photo.url))

    def preview_logo(self, obj):
        return format_html('<img src="{}" width="50" height="50" />'.format(obj.logo.url))

admin.site.register(Student, StudentAdmin)

class StudentIdentityCardAdmin(admin.ModelAdmin):
    list_display = ('student', 'preview_id')
    
    def preview_id(self, obj):
        return format_html('<img src="{}" width="50" height="50" />'.format(obj.image_file.url))
    
admin.site.register(StudentIdentityCard, StudentIdentityCardAdmin)