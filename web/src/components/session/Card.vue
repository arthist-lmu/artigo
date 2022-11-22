<template>
  <v-hover v-slot="{ hover }">
    <div
      @click="goTo('session')"
      @keyDown="goTo('session')"
      class="grid-item"
      :disabled="isDisabled"
    >
      <img
        :src="entry.path"
        v-on:error="onError"
        alt=""
      />

      <v-container class="overlay">
        <v-row style="flex: 0;">
          <v-col class="pa-4">
            <div class="text-subtitle-1 white--text">
              <b>{{ date }}</b>
            </div>

            <div class="text-caption">
              <v-icon
                class="mt-n1"
                color="white"
                x-small
                left
              >
                mdi-clock-outline
              </v-icon>

              <span>{{ time }}</span>
            </div>
          </v-col>
        </v-row>

        <v-row></v-row>

        <v-row style="flex: 0;">
          <v-col class="pa-4" align="right">
            <v-btn
              color="primary"
              style="min-width: 50px !important;"
              depressed
              absolute
              rounded
              bottom
              right
            >
              <v-icon left>
                mdi-tag-outline
              </v-icon>

              {{ entry.annotations }}
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </div>
  </v-hover>
</template>

<script>
export default {
  props: {
    entry: Object,
    height: {
      type: String,
      default: '225',
    },
  },
  data() {
    return {
      isDisabled: false,
    };
  },
  methods: {
    goTo(name) {
      const params = { id: this.entry.id };
      this.$router.push({ name, params });
    },
    onError() {
      this.isDisabled = true;
    },
  },
  computed: {
    lang() {
      return this.$i18n.locale;
    },
    date() {
      const created = new Date(this.entry.created);
      return created.toLocaleDateString(this.lang);
    },
    time() {
      const created = new Date(this.entry.created);
      return created.toLocaleTimeString(this.lang);
    },
  },
};
</script>

<style scoped>
.grid-item {
  border-radius: 28px;
  position: relative;
  overflow: hidden;
  min-width: 80px;
  cursor: pointer;
  display: block;
  height: 225px;
  flex-grow: 1;
}

.grid-item[disabled] {
  display: none;
}

.grid-item > img {
  transition: transform 0.5s ease;
  transform: scale(1.05);
  object-position: top;
  object-fit: cover;
  min-width: 100%;
  max-width: 100%;
  height: 100%;
}

.grid-item:hover > img {
  transform: scale(1.3);
}

.container {
  position: absolute;
  width: 100%;
  bottom: 0;
  left: 0;
}

.container {
  flex-direction: column;
  display: flex;
  height: 100%;
}

.container .overlay {
  background: linear-gradient(to bottom, black, #00000000 40%);
  transform: translate(-50%, -50%);
  position: absolute;
  object-fit: cover;
  min-width: 100%;
  max-width: 100%;
  color: #ffffff;
  height: 100%;
  left: 50%;
  top: 50%;
}

.container .overlay .col > * {
  text-overflow: ellipsis;
  line-height: 1.25rem;
  white-space: nowrap;
  overflow: hidden;
}
</style>
