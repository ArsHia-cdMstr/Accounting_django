# # app/templatetags/__init__.py
#
# from django import template
#
# register = template.Library()
#
# @register.filter(name='add_class')
# def add_class(field, css_class):
#     """
#     Adds a CSS class to a form field widget.
#
#     Usage in template:
#     {{ form.field_name|add_class:"your-class-name" }}
#     """
#     return field.as_widget(attrs={"class": css_class})
