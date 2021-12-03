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
          max-height="281"
          max-width="500"
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
        <v-list-item>
          <router-link to="">{{ $t('navbar.about') }}</router-link>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
          <v-list-item-title>
            <router-link :to="'/' + $i18n.locale + '/publications'">
            {{ $t('navbar.publications') }}
            </router-link>
            </v-list-item-title>
          <v-list-item-subtitle>Research, literature, media</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <router-link to="">{{ $t('navbar.about') }}</router-link>
        </v-list-item>
        <v-list-item
          v-for="item in items"
          :key="item.title"
          link
        >
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title><router-link to="item.link">{{ $t('navbar.about') }}</router-link></v-list-item-title>
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
  components: {
    AppBar,
  },
  data() {
    return {
      items: [
        { title: i18n.t('navbar.about'), link: "", icon: 'mdi-view-dashboard' },
        { title: i18n.t('navbar.publications'), link: "/en/publications", icon: 'mdi-view-dashboard' },
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
