$(document).ready(function(){
    var socket = io.connect();
    socket.on('users_change', function(msg) {
        $('#log').append('Received: ' + msg.data).append($('<br>'));
    });
});
