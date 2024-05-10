import router from '@/router'

export default function useGoTo(name, extern = false, openInNewTab = false) {
  if (openInNewTab) {
    window.open(router.resolve({ name }).href, '_blank')
  } else {
    if (extern) {
      window.open(name, '_blank')
    } else {
      router.push({ name })
    }
  }
}
