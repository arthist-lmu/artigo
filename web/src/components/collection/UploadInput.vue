<template>
  <div class="v-drop-input">
    <div
      class="container pa-0"
      @dragover="onDragover"
      @dragleave="onDragleave"
      @drop="onDrop"
    >
      <label for="input">
        <input
          class="hidden-input"
          @change="onChange"
          id="input"
          type="file"
          name="input"
          ref="input"
          accept=".zip,.tar,.tar.gz,.tar.bz2,.tar.xz,.csv,.json,.jsonl,.gif,.png,.jpg,.jpeg"
          multiple
        />

        <div class="pa-6">
          <v-icon
            class="mb-4"
            color="primary"
            x-large
          >
            mdi-cloud-upload-outline
          </v-icon>

          <div>{{ $t("user.upload.fields.drag-file") }}</div>

          <v-btn
            @click="$refs.input.click();"
            class="mt-2"
            color="primary"
            outlined
            rounded
          >
            {{ $t("user.upload.fields.browse-file") }}
          </v-btn>
        </div>
      </label>

      <v-data-table
        v-if="files && files.length"
        class="mt-4"
        :headers="fileHeaders"
        :items="fileItems"
        style="background-color: transparent;"
        hide-default-header
        hide-default-footer
      >
        <template v-slot:[`item.extension`]="{ item }">
          <v-icon small>
            <template v-if="endsWith(item.name, ['.zip', '.tar', '.tar.gz', '.tar.bz2', '.tar.xz', '.gif', '.png', '.jpg', '.jpeg'])">
              mdi-file-image-outline
            </template>
            <template v-else>
              mdi-file-delimited-outline
            </template>
          </v-icon>
        </template>

        <template v-slot:[`item.actions`]="{ item }">
          <v-icon
            @click="removeFileItem(item)"
            small
          >
            mdi-close-circle-outline
          </v-icon>
        </template>
      </v-data-table>
    </div>

    <VMessages
      v-if="files && errorBucket.length"
      class="pt-1 px-3"
      style="width: 100%;"
      :value="errorBucket"
      color="error"
    />
  </div>
</template>

<script>
import VInput from 'vuetify/lib/components/VInput/VInput';

export default {
  extends: VInput,
  props: {
    value: {
      type: [Array, FileList],
      required: false,
    },
  },
  data() {
    return {
      files: null,
      isDragging: false,
      fileHeaders: [
        { text: '', value: 'extension' },
        { text: '', value: 'name' },
        { text: '', value: 'actions', align: 'end' },
      ],
    };
  },
  methods: {
    onChange() {
      if (!this.isArray(this.files)) {
        this.files = [...this.$refs.input.files];
      } else {
        this.files.push(...this.$refs.input.files);
      }
      this.$emit('input', this.files);
    },
    onDragover(evt) {
      evt.preventDefault();
      this.isDragging = true;
    },
    onDragleave() {
      this.isDragging = false;
    },
    onDrop(evt) {
      evt.preventDefault();
      this.$refs.input.files = evt.dataTransfer.files;
      this.onChange();
      this.isDragging = false;
    },
    removeFileItem(item) {
      const index = this.fileItems.indexOf(item);
      this.files.splice(index, 1);
    },
  },
  computed: {
    fileItems() {
      return this.files.map(({ name }) => ({ name }));
    },
  },
  watch: {
    value: {
      handler(value) {
        if (value) {
          this.files = value;
        }
      },
      deep: true,
    },
  },
};
</script>

<style scoped>
.v-drop-input {
  justify-content: center;
  flex-direction: column;
  align-items: center;
  text-align: center;
  display: flex;
  flex-grow: 1;
}

.v-drop-input > div:first-child {
  border: 1px dotted #e2e8f0;
  border-radius: 28px;
  border-width: 2px;
  min-height: 100px;
  overflow: hidden;
}

.hidden-input {
  position: absolute;
  overflow: hidden;
  opacity: 0;
  height: 0;
  width: 0;
}

label {
  cursor: pointer;
}
</style>
