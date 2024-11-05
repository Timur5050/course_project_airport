from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.forms import DateInput

from hangar.models import User, Airplane, Flight


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
        )
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class AirplaneForm(forms.ModelForm):
    class Meta:
        model = Airplane
        fields = "__all__"


class FlightForm(forms.ModelForm):
    astronauts = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    flight_date = forms.DateField(widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Flight
        fields = "__all__"


class FlightSearchFormSource(forms.Form):
    source = forms.CharField(
        required=False,
        label="",
        max_length=255,
        widget=forms.TextInput(attrs={"placeholder": "search by source"}),
    )


class FlightSearchFormDestination(forms.Form):
    destination = forms.CharField(
        required=False,
        label="",
        max_length=255,
        widget=forms.TextInput(attrs={"placeholder": "search by destination"}),
    )


class AirplaneSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        label="",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "search by name"})
    )


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
