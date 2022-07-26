$(function(){
            setInterval(oneSecondFunction, 1000);
        });

function oneSecondFunction() {
    $.get( "http://localhost:5000/ping/", function( data ) {
        console.log( data );

        if(Object.keys(data).length > 0) {

            if(data["test/pls"] != undefined && data["test/pls"][1] >= 10 && data["test/pls"][0] == "hi") {
                $("#image").html('<img src="/static/img/BigTextandQRcode.png" alt="">')
                

            } else if (data["test/hey"]  != undefined && data["test/hey"][1] >= 10 && data["test/hey"][0] == "hi") {
                $("#image").html('<img src="/static/img/list.png" alt="">')

            } else if (data["test/hey"]  != undefined && data["test/hey"][1] >= 10 && data["test/hey"][0] == "hello") {

                $("#data").text("hello from hey")      
            }
        } else {
            $("#image").html("<img src='/static/img/titlePage.png' alt=''>");
        }
    });
}