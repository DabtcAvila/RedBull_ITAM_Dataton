#!/usr/bin/env python3
"""
MOTOR DE RECOMENDACIONES INTELIGENTE - DATATÓN ITAM 2025
Algoritmo avanzado de scoring personalizado para zonas CDMX

David Fernando Ávila Díaz - ITAM
"""

import json
import math
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

@dataclass
class UserProfile:
    """Perfil de usuario para personalización"""
    presupuesto_max_renta: int = 25000  # Pesos mexicanos
    presupuesto_max_compra: int = 3000000
    tamano_familia: int = 2  # Número de personas
    tiene_hijos: bool = False
    edades_hijos: List[int] = None
    
    # Prioridades (0-10, 10=máxima prioridad)
    prioridad_seguridad: int = 8
    prioridad_transporte: int = 7
    prioridad_precio: int = 6
    prioridad_escuelas: int = 3
    prioridad_hospitales: int = 5
    prioridad_vida_nocturna: int = 4
    prioridad_areas_verdes: int = 6
    prioridad_centros_comerciales: int = 5
    
    # Preferencias específicas
    prefiere_zonas_tranquilas: bool = True
    requiere_estacionamiento: bool = True
    acepta_ruido_trafico: bool = False
    tiempo_max_trabajo_min: int = 45
    ubicacion_trabajo: str = "Centro"  # Centro, Polanco, Santa Fe, etc.
    
    # Estilo de vida
    estilo_vida: str = "familiar"  # familiar, joven_profesional, retirado, estudiante
    
    def __post_init__(self):
        if self.edades_hijos is None:
            self.edades_hijos = []

@dataclass
class ZoneRecommendation:
    """Recomendación de zona con explicación"""
    colonia: str
    alcaldia: str
    score_total: float
    score_personalizado: float
    ranking: int
    
    # Scores por categoría
    score_seguridad: float
    score_transporte: float
    score_precio: float
    score_amenidades: float
    score_calidad_vida: float
    
    # Información clave
    precio_renta_estimado: int
    precio_compra_m2: int
    tiempo_trabajo_min: int
    
    # Explicación de la recomendación
    razones_principales: List[str]
    pros: List[str]
    contras: List[str]
    
    # Datos adicionales para mostrar
    datos_destacados: Dict[str, Any]

class IntelligentRecommendationEngine:
    """Motor de recomendaciones inteligente con algoritmo personalizado"""
    
    def __init__(self):
        # Pesos base del algoritmo (pueden ser ajustados por usuario)
        self.default_weights = {
            'seguridad': 0.25,
            'transporte': 0.20, 
            'precio': 0.20,
            'amenidades': 0.15,
            'calidad_vida': 0.10,
            'compatibilidad_estilo': 0.10
        }
        
        # Perfiles de estilo de vida
        self.lifestyle_profiles = self.define_lifestyle_profiles()
        
        # Mapeo de ubicaciones de trabajo a coordenadas aproximadas
        self.work_locations = {
            'Centro': {'lat': 19.4326, 'lon': -99.1332, 'zonas_cercanas': ['Centro Histórico', 'Doctores']},
            'Polanco': {'lat': 19.4338, 'lon': -99.1929, 'zonas_cercanas': ['Polanco', 'Anzures']},
            'Santa Fe': {'lat': 19.3583, 'lon': -99.2714, 'zonas_cercanas': ['Santa Fe', 'Cuajimalpa']},
            'Roma Norte': {'lat': 19.4149, 'lon': -99.1625, 'zonas_cercanas': ['Roma Norte', 'Condesa']},
            'Insurgentes Sur': {'lat': 19.3729, 'lon': -99.1619, 'zonas_cercanas': ['Del Valle', 'Narvarte']}
        }
    
    def define_lifestyle_profiles(self) -> Dict[str, Dict[str, Any]]:
        """Define perfiles de estilo de vida con preferencias específicas"""
        return {
            'familiar': {
                'weight_adjustments': {
                    'seguridad': 1.3,  # Mayor importancia a seguridad
                    'amenidades': 1.2,  # Escuelas, hospitales importantes
                    'transporte': 1.0,
                    'precio': 1.1,
                    'calidad_vida': 1.2
                },
                'preferred_zones': ['Del Valle', 'San Ángel', 'Coyoacán Centro'],
                'avoided_zones': ['Centro Histórico', 'Doctores'],
                'key_amenities': ['escuelas', 'hospitales', 'parques', 'supermercados']
            },
            'joven_profesional': {
                'weight_adjustments': {
                    'transporte': 1.4,  # Conectividad muy importante
                    'vida_nocturna': 1.3,
                    'seguridad': 1.1,
                    'precio': 1.2,  # Sensible al precio
                    'amenidades': 0.9
                },
                'preferred_zones': ['Roma Norte', 'Condesa', 'Polanco', 'Zona Rosa'],
                'avoided_zones': [],
                'key_amenities': ['restaurantes', 'bares', 'centros_comerciales', 'transporte']
            },
            'retirado': {
                'weight_adjustments': {
                    'seguridad': 1.4,  # Muy importante
                    'amenidades': 1.3,  # Hospitales críticos
                    'calidad_vida': 1.3,  # Tranquilidad
                    'transporte': 0.8,
                    'vida_nocturna': 0.3
                },
                'preferred_zones': ['San Ángel', 'Coyoacán Centro', 'Del Valle'],
                'avoided_zones': ['Centro Histórico', 'Roma Norte'],
                'key_amenities': ['hospitales', 'parques', 'bancos', 'supermercados']
            },
            'estudiante': {
                'weight_adjustments': {
                    'precio': 1.5,  # Muy sensible al precio
                    'transporte': 1.3,  # Necesita moverse mucho
                    'vida_nocturna': 1.2,
                    'seguridad': 1.0,
                    'amenidades': 0.9
                },
                'preferred_zones': ['Narvarte', 'Doctores', 'Escandón'],
                'avoided_zones': ['Polanco', 'Santa Fe'],
                'key_amenities': ['transporte', 'restaurantes_economicos', 'universidades']
            }
        }
    
    def calculate_personalized_weights(self, user_profile: UserProfile) -> Dict[str, float]:
        """Calcula pesos personalizados basados en perfil de usuario"""
        weights = self.default_weights.copy()
        
        # Aplicar ajustes de estilo de vida
        lifestyle = self.lifestyle_profiles.get(user_profile.estilo_vida, {})
        adjustments = lifestyle.get('weight_adjustments', {})
        
        for category, adjustment in adjustments.items():
            if category in weights:
                weights[category] *= adjustment
        
        # Aplicar prioridades específicas del usuario
        priority_mapping = {
            'seguridad': user_profile.prioridad_seguridad,
            'transporte': user_profile.prioridad_transporte,
            'precio': user_profile.prioridad_precio,
            'amenidades': (user_profile.prioridad_escuelas + user_profile.prioridad_hospitales + 
                          user_profile.prioridad_centros_comerciales) / 3
        }
        
        # Normalizar prioridades (0-10 → 0.5-1.5 factor)
        for category, priority in priority_mapping.items():
            if category in weights:
                priority_factor = 0.5 + (priority / 10.0)  # 0.5 a 1.5
                weights[category] *= priority_factor
        
        # Ajustes específicos para familias con hijos
        if user_profile.tiene_hijos:
            weights['seguridad'] *= 1.3
            weights['amenidades'] *= 1.2
            
            # Si tiene hijos pequeños, priorizar escuelas
            if any(edad < 12 for edad in user_profile.edades_hijos):
                weights['amenidades'] *= 1.1
        
        # Renormalizar pesos para que sumen 1.0
        total_weight = sum(weights.values())
        weights = {k: v/total_weight for k, v in weights.items()}
        
        return weights
    
    def calculate_zone_scores(self, zone_data: Dict[str, Any], user_profile: UserProfile) -> Dict[str, float]:
        """Calcula scores detallados para una zona"""
        scores = {}
        
        # 1. SCORE DE SEGURIDAD (0-100)
        scores['seguridad'] = zone_data.get('indice_seguridad', 50)
        
        # 2. SCORE DE TRANSPORTE (0-100) 
        scores['transporte'] = self.calculate_transport_score(zone_data, user_profile)
        
        # 3. SCORE DE PRECIO (0-100, mayor score = mejor precio/valor)
        scores['precio'] = self.calculate_price_score(zone_data, user_profile)
        
        # 4. SCORE DE AMENIDADES (0-100)
        scores['amenidades'] = zone_data.get('score_amenidades', 50)
        
        # 5. SCORE DE CALIDAD DE VIDA (0-100)
        scores['calidad_vida'] = self.calculate_quality_of_life_score(zone_data, user_profile)
        
        # 6. SCORE DE COMPATIBILIDAD DE ESTILO (0-100)
        scores['compatibilidad_estilo'] = self.calculate_lifestyle_compatibility(zone_data, user_profile)
        
        return scores
    
    def calculate_transport_score(self, zone_data: Dict[str, Any], user_profile: UserProfile) -> float:
        """Calcula score de transporte personalizado"""
        base_score = zone_data.get('score_conectividad', 50)
        
        # Ajustar por tiempo al trabajo
        work_location = user_profile.ubicacion_trabajo
        if work_location in self.work_locations:
            work_zones = self.work_locations[work_location]['zonas_cercanas']
            
            # Bonus si está cerca del trabajo
            if zone_data.get('colonia') in work_zones:
                base_score *= 1.2
            
            # Penalizar si el tiempo estimado supera el máximo aceptable
            time_to_work_field = f'tiempo_{work_location.lower().replace(" ", "_")}_min'
            estimated_time = zone_data.get(time_to_work_field, user_profile.tiempo_max_trabajo_min)
            
            if estimated_time > user_profile.tiempo_max_trabajo_min:
                penalty = min(0.5, (estimated_time - user_profile.tiempo_max_trabajo_min) / user_profile.tiempo_max_trabajo_min)
                base_score *= (1 - penalty)
        
        return min(base_score, 100)
    
    def calculate_price_score(self, zone_data: Dict[str, Any], user_profile: UserProfile) -> float:
        """Calcula score de precio (mayor score = mejor valor)"""
        price_rent = zone_data.get('precio_m2_renta_pesos', 400)  # Default 400 pesos/m²
        
        # Estimar costo mensual para el tamaño requerido
        family_size = user_profile.tamano_familia
        estimated_size_needed = 30 + (family_size * 15)  # m² básicos + 15m² por persona
        estimated_monthly_rent = price_rent * estimated_size_needed
        
        # Score basado en presupuesto (100 = perfecto para presupuesto, 0 = muy caro)
        budget = user_profile.presupuesto_max_renta
        
        if estimated_monthly_rent <= budget * 0.7:  # Muy económico
            price_score = 100
        elif estimated_monthly_rent <= budget:  # Dentro del presupuesto
            price_score = 80 + (budget - estimated_monthly_rent) / (budget * 0.3) * 20
        elif estimated_monthly_rent <= budget * 1.2:  # Ligeramente sobre presupuesto
            price_score = 40 + (budget * 1.2 - estimated_monthly_rent) / (budget * 0.2) * 40
        else:  # Muy caro
            price_score = max(10, 40 - min(60, (estimated_monthly_rent - budget * 1.2) / budget * 100))
        
        return price_score
    
    def calculate_quality_of_life_score(self, zone_data: Dict[str, Any], user_profile: UserProfile) -> float:
        """Calcula score de calidad de vida"""
        base_score = 50
        
        # Factores positivos
        parks_nearby = zone_data.get('parques_1km', 0)
        base_score += min(20, parks_nearby * 3)  # Hasta 20 puntos por parques
        
        noise_level = zone_data.get('nivel_ruido', 5)  # 1-10, 10=muy ruidoso
        if user_profile.prefiere_zonas_tranquilas:
            base_score += (10 - noise_level) * 2  # Hasta 18 puntos por tranquilidad
        
        # Densidad poblacional (preferencia por zonas menos densas para familias)
        density = zone_data.get('densidad_poblacional', 5000)
        if user_profile.tiene_hijos and density < 3000:
            base_score += 15  # Bonus por baja densidad con hijos
        
        # Calidad del aire (factor importante)
        air_quality = zone_data.get('calidad_aire_promedio', 50)  # 0-100, 100=excelente
        base_score += air_quality * 0.3  # Hasta 30 puntos
        
        return min(base_score, 100)
    
    def calculate_lifestyle_compatibility(self, zone_data: Dict[str, Any], user_profile: UserProfile) -> float:
        """Calcula compatibilidad con estilo de vida"""
        lifestyle = user_profile.estilo_vida
        lifestyle_config = self.lifestyle_profiles.get(lifestyle, {})
        
        base_score = 50
        
        # Bonus/penalty por zonas preferidas/evitadas
        colonia = zone_data.get('colonia', '')
        preferred_zones = lifestyle_config.get('preferred_zones', [])
        avoided_zones = lifestyle_config.get('avoided_zones', [])
        
        if colonia in preferred_zones:
            base_score += 30
        elif colonia in avoided_zones:
            base_score -= 20
        
        # Amenidades clave para el estilo de vida
        key_amenities = lifestyle_config.get('key_amenities', [])
        for amenity in key_amenities:
            amenity_count = zone_data.get(f'{amenity}_1km', 0)
            if amenity_count > 0:
                base_score += min(15, amenity_count * 2)
        
        # Ajustes específicos por estilo
        if lifestyle == 'joven_profesional':
            nightlife_score = zone_data.get('vida_nocturna_score', 0)
            base_score += nightlife_score * 0.3
            
        elif lifestyle == 'familiar':
            school_score = zone_data.get('escuelas_primarias_1km', 0)
            base_score += min(20, school_score * 4)
            
        elif lifestyle == 'retirado':
            medical_score = zone_data.get('hospitales_1km', 0)
            base_score += min(25, medical_score * 5)
        
        return min(base_score, 100)
    
    def generate_recommendations(self, zones_data: List[Dict[str, Any]], 
                                user_profile: UserProfile, 
                                num_recommendations: int = 5) -> List[ZoneRecommendation]:
        """Genera recomendaciones personalizadas de zonas"""
        
        # Calcular pesos personalizados
        weights = self.calculate_personalized_weights(user_profile)
        
        zone_recommendations = []
        
        for zone in zones_data:
            # Calcular scores por categoría
            category_scores = self.calculate_zone_scores(zone, user_profile)
            
            # Calcular score total ponderado
            total_score = sum(
                category_scores.get(category, 50) * weight 
                for category, weight in weights.items()
                if category in category_scores
            )
            
            # Crear recomendación
            recommendation = self.create_zone_recommendation(
                zone, category_scores, total_score, user_profile, weights
            )
            
            zone_recommendations.append(recommendation)
        
        # Ordenar por score y asignar ranking
        zone_recommendations.sort(key=lambda x: x.score_personalizado, reverse=True)
        for i, rec in enumerate(zone_recommendations):
            rec.ranking = i + 1
        
        # Aplicar diversificación (evitar recomendar zonas muy similares)
        diversified_recommendations = self.diversify_recommendations(
            zone_recommendations, num_recommendations
        )
        
        return diversified_recommendations[:num_recommendations]
    
    def create_zone_recommendation(self, zone_data: Dict[str, Any], 
                                 category_scores: Dict[str, float],
                                 total_score: float,
                                 user_profile: UserProfile,
                                 weights: Dict[str, float]) -> ZoneRecommendation:
        """Crea recomendación detallada para una zona"""
        
        colonia = zone_data.get('colonia', 'Desconocida')
        
        # Generar explicaciones automáticas
        razones_principales = self.generate_main_reasons(category_scores, weights, user_profile)
        pros = self.generate_pros(zone_data, category_scores)
        contras = self.generate_contras(zone_data, category_scores)
        
        # Estimar precios específicos
        price_per_m2_rent = zone_data.get('precio_m2_renta_pesos', 400)
        family_size = user_profile.tamano_familia
        estimated_size = 30 + (family_size * 15)
        estimated_rent = int(price_per_m2_rent * estimated_size)
        
        # Datos destacados
        datos_destacados = {
            'seguridad_clasificacion': self.classify_score(category_scores.get('seguridad', 50)),
            'transporte_clasificacion': self.classify_score(category_scores.get('transporte', 50)),
            'precio_clasificacion': self.classify_price_score(category_scores.get('precio', 50)),
            'tiempo_estimado_trabajo': zone_data.get(f'tiempo_{user_profile.ubicacion_trabajo.lower().replace(" ", "_")}_min', 'N/A'),
            'servicios_cercanos': self.count_nearby_services(zone_data),
            'nivel_socioeconomico': zone_data.get('nivel_socioeconomico', 5)
        }
        
        return ZoneRecommendation(
            colonia=colonia,
            alcaldia=zone_data.get('alcaldia', 'N/A'),
            score_total=zone_data.get('score_general', total_score),
            score_personalizado=total_score,
            ranking=0,  # Se asignará después
            score_seguridad=category_scores.get('seguridad', 50),
            score_transporte=category_scores.get('transporte', 50),
            score_precio=category_scores.get('precio', 50),
            score_amenidades=category_scores.get('amenidades', 50),
            score_calidad_vida=category_scores.get('calidad_vida', 50),
            precio_renta_estimado=estimated_rent,
            precio_compra_m2=zone_data.get('precio_m2_venta_pesos', 40000),
            tiempo_trabajo_min=zone_data.get(f'tiempo_{user_profile.ubicacion_trabajo.lower().replace(" ", "_")}_min', 0),
            razones_principales=razones_principales,
            pros=pros,
            contras=contras,
            datos_destacados=datos_destacados
        )
    
    def generate_main_reasons(self, category_scores: Dict[str, float], 
                            weights: Dict[str, float], user_profile: UserProfile) -> List[str]:
        """Genera las principales razones de la recomendación"""
        reasons = []
        
        # Identificar top 2 categorías con mayor impacto
        weighted_scores = {
            category: score * weights.get(category, 0) 
            for category, score in category_scores.items()
        }
        top_categories = sorted(weighted_scores.items(), key=lambda x: x[1], reverse=True)[:2]
        
        for category, weighted_score in top_categories:
            if category == 'seguridad' and category_scores[category] >= 70:
                reasons.append(f"Zona muy segura (índice de seguridad: {category_scores[category]:.0f}/100)")
            elif category == 'transporte' and category_scores[category] >= 75:
                reasons.append(f"Excelente conectividad al transporte público")
            elif category == 'precio' and category_scores[category] >= 80:
                reasons.append(f"Excelente relación precio-calidad dentro de su presupuesto")
            elif category == 'amenidades' and category_scores[category] >= 70:
                reasons.append(f"Amplia variedad de servicios y amenidades cercanas")
        
        # Razón específica por estilo de vida
        if user_profile.estilo_vida == 'familiar' and user_profile.tiene_hijos:
            reasons.append("Ideal para familias con niños")
        elif user_profile.estilo_vida == 'joven_profesional':
            reasons.append("Perfecta para profesionales jóvenes")
        
        return reasons[:3]  # Máximo 3 razones principales
    
    def generate_pros(self, zone_data: Dict[str, Any], category_scores: Dict[str, float]) -> List[str]:
        """Genera lista de pros de la zona"""
        pros = []
        
        if category_scores.get('seguridad', 0) >= 80:
            pros.append("Muy seguro - bajo índice delictivo")
        
        if category_scores.get('transporte', 0) >= 75:
            pros.append("Excelente conectividad - múltiples opciones de transporte")
        
        if zone_data.get('parques_1km', 0) >= 3:
            pros.append("Múltiples parques y áreas verdes cercanas")
        
        if zone_data.get('restaurantes_1km', 0) >= 20:
            pros.append("Gran variedad gastronómica")
        
        if zone_data.get('hospitales_1km', 0) >= 2:
            pros.append("Buenos servicios médicos cerca")
        
        if zone_data.get('nivel_socioeconomico', 0) >= 7:
            pros.append("Zona de nivel socioeconómico alto")
        
        return pros[:4]  # Máximo 4 pros
    
    def generate_contras(self, zone_data: Dict[str, Any], category_scores: Dict[str, float]) -> List[str]:
        """Genera lista de contras de la zona"""
        contras = []
        
        if category_scores.get('precio', 100) <= 40:
            contras.append("Precios por encima del presupuesto ideal")
        
        if category_scores.get('seguridad', 100) <= 50:
            contras.append("Índice de seguridad moderado - precaución recomendada")
        
        if zone_data.get('densidad_poblacional', 0) >= 8000:
            contras.append("Zona densamente poblada - puede ser ruidosa")
        
        if zone_data.get('estaciones_metro_1km', 0) == 0:
            contras.append("Sin estaciones de metro muy cercanas")
        
        if zone_data.get('parques_1km', 10) <= 1:
            contras.append("Pocas áreas verdes cercanas")
        
        return contras[:3]  # Máximo 3 contras
    
    def classify_score(self, score: float) -> str:
        """Clasifica un score numérico en texto"""
        if score >= 85: return "Excelente"
        elif score >= 70: return "Muy Bueno"
        elif score >= 55: return "Bueno"
        elif score >= 40: return "Regular"
        else: return "Mejorable"
    
    def classify_price_score(self, score: float) -> str:
        """Clasifica score de precio"""
        if score >= 90: return "Muy Económico"
        elif score >= 70: return "Buen Precio"
        elif score >= 50: return "Precio Justo"
        elif score >= 30: return "Caro"
        else: return "Muy Caro"
    
    def count_nearby_services(self, zone_data: Dict[str, Any]) -> int:
        """Cuenta servicios cercanos importantes"""
        services = [
            'hospitales_1km', 'escuelas_primarias_1km', 'supermercados_1km',
            'bancos_1km', 'parques_1km'
        ]
        return sum(zone_data.get(service, 0) for service in services)
    
    def diversify_recommendations(self, recommendations: List[ZoneRecommendation], 
                                num_needed: int) -> List[ZoneRecommendation]:
        """Diversifica recomendaciones para evitar zonas muy similares"""
        if len(recommendations) <= num_needed:
            return recommendations
        
        diversified = [recommendations[0]]  # Siempre incluir la mejor
        
        for rec in recommendations[1:]:
            if len(diversified) >= num_needed:
                break
            
            # Verificar que no sea muy similar a las ya seleccionadas
            is_diverse = True
            for selected in diversified:
                if (abs(rec.score_personalizado - selected.score_personalizado) < 10 and 
                    rec.alcaldia == selected.alcaldia):
                    is_diverse = False
                    break
            
            if is_diverse:
                diversified.append(rec)
        
        # Si aún necesitamos más, llenar con las siguientes mejores
        while len(diversified) < num_needed and len(diversified) < len(recommendations):
            for rec in recommendations:
                if rec not in diversified:
                    diversified.append(rec)
                    break
        
        return diversified

def create_sample_user_profiles() -> List[UserProfile]:
    """Crea perfiles de usuario de ejemplo para testing"""
    return [
        UserProfile(
            presupuesto_max_renta=35000,
            tamano_familia=4,
            tiene_hijos=True,
            edades_hijos=[8, 12],
            prioridad_seguridad=9,
            prioridad_escuelas=8,
            prefiere_zonas_tranquilas=True,
            ubicacion_trabajo="Polanco",
            estilo_vida="familiar"
        ),
        UserProfile(
            presupuesto_max_renta=20000,
            tamano_familia=1,
            tiene_hijos=False,
            prioridad_transporte=9,
            prioridad_vida_nocturna=8,
            prioridad_precio=7,
            ubicacion_trabajo="Roma Norte",
            estilo_vida="joven_profesional"
        ),
        UserProfile(
            presupuesto_max_renta=45000,
            tamano_familia=2,
            tiene_hijos=False,
            prioridad_seguridad=9,
            prioridad_hospitales=8,
            prioridad_areas_verdes=7,
            prefiere_zonas_tranquilas=True,
            ubicacion_trabajo="Centro",
            estilo_vida="retirado"
        )
    ]

def main():
    """Función principal para demo del motor de recomendaciones"""
    print("🧠 MOTOR DE RECOMENDACIONES INTELIGENTE - DATATÓN ITAM 2025")
    print("🏆 CasaMX: Algoritmo de Scoring Personalizado")
    print("=" * 70)
    
    engine = IntelligentRecommendationEngine()
    
    # Mostrar configuración del motor
    print("\n⚙️ CONFIGURACIÓN DEL ALGORITMO:")
    print(f"   🎯 Pesos por defecto:")
    for category, weight in engine.default_weights.items():
        print(f"      • {category}: {weight:.1%}")
    
    print(f"\n👥 PERFILES DE ESTILO DE VIDA:")
    for lifestyle, config in engine.lifestyle_profiles.items():
        print(f"   🎭 {lifestyle}:")
        print(f"      • Zonas preferidas: {config['preferred_zones'][:2]}...")
        print(f"      • Amenidades clave: {config['key_amenities'][:3]}...")
    
    # Crear perfiles de ejemplo
    sample_profiles = create_sample_user_profiles()
    
    print(f"\n👤 PERFILES DE USUARIO DE EJEMPLO:")
    for i, profile in enumerate(sample_profiles, 1):
        print(f"   {i}. {profile.estilo_vida.title()} - Familia de {profile.tamano_familia}")
        print(f"      💰 Presupuesto: ${profile.presupuesto_max_renta:,}")
        print(f"      🏢 Trabajo: {profile.ubicacion_trabajo}")
        print(f"      👶 Hijos: {profile.tiene_hijos} ({profile.edades_hijos if profile.tiene_hijos else 'N/A'})")
    
    print(f"\n🚀 MOTOR DE RECOMENDACIONES LISTO")
    print(f"📊 Algoritmo personalizado con {len(engine.default_weights)} categorías")
    print(f"🎭 {len(engine.lifestyle_profiles)} perfiles de estilo de vida")
    print(f"🏙️ {len(engine.work_locations)} ubicaciones de trabajo soportadas")
    
    return engine

if __name__ == "__main__":
    engine = main()