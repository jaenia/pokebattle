from django import forms

from users.models import User


class SignUpForm(forms.ModelForm):
    email = forms.EmailField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["email", "password"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
