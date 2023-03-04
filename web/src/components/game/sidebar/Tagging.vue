<template>
  <Sidebar
    v-bind="$props"
    v-on="$listeners"
  >
    <template v-slot:append-item>
      <v-row style="flex: 0;">
        <v-col>
          <v-combobox
            v-model="input"
            ref="input"
            v-on:blur="onBlur"
            @focus="focus = true;"
            @blur="focus = false;"
            @keyup.enter.native="post"
            :placeholder="$t('game.fields.tagging.post')"
            append-icon=""
            tabindex="0"
            background-color="#f9f9f9"
            hide-details
            rounded
            dense
            solo
            flat
          >
            <template v-slot:append-outer>
              <v-btn
                @click="onButton"
                class="post"
                color="primary"
                icon
              >
                <v-icon>
                  mdi-send
                </v-icon>
              </v-btn>
            </template>
          </v-combobox>
        </v-col>
      </v-row>
    </template>
  </Sidebar>
</template>

<script>
import Sidebar from '@/components/game/sidebar/Default.vue';

export default {
  extends: Sidebar,
  props: {
    ...Sidebar.props,
  },
  data() {
    return {
      input: null,
    };
  },
  methods: {
    post() {
      if (this.input) {
        const params = {
          tag: { name: this.input },
          game_language: this.$i18n.locale,
          resource_id: this.entry.resource_id,
        };
        this.$store.dispatch('game/post', params).then(() => {
          this.input = null;
          this.focusInput();
        });
      } else {
        this.focusInput();
      }
    },
    onButton() {
      this.blurInput();
      this.$nextTick(() => {
        this.post();
      });
    },
  },
  created() {
    this.$nextTick(() => {
      this.focusInput();
    });
  },
  components: {
    Sidebar,
  },
};
</script>

<style scoped>
.v-btn.post {
  transform: rotate(-45deg);
  transition: transform .3s ease-in-out !important;
}

.v-btn.post:hover {
  transform: rotate(0deg);
}
</style>
