#!/usr/bin/env python3
"""
INEGI Datatón - Sistema de Monitoreo y Logging Comprehensivo
Sistema de observabilidad enterprise con métricas en tiempo real

David Fernando Ávila Díaz - ITAM
"""

import asyncio
import json
import time
import uuid
import psutil
import threading
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, List, Optional, Any, Callable
from pathlib import Path
import logging
import sqlite3
import queue
import statistics
from collections import deque, defaultdict
import warnings
warnings.filterwarnings("ignore")

class AlertLevel(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class MetricType(Enum):
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    TIMER = "timer"

@dataclass
class SystemAlert:
    id: str
    level: AlertLevel
    component: str
    message: str
    timestamp: str
    metadata: Dict[str, Any]
    resolved: bool = False
    resolution_timestamp: Optional[str] = None

@dataclass
class PerformanceMetric:
    name: str
    value: float
    unit: str
    timestamp: str
    tags: Dict[str, str]
    metric_type: MetricType

@dataclass
class AgentHealthStatus:
    agent_id: str
    status: str
    last_heartbeat: str
    tasks_completed: int
    tasks_failed: int
    avg_response_time: float
    memory_usage_mb: float
    cpu_usage_percent: float
    error_rate: float

class RealTimeMonitor:
    """Monitor en tiempo real con alertas y métricas"""
    
    def __init__(self):
        self.metrics_queue = queue.Queue(maxsize=10000)
        self.alerts_queue = queue.Queue(maxsize=1000)
        self.active_alerts: Dict[str, SystemAlert] = {}
        
        # Métricas en memoria para acceso rápido
        self.metrics_buffer: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        self.agent_health: Dict[str, AgentHealthStatus] = {}
        
        # Callbacks para alertas
        self.alert_callbacks: List[Callable[[SystemAlert], None]] = []
        
        self.monitoring_active = False
        self.lock = threading.RLock()
    
    def start_monitoring(self):
        """Inicia monitoreo en tiempo real"""
        self.monitoring_active = True
        
        # Thread para procesamiento de métricas
        threading.Thread(target=self._process_metrics_loop, daemon=True).start()
        
        # Thread para procesamiento de alertas
        threading.Thread(target=self._process_alerts_loop, daemon=True).start()
        
        # Thread para monitoreo de sistema
        threading.Thread(target=self._system_monitoring_loop, daemon=True).start()
    
    def record_metric(self, name: str, value: float, unit: str = "", 
                     tags: Dict[str, str] = None, metric_type: MetricType = MetricType.GAUGE):
        """Registra métrica en tiempo real"""
        metric = PerformanceMetric(
            name=name,
            value=value,
            unit=unit,
            timestamp=datetime.now(timezone.utc).isoformat(),
            tags=tags or {},
            metric_type=metric_type
        )
        
        try:
            self.metrics_queue.put_nowait(metric)
        except queue.Full:
            pass  # Descartar métricas si la cola está llena
    
    def create_alert(self, level: AlertLevel, component: str, 
                    message: str, metadata: Dict[str, Any] = None):
        """Crea alerta del sistema"""
        alert = SystemAlert(
            id=f"alert_{uuid.uuid4().hex[:8]}",
            level=level,
            component=component,
            message=message,
            timestamp=datetime.now(timezone.utc).isoformat(),
            metadata=metadata or {}
        )
        
        try:
            self.alerts_queue.put_nowait(alert)
        except queue.Full:
            pass  # Descartar alertas si la cola está llena
    
    def update_agent_health(self, agent_id: str, status_data: Dict[str, Any]):
        """Actualiza estado de salud de agente"""
        with self.lock:
            self.agent_health[agent_id] = AgentHealthStatus(
                agent_id=agent_id,
                status=status_data.get('status', 'unknown'),
                last_heartbeat=datetime.now(timezone.utc).isoformat(),
                tasks_completed=status_data.get('tasks_completed', 0),
                tasks_failed=status_data.get('tasks_failed', 0),
                avg_response_time=status_data.get('avg_response_time', 0.0),
                memory_usage_mb=status_data.get('memory_usage_mb', 0.0),
                cpu_usage_percent=status_data.get('cpu_usage_percent', 0.0),
                error_rate=status_data.get('error_rate', 0.0)
            )
    
    def get_recent_metrics(self, metric_name: str, count: int = 100) -> List[float]:
        """Obtiene métricas recientes"""
        with self.lock:
            return list(self.metrics_buffer[metric_name])[-count:]
    
    def get_system_health_summary(self) -> Dict[str, Any]:
        """Obtiene resumen de salud del sistema"""
        with self.lock:
            active_agents = len(self.agent_health)
            healthy_agents = len([a for a in self.agent_health.values() if a.status == 'healthy'])
            
            avg_response_time = statistics.mean([
                a.avg_response_time for a in self.agent_health.values()
            ]) if self.agent_health else 0
            
            total_errors = sum(a.tasks_failed for a in self.agent_health.values())
            total_completed = sum(a.tasks_completed for a in self.agent_health.values())
            
            return {
                'active_agents': active_agents,
                'healthy_agents': healthy_agents,
                'health_ratio': healthy_agents / active_agents if active_agents > 0 else 0,
                'avg_response_time': avg_response_time,
                'total_tasks_completed': total_completed,
                'total_errors': total_errors,
                'error_rate': total_errors / (total_completed + total_errors) if (total_completed + total_errors) > 0 else 0,
                'active_alerts': len(self.active_alerts),
                'critical_alerts': len([a for a in self.active_alerts.values() if a.level == AlertLevel.CRITICAL]),
                'timestamp': datetime.now(timezone.utc).isoformat()
            }
    
    def _process_metrics_loop(self):
        """Loop de procesamiento de métricas"""
        while self.monitoring_active:
            try:
                metric = self.metrics_queue.get(timeout=1)
                
                with self.lock:
                    self.metrics_buffer[metric.name].append(metric.value)
                
                # Verificar umbrales y generar alertas
                self._check_metric_thresholds(metric)
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error procesando métrica: {e}")
    
    def _process_alerts_loop(self):
        """Loop de procesamiento de alertas"""
        while self.monitoring_active:
            try:
                alert = self.alerts_queue.get(timeout=1)
                
                with self.lock:
                    self.active_alerts[alert.id] = alert
                
                # Ejecutar callbacks
                for callback in self.alert_callbacks:
                    try:
                        callback(alert)
                    except Exception as e:
                        print(f"Error en callback de alerta: {e}")
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error procesando alerta: {e}")
    
    def _system_monitoring_loop(self):
        """Loop de monitoreo de sistema"""
        while self.monitoring_active:
            try:
                # Obtener métricas de sistema
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                
                # Registrar métricas
                self.record_metric("system.cpu_percent", cpu_percent, "%")
                self.record_metric("system.memory_percent", memory.percent, "%")
                self.record_metric("system.memory_used_gb", memory.used / (1024**3), "GB")
                self.record_metric("system.disk_percent", disk.percent, "%")
                
                # Verificar umbrales críticos
                if cpu_percent > 90:
                    self.create_alert(
                        AlertLevel.CRITICAL,
                        "system",
                        f"CPU usage crítico: {cpu_percent:.1f}%",
                        {"value": cpu_percent, "threshold": 90}
                    )
                
                if memory.percent > 85:
                    self.create_alert(
                        AlertLevel.WARNING,
                        "system",
                        f"Uso de memoria alto: {memory.percent:.1f}%",
                        {"value": memory.percent, "threshold": 85}
                    )
                
                time.sleep(5)  # Monitorear cada 5 segundos
                
            except Exception as e:
                print(f"Error en monitoreo de sistema: {e}")
                time.sleep(10)
    
    def _check_metric_thresholds(self, metric: PerformanceMetric):
        """Verifica umbrales de métricas y genera alertas"""
        thresholds = {
            "agent.response_time": {"warning": 5.0, "critical": 10.0},
            "agent.error_rate": {"warning": 0.05, "critical": 0.1},
            "agent.memory_usage": {"warning": 1024, "critical": 2048},
        }
        
        if metric.name in thresholds:
            threshold_config = thresholds[metric.name]
            
            if metric.value >= threshold_config.get("critical", float('inf')):
                self.create_alert(
                    AlertLevel.CRITICAL,
                    "agent",
                    f"{metric.name} crítico: {metric.value} {metric.unit}",
                    {"metric": metric.name, "value": metric.value, "threshold": threshold_config["critical"]}
                )
            elif metric.value >= threshold_config.get("warning", float('inf')):
                self.create_alert(
                    AlertLevel.WARNING,
                    "agent",
                    f"{metric.name} alto: {metric.value} {metric.unit}",
                    {"metric": metric.name, "value": metric.value, "threshold": threshold_config["warning"]}
                )

class ComprehensiveMonitoringSystem:
    """Sistema de monitoreo comprehensivo con persistencia y análisis"""
    
    def __init__(self, db_path: str = "monitoring.db"):
        self.db_path = db_path
        self.real_time_monitor = RealTimeMonitor()
        
        self.init_monitoring_database()
        self.setup_monitoring_logging()
        
        # Configurar callbacks
        self.real_time_monitor.alert_callbacks.append(self._handle_alert)
        
        # Métricas de rendimiento
        self.performance_tracker = PerformanceTracker()
        
        self.logger.info("🔍 Sistema de monitoreo comprehensivo iniciado")
    
    def init_monitoring_database(self):
        """Inicializa base de datos de monitoreo"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS performance_metrics (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    value REAL NOT NULL,
                    unit TEXT,
                    timestamp TEXT NOT NULL,
                    tags TEXT,
                    metric_type TEXT,
                    INDEX(name),
                    INDEX(timestamp)
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS system_alerts (
                    id TEXT PRIMARY KEY,
                    level TEXT NOT NULL,
                    component TEXT NOT NULL,
                    message TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    metadata TEXT,
                    resolved BOOLEAN DEFAULT 0,
                    resolution_timestamp TEXT,
                    INDEX(level),
                    INDEX(component),
                    INDEX(timestamp)
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS agent_health_history (
                    id TEXT PRIMARY KEY,
                    agent_id TEXT NOT NULL,
                    status TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    tasks_completed INTEGER,
                    tasks_failed INTEGER,
                    avg_response_time REAL,
                    memory_usage_mb REAL,
                    cpu_usage_percent REAL,
                    error_rate REAL,
                    INDEX(agent_id),
                    INDEX(timestamp)
                )
            ''')
    
    def setup_monitoring_logging(self):
        """Configuración de logging para monitoreo"""
        log_dir = Path("logs/monitoring")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger = logging.getLogger("ComprehensiveMonitoring")
        self.logger.setLevel(logging.DEBUG)
        
        # Handler para métricas
        metrics_handler = logging.FileHandler(log_dir / "metrics.log")
        metrics_handler.setLevel(logging.INFO)
        
        # Handler para alertas
        alerts_handler = logging.FileHandler(log_dir / "alerts.log")
        alerts_handler.setLevel(logging.WARNING)
        
        # Handler para análisis de rendimiento
        performance_handler = logging.FileHandler(log_dir / "performance_analysis.log")
        performance_handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - [%(levelname)s] - %(message)s'
        )
        
        for handler in [metrics_handler, alerts_handler, performance_handler]:
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def start(self):
        """Inicia el sistema de monitoreo"""
        self.real_time_monitor.start_monitoring()
        self.performance_tracker.start()
        
        # Thread para persistencia periódica
        threading.Thread(target=self._persistence_loop, daemon=True).start()
        
        self.logger.info("🚀 Sistema de monitoreo iniciado")
    
    def _handle_alert(self, alert: SystemAlert):
        """Maneja alertas del sistema"""
        self.logger.log(
            logging.CRITICAL if alert.level == AlertLevel.CRITICAL else logging.WARNING,
            f"ALERTA [{alert.level.value.upper()}] {alert.component}: {alert.message}"
        )
        
        # Guardar alerta en base de datos
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO system_alerts
                (id, level, component, message, timestamp, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                alert.id, alert.level.value, alert.component, alert.message,
                alert.timestamp, json.dumps(alert.metadata)
            ))
    
    def _persistence_loop(self):
        """Loop para persistir métricas periódicamente"""
        while True:
            try:
                time.sleep(60)  # Persistir cada minuto
                self._persist_metrics()
                self._persist_agent_health()
            except Exception as e:
                self.logger.error(f"Error en persistencia: {e}")
    
    def _persist_metrics(self):
        """Persiste métricas en base de datos"""
        with sqlite3.connect(self.db_path) as conn:
            # Obtener métricas del buffer
            metrics_to_persist = []
            
            with self.real_time_monitor.lock:
                for metric_name, values in self.real_time_monitor.metrics_buffer.items():
                    if values:
                        # Tomar muestra representativa
                        recent_values = list(values)[-10:]  # Últimos 10 valores
                        avg_value = statistics.mean(recent_values)
                        
                        metrics_to_persist.append((
                            f"metric_{uuid.uuid4().hex[:8]}",
                            metric_name,
                            avg_value,
                            "",  # unit
                            datetime.now(timezone.utc).isoformat(),
                            json.dumps({}),  # tags
                            MetricType.GAUGE.value
                        ))
            
            if metrics_to_persist:
                conn.executemany('''
                    INSERT INTO performance_metrics
                    (id, name, value, unit, timestamp, tags, metric_type)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', metrics_to_persist)
    
    def _persist_agent_health(self):
        """Persiste estado de salud de agentes"""
        with sqlite3.connect(self.db_path) as conn:
            with self.real_time_monitor.lock:
                for agent_id, health in self.real_time_monitor.agent_health.items():
                    conn.execute('''
                        INSERT INTO agent_health_history
                        (id, agent_id, status, timestamp, tasks_completed, tasks_failed,
                         avg_response_time, memory_usage_mb, cpu_usage_percent, error_rate)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        f"health_{uuid.uuid4().hex[:8]}",
                        agent_id,
                        health.status,
                        datetime.now(timezone.utc).isoformat(),
                        health.tasks_completed,
                        health.tasks_failed,
                        health.avg_response_time,
                        health.memory_usage_mb,
                        health.cpu_usage_percent,
                        health.error_rate
                    ))
    
    def get_monitoring_dashboard_data(self) -> Dict[str, Any]:
        """Obtiene datos para dashboard de monitoreo"""
        health_summary = self.real_time_monitor.get_system_health_summary()
        performance_metrics = self.performance_tracker.get_performance_summary()
        
        # Obtener alertas recientes
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT level, COUNT(*) FROM system_alerts
                WHERE timestamp > datetime('now', '-1 hour')
                GROUP BY level
            ''')
            recent_alerts = dict(cursor.fetchall())
        
        return {
            'health_summary': health_summary,
            'performance_metrics': performance_metrics,
            'recent_alerts': recent_alerts,
            'agent_details': {
                agent_id: asdict(health) 
                for agent_id, health in self.real_time_monitor.agent_health.items()
            },
            'timestamp': datetime.now(timezone.utc).isoformat()
        }

class PerformanceTracker:
    """Tracker de rendimiento con análisis de tendencias"""
    
    def __init__(self):
        self.start_time = time.time()
        self.request_times: deque = deque(maxlen=1000)
        self.error_count = 0
        self.success_count = 0
        self.active = False
    
    def start(self):
        """Inicia tracking de rendimiento"""
        self.active = True
        self.start_time = time.time()
    
    def record_request_time(self, duration: float):
        """Registra tiempo de request"""
        if self.active:
            self.request_times.append(duration)
    
    def record_success(self):
        """Registra operación exitosa"""
        self.success_count += 1
    
    def record_error(self):
        """Registra error"""
        self.error_count += 1
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Obtiene resumen de rendimiento"""
        if not self.request_times:
            return {
                'avg_response_time': 0,
                'min_response_time': 0,
                'max_response_time': 0,
                'total_requests': 0,
                'success_rate': 0,
                'error_rate': 0,
                'uptime_seconds': time.time() - self.start_time
            }
        
        total_requests = self.success_count + self.error_count
        
        return {
            'avg_response_time': statistics.mean(self.request_times),
            'min_response_time': min(self.request_times),
            'max_response_time': max(self.request_times),
            'median_response_time': statistics.median(self.request_times),
            'p95_response_time': sorted(self.request_times)[int(0.95 * len(self.request_times))] if len(self.request_times) > 20 else max(self.request_times),
            'total_requests': total_requests,
            'success_count': self.success_count,
            'error_count': self.error_count,
            'success_rate': self.success_count / total_requests if total_requests > 0 else 0,
            'error_rate': self.error_count / total_requests if total_requests > 0 else 0,
            'uptime_seconds': time.time() - self.start_time,
            'requests_per_second': total_requests / (time.time() - self.start_time) if (time.time() - self.start_time) > 0 else 0
        }

if __name__ == "__main__":
    print("🔍 Sistema de Monitoreo Comprehensivo - INEGI Datatón")
    print("👨‍💻 David Fernando Ávila Díaz - ITAM")
    print("=" * 60)
    
    # Inicializar sistema de monitoreo
    monitoring_system = ComprehensiveMonitoringSystem()
    monitoring_system.start()
    
    print("✅ Sistema de monitoreo iniciado")
    print("📊 Monitoreando métricas en tiempo real...")
    print("🚨 Sistema de alertas activo")
    
    # Simular algunas métricas para demostración
    monitor = monitoring_system.real_time_monitor
    
    # Simular métricas de agentes
    monitor.update_agent_health("agent_001", {
        'status': 'healthy',
        'tasks_completed': 25,
        'tasks_failed': 1,
        'avg_response_time': 2.5,
        'memory_usage_mb': 512,
        'cpu_usage_percent': 15.5,
        'error_rate': 0.04
    })
    
    # Registrar algunas métricas
    monitor.record_metric("agent.response_time", 2.5, "s")
    monitor.record_metric("agent.memory_usage", 512, "MB")
    
    # Crear alerta de prueba
    monitor.create_alert(
        AlertLevel.INFO,
        "test",
        "Sistema de monitoreo funcionando correctamente",
        {"component": "monitoring_system", "status": "operational"}
    )
    
    time.sleep(2)  # Esperar procesamiento
    
    # Obtener dashboard de datos
    dashboard_data = monitoring_system.get_monitoring_dashboard_data()
    print(f"\n📋 Estado del sistema:")
    print(f"   - Agentes activos: {dashboard_data['health_summary']['active_agents']}")
    print(f"   - Agentes saludables: {dashboard_data['health_summary']['healthy_agents']}")
    print(f"   - Alertas activas: {dashboard_data['health_summary']['active_alerts']}")
    
    print("\n🔍 Sistema de monitoreo listo para Datatón INEGI")