from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from accounts.models import QuoraUser


class PasswordChangeForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput)
    current_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)


class UserLoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = QuoraUser.objects.filter(email=email)
        if qs.exists():
            return email
        raise forms.ValidationError("This email is not registered.")


class QuoraUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = QuoraUser
        fields = ('username', 'email', 'date_of_birth', 'first_name', 'last_name', 'description')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1!=password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class QuoraUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = QuoraUser
        fields = ('username', 'email', 'date_of_birth', 'first_name', 'last_name', 'description', 'is_staff',
                  'is_admin', 'is_active')

    def clean_password(self):
        return self.initial['password']

