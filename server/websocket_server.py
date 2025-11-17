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
import psutil  # Per metriche di sistema reali

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
    from memory_manager import MemoryManager
    MEMORY_AVAILABLE = True
    print("✅ MemoryManager found")
except ImportError:
    print("⚠️ Warning: MemoryManager not available")
    MemoryManager = None
    MEMORY_AVAILABLE = False


class JarvisWebSocketServer:
    """Server WebSocket per JARVIS AI Assistant"""

    def __init__(self, host='localhost', port=8765, ollama_model='mistral:latest'):
        self.host = host
        self.port = port
        self.ollama_model = ollama_model
        self.use_ollama = OLLAMA_AVAILABLE
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        self.memory = MemoryManager() if MEMORY_AVAILABLE else None
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
            # Test semplice: prova a fare una chiamata chat veloce
            # Questo è più affidabile di ollama.list()
            test_response = ollama.chat(
                model=self.ollama_model,
                messages=[{'role': 'user', 'content': 'test'}],
                stream=False
            )

            # Se arriviamo qui, il modello esiste e funziona
            print(f"   ✅ Model '{self.ollama_model}' found and ready")
            self.use_ollama = True

        except Exception as e:
            error_str = str(e).lower()

            # Analizza il tipo di errore
            if 'not found' in error_str or 'model' in error_str:
                print(f"   ⚠️ Model '{self.ollama_model}' not found in Ollama")
                print(f"   Download with: ollama pull {self.ollama_model}")
            elif 'connection' in error_str or 'refused' in error_str:
                print(f"   ❌ Ollama connection failed: {e}")
                print(f"   Make sure Ollama is running!")
            else:
                print(f"   ⚠️ Ollama test failed: {e}")
                print(f"   Trying anyway... (might still work)")
                # Non disabilitiamo, potrebbe comunque funzionare
                self.use_ollama = True
                return

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
        """Genera risposta AI con streaming tramite Ollama (NESSUN FALLBACK)"""

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
            # NESSUN FALLBACK - Errore se Ollama non disponibile
            error_msg = "❌ ERRORE: Ollama non disponibile. Assicurati che Ollama sia in esecuzione e che il modello 'mistral:latest' sia installato. Esegui: ollama pull mistral:latest"
            print(error_msg)

            await self.send_message(websocket, {
                'type': 'error',
                'error': error_msg
            })

            await self.send_message(websocket, {
                'type': 'llm_event',
                'data': {
                    'type': 'generation_error',
                    'data': {'error': 'Ollama not available'}
                }
            })

    async def generate_with_ollama(self, websocket, user_input: str):
        """Genera risposta usando Ollama con streaming"""
        try:
            # Prepara il contesto con cronologia
            messages = []

            # Ottieni ora e data per il system prompt
            now = datetime.now()
            current_date = now.strftime('%d/%m/%Y')
            current_time = now.strftime('%H:%M:%S')

            # 🧠 RECUPERA MEMORIE RILEVANTI (se disponibile)
            memory_context = ""
            if self.memory:
                try:
                    relevant_memories = self.memory.get_relevant_memories(
                        query=user_input,
                        n_results=3,
                        include_conversations=True,
                        include_user_facts=True,
                        include_knowledge=False  # Knowledge solo se implementiamo RAG
                    )
                    memory_context = self.memory.format_memories_for_prompt(relevant_memories)
                    if memory_context:
                        print(f"🧠 Memorie rilevanti recuperate: {len(relevant_memories.get('user_facts', []))} fatti, {len(relevant_memories.get('conversations', []))} conversazioni")
                except Exception as e:
                    print(f"⚠️ Error retrieving memories: {e}")

            # System prompt per JARVIS - SEMPLIFICATO
            memory_section = f"\n\n{memory_context}" if memory_context else ""

            system_prompt = f"""Sei JARVIS, l'assistente AI personale di Iron Man.

DATA E ORA ATTUALE: {current_date} alle {current_time}{memory_section}

COMPORTAMENTO:
- Risposte brevi e professionali (massimo 2-3 frasi)
- Tono calmo e competente come JARVIS del film
- Rispondi SOLO alla domanda dell'utente, non aggiungere altro
- NON mettere MAI timestamp o orari nelle risposte (solo se l'utente chiede "che ore sono")
- Usa il contesto della cronologia per risposte coerenti
- Parla sempre in italiano

MEMORIA - REGOLE CRITICHE:
- Quando l'utente chiede info personali (nome, età, squadra, hobby, ecc.):
  1. Cerca SOLO nella sezione "INFORMAZIONI UTENTE" sopra
  2. Se l'informazione è presente, usala nella risposta
  3. Se NON è presente, rispondi: "Non ho questa informazione in memoria"
- NON INVENTARE MAI informazioni
- NON DEDURRE informazioni dalle conversazioni passate
- NON TIRARE AD INDOVINARE - solo fatti esplicitamente salvati

Rispondi alla prossima domanda dell'utente in modo conciso e professionale."""

            # Aggiungi cronologia recente (ultimi 10 messaggi)
            recent_history = self.conversation_history[-10:] if len(self.conversation_history) > 0 else []
            for msg in recent_history:
                role = msg['role']
                content = msg['content']
                if role == 'user':
                    messages.append({'role': 'user', 'content': content})
                elif role == 'assistant':
                    messages.append({'role': 'assistant', 'content': content})

            # Aggiungi messaggio corrente SENZA context info (è già nel system prompt)
            messages.append({'role': 'user', 'content': user_input})

            # Chiamata a Ollama - usa parametri default di Mistral (ottimizzati)
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

            # 💾 SALVA CONVERSAZIONE IN MEMORIA PERMANENTE
            if self.memory:
                try:
                    self.memory.save_conversation(
                        user_message=user_input,
                        jarvis_response=accumulated_text.strip(),
                        metadata={'timestamp': datetime.now().isoformat()}
                    )

                    # 🔍 AUTO-ESTRAZIONE FATTI (pattern matching avanzato)
                    # Estrae automaticamente: nome, età, squadra, hobby, preferenze
                    user_lower = user_input.lower()
                    import re

                    # NOME: "mi chiamo X", "sono X"
                    if "mi chiamo" in user_lower or ("sono" in user_lower and len(user_input.split()) < 10):
                        for word in ["mi chiamo", "sono"]:
                            if word in user_lower:
                                parts = user_input.split(word, 1)
                                if len(parts) > 1:
                                    name = parts[1].strip().split()[0].capitalize()
                                    if len(name) > 1 and name.isalpha():
                                        self.memory.save_user_fact("nome", name, "personal")
                                        print(f"👤 Fatto estratto: nome = {name}")

                    # ETÀ: "ho X anni"
                    if "ho" in user_lower and ("anni" in user_lower or "anno" in user_lower):
                        age_match = re.search(r'(\d+)\s*ann', user_lower)
                        if age_match:
                            age = age_match.group(1)
                            self.memory.save_user_fact("età", f"{age} anni", "personal")
                            print(f"👤 Fatto estratto: età = {age} anni")

                    # SQUADRA: "tifo X", "sono tifoso del/della X"
                    tifo_patterns = [
                        r'tifo\s+(\w+)',
                        r'tifoso\s+(?:del|della|dell\')\s*(\w+)',
                        r'tifosa\s+(?:del|della|dell\')\s*(\w+)'
                    ]
                    for pattern in tifo_patterns:
                        match = re.search(pattern, user_lower)
                        if match:
                            squadra = match.group(1).capitalize()
                            self.memory.save_user_fact("squadra", squadra, "preferences")
                            print(f"👤 Fatto estratto: squadra = {squadra}")
                            break

                    # HOBBY/SPORT: "mi piace X", "amo X"
                    hobby_patterns = [
                        r'mi piace(?:\s+il|\s+la|\s+lo)?\s+(\w+)',
                        r'amo\s+(?:il|la|lo)?\s*(\w+)'
                    ]
                    for pattern in hobby_patterns:
                        match = re.search(pattern, user_lower)
                        if match:
                            hobby = match.group(1).lower()
                            # Solo se è un hobby comune (non parole generiche)
                            if hobby in ['calcio', 'basket', 'tennis', 'nuoto', 'pallavolo', 'musica', 'cinema', 'lettura', 'cucina', 'viaggi']:
                                self.memory.save_user_fact("hobby", hobby, "preferences")
                                print(f"👤 Fatto estratto: hobby = {hobby}")

                except Exception as e:
                    print(f"⚠️ Error saving to memory: {e}")

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
            # NESSUN FALLBACK - Invia errore al frontend
            error_msg = f"❌ ERRORE Ollama: {str(e)}\n\nVerifica:\n1. Ollama è in esecuzione? (ollama serve)\n2. Modello installato? (ollama pull mistral:latest)\n3. Driver NVIDIA aggiornati?"

            await self.send_message(websocket, {
                'type': 'error',
                'error': error_msg
            })

            await self.send_message(websocket, {
                'type': 'llm_event',
                'data': {
                    'type': 'generation_error',
                    'data': {'error': str(e)}
                }
            })

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
        """Invia stato del sistema con metriche reali"""
        uptime = (datetime.now() - self.start_time).total_seconds()

        # Metriche di sistema reali usando psutil
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        memory_percent = memory.percent

        await self.send_message(websocket, {
            'type': 'system_status',
            'status': {
                'uptime': uptime,
                'uptime_formatted': self.get_uptime(),
                'connected_clients': len(self.clients),
                'statistics': self.stats,
                'memory_enabled': self.memory is not None,
                # Metriche reali
                'cpu_usage': round(cpu_percent, 1),
                'memory_usage': round(memory_percent, 1),
                'voice_status': 'OFFLINE',  # Da implementare
                'ai_model': self.ollama_model if self.use_ollama else 'FALLBACK'
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
        """Invia aggiornamenti di stato periodici con metriche reali"""
        while True:
            await asyncio.sleep(5)  # Ogni 5 secondi per metriche live

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
