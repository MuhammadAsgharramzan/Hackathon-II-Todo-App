'use client';

import { useState, useRef, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { apiClient } from '@/lib/api';

interface Message {
  id?: number;
  role: 'user' | 'assistant';
  content: string;
  createdAt?: string;
}

interface ToolCall {
  tool_name: string;
  arguments: Record<string, any>;
  result: any;
}

interface ChatResponse {
  conversation_id: number;
  assistant_response: string;
  tool_calls?: ToolCall[];
}

interface ChatProps {
  userId: string;
}

export default function ChatInterface({ userId }: ChatProps) {
  const router = useRouter();
  const [inputMessage, setInputMessage] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [currentConversationId, setCurrentConversationId] = useState<number | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom of messages when they change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!inputMessage.trim() || isLoading) return;

    // Add user message to the chat
    const userMessage: Message = {
      role: 'user',
      content: inputMessage,
      createdAt: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      // Send message to the chat API
      const response: ChatResponse = await apiClient.request('/chat', {
        method: 'POST',
        body: JSON.stringify({
          conversation_id: currentConversationId || undefined,
          message: inputMessage,
        }),
      });

      // Update conversation ID if it's the first message
      if (!currentConversationId && response.conversation_id) {
        setCurrentConversationId(response.conversation_id);
      }

      // Add assistant response to the chat
      const assistantMessage: Message = {
        role: 'assistant',
        content: response.assistant_response,
        createdAt: new Date().toISOString(),
      };

      setMessages(prev => [...prev, assistantMessage]);

      // Visualize tool calls in the chat interface
      if (response.tool_calls && response.tool_calls.length > 0) {
        // Add a subtle indicator that tools were executed
        const toolIndicator: Message = {
          role: 'assistant',
          content: `🔧 ${response.tool_calls.length} tool(s) executed successfully`,
          createdAt: new Date().toISOString(),
        };

        // Add the tool indicator message briefly, then remove it after 2 seconds
        setMessages(prev => [...prev, toolIndicator]);
        setTimeout(() => {
          setMessages(prev => prev.filter(msg => msg.content !== toolIndicator.content));
        }, 2000);
      }
    } catch (error: any) {
      if (error.message && error.message.includes('Unauthorized')) {
        // If unauthorized, redirect to login
        localStorage.removeItem('authToken');
        router.push('/login');
      } else {
        console.error('Error sending message:', error);

      // Add error message to chat
      const errorMessage: Message = {
        role: 'assistant',
        content: '❌ Sorry, I encountered an error processing your request. Please try again.',
        createdAt: new Date().toISOString(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="border border-gray-200 rounded-lg shadow-sm bg-white">
      <div className="p-4 border-b border-gray-200">
        <h3 className="text-lg font-medium text-gray-900">AI Assistant</h3>
        <p className="text-sm text-gray-500">Manage your tasks using natural language</p>
      </div>

      <div className="h-96 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <p>Start a conversation with the AI assistant to manage your tasks.</p>
            <p className="mt-2 text-sm">Try: "Add a task to buy groceries" or "Show my tasks"</p>
          </div>
        ) : (
          messages.map((msg, index) => (
            <div
              key={index}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                  msg.role === 'user'
                    ? 'bg-indigo-600 text-white'
                    : msg.content.startsWith('❌')
                      ? 'bg-red-100 text-red-800'
                      : msg.content.startsWith('🔧')
                        ? 'bg-blue-100 text-blue-800 italic'
                        : 'bg-gray-100 text-gray-800'
                }`}
              >
                <div className="whitespace-pre-wrap">{msg.content}</div>
                {msg.createdAt && (
                  <div
                    className={`text-xs mt-1 ${
                      msg.role === 'user'
                        ? 'text-indigo-200'
                        : msg.content.startsWith('❌')
                          ? 'text-red-500'
                          : msg.content.startsWith('🔧')
                            ? 'text-blue-500'
                            : 'text-gray-500'
                    }`}
                  >
                    {new Date(msg.createdAt).toLocaleTimeString([], {
                      hour: '2-digit',
                      minute: '2-digit',
                    })}
                  </div>
                )}
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 text-gray-800 max-w-xs lg:max-w-md px-4 py-2 rounded-lg">
              <div className="flex items-center space-x-2">
                <span>Thinking...</span>
                <div className="flex space-x-1">
                  <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce"></div>
                  <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce delay-75"></div>
                  <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce delay-150"></div>
                </div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="p-4 border-t border-gray-200">
        <div className="flex space-x-2">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Type a message to manage your tasks..."
            className="flex-1 border border-gray-300 rounded-md px-3 py-2 text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={!inputMessage.trim() || isLoading}
            className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Send
          </button>
        </div>
        <p className="mt-2 text-xs text-gray-500">
          Examples: "Add task: Buy groceries", "Show my tasks", "Complete task 1"
        </p>
      </form>
    </div>
  );
}