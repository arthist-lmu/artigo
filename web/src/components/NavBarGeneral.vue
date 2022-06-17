<template>
  <div>
    <h3 class="mx-8 mt-4 uppercase">
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

    <h3 class="mx-8 mt-4 uppercase">
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
  </div>
</template>

<script>
export default {
  data() {
    return {
      dialog: {
        search: false,
      },
      games: [
        'default',
        'taboo',
        'tag-a-tag',
        'roi',
      ],
    };
  },
  methods: {
    goTo(page, query) {
      this.$router.push({ name: page, query });
    },
    focus(field) {
      document.getElementById(field).focus();
    },
  },
  components: {
    SearchCard: () => import('@/components/SearchCard.vue'),
  },
};
</script>

<style scoped>
.v-list-item__content {
  padding: 0 !important;
}
</style>
