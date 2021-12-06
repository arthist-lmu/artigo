<template>
  <v-app-bar
    app
    flat
  >
  <h1>{{$router.currentRoute.name}}</h1>
  <v-spacer></v-spacer>
    <v-menu
      top
      :offset-y="offset"
      :close-on-click="closeOnClick"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          color="primary"
          dark
          v-bind="attrs"
          v-on="on"
        >
          {{locale}}
        </v-btn>
      </template>

      <v-list>
        <v-list-item
          v-for="(lang, index) in lang_list"
          :key="index"
          @click="onButtonClick(lang)"
        >
          <v-list-item-title>{{ lang }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
    <UserMenu />
  </v-app-bar>
</template>

<script>
import UserMenu from '@/components/UserMenu.vue';
import i18n from '@/plugins/i18n';

export default {
  data: () => ({
    closeOnClick: true,
    offset: true,
    locale: i18n.locale,
    lang_list: ['en', 'de'],
    reactive: true,
  }),
  components: {
    UserMenu,
  },
  methods: {
    onButtonClick(lang) {
      i18n.locale = lang;
    },
  },
};
</script>
