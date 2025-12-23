import { useState } from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';
import { Send, Loader } from 'lucide-react';
import toast from 'react-hot-toast';
import { chatAPI } from '../services/api';

export default function AIChat() {
    const [message, setMessage] = useState('');
    const [currentSessionId, setCurrentSessionId] = useState(null);
    const [mode, setMode] = useState('BEGINNER');
    const [messages, setMessages] = useState([]);

    const sendMutation = useMutation({
        mutationFn: (data) => chatAPI.sendMessage(data),
        onSuccess: (response) => {
            const { user_message, ai_response, session_id } = response.data;
            setCurrentSessionId(session_id);
            setMessages((prev) => [...prev, user_message, ai_response]);
            setMessage('');
        },
        onError: () => {
            toast.error('Failed to send message');
        },
    });

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!message.trim()) return;

        sendMutation.mutate({
            message,
            mode,
            session_id: currentSessionId,
        });
    };

    return (
        <div className="space-y-6 animate-fade-in">
            <div className="flex items-center justify-between">
                <h1 className="text-3xl font-bold">AI German Tutor 🤖</h1>

                <select
                    value={mode}
                    onChange={(e) => setMode(e.target.value)}
                    className="input w-auto"
                >
                    <option value="BEGINNER">Beginner Mode</option>
                    <option value="GRAMMAR">Grammar Explanation</option>
                    <option value="CONVERSATION">Conversation Practice</option>
                </select>
            </div>

            <div className="card h-[600px] flex flex-col">
                {/* Messages */}
                <div className="flex-1 overflow-y-auto space-y-4 mb-4">
                    {messages.length === 0 ? (
                        <div className="text-center py-12 text-gray-500">
                            <p className="text-lg mb-2">👋 Hallo! How can I help you today?</p>
                            <p className="text-sm">Ask me anything about German!</p>
                        </div>
                    ) : (
                        messages.map((msg, index) => (
                            <div
                                key={index}
                                className={`flex ${msg.role === 'USER' ? 'justify-end' : 'justify-start'}`}
                            >
                                <div
                                    className={`max-w-[70%] p-4 rounded-lg ${msg.role === 'USER'
                                            ? 'bg-primary-600 text-white'
                                            : 'bg-gray-100 dark:bg-dark-700'
                                        }`}
                                >
                                    <p className="whitespace-pre-wrap">{msg.content}</p>
                                </div>
                            </div>
                        ))
                    )}

                    {sendMutation.isPending && (
                        <div className="flex justify-start">
                            <div className="bg-gray-100 dark:bg-dark-700 p-4 rounded-lg">
                                <Loader className="w-5 h-5 animate-spin" />
                            </div>
                        </div>
                    )}
                </div>

                {/* Input */}
                <form onSubmit={handleSubmit} className="flex gap-2">
                    <input
                        type="text"
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        placeholder="Type your message in German or English..."
                        className="input flex-1"
                        disabled={sendMutation.isPending}
                    />
                    <button
                        type="submit"
                        disabled={sendMutation.isPending || !message.trim()}
                        className="btn btn-primary"
                    >
                        <Send className="w-5 h-5" />
                    </button>
                </form>
            </div>
        </div>
    );
}
