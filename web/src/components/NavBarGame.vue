<template>
  <div v-if="entry">
    <h3
      v-if="rounds > 0"
      class="mx-8 mt-4 mb-0 uppercase row"
    >
      <div>
        {{ $t("game.fields.basic.rounds", { i: roundId, total: rounds }) }}
      </div>

      <v-spacer />

      <div v-if="this.tags">
        {{ this.score }}
      </div>
    </h3>

    <v-list
      v-if="tabooTags && tabooTags.length"
      class="pb-0"
      subheader
      dense
      flat
    >
      <v-subheader
        class="pl-1"
        inset
      >
        {{ $t("game.fields.taboo.tags") }}
      </v-subheader>

      <v-list-item
        dense
      >
        <v-list-item-content>
          <v-row class="ma-0">
            <v-chip
              v-for="tag in tabooTags"
              :key="tag.name"
              :title="tag.name"
              class="mr-1 mb-1 uppercase"
              small
            >
              {{ tag.name }}
            </v-chip>
          </v-row>
        </v-list-item-content>
      </v-list-item>
    </v-list>

    <v-list
      subheader
      dense
      flat
    >
      <v-subheader
        class="pl-1"
        inset
      >
        {{ $t("game.fields.basic.tags") }}
      </v-subheader>

      <v-list-item
        v-if="opponentTags && opponentTags.length"
        dense
      >
        <v-list-item-content>
          <v-row class="v-btn v-btn__content v-size--default">
            <v-col cols="auto">
              <v-icon
                color="primary"
                left
              >
                mdi-arrow-right-box
              </v-icon>

              {{ $t("game.fields.basic.opponent-tags") }}
            </v-col>

            <v-spacer />

            <v-col cols="auto">
              {{ opponentTagCount }}
            </v-col>
          </v-row>
        </v-list-item-content>
      </v-list-item>

      <v-list-item dense>
        <v-list-item-content>
          <v-row class="v-btn v-btn__content v-size--default">
            <v-col cols="auto">
              <v-icon
                color="primary"
                left
              >
                mdi-arrow-right-box
              </v-icon>

              {{ $t("game.fields.basic.own-tags") }}
            </v-col>

            <v-spacer />

            <v-col cols="auto">
              {{ this.tags.length }}
            </v-col>
          </v-row>
        </v-list-item-content>
      </v-list-item>
    </v-list>

    <v-list
      v-if="this.tags"
      class="pt-0"
      dense
      flat
    >
      <v-list-item
        dense
      >
        <v-list-item-content>
          <v-row class="ma-0">
            <v-chip
              v-for="tag in tags"
              :key="tag.name"
              :title="tag.name"
              class="mr-1 mb-1 uppercase"
              small
            >
              {{ tag.name }}

              <v-badge
                v-if="tag.score > 0"
                :content="tag.score"
                class="mr-n4"
                color="grey lighten-1"
                inline
              />
            </v-chip>
          </v-row>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </div>
</template>

<script>
export default {
  computed: {
    entry() {
      return this.$store.state.game.entry;
    },
    roundId() {
      return this.$store.state.game.roundId;
    },
    rounds() {
      return this.$store.state.game.rounds;
    },
    tags() {
      return this.$store.state.game.tags;
    },
    score() {
      let scoreSum = 0;
      this.tags.forEach(({ score }) => {
        scoreSum += score;
      });
      return scoreSum;
    },
    opponentTags() {
      return this.entry.opponent_tags;
    },
    tabooTags() {
      return this.entry.taboo_tags;
    },
    opponentTagCount() {
      const tags = this.opponentTags.filter((tag) => {
        return tag.created_after <= this.seconds;
      });
      return tags.length;
    },
    seconds() {
      return this.$store.state.game.seconds;
    },
  },
};
</script>
