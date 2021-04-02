<template>
  <v-navigation-drawer
    fixed
    absolute
    dark
    color='purple darken-2'
    width="330px"
    class="sidebar"
  >
    <v-list-item 
      disabled
      style="margin-top: 25px; margin-right: 60px;"
      class="text-center"
    >
      <v-list-item-content>
        <v-list-item-title>
          <span class='title'>IT Mozhayka</span>
        </v-list-item-title>
        <v-list-item-subtitle>
          <span class='subtitle'>news</span>
        </v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>

    <v-list
      nav
      dense
      style="margin-top: 40px"
    >
      <v-list-item-group>
        
        <v-list-item>
            <v-select
            :items="sources"
            label="Источник"
            v-model="source"
          ></v-select>
        </v-list-item>

        <v-list-item>
          <v-menu
          v-model="menu"
          :close-on-content-click="false"
          :nudge-right="40"
          transition="scale-transition"
          offset-y
          min-width="auto"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-text-field
                v-model="start_date"
                label="С"
                prepend-icon="mdi-calendar"
                readonly
                v-bind="attrs"
                v-on="on"
              ></v-text-field>
            </template>
            <v-date-picker
              v-model="start_date"
              @input="menu = false"
            >
              <v-spacer></v-spacer>
              <v-btn
                text
                color="primary"
                @click="start_date = ''; menu = false;"
              >
                Clear
              </v-btn>
              <v-btn
                text
                color="primary"
                @click="menu = false"
              >
                Cancel
              </v-btn>
            </v-date-picker>
          </v-menu>
          <input class='ml-3 time' type="time" v-model="start_time">
        </v-list-item>

        <v-list-item>
          <v-menu
          v-model="menu2"
          :close-on-content-click="false"
          :nudge-right="40"
          transition="scale-transition"
          offset-y
          min-width="auto"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-text-field
                v-model="end_date"
                label="По"
                prepend-icon="mdi-calendar"
                readonly
                v-bind="attrs"
                v-on="on"
              ></v-text-field>
            </template>
            <v-date-picker
              v-model="end_date"
              @input="menu2 = false"
            >
              <v-spacer></v-spacer>
              <v-btn
                text
                color="primary"
                @click="end_date = ''; menu2 = false;"
              >
                Clear
              </v-btn>
              <v-btn
                text
                color="primary"
                @click="menu2 = false"
              >
                Cancel
              </v-btn>
            </v-date-picker>
          </v-menu>
          <input class='ml-3 time' type="time" v-model="end_time">
        </v-list-item>

        <v-list-item>
          <v-text-field
              label="Поиск"
              v-model="search"
          ></v-text-field>
        </v-list-item>

        <v-list-item class="mt-2">
          <v-autocomplete
              v-model="tags_to_search"
              :items="tags"
              dense
              chips
              label="Поиск по тегам"
              small-chips
              deletable-chips
              multiple
              clearable
            >
              <template v-slot:selection="data">
                <v-chip 
                  color="white"
                  class="my-2 mx-1"
                  outlined
                >{{data.item}}
                </v-chip>
              </template>
            </v-autocomplete>
        </v-list-item>

        <v-list-item>
          <v-btn
                text
                @click="Clear()"
          >
            Clear filter
          </v-btn>
        </v-list-item>

      </v-list-item-group>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Sidebar',

  data: () => ({
    source: 'Любой',

    sources: [
      'habr.com',
      'www.securitylab.ru',
      'www.itsec.ru',
      'www.kaspersky.ru',
      'fstec.ru',
      'Любой'
    ],

    start_date: '',
    end_date: new Date().toISOString().substr(0, 10),

    start_time: '',
    end_time: '',

    menu: false,
    menu2: false,

    search: '',

    tags: [],
    tags_to_search: []
  }),

  computed: {
    start_datetime() {
      if (this.start_date && !this.start_time) return this.start_date + 'T0:00:00'
      else if (this.start_date && this.start_time) return this.start_date + 'T' + this.start_time + ":00"
      else return ''
    },

    end_datetime() {
      if (this.end_date && !this.end_time) return this.end_date + 'T0:00:00'
      else if (this.end_date && this.end_time) return this.end_date + 'T' + this.end_time + ":00"
      else return ''
    },

    filter_string() {
        let source = ''
        if (this.source!='Любой') source = this.source
        return `&source=${source}&posted_after=${this.start_datetime}&posted_before=${this.end_datetime}&tags=${this.tags_to_search.join()}&title=${this.search}`
    },
  },

  watch: {
    filter_string() {
      this.$store.commit('setFilter', this.filter_string)
    }
  },

  created() {
    this.$store.commit('setFilter', this.filter_string)

    axios({
        method: 'get',
        url: `${this.$store.state.backendUrl}/post/tags/`
    })
    .then((response) => {
      this.tags = response.data
    })
  },

  methods: {
    Clear() {
      this.start_date = ''
      this.start_time = ''
      this.end_date = ''
      this.end_time = ''
      this.source = ''
      this.search = ''
      this.tags_to_search = []
    }
  }
}
</script>


<style scoped>
  .sidebar {
    border-top-right-radius: 40px;
    box-shadow: 2px 0px 20px rgba(134, 87, 233, 0.8);
  }

  .title {
    font-family: Century Gothic;
    font-weight: bold;
    font-size: 30px;
    line-height: 37px;
    text-transform: uppercase;
  }

  .subtitle {
    font-family: Century Gothic;
    font-size: 15px;
    line-height: 18px;
    letter-spacing: 0.1em;
    text-transform: lowercase;
  }

  .link_text {
    font-family: Century Gothic;
    font-size: 22px;
    line-height: 27px;
    margin-left: 40px;
  }

  .router-link {
    margin-top: 40px;
  }

  .router-link:hover {
    text-decoration: none;
  }

  .time {
    color: #ffffff;
    cursor: pointer;
  }

  .time::-webkit-calendar-picker-indicator {
    color: #ffffff;
    cursor: pointer;
    display: none;
  }
</style>