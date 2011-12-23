from django.core.serializers.python import Serializer as PythonSerializer
from dzen.django.serializers import SerializerExclusionMixin

class Serializer(SerializerExclusionMixin, PythonSerializer):
    def serialize(self, queryset, **options):
        options['use_natural_keys'] = True
        return super(Serializer, self).serialize(queryset, **options)

    def end_object(self, obj):
        self.objects.append(self._current)
