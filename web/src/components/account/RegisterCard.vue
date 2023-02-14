<template>
  <Card
    v-bind="$props"
    v-on="$listeners"
    :title="$t('user.register.title')"
  >
    <v-form v-model="isFormValid">
      <v-text-field
        v-model="user.username"
        :placeholder="$t('user.fields.username')"
        :rules="[checkLength]"
        tabindex="0"
        counter="75"
        clearable
        outlined
        rounded
        dense
      />

      <v-text-field
        v-model="user.email"
        :placeholder="$t('user.fields.email')"
        :rules="[checkLength]"
        tabindex="0"
        counter="75"
        clearable
        outlined
        rounded
        dense
      />

      <v-text-field
        v-model="user.password1"
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
        v-model="user.password2"
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

      <v-checkbox
        v-model="user.privacy_policy"
        :rules="[checkTrue]"
        class="mt-0"
        on-icon="mdi-check-circle-outline"
        off-icon="mdi-checkbox-blank-circle-outline"
        tabindex="0"
        color="primary"
        hide-details
        dense
      >
        <template v-slot:label>
          {{ $t('user.fields.privacy-policy') }}

          <v-btn
            @click.stop
            class="ml-1"
            href="https://www.kunstgeschichte.uni-muenchen.de/funktionen/datenschutz/index.html"
            target="_blank"
            small
            icon
          >
            <v-icon>
              mdi-link-variant
            </v-icon>
          </v-btn>
        </template>
      </v-checkbox>
    </v-form>

    <template v-slot:actions>
      <v-row>
        <v-col>
          <v-btn
            @click="register"
            :disabled="!isFormValid"
            tabindex="0"
            color="primary"
            depressed
            rounded
            block
          >
            {{ $t("user.register.title") }}
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
    register() {
      this.$store.dispatch('user/register', this.user);
    },
    checkTrue(value) {
      if (value) {
        return true;
      }
      return this.$t('field.required');
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
      if (value && value === this.user.password1) {
        return true;
      }
      return this.$t('rules.password-repeat');
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
  components: {
    Card,
  },
};
</script>
