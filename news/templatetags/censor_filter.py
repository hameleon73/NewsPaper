from django import template

register = template.Library()

CENS_SYMBOLS = [
   'Астана', 'Астане', 'США', 'Украина', 'Украине'
]

@register.filter()
def censor(text):

   new_text = []


   for word in text.split():
      if word in CENS_SYMBOLS:
         new_text.append('***')
      else:
         new_text.append(word)
   text = " ".join(new_text)
   return f'{text}'