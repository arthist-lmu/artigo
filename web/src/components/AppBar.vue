<template>
  <v-app-bar app flat>
    <v-layout
      justify-end
      row
    >
      <UserMenu />
    </v-layout>
  </v-app-bar>
</template>

<script>
import UserMenu from '@/components/UserMenu.vue';

export default {
  components: {
    UserMenu,
  },
};
</script>
