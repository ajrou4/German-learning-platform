import { useQuery } from '@tanstack/react-query';
import { BookOpen, Clock } from 'lucide-react';
import { Link } from 'react-router-dom';
import { coursesAPI } from '../services/api';
import { useAuthStore } from '../store/useStore';

export default function Courses() {
    const user = useAuthStore((state) => state.user);

    const { data: courses, isLoading, error } = useQuery({
        queryKey: ['courses'],
        queryFn: () => coursesAPI.list().then((res) => res.data.results),
    });

    console.log('Courses data:', courses, 'Error:', error);

    if (isLoading) {
        return (
            <div className="flex items-center justify-center h-64">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
            </div>
        );
    }

    const levelColors = {
        A1: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
        A2: 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400',
        B1: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400',
        B2: 'bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-400',
        C1: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400',
        C2: 'bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-400',
    };

    return (
        <div className="space-y-6 animate-fade-in">
            <div className="flex items-center justify-between">
                <h1 className="text-3xl font-bold">Courses</h1>
                <div className="badge badge-info">
                    Your Level: {user?.language_level}
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {courses?.map((course) => (
                    <Link
                        key={course.id}
                        to={`/courses/${course.id}`}
                        className="card hover:shadow-xl transition-all hover:scale-105 cursor-pointer"
                    >
                        {course.thumbnail && (
                            <img
                                src={course.thumbnail}
                                alt={course.title}
                                className="w-full h-48 object-cover rounded-lg mb-4"
                            />
                        )}

                        <div className="flex items-center justify-between mb-3">
                            <span className={`badge ${levelColors[course.level]}`}>
                                {course.level}
                            </span>
                            <div className="flex items-center text-sm text-gray-600 dark:text-gray-400">
                                <BookOpen className="w-4 h-4 mr-1" />
                                {course.total_lessons} lessons
                            </div>
                        </div>

                        <h3 className="text-xl font-bold mb-2">{course.title}</h3>
                        <p className="text-gray-600 dark:text-gray-400 line-clamp-2">
                            {course.description}
                        </p>
                    </Link>
                ))}
            </div>

            {courses?.length === 0 && (
                <div className="card text-center py-12">
                    <BookOpen className="w-16 h-16 mx-auto text-gray-400 mb-4" />
                    <h3 className="text-xl font-semibold mb-2">No courses available</h3>
                    <p className="text-gray-600 dark:text-gray-400">
                        Check back later for new courses!
                    </p>
                </div>
            )}
        </div>
    );
}
