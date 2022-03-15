<template>
  <v-card
    max-width="450"
    flat
  >
    <v-card-title v-if="isDialog">
      {{ $t("user.login.title") }}

      <v-btn
        @click="close"
        absolute
        right
        icon
      >
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </v-card-title>

    <v-card-text :class="isDialog ? '' : 'pt-0 px-0'">
      <v-form v-model="isFormValid">
        <v-text-field
          v-model="user.username"
          :placeholder="$t('user.fields.username')"
          :rules="[checkLength]"
          prepend-icon="mdi-account"
          tabindex="1"
          counter="75"
          clearable
        />

        <v-text-field
          v-model="user.email"
          :placeholder="$t('user.fields.email')"
          :rules="[checkLength]"
          prepend-icon="mdi-email"
          tabindex="2"
          counter="75"
          clearable
        />

        <v-text-field
          v-model="user.password"
          @click:append="showPassword = !showPassword"
          :type="showPassword ? 'text' : 'password'"
          :placeholder="$t('user.fields.password')"
          :rules="[checkLength]"
          :append-icon="
            showPassword ? 'mdi-eye-outline' : 'mdi-eye-off-outline'
          "
          prepend-icon="mdi-lock"
          tabindex="3"
          counter="75"
          clearable
        />
      </v-form>
    </v-card-text>

    <v-card-actions :class="isDialog ? 'pt-0 pb-6 px-6' : 'pb-8 px-0'">
      <v-btn
        @click="login"
        :disabled="!isFormValid"
        tabindex="4"
        color="accent"
        depressed
        rounded
        block
      >
        {{ $t("user.login.title") }}
      </v-btn>

      <div
        class="grey--text pt-2"
        style="text-align: center"
      >
        {{ $t("user.login.text") }}

        <v-dialog
          v-model="dialog.register"
          max-width="400"
        >
          <template v-slot:activator="{ on }">
            <v-btn
              v-on="on"
              small
              text
            >
              {{ $t("user.register.title") }}
            </v-btn>
          </template>

          <RegisterCard
            v-model="dialog.register"
            :isDialog="true"
          />
        </v-dialog>
      </div>
    </v-card-actions>
  </v-card>
</template>

<script>
import RegisterCard from '@/components/RegisterCard.vue';

export default {
  props: {
    isDialog: Boolean,
    value: Boolean,
  },
  data() {
    return {
      showPassword: false,
      isFormValid: false,
      dialog: {
        register: false,
      },
      user: {},
    };
  },
  methods: {
    login() {
      this.$store.dispatch('user/login', this.user);
      // TODO: go to user-specific page if successful?
    },
    close() {
      this.$emit('input', false);
    },
    checkLength(value) {
      if (value) {
        if (value.length < 4) {
          return this.$tc('user.login.rules.min', 4);
        }
        if (value.length > 75) {
          return this.$tc('user.login.rules.max', 75);
        }
        return true;
      }
      return this.$t('field.required');
    },
  },
  computed: {
    status() {
      const { error, loading } = this.$store.state.utils.status;
      return !loading && !error;
    },
    timestamp() {
      return this.$store.state.utils.status.timestamp;
    },
  },
  watch: {
    'dialog.register'(value) {
      if (value) {
        this.close();
      }
    },
    timestamp() {
      if (this.status) {
        this.close();
      }
    },
  },
  components: {
    RegisterCard,
  },
};
</script>

<style scoped>
.v-card__actions {
  display: block;
}
</style>
