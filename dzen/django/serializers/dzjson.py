from django.core.serializers.json import Serializer as JSONSerializer

class Serializer(JSONSerializer):
    def serialize(self, queryset, **options):
        options['objects'] = queryset
        return super(Serializer, self).serialize([], **options)

    def end_serialization(self):
        self.objects = self.options.pop('objects')
        super(Serializer, self).end_serialization()
