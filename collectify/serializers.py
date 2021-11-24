from rest_framework import serializers

from .models import CarHasColor, Color, Car, User

class CarHasColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarHasColor
        fields = '__all__'


class ColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Color
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):
    colors = ColorSerializer(many=True)

    class Meta:
        model = Car
        fields = ['id', 'name', 'colors']

    def create(self, validated_data):
        color_data = validated_data.pop('colors')
        car = Car.objects.create(**validated_data)
        car.save()

        for data in color_data:
            color_instance = Color.objects.get(name=data.get('name'))
            CarHasColor.objects.create(car=car, color=color_instance)

        return car

    def update(self, instance, validated_data):
        color_data = validated_data.pop('colors')
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        car_has_colors = CarHasColor.objects.filter(car=instance).delete()

        for data in color_data:
            color_instance = Color.objects.get(name=data.get('name'))
            CarHasColor.objects.create(car=instance, color=color_instance)

        return instance


class UserSerializer(serializers.ModelSerializer):
    # Add foreign key fields using id.
    car_id = serializers.IntegerField()
    color_id = serializers.IntegerField()

    class Meta:
        model = User
        fields = '__all__'

