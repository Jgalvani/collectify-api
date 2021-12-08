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
    car_id = serializers.IntegerField(required=False)
    color_id = serializers.IntegerField(required=False)

    class Meta:
        model = User
        fields = '__all__'

    def set_car_and_color(self, validated_data):
        has_driver_licence = validated_data.get('has_driver_licence')
        car_id = validated_data.get('car_id')
        color_id = validated_data.get('color_id')

        if not has_driver_licence:
            validated_data['car_id'] = None
            validated_data['color_id']= None

        elif car_id and color_id:
            try:
                car = Car.objects.get(id=car_id)
                color_ids = [color.id for color in car.colors.all()]

                if color_id not in color_ids:
                    validated_data['color_id']= None

            except Car.DoesNotExist:
                validated_data['car_id'] = None
                validated_data['color_id']= None

    def create(self, validated_data):
        self.set_car_and_color(validated_data)

        user = User.objects.create(**validated_data)
        user.save()

        return user

    def update(self, user, validated_data):
        self.set_car_and_color(validated_data)

        user.firstname = validated_data.get('firsname', user.firstname)
        user.lastname = validated_data.get('lastname', user.lastname)
        user.date_of_birth = validated_data.get('date_of_birth', user.date_of_birth)
        user.has_driver_licence = validated_data.get('has_driver_licence', user.has_driver_licence)
        user.car_id = validated_data.get('car_id', user.car_id)
        user.color_id = validated_data.get('color_id', user.color_id)
        user.save()

        return user
