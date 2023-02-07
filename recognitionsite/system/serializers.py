from rest_framework import serializers

from recognitionsite.system.models import Result


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ('title', 'cat_id')