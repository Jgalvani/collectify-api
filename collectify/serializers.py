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
            color = Color.objects.get(name=data.get('name'))
            CarHasColor.objects.create(car=car, color=color)

        return car

    def update(self, car, validated_data):
        color_data = validated_data.pop('colors')
        car.name = validated_data.get('name', car.name)
        car.save()

        CarHasColor.objects.filter(car=car).delete()

        for data in color_data:
            color = Color.objects.get(name=data.get('name'))
            CarHasColor.objects.create(car=car, color=color)

        return car


class UserSerializer(serializers.ModelSerializer):
    # Add foreign key fields using id.
    car_id = serializers.IntegerField()
    color_id = serializers.IntegerField()

    class Meta:
        model = User
        fields = '__all__'

