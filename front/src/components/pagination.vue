<template>
    <div class="container justify-content-start row">
        <div class="col-4">
            <div class="row">
                <label style="margin-top: 22px; font-weight: 600">Номер страницы: </label>
                <input type="text" v-model="active" @keyup.enter="goto(active)"
                            class="form-control" style="width: 55px; height: 40px; margin: 15px; border: 1px solid black; font-weight: 600">
            </div>
        </div>
        
        <div class="col-4">
        
            <div v-if="pagination_lenght < 8" class="d-flex justify-content-center">
                <a :class="[base_class, non_active_class]" aria-label="Previous"
                    @click="decrement">
                        <span aria-hidden="true">&laquo;</span>
                        <span class="sr-only">Previous</span>
                </a>
                
                <div v-for="i in pagination_lenght" :key="i">
                    <a :class="[base_class, i==active ? active_class : non_active_class]"
                    @click="goto(i)"
                    >{{i}}</a>
                </div>
                
                <a :class="[base_class, non_active_class]" aria-label="Next"
                    @click="increment">
                        <span aria-hidden="true">&raquo;</span>
                        <span class="sr-only">Next</span>
                </a>
            </div>
        
            <div v-else class="d-flex justify-content-center">
                
                <a :class="[base_class, non_active_class]" aria-label="Previous"
                    @click="decrement">
                        <span aria-hidden="true">&laquo;</span>
                        <span class="sr-only">Previous</span>
                </a>
                
                <div v-for="i in edges_size" :key="i">
                    <a :class="[base_class, active==i ? active_class : non_active_class]"
                    @click="goto(i)"
                    >{{i}}</a>
                </div>
                
                <div v-if="first">
                    <a :class="[base_class, non_active_class]"
                    >...</a>
                </div>
                
                <div v-for="i in pagination_count.slice(start_pagination, start_pagination+3)" :key="i">
                        <a :class="[base_class, i==active ? active_class : non_active_class]"
                        @click="goto(i)"
                        >{{i}}</a>
                </div>
                
                <div v-if="second">
                    <a :class="[base_class, non_active_class]">...</a>
                </div>
                
                <div v-for="i in lasts" :key="i">
                    <a :class="[base_class, active==i ? active_class : non_active_class]"
                    @click="goto(i)"
                    >{{i}}</a>
                </div>
                
                <a :class="[base_class, non_active_class]" aria-label="Next"
                    @click="increment">
                        <span aria-hidden="true">&raquo;</span>
                        <span class="sr-only">Next</span>
                </a>
            </div>
            
        </div>
        
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'Pagination',

    props: {
            link: {
                type: String,
                required: true,
            },
            size: {
                type: Number,
                required: true,
            },
            edges_size: {
                type: Number,
                required: false,
                default: 1,
            },

            base_class: {
                type: String,
                required: false,
                default: 'btn m-3',
            },
            active_class: {
                type: String,
                required: false,
                default: 'btn-primary',
            },
            non_active_class: {
                type: String,
                required: false,
                default: 'btn-dark',
            }
        },

    data: () => ({
        active: 1, // number of active elements
        pagination_count: 1, // array [2 ... pagination_lenght-1 ]
        pagination_lenght: 1, // number of pages
        start_pagination: 0, // start of dynamic block
        first: false, // first ...
        second: true, // second ...

        pagination_next: null,
        pagination_previous: null,
        lasts: null
    }),

    computed: {
        filter() {return this.$store.state.filter}
    },

    created: function() {
            this.ask(this.link+'?page=1' + this.filter)
        },

    watch: {
        filter() {
            this.active = 1
            this.ask(this.link+'?page=1' + this.filter)
        },

        active: function() {
            this.start_pagination = this.active - (2 + this.edges_size)

            if (this.active > 2 + this.edges_size) { this.first = true }
            else { this.first = false }

            if (this.pagination_lenght - this.active <= 2 + this.edges_size) { this.second = false }
            else { this.second = true }

            if ( this.start_pagination < 0 ) { this.start_pagination = 0 }
            if ( this.second == false ) { this.start_pagination = this.pagination_lenght - 3 - this.edges_size*2 }
        }
    },

    methods: {
        decrement() {
            if (this.active > 1) {
                this.active--
                this.ask(this.pagination_previous)
            }
        },

        increment() {
            if (this.active < this.pagination_lenght) {
                this.active++
                this.ask(this.pagination_next)
            }
        },

        goto(number) {
            this.active = number
            this.ask(this.link+ "?page=" + (number) + this.filter)
        },

        ask(url) {
            axios({
                method: 'get',
                url: url
            })
            .then((response) => {
                this.pagination_lenght = Math.ceil(response.data.count / 10)
                if(this.edges_size > 1) {
                    this.pagination_count = [...Array(this.pagination_lenght).keys()].slice(1+this.edges_size, -(this.edges_size-1))
                }
                else {
                    this.pagination_count = [...Array(this.pagination_lenght).keys()].slice(2)
                }
                this.lasts = [...Array(this.pagination_lenght+1).keys()].slice(-this.edges_size)

                this.pagination_previous = response.data.previous
                this.pagination_next = response.data.next

                this.$emit('input', response.data.results)
            });
        }
    }
}
</script>

<style scoped>
    .btn-my {
        color: wheat !important;
        background-color: #AB47BC;
    }
</style>