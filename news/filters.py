from django_filters import FilterSet, ModelMultipleChoiceFilter, DateTimeFilter, ModelChoiceFilter
from django.forms import DateTimeInput
from .models import Post, Category


class PostFilter(FilterSet):
   category = ModelMultipleChoiceFilter(
       field_name='postcategory__category',
       queryset=Category.objects.all(),
       label='Категория',
       conjoined=True,
   )

   added_after = DateTimeFilter(
       field_name='time_in',
       lookup_expr='gt',
       widget=DateTimeInput(
           format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
       )
   )
   class Meta:
       model = Post
       fields = {
           'post_title': ['icontains'],

       }

