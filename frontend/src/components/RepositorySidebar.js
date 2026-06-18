import React from 'react';

function RepositorySidebar({ repositories, selectedRepo, onSelectRepo, onScan, loading }) {
  return (
    <aside className="w-64 bg-slate-800 border-r border-slate-700 flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-slate-700">
        <h2 className="text-lg font-semibold text-slate-100 mb-3">Repositories</h2>
        <button
          onClick={onScan}
          disabled={loading}
          className="w-full px-3 py-2 bg-green-600 hover:bg-green-700 disabled:bg-slate-600 text-white text-sm font-medium rounded transition-colors"
        >
          {loading ? 'Scanning...' : '🔄 Scan Workspace'}
        </button>
      </div>

      {/* Repository List */}
      <div className="flex-1 overflow-y-auto">
        {repositories.length === 0 ? (
          <div className="p-4 text-center text-slate-400 text-sm">
            No repositories found. Copy modules to workspace/modules/
          </div>
        ) : (
          <div className="space-y-2 p-2">
            {repositories.map((repo, idx) => (
              <button
                key={idx}
                onClick={() => onSelectRepo(repo)}
                className={`w-full text-left px-3 py-2 rounded text-sm transition-colors ${
                  selectedRepo?.name === repo.name
                    ? 'bg-blue-600 text-white'
                    : 'bg-slate-700 text-slate-100 hover:bg-slate-600'
                }`}
              >
                <div className="font-semibold truncate">{repo.name}</div>
                <div className="text-xs opacity-75 truncate">
                  {repo.language || repo.type || 'Unknown'}
                </div>
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Footer Info */}
      <div className="p-4 border-t border-slate-700 text-xs text-slate-400">
        <div>{repositories.length} repositories</div>
        <div className="mt-2 text-slate-500">
          Workspace: workspace/modules/
        </div>
      </div>
    </aside>
  );
}

export default RepositorySidebar;
