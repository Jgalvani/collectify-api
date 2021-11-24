from django.db import models

# Create your models here.
class Color(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'collectify_colors'

    def __str__(self):
        """
        return a string that represent the model in the admin app
        """
        return self.name


class Car(models.Model):
    name = models.CharField(max_length=255)
    colors = models.ManyToManyField(Color, through='CarHasColor')

    class Meta:
        db_table = 'collectify_cars'

    def __str__(self):
        """
        return a string that represent the model in the admin app
        """
        return self.name


class CarHasColor(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='car_has_color')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='car_has_color')

    class Meta:
        db_table = 'collectify_car_has_color'

    def __str__(self):
        """
        return a string that represent the model in the admin app
        """
        return ' '.join([self.car.name, self.color.name])


class User(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    has_driver_licence = models.BooleanField(default=False)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='users', blank=True, null=True, default=None)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='users', blank=True, null=True, default=None)

    class Meta:
        db_table = 'collectify_users'

    def __str__(self):
        """
        return a string that represent the model in the admin app
        """
        return ' '.join([self.firstname, self.lastname])


