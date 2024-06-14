import {Mapping, useMappingStore} from "../../../stores/config/mapping.store.ts";
import {Prompt} from "../../../stores/prompt.store.ts";
import {useMappingEntityStore} from "../../../stores/config/mappingEntity.store.ts";
import {autocompletion, CompletionContext} from "@codemirror/autocomplete";

export function createCompletions(mapping: Mapping, prompt: Prompt) {
    const mappingEntityStore = useMappingEntityStore()
    const options = []
    mappingEntityStore.getInputsByFilter(mapping, prompt).forEach(v => {
        options.push({label: v.macro, type: "text", apply: v.macro_value, detail: v.description})
    })

    mappingEntityStore.getMacroByFilter(mapping, prompt).forEach(v => {
        options.push({label: v.macro, type: "text", apply: v.macro_value, detail: v.description})
    })

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
