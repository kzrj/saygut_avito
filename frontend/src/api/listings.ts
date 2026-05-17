import { apiRequest, apiUpload } from "./client";
import type { Category, Listing } from "../types";

export function fetchCatalog(params: {
  page?: number;
  limit?: number;
  category?: string;
  q?: string;
}) {
  const search = new URLSearchParams();
  if (params.page) search.set("page", String(params.page));
  if (params.limit) search.set("limit", String(params.limit));
  if (params.category) search.set("category", params.category);
  if (params.q) search.set("q", params.q);
  return apiRequest<{
    items: Listing[];
    page: number;
    limit: number;
    total: number;
  }>(`/listings?${search}`);
}

export function fetchListing(id: string) {
  return apiRequest<Listing>(`/listings/${id}`);
}

export function fetchMyListings(status?: string) {
  const params = status ? `?status=${status}` : "";
  return apiRequest<{
    items: Listing[];
    page: number;
    limit: number;
    total: number;
  }>(`/listings/mine${params}`);
}

export function fetchCategories() {
  return apiRequest<Category[]>("/listings/categories");
}

export function createListing(data: {
  title: string;
  description: string;
  price_coins: number;
  images?: string[];
  category_id?: string;
}) {
  return apiRequest<Listing>("/listings", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export function publishListing(id: string) {
  return apiRequest<Listing>(`/listings/${id}/publish`, { method: "POST" });
}

export function uploadListingImages(id: string, files: File[]) {
  const form = new FormData();
  files.forEach((f) => form.append("files", f));
  return apiUpload<{ urls: string[] }>(`/listings/${id}/images`, form);
}
