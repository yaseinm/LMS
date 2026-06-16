from django.core.management.base import BaseCommand
from courses.models import Category, Course


class Command(BaseCommand):
    help = "Seed the database with sample courses"

    def handle(self, *args, **options):
        categories = {
            "web-development": ("Web Development", "Learn to build modern web applications"),
            "data-science": ("Data Science", "Master data analysis and machine learning"),
            "mobile-dev": ("Mobile Development", "Build iOS and Android applications"),
            "devops": ("DevOps", "Learn deployment, CI/CD, and cloud infrastructure"),
            "design": ("Design", "UI/UX design and creative tools"),
        }

        cat_objects = {}
        for slug, (name, desc) in categories.items():
            cat, _ = Category.objects.get_or_create(slug=slug, defaults={"name": name, "description": desc})
            cat_objects[slug] = cat

        courses = [
            {
                "title": "Complete Python Bootcamp",
                "slug": "complete-python-bootcamp",
                "description": "Learn Python from scratch to advanced level. This comprehensive course covers everything from basic syntax to object-oriented programming, web scraping, data analysis, and building real-world projects. Perfect for beginners who want to become proficient Python developers.",
                "short_description": "Master Python programming from zero to hero with hands-on projects.",
                "instructor": "Dr. Sarah Johnson",
                "category": cat_objects["web-development"],
                "price": 89.99,
                "discount_price": 49.99,
                "level": "beginner",
                "duration_hours": 42,
            },
            {
                "title": "React & Next.js Masterclass",
                "slug": "react-nextjs-masterclass",
                "description": "Build modern, production-ready web applications with React and Next.js. Learn component architecture, state management, server-side rendering, API routes, and deployment strategies. Includes 10 real-world projects.",
                "short_description": "Build production-ready apps with React and Next.js.",
                "instructor": "Alex Chen",
                "category": cat_objects["web-development"],
                "price": 129.99,
                "level": "intermediate",
                "duration_hours": 58,
            },
            {
                "title": "Machine Learning A-Z",
                "slug": "machine-learning-az",
                "description": "Comprehensive machine learning course covering supervised learning, unsupervised learning, deep learning, and reinforcement learning. Work with real datasets and build models using Python, scikit-learn, and TensorFlow.",
                "short_description": "Complete guide to machine learning with Python and TensorFlow.",
                "instructor": "Prof. Michael Torres",
                "category": cat_objects["data-science"],
                "price": 149.99,
                "discount_price": 99.99,
                "level": "intermediate",
                "duration_hours": 65,
            },
            {
                "title": "iOS App Development with Swift",
                "slug": "ios-swift-development",
                "description": "Learn to build beautiful iOS applications using Swift and SwiftUI. Cover the fundamentals of iOS development, UIKit, SwiftUI, Core Data, networking, and App Store submission process.",
                "short_description": "Create stunning iOS apps with Swift and SwiftUI.",
                "instructor": "Emily Park",
                "category": cat_objects["mobile-dev"],
                "price": 119.99,
                "level": "beginner",
                "duration_hours": 48,
            },
            {
                "title": "Docker & Kubernetes in Production",
                "slug": "docker-kubernetes-production",
                "description": "Master containerization and orchestration for production environments. Learn Docker fundamentals, multi-stage builds, Kubernetes architecture, Helm charts, monitoring, and CI/CD pipeline integration.",
                "short_description": "Deploy and manage containers at scale with Docker & K8s.",
                "instructor": "James Wilson",
                "category": cat_objects["devops"],
                "price": 139.99,
                "discount_price": 89.99,
                "level": "advanced",
                "duration_hours": 38,
            },
            {
                "title": "UI/UX Design Fundamentals",
                "slug": "uiux-design-fundamentals",
                "description": "Learn the principles of great user interface and user experience design. Cover design thinking, wireframing, prototyping, user research, accessibility, and tools like Figma.",
                "short_description": "Design intuitive and beautiful user experiences from scratch.",
                "instructor": "Lisa Nguyen",
                "category": cat_objects["design"],
                "price": 79.99,
                "level": "beginner",
                "duration_hours": 30,
            },
        ]

        for course_data in courses:
            Course.objects.get_or_create(
                slug=course_data["slug"],
                defaults=course_data,
            )

        self.stdout.write(self.style.SUCCESS(
            f"Created {len(categories)} categories and {len(courses)} courses."
        ))
