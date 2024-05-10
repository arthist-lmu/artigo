<template>
  <span v-if="!isUserAnonymous">
    <v-btn
      v-if="field"
      :title="$t('reconcile.title')"
      variant="plain"
      density="comfortable"
      icon="mdi-wiper"
      size="small"
      @click="reconcile(field)"
    />
    <v-menu
      v-else
      open-on-hover
    >
      <template #activator="{ props: activatorProps }">
        <v-btn
          v-bind="activatorProps"
          :title="$t('reconcile.title')"
          class="ml-1 mr-n2"
          variant="plain"
          density="comfortable"
          icon="mdi-wiper"
          size="small"
        />
      </template>

      <v-list>
        <v-list-item @click="reconcile('resource')">
          <v-list-item-title>
            {{ $t('reconcile.fields.resource') }}
          </v-list-item-title>
        </v-list-item>

        <v-list-item @click="reconcile('creator')">
          <v-list-item-title>
            {{ $t('reconcile.fields.creator') }}
          </v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </span>
</template>

<script setup>
import { computed } from 'vue'
import { useStore } from 'vuex'
import getTitle from '@/composables/useGetTitle'
import getCreators from '@/composables/useGetCreators'

const store = useStore()

const props = defineProps({
  items: {
    type: Array,
    default: null
  },
  field: {
    type: String,
    default: null
  }
})

function reconcile(field) {
  const queries = []
  props.items.forEach((item) => {
    switch (field) {
      case 'creator':
        queries.push({
          id: item.id,
          name: getCreators(item)[0],
          type: field
        })
        break
      case 'resource':
        queries.push({
          id: item.id,
          name: getTitle(item),
          type: field
        })
        break
      default:
        break
    }
  })
  store.dispatch('reconcile/post', { queries })
}

const isUserAnonymous = computed(() => store.state.user.isAnonymous)
</script>
