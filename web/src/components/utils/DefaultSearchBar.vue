<template>
  <v-combobox
    ref="input"
    v-model="query['all-text']"
    :hide-no-data="false"
    :placeholder="$t(`${storeName}.fields.query`)"
    menu-icon=""
    :menu-props="{
      'model-value': showMenu,
      'max-height': 400,
      class: 'white'
    }"
    bg-color="white"
    variant="solo"
    hide-details
    rounded
    flat
    @keyup.enter="search"
  >
    <template #prepend-inner>
      <v-icon
        class="mx-2"
        @click="onButton"
      >
        mdi-magnify
      </v-icon>
    </template>

    <template #no-data>
      <v-container
        v-click-outside="onClickOutside"
        class="pa-8"
      >
        <v-row
          v-for="item in items"
          :key="item.key"
          class="mb-2"
        >
          <v-combobox
            v-model="query[item.key]"
            :placeholder="$t(`resource.metadata.fields.${item.key}`)"
            clear-icon="mdi-close"
            append-icon=""
            border="secondary md opacity-100"
            density="comfortable"
            variant="outlined"
            hide-details
            single-line
            clearable
            multiple
            rounded
          >
            <template #selection="{ attrs, item: subitem, selected }">
              <v-chip
                v-bind="attrs"
                :model-value="selected"
                color="primary"
                variant="outlined"
                size="small"
                closable
              >
                {{ subitem.value }}
              </v-chip>
            </template>
          </v-combobox>
        </v-row>

        <v-row>
          <v-col
            class="pa-0 pt-1"
            align="right"
          >
            <v-btn
              color="primary"
              rounded
              flat
              @click="search"
            >
              {{ $t('search.title') }}
            </v-btn>

            <v-btn
              :title="$t('search.fields.reset')"
              class="ml-2"
              density="comfortable"
              variant="text"
              icon="mdi-restore"
              @click="reset"
            />
          </v-col>
        </v-row>
      </v-container>
    </template>

    <template #append-inner>
      <template v-if="filter">
        <v-badge
          v-if="numberOfQueries > 0"
          :content="numberOfQueries"
          color="primary"
          inline
        >
          <v-btn
            class="mr-1"
            density="comfortable"
            icon="mdi-tune-variant"
            @click="toggleMenu"
          />
        </v-badge>
        <v-btn
          v-else
          density="comfortable"
          icon="mdi-tune-variant"
          @click="toggleMenu"
        />
      </template>
      <template v-else>
        <v-btn
          v-if="query['hide-empty']"
          :title="$t(`${storeName}.fields.showEmpty`)"
          density="comfortable"
          icon="mdi-flask-empty-plus-outline"
          @click="hideEmpty"
        />
        <v-btn
          v-else
          :title="$t(`${storeName}.fields.hideEmpty`)"
          density="comfortable"
          icon="mdi-flask-empty-minus-outline"
          @click="hideEmpty"
        />
      </template>

      <template v-if="total > 0">
        <v-divider
          class="mx-4"
          vertical
        />

        <span>
          <v-btn
            :disabled="page <= 1"
            density="comfortable"
            icon="mdi-chevron-left"
            @click.stop="previousPage"
          />

          <span
            v-if="!smAndDown"
            class="ml-2"
          >
            {{ offset + 1 }}–{{ offset + entries.length }}
            {{ $t('sessions.fields.of') }} {{ total }}
          </span>

          <v-btn
            class="ml-2"
            :disabled="page >= numberOfPages"
            density="comfortable"
            icon="mdi-chevron-right"
            @click.stop="nextPage"
          />
        </span>
      </template>
    </template>
  </v-combobox>
</template>

<script setup>
import { ref, nextTick, computed, watch } from 'vue'
import { useStore } from 'vuex'
import { useDisplay } from 'vuetify'
import isArray from '@/composables/useIsArray'

const store = useStore()
const { smAndDown } = useDisplay()

const props = defineProps({
  storeName: {
    type: String,
    required: true
  },
  filter: {
    type: Boolean,
    required: false
  }
})

const items = [
  { key: 'titles' },
  { key: 'creators' },
  { key: 'location' },
  { key: 'institution' },
  { key: 'tags' }
]

const query = ref({})
function reset() {
  query.value = {}
}
function hideEmpty() {
  query.value['hide-empty'] = !query.value['hide-empty']
  search()
}
const numberOfQueries = computed(() => {
  let counter = 0
  Object.values(query.value).forEach((values) => {
    if (values instanceof Array) {
      counter += values.length
    }
  });
  return counter
})

const input = ref()
function onClickOutside({ target }) {
  if (input.value !== undefined) {
    if (!input.value.$el.contains(target)) {
      closeMenu()
    }
  }
}
function blurInput() {
  if (input.value !== undefined) {
    input.value.blur()
  }
}

const showMenu = ref(false)
function toggleMenu() {
  showMenu.value = !showMenu.value
}
function closeMenu() {
  showMenu.value = false
}
watch(showMenu,  (value) => {
  if (value) {
    blurInput()
  }
}, { immediate: true })

function onButton() {
  blurInput()
  nextTick(() => {
    search()
  })
}
function search() {
  store.dispatch(`${props.storeName}/post`, { 'query': query.value }).then(() => {
    closeMenu()
  })
}

const page = ref(1)
function nextPage() {
  page.value += 1
}
function previousPage() {
  page.value -= 1
}
const total = computed(() => {
  return store.state[props.storeName].data.total
})
const offset = computed(() => {
  return store.state[props.storeName].data.offset
})
const itemsPerPage = computed(() => {
  return store.state[props.storeName].itemsPerPage
})
const numberOfPages = computed(() => {
  return Math.ceil(total.value / itemsPerPage.value)
})
watch(page, (value) => {
  const lastEntry = entries.value.length + offset.value
  const withLastEntry = total.value === lastEntry
  if (
    ((value * itemsPerPage.value > lastEntry) && !withLastEntry)
    || (value * itemsPerPage.value <= offset.value)
  ) {
    const offset = (value - 1) * itemsPerPage.value
    store.dispatch(`${props.storeName}/post`, { offset })
  }
})

const params = computed(() => {
  return store.state.search.params
})
watch(params, ({ query: paramsQuery }) => {
  query.value = { 'hide-empty': false }
  if (paramsQuery) {
    Object.entries(paramsQuery).forEach(([key, values]) => {
      if (!isArray(values)) {
        values = [values]
      }
      if (['all-text', 'hide-empty'].includes(key)) {
        [values] = values
      }
      query.value[key] = values
    })
  }
}, { immediate: true })

const entries = computed(() => {
  return store.state[props.storeName].data.entries
})
watch(entries, () => {
  window.scrollTo(0, 0)
})
</script>

<style>
.v-field[role="combobox"],
.v-field[role="combobox"] .v-field__append-inner {
  display: flex;
}

.v-overlay.white .v-list {
  background-color: #fff;
}
</style>

<style scoped>
.v-list {
  padding: 0;
}
</style>
