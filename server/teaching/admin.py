from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import UserTeachingProfile, Course, Cls


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    search_fields = ['name',]
    #list_display = ['name', 'language', ]

@admin.register(Cls)
class ClsAdmin(admin.ModelAdmin):
    search_fields = ['name',]
    #list_display = ['name', 'language', ]

# @admin.register(CourseDetail)
# class CourseDetailAdmin(admin.ModelAdmin):
#     search_fields = []
#     list_display = ['course', 'homework', 'grade', 'type', 'cid', 'gid', 'idx']
#     #filter_horizontal = ('stages',)


# @admin.register(Cls)
# class ClsAdmin(admin.ModelAdmin):
#     list_display = ['name', 'address', 'teacher', 'start_time', \
#                     'end_time', 'enable', 'finish']

# @admin.register(Homework)
# class HomeworkAdmin(admin.ModelAdmin):
#     search_fields = []
#     list_display = ['name', 'teacher', 'end_time', 'pub_time', ]


# @admin.register(HomeworkDetail)
# class HomeworkDetailAdmin(admin.ModelAdmin):
#     search_fields = []
#     list_display = ['homework', 'type', 'gid', 'cid', ]


# @admin.register(Exam)
# class ExamAdmin(admin.ModelAdmin):
#     search_fields = []
#     list_display = ['title', 'enter_start_time', 'enter_end_time', 'start_time', 'end_time', 'category', 'finish', \
#                   'enable', 'create_user', 'pub', 'show_school', 'submit_count']

# @admin.register(ExamDetail)
# class ExamDetailAdmin(admin.ModelAdmin):
#     search_fields = []
#     list_display = ['exam', 'type', 'cid', 'gid',]

@admin.register(UserTeachingProfile)
class UserTeachingProfileAdmin(admin.ModelAdmin):
    search_fields = []
    #list_display = ['exam', 'type', 'cid', 'gid',]

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'last_name', 'first_name', 'is_active', 'is_staff')

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)