<template>
  <v-dialog v-model="dialog" max-width="350px">
    <template v-slot:activator="{ on }">
      <v-btn v-on="on" class="login" text block large>
        {{ $t('user.login.title') }}
      </v-btn>
    </template>

    <v-card class="login">
      <v-card-title>
        {{ $t('user.login.title') }}

        <v-btn icon @click="dialog = false" absolute right>
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>

      <v-card-text>
        <v-text-field
          v-model="user.name"
          :placeholder="$t('user.name')"
          :rules="[checkLength]"
          prepend-icon="mdi-account"
          counter="50"
          clearable
        ></v-text-field>

        <v-text-field
          v-model="user.password"
          @click:append="showPassword = !showPassword"
          :type="showPassword ? 'text' : 'password'"
          :placeholder="$t('user.password')"
          :rules="[checkLength]"
          :append-icon="
            showPassword ? 'mdi-eye-outline' :
            'mdi-eye-off-outline'
          "
          prepend-icon="mdi-lock"
          counter="50"
          clearable
        ></v-text-field>
      </v-card-text>

      <v-card-actions class="px-6 pt-2">
        <v-btn
          @click="login"
          :disabled="disabled"
          color="accent"
          depressed
          rounded
          block
        >
          {{ $t('user.login.title') }}
        </v-btn>
      </v-card-actions>

      <div class="grey--text px-6 pb-6" style="text-align: center">
        {{ $t('user.login.text') }} <UserRegister @close="dialog = false" />.
      </div>
    </v-card>
  </v-dialog>
</template>

<script>
import UserRegister from '@/components/UserRegister.vue';

export default {
  data() {
    return {
      showPassword: false,
      dialog: false,
      user: {},
    };
  },
  methods: {
    login() {
      this.$store.dispatch('user/login', this.user);
      this.dialog = false;
    },
    checkLength(value) {
      if (value) {
        if (value.length < 5) {
          return this.$t('user.login.rules.min');
        }
        if (value.length > 50) {
          return this.$t('user.login.rules.max');
        }
        return true;
      }
      return this.$t('field.required');
    },
  },
  computed: {
    disabled() {
      if (Object.keys(this.user).length) {
        const total = Object.values(this.user).reduce(
          (t, value) => t + (this.checkLength(value) === true),
          0,
        );
        if (total === 2) return false;
      }
      return true;
    },
  },
  watch: {
    dialog(value) {
      if (value) {
        this.$emit('close');
      }
    },
  },
  components: {
    UserRegister,
  },
};
</script>

<style>
.v-card.login .v-btn.register {
  min-width: auto !important;
  text-transform: capitalize;
  display: inline-block;
  letter-spacing: 0;
  font-size: 1rem;
  padding: 0 2px;
  height: 20px;
}

.v-card.login .v-btn.register:before,
.v-card.login .v-btn.register:hover:before,
.v-card.login .v-btn.register:focus:before {
  background-color: transparent;
}
</style>
