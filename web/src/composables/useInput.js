export default function useResource(input) {
  function blurInput() {
    if (input.value !== undefined) {
      input.value.blur()
    }
  }
  function focusInput() {
    window.setTimeout(() => {
      if (input.value !== undefined) {
        input.value.focus()
      }
    }, 0)
  }

  return {
    blurInput,
    focusInput
  }
}
