import { useQuery } from '@tanstack/react-query';
import { Flame, Trophy, BookOpen, Clock, TrendingUp } from 'lucide-react';
import { progressAPI } from '../services/api';
import { useAuthStore } from '../store/useStore';
import { Link } from 'react-router-dom';

export default function Dashboard() {
    const user = useAuthStore((state) => state.user);

    const { data: stats, isLoading } = useQuery({
        queryKey: ['dashboard-stats'],
        queryFn: () => progressAPI.getDashboard().then((res) => res.data),
    });

    if (isLoading) {
        return (
            <div className="flex items-center justify-center h-64">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
            </div>
        );
    }

    const statCards = [
        {
            title: 'Current Streak',
            value: stats?.current_streak || 0,
            unit: 'days',
            icon: Flame,
            color: 'text-orange-500',
            bgColor: 'bg-orange-100 dark:bg-orange-900/30',
        },
        {
            title: 'Lessons Completed',
            value: stats?.lessons_completed || 0,
            unit: 'lessons',
            icon: BookOpen,
            color: 'text-green-500',
            bgColor: 'bg-green-100 dark:bg-green-900/30',
        },
        {
            title: 'This Week',
            value: stats?.time_this_week_minutes || 0,
            unit: 'minutes',
            icon: Clock,
            color: 'text-blue-500',
            bgColor: 'bg-blue-100 dark:bg-blue-900/30',
        },
        {
            title: 'Longest Streak',
            value: stats?.longest_streak || 0,
            unit: 'days',
            icon: TrendingUp,
            color: 'text-purple-500',
            bgColor: 'bg-purple-100 dark:bg-purple-900/30',
        },
    ];

    return (
        <div className="space-y-6 animate-fade-in">
            {/* Welcome header */}
            <div className="card">
                <h1 className="text-3xl font-bold mb-2">
                    Welcome back, {user?.first_name || user?.username}! 👋
                </h1>
                <p className="text-gray-600 dark:text-gray-400">
                    You're currently at level <span className="font-bold text-primary-600">{stats?.language_level}</span>
                </p>
            </div>

            {/* Stats grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {statCards.map((stat, index) => (
                    <div key={index} className="card hover:shadow-xl transition-shadow">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                                    {stat.title}
                                </p>
                                <p className="text-3xl font-bold">
                                    {stat.value}
                                    <span className="text-sm font-normal text-gray-500 ml-1">
                                        {stat.unit}
                                    </span>
                                </p>
                            </div>
                            <div className={`p-3 rounded-lg ${stat.bgColor}`}>
                                <stat.icon className={`w-8 h-8 ${stat.color}`} />
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {/* Recent achievements */}
            {stats?.recent_achievements && stats.recent_achievements.length > 0 && (
                <div className="card">
                    <h2 className="text-2xl font-bold mb-4 flex items-center">
                        <Trophy className="w-6 h-6 mr-2 text-yellow-500" />
                        Recent Achievements
                    </h2>
                    <div className="space-y-3">
                        {stats.recent_achievements.map((achievement) => (
                            <div
                                key={achievement.id}
                                className="flex items-center p-3 bg-gray-50 dark:bg-dark-700 rounded-lg"
                            >
                                <span className="text-3xl mr-3">{achievement.icon}</span>
                                <div>
                                    <h3 className="font-semibold">{achievement.title}</h3>
                                    <p className="text-sm text-gray-600 dark:text-gray-400">
                                        {achievement.description}
                                    </p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Quick actions */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Link
                    to="/courses"
                    className="card hover:shadow-xl transition-all hover:scale-105 cursor-pointer"
                >
                    <BookOpen className="w-12 h-12 text-primary-600 mb-4" />
                    <h3 className="text-xl font-bold mb-2">Browse Courses</h3>
                    <p className="text-gray-600 dark:text-gray-400">
                        Explore lessons for your level
                    </p>
                </Link>

                <Link
                    to="/chat"
                    className="card hover:shadow-xl transition-all hover:scale-105 cursor-pointer"
                >
                    <svg className="w-12 h-12 text-secondary-500 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                    </svg>
                    <h3 className="text-xl font-bold mb-2">AI Tutor</h3>
                    <p className="text-gray-600 dark:text-gray-400">
                        Practice with AI chatbot
                    </p>
                </Link>

                <Link
                    to="/translator"
                    className="card hover:shadow-xl transition-all hover:scale-105 cursor-pointer"
                >
                    <svg className="w-12 h-12 text-green-500 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129" />
                    </svg>
                    <h3 className="text-xl font-bold mb-2">Translator</h3>
                    <p className="text-gray-600 dark:text-gray-400">
                        Translate with AI explanations
                    </p>
                </Link>
            </div>
        </div>
    );
}
