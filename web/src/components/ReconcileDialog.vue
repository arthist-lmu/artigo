<template>
  <v-dialog
    v-model="dialog"
    max-width="450"
  >
    <v-card>
      <v-expansion-panels
        v-if="reconciliations.length"
        v-model="panel"
        theme="dark"
        mandatory
        flat
      >
        <v-expansion-panel
          v-for="reconciliation in reconciliations"
          :key="reconciliation.name"
          :disabled="reconciliation.entries.length === 0"
        >
          <v-expansion-panel-title
            :disable-icon-rotate="keyInObj(reconciliation.name, isSubmitted)"
          >
            <span class="clip w100">
              {{ $t('reconcile.fields.results', reconciliation.entries.length) }}
              {{ reconciliation.name }}
            </span>

            <template #actions>
              <v-icon
                v-if="keyInObj(reconciliation.name, isSubmitted)"
                color="success"
                variant="text"
              >
                mdi-check-circle-outline
              </v-icon>
              <v-icon
                v-else
                variant="text"
              >
                mdi-menu-down
              </v-icon>
            </template>
          </v-expansion-panel-title>

          <v-expansion-panel-text>
            <v-list
              v-if="reconciliation.entries.length"
              lines="two"
              theme="light"
            >
              <template
                v-for="(entry, i) in reconciliation.entries"
                :key="i"
              >
                <v-list-item>
                  <template #prepend>
                    <v-avatar color="primary">
                      {{ entry.score }}
                    </v-avatar>
                  </template>

                  <v-list-item-title>
                    {{ entry.name }}

                    <v-btn
                      v-if="reconciliation.service === 'Wikidata'"
                      :href="`https://www.wikidata.org/wiki/${entry.id}`"
                      target="_blank"
                      rel="noopener noreferrer"
                      class="ml-1"
                      variant="text"
                      density="comfortable"
                      icon="mdi-link-variant"
                      size="small"
                    />
                  </v-list-item-title>

                  <v-list-item-subtitle
                    v-if="entry.description"
                    style="line-height: 1.25;"
                    :title="capitalize(entry.description)"
                    class="mt-2"
                  >
                    {{ capitalize(entry.description) }}
                  </v-list-item-subtitle>

                  <template #append>
                    <v-btn
                      v-if="isSubmitted[reconciliation.name] === entry.id"
                      class="remove ml-1"
                      color="success"
                      variant="text"
                      density="comfortable"
                      icon="mdi-check-circle-outline"
                      @click="remove(reconciliation)"
                    />
                    <v-btn
                      v-else
                      class="add ml-1"
                      variant="text"
                      density="comfortable"
                      icon="mdi-checkbox-blank-circle-outline"
                      @click="add(entry.id, reconciliation)"
                    />
                  </template>
                </v-list-item>

                <v-divider
                  v-if="i + 1 < reconciliation.entries.length"
                  :key="`${entry.id}:divider`"
                  inset
                />
              </template>
            </v-list>
          </v-expansion-panel-text>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, nextTick, computed, watch } from 'vue'
import { useStore } from 'vuex'
import keyInObj from '@/composables/useKeyInObj'
import capitalize from '@/composables/useCapitalize'

const store = useStore()

const isSubmitted = ref({})
function add(entryId, {
  ids, type, name, service
}) {
  const params = {
    ids,
    type,
    service,
    entry_id: entryId
  }
  store.dispatch('reconcile/add', params)
  isSubmitted.value[name] = entryId
}
function remove({
  ids, type, name, service
}) {
  const params = {
    ids,
    type,
    service
  };
  store.dispatch('reconcile/remove', params)
  delete isSubmitted.value[name]
}

const panel = ref(0)
const dialog = ref(false)
const reconciliations = computed(() => store.state.reconcile.data.reconciliations)
watch(reconciliations, () => {
  dialog.value = true
  isSubmitted.value = {}
  nextTick(() => {
    panel.value = 0
  })
})
</script>

<style scoped>
.v-expansion-panel-text {
  background-color: #f7f8fb;
}

.v-btn.add:hover .v-icon::before {
  content: "\F05E1";
}

.v-btn.remove:hover .v-icon::before {
  content: "\F015A";
}
</style>
