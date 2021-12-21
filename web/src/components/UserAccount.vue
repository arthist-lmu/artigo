<template>
  <v-list class="account">
    <v-list-item>
      <v-list-item-content class="justify-center pa-10">
        <div class="mx-auto text-center">
          <v-avatar color="secondary">
            <span class="white--text text-h5">{{ initials }}</span>
          </v-avatar>

          <h3 class="mt-5">{{ data.username }}</h3>

          <p class="text-caption clip mt-2 mb-0" style="max-width: 170px">
            {{ data.email }}
          </p>

          <p class="text-caption mb-0">
            <i>{{ joined }}</i>
          </p>
        </div>

        <div class="v-btn--absolute v-btn--right v-btn--top">
          <v-btn
            @click="logout"
            :title="$t('user.logout.title')"
            class="mr-n2 mt-n3"
            icon
          >
            <v-icon>mdi-logout-variant</v-icon>
          </v-btn>
        </div>
      </v-list-item-content>
    </v-list-item>
  </v-list>
</template>

<script>
export default {
  methods: {
    logout() {
      this.$store.dispatch("user/logout");
    },
  },
  computed: {
    data() {
      return this.$store.state.user.data;
    },
    nDays() {
      const diff = new Date() - new Date(this.data.date_joined);
      return Math.round(diff / (1000 * 60 * 60 * 24));
    },
    joined() {
      return this.$tc("user.menu.joined", this.nDays);
    },
    initials() {
      return "test";
      // return this.data.username.slice(0, 2);
    },
  },
};
</script>

<style>
.account .v-list-item__content {
  letter-spacing: 0.0892857143em;
}

.account .v-btn:not(.accent) {
  justify-content: center !important;
}
</style>
