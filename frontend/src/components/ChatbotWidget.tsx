import React, { useState, useRef, useEffect } from 'react';
import clsx from 'clsx';
import styles from './ChatbotWidget.module.css';
import VoiceInput from './VoiceInput';

type Message = {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
};

type ChatbotWidgetProps = {
  sessionId?: string;
  initialContext?: string;
  onSendMessage?: (message: string, sessionId: string) => Promise<any>;
};

const ChatbotWidget: React.FC<ChatbotWidgetProps> = ({
  sessionId: propSessionId,
  initialContext = '',
  onSendMessage,
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string>(propSessionId || '');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    // Add user message to the conversation
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // If we don't have a session ID, create a new one
      if (!sessionId) {
        // In a real app, this would call the backend to create a new session
        const newSessionId = `session_${Date.now()}`;
        setSessionId(newSessionId);
      }

      // Call the provided function to send the message to the backend
      if (onSendMessage) {
        const response = await onSendMessage(inputValue, sessionId);

        // Add bot response to the conversation
        const botMessage: Message = {
          id: Date.now().toString(),
          role: 'assistant',
          content: response.response || 'I received your message.',
          timestamp: new Date(),
        };

        setMessages(prev => [...prev, botMessage]);
      } else {
        // Fallback behavior if no onSendMessage is provided
        const botMessage: Message = {
          id: Date.now().toString(),
          role: 'assistant',
          content: `I received your message: "${inputValue}". This is a simulated response. In a real implementation, this would connect to the RAG chatbot API.`,
          timestamp: new Date(),
        };

        setMessages(prev => [...prev, botMessage]);
      }
    } catch (error) {
      console.error('Error sending message:', error);

      const errorMessage: Message = {
        id: Date.now().toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request.',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  return (
    <>
      {/* Floating chat button */}
      <button
        className={clsx(styles.chatButton, { [styles.open]: isOpen })}
        onClick={toggleChat}
        aria-label={isOpen ? 'Close chat' : 'Open chat'}
      >
        {isOpen ? '✕' : '🤖'}
      </button>

      {/* Chat widget */}
      {isOpen && (
        <div className={styles.chatWidget}>
          <div className={styles.chatHeader}>
            <h3>AI Textbook Assistant</h3>
            <p className={styles.chatSubtitle}>Ask questions about the content</p>
          </div>

          <div className={styles.chatMessages}>
            {messages.length === 0 ? (
              <div className={styles.welcomeMessage}>
                <p>Hello! I'm your AI assistant for the Physical AI & Humanoid Robotics textbook.</p>
                <p>Ask me questions about the current content or anything related to robotics.</p>
              </div>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={clsx(
                    styles.message,
                    styles[message.role],
                    message.role === 'user' ? styles.userMessage : styles.botMessage
                  )}
                >
                  <div className={styles.messageContent}>
                    {message.content}
                  </div>
                  <div className={styles.messageTimestamp}>
                    {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </div>
                </div>
              ))
            )}
            {isLoading && (
              <div className={clsx(styles.message, styles.botMessage)}>
                <div className={styles.typingIndicator}>
                  <div className={styles.dot}></div>
                  <div className={styles.dot}></div>
                  <div className={styles.dot}></div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className={styles.chatInputContainer}>
            <form onSubmit={handleSubmit} className={styles.chatInputForm}>
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Ask a question about this content..."
                className={styles.chatInput}
                disabled={isLoading}
                aria-label="Type your message"
              />
              <button
                type="submit"
                className={styles.sendButton}
                disabled={!inputValue.trim() || isLoading}
                aria-label="Send message"
              >
                ➤
              </button>
            </form>
            <div className={styles.voiceInputContainer}>
              <VoiceInput
                onTranscript={(transcript) => setInputValue(transcript)}
                onError={(error) => console.error('Voice input error:', error)}
              />
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default ChatbotWidget;