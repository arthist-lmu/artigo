<template>
  <v-navigation-drawer
    class="pl-2"
    color="transparent"
    width="400"
    clipped
    app
  >
    <v-img
      @click="goTo('home')"
      src="/assets/images/logo.svg"
      class="mx-8 mb-4"
      style="cursor: pointer;"
      max-width="250"
    />

    <v-list
      dense
      flat
    >
      <v-list-item
        v-for="page in pages"
        :key="page"
        dense
      >
        <v-list-item-content>
          <v-list-item-title>
            <v-btn
              @click="goTo(page)"
              text
            >
              {{ $t(page)["title"] }}
            </v-btn>
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>

    <h3 class="mx-8 mt-4">
      {{ $t("search.title") }}
    </h3>

    <v-list
      dense
      flat
    >
      <v-list-item dense>
        <v-list-item-content>
          <v-list-item-title>
            <v-btn
              @click="focus('search')"
              text
            >
              <v-icon
                color="primary"
                left
              >
                mdi-arrow-right-box
              </v-icon>

              {{ $t("search.fields.default") }}
            </v-btn>
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-list-item dense>
        <v-list-item-content>
          <v-list-item-title>
            <v-dialog
              v-model="dialog.search"
              max-width="400"
            >
              <template v-slot:activator="{ on }">
                <v-btn
                  v-on="on"
                  text
                >
                  <v-icon
                    color="primary"
                    left
                  >
                    mdi-arrow-right-box
                  </v-icon>

                  {{ $t("search.fields.advanced") }}
                </v-btn>
              </template>

              <SearchCard
                v-model="dialog.search"
                :isDialog="true"
              />
            </v-dialog>
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>

    <h3 class="mx-8 mt-4">
      {{ $t("game.title") }}
    </h3>

    <v-list
      dense
      flat
    >
      <v-list-item
        v-for="game in games"
        :key="game"
        dense
      >
        <v-list-item-content>
          <v-list-item-title>
            <v-btn
              @click="goTo('game', { type: game })"
              text
            >
              <v-icon
                color="primary"
                left
              >
                mdi-arrow-right-box
              </v-icon>

              {{ $t("game.fields")[game]["title"] }}

              <v-btn
                v-if="['default', 'taboo'].includes(game)"
                @click.stop="goTo('about', { tab: 'game' })"
                class="ml-2 mr-n2"
                color="primary"
                small
                icon
              >
                <v-icon small>
                  mdi-help-circle
                </v-icon>
              </v-btn>
            </v-btn>
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
import router from '@/router/index';

import SearchCard from '@/components/SearchCard.vue';

export default {
  data() {
    return {
      pages: [
        'about',
        'highscore',
      ],
      dialog: {
        search: false,
      },
      games: [
        'default',
        'taboo',
        'tag-a-tag',
      ],
    };
  },
  methods: {
    goTo(page, query) {
      router.push({ name: page, query });
    },
    focus(field) {
      document.getElementById(field).focus();
    },
  },
  components: {
    SearchCard,
  },
};
</script>

<style>
.v-navigation-drawer__border {
  display: none;
}
</style>

<style scoped>
.v-navigation-drawer {
  background-color: transparent;
}

.v-list-item__content {
  padding: 0 !important;
}

h3 {
  text-transform: uppercase;
}
</style>
