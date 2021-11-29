<template>
  <v-menu
    v-model="menu"
    min-width="175"
    open-on-hover
    offset-y
    bottom
    left
  >
    <template v-slot:activator="{ attrs, on: menu }">
      <v-btn
        v-bind="attrs"
        v-on="menu"
        :title="$t('user.menu.title')"
        class="ml-n2"
        icon
      >
        <v-badge
          v-if="loggedIn"
          color="accent"
          dot
        >
          <v-icon color="primary">mdi-account-circle</v-icon>
        </v-badge>
        <v-icon
          v-else
          color="primary"
        >
          mdi-account-circle
        </v-icon>
      </v-btn>
    </template>

    <UserAccount v-if="loggedIn" />

    <v-list v-if="!loggedIn" class="pa-0">
      <v-list-item-group>
        <v-list-item class="px-0">
          <UserLogin @close="menu = false" />
        </v-list-item>
        <v-list-item class="px-0">
          <UserRegister @close="menu = false" />
        </v-list-item>
      </v-list-item-group>
    </v-list>
  </v-menu>
</template>

<script>
import UserLogin from '@/components/UserLogin.vue';
import UserAccount from '@/components/UserAccount.vue';
import UserRegister from '@/components/UserRegister.vue';

export default {
  data() {
    return {
      menu: false,
    };
  },
  computed: {
    loggedIn() {
      return this.$store.state.user.loggedIn;
    },
  },
  components: {
    UserLogin,
    UserAccount,
    UserRegister,
  },
};
</script>

<style>
.v-menu__content .v-btn:not(.accent) {
  text-transform: capitalize;
  justify-content: left;
}

.v-btn:not(.v-btn--round).v-size--large {
  height: 48px;
}
</style>
