"""
JARVIS WebSocket Server - Python Backend
=========================================
Server WebSocket per comunicazione real-time con frontend Electron.
Supporta streaming, creatività, e memoria semantica.

Porta: 8765 (come richiesto da app.js)
"""

import asyncio
import json
import websockets
import random
from datetime import datetime
from typing import Set, Dict, Any
import sys
import os

# Aggiungi la directory corrente al path per importare i moduli
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Prova a importare Ollama
try:
    import ollama
    OLLAMA_AVAILABLE = True
    print("✅ Ollama library found")
except ImportError:
    OLLAMA_AVAILABLE = False
    print("⚠️ Warning: Ollama not installed. Using fallback mode.")
    print("   Install with: pip install ollama")

try:
    from memory_semantic import SemanticMemory
except ImportError:
    print("⚠️ Warning: SemanticMemory not available, using simple memory")
    SemanticMemory = None


class JarvisWebSocketServer:
    """Server WebSocket per JARVIS AI Assistant"""

    def __init__(self, host='localhost', port=8765, ollama_model='mistral:latest'):
        self.host = host
        self.port = port
        self.ollama_model = ollama_model
        self.use_ollama = OLLAMA_AVAILABLE
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        self.memory = SemanticMemory() if SemanticMemory else None
        self.conversation_history = []
        self.start_time = datetime.now()

        # Statistiche
        self.stats = {
            'messages_processed': 0,
            'streaming_chunks_sent': 0,
            'total_clients_connected': 0
        }

        print(f"🚀 JARVIS WebSocket Server initialized")
        print(f"📡 Will listen on {host}:{port}")

        # Verifica Ollama
        if self.use_ollama:
            print(f"🧠 AI Mode: Ollama ({self.ollama_model})")
            self.test_ollama_connection()
        else:
            print(f"🧠 AI Mode: Fallback (hardcoded responses)")

    def test_ollama_connection(self):
        """Testa la connessione a Ollama"""
        try:
            # Prova a listare i modelli disponibili
            models = ollama.list()
            model_names = [m['name'] for m in models.get('models', [])]

            if self.ollama_model in model_names:
                print(f"   ✅ Model '{self.ollama_model}' found and ready")
            else:
                print(f"   ⚠️ Model '{self.ollama_model}' not found in Ollama")
                print(f"   Available models: {', '.join(model_names) if model_names else 'None'}")
                print(f"   Download with: ollama pull {self.ollama_model}")
                self.use_ollama = False
        except Exception as e:
            print(f"   ❌ Ollama connection failed: {e}")
            print(f"   Make sure Ollama is running!")
            self.use_ollama = False

    async def register(self, websocket):
        """Registra un nuovo client"""
        self.clients.add(websocket)
        self.stats['total_clients_connected'] += 1
        print(f"✅ Client connected. Total clients: {len(self.clients)}")

        # Invia messaggio di benvenuto
        await self.send_message(websocket, {
            'type': 'connection_established',
            'message': 'Connected to JARVIS Core',
            'features': {
                'creative_mode': True,
                'stable_streaming': True,
                'anti_repetition': True,
                'semantic_memory': self.memory is not None
            }
        })

    async def unregister(self, websocket):
        """Rimuovi client disconnesso"""
        self.clients.discard(websocket)
        print(f"❌ Client disconnected. Total clients: {len(self.clients)}")

    async def send_message(self, websocket, message: Dict[str, Any]):
        """Invia un messaggio JSON al client"""
        try:
            await websocket.send(json.dumps(message))
        except Exception as e:
            print(f"❌ Error sending message: {e}")

    async def broadcast(self, message: Dict[str, Any]):
        """Invia messaggio a tutti i client connessi"""
        if self.clients:
            await asyncio.gather(
                *[self.send_message(client, message) for client in self.clients],
                return_exceptions=True
            )

    async def handle_text_command(self, websocket, data: Dict[str, Any]):
        """Gestisce comando testuale dall'utente"""
        text = data.get('text', '')
        if not text:
            return

        print(f"💬 User: {text}")
        self.stats['messages_processed'] += 1

        # Salva nella cronologia
        self.conversation_history.append({
            'role': 'user',
            'content': text,
            'timestamp': datetime.now().isoformat()
        })

        # Genera risposta con streaming
        await self.generate_response_streaming(websocket, text)

    async def generate_response_streaming(self, websocket, user_input: str):
        """Genera risposta AI con streaming tramite Ollama o fallback"""

        # Evento: generazione iniziata
        await self.send_message(websocket, {
            'type': 'llm_event',
            'data': {
                'type': 'generation_started',
                'data': {'using_ollama': self.use_ollama}
            }
        })

        if self.use_ollama:
            # USA OLLAMA per risposta intelligente
            await self.generate_with_ollama(websocket, user_input)
        else:
            # Fallback: risposte hardcoded
            await self.generate_with_fallback(websocket, user_input)

    async def generate_with_ollama(self, websocket, user_input: str):
        """Genera risposta usando Ollama con streaming"""
        try:
            # Prepara il contesto con cronologia
            messages = []

            # System prompt per JARVIS
            system_prompt = """Sei JARVIS (Just A Rather Very Intelligent System), un assistente AI avanzato ispirato a quello di Iron Man.
Caratteristiche:
- Professionale ma amichevole
- Conciso ma completo
- Usa un tono leggermente formale ma non robotico
- Rispondi SEMPRE in italiano (a meno che l'utente non parli un'altra lingua)
- Quando appropriato, mostra personalità
- Sei capace di ricordare le conversazioni passate"""

            # Aggiungi cronologia recente (ultimi 10 messaggi)
            recent_history = self.conversation_history[-10:] if len(self.conversation_history) > 0 else []
            for msg in recent_history:
                role = msg['role']
                content = msg['content']
                if role == 'user':
                    messages.append({'role': 'user', 'content': content})
                elif role == 'assistant':
                    messages.append({'role': 'assistant', 'content': content})

            # Aggiungi messaggio corrente
            messages.append({'role': 'user', 'content': user_input})

            # Chiamata a Ollama con streaming
            accumulated_text = ""
            chunk_count = 0

            stream = ollama.chat(
                model=self.ollama_model,
                messages=[{'role': 'system', 'content': system_prompt}] + messages,
                stream=True
            )

            for chunk in stream:
                if 'message' in chunk and 'content' in chunk['message']:
                    content = chunk['message']['content']
                    accumulated_text += content
                    chunk_count += 1

                    # Invia chunk al frontend
                    await self.send_message(websocket, {
                        'type': 'ai_response_chunk',
                        'chunk': content,
                        'chunk_number': chunk_count,
                        'is_final': False,
                        'creativity_mode': True
                    })

                    self.stats['streaming_chunks_sent'] += 1

            # Salva in cronologia
            self.conversation_history.append({
                'role': 'assistant',
                'content': accumulated_text.strip(),
                'timestamp': datetime.now().isoformat()
            })

            # Salva in memoria
            if self.memory:
                try:
                    self.memory.add(f"User: {user_input} | JARVIS: {accumulated_text.strip()}")
                except:
                    pass

            # Messaggio finale
            await self.send_message(websocket, {
                'type': 'ai_response_final',
                'response': accumulated_text.strip(),
                'creativity_mode': True
            })

            # Evento completamento
            await self.send_message(websocket, {
                'type': 'llm_event',
                'data': {
                    'type': 'generation_completed',
                    'data': {
                        'creativity_score': 0.9,
                        'tokens_generated': chunk_count
                    }
                }
            })

            print(f"🤖 JARVIS (Ollama): {accumulated_text.strip()[:100]}...")

        except Exception as e:
            print(f"❌ Ollama error: {e}")
            # Fallback in caso di errore
            await self.generate_with_fallback(websocket, user_input)

    async def generate_with_fallback(self, websocket, user_input: str):
        """Genera risposta con logica hardcoded (fallback)"""

        # Sistema anti-ripetizione - risposte creative varie
        greetings = [
            "Ciao! Come posso aiutarti oggi?",
            "Salve! Sono JARVIS, il tuo assistente personale. Cosa posso fare per te?",
            "Buongiorno! JARVIS è online e pronto ad assisterti.",
            "Eccomi qui! In cosa posso esserti utile?",
            "Ciao! Sono pronto a rispondere alle tue domande."
        ]

        questions_about_jarvis = [
            "Sono JARVIS, un assistente AI avanzato creato per aiutarti. Posso rispondere a domande, gestire informazioni e supportarti in vari compiti. La mia memoria semantica mi permette di ricordare le nostre conversazioni passate.",
            "Mi chiamo JARVIS - Just A Rather Very Intelligent System. Sono qui per assisterti con qualsiasi cosa tu abbia bisogno, dall'organizzazione delle informazioni alle risposte a domande complesse.",
            "Sono un assistente AI progettato per essere il tuo compagno digitale affidabile. Utilizzo memoria semantica avanzata e posso apprendere dalle nostre interazioni."
        ]

        time_responses = [
            f"Sono online da {self.get_uptime()}. Tutto funziona perfettamente!",
            f"Il sistema è attivo da {self.get_uptime()} e tutti i componenti sono operativi.",
            f"Uptime corrente: {self.get_uptime()}. Status: Operativo al 100%."
        ]

        # Logica semplice di risposta
        user_lower = user_input.lower()

        if any(word in user_lower for word in ['ciao', 'salve', 'buongiorno', 'buonasera', 'hello', 'hey']):
            response = random.choice(greetings)

        elif any(word in user_lower for word in ['chi sei', 'cosa sei', 'presentati', 'who are you', 'what are you']):
            response = random.choice(questions_about_jarvis)

        elif any(word in user_lower for word in ['come stai', 'tutto bene', 'how are you']):
            response = "Sto funzionando perfettamente! Tutti i sistemi sono operativi. Come posso aiutarti?"

        elif any(word in user_lower for word in ['ore', 'ora', 'tempo', 'time']):
            current_time = datetime.now().strftime('%H:%M:%S')
            response = f"Sono le {current_time}. " + random.choice(time_responses)

        elif any(word in user_lower for word in ['uptime', 'quanto tempo', 'da quanto']):
            response = random.choice(time_responses)

        elif any(word in user_lower for word in ['grazie', 'thanks', 'thank you']):
            response = "Prego! Sono sempre qui per aiutarti. Se hai altre domande, non esitare a chiedere!"

        else:
            # Risposta generica
            responses = [
                f"Ho ricevuto la tua richiesta: '{user_input}'. Al momento sono in modalità fallback. Attiva Ollama per risposte intelligenti!",
                f"Interessante! '{user_input}' - Per risposte AI avanzate, assicurati che Ollama sia attivo e configurato.",
                f"Ho capito: '{user_input}'. Nota: Sto usando risposte pre-programmate. Configura Ollama per funzionalità complete!"
            ]
            response = random.choice(responses)

        # Salva risposta in memoria
        if self.memory:
            try:
                self.memory.add(f"User: {user_input} | JARVIS: {response}")
            except:
                pass

        self.conversation_history.append({
            'role': 'assistant',
            'content': response,
            'timestamp': datetime.now().isoformat()
        })

        # STREAMING della risposta
        await self.stream_response(websocket, response)

    async def stream_response(self, websocket, response: str):
        """Invia la risposta in modalità streaming (chunk per chunk)"""

        # Evento: generazione iniziata
        await self.send_message(websocket, {
            'type': 'llm_event',
            'data': {
                'type': 'generation_started',
                'data': {}
            }
        })

        # Dividi la risposta in chunks (parole)
        words = response.split()
        accumulated_text = ""

        for i, word in enumerate(words):
            accumulated_text += word + " "

            # Invia chunk
            await self.send_message(websocket, {
                'type': 'ai_response_chunk',
                'chunk': word + " ",
                'chunk_number': i + 1,
                'is_final': False,
                'creativity_mode': True
            })

            self.stats['streaming_chunks_sent'] += 1

            # Piccolo delay per effetto streaming realistico
            await asyncio.sleep(0.05)  # 50ms tra parole

        # Messaggio finale completo
        await self.send_message(websocket, {
            'type': 'ai_response_final',
            'response': accumulated_text.strip(),
            'creativity_mode': True
        })

        # Evento: generazione completata
        creativity_score = random.uniform(0.7, 0.95)
        await self.send_message(websocket, {
            'type': 'llm_event',
            'data': {
                'type': 'generation_completed',
                'data': {
                    'creativity_score': creativity_score,
                    'tokens_generated': len(words)
                }
            }
        })

        print(f"🤖 JARVIS: {accumulated_text.strip()}")

    async def handle_ping(self, websocket):
        """Risponde a ping con pong"""
        await self.send_message(websocket, {'type': 'pong'})

    async def handle_message(self, websocket, message: str):
        """Gestisce messaggi in arrivo dai client"""
        try:
            data = json.loads(message)
            msg_type = data.get('type', '')

            # Routing dei messaggi
            if msg_type == 'text_command':
                await self.handle_text_command(websocket, data)

            elif msg_type == 'ping':
                await self.handle_ping(websocket)

            elif msg_type == 'get_status':
                await self.send_system_status(websocket)

            else:
                print(f"⚠️ Unknown message type: {msg_type}")

        except json.JSONDecodeError:
            print(f"❌ Invalid JSON received: {message}")
        except Exception as e:
            print(f"❌ Error handling message: {e}")
            await self.send_message(websocket, {
                'type': 'error',
                'error': str(e)
            })

    async def send_system_status(self, websocket):
        """Invia stato del sistema"""
        uptime = (datetime.now() - self.start_time).total_seconds()

        await self.send_message(websocket, {
            'type': 'system_status',
            'status': {
                'uptime': uptime,
                'uptime_formatted': self.get_uptime(),
                'connected_clients': len(self.clients),
                'statistics': self.stats,
                'memory_enabled': self.memory is not None
            }
        })

    def get_uptime(self) -> str:
        """Calcola uptime formattato"""
        delta = datetime.now() - self.start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)

        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"

    async def handler(self, websocket):
        """Handler principale per connessioni WebSocket"""
        await self.register(websocket)

        try:
            async for message in websocket:
                await self.handle_message(websocket, message)

        except websockets.exceptions.ConnectionClosed:
            print("🔌 Connection closed normally")

        except Exception as e:
            print(f"❌ Error in handler: {e}")

        finally:
            await self.unregister(websocket)

    async def periodic_status_broadcast(self):
        """Invia aggiornamenti di stato periodici"""
        while True:
            await asyncio.sleep(30)  # Ogni 30 secondi

            if self.clients:
                for client in self.clients:
                    await self.send_system_status(client)

    async def start(self):
        """Avvia il server WebSocket"""
        print(f"\n{'='*60}")
        print(f"🚀 Starting JARVIS WebSocket Server")
        print(f"📡 Host: {self.host}")
        print(f"🔌 Port: {self.port}")
        print(f"🧠 Semantic Memory: {'Enabled' if self.memory else 'Disabled'}")
        print(f"{'='*60}\n")

        # Avvia server
        async with websockets.serve(self.handler, self.host, self.port):
            print(f"✅ Server running on ws://{self.host}:{self.port}")
            print(f"💡 Waiting for connections...\n")

            # Avvia task di broadcast periodico
            asyncio.create_task(self.periodic_status_broadcast())

            # Mantieni il server in esecuzione
            await asyncio.Future()  # Run forever


async def main():
    """Funzione principale"""
    server = JarvisWebSocketServer(host='localhost', port=8765)
    await server.start()


if __name__ == "__main__":
    try:
        print("\n🎯 JARVIS WebSocket Server - Starting...\n")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
