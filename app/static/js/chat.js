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
        if(msg.role == 'judge' && msg.toUser == 'tester1'){
            if(currentUser=='judge'){
                $('#log').append('<br>'+ msg.time+' ' + msg.role+' : ' + msg.data);
            }
            else if(currentUser=='tester1'){
                $('#log').append('<br>'+ msg.time+' ' + msg.role+' : ' + msg.data);
            }
        }
        else if(msg.role == 'judge' && msg.toUser == 'tester2'){
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
        $('input#usermsg').val('')
        if(currentUser=='judge'){
            $('input#usermsg2').val('')
        }
    });



    if($("#broadcast").length != 0){
        $('form#broadcast').submit(function(event) {
            socket.emit('usr_message', {data: $('#usermsg').val(),toUser: 'tester1'});
            return false;
        });
    };
    if($("#broadcast2").length != 0){
        $('form#broadcast2').submit(function(event) {
        socket.emit('usr_message', {data: $('#usermsg2').val(),toUser: 'tester2'});
        return false;
    });
    };
    if($("#broadcast3").length != 0){

        $('form#broadcast3').submit(function(event) {
        socket.emit('usr_message', {data: $('#usermsg3').val(),toUser: 'judge'});
        return false;
    });
    }
})