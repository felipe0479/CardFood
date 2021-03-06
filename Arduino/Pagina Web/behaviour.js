var IP = "192.168.1.18";//la ip o dns del arduino
var IDCard;//id de la tajeta del ultimo usuario seleccionado
let Clientes =[];
let Cupones = [];
var ToastElement;

$(document).ready(function(){
  ToastElement = $('.toast');//se asigna el toast a una variable
  $('#IParduino').val(IP);
});

var myToastEl = document.getElementById('myToast');
/*myToastEl.addEventListener('hidden.bs.toast', function () {
  console.log("call");
})*/

var myCollapseEl = document.getElementById('#myCollapse');

/*myCollapseEl.addEventListener('shown.bs.collapse', function (event) {
  // Action to execute once the collapsible area is expanded
})*/
function changeip(){
  IP = $('#IParduino').val();
  console.log(IP);
}

function toastActive(bodytext,titletext,imgsrc){
  body = $('#toast-body');
  title = $('#toast-header');
  image = $('#toast-img');
  image.attr("src",imgsrc);
  title.html(titletext);
  body.html(bodytext);
  ToastElement.toast('show');
}


function ReadCardinfo(){//obtiene la informacion del arduino de la ultima tarjeta leida 
  $.ajaxSetup({timeout:2000}); 
  $.ajax({
        type: "GET",
        url: "http://"+IP+"/",
        //data: "",// la información a enviar (también es posible utilizar una cadena de datos)
        //dataType: "text/plain",// el tipo de información que se espera de respuesta
        success: function (response) {
          console.log(response);
          if (response.id == 0){
            toastActive("No se ha leido ninguna tarjeta","Arduino","info.png");
            return;
          }
          idcard = response['id'];
          toastActive("ID: "+idcard,"Arduino","info.png");
          GetDataPersona(idcard);
        }
  });

  /*arduino = "192.168.1.18/"
  var settings = {
    "url": arduino,
    "method": "GET",
    "timeout": 5000,
  };
  
  $.ajax(settings).done(function (response) {
    console.log('mensaje recibido');
    console.log(response);
  });*/
  

}

function GetDataPersona(idcard){
  $.ajax({
    type: "GET",
    url: "http://jsilva2021.pythonanywhere.com/client_by_card/"+idcard+"",
    //data: "data",
    //dataType: "dataType",
    success: function (response) {
      console.log(response);
      
      var {Nombre,edad,puntos,celular,cedula,chat_id} = response;
      Clientes[idcard] = {Nombre,edad,puntos,celular,cedula,chat_id};

      str = '<a id="'+idcard+'" style="cursor:pointer" class="list-group-item list-group-item-action flex-column align-items-start" onclick="clickcard(\''+idcard+'\')"> '+
      '<div class="d-flex w-100 justify-content-between">'+
          '<h5 class="mb-1">'+Nombre+'</h5> '+
          '<small><img src="card.png" width="25px" style="margin:5px;">'+idcard.toUpperCase()+'</small>'+
      '</div>'+
      '<div class="row">'+
          '<div class="col-sm">'+
              '<p class="mb-1">C.C: '+cedula+' ('+edad+') Años</p> '+
              '<p class="mb-1">Telefono: '+celular+'</p> '+
              '<p class="mb-1">UserTelegram:'+chat_id+'</p> '+
              '<p>Puntos: '+puntos+'</p>'+
          '</div>'+                        
          '<div class="col-3">'+
              '<button class="btn btn-success" onclick="telegram(\''+idcard+'\')">Enviar Telegram</button>'+
          '</div>'+
      '</div>'+
  '</a>';

      $('#lista-persona').prepend(str);
    }
  });
}

function clickcard(id) {
  IDCard = id;
  $('#'+id).tab('show');//pone el color azul a la tarjeta del usuario
  BonosUpdate();
}

function BonosUpdate(){
    url = "http://jsilva2021.pythonanywhere.com/bonus_by_tgm/"+Clientes[IDCard].chat_id;
    console.log(url);
    $.ajax({
      type: "GET",
      url: url,
      success: function (bonos) {
        Cupones = bonos;
        console.log(bonos);
        listahtml = $('#bonus');
        listahtml.empty();
        str="";
    
        for(var i=0;i<bonos.length;i++){
          str += '<a id="" style="cursor:pointer" class="list-group-item list-group-item-action flex-column align-items-start">'+
          '<div class="row">'+
              '<div class="col-2">';
    
          switch(bonos[i].empresa){
            case "exito":
              str += '<img src="exito.png" width="50px">';
              break;
            case "KFC":
              str += '<img src="kfc.png" width="50px">';
              break;
            case "Duno":
              str += '<img src="duno.png" width="50px">';
              break;
            default:
              str += '<img src="bonus.png" width="50px">';
          }
    
           str += '</div>'+
              '<div class="col-sm">'+
                  '<p>'+bonos[i].cupon+'</p>'+
                  'Puntos: '+bonos[i].puntos+
              '</div>'+
              '<div class="col-3">'+
                  '<button class="btn btn-primary" onclick="ReclamarBonus(\''+i+'\')">Reclamar</button>'+
              '</div>'+
          '</div>'+
          '</a>';
        }
    
        listahtml.append(str);
      }
    });
    
}

function ReclamarBonus(id){

  $.ajax({
    type: "GET",
    url: "http://jsilva2021.pythonanywhere.com/delete_bonus/"+Cupones[id].cupon,
    success: function (response) {
        console.log(response.Msg);
        toastActive(response.Msg,"Database response","server.png")
        BonosUpdate();
    }
  });
  console.log(Cupones);
  $.ajax({
    type: "GET",
    url: "http://"+IP+"/bonoreclamado?id="+Clientes[IDCard].chat_id+"&emp="+Cupones[id].empresa+"&p="+Clientes[IDCard].puntos,
    success: function (response) {
      console.log("Correcto bono reclamado telegram");
    }
  });
}

function Crearbonus() { 
  empresa = $('#empresa').val();
  puntos = $('#puntos').val();
  $.ajax({
    type: "GET",
    url: "http://jsilva2021.pythonanywhere.com/create_bonus/"+Clientes[IDCard].cedula+"/"+empresa+"/"+puntos,
    success: function (response) {
      console.log(response.Msg);
      toastActive(response.Msg,"Database response","server.png")
      BonosUpdate();
    }
  });
 }

function telegram(id) {
  console.log(Clientes[id].chat_id);
  $.ajax({
    type: "POST",
    url: "http://"+IP+"/telegram?id="+Clientes[id].chat_id,
    success: function (response) {
      console.log("Correcto");
      //toastActive('Mensaje enviado a '+Clientes[id].Nombre,"Telegram","Telegram_logo.png");
    }
  });
  toastActive('Mensaje enviado a '+Clientes[id].Nombre,"Telegram","Telegram_logo.png");
 
}

function Atualizar(){
  select = $('people');
}
