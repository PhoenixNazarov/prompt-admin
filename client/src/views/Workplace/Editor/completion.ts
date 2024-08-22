import {Mapping} from "../../../stores/config/mapping.store.ts";
import {Prompt} from "../../../stores/prompt.store.ts";
import {useMappingEntityStore} from "../../../stores/config/mappingEntity.store.ts";
import {autocompletion, CompletionContext} from "@codemirror/autocomplete";
import {useVarsStore} from "../../../stores/vars.store.ts";

type Completion = { label: string, type: "text", apply: string, detail: string }

function collectSyncDataObject(prefix: string, object: any, first = false): Completion[] {
    if (object.constructor.name == 'Object') {
        let output: Completion[] = []
        Object.keys(object).forEach(key => {
            const label = first ? key : `${prefix}.${key}`
            if (object[key] && object[key].constructor.name == 'Object') {
                output = [...output, ...collectSyncDataObject(label, object[key])]
            } else if (object[key] && object[key].constructor.name == 'Array') {
                output = [...output, ...collectSyncDataObject(label + '[0]', object[key][0])]
            } else {
                output.push(
                    {
                        label: '{{ ' + label + ' }}',
                        type: 'text',
                        apply: '{{ ' + label + ' }}',
                        detail: object[key]
                    }
                )
            }
        })
        return output
    }
    return []
}


export function createCompletions(mapping: Mapping, prompt: Prompt) {
    const mappingEntityStore = useMappingEntityStore()
    const varsStore = useVarsStore()
    let options = []

    const syncData = mappingEntityStore.getSyncDataByFilter(mapping, prompt)

    if (syncData) {
        try {
            const context = JSON.parse(syncData.template_context_default)
            options = collectSyncDataObject('', context, true)
        } catch (e) {
        }
    } else {
        mappingEntityStore.getInputsByFilter(mapping, prompt).forEach(v => {
            options.push({label: v.macro, type: "text", apply: v.macro_value, detail: v.description})
        })

        mappingEntityStore.getMacroByFilter(mapping, prompt).forEach(v => {
            options.push({label: v.macro, type: "text", apply: v.macro_value, detail: v.description})
        })
    }

    // VARIABLES
    const vars = varsStore.getByProject(mapping.connection_name)
    vars.forEach(
        v => {
            options.push({
                label: `{{ var.${v.key} }}`,
                type: 'text',
                apply: `{{ var.${v.key} }}`,
                detail: v.value
            })
        }
    )

    // TEMPLATES
    const template = varsStore.getTemplateByProject(mapping.connection_name)
    template.forEach(
        v => {
            options.push({
                label: `{{ render_template("${v.key}") }}`,
                type: 'text',
                apply: `{{ render_template("${v.key}") }}`,
                detail: v.value
            })
        }
    )

    function myCompletions(context: CompletionContext) {
        let word = context.matchBefore(/\w*/)
        if (!word) return
        if (word.from == word.to && !context.explicit)
            return null


        return {
            from: word.from,
            options: options
        }
    }

    return autocompletion({override: [myCompletions]})
}
