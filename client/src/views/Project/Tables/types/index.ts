import {NavigationSchema} from "./navigation.ts";
import {GroupSchema} from "./group.ts";
import {ElementSchema} from "./element.ts";

export * from "./base.ts"
export * from './navigation.ts'
export * from './group.ts'
export * from './element.ts'
export * from './event.ts'
export * from './input.ts'

export type GroupElementSchema = GroupSchema | ElementSchema
export type ComponentSchema = NavigationSchema | GroupElementSchema

