from django import forms
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.forms import widgets
from django.contrib import messages
from django.contrib.auth.models import User


class LoginUserForm (AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs )
        self.fields["username"].widget = widgets.TextInput(attrs={"class":"form-control"})
        self.fields["password"].widget = widgets.PasswordInput(attrs={"class":"form-control"})

    #istersek gelen bilgiyi düzenleyeiliriz
    def clean_username(self):
        username=self.cleaned_data.get("username")

        #login olan kişi admin ise mesaj ver
        if username == "admin":
            messages.add_message(self.request, messages.SUCCESS, "hoşgeldin admin")
        
        return username
    
    #gelen username ü ile başlıyorsa uyarı verebiliriz
    def confirm_login_allowed(self, user):
        if user.username.startswith("ü"):
            raise forms.ValidationError("bu kullanıcı adı ile login olamazsınız")
        







class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields=("username", "email", "first_name", "last_name", )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget = widgets.PasswordInput( attrs={"class": "form-control"})
        self.fields["password2"].widget = widgets.PasswordInput(   attrs={"class": "form-control"})
        self.fields["username"].widget = widgets.TextInput(  attrs={"class": "form-control"})
        self.fields["email"].widget = widgets.EmailInput( attrs={"class": "form-control"})
        self.fields["email"].required=True
        self.fields["first_name"].widget = widgets.TextInput(  attrs={"class": "form-control"})
        self.fields["last_name"].widget = widgets.TextInput(  attrs={"class": "form-control"})


   # def clean_password2(self):
    #    super.clean_password2() # clean_password2'deki aynı işleri icra etsin, ekleme işleri de aşağıda belirtelim


    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            self.add_error("email", "email daha önce kullanılmış")
            return email  





class UserChangePasswordForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password1"].widget = widgets.PasswordInput( attrs={"class": "form-control"})
        self.fields["new_password2"].widget = widgets.PasswordInput(   attrs={"class": "form-control"})
        self.fields["old_password"].widget = widgets.PasswordInput(  attrs={"class": "form-control"})
