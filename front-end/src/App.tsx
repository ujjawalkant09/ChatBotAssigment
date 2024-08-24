import React from 'react';
import ChatWidget from './components/ChatWidget';
import styles from './App.module.css';

const App: React.FC = () => {
  return (
    <div className={styles.app}>
      <ChatWidget />
    </div>
  );
};

export default App;