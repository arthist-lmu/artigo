<template>
  <v-card
    color="transparent"
    flat
  >
    <v-tabs
      v-model="tab"
      background-color="transparent"
    >
      <v-tab
        v-for="item in items"
        :key="item.title"
      >
        {{ item.title }}
      </v-tab>
    </v-tabs>

    <v-tabs-items v-model="tab">
      <v-tab-item
        v-for="item in items"
        :key="item.title"
        :transition="false"
      >
        <v-card flat>
          <v-card-text class="px-8 pt-8 pb-0">
            <div
              v-for="text in item.texts"
              :key="text.header"
              class="mb-8"
            >
              <h2
                v-if="text.header"
                class="mb-2"
              >
                {{ text.header }}
              </h2>

              <p
                v-for="p in text.content"
                :key="p"
                v-html="p"
              />
            </div>

            <slot :title="item.title"></slot>
          </v-card-text>
        </v-card>
      </v-tab-item>
    </v-tabs-items>
  </v-card>
</template>

<script>
export default {
  props: {
    value: Number,
    items: Array,
  },
  data() {
    return {
      tab: null,
    };
  },
  watch: {
    value(tab) {
      this.tab = tab;
    },
  },
};
</script>

<style scoped>
.v-tabs,
.v-tab {
  height: 28px;
}

.v-tab {
  font-size: 12px;
}

.v-tab--active {
  background-color: #b8c9e1;
  color: #fff !important;
  border-radius: 4px 4px 0 0;
}

.v-sheet.v-card {
  border-radius: 0 0  4px 4px;
}
</style>
