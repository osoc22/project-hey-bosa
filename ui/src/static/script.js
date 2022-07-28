$(function(){
            setInterval(oneSecondFunction, 1000);
        });

function oneSecondFunction() {
    $.get( "http://localhost:5000/ping/", function( data ) {
        console.log( data );

        if(Object.keys(data).length > 0) {
            if(data["hermes/handler/qr"] != undefined && data["hermes/handler/qr"][1] >= 10 && data["hermes/handler/qr"][0] == "{}") {
                $("#image").html('<img src="/static/img/BigTextandQRcode.png" alt="QR code to allesoverseks.be">');

            } 
            else if (data["hermes/handler/list"]  != undefined && data["hermes/handler/list"][1] >= 10) {
                $("#image").html('<img src="/static/img/list.png" alt="list of types of sexual abuse">');

            } else if (data["hermes/handler/conversation/stop"]  != undefined && data["hermes/handler/conversation/stop"][1] >= 10) {
                $("#image").html("<img src='/static/img/titlePage.png' alt='vac-title-page'>");
            }
            
        } else {
            $("#image").html("<img src='/static/img/titlePage.png' alt='vac-title-page'>");
        }
    });
};