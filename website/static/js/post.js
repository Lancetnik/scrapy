Vue.options.delimiters = ['[[', ']]'];


var app = new Vue({
    el: '#app',

    data: {
        post: JSON.parse(document.getElementById('data').textContent)
    }
})