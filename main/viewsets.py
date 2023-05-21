from rest_framework.viewsets import ModelViewSet


class MultiSerializerViewSet(ModelViewSet):
    serializers = {
        'list': None,
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['list'])