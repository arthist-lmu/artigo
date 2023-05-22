<template>
  <v-container :key="locale">
    <GameDrawer
      v-model="drawer"
      ref="drawer"
    />

    <v-row></v-row>

    <v-row
      v-if="creators && entries"
      style="flex: 0;"
    >
      <v-col
        :class="$vuetify.breakpoint.mdAndDown ? 'px-1 py-6' : 'pa-12'"
        :cols="$vuetify.breakpoint.mdAndDown ? 12 : 10"
      >
        <div :class="textSize">
          <Typer
            @onComplete="show('creator')"
            :strings="[$t('home.texts.intro')]"
            :loop="false"
          />

          <transition
            name="fade"
            mode="out-in"
            appear
          >
            <span
              v-if="typer.creator && creator"
              :key="creator"
            >
              {{ creator }}.
            </span>
          </transition>

          <Typer
            v-if="typer.prefix"
            @onComplete="show('examples')"
            class="space"
            :strings="[$t('home.texts.prefix')]"
            :loop="false"
          />

          <Typer
            v-if="typer.examples"
            @onComplete="show('button')"
            class="space"
            :removeBackspace="false"
            :strings="examples"
            :loop="false"
          />
        </div>
      </v-col>
    </v-row>

    <transition
      name="fade"
      appear
    >
      <v-row
        v-if="typer.button"
        style="flex: 0;"
      >
        <v-col
          :class="[$vuetify.breakpoint.mdAndDown ? 'px-1 pb-6' : 'px-12 pb-12', 'pt-0']"
          :cols="$vuetify.breakpoint.mdAndDown ? 12 : 10"
        >
          <v-btn
            @click="goTo('game')"
            outlined
            x-large
            rounded
            dark
          >
            {{ $t("home.fields.try-out") }}
          </v-btn>

          <v-btn
            @click="goTo('about')"
            :title="$t('about.title')"
            class="ml-2"
            x-large
            icon
            dark
          >
            <v-icon>
              mdi-help-circle-outline
            </v-icon>
          </v-btn>

          <v-chip
            style="background-color: transparent;"
            class="ml-10 pl-6"
            large
            dark
          >
            <small style="font-size: 12px;">European Union Prize <br>for Citizen Science</small>

            <img
              height="100%"
              class="ml-6 py-2"
              src="/assets/images/eu-citizen-science-prize-logo.png"
              alt="European Union Prize for Citizen Science Logo"
            />
          </v-chip>
        </v-col>
      </v-row>
    </transition>

    <v-dialog
      v-model="dialog.helper"
      max-width="400"
    >
      <HelperCard
        v-model="dialog.helper"
        :text="$t('language.helper')"
        icon="mdi-account-circle-outline"
      />
    </v-dialog>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      drawer: false,
      typer: {
        creator: false,
        prefix: false,
        examples: false,
        button: true,
      },
      dialog: {
        helper: false,
      },
      creator: null,
    };
  },
  methods: {
    show(name) {
      setTimeout(() => {
        this.$nextTick(() => {
          this.typer[name] = true;
          window.scrollTo(0, document.body.scrollHeight);
        });
      }, 250);
    },
    search(value, field) {
      const query = { [field]: value };
      this.$store.dispatch('search/post', { query });
    },
    goTo(name) {
      if (name === 'game') {
        if (!this.$vuetify.breakpoint.mdAndDown) {
          let params = {};
          this.entries.forEach((entry) => {
            if (entry.type === 'annotated-creator') {
              params = { ...params, ...entry.params };
            }
          });
          this.$store.commit('game/updateDialog', { params });
        }
        this.drawer = true;
      }
      this.$router.push({ name });
    },
  },
  computed: {
    locale() {
      return this.$i18n.locale;
    },
    textSize() {
      const values = ['accent--text'];
      switch (this.$vuetify.breakpoint.name) {
        case 'xs':
          values.push('text-h4');
          break;
        case 'sm':
          values.push('text-h3');
          break;
        default:
          values.push('text-h2');
          break;
      }
      return values;
    },
    data() {
      return this.$store.state.statistics.data;
    },
    entries() {
      return this.$store.state.home.data;
    },
    creators() {
      return this.data.creators;
    },
    examples() {
      return [
        this.$t('home.texts.example-1'),
        this.$t('home.texts.example-2'),
        this.$t('home.texts.example-3'),
        this.$t('home.texts.example-4'),
        this.$t('home.texts.example-5'),
        this.$t('home.texts.example-1'),
      ];
    },
  },
  watch: {
    locale() {
      this.typer = {
        creator: false,
        prefix: false,
        examples: false,
        button: true,
      };
    },
    typer: {
      handler({ creator, prefix }) {
        if (creator && !prefix) {
          let { names } = this.data.creators;
          names = this.shuffle(names).slice(0, 4);
          this.entries.forEach((entry) => {
            if (entry.type === 'annotated-creator') {
              names.push(entry.query);
            }
          });
          this.creator = names.shift();
          this.timer = setInterval(() => {
            if (names.length === 0) {
              clearInterval(this.timer);
              this.show('prefix');
            } else {
              this.creator = names.shift();
            }
          }, 1000);
        }
      },
      deep: true,
    },
  },
  mounted() {
    // see: @/components/game/Drawer.vue
    // this.$store.dispatch('statistics/get');
    window.scrollTo(0, document.body.scrollHeight);
  },
  created() {
    if (localStorage.getItem('langHelper') === null) {
      localStorage.setItem('langHelper', true);
      this.dialog.helper = true;
    }
  },
  components: {
    Typer: () => import('@/components/Typer.vue'),
    GameDrawer: () => import('@/components/game/Drawer.vue'),
    HelperCard: () => import('@/components/HelperCard.vue'),
  },
};
</script>

<style scoped>
.container {
  flex-direction: column;
  display: flex;
  height: 100%;
}

.text-h2 {
  line-height: 4.75rem;
}

.text-h2 .v-icon {
  font-size: 60px;
}

.text-h3 {
  line-height: 3.75rem;
}

.text-h3 .v-icon {
  font-size: 48px;
}

.text-h4 {
  line-height: 2.75rem;
}

.text-h4 .v-icon {
  font-size: 34px;
}

span.space::before {
  content: " ";
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity .5s
}

.fade-enter,
.fade-leave-to {
  opacity: 0
}
</style>
