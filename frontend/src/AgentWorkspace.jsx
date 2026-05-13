import React from 'react';

const AgentWorkspace = ({ agentData }) => {
  const { wallpaper, themeColor, name, role } = agentData;

  const style = {
    backgroundImage: `url(${wallpaper})`,
    backgroundSize: 'cover',
    border: `2px solid ${themeColor}`,
  };

  return (
    <div className="workspace-container" style={style}>
      <header className="glass-morphism">
        <h2>{name} <small>({role})</small></h2>
        <div className="status-indicator">Online</div>
      </header>

      <div className="terminal-emulator">
        {/* This would connect to the Docker container via WebSockets */}
        <code>$ nexus_forge --status</code>
      </div>

      <div className="agent-collaboration-feed">
        <p><strong>DevAgent:</strong> "I've updated the API. @DesignAgent, check the layout."</p>
      </div>
    </div>
  );
};