from django import template

register = template.Library()

@register.filter(name='range')
def _range(_min, args=None):
    _max, _step = None, None
    if args:
        if not isinstance(args, int):
            _max, _step = map(int, args.split(','))
        else:
            _max = args
    args = filter(None, (_min, _max, _step))
    return range(*args)

@register.filter(name='times') 
def times(number):
    # num = range(1, number+1)
    return range(number, 0, -1)

@register.filter(name='tim') 
def tis(number):
    num = range(1, number+1)
    nums =  range(number, 0, -1)
    return zip(num, nums)

@register.filter(name='dict_key')
def dict_key(d, k):
    '''Returns the given key from a dictionary.'''
    return d[k]

@register.filter
def subtract(value, arg):
    return value - arg