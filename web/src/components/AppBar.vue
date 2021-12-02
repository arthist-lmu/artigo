<template>
  <v-app-bar 
    app 
    flat
  >

    <v-layout
      right
    >
      <UserMenu />
    </v-layout>
  </v-app-bar>
</template>

<script>
import UserMenu from '@/components/UserMenu.vue';

export default {
  data: () => ({ drawer: null }),
  components: {
    UserMenu,
  },
};
</script>
