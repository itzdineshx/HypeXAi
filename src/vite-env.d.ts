/// <reference types="vite/client" />

interface ImportMetaEnv {
	readonly VITE_API_BASE_URL?: string;
	readonly VITE_APP_NAME?: string;
	readonly VITE_DEFAULT_CHAIN_ID?: string;
	readonly VITE_EMAILJS_SERVICE_ID?: string;
	readonly VITE_EMAILJS_TEMPLATE_ID?: string;
	readonly VITE_EMAILJS_PUBLIC_KEY?: string;
	readonly VITE_EMAIL_ALERT_TO_EMAIL?: string;
	readonly VITE_ALERT_TO_EMAIL?: string;
}

interface ImportMeta {
	readonly env: ImportMetaEnv;
}
