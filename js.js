$.ajax({
    type: "POST",
    url: 'API',

    data: {
        'пасивный переменный': 'переменная',
        'timeN': Date.now()
    },
    async: false,
    success: function(data) {
        console.log('Ответ от API - ', data);
    }
});