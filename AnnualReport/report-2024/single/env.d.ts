/// <reference types="vite/client" />
declare module '*.vue' {
  import { ComponentOptions } from 'vue'
  const componentOptions: ComponentOptions
  export default componentOptions
}

interface ImportMetaEnv {
  VITE_DESC_HELLO: string;
  VITE_DESC_TEXT: string;
  VITE_DESC_HELLO_OTHER: string;
  VITE_DESC_TEXT_OTHER: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}