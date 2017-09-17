$(function(){
$('#sumColumnEWTGroup').hide();

$('#btnClearAll').on('click', function(){
    console.log("Clearing....")
    $.ajax({
        url: "/clear_session/",
        method: 'GET', // or another (GET), whatever you need
        data: {
            "clear_all": 1 // data you need to pass to your function
        },
        success: function (data) {
            console.log("Cleared !!");
            window.location.href='/global/';

        }
    });
});


$('#aggregationTypeEWT').on('change',(function() {
            if($('#aggregationTypeEWT option:selected').val()==='SUM')
            {
            $('.sumColumnEWTGroup').show();
            }
            else
            {
            $('#sumColumnEWTGroup').hide();
            }
        }
        ));


});