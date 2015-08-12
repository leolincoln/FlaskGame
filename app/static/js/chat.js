$(document).ready(function(){
    var currentUser = $('#welcomemessage')[0].textContent.split(' ')[3]
    console.log(currentUser)
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', function() {
        socket.emit('connect_message', {data: 'I\'m connected!','role': ''+currentUser});

    });

    socket.on('connect_message',function(msg){
        if($("#log").length != 0){
            $('#log').append('<br>'+ msg.time+' ' + msg.role+' : ' + msg.data);
        }
        if($("#log2").length != 0){
            $('#log2').append('<br>'+ msg.time+' ' + msg.role+' : ' + msg.data);
        }
    });

    socket.on('new_message', function(msg) {
        if(msg.role == 'judge' && msg.toRole == 'tester1'){
            if(currentUser=='judge'){
                $('#log').append('<br>'+ msg.time+' ' + msg.role+' : ' + msg.data);
            }
            else if(currentUser=='tester1'){
                $('#log').append('<br>'+ msg.time+' ' + msg.role+' : ' + msg.data);
            }
        }
        else if(msg.role == 'judge' && msg.toRole == 'tester2'){
            if(currentUser=='judge'){
                $('#log2').append('<br>'+ msg.time+' ' + msg.role+' : ' + msg.data);
            }
            else if(currentUser=='tester2'){
                $('#log').append('<br>'+ msg.time+' ' + msg.role+' : ' + msg.data);
            }
        }
        else if(msg.role == 'tester1'){
            if(currentUser=='tester1'){
                $('#log').append('<br>'+ msg.time+' ' + msg.role+' : ' + msg.data);
            }
            else if(currentUser=='judge'){
                $('#log').append('<br>'+ msg.time+' ' + msg.role+' : ' + msg.data);
            }
        }
        else if(msg.role == 'tester2'){
            if(currentUser=='tester2'){
                $('#log').append('<br>'+ msg.time+' ' + msg.role+' : ' + msg.data);
            }
            else if (currentUser=='judge'){
                $('#log2').append('<br>'+ msg.time+' ' + msg.role+' : ' + msg.data);
            }
        }
        //clean up messages
        $('input#usermsg2').val('')
        $('input#usermsg3').val('')
        if(currentUser=='judge'){
            $('input#usermsg').val('')
        }
    });

    if($("#myModal").length!=0){
        console.log("found mymodal")
        $('form#moneymodal1').submit(function(event){
            socket.emit('money_message',{data: $('#money').val(),toRole: 'tester1'});
            console.log('binding complete for form#mymodal')
            return false;
        });
    };
    if($("#myModal2").length!=0){
        console.log("found mymodal2")
        $('form#moneymodal2').submit(function(event){

            socket.emit('money_message',{data: $('#money2').val(),toRole: 'tester2'});
            console.log('binding complete for form#mymodal2')

            return false;
        });
    };

    if($("#broadcast").length != 0){
        $('form#broadcast').submit(function(event) {
            socket.emit('usr_message', {data: $('#usermsg').val(),toRole: 'tester1'});
            console.log('binding complete for broadcast1 submit button')
            return false;
        });
    };
    if($("#broadcast2").length != 0){
        $('form#broadcast2').submit(function(event) {
        socket.emit('usr_message', {data: $('#usermsg2').val(),toRole: 'tester2'});
        return false;
    });
    };
    if($("#broadcast3").length != 0){

        $('form#broadcast3').submit(function(event) {
        socket.emit('usr_message', {data: $('#usermsg3').val(),toRole: 'judge'});
        return false;
    });
    }
})