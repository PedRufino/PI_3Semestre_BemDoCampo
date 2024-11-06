# produtos/templatetags/custom_filters.py
from django import template
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

register = template.Library()

@register.filter
def formatar_moeda(valor):
    return locale.currency(valor, grouping=True)
