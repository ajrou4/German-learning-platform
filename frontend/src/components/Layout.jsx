import { Outlet, Link, useNavigate } from 'react-router-dom';
import {
    Home, BookOpen, MessageCircle, Languages, User,
    LogOut, Moon, Sun, Menu, X
} from 'lucide-react';
import { useState } from 'react';
import { useAuthStore, useThemeStore } from '../store/useStore';

export default function Layout() {
    const [sidebarOpen, setSidebarOpen] = useState(false);
    const navigate = useNavigate();
    const logout = useAuthStore((state) => state.logout);
    const user = useAuthStore((state) => state.user);
    const { isDark, toggleTheme } = useThemeStore();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    const navigation = [
        { name: 'Dashboard', href: '/', icon: Home },
        { name: 'Courses', href: '/courses', icon: BookOpen },
        { name: 'AI Chat', href: '/chat', icon: MessageCircle },
        { name: 'Translator', href: '/translator', icon: Languages },
        { name: 'Profile', href: '/profile', icon: User },
    ];

    return (
        <div className="min-h-screen flex">
            {/* Sidebar */}
            <aside
                className={`fixed inset-y-0 left-0 z-50 w-64 bg-white dark:bg-dark-800 border-r border-gray-200 dark:border-dark-700 transform transition-transform duration-200 ease-in-out lg:translate-x-0 ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'
                    }`}
            >
                <div className="flex flex-col h-full">
                    {/* Logo */}
                    <div className="flex items-center justify-between h-16 px-6 border-b border-gray-200 dark:border-dark-700">
                        <h1 className="text-xl font-bold text-gradient">
                            🇩🇪 Deutsch Lernen
                        </h1>
                        <button
                            onClick={() => setSidebarOpen(false)}
                            className="lg:hidden"
                        >
                            <X className="w-6 h-6" />
                        </button>
                    </div>

                    {/* Navigation */}
                    <nav className="flex-1 px-4 py-6 space-y-2 overflow-y-auto">
                        {navigation.map((item) => (
                            <Link
                                key={item.name}
                                to={item.href}
                                onClick={() => setSidebarOpen(false)}
                                className="flex items-center px-4 py-3 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-dark-700 transition-colors"
                            >
                                <item.icon className="w-5 h-5 mr-3" />
                                {item.name}
                            </Link>
                        ))}
                    </nav>

                    {/* User info & logout */}
                    <div className="p-4 border-t border-gray-200 dark:border-dark-700">
                        <div className="flex items-center mb-3">
                            <div className="w-10 h-10 rounded-full bg-primary-500 flex items-center justify-center text-white font-bold">
                                {user?.email?.[0]?.toUpperCase() || 'U'}
                            </div>
                            <div className="ml-3 flex-1">
                                <p className="text-sm font-medium">{user?.email}</p>
                                <p className="text-xs text-gray-500">Level: {user?.language_level || 'A1'}</p>
                            </div>
                        </div>
                        <button
                            onClick={handleLogout}
                            className="w-full flex items-center px-4 py-2 text-red-600 dark:text-red-400 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
                        >
                            <LogOut className="w-5 h-5 mr-3" />
                            Logout
                        </button>
                    </div>
                </div>
            </aside>

            {/* Main content */}
            <div className="flex-1 lg:ml-64">
                {/* Top bar */}
                <header className="h-16 bg-white dark:bg-dark-800 border-b border-gray-200 dark:border-dark-700 flex items-center justify-between px-6">
                    <button
                        onClick={() => setSidebarOpen(true)}
                        className="lg:hidden"
                    >
                        <Menu className="w-6 h-6" />
                    </button>

                    <div className="flex-1" />

                    {/* Theme toggle */}
                    <button
                        onClick={toggleTheme}
                        className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-dark-700 transition-colors"
                    >
                        {isDark ? (
                            <Sun className="w-5 h-5" />
                        ) : (
                            <Moon className="w-5 h-5" />
                        )}
                    </button>
                </header>

                {/* Page content */}
                <main className="p-6">
                    <Outlet />
                </main>
            </div>

            {/* Overlay for mobile */}
            {sidebarOpen && (
                <div
                    className="fixed inset-0 bg-black/50 z-40 lg:hidden"
                    onClick={() => setSidebarOpen(false)}
                />
            )}
        </div>
    );
}
