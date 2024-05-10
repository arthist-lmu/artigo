import i18n from '@/plugins/i18n'

export default function getCreators(item) {
  const { t } = i18n.global

  if (item && item.meta) {
    const creators = item.meta
      .filter(({ name, value_str }) => name === 'creators' && value_str)
      .map(({ value_str }) => value_str)

    if (creators.length > 0) {
      return Array.from(new Set(creators))
    }
  }
  return [t('resource.default.creator')]
}
