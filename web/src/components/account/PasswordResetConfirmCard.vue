<template>
  <Card
    v-bind="$props"
    v-on="$listeners"
    :title="$t('user.password-reset.title')"
  >
    <v-form v-model="isFormValid">
      <v-text-field
        v-model="user.new_password1"
        @click:append="showPassword = !showPassword"
        :type="showPassword ? 'text' : 'password'"
        :placeholder="$t('user.fields.password')"
        :rules="[checkLength]"
        :append-icon="
          showPassword ? 'mdi-eye-outline' : 'mdi-eye-off-outline'
        "
        tabindex="0"
        counter="75"
        clearable
        outlined
        rounded
        dense
      />

      <v-text-field
        v-model="user.new_password2"
        @click:append="showPassword = !showPassword"
        :type="showPassword ? 'text' : 'password'"
        :placeholder="$t('user.fields.password-repeat')"
        :rules="[checkLength, checkPasswordRepeat]"
        :append-icon="
          showPassword ? 'mdi-eye-outline' : 'mdi-eye-off-outline'
        "
        tabindex="0"
        counter="75"
        clearable
        outlined
        rounded
        dense
      />
      </v-form>

    <template v-slot:actions>
      <v-row>
        <v-col>
          <v-btn
            @click="resetPassword"
            :disabled="!isFormValid"
            tabindex="0"
            color="primary"
            depressed
            rounded
            block
          >
            {{ $t("user.password-reset.title") }}
          </v-btn>
        </v-col>
      </v-row>
    </template>
  </Card>
</template>

<script>
import Card from '@/components/utils/Card.vue';

export default {
  extends: Card,
  props: {
    ...Card.props,
  },
  data() {
    return {
      user: {},
      isFormValid: false,
      showPassword: false,
    };
  },
  methods: {
    resetPassword() {
      this.$store.dispatch('user/resetPasswordConfirm', this.user);
    },
    close() {
      this.$emit('input', false);
    },
    checkLength(value) {
      if (value) {
        if (value.length < 5) {
          return this.$tc('rules.min', 5);
        }
        if (value.length > 75) {
          return this.$tc('rules.max', 75);
        }
        return true;
      }
      return this.$t('field.required');
    },
    checkPasswordRepeat(value) {
      if (value && value === this.user.new_password1) {
        return true;
      }
      return this.$t('rules.password-repeat');
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
    timestamp() {
      if (this.isFormValid && this.status) {
        if (this.isDialog) {
          this.close();
        } else {
          this.$router.push({ name: 'home' });
        }
      }
    },
  },
  created() {
    let path = this.$route.path.split('/');
    path = path.filter((item) => item);
    this.user = {
      uid: path[path.length - 2],
      token: path[path.length - 1],
    };
  },
  components: {
    Card,
  },
};
</script>
