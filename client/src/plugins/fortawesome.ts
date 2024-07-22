import {
    faCalculator,
    faCheck,
    faCirclePlus,
    faDiagramProject,
    faInfoCircle,
    faPen,
    faPlus,
    faTable,
    faTerminal,
    faTrash,
    faUser,
    faXmark
} from '@fortawesome/free-solid-svg-icons'
import {dom, library} from '@fortawesome/fontawesome-svg-core'
import type {App} from "vue";

export function installFortAwesome(_: App) {
    dom.watch()
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
