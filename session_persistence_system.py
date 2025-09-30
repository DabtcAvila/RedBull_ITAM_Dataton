#!/usr/bin/env python3
"""
INEGI Datatón - Sistema de Persistencia de Sesiones
Continuidad garantizada a través de múltiples sesiones

David Fernando Ávila Díaz - ITAM
"""

import asyncio
import json
import sqlite3
import time
import uuid
import pickle
import gzip
import base64
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
import threading
import logging
import hashlib

class PersistenceLevel(Enum):
    MINIMAL = "minimal"      # Solo objetivos críticos
    STANDARD = "standard"    # Objetivos + resultados clave
    COMPLETE = "complete"    # Todo el estado
    ENTERPRISE = "enterprise" # Con respaldo y versionado

class CheckpointType(Enum):
    AUTOMATIC = "automatic"   # Por tiempo/tokens
    MANUAL = "manual"        # Solicitado por usuario
    DELEGATION = "delegation" # Pre-delegación
    ERROR_RECOVERY = "error_recovery"
    MILESTONE = "milestone"   # Hitos importantes

@dataclass
class SessionCheckpoint:
    id: str
    session_id: str
    checkpoint_type: CheckpointType
    timestamp: str
    context_snapshot: Dict[str, Any]
    objectives_state: Dict[str, Any]
    accumulated_results: Dict[str, Any]
    agent_states: Dict[str, Any]
    system_metrics: Dict[str, Any]
    recovery_instructions: List[str]
    compression_level: int = 6
    version: str = "1.0"

@dataclass
class ContinuityBridge:
    """Puente de continuidad entre sesiones"""
    bridge_id: str
    source_session: str
    target_session: str
    transfer_timestamp: str
    critical_objectives: List[str]
    essential_context: Dict[str, Any]
    progress_mapping: Dict[str, float]
    success_criteria_met: List[str]
    pending_dependencies: List[str]

class SessionPersistenceManager:
    """Gestor avanzado de persistencia con múltiples niveles"""
    
    def __init__(self, 
                 persistence_level: PersistenceLevel = PersistenceLevel.ENTERPRISE,
                 checkpoint_interval: int = 300,  # 5 minutos
                 auto_cleanup_days: int = 30):
        
        self.persistence_level = persistence_level
        self.checkpoint_interval = checkpoint_interval
        self.auto_cleanup_days = auto_cleanup_days
        
        self.db_path = "dataton_persistence.db"
        self.backup_dir = Path("backups/sessions")
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        self.init_persistence_database()
        self.setup_persistence_logging()
        
        # Cache en memoria para acceso rápido
        self.active_checkpoints: Dict[str, SessionCheckpoint] = {}
        self.continuity_bridges: Dict[str, ContinuityBridge] = {}
        
        # Sistema de auto-checkpoint
        self.checkpoint_scheduler = None
        self.lock = threading.RLock()
        
        self.logger.info(f"🔒 PersistenceManager iniciado - Nivel: {persistence_level.value}")
    
    def init_persistence_database(self):
        """Inicializa base de datos de persistencia empresarial"""
        with sqlite3.connect(self.db_path) as conn:
            # Tabla principal de checkpoints
            conn.execute('''
                CREATE TABLE IF NOT EXISTS session_checkpoints (
                    id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    checkpoint_type TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    context_snapshot_compressed TEXT,
                    objectives_state TEXT,
                    accumulated_results TEXT,
                    agent_states TEXT,
                    system_metrics TEXT,
                    recovery_instructions TEXT,
                    compression_level INTEGER DEFAULT 6,
                    version TEXT DEFAULT '1.0',
                    file_size_bytes INTEGER,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    INDEX(session_id),
                    INDEX(timestamp),
                    INDEX(checkpoint_type)
                )
            ''')
            
            # Tabla de puentes de continuidad
            conn.execute('''
                CREATE TABLE IF NOT EXISTS continuity_bridges (
                    bridge_id TEXT PRIMARY KEY,
                    source_session TEXT NOT NULL,
                    target_session TEXT NOT NULL,
                    transfer_timestamp TEXT NOT NULL,
                    critical_objectives TEXT,
                    essential_context TEXT,
                    progress_mapping TEXT,
                    success_criteria_met TEXT,
                    pending_dependencies TEXT,
                    bridge_integrity_hash TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    INDEX(source_session),
                    INDEX(target_session)
                )
            ''')
            
            # Tabla de métricas de continuidad
            conn.execute('''
                CREATE TABLE IF NOT EXISTS continuity_metrics (
                    id TEXT PRIMARY KEY,
                    session_id TEXT,
                    metric_name TEXT,
                    metric_value REAL,
                    metric_unit TEXT,
                    timestamp TEXT,
                    checkpoint_id TEXT,
                    INDEX(session_id),
                    INDEX(metric_name),
                    FOREIGN KEY(checkpoint_id) REFERENCES session_checkpoints(id)
                )
            ''')
            
            # Tabla de eventos de recuperación
            conn.execute('''
                CREATE TABLE IF NOT EXISTS recovery_events (
                    id TEXT PRIMARY KEY,
                    session_id TEXT,
                    recovery_type TEXT,
                    source_checkpoint_id TEXT,
                    recovery_timestamp TEXT,
                    recovery_success BOOLEAN,
                    recovery_details TEXT,
                    time_to_recovery_seconds INTEGER,
                    data_integrity_score REAL,
                    INDEX(session_id),
                    FOREIGN KEY(source_checkpoint_id) REFERENCES session_checkpoints(id)
                )
            ''')
    
    def setup_persistence_logging(self):
        """Configuración de logging para persistencia"""
        log_dir = Path("logs/persistence")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger = logging.getLogger("SessionPersistence")
        self.logger.setLevel(logging.DEBUG)
        
        # Handler para eventos de persistencia
        persistence_handler = logging.FileHandler(log_dir / "persistence_events.log")
        persistence_handler.setLevel(logging.INFO)
        
        # Handler para recuperación
        recovery_handler = logging.FileHandler(log_dir / "recovery_events.log")
        recovery_handler.setLevel(logging.WARNING)
        
        # Handler para métricas
        metrics_handler = logging.FileHandler(log_dir / "continuity_metrics.log")
        metrics_handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - [%(levelname)s] - %(funcName)s - %(message)s'
        )
        
        for handler in [persistence_handler, recovery_handler, metrics_handler]:
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def compress_data(self, data: Dict[str, Any], compression_level: int = 6) -> str:
        """Comprime datos usando gzip y base64"""
        json_data = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
        compressed = gzip.compress(json_data.encode('utf-8'), compresslevel=compression_level)
        return base64.b64encode(compressed).decode('ascii')
    
    def decompress_data(self, compressed_data: str) -> Dict[str, Any]:
        """Descomprime datos desde base64 y gzip"""
        try:
            compressed_bytes = base64.b64decode(compressed_data.encode('ascii'))
            decompressed = gzip.decompress(compressed_bytes)
            return json.loads(decompressed.decode('utf-8'))
        except Exception as e:
            self.logger.error(f"Error decompressing data: {e}")
            return {}
    
    def create_checkpoint(self, 
                         session_id: str,
                         checkpoint_type: CheckpointType,
                         context_snapshot: Dict[str, Any],
                         objectives_state: Dict[str, Any],
                         accumulated_results: Dict[str, Any],
                         agent_states: Dict[str, Any] = None,
                         system_metrics: Dict[str, Any] = None,
                         recovery_instructions: List[str] = None) -> str:
        """Crea checkpoint completo de sesión"""
        
        checkpoint_id = f"chk_{uuid.uuid4().hex[:12]}"
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Preparar datos del checkpoint
        checkpoint_data = SessionCheckpoint(
            id=checkpoint_id,
            session_id=session_id,
            checkpoint_type=checkpoint_type,
            timestamp=timestamp,
            context_snapshot=context_snapshot,
            objectives_state=objectives_state,
            accumulated_results=accumulated_results,
            agent_states=agent_states or {},
            system_metrics=system_metrics or {},
            recovery_instructions=recovery_instructions or []
        )
        
        # Comprimir contexto si es necesario
        compressed_context = ""
        if self.persistence_level in [PersistenceLevel.COMPLETE, PersistenceLevel.ENTERPRISE]:
            compressed_context = self.compress_data(context_snapshot)
        
        # Calcular tamaño del archivo
        file_size = len(compressed_context.encode('utf-8'))
        
        try:
            with self.lock, sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT INTO session_checkpoints
                    (id, session_id, checkpoint_type, timestamp, context_snapshot_compressed,
                     objectives_state, accumulated_results, agent_states, system_metrics,
                     recovery_instructions, compression_level, version, file_size_bytes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    checkpoint_id, session_id, checkpoint_type.value, timestamp,
                    compressed_context, json.dumps(objectives_state),
                    json.dumps(accumulated_results), json.dumps(agent_states or {}),
                    json.dumps(system_metrics or {}), json.dumps(recovery_instructions or []),
                    checkpoint_data.compression_level, checkpoint_data.version, file_size
                ))
                
                # Cache en memoria
                self.active_checkpoints[checkpoint_id] = checkpoint_data
                
                self.logger.info(
                    f"💾 Checkpoint creado: {checkpoint_id} "
                    f"[{checkpoint_type.value}] - {file_size:,} bytes"
                )
                
                # Crear respaldo si es nivel enterprise
                if self.persistence_level == PersistenceLevel.ENTERPRISE:
                    self.create_backup_file(checkpoint_data)
        
        except Exception as e:
            self.logger.error(f"❌ Error creando checkpoint: {e}")
            return None
        
        return checkpoint_id
    
    def create_backup_file(self, checkpoint: SessionCheckpoint):
        """Crea archivo de respaldo físico"""
        backup_filename = f"{checkpoint.session_id}_{checkpoint.id}_{checkpoint.timestamp[:10]}.pkl.gz"
        backup_path = self.backup_dir / backup_filename
        
        try:
            with gzip.open(backup_path, 'wb') as f:
                pickle.dump(asdict(checkpoint), f, protocol=pickle.HIGHEST_PROTOCOL)
            
            self.logger.debug(f"💿 Backup creado: {backup_filename}")
        
        except Exception as e:
            self.logger.error(f"❌ Error creando backup: {e}")
    
    def create_continuity_bridge(self,
                               source_session: str,
                               target_session: str,
                               critical_objectives: List[str],
                               essential_context: Dict[str, Any],
                               progress_mapping: Dict[str, float]) -> str:
        """Crea puente de continuidad entre sesiones"""
        
        bridge_id = f"bridge_{uuid.uuid4().hex[:10]}"
        timestamp = datetime.now(timezone.utc).isoformat()
        
        bridge = ContinuityBridge(
            bridge_id=bridge_id,
            source_session=source_session,
            target_session=target_session,
            transfer_timestamp=timestamp,
            critical_objectives=critical_objectives,
            essential_context=essential_context,
            progress_mapping=progress_mapping,
            success_criteria_met=[],
            pending_dependencies=[]
        )
        
        # Calcular hash de integridad
        integrity_data = {
            'objectives': critical_objectives,
            'progress': progress_mapping,
            'timestamp': timestamp
        }
        integrity_hash = hashlib.sha256(
            json.dumps(integrity_data, sort_keys=True).encode()
        ).hexdigest()
        
        try:
            with self.lock, sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT INTO continuity_bridges
                    (bridge_id, source_session, target_session, transfer_timestamp,
                     critical_objectives, essential_context, progress_mapping,
                     success_criteria_met, pending_dependencies, bridge_integrity_hash)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    bridge_id, source_session, target_session, timestamp,
                    json.dumps(critical_objectives), json.dumps(essential_context),
                    json.dumps(progress_mapping), json.dumps([]), json.dumps([]),
                    integrity_hash
                ))
                
                self.continuity_bridges[bridge_id] = bridge
                
                self.logger.info(f"🌉 Puente de continuidad creado: {bridge_id}")
                self.logger.info(f"📊 {len(critical_objectives)} objetivos críticos transferidos")
        
        except Exception as e:
            self.logger.error(f"❌ Error creando puente de continuidad: {e}")
            return None
        
        return bridge_id
    
    def recover_session(self, checkpoint_id: str) -> Optional[Dict[str, Any]]:
        """Recupera sesión desde checkpoint"""
        recovery_start = time.time()
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('''
                    SELECT * FROM session_checkpoints WHERE id = ?
                ''', (checkpoint_id,))
                
                row = cursor.fetchone()
                if not row:
                    self.logger.error(f"❌ Checkpoint no encontrado: {checkpoint_id}")
                    return None
                
                # Reconstruir checkpoint
                checkpoint_data = {
                    'id': row[0],
                    'session_id': row[1],
                    'checkpoint_type': row[2],
                    'timestamp': row[3],
                    'objectives_state': json.loads(row[5]) if row[5] else {},
                    'accumulated_results': json.loads(row[6]) if row[6] else {},
                    'agent_states': json.loads(row[7]) if row[7] else {},
                    'system_metrics': json.loads(row[8]) if row[8] else {},
                    'recovery_instructions': json.loads(row[9]) if row[9] else []
                }
                
                # Descomprimir contexto si existe
                if row[4]:  # context_snapshot_compressed
                    checkpoint_data['context_snapshot'] = self.decompress_data(row[4])
                else:
                    checkpoint_data['context_snapshot'] = {}
                
                recovery_time = time.time() - recovery_start
                
                # Registrar evento de recuperación
                self.record_recovery_event(
                    session_id=checkpoint_data['session_id'],
                    recovery_type="checkpoint_recovery",
                    source_checkpoint_id=checkpoint_id,
                    recovery_success=True,
                    recovery_details=f"Recuperación exitosa en {recovery_time:.2f}s",
                    time_to_recovery=recovery_time
                )
                
                self.logger.info(
                    f"🔄 Sesión recuperada desde checkpoint: {checkpoint_id} "
                    f"({recovery_time:.2f}s)"
                )
                
                return checkpoint_data
        
        except Exception as e:
            self.logger.error(f"❌ Error recuperando sesión: {e}")
            
            # Registrar evento de recuperación fallida
            self.record_recovery_event(
                session_id="unknown",
                recovery_type="checkpoint_recovery",
                source_checkpoint_id=checkpoint_id,
                recovery_success=False,
                recovery_details=f"Error: {str(e)}",
                time_to_recovery=time.time() - recovery_start
            )
        
        return None
    
    def record_recovery_event(self,
                            session_id: str,
                            recovery_type: str,
                            source_checkpoint_id: str,
                            recovery_success: bool,
                            recovery_details: str,
                            time_to_recovery: float,
                            data_integrity_score: float = 1.0):
        """Registra evento de recuperación"""
        
        event_id = f"rec_{uuid.uuid4().hex[:8]}"
        timestamp = datetime.now(timezone.utc).isoformat()
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT INTO recovery_events
                    (id, session_id, recovery_type, source_checkpoint_id,
                     recovery_timestamp, recovery_success, recovery_details,
                     time_to_recovery_seconds, data_integrity_score)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    event_id, session_id, recovery_type, source_checkpoint_id,
                    timestamp, recovery_success, recovery_details,
                    int(time_to_recovery), data_integrity_score
                ))
        
        except Exception as e:
            self.logger.error(f"❌ Error registrando evento de recuperación: {e}")
    
    def get_session_checkpoints(self, session_id: str) -> List[Dict[str, Any]]:
        """Obtiene todos los checkpoints de una sesión"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('''
                    SELECT id, checkpoint_type, timestamp, file_size_bytes
                    FROM session_checkpoints
                    WHERE session_id = ?
                    ORDER BY timestamp DESC
                ''', (session_id,))
                
                checkpoints = []
                for row in cursor.fetchall():
                    checkpoints.append({
                        'id': row[0],
                        'type': row[1],
                        'timestamp': row[2],
                        'size_bytes': row[3]
                    })
                
                return checkpoints
        
        except Exception as e:
            self.logger.error(f"❌ Error obteniendo checkpoints: {e}")
            return []
    
    def cleanup_old_checkpoints(self, days_old: int = None):
        """Limpia checkpoints antiguos"""
        cleanup_days = days_old or self.auto_cleanup_days
        cutoff_date = (datetime.now(timezone.utc) - timedelta(days=cleanup_days)).isoformat()
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Contar checkpoints a eliminar
                cursor = conn.execute('''
                    SELECT COUNT(*) FROM session_checkpoints WHERE timestamp < ?
                ''', (cutoff_date,))
                count_to_delete = cursor.fetchone()[0]
                
                if count_to_delete > 0:
                    # Eliminar checkpoints antiguos
                    conn.execute('''
                        DELETE FROM session_checkpoints WHERE timestamp < ?
                    ''', (cutoff_date,))
                    
                    self.logger.info(f"🧹 {count_to_delete} checkpoints antiguos eliminados")
        
        except Exception as e:
            self.logger.error(f"❌ Error limpiando checkpoints: {e}")
    
    def get_continuity_metrics(self) -> Dict[str, Any]:
        """Obtiene métricas de continuidad del sistema"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Total de checkpoints
                cursor = conn.execute('SELECT COUNT(*) FROM session_checkpoints')
                total_checkpoints = cursor.fetchone()[0]
                
                # Checkpoints por tipo
                cursor = conn.execute('''
                    SELECT checkpoint_type, COUNT(*) FROM session_checkpoints
                    GROUP BY checkpoint_type
                ''')
                checkpoints_by_type = dict(cursor.fetchall())
                
                # Eventos de recuperación exitosos
                cursor = conn.execute('''
                    SELECT COUNT(*) FROM recovery_events WHERE recovery_success = 1
                ''')
                successful_recoveries = cursor.fetchone()[0]
                
                # Tiempo promedio de recuperación
                cursor = conn.execute('''
                    SELECT AVG(time_to_recovery_seconds) FROM recovery_events
                    WHERE recovery_success = 1
                ''')
                avg_recovery_time = cursor.fetchone()[0] or 0
                
                # Puentes de continuidad activos
                cursor = conn.execute('SELECT COUNT(*) FROM continuity_bridges')
                active_bridges = cursor.fetchone()[0]
                
                return {
                    'total_checkpoints': total_checkpoints,
                    'checkpoints_by_type': checkpoints_by_type,
                    'successful_recoveries': successful_recoveries,
                    'avg_recovery_time_seconds': avg_recovery_time,
                    'active_continuity_bridges': active_bridges,
                    'persistence_level': self.persistence_level.value,
                    'last_updated': datetime.now(timezone.utc).isoformat()
                }
        
        except Exception as e:
            self.logger.error(f"❌ Error obteniendo métricas: {e}")
            return {}

if __name__ == "__main__":
    print("🔒 Sistema de Persistencia de Sesiones - INEGI Datatón")
    print("👨‍💻 David Fernando Ávila Díaz - ITAM")
    print("=" * 60)
    
    # Demostrar sistema de persistencia
    persistence_manager = SessionPersistenceManager(
        persistence_level=PersistenceLevel.ENTERPRISE,
        checkpoint_interval=300
    )
    
    # Crear checkpoint de prueba
    test_checkpoint = persistence_manager.create_checkpoint(
        session_id="test_session_001",
        checkpoint_type=CheckpointType.MANUAL,
        context_snapshot={"test": "data", "objectives": ["obj1", "obj2"]},
        objectives_state={"obj1": {"progress": 0.5}, "obj2": {"progress": 0.3}},
        accumulated_results={"results": ["analysis_complete", "visualization_ready"]},
        system_metrics={"memory_usage": 512, "cpu_usage": 25.5}
    )
    
    print(f"✅ Checkpoint de prueba creado: {test_checkpoint}")
    
    # Obtener métricas
    metrics = persistence_manager.get_continuity_metrics()
    print(f"📊 Métricas del sistema:")
    for key, value in metrics.items():
        print(f"   - {key}: {value}")
    
    print("\n🔒 Sistema de Persistencia listo para Datatón INEGI")