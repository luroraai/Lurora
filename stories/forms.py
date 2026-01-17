#  Author : Wosvo Interactive
#  Developer : Fürkan Göktaş
#  Email : furkan@wosvo.com
#  Date : 12.02.2025 19:27
#  Filename : forms.py
#  Last Modified : 12.02.2025 19:27
#  Project : backend
#  Module : backend
#
#  Copyright (c) 2025
from django import forms
from .models import Stories, Scenes
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django.forms import widgets
from crispy_forms.bootstrap import InlineRadios


class CustomRadioSelect(widgets.RadioSelect):
    template_name = 'forms/custom_radio_select.html'


class StoryForm(forms.ModelForm):
    SCENE_CHOICES = [(i, str(i)) for i in range(1, 5)]  # 1 ile 10 arasında seçim
    scene_count = forms.ChoiceField(
        choices=SCENE_CHOICES,
        widget=widgets.RadioSelect(),
        required=True,
        label='Scene Count'
    )

    class Meta:
        model = Stories
        fields = ['title', 'topic', 'scene_count']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('title'),
            Field('topic'),
            InlineRadios('scene_count', template='forms/custom_radio_select.html'),
        )

    def clean_scene_count(self):
        scene_count = self.cleaned_data['scene_count']
        if int(scene_count) > 4:
            raise forms.ValidationError('Maximum scene count is 4')
        if int(scene_count) < 1:
            raise forms.ValidationError('Minimum scene count is 1')
        return int(scene_count)


class SceneForm(forms.ModelForm):
    class Meta:
        model = Scenes
        fields = ['scene_title', 'scene_number', 'content']


class SceneKeyForm(forms.ModelForm):
    class Meta:
        model = Scenes
        fields = ['keyword']
