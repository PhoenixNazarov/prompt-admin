import {Mapping} from "../../../stores/config/mapping.store.ts";
import {Prompt} from "../../../stores/prompt.store.ts";
import {useMappingEntityStore} from "../../../stores/config/mappingEntity.store.ts";
import {Diagnostic, linter} from "@codemirror/lint";

export function buildLinter(mapping: Mapping, prompt: Prompt) {
    const mappingEntityStore = useMappingEntityStore()
    const options = []
    mappingEntityStore.getInputsByFilter(mapping, prompt).forEach(v => {
        options.push({find: v.macro_value.replace('{{', '').replace('}}', '').trim(), description: v.description, macro: v.macro})
    })
    return linter(view => {
        const diagnostics: Diagnostic[] = []
        const originText = view.state.doc.toString()
        let startInd = 0
        let open = true
        for (let i = 0; i < originText.length; i++) {
            if (open) {
                if (originText[i] == '{' && originText[i + 1] == '{') {
                    startInd = i
                    open = false
                }
            } else {
                if (originText[i] == '}' && originText[i + 1] == '}') {
                    const splitText = originText.substring(startInd + 2, i).trim()
                    const input = options.find(e => e.find == splitText)
                    console.log(options)
                    if (input != undefined) {
                        diagnostics.push({
                            from: startInd,
                            to: i + 2,
                            severity: "hint",
                            message: input.description,
                            actions: [
                                // {
                                // name: "Remove",
                                // apply(view, from, to) {
                                //   view.dispatch({changes: {from, to}})
                                // }
                                // }
                            ]
                        })
                    } else {
                        diagnostics.push({
                            from: startInd,
                            to: i + 2,
                            severity: "error",
                            message: "Jinja var",
                            actions: [
                                // {
                                // name: "Remove",
                                // apply(view, from, to) {
                                //   view.dispatch({changes: {from, to}})
                                // }
                                // }
                            ]
                        })
                    }
                    startInd = 0
                    open = true
                }
            }
        }
        return diagnostics
    })
}
