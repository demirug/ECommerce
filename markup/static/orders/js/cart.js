$(document).ready(function() {
    let csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value
    total_price = $('#totalPrice')
    $('button.close').click(function (e) {
        parent = $(this).parents('.parent');
         $.ajax({
            url: '/cart-operation/',
            type: 'post',
            data: {
                'operation': 'set',
                'slug': parent.attr('product'),
                'value': 0,
                'csrfmiddlewaretoken': csrf_token,
            },
            success: function (response) {
                parent.remove()
            }

        });
    })

    $('input').change(function (e) {
        parent = $(this).parents('.parent');
        price = parent.find('.price-field')

        $.ajax({
            url: '/cart-operation/',
            type: 'post',
            data: {
                'operation': 'set',
                'slug': parent.attr('product'),
                'value': $(this).val(),
                'csrfmiddlewaretoken': csrf_token,
            },
            success: function (response) {
                let data = JSON.parse(response)
                e.target.value = data['count']
                price.text(data['price'])

                var total = 0
                $('.price-field').each(function(index) {
                   total += Number($(this).text())
                })

                total_price.text(total)


            }
        });
    })


})
