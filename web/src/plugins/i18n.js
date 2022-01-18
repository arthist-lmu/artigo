import Vue from 'vue';
import VueI18n from 'vue-i18n';

Vue.use(VueI18n);

function loadLocaleMessages() {
  const locales = require.context('../locales', true,
    /[A-Za-z0-9-_,\s]+\.json$/i);
  const messages = {};
  locales.keys().forEach((key) => {
    const matched = key.match(/([A-Za-z0-9-_]+)\./i);
    if (matched && matched.length > 1) {
      messages[matched[1]] = locales(key);
    }
  });
  return messages;
}

function getBrowserLocale(options = {}) {
  const defaultOptions = { countryCodeOnly: false };
  const opt = { ...defaultOptions, ...options };
  const navigatorLocale = navigator.languages !== undefined
    ? navigator.languages[0]
    : navigator.language;
  if (!navigatorLocale) {
    return undefined;
  }
  const trimmedLocale = opt.countryCodeOnly
    ? navigatorLocale.trim().split(/-|_/)[0]
    : navigatorLocale.trim();
  return trimmedLocale;
}

function supportedLocalesInclude(locale) {
  const locales = require.context('../locales', true,
    /[A-Za-z0-9-_,\s]+\.json$/i);
  const locale_list = locales.keys();
  for (let i = 0; i < locale_list.length; i += 1) {
    const lang = locale_list[i].split('/')[1].split('.')[0];
    if (lang === locale) {
      return true;
    }
    return false;
  }
  return locale.match(/([A-Za-z0-9-_]+)\./i);
}

function getStartingLocale() {
  const browserLocale = getBrowserLocale({ countryCodeOnly: true });
  if (supportedLocalesInclude(browserLocale)) {
    return browserLocale;
  }
  return process.env.VUE_APP_I18N_LOCALE || 'en';
}

export default new VueI18n({
  locale: getStartingLocale(),
  fallbackLocale: process.env.VUE_APP_I18N_FALLBACK_LOCALE || 'en',
  messages: loadLocaleMessages(),
});
