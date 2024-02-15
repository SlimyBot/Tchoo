import js from "@eslint/js";
import vue from "eslint-plugin-vue";
import globals from "globals";
import vueEslintParser from "vue-eslint-parser";


export default [

    {
        languageOptions: {
            globals: {
                ...globals.browser,
                myCustomGlobal: "readonly"
            },
            parser: vueEslintParser,
            parserOptions: {
                ecmaVersion: 2022,
                sourceType: "module"
            }
        },
    
  files: ["**/*.js", "**/*.vue"],
  plugins: {
    js: js,
    vue: vue
  },
  rules: {
    "vue/no-deprecated-scope-attribute": "error",
    "vue/no-unused-components": "error", 
    "vue/no-unused-vars": "warn",
    "vue/no-unused-properties": "error",
    "vue/html-indent": "error",
    "vue/script-indent": ["error", 2, { "baseIndent": 0 }], 
    "vue/max-attributes-per-line": "error",
    "vue/html-closing-bracket-newline": "error",
    "vue/html-self-closing": "error",
    "vue/order-in-components": "error",
    "vue/attributes-order": "error",
    "vue/singleline-html-element-content-newline": "error",
    "vue/multiline-html-element-content-newline": "error",
    "vue/require-default-prop": "error",
    "vue/require-prop-types": "error",
    "vue/require-v-for-key": "error",
    "vue/no-v-html": "error",
    "vue/attribute-hyphenation": ["error", "always"],
    "vue/html-quotes": ["error", "double"],
    "vue/no-reserved-keys": "error",
    "vue/no-shared-component-data": "error",
    "vue/no-template-shadow": "error",
    "vue/prop-name-casing": ["error", "camelCase"],
    "vue/require-direct-export": "error",
    "vue/v-bind-style": ["error", "shorthand"],
    "vue/v-on-style": ["error", "shorthand"],
    "vue/this-in-template": ["error", "never"],
    "vue/component-definition-name-casing": ["error", "PascalCase"],
    "vue/no-deprecated-slot-attribute": "error",
    "vue/no-template-target-blank": "error",
    "vue/valid-v-slot": "error",
    "vue/singleline-html-element-content-newline": "error",
    "vue/no-duplicate-attributes": "error",
    "vue/no-useless-mustaches": "error",
    "vue/no-useless-v-bind": "error",
    "vue/valid-v-on": "error",
    "vue/no-lone-template": "error",
    "vue/no-parsing-error": "error",
    "vue/no-multiple-slot-args": "error",
    "vue/no-ref-object-reactivity-loss": "error",
    "vue/no-required-prop-with-default": "error",
    "vue/no-restricted-class": "error",
    "vue/no-this-in-before-route-enter": "error",
    "vue/prefer-prop-type-boolean-first": "error",
    "vue/valid-define-options": "error",
    "vue/no-irregular-whitespace": "error",
    "vue/valid-template-root": "error",
    "vue/no-use-v-if-with-v-for": "error",
    "vue/require-name-property": "error",
    "vue/require-render-return": "error",

  },
  
  
}
];
