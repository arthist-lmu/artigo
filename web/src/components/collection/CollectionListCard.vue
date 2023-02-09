<template>
  <v-card
    max-width="900"
    flat
  >
    <v-card-title :class="{ 'pt-6 px-6': !isDialog }">
      {{ $t("collection.title") }}

      <v-btn
        v-if="isDialog"
        @click="close"
        absolute
        right
        icon
      >
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </v-card-title>

    <v-card-text :class="[isDialog ? undefined : 'px-6', 'pt-4']">
      <v-data-table
        :headers="headers"
        :footer-props="footerProps"
        :items="collections"
        hide-default-footer
        multi-sort
      >
        <template v-slot:[`item.status`]="{ item }">
          <v-progress-circular
            v-if="item.status === 'U'"
            :title="item.progress + '%'"
            indeterminate
            color="primary"
            width="1.25"
            size="15"
          />

          <v-icon
            v-if="item.status === 'F'"
            style="font-size: 20px;"
          >
            mdi-check-circle-outline
          </v-icon>

          <v-icon
            v-if="item.status === 'E'"
            style="font-size: 20px;"
            color="accent"
          >
            mdi-alert-circle-outline
          </v-icon>
        </template>

        <template v-slot:[`item.date`]="{ item }">
          {{ toDate(item.date) }}
        </template>

        <template v-slot:[`item.actions`]="{ item }">
          <v-icon
            @click="show(item)"
            :title="$t('button.show')"
            class="mr-2"
            small
           >
            mdi-eye-outline
          </v-icon>

          <v-icon
            @click="remove(item)"
            :title="$t('button.delete')"
            small
          >
            mdi-close-circle-outline
          </v-icon>
        </template>
      </v-data-table>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  props: {
    isDialog: {
      type: Boolean,
      default: true,
    },
    value: Boolean,
  },
  data() {
    return {
      checkInterval: null,
      headers: [
        {
          text: '',
          value: 'status',
          width: 10,
          sortable: false,
        },
        {
          text: this.$t('collection.fields.name'),
          value: 'name',
        },
        {
          text: this.$t('collection.fields.count'),
          value: 'count',
          align: 'end',
          width: 150,
        },
        {
          text: this.$t('collection.fields.date'),
          value: 'date',
          align: 'end',
          width: 150,
        },
        {
          text: this.$t('collection.fields.actions'),
          value: 'actions',
          align: 'end',
          width: 100,
          sortable: false,
        },
      ],
      footerProps: {
        'items-per-page-text': '',
      },
    };
  },
  methods: {
    close() {
      clearInterval(this.checkInterval);
      this.$emit('input', false);
    },
    show() {
      // TODO
    },
    remove(item) {
      this.$store.dispatch('collection/remove', item).then(() => {
        this.$store.dispatch('collection/post');
      });
    },
    toDate(item) {
      return new Date(item).toLocaleDateString();
    },
  },
  computed: {
    collections() {
      return this.$store.state.collection.data.collections;
    },
  },
  watch: {
    collections() {
      clearInterval(this.checkInterval);
      if (this.value) {
        this.checkInterval = setInterval(() => {
          if (this.value) {
            this.$store.dispatch('collection/post');
          } else {
            clearInterval(this.checkInterval);
          }
        }, 10 * 1000);
      }
    },
    value: {
      handler(visible) {
        if (visible) {
          this.$store.dispatch('collection/post');
        } else {
          clearInterval(this.checkInterval);
        }
      },
      immediate: true,
    },
  },
};
</script>
