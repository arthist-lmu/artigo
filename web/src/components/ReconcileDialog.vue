<template>
  <v-dialog
    v-model="dialog"
    max-width="450"
  >
    <v-card>
      <v-list
        v-if="entries.length"
        two-line
      >
        <template v-for="(entry, index) in entries">
          <v-list-item :key="entry.id">
            <v-list-item-avatar color="primary">
              <span class="white--text">{{ index + 1 }}</span>
            </v-list-item-avatar>

            <v-list-item-content>
              <v-list-item-title class="text-h6">
                {{ entry.name }}

                <v-chip
                  class="ml-2"
                  outlined
                  small
                >
                  {{ entry.score }}
                </v-chip>
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
                @click="confirm(entry.id)"
                icon
              >
                <v-icon>
                  mdi-check-circle-outline
                </v-icon>
              </v-btn>
            </v-list-item-action>
          </v-list-item>

          <v-divider
            v-if="index + 1 < entries.length"
            :key="`${entry.id}:divider`"
            inset
          />
        </template>
      </v-list>

      <v-card-text
        v-else
        class="pt-5"
      >
        {{ $t('reconcile.fields.no-results') }}
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  data() {
    return {
      dialog: false,
    };
  },
  methods: {
    confirm(id) {
      console.log(id);
    },
  },
  computed: {
    entries() {
      return this.$store.state.reconcile.data.entries;
    },
  },
  watch: {
    entries() {
      this.dialog = true;
    },
  },
};
</script>
