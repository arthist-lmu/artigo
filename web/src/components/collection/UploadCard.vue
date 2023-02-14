<template>
  <Card
    v-bind="$props"
    v-on="$listeners"
    :title="$t('user.upload.title')"
  >
    <v-form v-model="isFormValid">
      <v-text-field
        v-model="collection.name"
        :placeholder="$t('user.upload.fields.name')"
        :rules="[checkLength]"
        class="mb-1"
        tabindex="0"
        counter="75"
        clearable
        outlined
        rounded
        dense
      />

      <UploadInput
        v-model="collection.files"
        :rules="[checkFiles]"
      />
    </v-form>

    <template v-slot:actions>
      <v-row>
        <v-col>
          <v-btn
            @click="upload"
            :disabled="!isFormValid"
            tabindex="0"
            color="primary"
            depressed
            rounded
            block
          >
            {{ $t("user.upload.title") }}
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
      collection: {},
      isFormValid: false,
    };
  },
  methods: {
    upload() {
      this.$store.dispatch('collection/add', this.collection).then(() => {
        this.$store.dispatch('collections/post', {});
        this.collection = {};
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
      return this.$t('field.required');
    },
    checkFiles(value) {
      if (value && value.length) {
        for (let i = 0; i < value.length; i += 1) {
          if (value[i].size >= (50 * 1024 * 1024)) {
            return this.$tc('rules.file-size', 50);
          }
        }
        return true;
      }
      return this.$t('field.required');
    },
  },
  watch: {
    timestamp() {
      if (this.isFormValid && this.status) {
        this.$router.push({ name: 'collections' });
      }
    },
  },
  components: {
    UploadInput: () => import('@/components/collection/UploadInput.vue'),
    Card,
  },
};
</script>
