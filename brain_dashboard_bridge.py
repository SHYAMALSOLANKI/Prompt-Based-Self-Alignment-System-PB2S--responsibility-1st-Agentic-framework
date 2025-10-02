#!/usr/bin/env python3
"""
Brain-Dashboard Integration Service
Enables real-time communication between autonomous brain and monitoring dashboard
"""
import json
import time
import threading
import asyncio
import websockets
from datetime import datetime
from pathlib import Path
import logging
from typing import Dict, List, Any

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BrainDashboardBridge:
    """Bridge service for brain-dashboard communication"""
    
    def __init__(self, port=8765):
        self.port = port
        self.clients = set()
        self.brain_state = {
            'status': 'offline',
            'last_heartbeat': None,
            'current_action': None,
            'capabilities_active': 0,
            'learning_progress': 0,
            'errors': [],
            'achievements': []
        }
        
    async def register_client(self, websocket, path):
        """Register a new dashboard client"""
        self.clients.add(websocket)
        logger.info(f"Dashboard client connected: {websocket.remote_address}")
        
        # Send current brain state
        await websocket.send(json.dumps({
            'type': 'brain_state',
            'data': self.brain_state
        }))
        
        try:
            async for message in websocket:
                await self.handle_client_message(websocket, message)
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.clients.remove(websocket)
            logger.info(f"Dashboard client disconnected")
    
    async def handle_client_message(self, websocket, message):
        """Handle messages from dashboard clients"""
        try:
            data = json.loads(message)
            msg_type = data.get('type')
            
            if msg_type == 'get_brain_state':
                await websocket.send(json.dumps({
                    'type': 'brain_state',
                    'data': self.brain_state
                }))
            elif msg_type == 'brain_command':
                # Forward command to brain (implement brain control)
                await self.send_brain_command(data.get('command'))
                
        except Exception as e:
            logger.error(f"Error handling client message: {e}")
    
    async def send_brain_command(self, command):
        """Send command to brain system"""
        # This would connect to brain's command interface
        logger.info(f"Brain command received: {command}")
        # For now, just log - implement actual brain control later
    
    async def broadcast_to_dashboard(self, message):
        """Broadcast message to all connected dashboard clients"""
        if self.clients:
            disconnected = set()
            for client in self.clients:
                try:
                    await client.send(json.dumps(message))
                except websockets.exceptions.ConnectionClosed:
                    disconnected.add(client)
            
            # Remove disconnected clients
            self.clients -= disconnected
    
    def update_brain_state(self, new_state: Dict[str, Any]):
        """Update brain state and notify dashboards"""
        self.brain_state.update(new_state)
        self.brain_state['last_heartbeat'] = datetime.now().isoformat()
        
        # Broadcast update asynchronously
        if self.clients:
            asyncio.create_task(self.broadcast_to_dashboard({
                'type': 'brain_state_update',
                'data': self.brain_state
            }))
    
    def monitor_brain_logs(self):
        """Monitor brain log file for updates"""
        log_file = Path("autonomous_brain.log")
        last_size = 0
        
        while True:
            try:
                if log_file.exists():
                    current_size = log_file.stat().st_size
                    if current_size > last_size:
                        # New log entries
                        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                            f.seek(last_size)
                            new_logs = f.read()
                            
                        # Parse and broadcast new logs
                        for line in new_logs.strip().split('\n'):
                            if line.strip():
                                self.parse_log_line(line)
                        
                        last_size = current_size
                        self.brain_state['status'] = 'active'
                    else:
                        # No new logs - check if brain is still active
                        if self.brain_state['last_heartbeat']:
                            last_update = datetime.fromisoformat(self.brain_state['last_heartbeat'])
                            if (datetime.now() - last_update).seconds > 60:
                                self.brain_state['status'] = 'inactive'
                else:
                    self.brain_state['status'] = 'offline'
                
                time.sleep(2)  # Check every 2 seconds
                
            except Exception as e:
                logger.error(f"Error monitoring brain logs: {e}")
                time.sleep(5)
    
    def parse_log_line(self, line: str):
        """Parse a log line and extract brain state information"""
        try:
            if "🧠 BRAIN CYCLE" in line:
                self.brain_state['current_action'] = "Thinking..."
            elif "✅" in line and "capability" in line.lower():
                self.brain_state['capabilities_active'] += 1
            elif "🎯 LEARNING" in line:
                self.brain_state['current_action'] = "Learning..."
            elif "ERROR" in line or "❌" in line:
                self.brain_state['errors'].append({
                    'timestamp': datetime.now().isoformat(),
                    'message': line.strip()
                })
            elif "🏆" in line or "achievement" in line.lower():
                self.brain_state['achievements'].append({
                    'timestamp': datetime.now().isoformat(),
                    'message': line.strip()
                })
            
            # Update heartbeat
            self.update_brain_state({})
            
        except Exception as e:
            logger.error(f"Error parsing log line: {e}")
    
    def start_server(self):
        """Start the WebSocket server"""
        logger.info(f"Starting Brain-Dashboard Bridge on port {self.port}")
        
        # Start log monitoring in background thread
        log_monitor = threading.Thread(target=self.monitor_brain_logs, daemon=True)
        log_monitor.start()
        
        # Start WebSocket server
        start_server = websockets.serve(self.register_client, "localhost", self.port)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

# Standalone service functions
def create_bridge_service():
    """Create and return bridge service instance"""
    return BrainDashboardBridge()

def start_bridge_service():
    """Start the bridge service"""
    bridge = create_bridge_service()
    bridge.start_server()

if __name__ == "__main__":
    print("🌉 Starting Brain-Dashboard Bridge Service...")
    print("🔗 This enables real-time communication between your brain and dashboard")
    print("📊 Dashboard clients can connect via WebSocket on port 8765")
    print("🧠 Monitoring brain logs for real-time updates...")
    print()
    
    try:
        start_bridge_service()
    except KeyboardInterrupt:
        print("\n👋 Bridge service stopped")
    except Exception as e:
        print(f"❌ Bridge service error: {e}")