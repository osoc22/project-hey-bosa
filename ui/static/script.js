$(function(){
            setInterval(oneSecondFunction, 1000);
        });

function oneSecondFunction() {
    $.get( "http://localhost:5000/ping/", function( data ) {
        console.log( data );

        if(Object.keys(data).length > 0) {

            if(data["test/pls"] != undefined && data["test/pls"][1] >= 10 && data["test/pls"][0] == "hi") {
                $("#image").html('<img src="/static/img/BigTextandQRcode.png" alt="QR code to allesoverseks.be">');

            } else if (data["test/hey"]  != undefined && data["test/hey"][1] >= 10 && data["test/hey"][0] == "hi") {
                $("#image").html('<img src="/static/img/list.png" alt="list of types of sexual abuse">');
            } else {
                // TODO rework script structure to make it cleaner
            }
        } else {
            $("#image").html("<img src='/static/img/titlePage.png' alt='vac-title-page'>");
        }
    });
};