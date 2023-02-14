<template>
  <Card
    v-bind="$props"
    v-on="$listeners"
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
          large
        >
          {{ icon }}
        </v-icon>
      </v-col>

      <v-col>
        <p class="mb-0">{{ text }}</p>
      </v-col>
    </v-row>

    <template v-slot:actions>
      <v-row>
        <v-col cols="6">
          <v-btn
            v-if="page"
            @click="goTo(page)"
            tabindex="0"
            color="primary"
            depressed
            rounded
            block
          >
            {{ $t("field.okay") }}
          </v-btn>
          <v-btn
            v-else
            @click="close"
            tabindex="0"
            color="primary"
            depressed
            rounded
            block
          >
            {{ $t("field.okay") }}
          </v-btn>
        </v-col>

        <v-col cols="6">
          <v-btn
            @click="close"
            tabindex="0"
            depressed
            rounded
            block
          >
            {{ $t("field.abort") }}
          </v-btn>
        </v-col>
      </v-row>
    </template>
  </Card>
</template>

<script>
import Card from '@/components/utils/Card.vue';

export default {
  extends: Card,
  props: {
    text: String,
    icon: {
      type: String,
      required: false,
    },
    page: {
      type: String,
      required: false,
    },
    ...Card.props,
  },
  methods: {
    goTo(name) {
      const route = this.$router.resolve({ name });
      window.open(route.href, '_blank');
      this.close();
    },
  },
  components: {
    Card,
  },
};
</script>
