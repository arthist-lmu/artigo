<template>
    <v-navigation-drawer
        app
        permanent
    >
        <v-img
        id="logo"
        src="/assets/images/logo.svg"
        >
        </v-img>
        <h4 id="subtitle">Social Image Tagging</h4>

        <v-divider></v-divider>

        <v-list
        nav
        >
        <v-list-item
            v-for="nav_entry in nav_list"
            :key="nav_entry.title"
            link
            :to="'/' + $i18n.locale + '/' + nav_entry.link"
        >
            <v-list-item-content>
            <v-list-item-title>
                <!-- <router-link :to="'/' + $i18n.locale + '/' + nav_entry.link"> -->
                {{ nav_entry.title }}
                <!-- </router-link> -->
            </v-list-item-title>
            <v-list-item-subtitle>
                {{ nav_entry.subtitle }}
            </v-list-item-subtitle>
            </v-list-item-content>
        </v-list-item>
        </v-list>

        <v-divider></v-divider>

        <v-list-item>
        <v-list-item-content>
            <v-list-item-title>
            <a href="https://www.kunstgeschichte.uni-muenchen.de/funktionen/impressum/index.html">{{ $t("navbar.imprint") }}</a>
            </v-list-item-title>
        </v-list-item-content>
        </v-list-item>

        <v-list-item>
            <v-list-item-title>
            <a href="https://www.kunstgeschichte.uni-muenchen.de/funktionen/datenschutz/index.html">{{ $t("navbar.privacy") }}</a>
            </v-list-item-title>
        </v-list-item>
    </v-navigation-drawer>
</template>

<style>
#logo { margin: 10px; }
#subtitle { margin: 10px; }
</style>

<script>
import i18n from '@/plugins/i18n';

export default {
  data() {
    return {
      nav_list: [
        { link: 'about', title: i18n.t('navbar.about'), subtitle: 'Idea, Goals, Project details' },
        { link: 'publications', title: i18n.t('navbar.publications'), subtitle: 'Research, literature, media' },
        { link: 'artigo-game', title: 'Artigo-Game', subtitle: 'Not implemented' },
        { link: 'artigo-game', title: 'Karido', subtitle: 'Not implemented' },
        { link: 'artigo-game', title: 'ARTigo-Quiz', subtitle: 'Not implemented' },
        { link: 'artigo-game', title: 'ARTigo-Taboo', subtitle: 'Not implemented' },
        { link: 'artigo-game', title: 'Tag A Tag', subtitle: 'Not implemented' },
        { link: 'artigo-game', title: 'Combino', subtitle: 'Not implemented' },
        { link: 'artigo-game', title: 'ARTime', subtitle: 'Not implemented' },
        { link: 'artigo-game', title: 'Crossover', subtitle: 'Not implemented' },
      ],
    };
  },
};
</script>