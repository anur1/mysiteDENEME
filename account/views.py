from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm

from account.forms import LoginUserForm, NewUserForm, UserChangePasswordForm

def user_login (request,):
    #kullanıcı super admin değilse, url'deki next çıkar. Yani kullanıcı yetkisizdir. 
    if request.user.is_authenticated and "next" in request.GET: 
        return render(request, "account/login.html", {"error":"username ya da password yetkisiz alana giremez!"})
    
    if request.method =="POST":
        #Login formunu django builtin form'dan al.
        #form = AuthenticationForm(request, data =request.POST)
        form = LoginUserForm(request, data=request.POST) #LoginUserForm AuthenticationForm'dan türetilmiştir. 
        if form.is_valid():            #not: request.cleaned_data çalışmıyor. form.cleaned_data çalıştı. 
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            #Authentication Form kullanmadan önce bunları kullanıyorduk.
            # username = request.POST["username"]
            # password = request.POST["password"]
            # user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, "giriş başarılı")
                #return redirect( "index"   )  next yoksa gitsin, varsa ilgili sayfaya gitsin
                nextUrl = request.GET.get("next", None)
                if nextUrl is None:
                    return redirect("index")
                else: 
                    return redirect(nextUrl)
                
            else: #kullanıcı None ise login formu login.html'ye gider.
                return render(request, "account/login.html", {"form": form} )
            
        else:# form valid değilse, login formu login.html'ye gider
            #messages.add_message(request, messages.ERROR, "giriş başarısız, username ya da password yanlış") bu hata mesajına artık gerek yok. form dan geliyor zaten
            return render(request, "account/login.html", {"form": form} )
        
    else:   #GET ile gelinmişse boş Login formu login.html'ye gönderilir
        #form = AuthenticationForm()
        form = LoginUserForm()
        return render (request, "account/login.html", {"form": form})





def user_register (request,):
    if request.method=="POST":
        #form = UserCreationForm (request.POST)
        form = NewUserForm(request.POST)  
        if form.is_valid():  
            form.save()   
            
            #kişiyi kaydettikten sonra login olsun
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(request, username = username, password = password)
            login (request, user)
            return redirect("index")   
        else:
            return render(request, "account/register.html", {"form": form})



    else:
        #form = UserCreationForm()
        form = NewUserForm()
        return render(request, "account/register.html", {"form": form})





# built in formu kullanmadan önceki register formu
# def user_register (request,):
#     if request.method=="POST":
#         username = request.POST["username"]
#         email = request.POST["email"]
#         password = request.POST["password"]
#         repassword = request.POST["repassword"]

#         if password != repassword: 
#             return render (request, "account/register.html", {"error": "parlolalar eşleşmiyor", "username": username, "email": email})

#         if User.objects.filter(username= username).exists():
#                 return render (request, "account/register.html", {"error": "aynı isimli bir kullanıcı daha var, başka bir isim seçiniz", "username": username, "email": email})
        
#         if User.objects.filter(email=email).exists():
#             return render (request, "account/register.html", {"error": "aynı email adresli birisi daha var, başka bir email adresi giriniz..", "username": username, "email": email})

#         user = User.objects.create_user(username = username, email= email, password = password)
#         user.save()
#         return redirect("user_login")


#     else:
#         return render (request, "account/register.html", )





def change_password(request, ):
    if request.method == "POST":
        #form = PasswordChangeForm(request.user, request.POST)
        form = UserChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user=form.save()  #save'den dönen user update'e verilir
            update_session_auth_hash(request, user)
            messages.success(request, "Parola başarı ile güncellendi..")
            return redirect("change_password")
        else:
            return  render(request, "account/change-password.html", {"form":form})


    #form = PasswordChangeForm(request.user)
    form = UserChangePasswordForm(request.user)
    return  render(request, "account/change-password.html", {"form":form})



def user_logout (request,):  #logout yap, cookies sil, anasayfaya yönlendir. 
    messages.add_message(request, messages.SUCCESS,"Çıkış başarılı")
    logout(request)
    return redirect ("index" )

