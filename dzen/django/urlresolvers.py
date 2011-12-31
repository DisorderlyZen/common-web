try:
    from django.core.urlresolvers import reverse_lazy
except ImportError:
    from django.core.urlresolvers import reverse
    from django.utils.functional import lazy

    reverse_lazy = lazy(reverse, str)
