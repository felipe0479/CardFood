from django.shortcuts import render
from django.http import JsonResponse 
from django.shortcuts import get_object_or_404

from .models import Client,Bonus,Empresa,Card


# Create your views here.

"""def post_list(request):
    return render(request, 'apps/product_list.html', {})"""

def get_client(request,id):
    try:
        client=get_object_or_404(Client, cedula=id)
        nombre=client.name
        edad=client.age
        puntos=client.points
        celular=client.celular
        cedula=client.cedula
        chat_id=client.chat_id

        return JsonResponse({ 'Nombre': nombre, 'edad': edad,'puntos':puntos,'celular':celular,'cedula':cedula,'chat_id':chat_id })
    except:
        return JsonResponse({ 'Msg' :"El usuario no exite"})
def client_by_card(request,id):
    try:
        card=get_object_or_404(Card, codigo=id)
        nombre=card.owner.name
        edad=card.owner.age
        puntos=card.owner.points
        celular=card.owner.celular
        cedula=card.owner.cedula
        chat_id=card.owner.chat_id

        return JsonResponse({ 'Nombre': nombre, 'edad': edad,'puntos':puntos,'celular':celular,'cedula':cedula ,'chat_id':chat_id})
    except:
        return JsonResponse({ 'Msg' :"La Tarjeta no existe"})

def get_bonus_client(request,id):
    try:
        client=get_object_or_404(Client, cedula=id)
        try:
            bono=get_object_or_404(Bonus,client=client,status=True)
            cupon=bono.id
            empresa=bono.empresa.title

            return JsonResponse({ 'Msg' :"El usuario tiene cupon","cupon":cupon,"empresa":empresa})
        except:
            return JsonResponse({ 'Msg' :"El usuario no tiene bono"})

    except:
        return JsonResponse({ 'Msg' :"El usuario no exite"})

def delete_bonus_client(request,id):
    try:
        client=get_object_or_404(Client, cedula=id)
        try:
            bono=get_object_or_404(Bonus,client=client,status=True)
            bono.status=False
            cupon=bono.id
            bono.save()
            client.points=client.points-bono.points
            client.save()
            ptos=client.points

            return JsonResponse({ 'Msg' :"El usuario ha reclamado cupon","cupon":cupon,"puntos":ptos})
        except:
            return JsonResponse({ 'Msg' :"El usuario no tiene bono"})

    except:
        return JsonResponse({ 'Msg' :"El usuario no exite"})

def create_bonus_client(request,id,emp,pts):
    try:
        client=get_object_or_404(Client, cedula=id)
        print("si hay client")
        empresa=get_object_or_404(Empresa,title=emp)
        print("si ahy empresa")    
        nombre=client.name
        bono=Bonus(empresa=empresa,points=pts,client=client)
        bono.save()
        client.points=client.points+pts
        client.save()
        ptos=client.points
        cupon=bono.id
        return JsonResponse({ 'Msg' :"Cupon creado exitosamente","name":nombre,"cupon":cupon,"puntos":ptos})

    except:
        return JsonResponse({ 'Msg' :"El usuario o empresa no exite "})

def create_card(request,id,code):
    try:
        client=get_object_or_404(Client, cedula=id)
        try:
            card=get_object_or_404(Card,owner=client,status=True)
            codigo=card.codigo
            
            return JsonResponse({ 'Msg' :"El usuario ya posee una tarjeta","card":codigo})
        except:
            card=Card(owner=client,codigo=code)
            card.save()
            return JsonResponse({ 'Msg' :"Creacion de tarjeta existosa"})

    except:
        return JsonResponse({ 'Msg' :"El usuario no exite"})

def deactivate_card(request,id):
    try:
        client=get_object_or_404(Client, cedula=id)
        try:
            card=get_object_or_404(Card,owner=client,status=True)
            card.status=False
            card.save()
            return JsonResponse({ 'Msg' :"La Tarjeta ha sido deshabilitada"})
        except:
            card=Card(owner=client,codigo=code)
            card.save()
            return JsonResponse({ 'Msg' :"El usuario no tiene tarjeta activa"})

    except:
        return JsonResponse({ 'Msg' :"El usuario no exite"})

def bonus_by_id(request,id):
    data={}
    try:
        client=get_object_or_404(Client, chat_id=id)
        try:
            print("Entra a try")
            bono=Bonus.objects.filter(client=client,status=True).all()
            i=1
            print("encuentra bonos")
            if bono is not '':
                print("entra en el if ")
                for b in bono:
                    print("entra en el for ")
                    cupon=b.id
                    cupon=str(cupon)
                    empresa=b.empresa.title
                    data.update({'cupon '+str(i):cupon,'empresa '+str(i):empresa})    
                    print("imprimimos la data",data)
                    i=i+1


            return JsonResponse(data)
        except:
            return JsonResponse({ 'Msg' :"El usuario no tiene bono"})

    except:
        return JsonResponse({ 'Msg' :"El usuario no exite"})