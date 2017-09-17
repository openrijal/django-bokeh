$(function(){
$('#sumColumnEWTGroup').hide();
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