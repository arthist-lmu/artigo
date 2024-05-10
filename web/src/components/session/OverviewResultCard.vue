<template>
  <v-hover
    v-if="!isDisabled"
    v-slot="{ isHovering, props: activatorProps }"
  >
    <v-card
      v-bind="activatorProps"
      :class="{ opaque: opaque }"
      :disabled="isDisabled ? true : undefined"
      class="bg-surface-variant text-primary-darken-1"
      flat
    >
      <v-img
        :src="item.path"
        alt=""
        style="cursor: pointer;"
        class="bg-grey-lighten-2"
        :height="height"
        contain
        @error="onError"
        @load="onLoad"
        @click="showDialog"
        @key-down="showDialog"
      >
        <template #placeholder>
          <v-row
            class="fill-height ma-0"
            justify="center"
            align="center"
          >
            <v-progress-circular indeterminate />
          </v-row>
        </template>

        <v-btn
          style="bottom: 0; right: 0;"
          class="ma-4"
          color="primary"
          position="absolute"
          rounded
          flat
        >
          <v-icon class="mr-2">
            mdi-tag-outline
          </v-icon>

          {{ tags.length }}
        </v-btn>

        <v-fade-transition>
          <div v-if="isLoaded && isHovering">
            <div class="pa-4">
              <TagCloud :tags="tags" />
            </div>
          </div>
        </v-fade-transition>
      </v-img>

      <v-card-title
        class="text-subtitle-1 pb-0"
        :title="title"
      >
        {{ title }}
      </v-card-title>

      <v-card-subtitle class="pb-4">
        <span
          v-for="creator in creators"
          :key="creator"
          :title="creator"
        >
          {{ creator }}
        </span>
      </v-card-subtitle>
    </v-card>
  </v-hover>
</template>

<script setup>
import useResource from '@/composables/useResource'
import TagCloud from '@/components/TagCloud.vue'

const props = defineProps({
  item: {
    type: Object,
    default: null,
    required: true
  },
  opaque: {
    type: Boolean,
    default: false
  },
  height: {
    type: String,
    default: '225'
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
</script>

<style scoped>
.v-card {
  transition: opacity 0.25s linear;
}

.opaque {
  opacity: 0.5;
}
</style>
