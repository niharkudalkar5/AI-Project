import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ChatPanel from './components/ChatPanel';
import RepositorySidebar from './components/RepositorySidebar';
import StatusBar from './components/StatusBar';
import './App.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

function App() {
  const [status, setStatus] = useState('initializing');
  const [llmStatus, setLlmStatus] = useState(null);
  const [repositories, setRepositories] = useState([]);
  const [selectedRepo, setSelectedRepo] = useState(null);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    initializeApp();
  }, []);

  const initializeApp = async () => {
    try {
      setStatus('bootstrapping');
      
      // Check system health
      const healthRes = await axios.get(`${API_BASE_URL}/health`);
      console.log('Health check:', healthRes.data);
      
      // Check LLM connection
      const llmRes = await axios.get(`${API_BASE_URL}/health/llm`);
      setLlmStatus(llmRes.data);
      
      // Scan workspace
      const scanRes = await axios.post(`${API_BASE_URL}/workspace/scan`);
      setRepositories(scanRes.data.modules || []);
      
      setStatus('ready');
      setMessages([{
        id: 1,
        role: 'system',
        content: 'Standalone Local LLM Workspace initialized successfully!'
      }]);
    } catch (error) {
      console.error('Initialization failed:', error);
      setStatus('error');
      setMessages([{
        id: 1,
        role: 'error',
        content: `Initialization error: ${error.message}`
      }]);
    }
  };

  const handleSendMessage = async (message, intent = 'chat') => {
    try {
      setLoading(true);
      const newMessage = {
        id: Date.now(),
        role: 'user',
        content: message
      };

      setMessages((prev) => [...prev, newMessage]);

      const response = await axios.post(`${API_BASE_URL}/chat`, {
        message,
        context: selectedRepo ? `Repository: ${selectedRepo.name}` : '',
        intent
      });

      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          role: 'assistant',
          content: response.data?.response || 'No response received from the API'
        }
      ]);
    } catch (error) {
      console.error('Chat failed:', error);
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 2,
          role: 'error',
          content: `Error: ${error.message}`
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleScanWorkspace = async () => {
    try {
      setLoading(true);
      const response = await axios.post(`${API_BASE_URL}/workspace/scan`);
      setRepositories(response.data.modules || []);
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 3,
          role: 'system',
          content: `Found ${response.data.count} repositories in workspace`
        }
      ]);
    } catch (error) {
      console.error('Workspace scan failed:', error);
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 4,
          role: 'error',
          content: `Workspace scan failed: ${error.message}`
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-slate-900 text-slate-100">
      {/* Header */}
      <header className="bg-gradient-to-r from-blue-900 to-purple-900 border-b border-slate-700 px-6 py-4 shadow-lg">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold">Standalone Local LLM Workspace</h1>
            <p className="text-sm text-slate-300 mt-1">v0.1.0</p>
          </div>
          <StatusBar status={status} llmStatus={llmStatus} />
        </div>
      </header>

      {/* Main Content Area */}
      <div className="flex flex-1 overflow-hidden gap-0">
        {/* Left Sidebar - Repositories */}
        <RepositorySidebar
          repositories={repositories}
          selectedRepo={selectedRepo}
          onSelectRepo={setSelectedRepo}
          onScan={handleScanWorkspace}
          loading={loading}
        />

        {/* Center Panel - Chat */}
        <ChatPanel
          messages={messages}
          onSendMessage={handleSendMessage}
          loading={loading}
          selectedRepo={selectedRepo}
        />

        {/* Right Panel - Details */}
        <aside className="w-64 bg-slate-800 border-l border-slate-700 p-4 overflow-y-auto">
          <div>
            <h3 className="text-lg font-semibold mb-4 text-slate-100">Details</h3>
            
            {selectedRepo ? (
              <div className="space-y-4 text-sm">
                <div>
                  <label className="text-slate-400 text-xs uppercase font-semibold">Repository</label>
                  <p className="text-slate-100 font-mono">{selectedRepo.name}</p>
                </div>
                <div>
                  <label className="text-slate-400 text-xs uppercase font-semibold">Type</label>
                  <p className="text-slate-100">{selectedRepo.type || 'Unknown'}</p>
                </div>
                <div>
                  <label className="text-slate-400 text-xs uppercase font-semibold">Language</label>
                  <p className="text-slate-100">{selectedRepo.language || 'N/A'}</p>
                </div>
                <div>
                  <label className="text-slate-400 text-xs uppercase font-semibold">Files</label>
                  <p className="text-slate-100">{selectedRepo.files?.length || 0}</p>
                </div>
              </div>
            ) : (
              <p className="text-slate-400 text-center py-8">Select a repository to view details</p>
            )}

            <hr className="border-slate-700 my-4" />

            <div>
              <h4 className="font-semibold mb-3 text-slate-100">LLM Configuration</h4>
              {llmStatus && (
                <div className="space-y-2 text-sm">
                  <div>
                    <label className="text-slate-400 text-xs uppercase font-semibold">Status</label>
                    <p className={llmStatus.connected ? 'text-green-400' : 'text-red-400'}>
                      {llmStatus.connected ? '✓ Connected' : '✗ Disconnected'}
                    </p>
                  </div>
                  <div>
                    <label className="text-slate-400 text-xs uppercase font-semibold">Model</label>
                    <p className="text-slate-100 font-mono text-xs">{llmStatus.active_model}</p>
                  </div>
                  <div>
                    <label className="text-slate-400 text-xs uppercase font-semibold">Adapter</label>
                    <p className="text-slate-100 capitalize">{llmStatus.adapter}</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </aside>
      </div>
    </div>
  );
}

export default App;
