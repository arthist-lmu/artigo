import i18n from '@/plugins/i18n'

export default function getTitle(item, multiple = false) {
  const { t } = i18n.global

  if (item && item.meta) {
    const titles = item.meta
      .filter(({ name, value_str }) => name === 'titles' && value_str)
      .map(({ value_str }) => value_str)

    if (titles.length > 0) {
      return multiple ? Array.from(new Set(titles)) : titles[0]
    }
  }
  return t('resource.default.title')
}
