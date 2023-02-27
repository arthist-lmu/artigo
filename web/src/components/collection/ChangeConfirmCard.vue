<template>
  <Card
    v-bind="$props"
    v-on="$listeners"
    :title="$t('collections.fields.change')"
  >
    <p class="pb-4">{{ $t('user.upload.note-access') }}</p>

    <v-form
      v-model="isFormValid"
      @submit.prevent="change"
    >
      <v-text-field
        v-model="params.title.de"
        :placeholder="$t('user.upload.fields.name')"
        :rules="[checkLength]"
        class="mb-1"
        tabindex="0"
        counter="75"
        clearable
        outlined
        rounded
        dense
      >
        <template v-slot:append>
          <span>DE</span>
        </template>
      </v-text-field>

      <v-text-field
        v-model="params.title.en"
        :placeholder="$t('user.upload.fields.name')"
        :rules="[checkLength]"
        class="mb-1"
        tabindex="0"
        counter="75"
        clearable
        outlined
        rounded
        dense
      >
        <template v-slot:append>
          <span>EN</span>
        </template>
      </v-text-field>

      <v-select
        v-model="params.access"
        :placeholder="$t('user.upload.fields.access')"
        :items="items.access"
        item-text="name"
        item-value="value"
        hide-details
        outlined
        rounded
        dense
      />
    </v-form>

    <template v-slot:actions>
      <v-row>
        <v-col>
          <v-btn
            @click="change"
            :disabled="!isFormValid"
            type="submit"
            tabindex="0"
            color="primary"
            depressed
            rounded
            block
          >
            {{ $t("collections.fields.change") }}
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
    entry: Object,
    ...Card.props,
  },
  data() {
    return {
      params: {
        title: {
          de: this.entry.title.de,
          en: this.entry.title.en,
        },
        access: this.entry.access,
      },
      isFormValid: false,
    };
  },
  methods: {
    change() {
      if (this.isFormValid) {
        const entry = { hash_id: this.entry.hash_id, ...this.params };
        this.$store.dispatch('collection/change', entry);
      }
    },
    checkLength(value) {
      if (value) {
        if (value.length < 4) {
          return this.$tc('rules.min', 4);
        }
        if (value.length > 75) {
          return this.$tc('rules.max', 75);
        }
        return true;
      }
      return true;
    },
  },
  computed: {
    items() {
      return {
        access: [
          {
            name: this.$t('collections.fields.access-open'),
            value: 'O',
          },
          {
            name: this.$t('collections.fields.access-restricted'),
            value: 'R',
          },
        ],
      };
    },
  },
  watch: {
    value(visible) {
      if (!visible) {
        this.$store.dispatch('collections/post', {});
      }
    },
    timestamp() {
      if (this.isFormValid && this.status) {
        if (this.isDialog) {
          this.close();
        }
      }
    },
  },
  components: {
    Card,
  },
};
</script>
