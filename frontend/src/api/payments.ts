import { apiRequest } from "./client";
import type { PaymentStatus } from "../types";

export function initiateTopup(data: { amount_rub?: number; coins_amount?: number }) {
  return apiRequest<{ payment_id: string; confirmation_url: string }>(
    "/payments/topup",
    { method: "POST", body: JSON.stringify(data) }
  );
}

export function fetchPaymentStatus(paymentId: string) {
  return apiRequest<PaymentStatus>(`/payments/${paymentId}/status`);
}
