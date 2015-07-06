$(document).ready(function(){
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', function() {
        socket.emit('usr_message', {data: 'I\'m connected!'});

    });

    socket.on('new_message', function(msg) {
        $('#log').append('<br>'+ msg.time+' ' + msg.role+' : ' + msg.data);
        $('input#usermsg').val('')
    });
    $('form#broadcast').submit(function(event) {
        socket.emit('usr_message', {data: $('#usermsg').val()});
        return false;
    });
})
