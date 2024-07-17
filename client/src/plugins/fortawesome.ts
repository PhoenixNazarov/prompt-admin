import {
    faCalculator,
    faCheck,
    faDiagramProject,
    faPen,
    faTable,
    faTerminal,
    faXmark,
    faTrash
} from '@fortawesome/free-solid-svg-icons'
import {library} from '@fortawesome/fontawesome-svg-core'
import type {App} from "vue";

export function installFortAwesome(_: App) {
    library.add(
        faDiagramProject,
        faTable,
        faTerminal,
        faPen,
        faCalculator,
        faCheck,
        faXmark,
        faTrash
    )
}
