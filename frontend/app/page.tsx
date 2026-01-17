'use client';

import { useEffect, useState, useRef } from 'react';

interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

export default function Home() {
  const [theme, setTheme] = useState({
    primary: '#0066cc',
    secondary: '#003366',
    background: '#ffffff',
    font: 'Arial, sans-serif'
  });
  const [mockUser, setMockUser] = useState<string>('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Get theme from URL params
    const params = new URLSearchParams(window.location.search);
    const themeParam = params.get('theme');
    const userParam = params.get('mockUser');

    if (userParam) {
      setMockUser(userParam);
    }

    if (themeParam === 'corporate-blue') {
      setTheme({
        primary: '#003366',
        secondary: '#0066cc',
        background: '#f5f5f5',
        font: 'Arial, sans-serif'
      });
    }

    // Listen for theme messages from parent
    const handleMessage = (event: MessageEvent) => {
      if (event.data.type === 'theme') {
        setTheme({
          primary: event.data.primary || theme.primary,
          secondary: event.data.secondary || theme.secondary,
          background: event.data.background || theme.background,
          font: event.data.font || theme.font
        });
      }
    };

    window.addEventListener('message', handleMessage);
    return () => window.removeEventListener('message', handleMessage);
  }, []);

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/chat/stream', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Mock-User': mockUser || 'anonymous@dept.gov'
        },
        body: JSON.stringify({
          messages: [...messages, userMessage],
          stream: true
        })
      });

      if (!response.ok) throw new Error('Failed to get response');

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      let assistantMessage = '';

      setMessages(prev => [...prev, { role: 'assistant', content: '' }]);

      while (true) {
        const { done, value } = await reader!.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6);
            if (data === '[DONE]') break;
            if (data.startsWith('[ERROR]')) {
              throw new Error(data.slice(8));
            }
            assistantMessage += data;
            setMessages(prev => {
              const newMessages = [...prev];
              newMessages[newMessages.length - 1] = {
                role: 'assistant',
                content: assistantMessage
              };
              return newMessages;
            });
          }
        }
      }
    } catch (error) {
      console.error('Chat error:', error);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `Error: ${error instanceof Error ? error.message : 'Failed to get response'}`
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div 
      className="min-h-screen flex flex-col"
      style={{ 
        backgroundColor: theme.background,
        fontFamily: theme.font 
      }}
    >
      {/* Dev Mode Banner */}
      {mockUser && (
        <div 
          className="text-white text-sm px-4 py-2 text-center font-semibold"
          style={{ backgroundColor: theme.secondary }}
        >
          🔧 DEV MODE - Authenticated as: {mockUser}
        </div>
      )}

      {/* Chat Interface */}
      <div className="flex-1 flex flex-col p-4">
        <div className="flex-1 bg-white rounded-lg shadow-lg overflow-hidden flex flex-col">
          {/* Chat Header */}
          <div 
            className="text-white p-4"
            style={{ backgroundColor: theme.primary }}
          >
            <h2 className="text-xl font-bold">🤖 AI Assistant</h2>
            <p className="text-sm opacity-90">Powered by Ollama (llama3:latest)</p>
          </div>

          {/* Chat Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.length === 0 && (
              <div className="bg-gray-100 rounded-lg p-3 max-w-[80%]">
                <p className="text-sm text-gray-700">
                  👋 Hello! I&apos;m your AI assistant. I can help you with questions about our department.
                </p>
                <p className="mt-2 text-xs text-gray-600 italic">
                  Connected to Ollama at http://localhost:8000
                </p>
              </div>
            )}
            
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`rounded-lg p-3 max-w-[80%] ${
                  msg.role === 'user'
                    ? 'ml-auto text-white'
                    : 'bg-gray-100 text-gray-900'
                }`}
                style={msg.role === 'user' ? { backgroundColor: theme.primary } : {}}
              >
                <p className="text-sm whitespace-pre-wrap">
                  {msg.content || '...'}
                </p>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          {/* Chat Input */}
          <div className="border-t p-4">
            <div className="flex gap-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Type your message..."
                className="flex-1 border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 text-gray-900"
                style={{ 
                  borderColor: theme.primary,
                }}
                disabled={isLoading}
              />
              <button
                onClick={sendMessage}
                className="text-white px-6 py-2 rounded-lg font-semibold disabled:opacity-50"
                style={{ backgroundColor: theme.primary }}
                disabled={isLoading || !input.trim()}
              >
                {isLoading ? '...' : 'Send'}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
