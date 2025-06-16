from django import template

register = template.Library()

@register.filter(name='currency_filter')  # Registering with the correct name
def currency_filter(value):
    try:
        value = float(value)
        if value >= 1_00_00_000:
            return f"₹{value / 1_00_00_000:.2f} Cr"
        elif value >= 1_00_000:
            return f"₹{value / 1_00_000:.2f} L"
        else:
            return f"₹{value:,.2f}"
    except (ValueError, TypeError):
        return value
