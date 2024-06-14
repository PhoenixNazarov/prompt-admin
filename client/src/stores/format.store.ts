import {defineStore} from "pinia";
import {ApiService} from "../api/ApiService.ts";


export interface ConsistentReport {
    to_dict: boolean

    make_example_obj: boolean
    make_example_obj_converse: boolean
    make_example_obj_converse_equal: boolean

    make_example_json: boolean
    make_example_json_converse: boolean
    make_example_json_converse_equal: boolean

    make_example_xml: boolean
    make_example_xml_converse: boolean
    make_example_xml_converse_equal: boolean
}

export interface CalculateOutput {
    cant_load_schema_error?: string
    cant_generate_schema_error?: string

    format_json?: string

    example_json?: string
    cant_make_example_json_error?: string
    example_xml?: string
    cant_make_example_xml_error?: string

    consistent_report?: ConsistentReport
}

export interface ValidateOutput {
    cant_load_schema_error?: string
    cant_validate_value_error?: string
    validate_value?: string
}


export const useFormatStore = defineStore({
    id: 'format',
    state: () => ({}),
    getters: {},
    actions: {
        async load(schema_json: string): Promise<CalculateOutput> {
            return await ApiService.post<CalculateOutput>('/api/format/load', {schema_json})
        },
        async generate(input_object: string, mode: string): Promise<CalculateOutput> {
            return await ApiService.post<CalculateOutput>('/api/format/generate', {input_object, mode})
        },
        async validate(schema_json: string, obj: string): Promise<ValidateOutput> {
            return await ApiService.post<ValidateOutput>('/api/format/validate', {schema_json, obj})
        }
    }
})