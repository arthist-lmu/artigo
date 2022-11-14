<template>
  <v-container :key="$i18n.locale">
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
              v-if="dialog.creator && creator"
              :key="creator"
              @click="search(creator, 'creators')"
              @keydown="search(creator, 'creators')"
              class="creator space"
              style="cursor: pointer;"
            >
              <span>{{ creator }}</span>
            </span>
          </transition>

          <Typer
            v-if="dialog.prefix"
            @onComplete="show('examples')"
            class="space"
            :strings="[$t('home.texts.prefix')]"
            :loop="false"
          />

          <Typer
            v-if="dialog.examples"
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
        v-if="dialog.button"
        style="flex: 0;"
      >
        <v-col
          :class="[$vuetify.breakpoint.mdAndDown ? 'px-1 pb-6' : 'px-12 pb-12', 'pt-0']"
          :cols="$vuetify.breakpoint.mdAndDown ? 12 : 10"
        >
          <v-btn
            @click="goToGame()"
            outlined
            x-large
            rounded
            dark
          >
            {{ $t("home.fields.try-out") }}
          </v-btn>

          <v-btn
            @click="search('', 'all-text')"
            :title="$t('search.title')"
            class="ml-2"
            x-large
            icon
            dark
          >
            <v-icon>
              mdi-magnify
            </v-icon>
          </v-btn>
        </v-col>
      </v-row>
    </transition>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      drawer: false,
      dialog: {
        creator: false,
        prefix: false,
        examples: false,
        button: true,
      },
      creator: null,
    };
  },
  methods: {
    show(name) {
      setTimeout(() => {
        this.$nextTick(() => {
          this.dialog[name] = true;
          window.scrollTo(0, document.body.scrollHeight);
        });
      }, 250);
    },
    search(value, field) {
      const query = { [field]: value };
      this.$store.dispatch('search/post', { query });
    },
    goToGame() {
      if (!this.$vuetify.breakpoint.mdAndDown) {
        const values = { show: true, params: {} };
        this.$store.commit('game/updateDialog', values);
        this.$router.push({ name: 'game' });
      }
      this.drawer = true;
    },
  },
  computed: {
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
    dialog: {
      handler({ creator, prefix }) {
        if (creator && !prefix) {
          let { names } = this.data.creators;
          names = this.shuffle(names).slice(0, 4);
          this.entries.forEach((entry) => {
            if (entry.type === 'creator') {
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
  },
  components: {
    Typer: () => import('@/components/Typer.vue'),
    GameDrawer: () => import('@/components/game/Drawer.vue'),
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

.text-h3 {
  line-height: 3.75rem;
}

.text-h4 {
  line-height: 2.75rem;
}

span.space::before {
  content: " ";
}

.creator::after {
  content: ". ";
}

.creator > span {
  border-bottom: 2px rgb(247, 248, 251) solid;
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
