#!/usr/bin/env python3
"""
INEGI Datatón - Sistema de Validación Contextual y Optimización de Tareas
Garantiza que cada agente tenga contexto claro: QUÉ, POR QUÉ, CON QUÉ

David Fernando Ávila Díaz - ITAM
Sistema Anti-Trabajo Inútil con Validación de Propósito
"""

import json
import uuid
import time
from datetime import datetime, timezone
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, List, Optional, Any, Union, Callable
from abc import ABC, abstractmethod
import logging
from pathlib import Path

class TaskRelevance(Enum):
    CRITICAL = "critical"          # Esencial para el objetivo
    HIGH = "high"                 # Muy importante
    MEDIUM = "medium"             # Útil pero no esencial
    LOW = "low"                   # Marginal
    IRRELEVANT = "irrelevant"     # No contribuye al objetivo
    HARMFUL = "harmful"           # Contraproducente

class ContextClarity(Enum):
    CRYSTAL_CLEAR = "crystal_clear"    # 100% claro
    CLEAR = "clear"                    # Suficientemente claro
    ACCEPTABLE = "acceptable"          # Mínimo aceptable
    UNCLEAR = "unclear"                # Requiere clarificación
    CONFUSING = "confusing"            # Contradictorio o confuso

class ToolAvailability(Enum):
    FULLY_AVAILABLE = "fully_available"    # Todas las herramientas disponibles
    MOSTLY_AVAILABLE = "mostly_available"  # >80% disponible
    PARTIALLY_AVAILABLE = "partially_available"  # 50-80% disponible
    LIMITED = "limited"                    # <50% disponible
    NOT_AVAILABLE = "not_available"        # Herramientas no disponibles

@dataclass
class TaskContext:
    """Contexto completo y validado para una tarea"""
    task_id: str
    
    # QUÉ hacer (objetivo específico)
    objective: str
    deliverable: str
    success_criteria: List[str]
    scope_boundaries: Dict[str, Any]
    
    # POR QUÉ hacerlo (justificación y valor)
    business_value: str
    priority_justification: str
    impact_assessment: Dict[str, float]
    dependency_chain: List[str]
    
    # CON QUÉ hacerlo (herramientas y recursos)
    required_tools: List[str]
    available_tools: List[str]
    tool_alternatives: Dict[str, List[str]]
    resource_requirements: Dict[str, Any]
    
    # Validación de contexto
    relevance_score: TaskRelevance
    clarity_score: ContextClarity
    tool_availability: ToolAvailability
    
    # Metadatos
    created_by: str
    validated_by: Optional[str]
    last_updated: str
    validation_timestamp: Optional[str]

@dataclass
class ValidationResult:
    """Resultado de validación contextual"""
    is_valid: bool
    relevance_score: float
    clarity_score: float
    tool_readiness: float
    
    blocking_issues: List[str]
    warnings: List[str]
    recommendations: List[str]
    
    estimated_value: float
    estimated_effort: float
    value_effort_ratio: float
    
    validation_details: Dict[str, Any]
    timestamp: str

class ContextValidator:
    """Validador principal de contexto de tareas"""
    
    def __init__(self):
        self.validation_rules = self.load_validation_rules()
        self.tool_registry = self.load_tool_registry()
        self.objective_hierarchy = self.load_objective_hierarchy()
        
        self.logger = self.setup_logger()
        
        # Métricas de validación
        self.validations_performed = 0
        self.tasks_rejected = 0
        self.tasks_approved = 0
        self.avg_relevance_score = 0.0
        
        self.logger.info("🎯 Sistema de Validación Contextual inicializado")
    
    def setup_logger(self):
        log_dir = Path("logs/context_validation")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logger = logging.getLogger("ContextValidator")
        logger.setLevel(logging.INFO)
        
        handler = logging.FileHandler(log_dir / "context_validation.log")
        handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - [%(levelname)s] - %(funcName)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def load_validation_rules(self) -> Dict[str, Any]:
        """Carga reglas de validación contextual"""
        return {
            'objective_clarity': {
                'min_word_count': 10,
                'requires_specific_deliverable': True,
                'must_have_success_criteria': True,
                'forbidden_vague_terms': ['algo', 'cosa', 'mejorar', 'analizar genéricamente']
            },
            'business_value': {
                'min_impact_score': 0.3,
                'requires_quantifiable_benefit': True,
                'must_align_with_project_goals': True
            },
            'tool_requirements': {
                'min_tool_availability': 0.7,
                'requires_fallback_options': True,
                'validates_tool_compatibility': True
            },
            'effort_justification': {
                'max_effort_for_low_value': 2.0,  # horas
                'min_value_effort_ratio': 0.5,
                'requires_cost_benefit_analysis': True
            }
        }
    
    def load_tool_registry(self) -> Dict[str, Any]:
        """Registro de herramientas disponibles y sus capacidades"""
        return {
            'data_analysis': {
                'pandas': {'available': True, 'capability_score': 0.9},
                'numpy': {'available': True, 'capability_score': 0.9},
                'scipy': {'available': True, 'capability_score': 0.8},
                'sklearn': {'available': True, 'capability_score': 0.8},
                'statsmodels': {'available': True, 'capability_score': 0.7}
            },
            'visualization': {
                'matplotlib': {'available': True, 'capability_score': 0.8},
                'plotly': {'available': True, 'capability_score': 0.9},
                'seaborn': {'available': True, 'capability_score': 0.7},
                'altair': {'available': False, 'capability_score': 0.6}
            },
            'machine_learning': {
                'xgboost': {'available': True, 'capability_score': 0.9},
                'lightgbm': {'available': True, 'capability_score': 0.8},
                'tensorflow': {'available': False, 'capability_score': 0.9},
                'pytorch': {'available': False, 'capability_score': 0.9}
            },
            'inegi_specific': {
                'inegi_api_client': {'available': True, 'capability_score': 0.8},
                'geographic_processing': {'available': True, 'capability_score': 0.7},
                'demographic_analysis': {'available': True, 'capability_score': 0.8}
            }
        }
    
    def load_objective_hierarchy(self) -> Dict[str, Any]:
        """Jerarquía de objetivos del proyecto (se actualizará con info real)"""
        return {
            'primary_objectives': [
                'Análisis demográfico nacional comprensivo',
                'Modelo predictivo socioeconómico',
                'Dashboard interactivo INEGI'
            ],
            'secondary_objectives': [
                'Visualizaciones avanzadas',
                'Reportes automatizados',
                'Sistema de alertas de datos'
            ],
            'support_objectives': [
                'Documentación técnica',
                'Validación de calidad de datos',
                'Optimización de rendimiento'
            ],
            'excluded_objectives': [
                'Análisis no relacionados con INEGI',
                'Desarrollos sin valor agregado',
                'Tareas duplicadas o redundantes'
            ]
        }
    
    def validate_task_context(self, task_context: TaskContext) -> ValidationResult:
        """Validación completa del contexto de tarea"""
        start_time = time.time()
        
        # Validaciones individuales
        objective_validation = self._validate_objective_clarity(task_context)
        value_validation = self._validate_business_value(task_context)
        tool_validation = self._validate_tool_availability(task_context)
        relevance_validation = self._validate_task_relevance(task_context)
        
        # Calcular scores agregados
        relevance_score = relevance_validation['score']
        clarity_score = objective_validation['score']
        tool_readiness = tool_validation['score']
        
        # Determinar si la tarea es válida
        is_valid = (
            relevance_score >= 0.6 and
            clarity_score >= 0.7 and
            tool_readiness >= 0.7 and
            len(self._get_blocking_issues(
                objective_validation, value_validation, 
                tool_validation, relevance_validation
            )) == 0
        )
        
        # Recopilar issues y recomendaciones
        blocking_issues = self._get_blocking_issues(
            objective_validation, value_validation, tool_validation, relevance_validation
        )
        warnings = self._get_warnings(
            objective_validation, value_validation, tool_validation, relevance_validation
        )
        recommendations = self._generate_recommendations(task_context, 
            objective_validation, value_validation, tool_validation, relevance_validation
        )
        
        # Calcular valor vs esfuerzo
        estimated_value = value_validation.get('estimated_value', 0.5)
        estimated_effort = self._estimate_effort(task_context)
        value_effort_ratio = estimated_value / max(estimated_effort, 0.1)
        
        validation_result = ValidationResult(
            is_valid=is_valid,
            relevance_score=relevance_score,
            clarity_score=clarity_score,
            tool_readiness=tool_readiness,
            blocking_issues=blocking_issues,
            warnings=warnings,
            recommendations=recommendations,
            estimated_value=estimated_value,
            estimated_effort=estimated_effort,
            value_effort_ratio=value_effort_ratio,
            validation_details={
                'objective_validation': objective_validation,
                'value_validation': value_validation,
                'tool_validation': tool_validation,
                'relevance_validation': relevance_validation
            },
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        
        # Logging y métricas
        self.validations_performed += 1
        if is_valid:
            self.tasks_approved += 1
            self.logger.info(f"✅ Tarea validada: {task_context.task_id} - "
                           f"Relevancia: {relevance_score:.2f}, "
                           f"Claridad: {clarity_score:.2f}, "
                           f"Herramientas: {tool_readiness:.2f}")
        else:
            self.tasks_rejected += 1
            self.logger.warning(f"❌ Tarea rechazada: {task_context.task_id} - "
                              f"Issues: {len(blocking_issues)}")
            self.logger.warning(f"   Blocking issues: {blocking_issues}")
        
        return validation_result
    
    def _validate_objective_clarity(self, context: TaskContext) -> Dict[str, Any]:
        """Valida claridad del objetivo"""
        score = 1.0
        issues = []
        
        # Verificar longitud y especificidad del objetivo
        if len(context.objective.split()) < self.validation_rules['objective_clarity']['min_word_count']:
            score -= 0.3
            issues.append("Objetivo demasiado vago o corto")
        
        # Verificar términos prohibidos
        forbidden_terms = self.validation_rules['objective_clarity']['forbidden_vague_terms']
        for term in forbidden_terms:
            if term.lower() in context.objective.lower():
                score -= 0.2
                issues.append(f"Término vago detectado: '{term}'")
        
        # Verificar deliverable específico
        if not context.deliverable or len(context.deliverable.strip()) < 10:
            score -= 0.4
            issues.append("Deliverable no específico o ausente")
        
        # Verificar criterios de éxito
        if not context.success_criteria or len(context.success_criteria) == 0:
            score -= 0.3
            issues.append("Criterios de éxito no definidos")
        
        return {
            'score': max(score, 0.0),
            'issues': issues,
            'details': {
                'objective_word_count': len(context.objective.split()),
                'has_specific_deliverable': bool(context.deliverable),
                'success_criteria_count': len(context.success_criteria)
            }
        }
    
    def _validate_business_value(self, context: TaskContext) -> Dict[str, Any]:
        """Valida valor de negocio y justificación"""
        score = 1.0
        issues = []
        
        # Verificar justificación de valor
        if not context.business_value or len(context.business_value.strip()) < 20:
            score -= 0.4
            issues.append("Valor de negocio no justificado adecuadamente")
        
        # Verificar alineación con objetivos del proyecto
        is_aligned = self._check_alignment_with_project_goals(context.objective)
        if not is_aligned:
            score -= 0.5
            issues.append("Objetivo no alineado con metas del proyecto")
        
        # Calcular impacto estimado
        avg_impact = sum(context.impact_assessment.values()) / len(context.impact_assessment) if context.impact_assessment else 0.3
        estimated_value = min(avg_impact * score, 1.0)
        
        return {
            'score': max(score, 0.0),
            'estimated_value': estimated_value,
            'issues': issues,
            'details': {
                'business_value_length': len(context.business_value),
                'is_aligned_with_project': is_aligned,
                'impact_score': avg_impact
            }
        }
    
    def _validate_tool_availability(self, context: TaskContext) -> Dict[str, Any]:
        """Valida disponibilidad de herramientas requeridas"""
        score = 1.0
        issues = []
        available_count = 0
        total_required = len(context.required_tools)
        
        if total_required == 0:
            return {'score': 0.5, 'issues': ["No se especificaron herramientas requeridas"], 'details': {}}
        
        for tool in context.required_tools:
            is_available = self._check_tool_availability(tool)
            if is_available:
                available_count += 1
            else:
                issues.append(f"Herramienta no disponible: {tool}")
        
        availability_ratio = available_count / total_required
        
        if availability_ratio < 0.5:
            score = 0.2
            issues.append("Menos del 50% de herramientas disponibles")
        elif availability_ratio < 0.7:
            score = 0.6
            issues.append("Disponibilidad de herramientas limitada")
        elif availability_ratio < 0.9:
            score = 0.8
        
        # Verificar alternativas para herramientas faltantes
        missing_tools = [t for t in context.required_tools if not self._check_tool_availability(t)]
        has_alternatives = all(
            tool in context.tool_alternatives and len(context.tool_alternatives[tool]) > 0
            for tool in missing_tools
        )
        
        if missing_tools and not has_alternatives:
            score -= 0.2
            issues.append("Faltan alternativas para herramientas no disponibles")
        
        return {
            'score': max(score, 0.0),
            'issues': issues,
            'details': {
                'total_required_tools': total_required,
                'available_tools': available_count,
                'availability_ratio': availability_ratio,
                'missing_tools': missing_tools,
                'has_alternatives': has_alternatives
            }
        }
    
    def _validate_task_relevance(self, context: TaskContext) -> Dict[str, Any]:
        """Valida relevancia de la tarea para los objetivos del proyecto"""
        score = 0.5  # Score base
        issues = []
        
        # Verificar alineación con objetivos primarios
        primary_alignment = self._calculate_alignment_score(
            context.objective, self.objective_hierarchy['primary_objectives']
        )
        
        # Verificar alineación con objetivos secundarios
        secondary_alignment = self._calculate_alignment_score(
            context.objective, self.objective_hierarchy['secondary_objectives']
        )
        
        # Verificar si está en objetivos excluidos
        excluded_alignment = self._calculate_alignment_score(
            context.objective, self.objective_hierarchy['excluded_objectives']
        )
        
        if excluded_alignment > 0.3:
            score = 0.1
            issues.append("Tarea alineada con objetivos excluidos")
        elif primary_alignment > 0.6:
            score = 0.9
        elif primary_alignment > 0.3 or secondary_alignment > 0.5:
            score = 0.7
        elif secondary_alignment > 0.3:
            score = 0.5
        else:
            score = 0.2
            issues.append("Baja relevancia para objetivos del proyecto")
        
        return {
            'score': score,
            'issues': issues,
            'details': {
                'primary_alignment': primary_alignment,
                'secondary_alignment': secondary_alignment,
                'excluded_alignment': excluded_alignment
            }
        }
    
    def _check_alignment_with_project_goals(self, objective: str) -> bool:
        """Verifica alineación con metas del proyecto"""
        # Palabras clave que indican alineación con INEGI/Datatón
        inegi_keywords = [
            'inegi', 'demográfico', 'económico', 'censo', 'poblacional',
            'estadística', 'socioeconómico', 'territorial', 'nacional'
        ]
        
        objective_lower = objective.lower()
        return any(keyword in objective_lower for keyword in inegi_keywords)
    
    def _check_tool_availability(self, tool_name: str) -> bool:
        """Verifica si una herramienta está disponible"""
        for category, tools in self.tool_registry.items():
            if tool_name in tools:
                return tools[tool_name]['available']
        return False
    
    def _calculate_alignment_score(self, objective: str, target_objectives: List[str]) -> float:
        """Calcula score de alineación usando palabras clave"""
        objective_words = set(objective.lower().split())
        max_score = 0.0
        
        for target in target_objectives:
            target_words = set(target.lower().split())
            intersection = objective_words.intersection(target_words)
            score = len(intersection) / len(target_words.union(objective_words))
            max_score = max(max_score, score)
        
        return max_score
    
    def _estimate_effort(self, context: TaskContext) -> float:
        """Estima esfuerzo requerido en horas"""
        base_effort = 2.0  # horas base
        
        # Ajustar por complejidad del objetivo
        complexity_indicators = ['modelo', 'predicción', 'dashboard', 'análisis completo']
        complexity_factor = 1.0
        
        for indicator in complexity_indicators:
            if indicator in context.objective.lower():
                complexity_factor += 0.5
        
        # Ajustar por disponibilidad de herramientas
        tool_factor = 1.0
        if context.tool_availability == ToolAvailability.LIMITED:
            tool_factor = 1.5
        elif context.tool_availability == ToolAvailability.NOT_AVAILABLE:
            tool_factor = 2.0
        
        return base_effort * complexity_factor * tool_factor
    
    def _get_blocking_issues(self, *validations) -> List[str]:
        """Obtiene issues que bloquean la tarea"""
        blocking_issues = []
        for validation in validations:
            if validation['score'] < 0.5:  # Threshold crítico
                blocking_issues.extend(validation['issues'])
        return blocking_issues
    
    def _get_warnings(self, *validations) -> List[str]:
        """Obtiene warnings no bloqueantes"""
        warnings = []
        for validation in validations:
            if 0.5 <= validation['score'] < 0.7:
                warnings.extend([f"⚠️ {issue}" for issue in validation['issues']])
        return warnings
    
    def _generate_recommendations(self, context: TaskContext, *validations) -> List[str]:
        """Genera recomendaciones para mejorar la tarea"""
        recommendations = []
        
        # Recomendaciones basadas en validaciones específicas
        obj_val, val_val, tool_val, rel_val = validations
        
        if obj_val['score'] < 0.7:
            recommendations.append("Especificar más claramente el objetivo y deliverable")
        
        if val_val['score'] < 0.7:
            recommendations.append("Justificar mejor el valor de negocio y alineación")
        
        if tool_val['score'] < 0.8:
            recommendations.append("Verificar disponibilidad de herramientas o definir alternativas")
        
        if rel_val['score'] < 0.6:
            recommendations.append("Revisar relevancia para objetivos del Datatón INEGI")
        
        # Recomendaciones de optimización
        if context.estimated_effort and context.estimated_effort > 8:
            recommendations.append("Considerar dividir en subtareas más pequeñas")
        
        return recommendations
    
    def get_validation_statistics(self) -> Dict[str, Any]:
        """Obtiene estadísticas del sistema de validación"""
        approval_rate = self.tasks_approved / max(self.validations_performed, 1)
        
        return {
            'total_validations': self.validations_performed,
            'tasks_approved': self.tasks_approved,
            'tasks_rejected': self.tasks_rejected,
            'approval_rate': approval_rate,
            'avg_relevance_score': self.avg_relevance_score,
            'validation_efficiency': approval_rate,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }

class ContextAwareTaskManager:
    """Gestor de tareas con validación contextual integrada"""
    
    def __init__(self):
        self.validator = ContextValidator()
        self.pending_tasks: Dict[str, TaskContext] = {}
        self.validated_tasks: Dict[str, TaskContext] = {}
        self.rejected_tasks: Dict[str, TaskContext] = {}
        
        self.logger = logging.getLogger("ContextAwareTaskManager")
    
    def submit_task(self, task_context: TaskContext) -> ValidationResult:
        """Somete tarea para validación contextual"""
        validation_result = self.validator.validate_task_context(task_context)
        
        if validation_result.is_valid:
            self.validated_tasks[task_context.task_id] = task_context
            task_context.validated_by = "context_validator"
            task_context.validation_timestamp = validation_result.timestamp
        else:
            self.rejected_tasks[task_context.task_id] = task_context
        
        return validation_result
    
    def get_validated_tasks(self) -> List[TaskContext]:
        """Obtiene tareas validadas listas para ejecución"""
        return list(self.validated_tasks.values())
    
    def get_rejection_report(self) -> Dict[str, Any]:
        """Obtiene reporte de tareas rechazadas"""
        return {
            'total_rejected': len(self.rejected_tasks),
            'rejected_tasks': {
                task_id: {
                    'objective': task.objective,
                    'business_value': task.business_value
                }
                for task_id, task in self.rejected_tasks.items()
            }
        }

if __name__ == "__main__":
    print("🎯 Sistema de Validación Contextual - INEGI Datatón")
    print("👨‍💻 David Fernando Ávila Díaz - ITAM")
    print("🚫 Anti-Trabajo Inútil - Pro-Eficiencia Total")
    print("=" * 60)
    
    # Inicializar sistema
    task_manager = ContextAwareTaskManager()
    
    # Ejemplo de tarea BUENA
    good_task = TaskContext(
        task_id="task_good_001",
        objective="Crear análisis demográfico completo de la población mexicana por entidades federativas usando datos del Censo 2020 de INEGI",
        deliverable="Dashboard interactivo con pirámides poblacionales, mapas de densidad y métricas demográficas clave",
        success_criteria=[
            "Dashboard funcional con datos de 32 entidades",
            "Visualizaciones responsivas e interactivas",
            "Métricas validadas contra fuente oficial INEGI"
        ],
        scope_boundaries={"geographic": "nacional", "temporal": "2020", "demographic_indicators": 15},
        business_value="Proporciona base analítica fundamental para decisiones de política pública demográfica",
        priority_justification="Objetivo primario del Datatón INEGI - análisis demográfico nacional",
        impact_assessment={"project_success": 0.9, "user_value": 0.8, "technical_learning": 0.7},
        dependency_chain=["data_extraction", "data_cleaning", "visualization_framework"],
        required_tools=["pandas", "plotly", "inegi_api_client"],
        available_tools=["pandas", "plotly", "inegi_api_client", "matplotlib"],
        tool_alternatives={"plotly": ["matplotlib", "seaborn"]},
        resource_requirements={"data_storage": "2GB", "processing_power": "medium"},
        relevance_score=TaskRelevance.CRITICAL,
        clarity_score=ContextClarity.CRYSTAL_CLEAR,
        tool_availability=ToolAvailability.FULLY_AVAILABLE,
        created_by="project_manager",
        validated_by=None,
        last_updated=datetime.now(timezone.utc).isoformat(),
        validation_timestamp=None
    )
    
    # Ejemplo de tarea MALA
    bad_task = TaskContext(
        task_id="task_bad_001",
        objective="Hacer algo con datos",
        deliverable="Análisis",
        success_criteria=[],
        scope_boundaries={},
        business_value="Podría ser útil",
        priority_justification="No sé, tal vez sirva",
        impact_assessment={},
        dependency_chain=[],
        required_tools=["tensorflow", "pytorch"],  # No disponibles
        available_tools=[],
        tool_alternatives={},
        resource_requirements={},
        relevance_score=TaskRelevance.LOW,
        clarity_score=ContextClarity.CONFUSING,
        tool_availability=ToolAvailability.NOT_AVAILABLE,
        created_by="unknown",
        validated_by=None,
        last_updated=datetime.now(timezone.utc).isoformat(),
        validation_timestamp=None
    )
    
    # Validar tareas
    print("\n🔍 Validando tarea BUENA...")
    good_result = task_manager.submit_task(good_task)
    print(f"   ✅ Válida: {good_result.is_valid}")
    print(f"   📊 Relevancia: {good_result.relevance_score:.2f}")
    print(f"   💎 Claridad: {good_result.clarity_score:.2f}")
    print(f"   🛠️ Herramientas: {good_result.tool_readiness:.2f}")
    
    print(f"\n🔍 Validando tarea MALA...")
    bad_result = task_manager.submit_task(bad_task)
    print(f"   ❌ Válida: {bad_result.is_valid}")
    print(f"   📊 Relevancia: {bad_result.relevance_score:.2f}")
    print(f"   💎 Claridad: {bad_result.clarity_score:.2f}")
    print(f"   🛠️ Herramientas: {bad_result.tool_readiness:.2f}")
    print(f"   🚫 Issues: {bad_result.blocking_issues}")
    
    # Estadísticas
    stats = task_manager.validator.get_validation_statistics()
    print(f"\n📈 Estadísticas del Sistema:")
    print(f"   - Validaciones realizadas: {stats['total_validations']}")
    print(f"   - Tareas aprobadas: {stats['tasks_approved']}")
    print(f"   - Tareas rechazadas: {stats['tasks_rejected']}")
    print(f"   - Tasa de aprobación: {stats['approval_rate']:.1%}")
    
    print(f"\n✅ Sistema Anti-Trabajo Inútil funcionando")
    print(f"🎯 Garantiza contexto claro: QUÉ, POR QUÉ, CON QUÉ")