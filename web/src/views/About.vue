<template>
  <v-container>
    <GameDrawer />

    <v-row>
      <v-col class="pa-12">
        <div class="text-h2 accent--text mb-6">
          {{ $t("contributors.title") }}
        </div>

        <Contributors />
      </v-col>
    </v-row>

    <v-row>
      <v-col class="pa-12">
        <div class="text-h2 accent--text mb-6">
          {{ $t("publications.title") }}
        </div>

        <Publications />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data() {
    return {

    };
  },
  computed: {

  },
  components: {
    GameDrawer: () => import('@/components/game/Drawer.vue'),
    Contributors: () => import('@/components/Contributors.vue'),
    Publications: () => import('@/components/Publications.vue'),
  },
};
</script>
