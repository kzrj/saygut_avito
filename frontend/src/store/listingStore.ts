import { create } from "zustand";
import * as listingsApi from "../api/listings";
import type { Category, Listing } from "../types";

interface ListingState {
  catalog: Listing[];
  catalogTotal: number;
  myListings: Listing[];
  categories: Category[];
  current: Listing | null;
  loading: boolean;
  error: string | null;
  loadCatalog: (params?: {
    page?: number;
    category?: string;
    q?: string;
  }) => Promise<void>;
  loadCategories: () => Promise<void>;
  loadListing: (id: string) => Promise<void>;
  loadMine: (status?: string) => Promise<void>;
  createAndPublish: (data: {
    title: string;
    description: string;
    price_coins: number;
    category_id?: string;
    files?: File[];
  }) => Promise<Listing>;
}

export const useListingStore = create<ListingState>((set) => ({
  catalog: [],
  catalogTotal: 0,
  myListings: [],
  categories: [],
  current: null,
  loading: false,
  error: null,

  loadCatalog: async (params = {}) => {
    set({ loading: true, error: null });
    try {
      const res = await listingsApi.fetchCatalog(params);
      set({ catalog: res.items, catalogTotal: res.total, loading: false });
    } catch (e) {
      set({
        loading: false,
        error: e instanceof Error ? e.message : "Failed to load catalog",
      });
    }
  },

  loadCategories: async () => {
    try {
      const categories = await listingsApi.fetchCategories();
      set({ categories });
    } catch {
      /* optional */
    }
  },

  loadListing: async (id) => {
    set({ loading: true, error: null });
    try {
      const listing = await listingsApi.fetchListing(id);
      set({ current: listing, loading: false });
    } catch (e) {
      set({
        loading: false,
        error: e instanceof Error ? e.message : "Listing not found",
      });
    }
  },

  loadMine: async (status) => {
    set({ loading: true });
    try {
      const res = await listingsApi.fetchMyListings(status);
      set({ myListings: res.items, loading: false });
    } catch (e) {
      set({
        loading: false,
        error: e instanceof Error ? e.message : "Failed to load listings",
      });
    }
  },

  createAndPublish: async (data) => {
    set({ loading: true, error: null });
    try {
      let listing = await listingsApi.createListing({
        title: data.title,
        description: data.description,
        price_coins: data.price_coins,
        category_id: data.category_id,
      });
      if (data.files?.length) {
        await listingsApi.uploadListingImages(listing.id, data.files);
      }
      listing = await listingsApi.publishListing(listing.id);
      set({ loading: false });
      return listing;
    } catch (e) {
      set({
        loading: false,
        error: e instanceof Error ? e.message : "Failed to create listing",
      });
      throw e;
    }
  },
}));
