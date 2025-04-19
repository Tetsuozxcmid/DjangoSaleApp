from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Offer


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'category', 'condition']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class ExchangeOfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['ad_receiver', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Ваше предложение обмена...'
            }),
        }
        labels = {
            'ad_receiver': 'Объявление для обмена',
            'comment': 'Комментарий'
        }

    def __init__(self, *args, user=None, initial_receiver=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['ad_receiver'].queryset = Post.objects.exclude(author=user)

        if initial_receiver:
            self.fields['ad_receiver'].initial = initial_receiver

        self.fields['ad_receiver'].label_from_instance = lambda obj: f"{obj.title} (Категория: {obj.get_category_display()})"
