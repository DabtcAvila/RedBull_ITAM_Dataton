/**
 * CasaMX Recommendation Engine
 * Advanced AI-powered neighborhood matching system
 * Version: 1.0.0
 * Author: David Fernando Ávila Díaz
 */

class CasaMXRecommendationEngine {
  constructor() {
    this.neighborhoods = [];
    this.userProfile = {};
    this.weights = {
      budget: 0.25,
      security: 0.20,
      transport: 0.15,
      amenities: 0.15,
      education: 0.10,
      entertainment: 0.10,
      demographics: 0.05
    };
    this.initialized = false;
  }

  /**
   * Initialize the recommendation engine with neighborhood data
   */
  async initialize() {
    try {
      const response = await fetch('./assets/data/cdmx-neighborhoods.json');
      const data = await response.json();
      this.neighborhoods = data.neighborhoods;
      this.initialized = true;
      console.log('✅ Recommendation Engine initialized with', this.neighborhoods.length, 'neighborhoods');
      return true;
    } catch (error) {
      console.error('❌ Failed to initialize recommendation engine:', error);
      return false;
    }
  }

  /**
   * Calculate comprehensive recommendation score for a neighborhood
   * @param {Object} neighborhood - Neighborhood data
   * @param {Object} userPrefs - User preferences
   * @returns {Object} Detailed scoring breakdown
   */
  calculateMatch(neighborhood, userPrefs) {
    const scores = {};
    let totalScore = 0;

    // 1. Budget Compatibility (25% weight)
    scores.budget = this.calculateBudgetScore(neighborhood, userPrefs);
    totalScore += scores.budget * this.weights.budget;

    // 2. Security Score (20% weight)
    scores.security = this.calculateSecurityScore(neighborhood, userPrefs);
    totalScore += scores.security * this.weights.security;

    // 3. Transport Accessibility (15% weight)
    scores.transport = this.calculateTransportScore(neighborhood, userPrefs);
    totalScore += scores.transport * this.weights.transport;

    // 4. Amenities & Lifestyle (15% weight)
    scores.amenities = this.calculateAmenitiesScore(neighborhood, userPrefs);
    totalScore += scores.amenities * this.weights.amenities;

    // 5. Education Quality (10% weight - higher if has children)
    scores.education = this.calculateEducationScore(neighborhood, userPrefs);
    const educationWeight = userPrefs.hasChildren ? 0.20 : 0.05;
    totalScore += scores.education * educationWeight;

    // 6. Entertainment & Culture (10% weight)
    scores.entertainment = this.calculateEntertainmentScore(neighborhood, userPrefs);
    totalScore += scores.entertainment * this.weights.entertainment;

    // 7. Demographics Fit (5% weight)
    scores.demographics = this.calculateDemographicsScore(neighborhood, userPrefs);
    totalScore += scores.demographics * this.weights.demographics;

    // 8. Special Bonuses/Penalties
    const adjustments = this.calculateAdjustments(neighborhood, userPrefs);
    totalScore += adjustments.total;

    // Ensure score is between 0 and 100
    const finalScore = Math.max(0, Math.min(100, totalScore * 100));

    return {
      totalScore: finalScore,
      breakdown: scores,
      adjustments: adjustments,
      confidence: this.calculateConfidence(scores, userPrefs)
    };
  }

  /**
   * Calculate budget compatibility score
   */
  calculateBudgetScore(neighborhood, userPrefs) {
    const budget = userPrefs.budget;
    const { min, max, average } = neighborhood.price_range;

    // Perfect match if budget is within range
    if (budget >= min && budget <= max) {
      // Even better if close to average
      const distanceFromAverage = Math.abs(budget - average) / average;
      return Math.max(0.8, 1.0 - distanceFromAverage);
    }

    // Penalty for being outside range
    if (budget < min) {
      const shortfall = (min - budget) / min;
      return Math.max(0, 1.0 - shortfall * 2);
    }

    if (budget > max) {
      const excess = (budget - max) / max;
      return Math.max(0.3, 1.0 - excess * 0.5); // Less penalty for higher budget
    }

    return 0.5;
  }

  /**
   * Calculate security score based on user priority
   */
  calculateSecurityScore(neighborhood, userPrefs) {
    const baseScore = neighborhood.scores.security / 10;
    const priority = userPrefs.priorities.security / 10;
    
    // High priority users need high security neighborhoods
    if (priority >= 0.8 && baseScore < 0.7) {
      return baseScore * 0.6; // Heavy penalty
    }
    
    return baseScore;
  }

  /**
   * Calculate transport accessibility score
   */
  calculateTransportScore(neighborhood, userPrefs) {
    const baseScore = neighborhood.scores.transport / 10;
    const priority = userPrefs.priorities.transport / 10;
    
    // Bonus for metro access
    const metroBonus = neighborhood.features.metro_stations.length > 0 ? 0.1 : 0;
    
    return Math.min(1.0, baseScore + metroBonus);
  }

  /**
   * Calculate amenities and lifestyle score
   */
  calculateAmenitiesScore(neighborhood, userPrefs) {
    const baseScore = neighborhood.scores.amenities / 10;
    const priority = userPrefs.priorities.amenities / 10;
    
    // Count quality amenities
    let amenityBonus = 0;
    
    // Shopping centers
    if (neighborhood.features.shopping_centers.length >= 2) {
      amenityBonus += 0.05;
    }
    
    // Healthcare facilities
    if (neighborhood.features.hospitals.length >= 2) {
      amenityBonus += 0.05;
    }
    
    // Parks and recreation
    if (neighborhood.features.parks.length >= 2) {
      amenityBonus += 0.05;
    }
    
    return Math.min(1.0, baseScore + amenityBonus);
  }

  /**
   * Calculate education quality score
   */
  calculateEducationScore(neighborhood, userPrefs) {
    const baseScore = neighborhood.scores.education / 10;
    
    if (!userPrefs.hasChildren) {
      return baseScore * 0.5; // Less important without children
    }
    
    // Bonus for international schools (important for expats)
    const internationalSchoolBonus = neighborhood.features.schools.some(school => 
      school.includes('American') || 
      school.includes('International') || 
      school.includes('Franco') ||
      school.includes('Alemán')
    ) ? 0.15 : 0;
    
    return Math.min(1.0, baseScore + internationalSchoolBonus);
  }

  /**
   * Calculate entertainment and culture score
   */
  calculateEntertainmentScore(neighborhood, userPrefs) {
    const baseScore = neighborhood.scores.entertainment / 10;
    const priority = userPrefs.priorities.entertainment / 10;
    
    // Young professionals value entertainment more
    if (userPrefs.familySize <= 2 && !userPrefs.hasChildren) {
      return Math.min(1.0, baseScore + 0.1);
    }
    
    return baseScore;
  }

  /**
   * Calculate demographics compatibility
   */
  calculateDemographicsScore(neighborhood, userPrefs) {
    const demographics = neighborhood.demographics;
    let score = 0;
    let factors = 0;
    
    // Expat friendliness (for non-Mexican users)
    if (userPrefs.country !== 'mexico') {
      score += demographics.expat_friendly / 10;
      factors++;
    }
    
    // Family orientation
    if (userPrefs.hasChildren) {
      score += demographics.family_oriented / 10;
      factors++;
    } else if (userPrefs.familySize <= 2) {
      score += demographics.young_professional / 10;
      factors++;
    }
    
    return factors > 0 ? score / factors : 0.7; // Default if no specific factors
  }

  /**
   * Calculate special adjustments and bonuses
   */
  calculateAdjustments(neighborhood, userPrefs) {
    const adjustments = {
      items: [],
      total: 0
    };

    // Luxury zone bonus for high budget
    if (userPrefs.budget > 60000 && neighborhood.tags?.includes('luxury')) {
      adjustments.items.push({ reason: 'Luxury zone match', value: 0.05 });
      adjustments.total += 0.05;
    }

    // Embassy zone bonus for internationals
    if (userPrefs.country !== 'mexico' && neighborhood.tags?.includes('embassy_zone')) {
      adjustments.items.push({ reason: 'Embassy zone (expat friendly)', value: 0.08 });
      adjustments.total += 0.08;
    }

    // Cultural bonus for specific preferences
    if (userPrefs.country === 'france' && neighborhood.tags?.includes('cultural')) {
      adjustments.items.push({ reason: 'Cultural district match', value: 0.06 });
      adjustments.total += 0.06;
    }

    // Young professional bonus
    if (userPrefs.familySize <= 2 && !userPrefs.hasChildren) {
      if (neighborhood.tags?.includes('hipster') || neighborhood.tags?.includes('nightlife')) {
        adjustments.items.push({ reason: 'Young professional lifestyle', value: 0.07 });
        adjustments.total += 0.07;
      }
    }

    // Safety penalty for low-security high-priority users
    if (userPrefs.priorities.security >= 8 && neighborhood.scores.security < 7.5) {
      adjustments.items.push({ reason: 'Security concerns', value: -0.15 });
      adjustments.total -= 0.15;
    }

    // Budget student bonus
    if (userPrefs.budget < 20000 && neighborhood.tags?.includes('affordable')) {
      adjustments.items.push({ reason: 'Budget-friendly option', value: 0.04 });
      adjustments.total += 0.04;
    }

    return adjustments;
  }

  /**
   * Calculate confidence level in recommendation
   */
  calculateConfidence(scores, userPrefs) {
    let confidence = 0.5;
    
    // Higher confidence if strong matches in top priorities
    const priorities = userPrefs.priorities;
    const topPriorities = Object.entries(priorities)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 3);
    
    for (const [category, priority] of topPriorities) {
      if (scores[category] && scores[category] > 0.8) {
        confidence += 0.15;
      }
    }
    
    // Lower confidence for edge cases
    if (scores.budget < 0.5) confidence -= 0.2;
    if (scores.security < 0.6 && priorities.security > 7) confidence -= 0.15;
    
    return Math.max(0.3, Math.min(0.95, confidence));
  }

  /**
   * Get personalized recommendations
   * @param {Object} userPrefs - User preferences object
   * @param {number} limit - Maximum number of recommendations (default: 5)
   * @returns {Array} Sorted array of neighborhood recommendations
   */
  async getRecommendations(userPrefs, limit = 5) {
    if (!this.initialized) {
      await this.initialize();
    }

    console.log('🔍 Calculating recommendations for user preferences:', userPrefs);

    const recommendations = this.neighborhoods.map(neighborhood => {
      const matchData = this.calculateMatch(neighborhood, userPrefs);
      
      return {
        neighborhood,
        score: matchData.totalScore,
        breakdown: matchData.breakdown,
        adjustments: matchData.adjustments,
        confidence: matchData.confidence,
        reasons: this.generateReasons(neighborhood, matchData, userPrefs)
      };
    });

    // Sort by score (highest first)
    recommendations.sort((a, b) => b.score - a.score);

    const topRecommendations = recommendations.slice(0, limit);

    console.log('✅ Top recommendations calculated:', topRecommendations.map(r => ({
      name: r.neighborhood.name,
      score: Math.round(r.score),
      confidence: Math.round(r.confidence * 100)
    })));

    return topRecommendations;
  }

  /**
   * Generate human-readable reasons for recommendation
   */
  generateReasons(neighborhood, matchData, userPrefs) {
    const reasons = [];
    const breakdown = matchData.breakdown;

    // Budget reasons
    if (breakdown.budget > 0.8) {
      reasons.push(`💰 Perfecto para tu presupuesto de $${userPrefs.budget.toLocaleString()}`);
    } else if (breakdown.budget < 0.5) {
      reasons.push(`💸 Fuera de tu rango de presupuesto`);
    }

    // Security reasons
    if (breakdown.security > 0.8 && userPrefs.priorities.security >= 8) {
      reasons.push(`🛡️ Zona altamente segura (${neighborhood.safety_index}/100)`);
    }

    // Transport reasons
    if (breakdown.transport > 0.8) {
      const metros = neighborhood.features.metro_stations;
      reasons.push(`🚇 Excelente conectividad (${metros.length} estaciones de metro)`);
    }

    // Family reasons
    if (userPrefs.hasChildren && breakdown.education > 0.8) {
      reasons.push(`🎓 Excelentes escuelas para tus hijos`);
    }

    // Expat reasons
    if (userPrefs.country !== 'mexico' && neighborhood.demographics.expat_friendly > 8) {
      reasons.push(`🌍 Muy amigable para expatriados`);
    }

    // Lifestyle reasons
    if (!userPrefs.hasChildren && breakdown.entertainment > 0.8) {
      reasons.push(`🎭 Vida nocturna y entretenimiento vibrante`);
    }

    // Adjustments reasons
    matchData.adjustments.items.forEach(adj => {
      if (adj.value > 0.05) {
        reasons.push(`⭐ ${adj.reason}`);
      } else if (adj.value < -0.05) {
        reasons.push(`⚠️ ${adj.reason}`);
      }
    });

    return reasons.slice(0, 4); // Limit to most important reasons
  }

  /**
   * Get demo case recommendations
   * @param {string} caseId - Demo case identifier
   * @returns {Array} Recommendations for demo case
   */
  async getDemoRecommendations(caseId) {
    try {
      const response = await fetch('./assets/data/demo-cases.json');
      const data = await response.json();
      
      const demoCase = data.demo_cases.find(c => c.id === caseId);
      if (!demoCase) {
        throw new Error(`Demo case ${caseId} not found`);
      }

      // Convert demo case to user preferences format
      const userPrefs = {
        budget: demoCase.criteria.budget,
        familySize: demoCase.criteria.family_size,
        hasChildren: demoCase.criteria.has_children,
        country: demoCase.country.toLowerCase().split(' ')[0], // Extract country code
        priorities: demoCase.criteria.priorities
      };

      const recommendations = await this.getRecommendations(userPrefs, 3);
      
      return {
        case: demoCase,
        recommendations
      };
    } catch (error) {
      console.error('❌ Failed to get demo recommendations:', error);
      return null;
    }
  }

  /**
   * Validate user input
   */
  validateUserInput(userPrefs) {
    const errors = [];

    if (!userPrefs.budget || userPrefs.budget < 1000 || userPrefs.budget > 500000) {
      errors.push('Budget must be between $1,000 and $500,000 MXN');
    }

    if (!userPrefs.familySize || userPrefs.familySize < 1 || userPrefs.familySize > 10) {
      errors.push('Family size must be between 1 and 10');
    }

    if (typeof userPrefs.hasChildren !== 'boolean') {
      errors.push('Has children must be true or false');
    }

    const requiredPriorities = ['security', 'transport', 'amenities', 'education', 'price', 'entertainment'];
    for (const priority of requiredPriorities) {
      const value = userPrefs.priorities?.[priority];
      if (!value || value < 1 || value > 10) {
        errors.push(`${priority} priority must be between 1 and 10`);
      }
    }

    return {
      isValid: errors.length === 0,
      errors
    };
  }

  /**
   * Get neighborhood details by ID
   */
  getNeighborhoodById(id) {
    return this.neighborhoods.find(n => n.id === id);
  }

  /**
   * Get all neighborhoods for map display
   */
  getAllNeighborhoods() {
    return this.neighborhoods;
  }

  /**
   * Filter neighborhoods by criteria
   */
  filterNeighborhoods(filters) {
    return this.neighborhoods.filter(neighborhood => {
      // Budget filter
      if (filters.maxBudget && neighborhood.price_range.min > filters.maxBudget) {
        return false;
      }
      
      if (filters.minBudget && neighborhood.price_range.max < filters.minBudget) {
        return false;
      }

      // Security filter
      if (filters.minSecurity && neighborhood.scores.security < filters.minSecurity) {
        return false;
      }

      // Tags filter
      if (filters.tags && !filters.tags.some(tag => neighborhood.tags?.includes(tag))) {
        return false;
      }

      return true;
    });
  }
}

// Export for use in main app
window.CasaMXRecommendationEngine = CasaMXRecommendationEngine;