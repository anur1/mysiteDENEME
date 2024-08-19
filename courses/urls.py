from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('search', views.search, name='search'),
    path('add-course', views.add_course, name='add_course'),
    path('course-list', views.course_list, name='course_list'),
    path('course-edit/<int:id>', views.course_edit, name="course_edit"),
    path('course-delete/<int:id>', views.course_delete, name="course_delete"),
    path('upload-image', views.upload_image, name="upload_image"),
    path('<slug:slug>', views.details, name="course_details"),
    path('kategori/<slug:slug>', views.getCoursesByCategory, name='courses_by_category'),
]