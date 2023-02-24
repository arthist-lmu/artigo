<template>
  <v-hover v-slot="{ hover }">
    <v-card
      @click="play"
      @keydown="play"
      class="grid-item"
      :disabled="isDisabled"
      flat
    >
      <img
        :src="entry.path"
        v-on:error="onError"
        alt=""
      />

      <v-fade-transition>
        <v-container v-if="hover && entry.status === 'F'">
          <v-row
            justify="center"
            align="center"
          >
            <v-col cols="auto">
              <v-btn
                color="primary"
                large
                fab
              >
                <v-icon color="accent">
                  mdi-play
                </v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </v-container>
      </v-fade-transition>

      <v-container class="overlay">
        <v-row style="flex: 0;">
          <v-col class="pa-4">
            <div class="text-subtitle-1 white--text">
              <b>{{ entry.title[lang] }}</b>

              <v-icon
                v-if="entry.access === 'O'"
                :title="$t('collections.fields.access-open')"
                class="ml-2 mb-1"
                color="white"
                small
              >
                mdi-lock-open-variant-outline
              </v-icon>

              <v-icon
                v-if="entry.access === 'P'"
                :title="$t('collections.fields.access-pending')"
                class="ml-2 mb-1"
                color="white"
                small
              >
                mdi-progress-pencil
              </v-icon>

              <v-icon
                v-if="entry.access === 'R'"
                :title="$t('collections.fields.access-restricted')"
                class="ml-2 mb-1"
                color="white"
                small
              >
                mdi-lock-outline
              </v-icon>
            </div>

            <div class="text-caption">
              <v-icon
                class="mt-n1"
                color="white"
                x-small
                left
              >
                mdi-clock-outline
              </v-icon>

              <span>{{ date }}</span>
            </div>
          </v-col>

          <v-col cols="auto">
            <v-menu @click.native.stop.prevent>
              <template v-slot:activator="{ attrs, on }">
                <v-btn
                  v-bind="attrs"
                  v-on="on"
                  color="white"
                  icon
                >
                  <v-icon>
                    mdi-dots-vertical
                  </v-icon>
                </v-btn>
              </template>

              <v-list>
                <v-list-item @click="dialog.change = true">
                  <v-list-item-content>
                    {{ $t('collections.fields.change') }}
                  </v-list-item-content>
                </v-list-item>

                <v-list-item @click="dialog.remove = true">
                  <v-list-item-content>
                    {{ $t('collections.fields.remove') }}
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            </v-menu>
          </v-col>
        </v-row>

        <v-row></v-row>

        <v-row style="flex: 0;">
          <v-col class="pa-4" align="right">
            <v-btn
              @click.stop=""
              color="primary"
              style="min-width: 50px !important;"
              depressed
              rounded
            >
              <v-icon left>
                mdi-file-image-outline
              </v-icon>

              {{ entry.resources.length }}
            </v-btn>
          </v-col>
        </v-row>
      </v-container>

      <v-dialog
        v-model="dialog.remove"
        max-width="450"
      >
        <RemoveConfirmCard
          v-model="dialog.remove"
          :entry="entry"
        />
      </v-dialog>

      <v-dialog
        v-model="dialog.change"
        max-width="450"
      >
        <ChangeConfirmCard
          v-model="dialog.change"
          :entry="entry"
        />
      </v-dialog>
    </v-card>
  </v-hover>
</template>

<script>
export default {
  props: {
    entry: Object,
    height: {
      type: String,
      default: '225',
    },
  },
  data() {
    return {
      isDisabled: false,
      dialog: {
        remove: false,
        change: false,
      },
    };
  },
  methods: {
    play() {
      const params = {
        resource_inputs: this.entry.resources,
        resource_type: 'custom_resource',
        resource_max_last_played: 0,
        resource_min_tags: 0,
      };
      this.$store.commit('game/updateDialog', { params });
      this.$router.push({ name: 'game' });
    },
    onError() {
      this.isDisabled = true;
    },
  },
  computed: {
    lang() {
      return this.$i18n.locale;
    },
    date() {
      const created = new Date(this.entry.created);
      return created.toLocaleDateString(this.lang);
    },
  },
  watch: {
    'entry.status': {
      handler(value) {
        if (value === 'F') {
          this.isDisabled = false;
        } else {
          this.isDisabled = true;
        }
      },
      immediate: true,
    },
  },
  components: {
    ChangeConfirmCard: () => import('@/components/collection/ChangeConfirmCard.vue'),
    RemoveConfirmCard: () => import('@/components/collection/RemoveConfirmCard.vue'),
  },
};
</script>

<style scoped>
.container {
  position: absolute;
  width: 100%;
  bottom: 0;
  left: 0;
}

.container {
  flex-direction: column;
  display: flex;
  height: 100%;
}

.container .overlay {
  background: linear-gradient(to bottom, black, #00000000 40%);
  transform: translate(-50%, -50%);
  position: absolute;
  object-fit: cover;
  min-width: 100%;
  max-width: 100%;
  color: #ffffff;
  height: 100%;
  left: 50%;
  top: 50%;
}

.container .overlay .col > * {
  text-overflow: ellipsis;
  line-height: 1.25rem;
  white-space: nowrap;
  overflow: hidden;
}
</style>
