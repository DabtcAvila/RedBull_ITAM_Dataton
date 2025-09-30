#!/usr/bin/env python3
"""
INEGI Datatón - Multi-Agent Orchestrator System
Enterprise-Grade AI Development Framework

David Fernando Ávila Díaz - ITAM
Sistema Infalible con Paralelismo Controlado (3-12 Agentes)
"""

import asyncio
import json
import logging
import time
import uuid
from datetime import datetime, timezone
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, List, Optional, Any, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from pathlib import Path

class AgentStatus(Enum):
    IDLE = "idle"
    WORKING = "working"
    COMPLETED = "completed"
    ERROR = "error"
    PAUSED = "paused"

class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class AgentMetrics:
    agent_id: str
    tasks_completed: int = 0
    tasks_failed: int = 0
    avg_execution_time: float = 0.0
    last_activity: str = ""
    tokens_used: int = 0
    success_rate: float = 0.0

@dataclass
class Task:
    id: str
    name: str
    description: str
    priority: TaskPriority
    agent_type: str
    data: Dict[str, Any]
    dependencies: List[str]
    created_at: str
    deadline: Optional[str] = None
    status: str = "pending"
    assigned_agent: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error_msg: Optional[str] = None

class SafeOrchestrator:
    """
    Sistema Orquestador Infalible con Límites de Seguridad
    Garantiza estabilidad enterprise con paralelismo controlado
    """
    
    def __init__(self, min_agents: int = 3, max_agents: int = 12):
        self.min_agents = min_agents
        self.max_agents = max_agents
        self.active_agents: Dict[str, Any] = {}
        self.task_queue: List[Task] = []
        self.completed_tasks: List[Task] = []
        self.failed_tasks: List[Task] = []
        self.metrics: Dict[str, AgentMetrics] = {}
        self.system_status = "initializing"
        self.lock = threading.RLock()
        self.executor = ThreadPoolExecutor(max_workers=max_agents)
        
        # Sistema de logs enterprise
        self.setup_logging()
        
        # Métricas del sistema
        self.start_time = datetime.now(timezone.utc)
        self.total_tasks_processed = 0
        self.system_uptime = 0
        
        # Handlers de eventos
        self.event_handlers: Dict[str, List[Callable]] = {
            'agent_started': [],
            'agent_completed': [],
            'agent_failed': [],
            'system_overload': [],
            'task_completed': [],
        }
        
        self.logger.info(f"🚀 SafeOrchestrator initialized: {min_agents}-{max_agents} agents")
    
    def setup_logging(self):
        """Configuración de logging enterprise con múltiples niveles"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Logger principal
        self.logger = logging.getLogger("SafeOrchestrator")
        self.logger.setLevel(logging.DEBUG)
        
        # Handler para archivo principal
        main_handler = logging.FileHandler(log_dir / "orchestrator.log")
        main_handler.setLevel(logging.INFO)
        
        # Handler para errores críticos
        error_handler = logging.FileHandler(log_dir / "errors.log")
        error_handler.setLevel(logging.ERROR)
        
        # Handler para métricas
        metrics_handler = logging.FileHandler(log_dir / "metrics.log")
        metrics_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s:%(lineno)d] - %(message)s'
        )
        
        main_handler.setFormatter(formatter)
        error_handler.setFormatter(formatter)
        metrics_handler.setFormatter(formatter)
        
        self.logger.addHandler(main_handler)
        self.logger.addHandler(error_handler)
        
        # Console handler para debugging
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
    
    def register_event_handler(self, event: str, handler: Callable):
        """Registra handlers para eventos del sistema"""
        if event in self.event_handlers:
            self.event_handlers[event].append(handler)
            self.logger.debug(f"Handler registrado para evento: {event}")
    
    def emit_event(self, event: str, data: Dict[str, Any]):
        """Emite eventos a todos los handlers registrados"""
        if event in self.event_handlers:
            for handler in self.event_handlers[event]:
                try:
                    handler(data)
                except Exception as e:
                    self.logger.error(f"Error en handler de evento {event}: {e}")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Obtiene el status completo del sistema"""
        with self.lock:
            current_time = datetime.now(timezone.utc)
            uptime = (current_time - self.start_time).total_seconds()
            
            return {
                "system_status": self.system_status,
                "uptime_seconds": uptime,
                "active_agents": len(self.active_agents),
                "max_agents": self.max_agents,
                "min_agents": self.min_agents,
                "pending_tasks": len([t for t in self.task_queue if t.status == "pending"]),
                "running_tasks": len([t for t in self.task_queue if t.status == "running"]),
                "completed_tasks": len(self.completed_tasks),
                "failed_tasks": len(self.failed_tasks),
                "total_processed": self.total_tasks_processed,
                "agent_metrics": {k: asdict(v) for k, v in self.metrics.items()},
                "memory_usage": self.get_memory_usage(),
                "last_updated": current_time.isoformat()
            }
    
    def get_memory_usage(self) -> Dict[str, Any]:
        """Monitoreo básico de memoria para prevenir crashes"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        
        return {
            "rss_mb": memory_info.rss / 1024 / 1024,
            "vms_mb": memory_info.vms / 1024 / 1024,
            "cpu_percent": process.cpu_percent(),
            "num_threads": process.num_threads()
        }
    
    def create_specialized_agent(self, agent_type: str, config: Dict[str, Any]) -> str:
        """Crea agentes especializados con configuraciones específicas"""
        if len(self.active_agents) >= self.max_agents:
            self.logger.warning(f"Límite de agentes alcanzado ({self.max_agents})")
            return None
        
        agent_id = f"{agent_type}_{uuid.uuid4().hex[:8]}"
        
        agent_config = {
            "id": agent_id,
            "type": agent_type,
            "status": AgentStatus.IDLE,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "config": config,
            "current_task": None,
            "last_heartbeat": time.time()
        }
        
        with self.lock:
            self.active_agents[agent_id] = agent_config
            self.metrics[agent_id] = AgentMetrics(agent_id=agent_id)
        
        self.logger.info(f"✅ Agente creado: {agent_id} ({agent_type})")
        self.emit_event("agent_started", {"agent_id": agent_id, "type": agent_type})
        
        return agent_id
    
    def add_task(self, task: Task) -> str:
        """Añade tarea al sistema con validación de dependencias"""
        with self.lock:
            # Validar dependencias
            for dep_id in task.dependencies:
                if not any(t.id == dep_id and t.status == "completed" 
                          for t in self.completed_tasks):
                    dep_pending = any(t.id == dep_id for t in self.task_queue)
                    if not dep_pending:
                        self.logger.error(f"Dependencia no encontrada: {dep_id}")
                        return None
            
            self.task_queue.append(task)
            self.logger.info(f"📋 Tarea añadida: {task.id} - {task.name}")
            return task.id
    
    def execute_task_safely(self, task: Task, agent_id: str) -> Dict[str, Any]:
        """Ejecuta tarea con manejo de errores y límites de tiempo"""
        start_time = time.time()
        
        try:
            with self.lock:
                if agent_id not in self.active_agents:
                    raise Exception(f"Agente no encontrado: {agent_id}")
                
                self.active_agents[agent_id]["status"] = AgentStatus.WORKING
                self.active_agents[agent_id]["current_task"] = task.id
                task.status = "running"
                task.assigned_agent = agent_id
            
            self.logger.info(f"🔄 Ejecutando: {task.name} con agente {agent_id}")
            
            # Simular ejecución de tarea (aquí iría la lógica real)
            result = self.simulate_agent_work(task, agent_id)
            
            execution_time = time.time() - start_time
            
            with self.lock:
                task.status = "completed"
                task.result = result
                self.completed_tasks.append(task)
                self.task_queue.remove(task)
                
                # Actualizar métricas
                metrics = self.metrics[agent_id]
                metrics.tasks_completed += 1
                metrics.last_activity = datetime.now(timezone.utc).isoformat()
                metrics.avg_execution_time = (
                    (metrics.avg_execution_time * (metrics.tasks_completed - 1) + execution_time) 
                    / metrics.tasks_completed
                )
                metrics.success_rate = (
                    metrics.tasks_completed / 
                    (metrics.tasks_completed + metrics.tasks_failed) * 100
                )
                
                self.active_agents[agent_id]["status"] = AgentStatus.COMPLETED
                self.active_agents[agent_id]["current_task"] = None
            
            self.logger.info(f"✅ Completada: {task.name} en {execution_time:.2f}s")
            self.emit_event("task_completed", {"task": task, "agent_id": agent_id})
            
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Error en tarea {task.name}: {e}")
            
            with self.lock:
                task.status = "failed"
                task.error_msg = str(e)
                self.failed_tasks.append(task)
                if task in self.task_queue:
                    self.task_queue.remove(task)
                
                if agent_id in self.metrics:
                    self.metrics[agent_id].tasks_failed += 1
                    self.metrics[agent_id].success_rate = (
                        self.metrics[agent_id].tasks_completed / 
                        (self.metrics[agent_id].tasks_completed + self.metrics[agent_id].tasks_failed) * 100
                    )
                
                if agent_id in self.active_agents:
                    self.active_agents[agent_id]["status"] = AgentStatus.ERROR
                    self.active_agents[agent_id]["current_task"] = None
            
            self.emit_event("agent_failed", {"agent_id": agent_id, "error": str(e)})
            return {"error": str(e)}
    
    def simulate_agent_work(self, task: Task, agent_id: str) -> Dict[str, Any]:
        """Simulación de trabajo del agente - aquí se integraría con Claude Code"""
        import random
        
        # Simular trabajo variable basado en tipo de tarea
        work_time = {
            "data_analysis": random.uniform(2, 8),
            "visualization": random.uniform(1, 5),
            "model_training": random.uniform(5, 15),
            "report_generation": random.uniform(1, 3),
            "code_review": random.uniform(0.5, 2),
        }.get(task.agent_type, random.uniform(1, 5))
        
        time.sleep(work_time)  # Simular procesamiento
        
        return {
            "status": "success",
            "execution_time": work_time,
            "agent_id": agent_id,
            "result_data": f"Resultado para {task.name}",
            "tokens_used": random.randint(100, 1000),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    async def run_orchestration_loop(self):
        """Loop principal de orquestación con seguridad anti-crash"""
        self.system_status = "running"
        self.logger.info("🎯 Iniciando loop de orquestación")
        
        try:
            while self.system_status == "running":
                await self.orchestration_cycle()
                await asyncio.sleep(1)  # Prevenir uso excesivo de CPU
                
        except KeyboardInterrupt:
            self.logger.info("🛑 Shutdown solicitado por usuario")
        except Exception as e:
            self.logger.critical(f"💥 Error crítico en orchestration loop: {e}")
            self.system_status = "error"
        finally:
            await self.shutdown_graceful()
    
    async def orchestration_cycle(self):
        """Ciclo individual de orquestación"""
        with self.lock:
            # Verificar salud del sistema
            if self.check_system_health():
                self.emit_event("system_overload", self.get_system_status())
                return
            
            # Procesar tareas pendientes
            ready_tasks = [
                task for task in self.task_queue 
                if task.status == "pending" and self.check_dependencies(task)
            ]
            
            # Ordenar por prioridad
            ready_tasks.sort(key=lambda x: x.priority.value, reverse=True)
            
            # Asignar a agentes disponibles
            idle_agents = [
                aid for aid, agent in self.active_agents.items()
                if agent["status"] == AgentStatus.IDLE
            ]
            
            # Crear agentes adicionales si es necesario y hay tareas
            if len(idle_agents) < len(ready_tasks) and len(self.active_agents) < self.max_agents:
                needed_agents = min(
                    len(ready_tasks) - len(idle_agents),
                    self.max_agents - len(self.active_agents)
                )
                
                for _ in range(needed_agents):
                    agent_type = ready_tasks[0].agent_type if ready_tasks else "general"
                    new_agent_id = self.create_specialized_agent(agent_type, {})
                    if new_agent_id:
                        idle_agents.append(new_agent_id)
            
            # Ejecutar tareas en paralelo
            futures = []
            for i, task in enumerate(ready_tasks[:len(idle_agents)]):
                agent_id = idle_agents[i]
                future = self.executor.submit(self.execute_task_safely, task, agent_id)
                futures.append(future)
            
            # No bloquear el loop esperando resultados
            if futures:
                self.logger.debug(f"🔄 {len(futures)} tareas ejecutándose en paralelo")
    
    def check_system_health(self) -> bool:
        """Verifica la salud del sistema para prevenir crashes"""
        memory = self.get_memory_usage()
        
        # Límites de seguridad
        if memory["rss_mb"] > 2048:  # 2GB límite
            self.logger.warning(f"⚠️ Alto uso de memoria: {memory['rss_mb']:.1f}MB")
            return True
            
        if memory["cpu_percent"] > 90:
            self.logger.warning(f"⚠️ Alto uso de CPU: {memory['cpu_percent']:.1f}%")
            return True
            
        if len(self.active_agents) > self.max_agents:
            self.logger.warning(f"⚠️ Demasiados agentes activos: {len(self.active_agents)}")
            return True
        
        return False
    
    def check_dependencies(self, task: Task) -> bool:
        """Verifica que todas las dependencias estén completadas"""
        for dep_id in task.dependencies:
            if not any(t.id == dep_id and t.status == "completed" for t in self.completed_tasks):
                return False
        return True
    
    async def shutdown_graceful(self):
        """Shutdown graceful del sistema"""
        self.logger.info("🔄 Iniciando shutdown graceful...")
        self.system_status = "shutting_down"
        
        # Esperar tareas en progreso
        running_tasks = [t for t in self.task_queue if t.status == "running"]
        if running_tasks:
            self.logger.info(f"⏳ Esperando {len(running_tasks)} tareas...")
            timeout = 30  # 30 segundos timeout
            while running_tasks and timeout > 0:
                await asyncio.sleep(1)
                timeout -= 1
                running_tasks = [t for t in self.task_queue if t.status == "running"]
        
        # Cerrar executor
        self.executor.shutdown(wait=True)
        
        # Log final
        final_status = self.get_system_status()
        self.logger.info(f"📊 Sistema finalizado: {json.dumps(final_status, indent=2)}")
        self.system_status = "stopped"

def create_inegi_dataton_workflow():
    """Crea workflow especializado para el Datatón del INEGI"""
    orchestrator = SafeOrchestrator(min_agents=3, max_agents=12)
    
    # Crear agentes especializados para análisis de datos INEGI
    agents_config = [
        ("data_analyst", {"specialization": "demographic_data", "inegi_apis": True}),
        ("visualization", {"tools": ["matplotlib", "plotly", "seaborn"], "inegi_themes": True}),
        ("statistical_modeler", {"focus": "socioeconomic_indicators"}),
        ("report_generator", {"format": ["pdf", "html", "jupyter"], "inegi_templates": True}),
        ("quality_assurance", {"validation": "statistical_significance"}),
    ]
    
    # Crear agentes base
    for agent_type, config in agents_config:
        orchestrator.create_specialized_agent(agent_type, config)
    
    return orchestrator

if __name__ == "__main__":
    # Demostración del sistema
    print("🚀 Iniciando Sistema Multi-Agente Infalible - INEGI Datatón")
    print("👨‍💻 Desarrollado por: David Fernando Ávila Díaz - ITAM")
    print("=" * 60)
    
    orchestrator = create_inegi_dataton_workflow()
    
    # Crear tareas de ejemplo
    sample_tasks = [
        Task(
            id="task_001",
            name="Análisis Demográfico Nacional",
            description="Análisis de datos demográficos del INEGI por entidad federativa",
            priority=TaskPriority.HIGH,
            agent_type="data_analysis",
            data={"dataset": "censo_poblacion_vivienda", "scope": "nacional"},
            dependencies=[],
            created_at=datetime.now(timezone.utc).isoformat()
        ),
        Task(
            id="task_002",
            name="Visualización Indicadores Socioeconómicos",
            description="Crear dashboards interactivos de indicadores clave",
            priority=TaskPriority.MEDIUM,
            agent_type="visualization",
            data={"charts": ["choropleth", "time_series", "scatter"]},
            dependencies=["task_001"],
            created_at=datetime.now(timezone.utc).isoformat()
        ),
    ]
    
    # Añadir tareas
    for task in sample_tasks:
        orchestrator.add_task(task)
    
    print(f"📋 {len(sample_tasks)} tareas añadidas al sistema")
    print("🎯 Sistema listo para Datatón INEGI")
    print("\nUsa 'asyncio.run(orchestrator.run_orchestration_loop())' para iniciar")