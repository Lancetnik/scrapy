<template>
  <v-app style="background: #ffffff">
    <Sidebar/>

    <v-main style="padding-left: 330px">
      <div class="px-3">
        <Pagination :size='10' :link='`${this.$store.state.backendUrl}/post/`' 
          v-model="posts" :edges_size="2" active_class='btn-my' non_active_class='btn-light'/>

        <div v-if='cur_post_data'>
          <v-row justify='start'>
            <v-col style="flex: 0 0 20%;" v-for="post in posts" :key="post.id">
              <v-card class="p-3" style="height: 100%;">
                <div class="post-date">{{post.posted.replace("T", " ").replace('Z','')}}</div>
                <div class="mb-2"><a class="post-text" @click="select_post(post.id)"><b>{{post.title}}</b></a></div>
                <div class='link-bottom'><a :href="post.link" class="post-source" target="_blank">Источник: {{post.source}}</a></div>
              </v-card>
            </v-col>
          </v-row>

          <v-card class="p-3 mt-2" transition="scale-transition">
            <v-row class='px-3' justify="space-between">
              <span v-text="cur_post_data.title" class="post-title-detail"></span>
              <v-btn text color="black" @click="cur_post_data = null">
                Закрыть
              </v-btn>
            </v-row>
            <div class="mt-2" v-text="cur_post_data.text"></div>
          </v-card>
        </div>

        <v-card v-else class="mt-4 p-3" v-for="post in posts" :key="post.id">
          <div class="post-date">{{post.posted.replace("T", " ").replace('Z','')}}</div>
          <a class="post-title" @click="select_post(post.id)">{{post.title}}</a>
          <div class="post-text pl-3 mt-1">{{post.annotation}}</div>
          <a :href="post.link" class="post-source mt-1 pl-3" target="_blank">Источник: {{post.source}}</a>
        </v-card>
      </div>
    </v-main>

  </v-app>
</template>

<script>
import axios from 'axios'

import Pagination from '../components/pagination'
import Sidebar from '../components/sidebar'


export default {
  name: 'Start',

  components: {
    Pagination,
    Sidebar
  },

  data: () => ({
    posts: null,
    filter: '&source=habr.com',

    cur_post_data: null,
  }),

  methods: {
    select_post(index) {
      axios.get(`${this.$store.state.backendUrl}/post/${index}/`).then((response) => {
        this.cur_post_data = response.data
        console.log(response.data)
      })
    }
  }
}
</script>


<style scoped>
.post-title {
    font-size: 18px;
    color: black; 
    font-weight: 700;
}

.post-title:hover {
    cursor: pointer;
    text-decoration: underline;
}

.post-title-detail {
    font-size: 25px;
    color: black; 
    font-weight: 700;
}

.post-date {
    font-size: 14px;
    color: black; 
    font-weight: 300;
}

.post-text {
    font-size: 16px;
    color: #131313; 
    font-weight: 400;
    font-family: 'Open Sans', sans-serif;
}

.post-source {
    color: black;
    font-weight: 500;
}

.post-source:hover {
    color: black;
    cursor: pointer;
    text-decoration: underline;
}

.link-bottom {
  position: absolute;
  bottom: 0;
}
</style>