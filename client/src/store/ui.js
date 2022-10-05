import { reactive } from 'vue'

export default () => {
  const state = reactive({})
  const openForm = (modal_form) => {
    state.modal_form = modal_form
  }
  return { state, openForm }
}