import emailjs from "@emailjs/browser";
import type { EmailJSResponseStatus } from "@emailjs/browser/es/models/EmailJSResponseStatus";

export type EmailAlertPayload = {
  title: string;
  coin: string;
  message: string;
  severity: string;
  status: string;
  time: string;
};

const serviceId = import.meta.env.VITE_EMAILJS_SERVICE_ID as string | undefined;
const templateId = import.meta.env.VITE_EMAILJS_TEMPLATE_ID as string | undefined;
const publicKey = import.meta.env.VITE_EMAILJS_PUBLIC_KEY as string | undefined;
const toEmail =
  (import.meta.env.VITE_EMAIL_ALERT_TO_EMAIL as string | undefined) ||
  (import.meta.env.VITE_ALERT_TO_EMAIL as string | undefined);
const appName = (import.meta.env.VITE_APP_NAME as string | undefined) || "Hype Navigator";

export function isEmailAlertConfigured(): boolean {
  return Boolean(serviceId && templateId && publicKey);
}

export async function sendAlertEmail(payload: EmailAlertPayload): Promise<EmailJSResponseStatus> {
  if (!isEmailAlertConfigured()) {
    throw new Error("EmailJS is not configured. Add VITE_EMAILJS_* variables in your frontend .env file.");
  }

  // Send multiple key aliases so different EmailJS templates can map without code changes.
  return emailjs.send(
    serviceId as string,
    templateId as string,
    {
      app_name: appName,
      app: appName,
      subject: `[${appName}] ${payload.title} ${payload.coin}`,
      alert_title: payload.title,
      title: payload.title,
      alert_coin: payload.coin,
      coin: payload.coin,
      alert_message: payload.message,
      message: payload.message,
      alert_severity: payload.severity,
      severity: payload.severity,
      alert_status: payload.status,
      status: payload.status,
      alert_time: payload.time,
      time: payload.time,
      to_email: toEmail || "",
      recipient_email: toEmail || "",
      email: toEmail || "",
    },
    {
      publicKey: publicKey as string,
    }
  );
}
