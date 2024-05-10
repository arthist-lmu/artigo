<template>
  <v-hover
    v-if="!isDisabled"
    v-slot="{ isHovering, props: activatorProps }"
  >
    <div
      v-bind="activatorProps"
      class="grid-item"
      :disabled="isDisabled ? true : undefined"
      @click="showDialog"
      @key-down="showDialog"
    >
      <img
        :src="item.path"
        alt=""
        @error="onError"
        @load="onLoad"
      >

      <v-fade-transition>
        <v-container
          v-if="isLoaded && (isHovering || isSelected)"
          class="overlay"
        >
          <v-row style="flex: 0;">
            <v-col class="tags pa-4">
              <TagCloud :tags="tags" />
            </v-col>
          </v-row>

          <v-row />

          <v-row style="flex: 0;">
            <v-col class="pa-4">
              <div
                class="text-subtitle-1 white--text"
                :title="title"
              >
                <b>{{ title }}</b>
              </div>

              <div class="text-caption">
                <span
                  v-for="creator in creators"
                  :key="creator"
                  :title="creator"
                >
                  {{ creator }}
                </span>
              </div>
            </v-col>
          </v-row>
        </v-container>
      </v-fade-transition>
    </div>
  </v-hover>
</template>

<script setup>
import { computed, watch } from 'vue'
import useResource from '@/composables/useResource'
import TagCloud from '@/components/TagCloud.vue'

const props = defineProps({
  item: {
    type: Object,
    default: null,
    required: true
  }
})

const {
  isLoaded,
  isDisabled,
  onLoad,
  onError,
  showDialog,
  title,
  creators,
  tags
} = useResource(props.item)

const isSelected = computed(() => Math.random() < 0.15)

const emit = defineEmits(['disabled'])
watch(isDisabled, (value) => {
  if (value) {
    emit('disabled', true)
  }
})
</script>

<style scoped>
.v-container {
  position: absolute;
  flex-direction: column;
  display: flex;
  width: 100%;
  height: 100%;
  bottom: 0;
  left: 0;
}

.v-container .overlay {
  background: linear-gradient(to top, black, #0000 40%);
  transform: translate(-50%, -50%);
  position: absolute;
  object-fit: cover;
  min-width: 100%;
  max-width: 100%;
  color: #fff;
  height: 100%;
  left: 50%;
  top: 50%;
}

.v-container .overlay .v-col:not(.tags) > * {
  text-overflow: ellipsis;
  line-height: 1.25rem;
  white-space: nowrap;
  overflow: hidden;
}

.v-container .overlay span:not(:first-child)::before {
  content: ", ";
}
</style>
