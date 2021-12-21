<template>
  <div id="artigo-game">
    <v-progress-linear :value="progress"></v-progress-linear>
    <h2>Only {{ secondsLeft }} seconds left!</h2>
    <v-img id="main-image" contain max-height="65vh" :src="data.path"></v-img>
    <v-container>
      <v-row>
        <v-text-field
          v-model="tagging"
          label="Discribe what you see"
          clearable
        ></v-text-field>
        <v-btn @click="displayImgUrl" color="primary" depressed rounded>
          Enter
        </v-btn>
        <v-btn @click="getRes" color="accent" depressed rounded> Skip </v-btn>
      </v-row>
    </v-container>
  </div>
</template>

<style>
#main-image {
  margin: 5%;
}
</style>

<script>
export default {
  data() {
    return {
      tagging: "",
      secondsLeft: 5,
      timeLimit: 5,
      progress: 0,
    };
  },

  methods: {
    getRes() {
      this.$store.dispatch("resource/get", { random: true });
    },
    displayImgUrl() {
      console.log(this.data.path);
    },
  },

  computed: {
    data() {
      return this.$store.state.resource.data;
    },
    metadata() {
      const metadata = {};
      const fields = [
        "titles",
        "creators",
        "location",
        "institution",
        "source",
      ];
      Object.keys(this.data).forEach((key) => {
        if (fields.includes(key)) {
          let values = this.data[key];
          if (values && typeof values !== "boolean") {
            if (typeof values === "string") {
              values = [{ name: values }];
            } else if (!this.isArray(values)) {
              values = [values];
            }
            if (this.isArray(values)) {
              metadata[key] = values;
            }
          }
        }
      });
      return metadata;
    },
    title() {
      if (this.keyInObj("titles", this.metadata)) {
        return this.metadata.titles[0];
      }
      return { id: -1, name: this.$t("resource.default.title") };
    },
    creator() {
      if (this.keyInObj("creators", this.metadata)) {
        return this.metadata.creators[0];
      }
      return { id: -1, name: this.$t("resource.default.creator") };
    },
    tags() {
      if (this.keyInObj("tags", this.data)) {
        if (this.moreTags && this.data.tags.length > 20) {
          return this.data.tags.slice(0, 20);
        }
        return this.data.tags;
      }
      return [];
    },
  },

  watch: {
    secondsLeft: {
      handler(value) {
        if (value > 0) {
          setTimeout(() => {
            this.secondsLeft -= 1;
            this.progress = 100 - (100 / this.timeLimit) * this.secondsLeft;
            if (this.secondsLeft === 0) {
              this.getRes();
            }
          }, 1000);
        }
      },
      immediate: true, // This ensures the watcher is triggered upon creation
    },
    "$route.params.id": function (id) {
      this.getData(id);
    },
  },

  created() {
    this.getRes();
  },
};
</script>
