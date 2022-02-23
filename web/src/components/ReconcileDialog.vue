<template>
  <v-dialog
    v-model="dialog"
    max-width="450"
  >
    <v-card>
      <v-expansion-panels
        v-if="reconciliations.length"
        v-model="panel"
        mandatory
      >
        <v-expansion-panel
          v-for="reconciliation in reconciliations"
          :key="reconciliation.name"
          :disabled="reconciliation.entries.length === 0"
        >
          <v-expansion-panel-header :disable-icon-rotate="keyInObj(reconciliation.name, isSubmitted)">
            <span class="clip w100">
              {{ $tc('reconcile.fields.results', reconciliation.entries.length) }}
              {{ reconciliation.name }}
            </span>

            <template v-slot:actions>
              <v-icon
                v-if="keyInObj(reconciliation.name, isSubmitted)"
                color="success"
              >
                mdi-check-circle-outline
              </v-icon>
              <v-icon v-else>
                mdi-menu-down
              </v-icon>
            </template>
          </v-expansion-panel-header>

          <v-expansion-panel-content>
            <v-list
              v-if="reconciliation.entries.length"
              two-line
              flat
            >
              <template v-for="(entry, index) in reconciliation.entries">
                <v-list-item :key="entry.id">
                  <v-list-item-avatar color="primary">
                    <span class="white--text">{{ entry.score }}</span>
                  </v-list-item-avatar>

                  <v-list-item-content>
                    <v-list-item-title class="text-h6">
                      <v-btn
                        v-if="reconciliation.service === 'Wikidata'"
                        :href="`https://www.wikidata.org/wiki/${entry.id}`"
                        target="_blank"
                        small
                        icon
                      >
                        <v-icon small>
                          mdi-link-variant
                        </v-icon>
                      </v-btn>

                      {{ entry.name }}
                    </v-list-item-title>

                    <v-list-item-subtitle
                      v-if="entry.description"
                      :title="capitalize(entry.description)"
                      class="mt-2"
                    >
                      {{ capitalize(entry.description) }}
                    </v-list-item-subtitle>
                  </v-list-item-content>

                  <v-list-item-action>
                    <v-btn
                      v-if="isSubmitted[reconciliation.name] === entry.id"
                      @click="remove(reconciliation)"
                      class="remove"
                      color="success"
                      icon
                    >
                      <v-icon>
                        mdi-check-circle-outline
                      </v-icon>
                    </v-btn>

                    <v-btn
                      v-else
                      @click="add(entry.id, reconciliation)"
                      class="add"
                      icon
                    >
                      <v-icon>
                        mdi-checkbox-blank-circle-outline
                      </v-icon>
                    </v-btn>
                  </v-list-item-action>
                </v-list-item>

                <v-divider
                  v-if="index + 1 < reconciliation.entries.length"
                  :key="`${entry.id}:divider`"
                  inset
                />
              </template>
            </v-list>
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-card>
  </v-dialog>
</template>

<script>
import Vue from 'vue';

export default {
  data() {
    return {
      isSubmitted: {},
      dialog: false,
      panel: 0,
    };
  },
  methods: {
    add(entryId, { name }) {
      // TODO: send update request to Django backend
      Vue.set(this.isSubmitted, name, entryId);
    },
    remove({ name }) {
      // TODO: send update request to Django backend
      Vue.delete(this.isSubmitted, name);
    },
  },
  computed: {
    reconciliations() {
      return this.$store.state.reconcile.data.reconciliations || [];
    },
  },
  watch: {
    reconciliations() {
      this.dialog = true;
      this.isSubmitted = {};
      this.$nextTick(() => {
        this.panel = 0;
      });
    },
    panel(value) {
      if (value === undefined) {
        this.panel = 0;
      }
    },
  },
};
</script>

<style>
.v-expansion-panel::before {
  box-shadow: 0 0 0 0 rgba(0, 0, 0, .2),
    0 0 0 0 rgba(0, 0, 0, .14),
    0 0 0 0 rgba(0, 0, 0, .12);
}
</style>

<style scoped>
.v-btn.add:hover .v-icon::before {
  content: "\F05E1";
}

.v-btn.remove:hover .v-icon::before {
  content: "\F015A";
}
</style>
