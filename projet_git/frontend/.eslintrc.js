module.exports = {
  root: true,
  env: {
    browser: true,
    node:    true,
  },
  extends: [
    'eslint:recommended'
  ],
  parserOptions: {
    ecmaVersion: 2020,
    sourceType:  'module'
  },
  rules: {
    // customize any rules here; e.g. disable console warnings:
    'no-console': 'off'
  }
}

