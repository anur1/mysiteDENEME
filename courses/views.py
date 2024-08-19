from datetime import date, datetime
from django.http import Http404, HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from courses.forms import CourseAddForm, CourseEditForm, UploadForm
from .models import Course, Category, Slider, UploadModel
from django.core.paginator import Paginator

import random, os
from django.contrib.auth.decorators import login_required, user_passes_test

# no @decorator -> bütün kullanıcılara açık
def index(request):  
    kurslar = Course.objects.filter(isActive=1, isHome=1)
    kategoriler = Category.objects.all()
#    for kurs in db["courses"]:
#         if kurs["isActive"] == True: 
#             kurslar.append(kurs)
    sliders = Slider.objects.filter (is_active=True)


    return render(request, 'courses/index.html', {
        'categories': kategoriler,
        'courses': kurslar,
        'sliders':sliders
    })


def isAdmin(user, ):
    return user.is_superuser
    


#@login_required()  # bu method login gerektirir
@user_passes_test(isAdmin) #isAdmin methodu yani superuser true geliyorsa, bu method çalışır, sıradan üyeler erişemez
def add_course(request, ): #sadece admin'e açık

    # #bu kontrolü artık decorator yapıyor
    # #admin veya super user  değilse index'e gider
    # if not request.user.is_authenticated: 
    #     return redirect("index")
    # if not request.user.is_superuser: 
    #     return redirect("index")
    
    if request.method == "POST": 
        form = CourseAddForm(request.POST, request.FILES)

        if form.is_valid(): 
            form.save()

            # kurs = Course(title = form.cleaned_data["title"], 
            #               description = form.cleaned_data["description"],
            #               imageUrl = form.cleaned_data["imageUrl"],
            #               slug = form.cleaned_data["slug"])
            # kurs.save()
            return redirect ("/kurslar")
    else: #GET form
        form = CourseAddForm()

    return render(request, "courses/add-course.html", {"form": form})


@login_required()
def course_list (request):
    kurslar = Course.objects.all()

    return render(request, 'courses/course-list.html', {
        'courses': kurslar
    })

def course_edit (request, id):
    course = get_object_or_404(Course, pk=id)

    if request.method == 'POST': #post ise güncelle ve listeye dön
        form = CourseEditForm(request.POST,  request.FILES, instance=course)
        form.save()
        return redirect ( "course_list")
    else: #get ise bilgileri görüntüle
        form = CourseEditForm(instance=course)


    return render(request, 'courses/edit-course.html', {"form": form})   




def course_delete (request, id):
    course = get_object_or_404(Course, pk=id)

    if request.method == "POST":
        course.delete()
        return redirect("course_list")



    return render(request, 'courses/delete-course.html', {"course": course})


def upload_image (request):
    if request.method=="POST":
        #uploaded_image = request.FILES['image'] #request'ten forma eklenen "image" adlı dosyayı getir. 
        #print(uploaded_image)
        #print(uploaded_image.name)
        #print(uploaded_image.size)
        #print(uploaded_image.content_type)
        #uploaded_images = request.FILES.getlist("images") #yüklenen dosyaların listesini al
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            model = UploadModel(image=request.FILES["image"])
            model.save()
            # uploaded_image=request.FILES["image"]
            # handle_uploaded_files (uploaded_image)

            # for file in uploaded_images: 
            #     handle_uploaded_files (file)
            return render (request, "courses/success.html") #başarı mesajı
    else:
        form=UploadForm()
    
    return render(request, "courses/upload-image.html", {"form":form})


# def handle_uploaded_files (file): #file'ı dizin içine kaydetme methodu
#     number = random.randint(1, 100) 
#     file_name, file_extension = os.path.splitext(file.name)
#     new_name = file_name + "_" + str(number) + file_extension  #resim_0001.jpg

#     #deploy için temp/ ---> /home/kursapp/mysite29H/temp olarak değişmesi gerekiyor
#     with open("temp/" + new_name, "wb+") as destination:
#         for chunk in file.chunks():
#             destination.write(chunk)





def search(request):
    if "q" in request.GET and request.GET["q"] !="":
        q = request.GET["q"]
        kurslar  = Course.objects.filter(isActive = True, title__contains=q).order_by("date")#category__slug = slug,
        kategoriler = Category.objects.all()
    else:
        return redirect("/kurslar")  

    
    return render(request, 'courses/search.html', {
        'categories': kategoriler,
        'courses': kurslar,
    })



def details(request, slug):
    course = get_object_or_404(Course, slug=slug)

    context = {
        'course': course
    }
    return render(request, 'courses/details.html', context)


# 




def getCoursesByCategory(request, slug):
    kurslar  = Course.objects.filter( categories__slug= slug, isActive = True).order_by("date")#category__slug = slug,
    kategoriler = Category.objects.all()


    
    paginator = Paginator(kurslar, 3) #filtrelenmiş kursları her sayfada 5'er adet göster
    page = request.GET.get('page', 1) #query'den gelen page number'ı kullan
    page_obj = paginator.page(page) #page e düşen kursları pageob'e at
    
    print(page_obj.paginator.count) #toplam ürün sayısı
    print(page_obj.paginator.num_pages) # toplam sayfa sayısı


    return render(request, 'courses/list.html', {
        'categories': kategoriler,
        'courses': kurslar,
        'page_obj': page_obj,
        'seciliKategori': slug
    })