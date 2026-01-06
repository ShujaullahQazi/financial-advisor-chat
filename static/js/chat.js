/**
 * FinAI - Financial Advisor Chat JavaScript
 * Handles chat functionality, session management, and UI interactions.
 */

// Chat application state
const ChatApp = {
    history: [],
    sessionId: null,
    isTyping: false,
    
    // DOM elements
    elements: {
        input: null,
        send: null,
        messages: null,
        typingIndicator: null,
        sessionInfo: null
    },

    /**
     * Initialize the chat application.
     */
    init() {
        this.cacheElements();
        this.initializeSession();
        this.bindEvents();
        this.showWelcomeMessage();
    },

    /**
     * Cache DOM elements for better performance.
     */
    cacheElements() {
        this.elements.input = document.getElementById('input');
        this.elements.send = document.getElementById('send');
        this.elements.messages = document.getElementById('messages');
        this.elements.typingIndicator = document.getElementById('typingIndicator');
        this.elements.sessionInfo = document.getElementById('sessionId');
    },

    /**
     * Initialize or restore session from localStorage.
     */
    initializeSession() {
        this.sessionId = localStorage.getItem('finai_session_id') || null;
        if (!this.sessionId) {
            this.sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('finai_session_id', this.sessionId);
        }
        this.elements.sessionInfo.textContent = this.sessionId;
    },

    /**
     * Bind event listeners.
     */
    bindEvents() {
        this.elements.send.onclick = () => this.sendMessage();
        this.elements.input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
    },

    /**
     * Add a message to the chat display.
     * @param {string} text - Message text
     * @param {string} sender - 'user' or 'ai'
     * @param {Array} toolsUsed - Tools used for the response
     * @param {number|null} confidence - Confidence score
     */
    addMessage(text, sender, toolsUsed = [], confidence = null) {
        const div = document.createElement('div');
        div.className = 'msg ' + sender;
        
        if (sender === 'ai') {
            // Render markdown for AI messages
            const markdownContent = document.createElement('div');
            markdownContent.className = 'markdown-content';
            markdownContent.innerHTML = marked.parse(text);
            div.appendChild(markdownContent);
            
            // Add tools used indicator
            if (toolsUsed && toolsUsed.length > 0) {
                const toolsDiv = document.createElement('div');
                toolsDiv.className = 'tools-used';
                toolsDiv.innerHTML = `🔧 Tools used: ${toolsUsed.join(', ')}`;
                div.appendChild(toolsDiv);
            }
            
            // Add confidence indicator
            if (confidence !== null) {
                const confidenceDiv = document.createElement('span');
                let confidenceClass = 'confidence-high';
                if (confidence < 0.7) confidenceClass = 'confidence-low';
                else if (confidence < 0.85) confidenceClass = 'confidence-medium';
                confidenceDiv.className = `confidence-indicator ${confidenceClass}`;
                confidenceDiv.textContent = `${Math.round(confidence * 100)}% confidence`;
                div.appendChild(confidenceDiv);
            }
        } else {
            div.textContent = text;
        }
        
        this.elements.messages.appendChild(div);
        this.elements.messages.scrollTop = this.elements.messages.scrollHeight;
    },

    /**
     * Show typing indicator.
     */
    showTypingIndicator() {
        this.isTyping = true;
        this.elements.typingIndicator.style.display = 'block';
        this.elements.messages.scrollTop = this.elements.messages.scrollHeight;
    },

    /**
     * Hide typing indicator.
     */
    hideTypingIndicator() {
        this.isTyping = false;
        this.elements.typingIndicator.style.display = 'none';
    },

    /**
     * Send a message to the server.
     */
    async sendMessage() {
        const msg = this.elements.input.value.trim();
        if (!msg || this.isTyping) return;
        
        this.addMessage(msg, 'user');
        this.history.push("User: " + msg);
        this.elements.input.value = '';
        
        this.showTypingIndicator();
        this.elements.send.disabled = true;
        
        try {
            const res = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    history: this.history,
                    session_id: this.sessionId,
                    user_preferences: {
                        risk_tolerance: 'moderate',
                        investment_horizon: 'long_term'
                    }
                })
            });
            
            if (!res.ok) throw new Error(await res.text());
            
            const data = await res.json();
            
            this.hideTypingIndicator();
            this.addMessage(data.response, 'ai', data.tools_used, data.confidence);
            this.history.push("AI: " + data.response);
            
            // Update session ID if provided
            if (data.session_id && data.session_id !== this.sessionId) {
                this.sessionId = data.session_id;
                localStorage.setItem('finai_session_id', this.sessionId);
                this.elements.sessionInfo.textContent = this.sessionId;
            }
            
        } catch (err) {
            this.hideTypingIndicator();
            this.addMessage('❌ Error: ' + err.message, 'ai');
        } finally {
            this.elements.send.disabled = false;
            this.elements.input.focus();
        }
    },

    /**
     * Show welcome message after brief delay.
     */
    showWelcomeMessage() {
        setTimeout(() => {
            this.addMessage(`👋 Welcome! I'm FinAI, your intelligent financial advisor agent. I can help you with:

• **Financial calculations** (compound interest, loan payments, retirement planning)
• **Financial education** and concepts
• **Budgeting advice** and strategies
• **Investment basics** and planning

Try asking me something like:
- "Calculate compound interest for $10,000 at 5% for 10 years"
- "What's a good emergency fund size?"
- "Help me understand 401(k) contributions"

What would you like to know about today?`, 'ai');
        }, 500);
    }
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => ChatApp.init());
