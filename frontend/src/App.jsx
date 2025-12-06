import { useState, useEffect, useRef } from "react"; // 1. Import useEffect and useRef
import axios from "axios";
import "./App.css";
import ReactMarkdown from "react-markdown";

const krishna = "/krishna (1).png";
const arjuna = "/arjuna.png";
const API = import.meta.env.BACKEND_URL 
function App() {
  const [messages, setMessages] = useState([
    { role: "assistant", content: "Radhey Radhey, I am GitaGPT. Ask me anything." }
  ]);
  const [input, setInput] = useState("");
  const [typing, setTyping] = useState(false);

  // 2. Create a reference for the end of the chat
  const messagesEndRef = useRef(null);

  // 3. Function to scroll to the bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };
  
  // 4. Trigger scroll whenever messages or typing state changes
  useEffect(() => {
    scrollToBottom();
  }, [messages, typing]);

  function handleKeyDown(e) {
    if (e.key === "Enter") {
      sendMessage();
    }
  }

  async function sendMessage() {
    if (!input.trim()) return;

    const updated = [...messages, { role: "user", content: input }];
    setMessages(updated);
    setInput("");
    setTyping(true);

    try {
      const res = await axios.post(`${API}/chat`, {
        messages: updated
      });

      setMessages([...updated, { role: "assistant", content: res.data.reply }]);
    } catch (error) {
      console.error("Error fetching chat:", error);
      // Optional: Add error handling message here
    } finally {
      setTyping(false);
    }
  }

  return (
    <>
      {/* HEADER */}
      <div className="custom-header">
        <img src={krishna} className="header-avatar" alt="Krishna" />
        GitaGPT
      </div>

      {/* CHAT */}
      <div className="chat-container">
        {messages.map((m, i) => (
          <div key={i} className={`chat-row ${m.role === "user" ? "user-row" : "bot-row"}`}>
            {m.role === "assistant" && <img src={krishna} className="bot-avatar" alt="Bot" />}

            {m.role === "assistant" ? (
              <div className="bot-wrapper">
                <div className="bot-name">GitaGPT</div>
                {/* Markdown is safe here */}
                <div className="bot-bubble"><ReactMarkdown>{m.content}</ReactMarkdown></div>
              </div>
            ) : (
              <>
                <div className="user-bubble"> <ReactMarkdown>{m.content}</ReactMarkdown></div>
                <img src={arjuna} className="user-avatar" alt="User" />
              </>
            )}
          </div>
        ))}

        {typing && (
          <div className="chat-row bot-row">
            <img src={krishna} className="bot-avatar" alt="Bot" />
            <div className="bot-wrapper">
              <div className="bot-name">GitaGPT</div>
              <div className="typing-bubble">
                <div className="typing-dots">
                  <span></span><span></span><span></span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* 5. Invisible div at the bottom to scroll to */}
        <div ref={messagesEndRef} />
      </div>

      {/* INPUT */}
      <div className="input-bar">
        <div className="input-wrapper">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask me anything..."
          />

          <button className="send-btn" onClick={sendMessage}>
            ➤
          </button>
        </div>
      </div>
    </>
  );
}

export default App;