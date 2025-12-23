import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export const useAuthStore = create(
    persist(
        (set) => ({
            user: null,
            accessToken: null,
            refreshToken: null,
            isAuthenticated: false,

            setAuth: (user, tokens) => {
                localStorage.setItem('access_token', tokens.access);
                localStorage.setItem('refresh_token', tokens.refresh);
                set({
                    user,
                    accessToken: tokens.access,
                    refreshToken: tokens.refresh,
                    isAuthenticated: true,
                });
            },

            updateUser: (userData) => set({ user: userData }),

            logout: () => {
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                set({
                    user: null,
                    accessToken: null,
                    refreshToken: null,
                    isAuthenticated: false,
                });
            },
        }),
        {
            name: 'auth-storage',
        }
    )
);

export const useThemeStore = create(
    persist(
        (set) => ({
            isDark: false,
            toggleTheme: () => set((state) => {
                const newIsDark = !state.isDark;
                if (newIsDark) {
                    document.documentElement.classList.add('dark');
                } else {
                    document.documentElement.classList.remove('dark');
                }
                return { isDark: newIsDark };
            }),
            setTheme: (isDark) => {
                if (isDark) {
                    document.documentElement.classList.add('dark');
                } else {
                    document.documentElement.classList.remove('dark');
                }
                set({ isDark });
            },
        }),
        {
            name: 'theme-storage',
        }
    )
);
