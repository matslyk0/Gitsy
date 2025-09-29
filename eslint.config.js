// eslint.config.js at the project root
import js from "@eslint/js";
import react from "eslint-plugin-react"
import reactHooks from "eslint-plugin-react-hooks"
import prettier from "eslint-config-prettier";
import globals from "globals";

export default [
    js.configs.recommended,
    {
        plugins: {
            react,
            "react-hooks": reactHooks
        },
        languageOptions: {
            globals: globals.browser,
            parserOptions: {
                ecmaVersion: "latest",
                sourceType: "module",
                ecmaFeatures: {
                    jsx: true
                }
            }
        },
        rules: {
            ...react.configs.recommended.rules,
            ...reactHooks.configs.recommended.rules
        },
        settings: {
            react: {
                version: "detect"
            }
        }
    },
    prettier,
];
