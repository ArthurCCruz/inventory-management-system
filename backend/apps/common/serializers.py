from rest_framework import serializers

class RelatedRecordSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "name"]
        read_only_fields = ["id", "name"]
        model = None
    
    def __init__(self, *args, **kwargs):
        # Allow model to be passed during initialization
        model = kwargs.pop('model', None)
        if model:
            self.Meta.model = model
        super().__init__(*args, **kwargs)