export interface UserProfile {
  id: string;
  email: string | null;
  phone: string | null;
  display_name: string;
  wallet_balance: number;
  referral_code: string;
  role: string;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  user: UserProfile;
}

export interface Listing {
  id: string;
  seller_id: string;
  title: string;
  description: string;
  category_id: string | null;
  images: string[];
  price_coins: number;
  price_mode: string;
  status: string;
  created_at: string;
  published_at: string | null;
}

export interface Transaction {
  id: string;
  type: string;
  amount: number;
  balance_after: number;
  status: string;
  related_type: string | null;
  related_id: string | null;
  created_at: string;
}

export interface Category {
  id: string;
  slug: string;
  name: string;
}

export interface ReferralStats {
  code: string;
  invited_count: number;
  earned_coins: number;
}

export interface PaymentStatus {
  id: string;
  status: string;
  amount_rub: number;
  coins_amount: number;
  confirmation_url: string | null;
  transaction_id: string | null;
  created_at: string;
}
