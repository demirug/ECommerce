var methods = {};

$(document).ready(function() {

    $('#id_delivery_service').change(function() {
        $('#delivery-options').empty();

        if(methods[$(this).val()] !== undefined && methods[$(this).val()]['select_handler'] !== undefined) {
            methods[$(this).val()]['select_handler']()
        }
    }).trigger("change")


    $('form').submit(function() {
        val = $('#id_delivery_service').val()
        if(methods[val] !== undefined && methods[val]['document_generate'] !== undefined) {
            $('#id_delivery_data').val(methods[val]['document_generate']())
        }
    })


})