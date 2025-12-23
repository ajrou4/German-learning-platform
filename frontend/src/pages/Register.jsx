import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { UserPlus } from 'lucide-react';
import toast from 'react-hot-toast';
import { authAPI } from '../services/api';
import { useAuthStore } from '../store/useStore';

export default function Register() {
    const [formData, setFormData] = useState({
        email: '',
        username: '',
        password: '',
        password_confirm: '',
        first_name: '',
        last_name: '',
        language_level: 'A1',
        native_language: 'EN',
    });
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();
    const setAuth = useAuthStore((state) => state.setAuth);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (formData.password !== formData.password_confirm) {
            toast.error('Passwords do not match');
            return;
        }

        setLoading(true);

        try {
            const response = await authAPI.register(formData);
            const { user, tokens } = response.data;

            setAuth(user, tokens);
            toast.success('Account created successfully!');
            navigate('/');
        } catch (error) {
            const errors = error.response?.data;
            if (errors) {
                Object.keys(errors).forEach((key) => {
                    toast.error(`${key}: ${errors[key]}`);
                });
            } else {
                toast.error('Registration failed');
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-500 via-secondary-500 to-primary-600 p-4">
            <div className="w-full max-w-2xl">
                <div className="card animate-fade-in">
                    <div className="text-center mb-8">
                        <h1 className="text-4xl font-bold text-gradient mb-2">
                            🇩🇪 Join Us
                        </h1>
                        <p className="text-gray-600 dark:text-gray-400">
                            Start your German learning journey
                        </p>
                    </div>

                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <label className="block text-sm font-medium mb-2">First Name</label>
                                <input
                                    type="text"
                                    name="first_name"
                                    value={formData.first_name}
                                    onChange={handleChange}
                                    className="input"
                                    required
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-medium mb-2">Last Name</label>
                                <input
                                    type="text"
                                    name="last_name"
                                    value={formData.last_name}
                                    onChange={handleChange}
                                    className="input"
                                    required
                                />
                            </div>
                        </div>

                        <div>
                            <label className="block text-sm font-medium mb-2">Email</label>
                            <input
                                type="email"
                                name="email"
                                value={formData.email}
                                onChange={handleChange}
                                className="input"
                                required
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium mb-2">Username</label>
                            <input
                                type="text"
                                name="username"
                                value={formData.username}
                                onChange={handleChange}
                                className="input"
                                required
                            />
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <label className="block text-sm font-medium mb-2">Language Level</label>
                                <select
                                    name="language_level"
                                    value={formData.language_level}
                                    onChange={handleChange}
                                    className="input"
                                >
                                    <option value="A1">A1 - Beginner</option>
                                    <option value="A2">A2 - Elementary</option>
                                    <option value="B1">B1 - Intermediate</option>
                                    <option value="B2">B2 - Upper Intermediate</option>
                                    <option value="C1">C1 - Advanced</option>
                                    <option value="C2">C2 - Proficient</option>
                                </select>
                            </div>

                            <div>
                                <label className="block text-sm font-medium mb-2">Native Language</label>
                                <select
                                    name="native_language"
                                    value={formData.native_language}
                                    onChange={handleChange}
                                    className="input"
                                >
                                    <option value="EN">English</option>
                                    <option value="AR">Arabic</option>
                                    <option value="ES">Spanish</option>
                                    <option value="FR">French</option>
                                </select>
                            </div>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <label className="block text-sm font-medium mb-2">Password</label>
                                <input
                                    type="password"
                                    name="password"
                                    value={formData.password}
                                    onChange={handleChange}
                                    className="input"
                                    required
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-medium mb-2">Confirm Password</label>
                                <input
                                    type="password"
                                    name="password_confirm"
                                    value={formData.password_confirm}
                                    onChange={handleChange}
                                    className="input"
                                    required
                                />
                            </div>
                        </div>

                        <button
                            type="submit"
                            disabled={loading}
                            className="btn btn-primary w-full flex items-center justify-center"
                        >
                            {loading ? (
                                'Creating account...'
                            ) : (
                                <>
                                    <UserPlus className="w-5 h-5 mr-2" />
                                    Register
                                </>
                            )}
                        </button>
                    </form>

                    <p className="mt-6 text-center text-sm text-gray-600 dark:text-gray-400">
                        Already have an account?{' '}
                        <Link to="/login" className="text-primary-600 hover:underline font-medium">
                            Login here
                        </Link>
                    </p>
                </div>
            </div>
        </div>
    );
}
