import {
    faCalculator,
    faCheck,
    faDiagramProject,
    faInfoCircle,
    faPen,
    faPlus,
    faTable,
    faTerminal,
    faTrash,
    faUser,
    faXmark,
    faCirclePlus
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
        faTrash,
        faUser,
        faInfoCircle,
        faPlus,
        faCirclePlus
    )
}
