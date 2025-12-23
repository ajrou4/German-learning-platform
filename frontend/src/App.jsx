import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuthStore } from './store/useStore';
import Layout from './components/Layout';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Courses from './pages/Courses';
import LessonViewer from './pages/LessonViewer';
import AIChat from './pages/AIChat';
import Translator from './pages/Translator';
import Profile from './pages/Profile';

// Protected Route wrapper
const ProtectedRoute = ({ children }) => {
    const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
    return isAuthenticated ? children : <Navigate to="/login" />;
};

function App() {
    return (
        <Routes>
            {/* Public routes */}
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />

            {/* Protected routes */}
            <Route
                path="/"
                element={
                    <ProtectedRoute>
                        <Layout />
                    </ProtectedRoute>
                }
            >
                <Route index element={<Dashboard />} />
                <Route path="courses" element={<Courses />} />
                <Route path="lessons/:id" element={<LessonViewer />} />
                <Route path="chat" element={<AIChat />} />
                <Route path="translator" element={<Translator />} />
                <Route path="profile" element={<Profile />} />
            </Route>

            {/* Catch all */}
            <Route path="*" element={<Navigate to="/" />} />
        </Routes>
    );
}

export default App;
