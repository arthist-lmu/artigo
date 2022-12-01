<template>
  <v-app
    id="app"
    :class="{ 'dark-variant': dark }"
  >
    <Loader />
    <Toaster />

    <v-main class="mx-6 mb-6">
      <v-container class="fill-height">
        <v-row>
          <v-col cols="6">
            <v-container class="fill-height">
              <v-row
                align="center"
                no-gutters
              >
                <Logo :dark="dark" />
              </v-row>
            </v-container>
          </v-col>

          <v-col cols="6">
            <slot />
          </v-col>
        </v-row>
      </v-container>
    </v-main>

    <Footer :dark="dark" />
  </v-app>
</template>

<script>
export default {
  props: {
    dark: {
      type: Boolean,
      default: false,
    },
  },
  components: {
    Logo: () => import('@/components/Logo.vue'),
    Loader: () => import('@/components/Loader.vue'),
    Toaster: () => import('@/components/Toaster.vue'),
    Footer: () => import('@/components/Footer.vue'),
  },
};
</script>

<style scoped>
.theme--light.dark-variant.v-application {
  background-color: rgb(66, 71, 152) !important;
}
</style>
