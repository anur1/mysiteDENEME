from django.db import models
from django.utils.text import slugify
#pip install django-ckeditor #ckeditor1  
#from ckeditor.fields import RichTextField    #ckeditor2    
  



class Category(models.Model):    
    name = models.CharField( max_length=50)      
    slug = models.SlugField(default= "", null=False, unique=True, db_index = True, max_length=50)

    def __str__(self):
        return f"{self.name}"
    


class Course(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    subtitle = models.CharField(max_length=100, default="")   #ckeditor4 
    #description = RichTextField()    #ckeditor3 
    #imageUrl = models.CharField(max_length=50, blank=False)  
    image = models.FileField(upload_to="images", default ="")  #yüklenen dosyaları uploads/images klasörüne kaydeder. ImageField çalışmazsa FileField kullanılabilir. 
    date = models.DateField(auto_now=True)
    isActive = models.BooleanField(default=False)
    isHome = models.BooleanField(default = False)
    slug = models.SlugField(default = "", null=False, blank=True,  unique=True, db_index=True)
    #category = models.ForeignKey(Category, default = 1, on_delete=models.CASCADE, related_name="kurslar")
    categories = models.ManyToManyField(Category,)
    #def save(self, *args, **kwargs):
        #self.slug=slugify(self.title)
        #super().save(args, kwargs)

    def __str__(self):
        return f"{self.title}"
    

class UploadModel (models.Model):
    image = models.FileField(upload_to="images")

class Slider (models.Model):
    title = models.CharField(max_length=100)
    image = models.FileField (upload_to="images")
    is_active = models.BooleanField(default=False)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True, blank=True)
    
    def __str__(self): 
        return f"{self.title}"
