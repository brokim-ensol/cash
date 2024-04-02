def format_datetime(value, fmt='%Y-%m-%d'):
    return value.strftime(fmt)
def number_format_simple(value):
    return '{:,}'.format(value)
def ratio_to_percent_format(value):
    return '{:.1%}'.format(value)