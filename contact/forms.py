from contact.models import Contact
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation

class ContactForm(forms.ModelForm): 
    pictures = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*',
            }
        ),
        required=False
    )


    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'phone', 'email', 'description', 'category', 'pictures')



    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')

        if first_name == 'ABC':
            self.add_error(
                'first_name', 
                ValidationError(
                    'Nao digite ABC nessa porra krl',
                    code='invalid'
                )
            )

        return first_name

    def clean(self):
        cleaned_data = self.cleaned_data
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if first_name == last_name:
            msg = ValidationError('Primeiro nome nao pode ser igual ao segundo', code='invalid')
            self.add_error('first_name', msg)
            self.add_error('last_name', msg)
        
        print(cleaned_data)
        return super().clean()

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        min_length=3,
    )
    last_name = forms.CharField(
        required=True,
        min_length=3,
    )
    email = forms.EmailField(
        required=True,
    )

    class Meta:
        model = User
        fields = ( 'first_name', 'last_name', 'email', 'username', 'password1', 'password2' )

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            self.add_error(
                'email', 
                ValidationError('Ja existe uma conta com esse email', code='invalid' )
            )

        return email
    
class RegisterUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required.',
        error_messages={
            'min_length': 'Please, add more than 2 letters.'
        }
    )
    last_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required.'
    )

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )

    password2 = forms.CharField(
        label="Password 2",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text='Use the same password as before.',
        required=False,
    )

     
    class Meta:
        model = User
        fields = ( 'first_name', 'last_name', 'email', 'username' )

    def save(self, commit=True):
        new_password = self.cleaned_data.get('password1')
        user:User = super().save(commit=False)
        
        if new_password:
            user.set_password(new_password)
        
        if commit:
            user.save()

        return user

    def clean(self):
        pass1 = self.cleaned_data.get('password1')
        pass2 = self.cleaned_data.get('password2')

        if pass1 or pass2:
            if pass1 != pass1:
                self.add_error(
                    'password2',
                    ValidationError('As senhas nao correspondem', code='invalid')
                )

        return super().clean()
    

    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email

        if current_email != email:
            if User.objects.filter(email=email).exists():
                self.add_error(
                    'email', 
                    ValidationError('Ja existe uma conta com esse email', code='invalid' )
                )
        
        return email

    def clean_password1(self):
        pass1 = self.cleaned_data.get('password1')

        if pass1:
            try:
                password_validation.validate_password(pass1)
            except ValidationError as error:
                self.add_error(
                    'password1', 
                    ValidationError(error, code='invalid')
                )

        return pass1
    
