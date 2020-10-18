Vue.options.delimiters = ['[[', ']]'];


var app = new Vue({
    el: '#app',

    data: {
        posts: [],
        source: 'habr'
    }
})


var filters = new Vue({
    el: '#filters',

    data: {
        source: 'habr.com',
        date: 'сегодня',
        category: 'все'
    },

    watch: {
        source: function() {
            app.source = this.source.split('.')[0]
        }
    },

    created: function() {
        this.get_posts();
    },

    methods: {
        get_posts() {
            axios({
                method: 'post',
                url: "./filter-changed", 
                data: {
                    source: this.source,
                    date: this.date,
                    category: this.category
                }
            })
            .then((response) => {
                app.posts = response.data;
            });
        }
    }
})