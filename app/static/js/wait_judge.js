$(document).ready(function(){
    var currentRole = $('#welcomemessage')[0].textContent.split(' ')[3]
    console.log(currentRole)
    var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('disconnect', function () {
   console.log('disconnect client event....');
   socket.emit('disconnect_message', {data: 'I\'m disconnected!','fromRole': currentRole});
});
    socket.on('connect_message',function(msg){
      //the logic is 
      //if both testers logged in,
      //then judge should log in too. 
        //document.location.href = '/chat'
        console.log("in connect_message: toRole="+currentRole+'fromRole='+msg.fromRole)
        if($('#'+msg.fromRole+'_status').length!=0){
            $('#'+msg.fromRole+'_status').text("Ready!!!")
            $('#'+msg.fromRole+'_status').addClass('label-success').removeClass('label-default')
        }
        if($("#log").length != 0){
            //$('#log').append('<br>'+ msg.time+' ' + msg.role+' : ' + msg.data);

        }
    });

    socket.on('new_message', function(msg) {
        if(msg.role == 'judge' && msg.toRole == 'tester1'){
            if(currentRole=='judge'){
                $('#log').append('<br>'+ msg.time+' ' + msg.role+' : ' + msg.data);
            }
            else if(currentRole=='tester1'){
                $('#log').append('<br>'+ msg.time+' ' + msg.role+' : ' + msg.data);
            }
        }
        else if(msg.role == 'judge' && msg.toRole == 'tester2'){
            if(currentRole=='judge'){
                $('#log2').append('<br>'+ msg.time+' ' + msg.role+' : ' + msg.data);
            }
            else if(currentRole=='tester2'){
                $('#log').append('<br>'+ msg.time+' ' + msg.role+' : ' + msg.data);
            }
        }
        else if(msg.role == 'tester1'){
            if(currentRole=='tester1'){
                $('#log').append('<br>'+ msg.time+' ' + msg.role+' : ' + msg.data);
            }
            else if(currentRole=='judge'){
                $('#log').append('<br>'+ msg.time+' ' + msg.role+' : ' + msg.data);
            }
        }
        else if(msg.role == 'tester2'){
            if(currentRole=='tester2'){
                $('#log').append('<br>'+ msg.time+' ' + msg.role+' : ' + msg.data);
            }
            else if (currentRole=='judge'){
                $('#log2').append('<br>'+ msg.time+' ' + msg.role+' : ' + msg.data);
            }
        }
        //clean up messages
        $('input#usermsg2').val('')
        $('input#usermsg3').val('')
        if(currentRole=='judge'){
            $('input#usermsg').val('')
        }
    });

    socket.on('money_message',function(msg){
        console.log('in money_message');
        if(currentRole==msg.fromRole || currentRole==msg.toRole){
            if(currentRole == 'judge' && toRole == 'tester2'){
                $('#log2').append('<br>'+ msg.time+' ' + msg.fromRole+' sent ' +msg.toRole + ' $'+msg.money);
            }
            else{
                $('#log').append('<br>'+ msg.time+' ' + msg.fromRole+' sent ' +msg.toRole + ' $'+msg.money);
            }
            var affix = $('a#bankmoney').text().split(' ')[0]
            var currency = $('a#bankmoney').text().split(' ')[1]
            var number = Number(currency.replace(/[^0-9\.]+/g,""));
        if (currentRole == msg.fromRole){
            console.log(currency)
            console.log(number)
            console.log(affix)
            console.log(msg.money)
            number-=Number(msg.money);
            $('a#bankmoney').text(affix+' '+number)

        }
        else{
                        number+=Number(msg.money);
            $('a#bankmoney').text(affix+' '+number)

        }
        }
    });
    socket.on('err_message',function(msg){
        console.log('in err_message');
        if(currentRole == msg.fromRole){
            if (msg.toRole == 'tester1'){
                $('#log').append('<br>'+msg.time+' '+msg.money);
            }
            else if(msg.toRole == 'tester2'){
                $('#log2').append('<br>'+msg.time+' '+msg.money);
            }
            else{
                $('#log').append('<br>'+msg.time+' '+msg.money);
            }
        }
    });
    if(currentRole != 'judge'){
            var toRole = 'judge'
    }
    else{
            var toRole = null
    }
    if($("#myModal").length!=0){

        console.log("found mymodal")

        $('form#moneymodal1').submit(function(event){
            if(toRole == null){
            socket.emit('money_message',{data: $('#money').val(),toRole: 'tester1',fromRole: currentRole});
        }
        else{
            socket.emit('money_message',{data: $('#money').val(),toRole: toRole,fromRole: currentRole});
        }
            $('#myModal').modal('hide');
            $('money1').val(0)
            console.log('binding complete for form#mymodal')
            return false;
        });
    
    };
    if($("#myModal2").length!=0){
        console.log("found mymodal2")
        $('form#moneymodal2').submit(function(event){
            if(toRole == null){
            socket.emit('money_message',{data: $('#money2').val(),toRole: 'tester2',fromRole: currentRole});
        }
        else{
            socket.emit('money_message',{data: $('#money2').val(),toRole: toRole,fromRole: currentRole});

        }
            $('#myModal2').modal('hide');
            $('money2').val(0)
            console.log('binding complete for form#mymodal2')
            return false;
        });
    };

    if($("#broadcast").length != 0){
        $('form#broadcast').submit(function(event) {
            socket.emit('usr_message', {data: $('#usermsg').val(),toRole: 'tester1',fromRole: 'judge'});
            console.log('binding complete for broadcast1 submit button')
            return false;
        });
    };

    if($("#broadcast2").length != 0){
        $('form#broadcast2').submit(function(event) {
        socket.emit('usr_message', {data: $('#usermsg2').val(),toRole: 'tester2',fromRole: 'judge'});
        return false;
    });
    };

    if($("#broadcast3").length != 0){

        $('form#broadcast3').submit(function(event) {
        socket.emit('usr_message', {data: $('#usermsg3').val(),toRole: 'judge',fromRole: currentRole});
        return false;
    });
    }

    if($("#continue_button").length!=0){
        $('#continue_button').click(function(){
            socket.emit('continue_message', {fromRole: currentRole});
            socket.disconnect()
            //document.location.href = '/wait_judge'
        });
    }
    if($("#winner_tester1").length!=0){
        $('#winner_tester1').click(function(){
            socket.emit('winner_message', {fromRole: currentRole,toRole:'tester1'});
            document.location.href = '/wait_tester'
        });
    }
        if($("#winner_tester2").length!=0){
        $('#winner_tester2').click(function(){
            socket.emit('winner_message', {fromRole: currentRole,toRole:'tester2'});
            document.location.href = '/wait_tester'
        });
    }
})