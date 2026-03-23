from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Course, Category, Enrollment


def course_list(request):
    courses = Course.objects.filter(is_published=True)
    categories = Category.objects.all()

    category_slug = request.GET.get("category")
    if category_slug:
        courses = courses.filter(category__slug=category_slug)

    level = request.GET.get("level")
    if level:
        courses = courses.filter(level=level)

    search = request.GET.get("q")
    if search:
        courses = courses.filter(title__icontains=search)

    return render(request, "courses/course_list.html", {
        "courses": courses,
        "categories": categories,
        "selected_category": category_slug,
        "selected_level": level,
        "search_query": search or "",
    })


def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(
            user=request.user, course=course
        ).exists()
    return render(request, "courses/course_detail.html", {
        "course": course,
        "is_enrolled": is_enrolled,
    })


@login_required
def my_courses(request):
    enrollments = Enrollment.objects.filter(user=request.user).select_related("course")
    return render(request, "courses/my_courses.html", {"enrollments": enrollments})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("course_list")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})
