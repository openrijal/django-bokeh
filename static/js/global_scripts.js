$(function () {
    $('#sumColumnEWTGroup').hide();
    $('#primary_param_div').hide();

    $('#btnClearAll').on('click', function () {
        console.log("Clearing....")
        $.ajax({
            url: "/clear_session/",
            method: 'GET', // or another (GET), whatever you need
            data: {
                "clear_all": 1 // data you need to pass to your function
            },
            success: function (data) {
                console.log("Cleared !!");
                window.location.href = '/global/';

            }
        });
    });


    $('#plot_type').on('change', function () {
       selected_type=$(this).val();
       alert(selected_type);
       options="";
       if(selected_type=="bar" || selected_type=="line")
       {
            options+= '   <option value="MLG">MLG</option>';
             options+= '   <option value="RPR_DT">RPR DT</option>';
               $('#x_prim_param')
          .append(options);
          $('#primary_param_div').show();

       }
       else
       {
            $('#primary_param_div').hide();
            $("#x_prim_param").val('')
       }
    });

    // $('#btnSaveAll').on('click', function () {
    //     console.log("Saving....");
    //     some_random = Math.floor((Math.random() * 100000000) + 1);
    //     $.ajax({
    //         url: "/save_session/",
    //         method: 'GET', // or another (GET), whatever you need
    //         data: {
    //             "canvas_name": "untitled-" + some_random // data you need to pass to your function
    //         },
    //         success: function (data) {
    //             console.log("Saved !!");
    //             window.location.href = '/list_plots/';
    //         }
    //     });
    // });


    $('#aggregationTypeEWT').on('change', (function () {
            if ($('#aggregationTypeEWT option:selected').val() === 'SUM') {
                $('.sumColumnEWTGroup').show();
            }
            else {
                $('#sumColumnEWTGroup').hide();
            }
        }
    ));


});

$("#formEWT").submit(function (e) {
    e.preventDefault();
    var compareTypeEWT = $('#compareTypeEWT').val();
    var aggregationTypeEWT = $('#aggregationTypeEWT').val();
    var sumColumnEWT = $('#sumColumnEWT').val();
    var plot_type=  $('#plot_type').val();
    var prim_param= $('#x_prim_param').val();
    var data={};
    data["plot_type"]=plot_type;
    data ["x_prim_param"]=prim_param;
      data["x_prim_bm"]="";
        data["x_prim_bp"]="";
    if(prim_param=="MLG")
    {
        data["x_prim_bm"]="number";
        data["x_prim_bp"]="1000";
    }
    else if (prim_param=="RPR_DT")
    {
        data["x_prim_bm"]="DATE";
        data["x_prim_bp"]="MONTH";
    }
    data["x_cat_param"]=compareTypeEWT;
    data["y_am"]=aggregationTypeEWT;
    data["y_ap"]=""
    if(aggregationTypeEWT=="SUM")
        data["y_ap"]=sumColumnEWT
   alert(JSON.stringify(data));
});

/*$("#formEWT").submit(function (e) {
    e.preventDefault();
    var compareTypeEWT = $('#compareTypeEWT').val();
    var aggregationTypeEWT = $('#aggregationTypeEWT').val();
    var sumColumnEWT = $('#sumColumnEWT').val();
    $.ajax("/get_iframe", {
        method: 'POST',
        data: {
            'compare_parameter': compareTypeEWT,
            'aggregation_method': aggregationTypeEWT,
            'aggregation_parameter': sumColumnEWT
        }
    }).done(function (data) {
        $('#plot_container').append(data);
        $('#inputSelModal').modal('toggle');
        $('#btnSaveAll').removeClass('hide');
        $('#btnClearAll').removeClass('hide');
    });
});*/


$("#filterIframeForm .form-control").change(function (e) {
    $("#filterIframeForm").submit();
});

$('#savePlotInput').submit(function (e) {
    e.preventDefault();
    var allPlots = new Array();
    $('iframe').each(function () {
        var singlePlot = {};
        singlePlot['default_filters'] = $(this).contents().find('#filFrmDefault').val();
        singlePlot['eng'] = $(this).contents().find('#filFrmEng').val();
        singlePlot['tran'] = $(this).contents().find('#filFrmTran').val();
        singlePlot['miles'] = $(this).contents().find('#filFrmMiles').val();
        singlePlot['freq'] = $(this).contents().find('#filFrmFreq').val();
        allPlots.push(singlePlot);
    });
    $.ajax('/save_session/', {
        method: 'POST',
        data: {
            'canvas_name': $('#canvasName').val(),
            'allPlots': JSON.stringify(allPlots)
        }
    }).done(function () {
       $('#savePlotModal').modal('hide');
    });
});


$('.plot_link').click( function(e) {
    e.preventDefault();
    var obj = JSON.parse($(this).attr('mydata'));
    var name=$(this).attr('myname');
    $('#plot_container').empty();
      $('#plot_container').append('<span class="label label-default full-width">Canvas Name:'+name+'</span>')
   e.target.parentElement.click();
    for (var i = 0, len = obj.length; i < len; ++i) {
         var filters = obj[i];
         plot_vars=filters.default_filters.split("&");
         compare_parameter= plot_vars[0].split("=")[1];
         aggregation_method= plot_vars[1].split("=")[1];
         aggregation_parameter= plot_vars[2].split("=")[1];

         $.ajax("/get_iframe", {
        method: 'POST',
        data: {
            'compare_parameter': compare_parameter,
            'aggregation_method': aggregation_method,
            'aggregation_parameter': aggregation_parameter
        }
    }).done(function (data) {


        $('#plot_container').append(data);
    });
    }

    return false;
} );