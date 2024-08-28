<template>
  <CardBase
    theme="light"
    @close="close"
  >
    <v-row
      align="center"
      justify="center"
    >
      <v-col
        v-if="icon"
        cols="auto"
      >
        <v-icon
          color="primary"
          size="large"
        >
          {{ icon }}
        </v-icon>
      </v-col>

      <v-col>
        <p class="text-body-2 text-grey-darken-1">
          {{ text }}
        </p>
      </v-col>
    </v-row>

    <template #actions>
      <v-row>
        <v-col cols="6">
          <template v-if="$slots.button">
            <slot name="button" />
          </template>
          <template v-else>
            <v-btn
              v-if="props.page"
              tabindex="0"
              class="bg-primary"
              rounded
              block
              @click="goTo(props.page, openInNewTab = true); close();"
            >
              {{ $t("field.okay") }}
            </v-btn>
            <v-btn
              v-else
              tabindex="0"
              class="bg-primary"
              rounded
              block
              @click="close"
            >
              {{ $t("field.okay") }}
            </v-btn>
          </template>
        </v-col>

        <v-col cols="6">
          <v-btn
            tabindex="0"
            rounded
            block
            @click="close"
          >
            {{ $t("field.abort") }}
          </v-btn>
        </v-col>
      </v-row>
    </template>
  </CardBase>
</template>

<script setup>
import goTo from '@/composables/useGoTo'
import CardBase from '@/components/utils/CardBase.vue'

const props = defineProps({
  text: {
    type: String,
    default: null
  },
  icon: {
    type: String,
    required: false,
    default: null
  },
  page: {
    type: String,
    required: false,
    default: null
  }
})

const emit = defineEmits(['close'])
function close() {
  emit('close')
}
</script>
