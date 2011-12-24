class SerializerExclusionMixin(object):
    def start_serialization(self):
        self.excluded_fields = self.options.pop('excluded_fields', None)
        super(SerializerExclusionMixin, self).start_serialization()

    def handle_field(self, obj, field):
        self.handle_exclusion(super(SerializerExclusionMixin, self).handle_field, obj, field)

    def handle_fk_field(self, obj, field):
        self.handle_exclusion(super(SerializerExclusionMixin, self).handle_fk_field, obj, field)

    def handle_m2m_field(self, obj, field):
        self.handle_exclusion(super(SerializerExclusionMixin, self).handle_m2m_field, obj, field)

    def handle_exclusion(self, fn, obj, field):
        not self.field_is_excluded(field) and fn(obj, field)

    def field_is_excluded(self, field):
        return self.excluded_fields and field.attname in self.excluded_fields
