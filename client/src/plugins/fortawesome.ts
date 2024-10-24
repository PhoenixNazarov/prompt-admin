import {
    faAngleRight,
    faArrowLeft,
    faCalculator,
    faCalendarPlus,
    faCaretRight,
    faCheck,
    faCircle,
    faCirclePlus,
    faClock,
    faDiagramProject,
    faEye,
    faEyeSlash,
    faFile,
    faFloppyDisk,
    faInfoCircle,
    faMagnifyingGlass,
    faPen,
    faPlus,
    faRepeat,
    faSpinner,
    faTable,
    faTableColumns,
    faTerminal,
    faTrash,
    faUser,
    faXmark
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
        faCaretRight,
        faFloppyDisk,
        faRepeat,
        faMagnifyingGlass,
        faCalendarPlus,
        faClock,
        faArrowLeft,
        faAngleRight,
        faTableColumns
    )
}
