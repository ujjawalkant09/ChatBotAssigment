import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import styles from './ChatWidget.module.css';
import botAvatar from '../bot.png';
var behost = "http://127.0.0.1:8000";

interface Message {
  id: number;
  content: string;
  is_user: boolean;
}

const ChatWidget: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [editMessageId, setEditMessageId] = useState<number | null>(null);
  const [editMessageContent, setEditMessageContent] = useState<string>('');
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  useEffect(() => {
    fetchMessages();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const fetchMessages = async () => {
    try {
      const response = await axios.get(`${behost}/messages`);
      setMessages([
        { id: 0, content: "Welcome to the chatbot! How can I assist you today?", is_user: false },
        ...response.data
      ]);
    } catch (error) {
      console.error('Error fetching messages:', error);
    }
  };

  const sendMessage = async () => {
    if (inputMessage.trim() === '') return;
    try {
      const response = await axios.post(`${behost}/messages`, { content: inputMessage });
      setMessages(prevMessages => [...prevMessages, ...response.data]);
      setInputMessage('');
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  const deleteMessage = async (id: number) => {
    try {
      await axios.delete(`${behost}/messages/${id}`);
      fetchMessages();
    } catch (error) {
      console.error('Error deleting message:', error);
    }
  };

  const startEditing = (id: number, content: string) => {
    setEditMessageId(id);
    setEditMessageContent(content);
  };

  const saveMessage = async (id: number) => {
    try {
      await axios.put(`${behost}/messages/${id}`, { content: editMessageContent });
      setEditMessageId(null);
      fetchMessages();
    } catch (error) {
      console.error('Error editing message:', error);
    }
  };

  return (
    <div className={styles.chatWidget}>
      <div className={styles.botInfo}>
        <img src={botAvatar} alt="Bot" className={styles.botAvatar} />
        <h2>Hey👋, I'm ChatBot</h2>
        <p>Ask me anything </p>
      </div>
      <div className={styles.messages}>
        {messages.map((message) => (
          <div key={message.id} className={`${styles.message} ${message.is_user ? styles.user : styles.bot}`}>
            {!message.is_user && (
              <img src={botAvatar} alt="Bot" className={styles.messageBotAvatar} />
            )}
            <div className={styles.messageContent}>
              {editMessageId === message.id ? (
                <div className={styles.editContainer}>
                  <input
                    className={styles.editInput}
                    type="text"
                    value={editMessageContent}
                    onChange={(e) => setEditMessageContent(e.target.value)}
                  />
                  <div className={styles.editActions}>
                    <button className={styles.saveButton} onClick={() => saveMessage(message.id)}>Save</button>
                    <button className={styles.cancelButton} onClick={() => setEditMessageId(null)}>Cancel</button>
                  </div>
                </div>
              ) : (
                <>
                  <p>{message.content}</p>
                  {message.is_user && (
                    <div className={styles.actions}>
                      <button className={styles.editButton} onClick={() => startEditing(message.id, message.content)}>Edit</button>
                      <button className={styles.deleteButton} onClick={() => deleteMessage(message.id)}>Delete</button>
                    </div>
                  )}
                </>
              )}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <div className={styles.inputArea}>
        <input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Your question"
        />
        <button onClick={sendMessage}>Send</button>
      </div>
      </div>
  
  );
};

export default ChatWidget;