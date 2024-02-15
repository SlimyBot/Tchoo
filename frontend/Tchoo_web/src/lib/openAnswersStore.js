import { reactive } from "vue"

const openStore = reactive({
    openAnswers: new Array(),

    addOpenAnswer(text) {
        this.openAnswers.push(text)
    },
    clear() {
        this.openAnswers.length = 0
    }
})

export default openStore
