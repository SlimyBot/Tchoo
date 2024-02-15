import { fileURLToPath, URL } from "node:url"

import { defineConfig } from "vite"
import vue from "@vitejs/plugin-vue"
import vsharp from "vite-plugin-vsharp"

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [
        vue(),
        vsharp({
            preserveMetadata: {
                orientation: true,
            },
        }),
    ],
    resolve: {
        alias: {
            "@": fileURLToPath(new URL("./src", import.meta.url)),
        },
    },
    test: {
        exclude: ["node_modules"],
    },
})
