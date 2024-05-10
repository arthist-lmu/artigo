import { createI18n } from 'vue-i18n'

function loadLocaleMessages() {
  const messages = {}
  const modules = import.meta.glob('@/locales/[a-z-_.\\s]+\\.json')
  for (const path in modules) {
    modules[path]().then((module) => {
      const matched = path.match(/([A-Za-z0-9-_]+)\./i)
      if (matched && matched.length > 1) {
        messages[matched[1]] = {
          ...messages[matched[1]],
          ...module
        }
      }
    })
  }
  return messages
}

function getBrowserLocale(options = {}) {
  const defaultOptions = { countryCodeOnly: false }
  const opt = { ...defaultOptions, ...options }
  const navigatorLocale = navigator.languages !== undefined
    ? navigator.languages[0]
    : navigator.language
  if (!navigatorLocale) {
    return undefined
  }
  const trimmedLocale = opt.countryCodeOnly
    ? navigatorLocale.trim().split(/-|_/)[0]
    : navigatorLocale.trim()
  return trimmedLocale
}

function supportedLocalesInclude(locale) {
  const modules = import.meta.glob('@/locales/[a-z-_.\\s]+\\.json')
  return Object.entries(modules).some(([path,]) => {
    const pathLocale = path.split('/').at(-1).split('.')[0]
    return pathLocale === locale
  })
}

function getStartingLocale() {
  const browserLocale = getBrowserLocale({ countryCodeOnly: true })
  if (supportedLocalesInclude(browserLocale)) {
    return browserLocale
  }
  return import.meta.env.VUE_APP_I18N_LOCALE || 'en'
}

export default createI18n({
  legacy: false,
  allowComposition: true,
  locale: getStartingLocale(),
  fallbackLocale: import.meta.env.VUE_APP_I18N_FALLBACK_LOCALE || 'en',
  messages: loadLocaleMessages(),
  silentTranslationWarn: true
})
