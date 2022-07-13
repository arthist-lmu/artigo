<template>
  <v-footer
    :dark="dark"
    padless
    fixed
    inset
    app
  >
    <v-container
      :class="{
        'px-7': isSmAndDown,
        transparent: hasOpacity,
      }"
    >
      <v-row>
        <v-col
          :cols="isSmAndDown ? '4' : '6'"
          align="left"
        >
          <v-btn
            @click="goTo('about')"
            :title="$t('about.title')"
            :color="dark ? 'accent' : 'primary'"
            depressed
            rounded
            small
          >
            <v-icon left>
              mdi-information-outline
            </v-icon>

            2010–{{ new Date().getFullYear() }}
          </v-btn>

          <v-chip
            v-if="!isSmAndDown"
            style="background-color: transparent;"
            class="ml-2"
            small
          >
            Ludwig-Maximilians-Universität München
          </v-chip>
        </v-col>

        <v-col
          :cols="isSmAndDown ? '8' : '6'"
          align="right"
        >
          <v-btn
            :href="api"
            target="_blank"
            small
            icon
          >
            <v-icon>
              mdi-api
            </v-icon>
          </v-btn>

          <v-btn
            v-for="page in pages"
            :key="page"
            @click="goTo(page)"
            class="ml-2"
            color="grey lighten-2"
            outlined
            rounded
            small
          >
            {{ $t(`${page}.title`) }}
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
  </v-footer>
</template>

<script>
export default {
  props: {
    dark: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      pages: [
        'imprint',
        'privacy-policy',
      ],
    };
  },
  methods: {
    goTo(name) {
      this.$router.push({ name });
    },
  },
  computed: {
    api() {
      let baseURL = 'http://localhost:8000';
      const { VUE_APP_API } = process.env;
      if (VUE_APP_API) {
        baseURL = `https://${VUE_APP_API}`;
      }
      return `${baseURL}/schema/redoc`;
    },
    isSmAndDown() {
      return this.$vuetify.breakpoint.smAndDown;
    },
    hasOpacity() {
      return ['game', 'session'].includes(this.$route.name);
    },
  },
};
</script>

<style scoped>
.v-footer > .container {
  transition: opacity .5s ease-out;
  -moz-transition: opacity .5s ease-out;
  -webkit-transition: opacity .5s ease-out;
  -o-transition: opacity .5s ease-out;
}

.v-footer > .container.transparent {
  opacity: 0.25;
}

.v-footer .container:hover {
  opacity: 1;
}
</style>
