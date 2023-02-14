<template>
  <Card
    v-bind="$props"
    v-on="$listeners"
    :title="$t('collections.fields.change')"
  >
    <v-form v-model="isFormValid">
      <v-text-field
        v-model="params.name"
        :placeholder="$t('user.upload.fields.name')"
        :rules="[checkLength]"
        tabindex="0"
        counter="75"
        clearable
        outlined
        rounded
        dense
      />

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
        name: this.entry.name,
        access: this.entry.access,
      },
      isFormValid: false,
    };
  },
  methods: {
    change() {
      const entry = { hash_id: this.entry.hash_id, ...this.params };
      this.$store.dispatch('collection/change', entry).then(() => {
        this.$store.dispatch('collections/post', {});
        this.close();
      });
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
  components: {
    Card,
  },
};
</script>
