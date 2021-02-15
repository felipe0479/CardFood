from django.db import models
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Empresa(models.Model):
    title=models.CharField(max_length=50)
    ubicacion=models.CharField(max_length=50)


class Client(models.Model):

    name=models.CharField(max_length=50)
    age=models.IntegerField(validators=[MinValueValidator(18)])
    points=models.IntegerField(validators=[MinValueValidator(0)],null=True)

    def __str__(self):
    		return '{} {}'.format(self.name)

class Bonus(models.Model):

    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created=models.DateTimeField(auto_now_add=True)
    status=models.BooleanField(default=True)
    empresa=models.ForeignKey(Empresa,on_delete= models.CASCADE)
    client=models.ForeignKey(Client,on_delete= models.CASCADE)
    points=models.IntegerField(validators=[MinValueValidator(0)],null=True)


class Card(models.Model):
    
    date=models.DateTimeField(auto_now_add=True)
    status=models.BooleanField(default=True)
    owner=models.ForeignKey(Client,on_delete= models.CASCADE)
    

class Producto(models.Model):

    title=models.CharField(max_length=50)
    points=models.IntegerField(validators=[MinValueValidator(0)],null=True)
    empresa=models.ForeignKey(Empresa,on_delete=models.CASCADE)
    
