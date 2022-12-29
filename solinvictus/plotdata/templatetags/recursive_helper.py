from django import template

register = template.Library()


@register.simple_tag
def recursive_display(data):
    if isinstance(data, dict):
        return ''.join([
            f'<tr><td colspan="2">{key}</td></tr>' + recursive_display(value)
            for key, value in data.items()
        ])
    elif isinstance(data, list):
        return ''.join([
            recursive_display(item)
            for item in data
        ])
    else:
        return f'<tr><td>{data}</td></tr>'
