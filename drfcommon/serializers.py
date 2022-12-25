from rest_framework.serializers import ModelSerializer


class CreatorOrUpdatorModelSerializer(ModelSerializer):
    """
    CreatorOrUpdatorModelSerializer
    """

    def create(self, validated_data):
        user = self.context.get('request').user
        validated_data["creator_id"] = user.id
        validated_data["update_id"] = user.id
        instance = super().create(validated_data)
        return instance

    def update(self, instance, validated_data):
        user = self.context.get('request').user
        validated_data["update_id"] = user.id
        instance = super().update(instance, validated_data)
        return instance
