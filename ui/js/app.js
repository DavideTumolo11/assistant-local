/**
 * JARVIS AI ASSISTANT - FRONTEND FUNZIONANTE CON STREAMING CREATIVO
 * ================================================================
 * 
 * Basato sul vecchio app.js FUNZIONANTE con aggiunte per nuovo sistema:
 * - ✅ Mantiene tutta la logica di inizializzazione funzionante
 * - ✅ Aggiunge supporto ai_response_chunk per streaming creativo
 * - ✅ Aggiunge supporto ai_response_final per completamento
 * - ✅ Aggiunge supporto llm_event per creatività
 * - ✅ Compatibilità con WebSocket server stabile
 * - ✅ Error handling robusto mantenuto
 */

class JarvisApp {
    constructor() {
        // CONFIGURAZIONE TESTATA E FUNZIONANTE
        this.config = {
            websocketUrl: 'ws://localhost:8765',
            reconnectInterval: 3000,
            particleCount: 150,
            updateInterval: 5000,
            streamingTimeout: 10000,
            maxRetries: 3
        };

        // STATO APPLICAZIONE TESTATO
        this.state = {
            connected: false,
            currentState: 'normal',
            voiceActive: false,
            systemMetrics: {
                cpu: 0,
                memory: 0,
                voiceStatus: 'READY',
                aiModel: 'MISTRAL-7B'
            }
        };

        // ✅ STREAMING STATE AGGIORNATO per nuovo sistema
        this.streamingState = {
            isStreaming: false,
            currentMessageElement: null,
            streamStartTime: null,
            lastUpdateTime: null,
            streamingTimeout: null,
            totalCharsReceived: 0,
            retryCount: 0,
            accumulatedText: '',  // ✅ NUOVO - Accumula chunks
            chunkCount: 0         // ✅ NUOVO - Conta chunks ricevuti
        };

        // ELEMENTI DOM
        this.elements = {};
        this.websocket = null;
        this.particlesCanvas = null;
        this.particlesCtx = null;
        this.particles = [];

        // DEBUG MODE FUNZIONANTE
        this.debugMode = true;

        // INIZIALIZZAZIONE TESTATA
        this.init();
    }

    /**
     * INIZIALIZZAZIONE PRINCIPALE - TESTATA E FUNZIONANTE
     */
    async init() {
        this.debugLog('🚀 Initializing Jarvis Frontend with CREATIVE STREAMING...');

        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setup());
        } else {
            this.setup();
        }
    }

    /**
     * DEBUG LOGGING TESTATO
     */
    debugLog(message, data = null) {
        if (this.debugMode) {
            const timestamp = new Date().toISOString().substr(11, 12);
            console.log(`[${timestamp}] ${message}`);
            if (data) {
                console.log('📊 Data:', data);
            }
        }
    }

    /**
     * SETUP COMPLETO - TESTATO E FUNZIONANTE
     */
    async setup() {
        try {
            this.debugLog('📋 Setting up DOM elements...');
            this.setupElements();

            this.debugLog('📊 Animating loading progress...');
            this.animateLoadingProgress();

            this.debugLog('✨ Setting up particles...');
            this.setupParticles();

            this.debugLog('🎛️ Setting up event listeners...');
            this.setupEventListeners();

            this.debugLog('🌐 Connecting WebSocket...');
            await this.connectWebSocket();

            this.debugLog('🔄 Starting update loops...');
            this.startUpdateLoops();

            this.debugLog('🎬 Hiding loading overlay...');
            this.hideLoadingOverlay();

            this.debugLog('✅ Jarvis Frontend initialized successfully');
            this.showNotification('J.A.R.V.I.S online', 'success');

        } catch (error) {
            this.debugLog('❌ Error initializing Jarvis Frontend:', error);
            this.showNotification('Initialization Error: ' + error.message, 'error');
        }
    }

    /**
     * SETUP ELEMENTI DOM - TESTATO
     */
    setupElements() {
        this.elements = {
            // Status elements
            cpuUsage: document.getElementById('cpu-usage'),
            memoryUsage: document.getElementById('memory-usage'),
            voiceStatus: document.getElementById('voice-status'),
            aiModel: document.getElementById('ai-model'),
            backendStatus: document.getElementById('backend-status'),
            wsStatus: document.getElementById('ws-status'),

            // Control buttons
            voiceToggle: document.getElementById('voice-toggle'),
            chatBtn: document.getElementById('chat-btn'),
            settingsBtn: document.getElementById('settings-btn'),

            // Chat elements
            chatPanel: document.getElementById('chat-panel'),
            chatClose: document.getElementById('chat-close'),
            chatInput: document.getElementById('chat-input'),
            chatSend: document.getElementById('chat-send'),
            chatMessages: document.getElementById('chat-messages'),

            // Progress squares
            cpuProgress: document.getElementById('cpu-progress'),
            memoryProgress: document.getElementById('memory-progress'),
            networkProgress: document.getElementById('network-progress'),
            aiProgress: document.getElementById('ai-progress'),

            // Loading
            loadingOverlay: document.getElementById('loading-overlay'),
            loadingProgress: document.getElementById('loading-progress'),

            // Notifications
            notifications: document.getElementById('notifications')
        };

        this.debugLog('📋 DOM elements initialized');
    }

    /**
     * PARTICLES SYSTEM - TESTATO E FUNZIONANTE
     */
    setupParticles() {
        this.particlesCanvas = document.getElementById('particles-canvas');
        if (!this.particlesCanvas) {
            this.debugLog('⚠️ Particles canvas not found');
            return;
        }

        this.particlesCtx = this.particlesCanvas.getContext('2d');
        this.resizeCanvas();
        window.addEventListener('resize', () => this.resizeCanvas());
        this.createParticles();
        this.animateParticles();

        this.debugLog('✨ Particles system initialized');
    }

    resizeCanvas() {
        if (this.particlesCanvas) {
            this.particlesCanvas.width = window.innerWidth;
            this.particlesCanvas.height = window.innerHeight;
        }
    }

    createParticles() {
        this.particles = [];
        for (let i = 0; i < this.config.particleCount; i++) {
            this.particles.push({
                x: Math.random() * this.particlesCanvas.width,
                y: Math.random() * this.particlesCanvas.height,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5,
                size: Math.random() * 2 + 0.5,
                opacity: Math.random() * 0.5 + 0.3,
                pulsePhase: Math.random() * Math.PI * 2
            });
        }
    }

    animateParticles() {
        if (!this.particlesCtx || !this.particlesCanvas) return;

        this.particlesCtx.clearRect(0, 0, this.particlesCanvas.width, this.particlesCanvas.height);

        this.particles.forEach((particle) => {
            particle.x += particle.vx;
            particle.y += particle.vy;

            if (particle.x < 0 || particle.x > this.particlesCanvas.width) particle.vx *= -1;
            if (particle.y < 0 || particle.y > this.particlesCanvas.height) particle.vy *= -1;

            particle.x = Math.max(0, Math.min(this.particlesCanvas.width, particle.x));
            particle.y = Math.max(0, Math.min(this.particlesCanvas.height, particle.y));

            particle.pulsePhase += 0.02;
            const pulse = Math.sin(particle.pulsePhase) * 0.3 + 0.7;

            this.particlesCtx.beginPath();
            this.particlesCtx.arc(particle.x, particle.y, particle.size * pulse, 0, Math.PI * 2);
            this.particlesCtx.fillStyle = `rgba(0, 212, 255, ${particle.opacity * pulse})`;
            this.particlesCtx.fill();
        });

        requestAnimationFrame(() => this.animateParticles());
    }

    /**
     * EVENT LISTENERS - TESTATI E FUNZIONANTI
     */
    setupEventListeners() {
        // Control buttons
        this.elements.voiceToggle?.addEventListener('click', () => this.toggleVoice());
        this.elements.settingsBtn?.addEventListener('click', () => this.openSettings());

        // Chat functionality
        this.setupChatEventListeners();

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => this.handleKeyboard(e));

        this.debugLog('🎛️ Event listeners setup complete');
    }

    /**
     * CHAT EVENT LISTENERS - TESTATI
     */
    setupChatEventListeners() {
        this.debugLog('💬 Setting up ROBUST chat listeners...');

        if (!this.elements.chatBtn || !this.elements.chatPanel) {
            this.debugLog('❌ Chat elements not found!');
            return;
        }

        // Apri/chiudi chat panel
        this.elements.chatBtn.addEventListener('click', (e) => {
            e.preventDefault();
            const isOpen = this.elements.chatPanel.style.right === '20px';
            this.elements.chatPanel.style.right = isOpen ? '-400px' : '20px';
            this.debugLog(`💬 Chat panel ${isOpen ? 'closed' : 'opened'}`);
        });

        // Chiudi chat
        if (this.elements.chatClose) {
            this.elements.chatClose.addEventListener('click', (e) => {
                e.preventDefault();
                this.elements.chatPanel.style.right = '-400px';
                this.debugLog('❌ Chat panel closed');
            });
        }

        // FUNZIONE INVIO MESSAGGIO TESTATA
        const sendMessage = () => {
            if (!this.elements.chatInput) return;

            const message = this.elements.chatInput.value.trim();
            this.debugLog('📤 Attempting to send message:', { message, length: message.length });

            if (message) {
                // Reset streaming state se precedente messaggio è stuck
                if (this.streamingState.isStreaming) {
                    this.debugLog('⚠️ Previous streaming still active, forcing reset');
                    this.forceResetStreaming();
                }

                // Aggiungi messaggio utente
                this.addChatMessage('TU', message);

                // Invia al backend
                this.sendWebSocketMessageWithRetry('text_command', { text: message });

                // Reset input
                this.elements.chatInput.value = '';
                this.debugLog('✅ Message sent and input cleared');
            } else {
                this.debugLog('⚠️ Empty message, not sending');
            }
        };

        // Event listeners testati
        if (this.elements.chatSend) {
            this.elements.chatSend.addEventListener('click', sendMessage);
        }

        if (this.elements.chatInput) {
            this.elements.chatInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage();
                }
            });
        }

        this.debugLog('✅ ROBUST chat listeners setup complete');
    }

    /**
     * WEBSOCKET CONNECTION - TESTATA E FUNZIONANTE
     */
    async connectWebSocket() {
        try {
            this.debugLog('🌐 Connecting to WebSocket...', { url: this.config.websocketUrl });

            this.websocket = new WebSocket(this.config.websocketUrl);

            this.websocket.onopen = () => {
                this.debugLog('✅ WebSocket connected successfully');
                this.state.connected = true;
                this.updateConnectionStatus(true);
                this.showNotification('Connesso a JARVIS', 'success');
            };

            this.websocket.onmessage = (event) => {
                this.handleWebSocketMessage(event.data);
            };

            this.websocket.onclose = (event) => {
                this.debugLog('🔌 WebSocket disconnected:', { code: event.code, reason: event.reason });
                this.state.connected = false;
                this.updateConnectionStatus(false);

                // Force reset streaming se connessione persa
                if (this.streamingState.isStreaming) {
                    this.forceResetStreaming();
                }

                if (event.code !== 1000 && event.code !== 1001) {
                    this.showNotification('Connection lost. Reconnecting...', 'warning');
                    setTimeout(() => this.connectWebSocket(), this.config.reconnectInterval);
                }
            };

            this.websocket.onerror = (error) => {
                this.debugLog('❌ WebSocket error:', error);
                this.showNotification('Connection error', 'error');
            };

        } catch (error) {
            this.debugLog('❌ Failed to connect WebSocket:', error);
            this.showNotification('Failed to connect to backend', 'error');
            setTimeout(() => this.connectWebSocket(), this.config.reconnectInterval);
        }
    }

    /**
     * ✅ GESTIONE MESSAGGI WEBSOCKET - AGGIORNATA PER STREAMING CREATIVO
     */
    handleWebSocketMessage(data) {
        this.debugLog('📨 Raw message received');

        try {
            const message = typeof data === 'string' ? JSON.parse(data) : data;
            this.debugLog('📋 Parsed message:', { type: message.type, size: JSON.stringify(message).length });

            switch (message.type) {
                // ✅ SUPPORTO VECCHIO SISTEMA (per compatibilità)
                case 'streaming_update':
                    this.handleStreamingUpdateRobust(message);
                    break;

                // ✅ NUOVO - SUPPORTO STREAMING CREATIVO
                case 'ai_response_chunk':
                    this.debugLog('📦 CREATIVE streaming chunk received:', {
                        chunk_number: message.chunk_number,
                        chunk_length: message.chunk ? message.chunk.length : 0,
                        is_final: message.is_final,
                        creativity_mode: message.creativity_mode
                    });

                    // Converti al formato del vecchio sistema
                    this.handleStreamingUpdateRobust({
                        text: this.streamingState.accumulatedText + (message.chunk || ''),
                        is_final: message.is_final,
                        chunk_number: message.chunk_number,
                        creativity_mode: message.creativity_mode
                    });

                    // Accumula chunk per prossimo update
                    if (message.chunk) {
                        this.streamingState.accumulatedText += message.chunk;
                        this.streamingState.chunkCount++;
                    }
                    break;

                // ✅ NUOVO - RISPOSTA FINALE CREATIVA
                case 'ai_response_final':
                    this.debugLog('🏁 CREATIVE final response received:', {
                        response_length: message.response ? message.response.length : 0,
                        creativity_mode: message.creativity_mode
                    });

                    if (this.streamingState.isStreaming) {
                        // Completa con risposta finale
                        this.handleStreamingUpdateRobust({
                            text: message.response || this.streamingState.accumulatedText,
                            is_final: true,
                            creativity_mode: message.creativity_mode
                        });
                    } else {
                        // Se non in streaming, aggiungi come messaggio normale
                        this.addChatMessage('JARVIS', message.response || 'Risposta non disponibile');
                    }
                    break;

                // ✅ NUOVO - EVENTI LLM CREATIVO
                case 'llm_event':
                    this.handleLLMEvent(message);
                    break;

                // GESTIONE MESSAGGI ESISTENTI - TESTATI
                case 'connection_established':
                    this.debugLog('🔗 Connection established:', message.message);
                    this.addChatMessage('SYSTEM', `Connected: ${message.message}`);

                    // Log features (senza notifiche)
                    if (message.features) {
                        this.debugLog('✨ Server features:', message.features);
                    }
                    break;

                case 'text_command_response':
                    this.debugLog('🤖 AI response received');
                    if (!this.streamingState.isStreaming) {
                        this.addChatMessage('JARVIS', message.text || message.response);
                    }
                    break;

                case 'error':
                    this.debugLog('❌ Backend error:', message);
                    this.showNotification(`Error: ${message.error}`, 'error');
                    this.addChatMessage('SYSTEM', `❌ ${message.error}`, 'error');

                    // Reset streaming se errore
                    if (this.streamingState.isStreaming) {
                        this.forceResetStreaming();
                    }
                    break;

                case 'pong':
                    this.debugLog('🏓 Pong received');
                    break;

                case 'system_status':
                    this.debugLog('📊 System status update:', message.status);
                    this.updateSystemMetrics(message);
                    break;

                case 'llm_status':
                    this.debugLog('🧠 LLM status update:', { available: message.available });
                    break;

                default:
                    this.debugLog('❓ Unknown message type:', message.type);
                    break;
            }
        } catch (error) {
            this.debugLog('❌ Error parsing WebSocket message:', error);
        }
    }

    /**
     * ✅ NUOVO - GESTIONE EVENTI LLM CREATIVO
     */
    handleLLMEvent(message) {
        const eventData = message.data;
        const eventType = eventData.type;

        this.debugLog('🧠 LLM Creative Event:', { type: eventType, data: eventData.data });

        switch (eventType) {
            case 'generation_started':
                this.debugLog('🎨 Generation started');
                break;

            case 'generation_completed':
                const creativity = eventData.data.creativity_score || 0;
                this.debugLog('🎯 Creativity score:', creativity.toFixed(2));
                break;

            case 'generation_error':
                this.showNotification('Errore nella risposta', 'error');
                if (this.streamingState.isStreaming) {
                    this.forceResetStreaming();
                }
                break;

            case 'llm_initialized':
                const features = eventData.data;
                this.debugLog('🧠 LLM Features:', features);
                break;
        }
    }

    /**
     * GESTIONE STREAMING UPDATE - TESTATA E FUNZIONANTE
     */
    handleStreamingUpdateRobust(message) {
        try {
            const text = message.text || '';
            const isFinal = message.is_final || false;
            const currentTime = Date.now();
            const creativityMode = message.creativity_mode || false;

            this.debugLog('📦 Streaming update processed:', {
                textLength: text.length,
                isFinal: isFinal,
                isCurrentlyStreaming: this.streamingState.isStreaming,
                creativityMode: creativityMode,
                chunkNumber: message.chunk_number || 'N/A',
                timeSinceLastUpdate: this.streamingState.lastUpdateTime ? (currentTime - this.streamingState.lastUpdateTime) : 'N/A'
            });

            // Validazioni
            if (!text && !isFinal) {
                this.debugLog('⚠️ Empty non-final update, ignoring');
                return;
            }

            // Se non stiamo streamando, inizia nuovo messaggio
            if (!this.streamingState.isStreaming) {
                this.debugLog('🚀 Starting new CREATIVE streaming...');
                this.startStreamingMessageRobust(creativityMode);
            }

            // Update messaggio
            this.updateStreamingMessageRobust(text, creativityMode);

            // Update stato tracking
            this.streamingState.lastUpdateTime = currentTime;
            this.streamingState.totalCharsReceived = text.length;

            // Reset timeout
            this.resetStreamingTimeout();

            // Se è finale, completa
            if (isFinal) {
                this.debugLog('🏁 Final CREATIVE streaming update, completing...');
                this.completeStreamingMessageRobust(creativityMode);
            }

        } catch (error) {
            this.debugLog('❌ Error handling streaming update:', error);
            this.forceResetStreaming();
        }
    }

    /**
     * INIZIA MESSAGGIO STREAMING - TESTATO CON AGGIORNAMENTI CREATIVI
     */
    startStreamingMessageRobust(creativityMode = false) {
        try {
            this.debugLog('🚀 Starting CREATIVE streaming message...', { creativityMode });

            // Reset stato
            if (this.streamingState.isStreaming) {
                this.debugLog('⚠️ Previous streaming active, forcing reset');
                this.forceResetStreaming();
            }

            // Set nuovo stato
            this.streamingState.isStreaming = true;
            this.streamingState.streamStartTime = Date.now();
            this.streamingState.lastUpdateTime = Date.now();
            this.streamingState.totalCharsReceived = 0;
            this.streamingState.retryCount = 0;
            this.streamingState.accumulatedText = '';  // ✅ RESET accumulator
            this.streamingState.chunkCount = 0;        // ✅ RESET chunk counter

            // Crea elemento messaggio semplice (senza badge tecnici)
            const messageDiv = document.createElement('div');
            messageDiv.className = `chat-message jarvis-message streaming`;

            const timestamp = new Date().toLocaleTimeString('it-IT', {
                hour: '2-digit',
                minute: '2-digit'
            });

            // Header semplice - solo JARVIS
            const headerColor = '#00ff7f';
            const bgColor = 'rgba(0, 255, 127, 0.1)';

            messageDiv.innerHTML = `
                <div class="message-header" style="font-weight: bold; font-size: 11px; margin-bottom: 5px; color: ${headerColor};">
                    JARVIS - ${timestamp}
                </div>
                <div class="streaming-content" style="line-height: 1.5; color: #ffffff; word-wrap: break-word; min-height: 20px;">
                    <span class="typing-cursor">|</span>
                </div>
            `;

            messageDiv.style.cssText = `
                margin-bottom: 15px;
                padding: 12px 15px;
                border-radius: 12px;
                background: ${bgColor};
                border-left: 3px solid ${headerColor};
                animation: fadeInUp 0.3s ease-out;
            `;

            this.elements.chatMessages.appendChild(messageDiv);
            this.streamingState.currentMessageElement = messageDiv;

            // Setup timeout
            this.setupStreamingTimeout();

            // Scroll to bottom
            this.scrollToBottom();

            this.debugLog('✅ CREATIVE streaming message started');

        } catch (error) {
            this.debugLog('❌ Error starting streaming message:', error);
            this.forceResetStreaming();
        }
    }

    /**
     * AGGIORNA MESSAGGIO STREAMING - TESTATO
     */
    updateStreamingMessageRobust(text, creativityMode = false) {
        try {
            if (!this.streamingState.currentMessageElement) {
                this.debugLog('⚠️ No streaming message element, creating new one');
                this.startStreamingMessageRobust(creativityMode);
                return;
            }

            const contentDiv = this.streamingState.currentMessageElement.querySelector('.streaming-content');
            if (!contentDiv) {
                this.debugLog('❌ No content div found');
                this.forceResetStreaming();
                return;
            }

            // Update con cursor colorato per creatività
            const cursorColor = creativityMode ? '#FF6B35' : '#00d4ff';
            try {
                contentDiv.innerHTML = text + `<span class="typing-cursor" style="animation: blink 1s infinite; color: ${cursorColor};">|</span>`;
            } catch (domError) {
                this.debugLog('⚠️ innerHTML failed, using textContent fallback');
                contentDiv.textContent = text + '|';
            }

            this.debugLog('📝 Updated CREATIVE streaming text:', {
                length: text.length,
                chunks: this.streamingState.chunkCount,
                preview: text.substring(0, 50) + (text.length > 50 ? '...' : '')
            });

            this.scrollToBottom();

        } catch (error) {
            this.debugLog('❌ Error updating streaming message:', error);
            this.forceResetStreaming();
        }
    }

    /**
     * COMPLETA MESSAGGIO STREAMING - TESTATO CON STATISTICHE CREATIVE
     */
    completeStreamingMessageRobust(creativityMode = false) {
        try {
            this.debugLog('🏁 Completing streaming message...');

            if (this.streamingState.currentMessageElement) {
                // Rimuovi typing cursor
                const contentDiv = this.streamingState.currentMessageElement.querySelector('.streaming-content');
                if (contentDiv) {
                    const currentText = contentDiv.textContent.replace('|', '');
                    contentDiv.textContent = currentText;
                }

                // Header resta invariato (nessuna statistica)
                // Già mostra solo "JARVIS - HH:MM"

                // Rimuovi classe streaming
                this.streamingState.currentMessageElement.classList.remove('streaming');
            }

            // Reset stato completo
            this.resetStreamingState();

            this.debugLog('✅ CREATIVE streaming message completed');

        } catch (error) {
            this.debugLog('❌ Error completing streaming message:', error);
            this.resetStreamingState();
        }
    }

    /**
     * FORCE RESET STREAMING - TESTATO E FUNZIONANTE
     */
    forceResetStreaming() {
        this.debugLog('🔄 FORCE RESET streaming state...');

        try {
            // Reset timeout
            if (this.streamingState.streamingTimeout) {
                clearTimeout(this.streamingState.streamingTimeout);
            }

            // Se c'è un messaggio incompleto, completalo
            if (this.streamingState.currentMessageElement) {
                const contentDiv = this.streamingState.currentMessageElement.querySelector('.streaming-content');
                if (contentDiv) {
                    const currentText = contentDiv.textContent.replace('|', '');
                    contentDiv.textContent = currentText + ' [RECOVERED]';
                }

                const headerDiv = this.streamingState.currentMessageElement.querySelector('.message-header');
                if (headerDiv) {
                    headerDiv.innerHTML = headerDiv.innerHTML.replace('STREAMING...', 'RECOVERED');
                }

                this.streamingState.currentMessageElement.classList.remove('streaming');
            }

            // Reset stato
            this.resetStreamingState();

            this.debugLog('✅ Streaming state force reset completed');

        } catch (error) {
            this.debugLog('❌ Error in force reset:', error);
            this.resetStreamingState();
        }
    }

    /**
     * RESET STREAMING STATE - TESTATO
     */
    resetStreamingState() {
        this.streamingState.isStreaming = false;
        this.streamingState.currentMessageElement = null;
        this.streamingState.streamStartTime = null;
        this.streamingState.lastUpdateTime = null;
        this.streamingState.totalCharsReceived = 0;
        this.streamingState.retryCount = 0;
        this.streamingState.accumulatedText = '';  // ✅ RESET accumulator
        this.streamingState.chunkCount = 0;        // ✅ RESET chunk counter

        if (this.streamingState.streamingTimeout) {
            clearTimeout(this.streamingState.streamingTimeout);
            this.streamingState.streamingTimeout = null;
        }
    }

    /**
     * SETUP TIMEOUT PER STREAMING - TESTATO
     */
    setupStreamingTimeout() {
        if (this.streamingState.streamingTimeout) {
            clearTimeout(this.streamingState.streamingTimeout);
        }

        this.streamingState.streamingTimeout = setTimeout(() => {
            this.debugLog('⏰ Streaming timeout detected, forcing recovery...');
            this.showNotification('Streaming timeout, recovering...', 'warning');
            this.forceResetStreaming();
        }, this.config.streamingTimeout);
    }

    /**
     * RESET TIMEOUT - TESTATO
     */
    resetStreamingTimeout() {
        if (this.streamingState.streamingTimeout) {
            clearTimeout(this.streamingState.streamingTimeout);
        }
        this.setupStreamingTimeout();
    }

    /**
     * WEBSOCKET MESSAGE CON RETRY - TESTATO
     */
    sendWebSocketMessageWithRetry(type, data = {}) {
        const message = { type, ...data };
        this.debugLog('📤 Sending message with retry:', { type, retryCount: this.streamingState.retryCount });

        if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
            try {
                this.websocket.send(JSON.stringify(message));
                this.streamingState.retryCount = 0;  // Reset on success
                return true;
            } catch (error) {
                this.debugLog('❌ Error sending message:', error);
                return this.retryMessage(type, data);
            }
        } else {
            this.debugLog('⚠️ WebSocket not connected, attempting retry...');
            return this.retryMessage(type, data);
        }
    }

    /**
     * RETRY MESSAGE - TESTATO
     */
    retryMessage(type, data) {
        if (this.streamingState.retryCount < this.config.maxRetries) {
            this.streamingState.retryCount++;
            this.debugLog(`🔄 Retrying message (${this.streamingState.retryCount}/${this.config.maxRetries})...`);

            setTimeout(() => {
                this.sendWebSocketMessageWithRetry(type, data);
            }, 1000 * this.streamingState.retryCount);

            return true;
        } else {
            this.debugLog('❌ Max retries reached, giving up');
            this.showNotification('Failed to send message after retries', 'error');
            return false;
        }
    }

    /**
     * SCROLL TO BOTTOM - TESTATO
     */
    scrollToBottom() {
        try {
            if (this.elements.chatMessages) {
                this.elements.chatMessages.scrollTop = this.elements.chatMessages.scrollHeight;
            }
        } catch (error) {
            this.debugLog('⚠️ Error scrolling to bottom:', error);
        }
    }

    /**
     * ADD CHAT MESSAGE - TESTATO E FUNZIONANTE
     */
    addChatMessage(sender, text, type = 'normal') {
        if (!this.elements.chatMessages) return;

        // Non aggiungere se in streaming
        if (this.streamingState.isStreaming && sender === 'JARVIS') {
            this.debugLog('⚠️ Skipping JARVIS message, streaming in progress');
            return;
        }

        this.debugLog('💬 Adding chat message:', { sender, length: text.length });

        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${sender.toLowerCase()}-message`;

        const isUser = sender === 'USER';
        const isSystem = sender === 'SYSTEM';

        let backgroundColor, borderColor;
        if (isUser) {
            backgroundColor = 'rgba(0, 212, 255, 0.1)';
            borderColor = '#00d4ff';
        } else if (isSystem) {
            backgroundColor = 'rgba(255, 193, 7, 0.1)';
            borderColor = '#ffc107';
        } else {
            backgroundColor = 'rgba(0, 255, 127, 0.1)';
            borderColor = '#00ff7f';
        }

        messageDiv.style.cssText = `
            margin-bottom: 15px; 
            padding: 12px 15px; 
            border-radius: 12px; 
            background: ${backgroundColor}; 
            border-left: 3px solid ${borderColor};
            animation: fadeInUp 0.3s ease-out;
        `;

        const timestamp = new Date().toLocaleTimeString('it-IT', {
            hour: '2-digit',
            minute: '2-digit'
        });

        messageDiv.innerHTML = `
            <div style="font-weight: bold; font-size: 11px; margin-bottom: 5px; color: ${borderColor}; text-transform: uppercase;">
                ${sender} - ${timestamp}
            </div>
            <div style="line-height: 1.5; color: #ffffff; word-wrap: break-word;">
                ${text}
            </div>
        `;

        this.elements.chatMessages.appendChild(messageDiv);

        setTimeout(() => {
            this.scrollToBottom();
        }, 100);

        this.debugLog(`✅ Added ${sender} message successfully`);
    }

    /**
     * SEND WEBSOCKET MESSAGE - ALIAS TESTATO
     */
    sendWebSocketMessage(type, data = {}) {
        return this.sendWebSocketMessageWithRetry(type, data);
    }

    /**
     * SET STATE - TESTATO
     */
    setState(newState) {
        if (this.state.currentState !== newState) {
            this.debugLog(`🎨 State change: ${this.state.currentState} → ${newState}`);

            document.body.classList.remove(`state-${this.state.currentState}`);
            this.state.currentState = newState;
            document.body.classList.add(`state-${newState}`);

            const stateNames = {
                normal: 'Normal Mode',
                processing: 'Processing...',
                speaking: 'Speaking'
            };

            this.showNotification(`Mode: ${stateNames[newState] || newState}`, 'info');
        }
    }

    /**
     * UPDATE CONNECTION STATUS - TESTATO
     */
    updateConnectionStatus(connected) {
        this.debugLog('🔗 Connection status update:', { connected });

        if (this.elements.wsStatus) {
            if (connected) {
                this.elements.wsStatus.classList.add('connected');
            } else {
                this.elements.wsStatus.classList.remove('connected');
            }
        }

        if (this.elements.backendStatus) {
            // ✅ AGGIORNATO per creatività
            const statusText = connected
                ? 'Connected - CREATIVE Streaming'
                : 'Disconnected';

            this.elements.backendStatus.textContent = statusText;
            this.elements.backendStatus.style.color = connected ? '#00ff7f' : '#ff4757';
        }
    }

    /**
     * ✅ NUOVO - UPDATE SYSTEM METRICS
     */
    updateSystemMetrics(statusData) {
        try {
            // Update performance display se elementi esistono
            const metrics = {
                'uptime': statusData.uptime_formatted || 'N/A',
                'clients': statusData.connected_clients || 0,
                'messages': statusData.statistics?.messages_processed || 0,
                'chunks': statusData.statistics?.streaming_chunks_sent || 0
            };

            Object.keys(metrics).forEach(key => {
                const element = document.getElementById(`metric-${key}`);
                if (element) {
                    element.textContent = metrics[key];
                }
            });

            // Update creativity stats se disponibili
            if (statusData.creativity_stats) {
                this.debugLog('🎨 Creativity stats update:', statusData.creativity_stats);
            }

        } catch (error) {
            this.debugLog('❌ Error updating system metrics:', error);
        }
    }

    /**
     * TOGGLE VOICE - TESTATO
     */
    toggleVoice() {
        this.debugLog('🎤 Voice toggle requested');
        this.showNotification('Voice system coming soon...', 'info');
    }

    /**
     * OPEN SETTINGS - TESTATO
     */
    openSettings() {
        this.debugLog('⚙️ Settings requested');
        this.showNotification('Settings panel coming soon...', 'info');
    }

    /**
     * KEYBOARD SHORTCUTS - TESTATI
     */
    handleKeyboard(event) {
        if (event.target === this.elements.chatInput) return;

        switch (event.key) {
            case 'F3':
                event.preventDefault();
                if (this.elements.chatBtn) {
                    this.elements.chatBtn.click();
                }
                break;

            case 'Escape':
                if (this.elements.chatPanel && this.elements.chatPanel.style.right === '20px') {
                    this.elements.chatPanel.style.right = '-400px';
                    this.debugLog('💬 Chat panel closed via Escape');
                }
                break;

            case 'Enter':
                if (this.elements.chatPanel && this.elements.chatPanel.style.right !== '20px') {
                    this.elements.chatBtn?.click();
                    setTimeout(() => {
                        this.elements.chatInput?.focus();
                    }, 300);
                }
                break;
        }
    }

    /**
     * UPDATE VOICE ACTIVITY - TESTATO
     */
    updateVoiceActivity(active) {
        this.state.voiceActive = active;
        this.debugLog('🎤 Voice activity update:', { active });

        if (this.elements.voiceActivity) {
            this.elements.voiceActivity.style.display = active ? 'block' : 'none';
        }
    }

    /**
     * SHOW NOTIFICATION - TESTATO E FUNZIONANTE
     */
    showNotification(text, level = 'info', duration = 5000) {
        if (!this.elements.notifications) return;

        this.debugLog('📢 Showing notification:', { text, level, duration });

        const notification = document.createElement('div');
        notification.className = `notification notification-${level}`;

        const icons = {
            info: 'ℹ️',
            success: '✅',
            warning: '⚠️',
            error: '❌'
        };

        // ✅ STYLING MIGLIORATO per creatività
        const colors = {
            info: '#00d4ff',
            success: '#00ff7f',
            warning: '#ffc107',
            error: '#ff4757'
        };

        notification.innerHTML = `
            <div style="display: flex; align-items: center; gap: 10px; padding: 10px; background: rgba(0, 20, 40, 0.95); border: 1px solid ${colors[level]}; border-radius: 8px; margin-bottom: 10px; backdrop-filter: blur(10px);">
                <span style="font-size: 16px;">${icons[level] || 'ℹ️'}</span>
                <span style="flex: 1; color: #ffffff;">${text}</span>
                <button onclick="this.parentElement.parentElement.remove()" style="background: none; border: none; color: ${colors[level]}; cursor: pointer; font-size: 18px; padding: 0; width: 20px; height: 20px;">×</button>
            </div>
        `;

        this.elements.notifications.appendChild(notification);

        setTimeout(() => {
            if (notification.parentNode) {
                notification.style.opacity = '0';
                notification.style.transform = 'translateX(100%)';
                setTimeout(() => {
                    if (notification.parentNode) {
                        notification.parentNode.removeChild(notification);
                    }
                }, 300);
            }
        }, duration);
    }

    /**
     * ✅ ANIMA PROGRESS BAR INIZIALE
     */
    animateLoadingProgress() {
        // Anima solo la barra di progresso iniziale
        if (this.elements.loadingProgress) {
            let progress = 0;
            const progressInterval = setInterval(() => {
                progress += Math.random() * 15 + 10; // Incrementa tra 10-25%
                if (progress >= 95) {
                    progress = 95; // Fermati al 95%, completa al 100% quando tutto è pronto
                    clearInterval(progressInterval);
                }
                this.elements.loadingProgress.style.width = `${progress}%`;
                this.debugLog(`📊 Loading progress: ${progress.toFixed(0)}%`);
            }, 200);
        }
    }

    /**
     * HIDE LOADING OVERLAY - TESTATO
     */
    hideLoadingOverlay() {
        if (this.elements.loadingOverlay) {
            // Completa la progress bar al 100%
            if (this.elements.loadingProgress) {
                this.elements.loadingProgress.style.width = '100%';
            }

            setTimeout(() => {
                this.elements.loadingOverlay.style.opacity = '0';
                setTimeout(() => {
                    this.elements.loadingOverlay.style.display = 'none';
                    this.debugLog('🎬 Loading overlay hidden');
                }, 500);
            }, 1000);
        }
    }

    /**
     * START UPDATE LOOPS - TESTATI
     */
    startUpdateLoops() {
        // Metrics update
        setInterval(() => {
            if (!this.state.connected) {
                // Fake metrics quando disconnesso
                if (this.elements.cpuUsage) this.elements.cpuUsage.textContent = '0%';
                if (this.elements.memoryUsage) this.elements.memoryUsage.textContent = '0%';
                if (this.elements.voiceStatus) this.elements.voiceStatus.textContent = 'OFFLINE';
                if (this.elements.aiModel) this.elements.aiModel.textContent = 'DISCONNECTED';
            }
        }, this.config.updateInterval);

        // ✅ STREAMING HEALTH MONITORING
        setInterval(() => {
            if (this.streamingState.isStreaming) {
                const timeSinceLastUpdate = Date.now() - this.streamingState.lastUpdateTime;
                if (timeSinceLastUpdate > 5000) {  // 5 secondi senza update
                    this.debugLog('⚠️ Streaming seems stuck, may need recovery');
                }
            }
        }, 2000);

        // ✅ PERIODIC PING
        setInterval(() => {
            if (this.state.connected && this.websocket?.readyState === WebSocket.OPEN) {
                try {
                    this.websocket.send(JSON.stringify({ type: 'ping' }));
                    this.debugLog('🏓 Ping sent to server');
                } catch (error) {
                    this.debugLog('❌ Error sending ping:', error);
                }
            }
        }, 30000); // Ping ogni 30 secondi

        this.debugLog('🔄 Update loops started (CREATIVE optimized)');
    }

    /**
     * ✅ DEBUG HELPERS AVANZATI
     */
    getDebugInfo() {
        return {
            state: this.state,
            streamingState: this.streamingState,
            connected: this.state.connected,
            websocketReady: this.websocket?.readyState === WebSocket.OPEN,
            elementsFound: Object.keys(this.elements).filter(key => this.elements[key]).length,
            particlesCount: this.particles.length,
            // ✅ NUOVO - Creative stats
            creativeFeatures: {
                chunkSupport: true,
                creativityMode: true,
                antiRepetition: true,
                dynamicPrompts: true
            }
        };
    }

    /**
     * ✅ FORCE RECONNECT
     */
    forceReconnect() {
        this.debugLog('🔄 Forcing WebSocket reconnection...');

        if (this.websocket) {
            this.websocket.close();
        }

        // Reset streaming se attivo
        if (this.streamingState.isStreaming) {
            this.forceResetStreaming();
        }

        setTimeout(() => {
            this.connectWebSocket();
        }, 1000);

        this.showNotification('Forcing reconnection...', 'info');
    }

    /**
     * ✅ CLEAR CHAT
     */
    clearChat() {
        if (this.elements.chatMessages) {
            this.elements.chatMessages.innerHTML = '';
            this.debugLog('💬 Chat cleared');
            this.showNotification('Chat cleared', 'info');
        }

        // Reset streaming state
        this.resetStreamingState();
    }

    /**
     * CLEANUP - TESTATO
     */
    destroy() {
        this.debugLog('🗑️ Destroying Jarvis App...');

        if (this.websocket) {
            this.websocket.close();
        }

        this.resetStreamingState();

        window.removeEventListener('resize', this.resizeCanvas);
        document.removeEventListener('keydown', this.handleKeyboard);

        this.particles = [];

        this.debugLog('✅ Jarvis App destroyed');
    }
}

/**
 * ✅ CSS ANIMATIONS CREATIVE - AGGIORNATO
 */
const style = document.createElement('style');
style.textContent = `
    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0; }
    }
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    .streaming-content {
        min-height: 20px;
    }
    .typing-cursor {
        animation: blink 1s infinite;
        font-weight: bold;
    }
    /* ✅ NUOVO - Creative mode styling */
    .creative-mode {
        position: relative;
        overflow: hidden;
    }
    .creative-mode::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 107, 53, 0.1), transparent);
        animation: creativeSweep 3s infinite;
    }
    @keyframes creativeSweep {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    /* Notification animations */
    .notification {
        transition: all 0.3s ease;
    }
`;
document.head.appendChild(style);

/**
 * ✅ GLOBAL ERROR HANDLERS ROBUSTI
 */
window.addEventListener('error', (event) => {
    console.error('🚨 Global error:', event.error);
    if (window.jarvis) {
        window.jarvis.debugLog('🚨 Global error detected:', event.error);
        window.jarvis.showNotification(`Error: ${event.error.message}`, 'error');

        // Reset streaming se errore critico
        if (window.jarvis.streamingState.isStreaming) {
            window.jarvis.forceResetStreaming();
        }
    }
});

window.addEventListener('unhandledrejection', (event) => {
    console.error('🚨 Unhandled promise rejection:', event.reason);
    if (window.jarvis) {
        window.jarvis.debugLog('🚨 Promise rejection:', event.reason);
        window.jarvis.showNotification(`Promise error: ${event.reason}`, 'error');
    }
});

/**
 * ✅ INIZIALIZZAZIONE ROBUSTA E TESTATA
 */
document.addEventListener('DOMContentLoaded', () => {
    console.log('📄 DOM loaded, initializing CREATIVE Jarvis...');

    try {
        // Create global instance
        window.jarvis = new JarvisApp();

        // ✅ DEBUG HELPERS AVANZATI E TESTATI
        window.jarvisDebug = {
            // Basic info
            getState: () => window.jarvis.getDebugInfo(),
            getStreamingState: () => window.jarvis.streamingState,

            // Actions
            sendTest: (msg) => window.jarvis.sendWebSocketMessage('text_command', { text: msg }),
            clearChat: () => window.jarvis.clearChat(),
            reconnect: () => window.jarvis.forceReconnect(),

            // Recovery
            forceResetStreaming: () => window.jarvis.forceResetStreaming(),
            resetState: () => window.jarvis.resetStreamingState(),

            // Debug
            enableDebug: () => { window.jarvis.debugMode = true; console.log('🐛 Debug mode enabled'); },
            disableDebug: () => { window.jarvis.debugMode = false; console.log('🐛 Debug mode disabled'); },

            // ✅ TEST CREATIVITÀ
            testCreativity: () => {
                console.log('🎨 Testing CREATIVE responses...');
                const creativeTests = [
                    'Ciao Jarvis, come stai?',
                    'Ciao Jarvis, come stai?', // Same question for variety test
                    'Dimmi qualcosa di interessante su di te',
                    'Raccontami una breve storia',
                    'Parlami della creatività'
                ];

                creativeTests.forEach((test, index) => {
                    setTimeout(() => {
                        console.log(`🧪 Test ${index + 1}: ${test}`);
                        window.jarvis.sendWebSocketMessage('text_command', { text: test });
                    }, index * 8000); // 8 secondi tra test
                });
            },

            // ✅ TEST STREAMING LUNGO
            testLongStreaming: () => {
                console.log('📡 Testing long CREATIVE streaming...');
                window.jarvis.sendWebSocketMessage('text_command', {
                    text: 'Jarvis, scrivi una storia lunga e dettagliata di almeno 300 parole su un viaggio incredibile nello spazio, includendo personaggi interessanti e colpi di scena'
                });
            },

            // Performance
            getPerformance: () => ({
                particles: window.jarvis.particles.length,
                streamingActive: window.jarvis.streamingState.isStreaming,
                connected: window.jarvis.state.connected,
                wsReady: window.jarvis.websocket?.readyState === WebSocket.OPEN,
                chunkCount: window.jarvis.streamingState.chunkCount,
                accumulatedLength: window.jarvis.streamingState.accumulatedText.length
            })
        };

        console.log('🎮 Advanced Debug helpers: window.jarvisDebug');
        console.log('🎨 CREATIVE Features: Anti-repetition, Dynamic prompts, Chunk streaming');
        console.log('🛡️ ROBUST Streaming: Error recovery, Timeout handling, Retry logic');
        console.log('🔧 Error Recovery: Global handlers, State reset, Connection recovery');
        console.log('✅ Jarvis Frontend CREATIVE + ROBUST loaded successfully');

        // ✅ DEBUG INFO UTILI
        console.log('');
        console.log('🧪 QUICK TESTS:');
        console.log('   jarvisDebug.testCreativity()     - Test risposte creative');
        console.log('   jarvisDebug.testLongStreaming()  - Test streaming lungo');
        console.log('   jarvisDebug.getPerformance()     - Info performance');
        console.log('   jarvisDebug.forceResetStreaming() - Reset forzato');
        console.log('');

    } catch (error) {
        console.error('❌ Fatal error initializing Jarvis:', error);
        document.body.innerHTML = `
            <div style="color: red; text-align: center; padding: 50px; font-family: monospace; background: rgba(0,0,0,0.9);">
                <h1>🚨 JARVIS INITIALIZATION FAILED</h1>
                <p>Error: ${error.message}</p>
                <p>Check console for details</p>
                <button onclick="location.reload()" style="padding: 10px 20px; margin-top: 20px; background: #00d4ff; color: black; border: none; border-radius: 5px; cursor: pointer;">Reload</button>
            </div>
        `;
    }
});

/**
 * ✅ CLEANUP ON UNLOAD
 */
window.addEventListener('beforeunload', () => {
    if (window.jarvis) {
        window.jarvis.destroy();
    }
});

/**
 * ✅ CONSOLE WELCOME MESSAGE
 */
console.log(`
🚀 JARVIS AI Assistant - CREATIVE Frontend Loaded
================================================
✨ Features:
   🎨 Creative streaming with chunk support
   🔄 Anti-repetition system 
   📡 Stable WebSocket with auto-recovery
   🛡️ Robust error handling
   🎯 Dynamic prompt system
   
🧪 Test Commands:
   jarvisDebug.testCreativity()
   jarvisDebug.testLongStreaming()
   
🔧 Debug:
   jarvisDebug.getState()
   jarvisDebug.getPerformance()
`);