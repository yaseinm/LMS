from django.contrib import admin
from .models import Category, Course, CourseRegistration, Enrollment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["title", "instructor", "category", "price", "level", "is_published"]
    list_filter = ["category", "level", "is_published"]
    search_fields = ["title", "description", "instructor"]
    prepopulated_fields = {"slug": ("title",)}


@admin.register(CourseRegistration)
class CourseRegistrationAdmin(admin.ModelAdmin):
    list_display = ["full_name", "email", "phone", "course_name", "is_paid", "registered_at"]
    list_filter = ["is_paid", "course_name", "registered_at"]
    search_fields = ["full_name", "email", "phone"]


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ["user", "course", "enrolled_at"]
    list_filter = ["enrolled_at"]
