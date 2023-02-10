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
              <b>{{ entry.name }}</b>
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
            <v-btn
              @click.stop="remove"
              color="white"
              icon
            >
              <v-icon>
                mdi-close
              </v-icon>
            </v-btn>
          </v-col>
        </v-row>

        <v-row></v-row>

        <v-row style="flex: 0;">
          <v-col class="pa-4" align="right">
            <v-btn
              color="primary"
              style="min-width: 50px !important;"
              depressed
              absolute
              rounded
              bottom
              right
            >
              <v-icon left>
                mdi-file-image-outline
              </v-icon>

              {{ entry.resources.length }}
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
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
    remove() {
      this.$store.dispatch('collection/remove', this.entry).then(() => {
        this.$store.dispatch('collection/post');
      });
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
    time() {
      const created = new Date(this.entry.created);
      return created.toLocaleTimeString(this.lang);
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
