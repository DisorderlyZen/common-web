from django.core.serializers.python import Serializer as PythonSerializer
from dzen.django.serializers import SerializerExclusionMixin

class Serializer(SerializerExclusionMixin, PythonSerializer):
    def serialize(self, queryset, **options):
        if 'use_natural_keys' not in options:
            options['use_natural_keys'] = True

        return super(Serializer, self).serialize(queryset, **options)

    def end_object(self, obj):
        super(Serializer, self).end_object(obj)
        self.finalize_object(self.objects[-1])

    def finalize_object(self, obj):
        if self.options.pop('simple_object', True):
            obj = self.simplify_object(obj)

        if not self.options.pop('allow_empty', False):
            obj = self.strip_empty(obj)

        self.objects[-1] = obj

    def simplify_object(self, obj):
        new = obj['fields']
        new['id'] = obj['pk']
        return new

    def strip_empty(self, obj):
        return dict((key, val) for key, val in obj.iteritems() if val not in ('', None, []))
