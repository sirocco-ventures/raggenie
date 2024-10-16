import { create } from "zustand";
import { persist } from 'zustand/middleware'

const useAppSettings = create((set) => ({
  username: '',
  isAuthenticated: false,

  setUsername: (username) => set({ username }),

  setIsAuthenticated: (isAuthenticated) => set({ isAuthenticated })
}));


export const useTokenStore = create(
  persist(
    (set) => ({
      token: '',
      setToken: (token) => set({ token }),
    }),
    { name: 'auth_token' },
  )
);

export const storeToken = (token) => {
  const setToken = useTokenStore.getState().setToken;
  setToken(token); 
};

export default useAppSettings;
