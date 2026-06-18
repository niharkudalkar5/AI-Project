import React, { useState, useRef, useEffect } from 'react';

function ChatPanel({ messages, onSendMessage, loading, selectedRepo }) {
  const [inputValue, setInputValue] = useState('');
  const [intent, setIntent] = useState('chat');
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputValue.trim() && !loading) {
      onSendMessage(inputValue, intent);
      setInputValue('');
    }
  };

  return (
    <div className="flex flex-col flex-1 bg-slate-950">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${
              msg.role === 'user' ? 'justify-end' : 'justify-start'
            }`}
          >
            <div
              className={`max-w-md px-4 py-2 rounded-lg ${
                msg.role === 'user'
                  ? 'bg-blue-600 text-white'
                  : msg.role === 'error'
                  ? 'bg-red-900 text-red-100'
                  : 'bg-slate-700 text-slate-100'
              }`}
            >
              <p className="text-sm">{msg.content}</p>
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-slate-700 px-4 py-2 rounded-lg">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="border-t border-slate-700 bg-slate-900 p-4 space-y-3">
        <div className="flex gap-2">
          <select
            value={intent}
            onChange={(e) => setIntent(e.target.value)}
            className="px-3 py-2 bg-slate-800 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-500"
          >
            <option value="chat">Chat</option>
            <option value="review">Code Review</option>
            <option value="modify">Modify Code</option>
            <option value="build">Build</option>
          </select>
          {selectedRepo && (
            <div className="px-3 py-2 bg-slate-800 text-slate-300 text-sm rounded">
              📦 {selectedRepo.name}
            </div>
          )}
        </div>

        <form onSubmit={handleSubmit} className="flex gap-2">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Ask me anything about your code..."
            className="flex-1 px-4 py-2 bg-slate-800 border border-slate-600 rounded text-slate-100 placeholder-slate-500 focus:outline-none focus:border-blue-500"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading || !inputValue.trim()}
            className="px-6 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-600 text-white rounded font-medium transition-colors"
          >
            {loading ? '...' : 'Send'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default ChatPanel;
