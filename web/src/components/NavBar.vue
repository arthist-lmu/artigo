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
            link
            :to="'/' + $i18n.locale + '/' + 'about'"
        >
            <v-list-item-content>
            <v-list-item-title>
                {{ $t("navbar.about") }}
            </v-list-item-title>
            <v-list-item-subtitle>
                Idea, Goals, Project details
            </v-list-item-subtitle>
            </v-list-item-content>
        </v-list-item>

        <v-list-item
            link
            :to="'/' + $i18n.locale + '/' + 'publications'"
        >
            <v-list-item-content>
            <v-list-item-title>
                {{ $t("navbar.publications") }}
            </v-list-item-title>
            <v-list-item-subtitle>
                Research, literature, media
            </v-list-item-subtitle>
            </v-list-item-content>
        </v-list-item>

        <v-list-item
            link
            :to="'/' + $i18n.locale + '/' + 'artigo-game'"
        >
            <v-list-item-content>
            <v-list-item-title>
                {{ $t("navbar.artigo-game") }}
            </v-list-item-title>
            <v-list-item-subtitle>
                Not implemented
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
    };
  },
};
</script>
