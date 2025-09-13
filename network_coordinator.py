#!/usr/bin/env python3
"""
Network Coordinator for Distributed AI Brain System
Manages communication between laptop and Jetson devices
"""
import asyncio
import aiohttp
import json
import logging
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
import websockets
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('network_coordinator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('NetworkCoordinator')

class NetworkNode:
    """Represents a brain network node"""
    def __init__(self, node_id: str, hostname: str, port: int, capabilities: List[str]):
        self.node_id = node_id
        self.hostname = hostname
        self.port = port
        self.capabilities = capabilities
        self.status = "unknown"
        self.last_seen = None
        self.websocket = None
        self.performance_metrics = {}
        
    @property
    def url(self):
        return f"ws://{self.hostname}:{self.port}"
        
    def is_online(self) -> bool:
        return self.status == "online" and self.websocket is not None

class BrainNetworkCoordinator:
    """Coordinates distributed brain processing across multiple devices"""
    
    def __init__(self):
        self.nodes = self._initialize_nodes()
        self.task_queue = asyncio.Queue()
        self.results = {}
        self.coordination_active = False
        
    def _initialize_nodes(self) -> Dict[str, NetworkNode]:
        """Initialize known network nodes"""
        return {
            'laptop': NetworkNode(
                'laptop_main_brain',
                'localhost',
                8765,
                ['coordination', 'llm_processing', 'data_storage', 'web_dashboard']
            ),
            'jetson_orin': NetworkNode(
                'jetson_orin_edge',
                'jetson-orin.local',  # or use IP like '192.168.1.100'
                8766,
                ['computer_vision', 'gpu_inference', 'real_time_processing', 'heavy_ml']
            ),
            'jetson_2gb': NetworkNode(
                'jetson_2gb_sensors',
                'jetson-2gb.local',   # or use IP like '192.168.1.101'
                8767,
                ['sensor_monitoring', 'iot_control', 'lightweight_processing', 'data_collection']
            )
        }
    
    async def start_coordination(self):
        """Start the network coordination system"""
        logger.info("🌐 Starting Brain Network Coordinator...")
        logger.info(f"📡 Managing {len(self.nodes)} brain nodes")
        
        self.coordination_active = True
        
        # Start coordination tasks
        tasks = [
            asyncio.create_task(self._discovery_loop()),
            asyncio.create_task(self._health_monitoring_loop()),
            asyncio.create_task(self._task_distribution_loop()),
            asyncio.create_task(self._performance_monitoring_loop()),
            asyncio.create_task(self._websocket_server())
        ]
        
        try:
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            logger.info("🛑 Coordination stopped by user")
        finally:
            await self.cleanup()
    
    async def _discovery_loop(self):
        """Discover and connect to brain nodes"""
        while self.coordination_active:
            for node_id, node in self.nodes.items():
                if not node.is_online():
                    try:
                        await self._connect_to_node(node)
                    except Exception as e:
                        logger.debug(f"🔍 Discovery failed for {node_id}: {e}")
            
            await asyncio.sleep(5)  # Discovery every 5 seconds
    
    async def _connect_to_node(self, node: NetworkNode):
        """Attempt to connect to a brain node"""
        try:
            logger.info(f"🔌 Attempting to connect to {node.node_id} at {node.url}")
            
            websocket = await websockets.connect(
                node.url,
                timeout=3,
                ping_interval=20,
                ping_timeout=10
            )
            
            # Send handshake
            handshake = {
                'type': 'handshake',
                'coordinator_id': 'main_coordinator',
                'timestamp': datetime.now().isoformat()
            }
            await websocket.send(json.dumps(handshake))
            
            # Wait for response
            response = await asyncio.wait_for(websocket.recv(), timeout=5)
            response_data = json.loads(response)
            
            if response_data.get('type') == 'handshake_ack':
                node.websocket = websocket
                node.status = "online"
                node.last_seen = datetime.now()
                logger.info(f"✅ Connected to {node.node_id}")
                
                # Start listening for messages from this node
                asyncio.create_task(self._listen_to_node(node))
                
        except Exception as e:
            node.status = "offline"
            logger.debug(f"❌ Failed to connect to {node.node_id}: {e}")
    
    async def _listen_to_node(self, node: NetworkNode):
        """Listen for messages from a connected node"""
        try:
            async for message in node.websocket:
                await self._handle_node_message(node, json.loads(message))
        except websockets.exceptions.ConnectionClosed:
            logger.warning(f"🔌 Connection to {node.node_id} lost")
            node.status = "offline"
            node.websocket = None
        except Exception as e:
            logger.error(f"❌ Error listening to {node.node_id}: {e}")
            node.status = "error"
    
    async def _handle_node_message(self, node: NetworkNode, message: Dict[str, Any]):
        """Handle incoming message from a brain node"""
        message_type = message.get('type')
        
        if message_type == 'status_update':
            node.last_seen = datetime.now()
            node.performance_metrics = message.get('metrics', {})
            
        elif message_type == 'task_result':
            task_id = message.get('task_id')
            if task_id:
                self.results[task_id] = {
                    'node_id': node.node_id,
                    'result': message.get('result'),
                    'timestamp': datetime.now().isoformat()
                }
                logger.info(f"📥 Received result for task {task_id} from {node.node_id}")
                
        elif message_type == 'alert':
            logger.warning(f"⚠️  Alert from {node.node_id}: {message.get('alert')}")
    
    async def _health_monitoring_loop(self):
        """Monitor health of all brain nodes"""
        while self.coordination_active:
            current_time = datetime.now()
            
            for node_id, node in self.nodes.items():
                if node.is_online():
                    # Send ping
                    try:
                        ping_message = {
                            'type': 'ping',
                            'timestamp': current_time.isoformat()
                        }
                        await node.websocket.send(json.dumps(ping_message))
                        
                        # Check if node is responsive
                        if node.last_seen:
                            time_since_last_seen = (current_time - node.last_seen).total_seconds()
                            if time_since_last_seen > 30:  # 30 seconds timeout
                                logger.warning(f"⚠️  {node.node_id} appears unresponsive")
                                node.status = "unresponsive"
                                
                    except Exception as e:
                        logger.warning(f"🏥 Health check failed for {node.node_id}: {e}")
                        node.status = "offline"
                        node.websocket = None
            
            await asyncio.sleep(10)  # Health check every 10 seconds
    
    async def _task_distribution_loop(self):
        """Distribute tasks to appropriate brain nodes"""
        while self.coordination_active:
            try:
                # Get task from queue (with timeout)
                task = await asyncio.wait_for(self.task_queue.get(), timeout=1.0)
                
                # Find best node for this task
                best_node = self._select_best_node_for_task(task)
                
                if best_node and best_node.is_online():
                    try:
                        task_message = {
                            'type': 'task_assignment',
                            'task_id': task['task_id'],
                            'task_data': task,
                            'timestamp': datetime.now().isoformat()
                        }
                        await best_node.websocket.send(json.dumps(task_message))
                        logger.info(f"📤 Assigned task {task['task_id']} to {best_node.node_id}")
                        
                    except Exception as e:
                        logger.error(f"❌ Failed to send task to {best_node.node_id}: {e}")
                        # Put task back in queue for retry
                        await self.task_queue.put(task)
                else:
                    logger.warning(f"⚠️  No suitable node found for task {task.get('task_id')}")
                    # Put task back in queue for retry
                    await self.task_queue.put(task)
                    await asyncio.sleep(2)  # Wait before retry
                    
            except asyncio.TimeoutError:
                continue  # No tasks in queue, continue loop
    
    def _select_best_node_for_task(self, task: Dict[str, Any]) -> Optional[NetworkNode]:
        """Select the best node for a given task based on capabilities and load"""
        task_type = task.get('type', '')
        required_capabilities = task.get('capabilities', [])
        
        # Filter nodes by capabilities
        suitable_nodes = []
        for node in self.nodes.values():
            if node.is_online():
                # Check if node has required capabilities
                if any(cap in node.capabilities for cap in required_capabilities):
                    suitable_nodes.append(node)
        
        if not suitable_nodes:
            return None
        
        # Select node with lowest load (simplified - use CPU usage from metrics)
        best_node = min(suitable_nodes, key=lambda n: n.performance_metrics.get('cpu_usage', 0))
        return best_node
    
    async def _performance_monitoring_loop(self):
        """Monitor and log performance metrics"""
        while self.coordination_active:
            performance_summary = {}
            
            for node_id, node in self.nodes.items():
                performance_summary[node_id] = {
                    'status': node.status,
                    'last_seen': node.last_seen.isoformat() if node.last_seen else None,
                    'metrics': node.performance_metrics
                }
            
            # Log performance summary
            logger.info(f"📊 Network Performance: {len([n for n in self.nodes.values() if n.is_online()])}/{len(self.nodes)} nodes online")
            
            # Save to file for dashboard
            with open('network_status.json', 'w') as f:
                json.dump(performance_summary, f, indent=2)
            
            await asyncio.sleep(30)  # Performance monitoring every 30 seconds
    
    async def _websocket_server(self):
        """WebSocket server for external connections (dashboard, etc.)"""
        async def handle_client(websocket, path):
            try:
                async for message in websocket:
                    data = json.loads(message)
                    
                    if data.get('type') == 'status_request':
                        # Send network status
                        status = {
                            'type': 'network_status',
                            'nodes': {
                                node_id: {
                                    'status': node.status,
                                    'capabilities': node.capabilities,
                                    'metrics': node.performance_metrics
                                }
                                for node_id, node in self.nodes.items()
                            }
                        }
                        await websocket.send(json.dumps(status))
                        
            except websockets.exceptions.ConnectionClosed:
                pass
        
        # Start WebSocket server for dashboard connections
        start_server = websockets.serve(handle_client, "localhost", 8768)
        logger.info("🌐 WebSocket server started on localhost:8768")
        await start_server
    
    async def submit_task(self, task_type: str, task_data: Dict[str, Any], capabilities: List[str] = None):
        """Submit a task to the network"""
        task_id = f"task_{int(time.time() * 1000)}"
        task = {
            'task_id': task_id,
            'type': task_type,
            'data': task_data,
            'capabilities': capabilities or [],
            'submitted_at': datetime.now().isoformat()
        }
        
        await self.task_queue.put(task)
        logger.info(f"📝 Submitted task {task_id} of type {task_type}")
        return task_id
    
    async def get_result(self, task_id: str, timeout: float = 30.0) -> Optional[Dict[str, Any]]:
        """Get result for a specific task"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if task_id in self.results:
                return self.results.pop(task_id)
            await asyncio.sleep(0.1)
        
        return None
    
    def get_network_status(self) -> Dict[str, Any]:
        """Get current network status"""
        return {
            'coordinator_active': self.coordination_active,
            'nodes': {
                node_id: {
                    'status': node.status,
                    'capabilities': node.capabilities,
                    'last_seen': node.last_seen.isoformat() if node.last_seen else None,
                    'metrics': node.performance_metrics
                }
                for node_id, node in self.nodes.items()
            },
            'queue_size': self.task_queue.qsize(),
            'pending_results': len(self.results)
        }
    
    async def cleanup(self):
        """Clean up resources"""
        logger.info("🧹 Cleaning up network coordinator...")
        self.coordination_active = False
        
        # Close all WebSocket connections
        for node in self.nodes.values():
            if node.websocket:
                await node.websocket.close()

async def main():
    """Main function to start the network coordinator"""
    coordinator = BrainNetworkCoordinator()
    
    try:
        await coordinator.start_coordination()
    except KeyboardInterrupt:
        logger.info("🛑 Network coordinator stopped")

if __name__ == "__main__":
    asyncio.run(main())