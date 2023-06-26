from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'categories',
            'post_title',
            'post_text',
            'author'
        ]

    def clean(self):
        cleaned_data = super().clean()
        categories = cleaned_data.get("categories")
        post_title = cleaned_data.get("post_title")
        post_text = cleaned_data.get("post_text")

        if post_title == categories:
            raise ValidationError(
                "Заголовок не должен совпадать с категорией"
            )

        if post_title == post_text:
            raise ValidationError(
                "Текст новости должен отличаться от ее названия"
            )

        return cleaned_data

    def clean_name(self):
        post_title = self.cleaned_data["post_title"]
        if post_title[0].islower():
            raise ValidationError(
                "Название должно начинаться с заглавной буквы"
            )
        return post_title

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'categories',
            'post_title',
            'post_text',
            'author'
        ]

    def clean(self):
        cleaned_data = super().clean()
        categories = cleaned_data.get("categories")
        post_title = cleaned_data.get("post_title")
        post_text = cleaned_data.get("post_text")

        if post_title == categories:
            raise ValidationError(
                "Заголовок не должен совпадать с категорией"
            )

        if post_title == post_text:
            raise ValidationError(
                "Текст статьи должен отличаться от ее названия"
            )

        return cleaned_data

    def clean_name(self):
        post_title = self.cleaned_data["post_title"]
        if post_title[0].islower():
            raise ValidationError(
                "Название должно начинаться с заглавной буквы"
            )
        return post_title