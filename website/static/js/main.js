Vue.options.delimiters = ['[[', ']]'];


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
    }
})


Vue.component('v-pagination', {
    template: '\
                <div class="d-flex justify-content-center">\
                    <div v-for="i in pagination_count">\
                        <a :class="[base_class, i==active ? active_class : non_active]" style="\
                            color: white;\
                            font-weight: 600;\
                        "\
                        @click="goto(i)"\
                        >[[ i ]]</a>\
                    </div>\
                </div>\
            ',

    props: {
        link: String,
        size: String
    },

    data() {
        return {
            active: 1,
            pagination_count: null,
            pagination_next: null,
            pagination_previous: null,

            base_class: "btn m-3",
            active_class: 'btn-primary',
            non_active: 'btn-dark'
        }
    },

    created: function() {
        this.ask(this.link)
    },
    
    methods: {
        goto(number) {
            this.active = number
            this.ask(this.link+ "?limit=" + this.size + "&offset=" + (number-1)*10)
        },

        ask(url) {
            axios({
                method: 'get',
                url: url
            })
            .then((response) => {
                up()

                this.pagination_count = Math.trunc(response.data.count / 10) + 1
    
                app.posts = response.data.results;
            });
        }
    }
});

var t;
var up = function up() {
	var top = Math.max(document.body.scrollTop,document.documentElement.scrollTop);
	if(top > 0) {
		window.scrollBy(0,-100);
		t = setTimeout('up()',20);
	} else clearTimeout(t);
	return false;
}


var app = new Vue({
    el: '#app',

    data: {
        posts: [],
        source: 'habr'
    }
})