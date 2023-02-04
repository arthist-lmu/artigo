<template>
  <v-card
    max-width="900"
    flat
  >
    <v-card-title :class="{ 'pt-6 px-6': !isDialog }">
      {{ $t("user.upload.title") }}

      <v-btn
        v-if="isDialog"
        @click="close"
        absolute
        right
        icon
      >
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </v-card-title>

    <v-card-text :class="[isDialog ? undefined : 'px-6', 'pt-4']">
      <v-form v-model="isFormValid">
        <v-text-field
          v-model="collection.name"
          :placeholder="$t('collection.fields.name')"
          :rules="[checkLength]"
          class="mb-1"
          tabindex="0"
          counter="75"
          clearable
          outlined
          rounded
          dense
        />

        <DropFileInput
          v-model="collection.files"
          :rules="[checkFiles]"
        />
      </v-form>
    </v-card-text>

    <v-card-actions
      class="pb-6 px-6"
      style="display: block;"
    >
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
    </v-card-actions>

    <v-dialog
      v-model="dialog.collectionList"
      max-width="900"
    >
      <CollectionListCard v-model="dialog.collectionList" />
    </v-dialog>
  </v-card>
</template>

<script>
export default {
  props: {
    isDialog: {
      type: Boolean,
      default: true,
    },
    value: Boolean,
  },
  data() {
    return {
      collection: {},
      isFormValid: false,
      dialog: {
        collectionList: false,
      },
    };
  },
  methods: {
    upload() {
      this.$store.dispatch('collection/add', this.collection);
    },
    close() {
      this.$emit('input', false);
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
        this.dialog.collectionList = true;
      }
    },
  },
  components: {
    DropFileInput: () => import('@/components/account/DropFileInput.vue'),
    CollectionListCard: () => import('@/components/account/CollectionListCard.vue'),
  },
};
</script>
