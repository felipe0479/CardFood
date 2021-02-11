from django.contrib import admin
from .models import Empresa
from .models import Client
from .models import Card
from .models import Bonus
from .models import Producto

# Register your models here.

admin.site.register(Empresa)
admin.site.register(Client)
admin.site.register(Card)
admin.site.register(Bonus)
admin.site.register(Producto)
