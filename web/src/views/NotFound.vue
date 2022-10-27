<template>
  <v-container class="text-center fill-height">
    <v-row align="center">
      <v-col class="pa-0">
        <div :class="[$vuetify.breakpoint.mdAndDown ? 'text-h3' : 'text-h2', 'mb-4']">
          {{ $t('not-found.title') }}
        </div>

        <p class="mx-8">
          {{ $t('not-found.fields.not-exist') }}
        </p>

        <v-btn
          @click="reset"
          color="grey lighten-2"
          outlined
          rounded
        >
          {{ $t('not-found.fields.go-home') }}
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  methods: {
    reset() {
      this.$router.push({ name: 'home' });
    },
    handleReset(evt) {
      if (evt.keyCode === 13) {
        reset();
      }
    },
  },
};
</script>
