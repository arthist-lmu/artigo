<template>
  <v-dialog v-model="dialog" max-width="350px">
    <template v-slot:activator="{ on }">
      <v-btn v-on="on" class="register" text block large>
        {{ $t('user.register.title') }}
      </v-btn>
    </template>

    <v-card class="register">
      <v-card-title>
        {{ $t('user.register.title') }}

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
          v-model="user.email"
          :placeholder="$t('user.email')"
          :rules="[checkLength]"
          prepend-icon="mdi-email"
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

      <v-card-actions class="px-6 pb-6">
        <v-btn
          @click="register"
          :disabled="disabled"
          color="accent"
          depressed
          rounded
          block
        >
          {{ $t('user.register.title') }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  data() {
    return {
      showPassword: false,
      dialog: false,
      user: {},
    };
  },
  methods: {
    register() {
      this.$store.dispatch('user/register', this.user);
      this.dialog = false;
    },
    checkLength(value) {
      if (value) {
        if (value.length < 5) {
          return this.$t('user.register.rules.min');
        }
        if (value.length > 50) {
          return this.$t('user.register.rules.max');
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
          0
        );
        if (total === 3) return false;
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
};
</script>
