#!/usr/bin/env python3
"""
JARVIS WebSocket Server - Backend con streaming creativo
=========================================================
Server WebSocket che gestisce la comunicazione tra frontend e Ollama/Mistral
Supporta streaming in tempo reale delle risposte AI
"""

import asyncio
import websockets
import json
import logging
import time
from datetime import datetime
from llm_client import OllamaClient

# Configurazione logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class JarvisWebSocketServer:
    """Server WebSocket per JARVIS Assistant"""

    def __init__(self, host='localhost', port=8765, model='mistral'):
        self.host = host
        self.port = port
        self.clients = set()
        self.llm = OllamaClient(model=model)
        self.statistics = {
            'messages_processed': 0,
            'streaming_chunks_sent': 0,
            'errors': 0
        }
        self.start_time = time.time()

    async def register(self, websocket):
        """Registra un nuovo client"""
        self.clients.add(websocket)
        logger.info(f"Nuovo client connesso. Totale: {len(self.clients)}")

        # Invia messaggio di benvenuto
        await self.send_message(websocket, {
            'type': 'connection_established',
            'message': 'Connesso a JARVIS Core',
            'features': {
                'creative_mode': True,
                'stable_streaming': True,
                'model': 'mistral'
            }
        })

    async def unregister(self, websocket):
        """Rimuove un client disconnesso"""
        self.clients.discard(websocket)
        logger.info(f"Client disconnesso. Totale: {len(self.clients)}")

    async def send_message(self, websocket, message):
        """Invia un messaggio JSON al client"""
        try:
            await websocket.send(json.dumps(message))
        except Exception as e:
            logger.error(f"Errore invio messaggio: {e}")

    async def handle_text_command(self, websocket, data):
        """
        Gestisce un comando testuale e invia la risposta in streaming
        """
        try:
            user_text = data.get('text', '')
            logger.info(f"Elaborazione comando: {user_text[:50]}...")

            # Invia evento di inizio generazione
            await self.send_message(websocket, {
                'type': 'llm_event',
                'data': {
                    'type': 'generation_started',
                    'data': {'query': user_text}
                }
            })

            # Genera la risposta usando Ollama
            try:
                full_response = self.llm.prompt(user_text)

                # Simula streaming dividendo la risposta in chunk
                # (Ollama run non supporta streaming nativo, quindi lo simuliamo)
                chunk_size = 10  # parole per chunk
                words = full_response.split()
                chunks = [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

                accumulated_text = ""
                for i, chunk in enumerate(chunks):
                    accumulated_text += (' ' if accumulated_text else '') + chunk

                    # Invia chunk
                    await self.send_message(websocket, {
                        'type': 'ai_response_chunk',
                        'chunk': chunk + (' ' if i < len(chunks) - 1 else ''),
                        'chunk_number': i + 1,
                        'is_final': False,
                        'creativity_mode': True
                    })

                    # Invia anche formato streaming_update (per compatibilità)
                    await self.send_message(websocket, {
                        'type': 'streaming_update',
                        'text': accumulated_text,
                        'is_final': False,
                        'creativity_mode': True
                    })

                    self.statistics['streaming_chunks_sent'] += 1

                    # Delay per simulare streaming naturale
                    await asyncio.sleep(0.1)

                # Invia risposta finale
                await self.send_message(websocket, {
                    'type': 'ai_response_final',
                    'response': full_response,
                    'creativity_mode': True
                })

                # Invia ultimo streaming_update
                await self.send_message(websocket, {
                    'type': 'streaming_update',
                    'text': full_response,
                    'is_final': True,
                    'creativity_mode': True
                })

                # Evento completamento
                await self.send_message(websocket, {
                    'type': 'llm_event',
                    'data': {
                        'type': 'generation_completed',
                        'data': {
                            'response_length': len(full_response),
                            'chunks_sent': len(chunks),
                            'creativity_score': 0.85
                        }
                    }
                })

                self.statistics['messages_processed'] += 1
                logger.info(f"Risposta completata: {len(chunks)} chunks inviati")

            except Exception as e:
                logger.error(f"Errore LLM: {e}")
                await self.send_message(websocket, {
                    'type': 'error',
                    'error': f'Errore nel generare la risposta: {str(e)}'
                })

                await self.send_message(websocket, {
                    'type': 'llm_event',
                    'data': {
                        'type': 'generation_error',
                        'data': {'error': str(e)}
                    }
                })
                self.statistics['errors'] += 1

        except Exception as e:
            logger.error(f"Errore handle_text_command: {e}")
            await self.send_message(websocket, {
                'type': 'error',
                'error': str(e)
            })

    async def handle_ping(self, websocket):
        """Risponde ai ping del client"""
        await self.send_message(websocket, {'type': 'pong'})

    async def handle_system_status(self, websocket):
        """Invia statistiche di sistema"""
        uptime = time.time() - self.start_time
        await self.send_message(websocket, {
            'type': 'system_status',
            'status': {
                'uptime': uptime,
                'uptime_formatted': f'{int(uptime//3600)}h {int((uptime%3600)//60)}m',
                'connected_clients': len(self.clients),
                'statistics': self.statistics
            }
        })

    async def handle_message(self, websocket, message_str):
        """
        Gestisce i messaggi ricevuti dal client
        """
        try:
            message = json.loads(message_str)
            msg_type = message.get('type', '')

            logger.debug(f"Messaggio ricevuto: {msg_type}")

            if msg_type == 'text_command':
                await self.handle_text_command(websocket, message)

            elif msg_type == 'ping':
                await self.handle_ping(websocket)

            elif msg_type == 'system_status_request':
                await self.handle_system_status(websocket)

            else:
                logger.warning(f"Tipo messaggio sconosciuto: {msg_type}")

        except json.JSONDecodeError as e:
            logger.error(f"Errore parsing JSON: {e}")
            await self.send_message(websocket, {
                'type': 'error',
                'error': 'Messaggio JSON non valido'
            })
        except Exception as e:
            logger.error(f"Errore gestione messaggio: {e}")
            await self.send_message(websocket, {
                'type': 'error',
                'error': str(e)
            })

    async def handler(self, websocket, path):
        """
        Handler principale per ogni connessione WebSocket
        """
        await self.register(websocket)

        try:
            async for message in websocket:
                await self.handle_message(websocket, message)
        except websockets.exceptions.ConnectionClosed:
            logger.info("Connessione chiusa dal client")
        except Exception as e:
            logger.error(f"Errore nella connessione: {e}")
        finally:
            await self.unregister(websocket)

    async def start(self):
        """
        Avvia il server WebSocket
        """
        logger.info("="*60)
        logger.info("🚀 JARVIS WebSocket Server - Avvio")
        logger.info("="*60)
        logger.info(f"Host: {self.host}")
        logger.info(f"Porta: {self.port}")
        logger.info(f"Modello LLM: mistral (via Ollama)")
        logger.info("Modalità creativa: ATTIVA")
        logger.info("="*60)

        async with websockets.serve(self.handler, self.host, self.port):
            logger.info(f"✅ Server WebSocket in ascolto su ws://{self.host}:{self.port}")
            logger.info("Pronto per ricevere connessioni...")
            await asyncio.Future()  # run forever


def main():
    """
    Funzione principale per avviare il server
    """
    server = JarvisWebSocketServer(
        host='localhost',
        port=8765,
        model='mistral'
    )

    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        logger.info("\n🛑 Server interrotto dall'utente")
    except Exception as e:
        logger.error(f"❌ Errore fatale: {e}")


if __name__ == '__main__':
    main()
