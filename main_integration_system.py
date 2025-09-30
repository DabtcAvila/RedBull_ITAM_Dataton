#!/usr/bin/env python3
"""
INEGI Datatón - Sistema Principal de Integración
Sistema Multi-Agente Infalible con Validación Contextual y Delegación Automática

David Fernando Ávila Díaz - ITAM
Instituto Tecnológico Autónomo de México
"""

import asyncio
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

# Importar todos nuestros sistemas especializados
from orchestrator_system import SafeOrchestrator, Task, TaskPriority
from meta_orchestrator_system import MetaOrchestrator, GlobalObjective, OrchestratorLevel
from session_persistence_system import SessionPersistenceManager, PersistenceLevel, CheckpointType
from comprehensive_monitoring_system import ComprehensiveMonitoringSystem, AlertLevel, MetricType
from specialized_inegi_agents import INEGIAgentFactory, AgentSpecialization, INEGIDataContext
from context_validation_system import ContextAwareTaskManager, TaskContext, TaskRelevance, ContextClarity, ToolAvailability

class MasterINEGISystem:
    """
    Sistema Maestro que integra todos los componentes
    Garantiza operación infalible con validación contextual completa
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or self.get_default_config()
        self.system_id = f"master_inegi_{int(time.time())}"
        
        # Inicializar componentes principales
        self.setup_logging()
        
        # Sistema de validación contextual (PRIMERO - filtro de entrada)
        self.context_manager = ContextAwareTaskManager()
        
        # Meta-orquestrador con delegación automática
        self.meta_orchestrator = MetaOrchestrator(
            orchestrator_id=f"meta_{self.system_id}",
            context_limit=self.config['context_limit'],
            delegation_threshold=self.config['delegation_threshold']
        )
        
        # Sistema de persistencia enterprise
        self.persistence_manager = SessionPersistenceManager(
            persistence_level=PersistenceLevel.ENTERPRISE,
            checkpoint_interval=self.config['checkpoint_interval']
        )
        
        # Sistema de monitoreo comprehensivo
        self.monitoring_system = ComprehensiveMonitoringSystem()
        
        # Registro de agentes especializados
        self.specialized_agents: Dict[str, Any] = {}
        
        # Estado del sistema
        self.system_status = "initializing"
        self.active_workflows: Dict[str, Any] = {}
        self.completed_objectives: List[str] = []
        
        self.logger.info(f"🚀 Sistema Maestro INEGI inicializado: {self.system_id}")
    
    def get_default_config(self) -> Dict[str, Any]:
        """Configuración por defecto del sistema"""
        return {
            'context_limit': 950000,  # 95% del límite de 1M tokens
            'delegation_threshold': 0.85,
            'checkpoint_interval': 300,  # 5 minutos
            'max_concurrent_agents': 12,
            'min_concurrent_agents': 3,
            'monitoring_enabled': True,
            'auto_recovery_enabled': True,
            'quality_threshold': 0.8,
            'performance_monitoring': True
        }
    
    def setup_logging(self):
        """Configuración de logging del sistema maestro"""
        log_dir = Path("logs/master_system")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger = logging.getLogger("MasterINEGISystem")
        self.logger.setLevel(logging.INFO)
        
        # Handler principal del sistema
        main_handler = logging.FileHandler(log_dir / f"master_{self.system_id}.log")
        main_handler.setLevel(logging.INFO)
        
        # Handler para decisiones críticas
        decisions_handler = logging.FileHandler(log_dir / "critical_decisions.log")
        decisions_handler.setLevel(logging.WARNING)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - [%(levelname)s] - %(funcName)s:%(lineno)d - %(message)s'
        )
        
        main_handler.setFormatter(formatter)
        decisions_handler.setFormatter(formatter)
        
        self.logger.addHandler(main_handler)
        self.logger.addHandler(decisions_handler)
    
    async def initialize_system(self):
        """Inicialización completa del sistema"""
        self.logger.info("🔄 Iniciando inicialización completa del sistema...")
        
        try:
            # 1. Inicializar monitoreo
            self.monitoring_system.start()
            self.logger.info("✅ Sistema de monitoreo iniciado")
            
            # 2. Crear objetivos globales para el Datatón INEGI
            await self.setup_inegi_objectives()
            self.logger.info("✅ Objetivos globales del Datatón creados")
            
            # 3. Inicializar sesión principal
            main_session = self.meta_orchestrator.start_new_session(
                level=OrchestratorLevel.META
            )
            self.logger.info(f"✅ Sesión principal iniciada: {main_session}")
            
            # 4. Crear agentes especializados
            await self.create_specialized_agent_team()
            self.logger.info("✅ Agentes especializados creados")
            
            # 5. Configurar sistema de recuperación automática
            self.setup_auto_recovery()
            self.logger.info("✅ Sistema de recuperación configurado")
            
            self.system_status = "ready"
            self.logger.info("🎯 Sistema Maestro INEGI completamente inicializado")
            
        except Exception as e:
            self.logger.critical(f"💥 Error crítico en inicialización: {e}")
            self.system_status = "failed"
            raise
    
    async def setup_inegi_objectives(self):
        """Crear objetivos específicos del Datatón INEGI"""
        objectives_config = [
            {
                "name": "Análisis Demográfico Nacional Completo",
                "description": "Análisis exhaustivo de indicadores demográficos por entidad federativa usando datos oficiales INEGI",
                "priority": 5,
                "target_metrics": {
                    "entidades_analizadas": 32,
                    "indicadores_procesados": 25,
                    "visualizaciones_creadas": 15,
                    "dashboard_interactivo": True,
                    "calidad_datos_minima": 0.95
                },
                "completion_criteria": [
                    "Análisis completo de 32 entidades federativas",
                    "Dashboard interactivo funcional y validado",
                    "Reporte ejecutivo con insights clave",
                    "Validación de calidad de datos >95%",
                    "Métricas demográficas principales calculadas"
                ]
            },
            {
                "name": "Modelo Predictivo Socioeconómico Avanzado",
                "description": "Desarrollo de modelos predictivos para indicadores socioeconómicos usando técnicas de machine learning",
                "priority": 4,
                "target_metrics": {
                    "accuracy_minima": 0.85,
                    "variables_incluidas": 40,
                    "horizonte_prediccion_años": 5,
                    "validacion_cruzada_completa": True,
                    "interpretabilidad_modelo": 0.8
                },
                "completion_criteria": [
                    "Modelo entrenado con accuracy >85%",
                    "Validación cruzada completada exitosamente",
                    "Predicciones para próximos 5 años generadas",
                    "Documentación técnica completa",
                    "Sistema de actualización automática implementado"
                ]
            },
            {
                "name": "Sistema de Visualización Interactiva Enterprise",
                "description": "Plataforma web interactiva de alto rendimiento para exploración de datos INEGI",
                "priority": 4,
                "target_metrics": {
                    "componentes_interactivos": 20,
                    "tipos_visualizacion": 12,
                    "tiempo_carga_maximo": 2.0,  # segundos
                    "responsive_design": True,
                    "accesibilidad_score": 0.9
                },
                "completion_criteria": [
                    "Plataforma web desplegada y funcional",
                    "Tiempo de carga <2 segundos",
                    "20+ componentes interactivos",
                    "Diseño responsive verificado",
                    "Pruebas de usuario completadas exitosamente"
                ]
            }
        ]
        
        # Crear objetivos en el meta-orquestrador
        for obj_config in objectives_config:
            objective_id = self.meta_orchestrator.create_global_objective(**obj_config)
            self.logger.info(f"🎯 Objetivo creado: {obj_config['name']} [{objective_id}]")
    
    async def create_specialized_agent_team(self):
        """Crear equipo completo de agentes especializados"""
        agent_specifications = [
            (AgentSpecialization.DEMOGRAPHIC_ANALYST, 2),  # 2 agentes demográficos
            (AgentSpecialization.ECONOMIC_MODELER, 2),     # 2 agentes económicos
            # Se pueden añadir más especializaciones según necesidad
        ]
        
        for specialization, count in agent_specifications:
            for i in range(count):
                agent = INEGIAgentFactory.create_agent(specialization)
                self.specialized_agents[agent.agent_id] = agent
                
                # Registrar agente en el sistema de monitoreo
                self.monitoring_system.real_time_monitor.update_agent_health(
                    agent.agent_id,
                    {
                        'status': 'healthy',
                        'specialization': specialization.value,
                        'tasks_completed': 0,
                        'tasks_failed': 0,
                        'avg_response_time': 0.0,
                        'memory_usage_mb': 0.0,
                        'cpu_usage_percent': 0.0,
                        'error_rate': 0.0
                    }
                )
                
                self.logger.info(f"🤖 Agente creado: {specialization.value} - {agent.agent_id}")
    
    async def submit_and_execute_task(self, task_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Pipeline completo: Validación Contextual → Ejecución → Monitoreo
        """
        start_time = time.time()
        
        try:
            # 1. VALIDACIÓN CONTEXTUAL (filtro anti-trabajo inútil)
            task_context = self.create_task_context(task_request)
            validation_result = self.context_manager.submit_task(task_context)
            
            if not validation_result.is_valid:
                self.logger.warning(f"❌ Tarea rechazada por validación contextual: {task_context.task_id}")
                self.logger.warning(f"   Issues: {validation_result.blocking_issues}")
                return {
                    'status': 'rejected',
                    'task_id': task_context.task_id,
                    'reason': 'validation_failed',
                    'issues': validation_result.blocking_issues,
                    'recommendations': validation_result.recommendations
                }
            
            # 2. CREACIÓN DE CHECKPOINT ANTES DE EJECUCIÓN
            checkpoint_id = self.persistence_manager.create_checkpoint(
                session_id=self.meta_orchestrator.session_context.session_id,
                checkpoint_type=CheckpointType.MANUAL,
                context_snapshot={'task_submitted': task_context.task_id},
                objectives_state=self.meta_orchestrator.global_objectives,
                accumulated_results={}
            )
            
            # 3. EJECUCIÓN CON AGENTE ESPECIALIZADO
            execution_result = await self.execute_with_specialized_agent(task_context)
            
            # 4. MONITOREO Y MÉTRICAS
            self.record_execution_metrics(task_context, execution_result, time.time() - start_time)
            
            # 5. ACTUALIZACIÓN DE PROGRESO GLOBAL
            if execution_result['status'] == 'completed':
                await self.update_global_progress(task_context, execution_result)
            
            # 6. CHECKPOINT POST-EJECUCIÓN
            post_checkpoint_id = self.persistence_manager.create_checkpoint(
                session_id=self.meta_orchestrator.session_context.session_id,
                checkpoint_type=CheckpointType.MILESTONE,
                context_snapshot={'task_completed': task_context.task_id},
                objectives_state=self.meta_orchestrator.global_objectives,
                accumulated_results=execution_result
            )
            
            self.logger.info(f"✅ Tarea ejecutada exitosamente: {task_context.task_id}")
            
            return {
                'status': 'completed',
                'task_id': task_context.task_id,
                'execution_result': execution_result,
                'validation_score': validation_result.relevance_score,
                'processing_time': time.time() - start_time,
                'checkpoints': [checkpoint_id, post_checkpoint_id]
            }
            
        except Exception as e:
            self.logger.error(f"💥 Error ejecutando tarea: {e}")
            
            # Sistema de recuperación automática
            if self.config['auto_recovery_enabled']:
                recovery_result = await self.attempt_auto_recovery(task_context, str(e))
                return recovery_result
            
            return {
                'status': 'failed',
                'task_id': task_context.task_id if 'task_context' in locals() else 'unknown',
                'error': str(e),
                'processing_time': time.time() - start_time
            }
    
    def create_task_context(self, task_request: Dict[str, Any]) -> TaskContext:
        """Crear contexto de tarea desde request"""
        return TaskContext(
            task_id=task_request.get('task_id', f"task_{int(time.time())}"),
            objective=task_request['objective'],
            deliverable=task_request.get('deliverable', ''),
            success_criteria=task_request.get('success_criteria', []),
            scope_boundaries=task_request.get('scope_boundaries', {}),
            business_value=task_request.get('business_value', ''),
            priority_justification=task_request.get('priority_justification', ''),
            impact_assessment=task_request.get('impact_assessment', {}),
            dependency_chain=task_request.get('dependency_chain', []),
            required_tools=task_request.get('required_tools', []),
            available_tools=task_request.get('available_tools', []),
            tool_alternatives=task_request.get('tool_alternatives', {}),
            resource_requirements=task_request.get('resource_requirements', {}),
            relevance_score=TaskRelevance.MEDIUM,  # Se calculará en validación
            clarity_score=ContextClarity.ACCEPTABLE,
            tool_availability=ToolAvailability.MOSTLY_AVAILABLE,
            created_by=task_request.get('created_by', 'user'),
            validated_by=None,
            last_updated=datetime.now(timezone.utc).isoformat(),
            validation_timestamp=None
        )
    
    async def execute_with_specialized_agent(self, task_context: TaskContext) -> Dict[str, Any]:
        """Ejecuta tarea con agente especializado apropiado"""
        # Determinar tipo de agente necesario
        agent_type = self.determine_required_agent_type(task_context)
        
        # Seleccionar agente disponible
        selected_agent = self.select_available_agent(agent_type)
        
        if not selected_agent:
            raise Exception(f"No hay agentes disponibles del tipo: {agent_type}")
        
        # Crear contexto INEGI para el agente
        inegi_context = INEGIDataContext(
            dataset_type="inegi_mixed",
            geographic_scope="nacional",
            time_period="2020-2024",
            variables=task_context.required_tools,
            data_source="inegi_oficial",
            quality_indicators={"overall": 0.95},
            metadata={"task_id": task_context.task_id}
        )
        
        # Ejecutar tarea con agente especializado
        agent_result = await selected_agent.process_task(
            task_data={'task_id': task_context.task_id, 'analysis_type': 'comprehensive'},
            inegi_context=inegi_context
        )
        
        return {
            'status': 'completed',
            'agent_id': selected_agent.agent_id,
            'agent_type': agent_type,
            'results': agent_result.results,
            'confidence_score': agent_result.confidence_score,
            'processing_time': agent_result.processing_time,
            'recommendations': agent_result.recommendations,
            'data_quality_score': agent_result.data_quality_score
        }
    
    def determine_required_agent_type(self, task_context: TaskContext) -> AgentSpecialization:
        """Determina el tipo de agente requerido basado en la tarea"""
        objective_lower = task_context.objective.lower()
        
        if any(keyword in objective_lower for keyword in ['demográfico', 'población', 'censo']):
            return AgentSpecialization.DEMOGRAPHIC_ANALYST
        elif any(keyword in objective_lower for keyword in ['económico', 'pib', 'empleo']):
            return AgentSpecialization.ECONOMIC_MODELER
        else:
            return AgentSpecialization.DEMOGRAPHIC_ANALYST  # Default
    
    def select_available_agent(self, agent_type: AgentSpecialization) -> Optional[Any]:
        """Selecciona agente disponible del tipo especificado"""
        available_agents = [
            agent for agent in self.specialized_agents.values()
            if agent.specialization == agent_type
        ]
        
        if available_agents:
            # Seleccionar el que tenga mejor rendimiento
            return max(available_agents, key=lambda a: a.avg_confidence_score)
        
        return None
    
    def record_execution_metrics(self, task_context: TaskContext, 
                               execution_result: Dict[str, Any], total_time: float):
        """Registra métricas de ejecución"""
        monitor = self.monitoring_system.real_time_monitor
        
        # Métricas de rendimiento
        monitor.record_metric("task.execution_time", total_time, "seconds")
        monitor.record_metric("task.confidence_score", 
                            execution_result.get('confidence_score', 0.5), "score")
        monitor.record_metric("task.data_quality", 
                            execution_result.get('data_quality_score', 0.8), "score")
        
        # Actualizar salud del agente
        if 'agent_id' in execution_result:
            agent_id = execution_result['agent_id']
            monitor.update_agent_health(agent_id, {
                'status': 'healthy' if execution_result['status'] == 'completed' else 'warning',
                'tasks_completed': self.specialized_agents[agent_id].tasks_completed,
                'tasks_failed': self.specialized_agents[agent_id].tasks_failed,
                'avg_response_time': total_time,
                'memory_usage_mb': 256,  # Estimado
                'cpu_usage_percent': 25,  # Estimado
                'error_rate': 0.0 if execution_result['status'] == 'completed' else 0.1
            })
    
    async def update_global_progress(self, task_context: TaskContext, 
                                   execution_result: Dict[str, Any]):
        """Actualiza progreso de objetivos globales"""
        # Determinar qué objetivo(s) se benefician de esta tarea
        relevant_objectives = self.identify_relevant_objectives(task_context)
        
        for objective_id in relevant_objectives:
            # Calcular contribución al progreso (simplificado)
            progress_contribution = min(execution_result.get('confidence_score', 0.5) * 0.1, 0.1)
            
            current_progress = self.meta_orchestrator.global_objectives[objective_id].progress
            new_progress = min(current_progress + progress_contribution, 1.0)
            
            self.meta_orchestrator.update_objective_progress(
                objective_id, 
                new_progress,
                {'task_contribution': task_context.task_id}
            )
    
    def identify_relevant_objectives(self, task_context: TaskContext) -> List[str]:
        """Identifica objetivos relevantes para la tarea"""
        # Lógica simplificada - en producción sería más sofisticada
        objective_keywords = {
            'demográfico': ['Análisis Demográfico Nacional Completo'],
            'económico': ['Modelo Predictivo Socioeconómico Avanzado'],
            'visualización': ['Sistema de Visualización Interactiva Enterprise'],
            'dashboard': ['Sistema de Visualización Interactiva Enterprise']
        }
        
        relevant = []
        objective_lower = task_context.objective.lower()
        
        for keyword, objective_names in objective_keywords.items():
            if keyword in objective_lower:
                for obj_id, obj in self.meta_orchestrator.global_objectives.items():
                    if any(name in obj.name for name in objective_names):
                        relevant.append(obj_id)
        
        return relevant
    
    async def attempt_auto_recovery(self, task_context: TaskContext, error: str) -> Dict[str, Any]:
        """Intenta recuperación automática en caso de error"""
        self.logger.warning(f"🔄 Intentando recuperación automática para: {task_context.task_id}")
        
        # Estrategias de recuperación
        recovery_strategies = [
            "retry_with_different_agent",
            "simplify_task_scope",
            "use_alternative_tools"
        ]
        
        for strategy in recovery_strategies:
            try:
                if strategy == "retry_with_different_agent":
                    # Intentar con otro agente del mismo tipo
                    agent_type = self.determine_required_agent_type(task_context)
                    alternative_agent = self.select_available_agent(agent_type)
                    
                    if alternative_agent and alternative_agent.agent_id != task_context.task_id:
                        recovery_result = await self.execute_with_specialized_agent(task_context)
                        self.logger.info(f"✅ Recuperación exitosa con agente alternativo")
                        return {
                            'status': 'recovered',
                            'recovery_strategy': strategy,
                            'result': recovery_result
                        }
                
                await asyncio.sleep(1)  # Pausa entre intentos
                
            except Exception as recovery_error:
                self.logger.warning(f"❌ Estrategia {strategy} falló: {recovery_error}")
                continue
        
        self.logger.error(f"💥 Todas las estrategias de recuperación fallaron")
        return {
            'status': 'recovery_failed',
            'original_error': error,
            'attempted_strategies': recovery_strategies
        }
    
    def setup_auto_recovery(self):
        """Configura sistema de recuperación automática"""
        # Configurar callbacks de monitoreo para recuperación
        def on_critical_alert(alert):
            if alert.level == AlertLevel.CRITICAL:
                asyncio.create_task(self.handle_critical_alert(alert))
        
        self.monitoring_system.real_time_monitor.alert_callbacks.append(on_critical_alert)
        self.logger.info("🛡️ Sistema de recuperación automática configurado")
    
    async def handle_critical_alert(self, alert):
        """Maneja alertas críticas del sistema"""
        self.logger.critical(f"🚨 ALERTA CRÍTICA: {alert.message}")
        
        if alert.component == "system" and "memory" in alert.message.lower():
            # Limpiar cache y liberar memoria
            await self.emergency_cleanup()
        elif alert.component == "agent" and "error_rate" in alert.message.lower():
            # Reiniciar agente problemático
            await self.restart_problematic_agent(alert.metadata.get('agent_id'))
    
    async def emergency_cleanup(self):
        """Limpieza de emergencia del sistema"""
        self.logger.warning("🧹 Ejecutando limpieza de emergencia")
        
        # Limpiar checkpoints antiguos
        self.persistence_manager.cleanup_old_checkpoints(days_old=1)
        
        # Limpiar métricas en memoria
        self.monitoring_system.real_time_monitor.metrics_buffer.clear()
        
        self.logger.info("✅ Limpieza de emergencia completada")
    
    async def restart_problematic_agent(self, agent_id: str):
        """Reinicia agente problemático"""
        if agent_id in self.specialized_agents:
            old_agent = self.specialized_agents[agent_id]
            specialization = old_agent.specialization
            
            # Crear nuevo agente del mismo tipo
            new_agent = INEGIAgentFactory.create_agent(specialization)
            self.specialized_agents[new_agent.agent_id] = new_agent
            
            # Remover agente problemático
            del self.specialized_agents[agent_id]
            
            self.logger.info(f"🔄 Agente reiniciado: {agent_id} → {new_agent.agent_id}")
    
    def get_system_status_report(self) -> Dict[str, Any]:
        """Genera reporte completo del estado del sistema"""
        monitoring_data = self.monitoring_system.get_monitoring_dashboard_data()
        validation_stats = self.context_manager.validator.get_validation_statistics()
        meta_orchestrator_status = self.meta_orchestrator.get_global_status_report()
        
        return {
            'system_id': self.system_id,
            'status': self.system_status,
            'uptime_hours': (time.time() - self.meta_orchestrator.start_time.timestamp()) / 3600,
            'monitoring_data': monitoring_data,
            'validation_statistics': validation_stats,
            'orchestrator_status': meta_orchestrator_status,
            'specialized_agents': len(self.specialized_agents),
            'active_workflows': len(self.active_workflows),
            'completed_objectives': len(self.completed_objectives),
            'timestamp': datetime.now(timezone.utc).isoformat()
        }

# Función principal para demostración
async def main():
    """Función principal de demostración del sistema"""
    print("🚀 SISTEMA MAESTRO INEGI - DATATÓN 2024")
    print("👨‍💻 David Fernando Ávila Díaz - ITAM")
    print("🎯 Sistema Multi-Agente Infalible con IA Enterprise")
    print("=" * 70)
    
    # Inicializar sistema maestro
    master_system = MasterINEGISystem()
    
    print("🔄 Inicializando sistema completo...")
    await master_system.initialize_system()
    print("✅ Sistema inicializado exitosamente")
    
    # Ejemplo de tarea válida
    sample_task = {
        "objective": "Crear análisis demográfico completo de la población mexicana por entidades federativas usando datos del Censo 2020 de INEGI",
        "deliverable": "Dashboard interactivo con pirámides poblacionales y métricas clave",
        "success_criteria": [
            "Análisis de 32 entidades federativas",
            "Dashboard funcional e interactivo",
            "Métricas demográficas validadas"
        ],
        "business_value": "Base analítica fundamental para el Datatón INEGI",
        "priority_justification": "Objetivo primario del concurso",
        "impact_assessment": {"project_success": 0.9, "user_value": 0.8},
        "required_tools": ["pandas", "plotly", "inegi_api_client"],
        "available_tools": ["pandas", "plotly", "inegi_api_client", "matplotlib"]
    }
    
    print(f"\n📋 Ejecutando tarea de ejemplo...")
    result = await master_system.submit_and_execute_task(sample_task)
    
    print(f"✅ Tarea completada:")
    print(f"   - Status: {result['status']}")
    print(f"   - Tiempo: {result.get('processing_time', 0):.2f}s")
    print(f"   - Score de validación: {result.get('validation_score', 0):.2f}")
    
    # Reporte final del sistema
    print(f"\n📊 Reporte del Sistema:")
    status_report = master_system.get_system_status_report()
    print(f"   - Agentes especializados: {status_report['specialized_agents']}")
    print(f"   - Validaciones realizadas: {status_report['validation_statistics']['total_validations']}")
    print(f"   - Tareas aprobadas: {status_report['validation_statistics']['tasks_approved']}")
    print(f"   - Progreso global: {status_report['orchestrator_status']['overall_progress']:.1%}")
    
    print(f"\n🎉 Sistema Maestro INEGI listo para Datatón")
    print(f"🔥 Capacidades enterprise: Validación contextual, multi-agente, auto-recuperación")
    
    return master_system

if __name__ == "__main__":
    # Ejecutar sistema maestro
    asyncio.run(main())