import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { ArrowRightLeft, Loader } from 'lucide-react';
import toast from 'react-hot-toast';
import { aiAPI } from '../services/api';

export default function Translator() {
    const [text, setText] = useState('');
    const [sourceLang, setSourceLang] = useState('de');
    const [targetLang, setTargetLang] = useState('en');
    const [result, setResult] = useState(null);

    const translateMutation = useMutation({
        mutationFn: (data) => aiAPI.translate(data),
        onSuccess: (response) => {
            setResult(response.data);
        },
        onError: () => {
            toast.error('Translation failed');
        },
    });

    const handleTranslate = () => {
        if (!text.trim()) {
            toast.error('Please enter text to translate');
            return;
        }

        translateMutation.mutate({
            text,
            source_lang: sourceLang,
            target_lang: targetLang,
        });
    };

    const swapLanguages = () => {
        setSourceLang(targetLang);
        setTargetLang(sourceLang);
        setText(result?.translation || '');
        setResult(null);
    };

    return (
        <div className="space-y-6 animate-fade-in">
            <h1 className="text-3xl font-bold">AI Translator 🌐</h1>

            <div className="card">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                    {/* Source */}
                    <div>
                        <label className="block text-sm font-medium mb-2">From</label>
                        <select
                            value={sourceLang}
                            onChange={(e) => setSourceLang(e.target.value)}
                            className="input mb-3"
                        >
                            <option value="de">German</option>
                            <option value="en">English</option>
                            <option value="ar">Arabic</option>
                        </select>
                        <textarea
                            value={text}
                            onChange={(e) => setText(e.target.value)}
                            placeholder="Enter text to translate..."
                            className="input min-h-[200px] resize-none"
                        />
                    </div>

                    {/* Target */}
                    <div>
                        <div className="flex items-center justify-between mb-2">
                            <label className="block text-sm font-medium">To</label>
                            <button
                                onClick={swapLanguages}
                                className="p-2 hover:bg-gray-100 dark:hover:bg-dark-700 rounded-lg transition-colors"
                                title="Swap languages"
                            >
                                <ArrowRightLeft className="w-5 h-5" />
                            </button>
                        </div>
                        <select
                            value={targetLang}
                            onChange={(e) => setTargetLang(e.target.value)}
                            className="input mb-3"
                        >
                            <option value="en">English</option>
                            <option value="de">German</option>
                            <option value="ar">Arabic</option>
                        </select>
                        <div className="input min-h-[200px] bg-gray-50 dark:bg-dark-700">
                            {translateMutation.isPending ? (
                                <div className="flex items-center justify-center h-full">
                                    <Loader className="w-8 h-8 animate-spin text-primary-600" />
                                </div>
                            ) : result ? (
                                <p className="whitespace-pre-wrap">{result.translation}</p>
                            ) : (
                                <p className="text-gray-400">Translation will appear here...</p>
                            )}
                        </div>
                    </div>
                </div>

                <button
                    onClick={handleTranslate}
                    disabled={translateMutation.isPending || !text.trim()}
                    className="btn btn-primary w-full"
                >
                    {translateMutation.isPending ? 'Translating...' : 'Translate'}
                </button>
            </div>

            {/* Grammar explanation */}
            {result && (
                <div className="card animate-slide-up">
                    <h2 className="text-xl font-bold mb-4">Grammar Explanation</h2>
                    <p className="text-gray-700 dark:text-gray-300 mb-6">
                        {result.grammar_explanation}
                    </p>

                    {result.word_breakdown && result.word_breakdown.length > 0 && (
                        <>
                            <h3 className="text-lg font-semibold mb-3">Word Breakdown</h3>
                            <div className="space-y-2">
                                {result.word_breakdown.map((word, index) => (
                                    <div
                                        key={index}
                                        className="p-3 bg-gray-50 dark:bg-dark-700 rounded-lg"
                                    >
                                        <p className="font-semibold">{word.word}</p>
                                        <p className="text-sm text-gray-600 dark:text-gray-400">
                                            {word.meaning}
                                        </p>
                                        {word.grammar_note && (
                                            <p className="text-xs text-primary-600 mt-1">
                                                {word.grammar_note}
                                            </p>
                                        )}
                                    </div>
                                ))}
                            </div>
                        </>
                    )}
                </div>
            )}
        </div>
    );
}
