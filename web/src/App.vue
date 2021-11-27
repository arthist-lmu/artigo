<template>
  <div id="app">
    <v-navigation-drawer
      app
      permanent
    >
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title class="text-h6">
            ARTigo
          </v-list-item-title>
          <v-list-item-subtitle>
            Social Image Tagging
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>

      <v-divider></v-divider>

      <v-list
        dense
        nav
      >
        <v-list-item
          v-for="item in items"
          :key="item.title"
          link
        >
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>

      <v-divider></v-divider>

      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>
            Imprint
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-list-item>
          <v-list-item-title>
            <a href="https://www.lmu.de/de/footer/datenschutz/index.html">Privacy Policy</a>
          </v-list-item-title>
      </v-list-item>

    </v-navigation-drawer>

    <v-app-bar app>
      <AppBar />
    </v-app-bar>
    <v-main>
      <router-view />
    </v-main>
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>

<script>
  import AppBar from '@/components/AppBar.vue';
  export default { 
    components: {
    AppBar,
    },
    data () {
      return {
        items: [
          { title: 'About Artigo', icon: 'mdi-view-dashboard' },
          { title: 'ARTigo-Game', icon: 'mdi-image' },
          { title: 'Karido', icon: 'mdi-help-box' },
          { title: 'ARTigo-Quiz beta', icon: 'mdi-image' },
          { title: 'ARTigo-Taboo', icon: 'mdi-help-box' },
          { title: 'Tag A Tag beta', icon: 'mdi-image' },
          { title: 'Combino beta', icon: 'mdi-help-box' },
          { title: 'ARTime beta', icon: 'mdi-image' },
          { title: 'Crossover', icon: 'mdi-help-box' },
        ],
        right: null,
      }
    },
  }
</script>



<!-- <button
      class="btn btn-primary btn-margin"
      v-if="!authenticated"
      @click="login()">
      Log In

    </button>
    <p>
      <!-- use router-link component for navigation. -->
      <!-- specify the link by passing the `to` prop. -->
      <!-- `<router-link>` will be rendered as an `<a>` tag by default -->
<!--      <router-link to="/foo">Go to Foo</router-link>
      <router-link to="/bar">Go to Bar</router-link>
    </p> -->