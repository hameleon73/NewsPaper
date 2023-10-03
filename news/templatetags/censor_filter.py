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
         new_text.append(word[0] + "*"*(len(word)-2) + word[-1])
      else:
         new_text.append(word)
   text = " ".join(new_text)
   return f'{text}'