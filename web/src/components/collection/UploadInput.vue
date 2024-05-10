<template>
  <div
    @drop.prevent="addDropFile"
    @dragover.prevent
  >
    <v-file-input
      v-model="files"
      class="upload"
      :rules="rules"
      :clearable="false"
      accept=".zip,.tar,.tar.gz,.tar.bz2,.tar.xz,.csv,.json,.jsonl,.gif,.png,.jpg,.jpeg"
      prepend-icon=""
      variant="plain"
      hide-details
      multiple
    >
      <template #prepend-inner>
        <div>
          <v-icon
            color="primary"
            size="x-large"
          >
            mdi-cloud-upload-outline
          </v-icon>

          <div class="mt-4">
            {{ $t("user.upload.fields.dragFile") }}
          </div>

          <v-btn
            class="mt-2"
            color="primary"
            variant="outlined"
            rounded
          >
            {{ $t("user.upload.fields.browseFile") }}
          </v-btn>
        </div>
      </template>

      <template #selection>
        <v-data-table
          v-if="files && files.length"
          :headers="fileHeaders"
          :items="files"
        >
          <template #[`item.extension`]="{ item }">
            <v-icon
              variant="text"
              size="small"
            >
              <template v-if="endsWith(item.name, ['.zip', '.tar', '.tar.gz', '.tar.bz2', '.tar.xz', '.gif', '.png', '.jpg', '.jpeg'])">
                mdi-file-image-outline
              </template>
              <template v-else>
                mdi-file-delimited-outline
              </template>
            </v-icon>
          </template>

          <template #[`item.actions`]="{ item }">
            <v-btn
              variant="text"
              density="comfortable"
              icon="mdi-close-circle-outline"
              size="small"
              @click.stop="removeFileByName(item.name)"
            />
          </template>

          <template #bottom />
        </v-data-table>
      </template>

      <template #message="{ message }">
        {{ message }}
      </template>
    </v-file-input>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import endsWith from '@/composables/useEndsWith'

const props = defineProps({
  modelValue: {
    type: Array,
    default: null
  },
  rules: {
    type: Array,
    default: null
  }
})

const files = ref({
  type: Array,
  default: []
})

const fileHeaders = [
  { text: '', value: 'extension' },
  { text: '', value: 'name', width: '100%' },
  { text: '', value: 'actions', align: 'end' }
]

function addDropFile(e) {
  if (e.dataTransfer.files.length) {
    if (files.value && files.value.length) {
      files.value.push(e.dataTransfer.files[0])
    } else {
      files.value = [e.dataTransfer.files[0]]
    }
  }
}
const fileNames = computed(() => files.value.map(({ name }) => name))
function removeFileByName(name) {
  const index = fileNames.value.indexOf(name)
  files.value.splice(index, 1)
}

const emit = defineEmits(['update:modelValue'])
watch(() => props.modelValue, (value) => {
  files.value = value
}, { immediate: true })
watch(files, (value) => emit('update:modelValue', value))
</script>

<style>
.v-input.upload {
  border: 1px dotted #e2e8f0;
  border-radius: 28px;
  border-width: 2px;
  cursor: pointer;
}

.v-input.upload .v-field {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.v-input.upload .v-field__prepend-inner {
  padding: 32px;
}

.v-input.upload .v-field__field {
  width: 100%;
}

.v-input.upload .v-table {
  background-color: transparent;
}

.v-input.upload .v-field__field input,
.v-input.upload .v-field__field thead,
.v-input.upload .v-field__field > div:empty {
  display: none;
}

.v-input.upload .v-field__input {
  padding: 0;
}
</style>
