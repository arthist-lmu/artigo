<template>
  <Card
    v-bind="$props"
    v-on="$listeners"
    :title="$t('user.password-reset.title')"
  >
    <p class="pb-4">{{ $t('user.password-reset.note') }}</p>

    <v-form
      v-model="isFormValid"
      @submit.prevent="resetPassword"
    >
      <v-text-field
        v-model="user.email"
        @keydown.enter="resetPassword"
        :placeholder="$t('user.fields.email')"
        :rules="[checkLength]"
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
            type="submit"
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
    };
  },
  methods: {
    resetPassword() {
      if (this.isFormValid) {
        this.user.lang = this.$i18n.locale; // fix locale
        this.$store.dispatch('user/resetPassword', this.user);
      }
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
  },
  watch: {
    timestamp() {
      if (this.status) {
        this.close();
      }
    },
  },
  components: {
    Card,
  },
};
</script>
