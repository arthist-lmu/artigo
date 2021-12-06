<template>
  <div id="app">
    <v-main>
      <v-navigation-drawer
      app
      permanent
      v-model="drawer"
    >
    <v-img
          id="logo"
          src="/assets/images/logo.svg"
        ></v-img>
      <v-list-item>
        
      </v-list-item>
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
        nav
      >
        <v-list-item
          v-for="nav_entry in nav_list"
          :key="nav_entry.title"
          link
        >
          <v-list-item-content>
            <v-list-item-title>
              <router-link :to="'/' + $i18n.locale + '/' + nav_entry.link">
              {{ nav_entry.title }}
              </router-link>
            </v-list-item-title>
            <v-list-item-subtitle>
              {{ nav_entry.subtitle }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>

      <v-divider></v-divider>

      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>
            {{ $t("navbar.imprint") }}
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-list-item>
          <v-list-item-title>
            <a href="https://www.lmu.de/de/footer/datenschutz/index.html">{{ $t("navbar.privacy") }}</a>
          </v-list-item-title>
      </v-list-item>

    </v-navigation-drawer>

    <AppBar />
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
#logo {
}
</style>

<script>
import AppBar from '@/components/AppBar.vue';
import i18n from '@/plugins/i18n.js'

export default {
  created(){
        document.title = "ARTigo - Social Image Tagging"},
  components: {
    AppBar,
  },
  data() {
    return {
      nav_list: [
        { link: "about", title: i18n.t('navbar.about'), subtitle: "Idea, Goals, Project details" },
        { link: "publications", title: i18n.t('navbar.publications'), subtitle: "Research, literature, media" },
        { link: "artigo-game", title: "Artigo-Game", subtitle: "Not implemented" },
        { link: "artigo-game", title: "Karido", subtitle: "Not implemented" },
        { link: "artigo-game", title: "ARTigo-Quiz", subtitle: "Not implemented" },
        { link: "artigo-game", title: "ARTigo-Taboo", subtitle: "Not implemented" },
        { link: "artigo-game", title: "Tag A Tag", subtitle: "Not implemented" },
        { link: "artigo-game", title: "Combino", subtitle: "Not implemented" },
        { link: "artigo-game", title: "ARTime", subtitle: "Not implemented" },
        { link: "artigo-game", title: "Crossover", subtitle: "Not implemented" },
      ],
    };
  },
};
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
