import {Diagnostic, linter} from "@codemirror/lint";
import "./linter.css"
import {JinjaError} from "../../../stores/prompt.store.ts";

export function buildJinjaVarLinter() {
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
                    diagnostics.push({
                        from: startInd,
                        to: i + 2,
                        severity: "jinja",
                        actions: [
                            // {
                            // name: "Remove",
                            // apply(view, from, to) {
                            //   view.dispatch({changes: {from, to}})
                            // }
                            // }
                        ]
                    })
                    startInd = 0
                    open = true
                }
            }
        }
        return diagnostics
    })
}


export function buildJinjaListLinter() {
    return linter(view => {
        const diagnostics: Diagnostic[] = []
        const originText = view.state.doc.toString()
        let startInd = 0
        let open = true
        for (let i = 0; i < originText.length; i++) {
            if (open) {
                if (originText[i] == '{' && originText[i + 1] == '%') {
                    startInd = i
                    open = false
                }
            } else {
                if (originText[i] == '%' && originText[i + 1] == '}') {
                    diagnostics.push({
                        from: startInd,
                        to: i + 2,
                        severity: "jinja",
                        actions: [
                            // {
                            // name: "Remove",
                            // apply(view, from, to) {
                            //   view.dispatch({changes: {from, to}})
                            // }
                            // }
                        ]
                    })
                    startInd = 0
                    open = true
                }
            }
        }
        return diagnostics
    })
}


export function buildJinjaSyntaxLinter(errors: JinjaError[]) {
    return linter(view => {
        const diagnostics: Diagnostic[] = []
        const originText = view.state.doc.toString()
        let prevInd = 0
        let currentLine = 1
        for (let i = 0; i < originText.length; i++) {
            if (originText[i] == '\n' || i + 1 == originText.length) {
                errors.forEach(e => {
                    if (e.line_number == currentLine) {
                        diagnostics.push({
                            from: prevInd,
                            to: i,
                            severity: e.severity,
                            message: e.message
                        })
                    }
                })
                currentLine += 1
                prevInd = i
            }
        }
        return diagnostics
    })
}