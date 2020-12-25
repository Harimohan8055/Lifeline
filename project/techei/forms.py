from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import SeatsEventModel,User,IndividualProfile,City,State,InstitutionProfile,EventModel,FestClubModel,FestImage,EventImage,ApplyEventModel
from django.forms.utils import ValidationError
from django.db import models

TYPE=[
    ('','------Select-----'),
    ('0','Student'),
    ('1','Professional'),
    ('3', 'Other')
]

class IndividualSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_individual = True
        user.is_confirm = True
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        return user


class IndividualProfileForm(forms.ModelForm):
    type=forms.CharField(label='User Type', widget=forms.Select(choices=TYPE))

    class Meta:
        model = IndividualProfile
        fields = ('college','contact','location','state' ,'city','type','age',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()

        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['city'].queryset = City.objects.filter(state_id=state_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.country.city_set.order_by('name')


class InstitutionSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_institution = True
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        return user


class InstitutionProfileForm(forms.ModelForm):
    class Meta:
        model = InstitutionProfile
        fields = ('institutionname','contact','location','regno','state' ,'city',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()

        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['city'].queryset = City.objects.filter(state_id=state_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.country.city_set.order_by('name')


class AddEventForm(forms.ModelForm):
    class Meta:
        model = EventModel
        fields = ('title', 'description', 'venue', 'address', 'time', 'start_date', 'end_date', 'seats' ,'fee' ,'prize', 'paylink', 'fest', 'state', 'city', 'category', 'attendee_type')
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['city'].queryset = City.objects.none()

            if 'state' in self.data:
                try:
                    state_id = int(self.data.get('state'))
                    self.fields['city'].queryset = City.objects.filter(state_id=state_id).order_by('name')
                except (ValueError, TypeError):
                    pass  # invalid input from the client; ignore and fallback to empty City queryset
            elif self.instance.pk:
                self.fields['city'].queryset = self.instance.country.city_set.order_by('name')

class AddFestClubForm(forms.ModelForm):

    class Meta:
        model = FestClubModel
        fields = ('name', 'description')



class FestImageForm(forms.ModelForm):
    class Meta:
        model = FestImage
        fields = ('name', )

class EventImageForm(forms.ModelForm):
    class Meta:
        model = EventImage
        fields = ('name', )

class ApplyEventForm(forms.ModelForm):
    class Meta:
        model = ApplyEventModel
        fields = '__all__'


class SeatsEventForm(forms.ModelForm):
    class Meta:
        model = SeatsEventModel
        fields = '__all__'

class SearchForm(forms.Form): #Note that it is not inheriting from forms.ModelForm
    que = forms.CharField(max_length=50)
