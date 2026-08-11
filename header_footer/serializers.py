from rest_framework import serializers

from .models import Header, Footer, FooterText


class HeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Header
        fields = '__all__'


class FooterTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterText
        fields = '__all__'


class FooterSerializer(serializers.ModelSerializer):
    footer_text_detail = FooterTextSerializer(
        source='footer_text',
        read_only=True,
    )

    class Meta:
        model = Footer
        fields = [
            'id',
            'logo',
            'title',
            'description',
            'footer_text',
            'footer_text_detail',
        ]
