import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor to add auth token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                const refreshToken = localStorage.getItem('refresh_token');
                const response = await axios.post(`${API_URL}/auth/token/refresh/`, {
                    refresh: refreshToken,
                });

                const { access } = response.data;
                localStorage.setItem('access_token', access);

                originalRequest.headers.Authorization = `Bearer ${access}`;
                return api(originalRequest);
            } catch (refreshError) {
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                window.location.href = '/login';
                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
);

// Auth API
export const authAPI = {
    register: (data) => api.post('/auth/register/', data),
    login: (data) => api.post('/auth/login/', data),
    getProfile: () => api.get('/auth/profile/'),
    updateProfile: (data) => api.patch('/auth/profile/', data),
    getStats: () => api.get('/auth/stats/'),
};

// Courses API
export const coursesAPI = {
    list: (params) => api.get('/courses/', { params }),
    get: (id) => api.get(`/courses/${id}/`),
    getModule: (id) => api.get(`/courses/modules/${id}/`),
};

// Lessons API
export const lessonsAPI = {
    list: (params) => api.get('/lessons/', { params }),
    get: (id) => api.get(`/lessons/${id}/`),
    complete: (id) => api.post(`/lessons/${id}/complete/`),
    submitExercise: (data) => api.post('/lessons/exercises/submit/', data),
};

// Progress API
export const progressAPI = {
    list: () => api.get('/progress/'),
    get: (id) => api.get(`/progress/${id}/`),
    getStreak: () => api.get('/progress/streak/'),
    getAchievements: () => api.get('/progress/achievements/'),
    getDashboard: () => api.get('/progress/dashboard/'),
};

// AI API
export const aiAPI = {
    translate: (data) => api.post('/ai/translate/', data),
    generateSentences: (data) => api.post('/ai/generate-sentences/', data),
    speechToText: (formData) =>
        api.post('/ai/speech-to-text/', formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
        }),
    textToSpeech: (data) => api.post('/ai/text-to-speech/', data),
    checkPronunciation: (formData) =>
        api.post('/ai/pronunciation/', formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
        }),
};

// Chat API
export const chatAPI = {
    listSessions: () => api.get('/chat/sessions/'),
    getSession: (id) => api.get(`/chat/sessions/${id}/`),
    createSession: (data) => api.post('/chat/sessions/', data),
    sendMessage: (data) => api.post('/chat/send/', data),
    clearSession: (id) => api.delete(`/chat/sessions/${id}/clear/`),
};

export default api;
