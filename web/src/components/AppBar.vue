<template>
  <v-app-bar 
    app 
    flat
  >
  <v-spacer></v-spacer>
    <UserMenu />
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
