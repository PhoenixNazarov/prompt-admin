import {
    faCalculator,
    faCheck,
    faCircle,
    faCirclePlus,
    faDiagramProject,
    faInfoCircle,
    faPen,
    faPlus,
    faTable,
    faTerminal,
    faTrash,
    faUser,
    faXmark,
    faSpinner,
    faEye,
    faEyeSlash,
    faFile,
    faCaretRight
} from '@fortawesome/free-solid-svg-icons'
import {faCircle as farCircle} from '@fortawesome/free-regular-svg-icons'
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
        faCirclePlus,
        faCircle,
        farCircle,
        faSpinner,
        faEye,
        faEyeSlash,
        faFile,
        faCaretRight
    )
}
