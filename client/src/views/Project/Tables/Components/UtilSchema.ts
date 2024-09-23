import {ComponentContextSchema, ComponentContextType} from "../types";

const contextRegexp = new RegExp('\\$[_a-zA-Z][a-zA-Z0-9]*(.[_a-zA-Z][a-zA-Z0-9]*)*')

class UtilSchema {
    getProject(contextSchema: ComponentContextSchema | undefined): string {
        return this.renderReference('$project', contextSchema) as string
    }

    renderReference(text: string, contextSchema: ComponentContextSchema | undefined) {
        const regexpExec = contextRegexp.exec(text)
        if (regexpExec && regexpExec[0] == text) {
            // is context key
            return this.getValueByKeyForContext(text, contextSchema)
        }
        // another: need to paste context components
        while (true) {
            const match = text.match(contextRegexp)
            if (match) {
                const key = match[0]
                const value = this.getValueByKeyForContext(key, contextSchema)
                text = text.replace(key, String(value))
            } else {
                break
            }
        }
        return text
    }


    getValueByKeyForContext(key: string, contextSchema: ComponentContextSchema | undefined): ComponentContextType {
        if (!contextSchema?.componentContext) return
        if (key[0] == '$') key = key.slice(1)
        else return

        const keys = key.split('.')
        let context = contextSchema.componentContext
        for (const key of keys) {
            if (typeof context == 'object') {
                const newContext = context[key]
                if (!newContext) return newContext
                context = newContext
            } else {
                return context
            }
        }
        return context
    }

    setValueByKeyForContext(key: string, value: ComponentContextType, contextSchema: ComponentContextSchema | undefined) {
        if (!contextSchema?.componentContext) return
        if (key[0] == '$') key = key.slice(1)
        else return

        const keys = key.split('.')
        let context = contextSchema.componentContext
        for (const key of keys.slice(0, keys.length - 1)) {
            if (typeof context == 'object') {
                let nextContext = context[key]
                if (!nextContext) {
                    nextContext = {}
                    context[key] = nextContext
                }
                context = nextContext
            } else {
                break
            }
        }
        if (typeof context == 'object') {
            context[keys[keys.length - 1]] = value
        }
    }
}

export default new UtilSchema()
