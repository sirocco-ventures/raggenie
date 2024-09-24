import globals from "globals";
import pluginJs from "@eslint/js";
import pluginReact from "eslint-plugin-react";


export default [
  {
    files: ["**/*.{js,mjs,cjs,jsx}"]
  },
  {
    languageOptions: { 
      globals: globals.browser 
    }
  },
  pluginJs.configs.recommended,
  pluginReact.configs.flat.recommended,
  {
    "rules": {
      "no-console": "error",
      "no-multiple-empty-lines": "error",
      "react/react-in-jsx-scope": "off",
      "react/prop-types": "off",
      "react/jsx-uses-react": "off",
    }
  }
  
];