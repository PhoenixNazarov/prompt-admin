import type {App} from "vue";
import VueDiff from "vue-diff";
import 'vue-diff/dist/index.css';

export function installDiff(app: App) {
    app.use(VueDiff);
}