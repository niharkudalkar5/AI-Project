import React from 'react';

function StatusBar({ status, llmStatus }) {
  const getStatusColor = (s) => {
    switch (s) {
      case 'ready':
        return 'text-green-400';
      case 'initializing':
      case 'bootstrapping':
        return 'text-yellow-400';
      case 'error':
        return 'text-red-400';
      default:
        return 'text-slate-400';
    }
  };

  const getStatusIndicator = (s) => {
    switch (s) {
      case 'ready':
        return '●';
      case 'initializing':
      case 'bootstrapping':
        return '⟳';
      case 'error':
        return '✕';
      default:
        return '○';
    }
  };

  const llmConnected = llmStatus?.connected;

  return (
    <div className="flex items-center gap-4 text-sm">
      {/* App Status */}
      <div className="flex items-center gap-2">
        <span className={getStatusColor(status)}>
          {getStatusIndicator(status)}
        </span>
        <span className="text-slate-300 capitalize">
          {status === 'initializing'
            ? 'Initializing...'
            : status === 'bootstrapping'
            ? 'Bootstrapping...'
            : status === 'ready'
            ? 'Ready'
            : 'Error'}
        </span>
      </div>

      {/* LLM Status */}
      {llmStatus && (
        <div className="flex items-center gap-2 pl-4 border-l border-slate-600">
          <span className={llmConnected ? 'text-green-400' : 'text-red-400'}>
            {llmConnected ? '●' : '✕'}
          </span>
          <span className="text-slate-300">
            {llmConnected ? 'LLM Connected' : 'LLM Offline'}
          </span>
        </div>
      )}
    </div>
  );
}

export default StatusBar;
