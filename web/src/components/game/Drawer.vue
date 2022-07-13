<template>
  <v-navigation-drawer
    :width="width"
    app
  >
    <v-container fill-height>
      <v-row
        v-for="n in 3"
        :key="n"
      >
        <v-col>
          <v-card flat>
            Game {{ n }}
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-navigation-drawer>
</template>

<script>
export default {
  props: {
    width: {
      type: Number,
      default: 300,
    },
  },
  data() {
    return {

    };
  },
  methods: {

  },
  computed: {

  },
};
</script>
