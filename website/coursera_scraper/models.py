from django.db import models
from django import forms

# Create your models here.
CATEGORIES_CHOICES = (
    ('data-science','Data Science'),
    ('business', 'Business'),
    ('computer-science','Computer Science'),
    ('personal-development','Personal Development'),
    ('language-learning','Language Learning'),
    ('information-technology','Information Technology'),
    ('health','Health'),
    ('math-and-logic',''),
    ('physical-science-and-engineering','Physical Science and Engineering'),
    ('social-sciences','Social Sciences'),
    ('arts-and-humanities','Arts and Humanities'),
)

class Category(models.Model):
    category = models.CharField(max_length=100, choices=CATEGORIES_CHOICES)
    
    def __str__(self):
        return self.category

# class DropDown(forms.ModelForm):
#     name = forms.CharField()
#     parts = forms.ModelChoiceField(queryset=Part.objects.values_list('category', flat=True).distinct())

#     class Meta:
#         model = UserItem
#         fields = ('name', 'category',)