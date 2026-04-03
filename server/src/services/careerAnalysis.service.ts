import type { IQuestionnaireResponse } from '../models/QuestionnaireResponse.model.js'
import type { ICareerPathway } from '../models/CareerPathway.model.js'
import { logger } from '../utils/logger.js'

interface SportInsight {
  pathwaySlug: string
  insights: string[]
}

interface CareerScore {
  [careerName: string]: number
}

interface RecommendationResult {
  rank: number
  career: string
  confidence: number
  reason: string
  insights?: string[]
}

interface FallbackRecommendations {
  primaryPrediction: string
  allRecommendations: RecommendationResult[]
  probabilities: number[]
  classes: string[]
}

interface StudentDataPrepared {
  academic_level: string
  primary_sport: string
  experience_years: string
  participation_level: string
  fitness: string
  technical_skill: string
  leadership: string
  data_comfort: string
  primary_motivation: string
  career_importance: string
  work_environment: string
  biggest_challenge: string
  injury_history: string
  education_commitment: string
}

interface MLPredictionResult {
  primaryPrediction: string
  probabilities: number[]
  sortedIndices: number[]
}

interface FeatureImportance {
  [feature: string]: number
}

/**
 * Enhanced Career Analysis Service
 * Combines ML-based predictions with rule-based scoring and narrative insights
 * Mirrors Python ml_service.py functionality for consistent recommendations
 */
export class CareerAnalysisService {
  private sportCareerData: Record<string, any> = {}
  private careerDetails: Record<string, any> = {}
  private mlModelLoaded: boolean = false
  private careerClasses: string[] = [
    'Coaching & Development',
    'Sports Management',
    'High Performance Sport',
    'Sports Science / Medicine',
    'Recreational / Fitness Industry'
  ]

  constructor() {
    this.initializeSportCareerData()
    this.initializeCareerDetails()
    this.initializeMLModel()
  }

  /**
   * Initialize ML model (stub for future joblib/TensorFlow.js integration)
   * TODO: Integrate with actual trained Random Forest model
   */
  private initializeMLModel(): void {
    try {
      // Future: Load trained ML model from joblib/TensorFlow.js
      // For now, use rule-based fallback with note
      logger.info('ML model initialization - using fallback rule-based recommendations')
      this.mlModelLoaded = false
    } catch (error) {
      logger.warn('ML model not loaded, using rule-based recommendations', { error })
      this.mlModelLoaded = false
    }
  }

  /**
   * Check if ML model is available
   */
  isMLModelLoaded(): boolean {
    return this.mlModelLoaded
  }

  /**
   * Prepare student data by mapping frontend fields to model feature names
   * Mirrors Python ml_service.prepare_student_data()
   */
  prepareStudentData(studentData: any): StudentDataPrepared {
    return {
      academic_level: String(studentData.academic_level || ''),
      primary_sport: String(studentData.primary_sport || studentData.primarySport || ''),
      experience_years: String(studentData.participation_years || studentData.participationYears || ''),
      participation_level: String(studentData.participation_level || studentData.participationLevel || ''),
      fitness: String(studentData.fitness_level || studentData.fitnessLevel || '3'),
      technical_skill: String(studentData.technical_skill || studentData.technicalSkill || '3'),
      leadership: String(studentData.leadership || '3'),
      data_comfort: String(studentData.data_comfort || studentData.dataComfort || '3'),
      primary_motivation: String(studentData.motivation || ''),
      career_importance: String(studentData.career_importance || studentData.careerImportance || ''),
      work_environment: String(studentData.work_environment || studentData.workEnvironment || ''),
      biggest_challenge: String(studentData.biggest_challenge || studentData.biggestChallenge || ''),
      injury_history: String(studentData.injury_history || studentData.injuryHistory || 'No injuries'),
      education_commitment: String(studentData.education_level || studentData.educationLevel || '')
    }
  }

  /**
   * Get ML predictions (stub - prepare for actual model integration)
   * Future: Load actual Random Forest predictions from trained model
   */
  getMLPredictions(preparedData: StudentDataPrepared): MLPredictionResult {
    // TODO: Call actual ML model when available
    // For now, return structure matching Python service

    if (!this.mlModelLoaded) {
      logger.debug('ML model not available, will use rule-based fallback')
      return {
        primaryPrediction: this.careerClasses[0],
        probabilities: this.careerClasses.map(() => 1 / this.careerClasses.length),
        sortedIndices: Array.from({ length: this.careerClasses.length }, (_, i) => i)
      }
    }

    // Placeholder for actual model prediction
    return {
      primaryPrediction: this.careerClasses[0],
      probabilities: this.careerClasses.map(() => 1 / this.careerClasses.length),
      sortedIndices: Array.from({ length: this.careerClasses.length }, (_, i) => i)
    }
  }

  /**
   * Create 5 ML-based recommendations from model predictions
   * Mirrors Python ml_service.create_ml_recommendations()
   */
  createMLRecommendations(
    probabilities: number[],
    sortedIndices: number[]
  ): RecommendationResult[] {
    const recommendations: RecommendationResult[] = []
    const maxRecommendations = Math.min(5, this.careerClasses.length)

    for (let i = 0; i < maxRecommendations; i++) {
      const idx = sortedIndices[i]
      recommendations.push({
        rank: i + 1,
        career: this.careerClasses[idx],
        confidence: Math.round(probabilities[idx] * 100),
        reason: 'ML Prediction based on your profile'
      })
    }

    return recommendations
  }

  /**
   * Create 6th motivation-based recommendation
   * Mirrors Python ml_service.create_motivation_recommendation()
   */
  createMotivationRecommendation(
    primaryMotivation: string,
    probabilities: number[],
    sortedIndices: number[]
  ): RecommendationResult {
    // Motivation-to-Career mapping from notebook analysis
    const motivationMap: Record<string, string> = {
      'Competition and performance': 'High Performance Sport',
      'Health and fitness': 'Recreational / Fitness Industry',
      'Helping or coaching others': 'Coaching & Development',
      'Academic or career opportunity': 'Sports Science / Medicine',
      'Fame, media, or recognition': 'Sports Management'
    }

    const motivationCareer = motivationMap[primaryMotivation] || this.careerClasses[0]

    // Calculate weighted confidence (75% of top prediction)
    const weightedConfidence = Math.round(probabilities[sortedIndices[0]] * 75)

    return {
      rank: 6,
      career: motivationCareer,
      confidence: weightedConfidence,
      reason: `Based on your primary motivation: ${primaryMotivation}`
    }
  }

  /**
   * Get comprehensive recommendations combining ML + motivation
   * Mirrors Python ml_service.get_comprehensive_recommendations()
   */
  getComprehensiveRecommendations(studentData: any): any {
    try {
      // Prepare student data
      const preparedData = this.prepareStudentData(studentData)

      // Get ML predictions (or fallback)
      const mlResult = this.getMLPredictions(preparedData)

      // Create 5 ML-based recommendations
      const mlRecommendations = this.createMLRecommendations(
        mlResult.probabilities,
        mlResult.sortedIndices
      )

      // Create 6th motivation-based recommendation
      const motivationRec = this.createMotivationRecommendation(
        studentData.motivation || '',
        mlResult.probabilities,
        mlResult.sortedIndices
      )

      // Combine all recommendations
      const allRecommendations = [...mlRecommendations, motivationRec]

      return {
        primaryPrediction: mlResult.primaryPrediction,
        allRecommendations,
        probabilities: mlResult.probabilities,
        classes: this.careerClasses,
        modelAvailable: this.mlModelLoaded
      }
    } catch (error) {
      logger.error('Error generating comprehensive recommendations:', { error })
      throw error
    }
  }

  /**
   * Initialize sport-to-career preference data from analysis
   */
  private initializeSportCareerData(): void {
    this.sportCareerData = {
      'Football (Soccer)': {
        totalStudents: 45,
        preferences: [
          { career: 'Coaching & Development', percentage: 42.2, count: 19, popularity: 'Very Popular' },
          { career: 'Sports Management', percentage: 26.7, count: 12, popularity: 'Popular' },
          { career: 'High Performance Sport', percentage: 15.6, count: 7, popularity: 'Moderate' },
          { career: 'Sports Science / Medicine', percentage: 11.1, count: 5, popularity: 'Common' },
          { career: 'Recreational / Fitness Industry', percentage: 4.4, count: 2, popularity: 'Low' }
        ]
      },
      Basketball: {
        totalStudents: 28,
        preferences: [
          { career: 'High Performance Sport', percentage: 39.3, count: 11, popularity: 'Very Popular' },
          { career: 'Coaching & Development', percentage: 32.1, count: 9, popularity: 'Popular' },
          { career: 'Sports Management', percentage: 17.9, count: 5, popularity: 'Moderate' },
          { career: 'Sports Science / Medicine', percentage: 7.1, count: 2, popularity: 'Low' },
          { career: 'Recreational / Fitness Industry', percentage: 3.6, count: 1, popularity: 'Low' }
        ]
      },
      'Athletics / Track & Field': {
        totalStudents: 22,
        preferences: [
          { career: 'Sports Science / Medicine', percentage: 36.4, count: 8, popularity: 'Very Popular' },
          { career: 'Coaching & Development', percentage: 31.8, count: 7, popularity: 'Popular' },
          { career: 'High Performance Sport', percentage: 18.2, count: 4, popularity: 'Moderate' },
          { career: 'Sports Management', percentage: 9.1, count: 2, popularity: 'Low' },
          { career: 'Recreational / Fitness Industry', percentage: 4.5, count: 1, popularity: 'Low' }
        ]
      }
    }
  }

  /**
   * Initialize detailed career pathway information
   */
  private initializeCareerDetails(): void {
    this.careerDetails = {
      'Coaching & Development': {
        id: 'coaching',
        title: 'Coaching & Development',
        description: 'Shape and develop the next generation of athletes through coaching and mentorship',
        requirements: {
          education: ['Sports Science degree', 'Physical Education'],
          skills: ['Communication', 'Leadership', 'Technical expertise', 'Patience'],
          certifications: ['UEFA B License', 'FA Coaching Badges', 'Level 2/3 Coaching'],
          experience: '1-2 years playing/coaching experience'
        },
        timeToEntry: '6-12 months',
        costLevel: 'Medium',
        averageSalary: '£25,000 - £45,000',
        jobOutlook: 'Growing demand, especially youth development',
        programs: ['FA Coaching Badges', 'UEFA Coaching License', 'Sports Pedagogy Certificate']
      },
      'Sports Management': {
        id: 'management',
        title: 'Sports Management',
        description: 'Lead and manage sports organizations, events, and business operations',
        requirements: {
          education: ['Business/Sports Management degree'],
          skills: ['Leadership', 'Business acumen', 'Project management', 'Communication'],
          certifications: ['Event Management', 'Sports Administration'],
          experience: '2-3 years in sports industry'
        },
        timeToEntry: '3-4 years',
        costLevel: 'High',
        averageSalary: '£28,000 - £55,000',
        jobOutlook: 'Stable with opportunities in growing sports sector',
        programs: ['BA Sports Management', 'MBA Sports Business', 'Event Management Certificate']
      },
      'High Performance Sport': {
        id: 'professional_athlete',
        title: 'High Performance Sport',
        description: 'Compete at elite levels as a professional athlete',
        requirements: {
          education: ['Not required (but helpful)'],
          skills: ['Elite performance', 'Mental resilience', 'Dedication', 'Physical conditioning'],
          certifications: ['Sport-specific qualifications'],
          experience: 'Years of competitive experience'
        },
        timeToEntry: 'Immediate (if qualified)',
        costLevel: 'Low',
        averageSalary: '£20,000 - £200,000+ (highly variable)',
        jobOutlook: 'Extremely competitive, limited positions',
        programs: ['Academy Programs', 'Professional Trials', 'Elite Training Centers']
      },
      'Sports Science / Medicine': {
        id: 'sports_science',
        title: 'Sports Science / Medicine',
        description: 'Apply scientific principles to optimize athletic performance and health',
        requirements: {
          education: ['BSc/MSc Sports Science', 'Sports Therapy', 'Physiotherapy'],
          skills: ['Research', 'Data analysis', 'Scientific knowledge', 'Problem-solving'],
          certifications: ['BASES accreditation', 'HCPC registration'],
          experience: 'Research/clinical experience'
        },
        timeToEntry: '3-5 years',
        costLevel: 'High',
        averageSalary: '£25,000 - £50,000',
        jobOutlook: 'Growing field with increasing demand',
        programs: ['BSc Sports Science', 'MSc Performance Analysis', 'PhD Sport & Exercise']
      },
      'Recreational / Fitness Industry': {
        id: 'fitness',
        title: 'Recreational / Fitness Industry',
        description: 'Promote health and fitness in community and commercial settings',
        requirements: {
          education: ['Fitness qualifications', 'Sports Studies'],
          skills: ['Motivation', 'Communication', 'Knowledge of exercise science'],
          certifications: ['Level 2/3 Fitness Instructor', 'Personal Training'],
          experience: '6-12 months training'
        },
        timeToEntry: '3-6 months',
        costLevel: 'Low',
        averageSalary: '£18,000 - £35,000',
        jobOutlook: 'Strong growth in wellness sector',
        programs: ['Fitness Instructor Course', 'Personal Training Diploma', 'Group Exercise']
      }
    }
  }

  /**
   * Build sport-specific narrative insights for a given pathway
   */
  getInsightsForPathway(
    pathway: Pick<ICareerPathway, 'slug' | 'title' | 'keySkills'>,
    response: any
  ): string[] {
    const insights: string[] = []
    const sport = response.primary_sport || response.primarySport
    const level = response.participation_level || response.participationLevel
    const leadership = response.leadership
    const technicalSkill = response.technical_skill || response.technicalSkill
    const fitnessLevel = response.fitness_level || response.fitnessLevel
    const motivation = response.motivation
    const yearsExp = response.participation_years || response.participationYears

    insights.push(
      `Your background in ${sport} at ${level} level gives you credibility and first-hand understanding that employers highly value.`
    )

    switch (pathway.slug) {
      case 'coaching-development':
        if (leadership >= 4)
          insights.push(
            `Your strong leadership rating (${leadership}/5) indicates you are well-suited to guiding athletes through development phases.`
          )
        if (yearsExp === '> 5')
          insights.push(
            'Over 5 years of participation means you bring experiential knowledge that benefits coaching positions.'
          )
        break

      case 'sports-management':
        if (response.data_comfort >= 4 || response.dataComfort >= 4)
          insights.push(
            `Your data comfort will help you make evidence-based decisions in commercial sports management.`
          )
        insights.push(`Experience managing competitive pressures has built strategic thinking required.`)
        break

      case 'high-performance-sport':
        if (fitnessLevel >= 4)
          insights.push(
            `Your high fitness awareness (${fitnessLevel}/5) and elite exposure in ${sport} deepens understanding of performance demands.`
          )
        if (technicalSkill >= 4)
          insights.push(`High technical skill (${technicalSkill}/5) is valuable in elite-level analysis roles.`)
        break

      case 'sports-science-medicine':
        insights.push(
          `Your personal experience with athletic training in ${sport} provides unique perspective as a practitioner.`
        )
        if (response.data_comfort >= 3 || response.dataComfort >= 3)
          insights.push('Your comfort with data is an asset in evidence-driven sport science.')
        break

      case 'recreational-fitness-industry':
        if (motivation === 'Health')
          insights.push('Your health-oriented motivation aligns with helping people improve fitness.')
        insights.push(`Your ${level}-level training experience provides comprehensive fitness progression knowledge.`)
        break

      default:
        insights.push(
          `Your experience in ${sport} has built discipline, teamwork, and resilience—highly valued skills.`
        )
    }

    return insights.slice(0, 3)
  }

  /**
   * Generate feature importance analysis (stub for future ML model)
   * Mirrors Python ml_service.get_feature_importance()
   */
  getFeatureImportance(): FeatureImportance {
    // TODO: Extract from actual trained Random Forest model when available
    if (!this.mlModelLoaded) {
      return {}
    }

    // Placeholder importance scores
    return {
      primary_sport: 0.18,
      participation_level: 0.15,
      leadership: 0.12,
      primary_motivation: 0.11,
      technical_skill: 0.1,
      fitness: 0.09,
      data_comfort: 0.08,
      experience_years: 0.07,
      academic_level: 0.06,
      work_environment: 0.04
    }
  }

  /**
   * Generate rule-based fallback recommendations (existing logic)
   */
  generateFallbackRecommendations(studentData: any): FallbackRecommendations {
    logger.info('Generating fallback recommendations based on rules')

    const careerScores: CareerScore = {
      'Coaching & Development': 0,
      'Sports Management': 0,
      'High Performance Sport': 0,
      'Sports Science / Medicine': 0,
      'Recreational / Fitness Industry': 0
    }

    const careerInterests = studentData.career_interests || studentData.careerInterests || []
    if (Array.isArray(careerInterests)) {
      for (const interest of careerInterests) {
        const lowerInterest = interest.toLowerCase()
        if (lowerInterest.includes('coach')) careerScores['Coaching & Development'] += 40
        if (lowerInterest.includes('manage') || lowerInterest.includes('business'))
          careerScores['Sports Management'] += 40
        if (lowerInterest.includes('athlete') || lowerInterest.includes('player'))
          careerScores['High Performance Sport'] += 40
        if (lowerInterest.includes('science') || lowerInterest.includes('research'))
          careerScores['Sports Science / Medicine'] += 40
        if (lowerInterest.includes('fitness') || lowerInterest.includes('health'))
          careerScores['Recreational / Fitness Industry'] += 40
      }
    }

    const motivation = String(studentData.motivation || '').toLowerCase()
    if (motivation.includes('coaching') || motivation.includes('helping'))
      careerScores['Coaching & Development'] += 30
    if (motivation.includes('competition') || motivation.includes('performance'))
      careerScores['High Performance Sport'] += 30
    if (motivation.includes('academic') || motivation.includes('career'))
      careerScores['Sports Science / Medicine'] += 25

    const leadership = studentData.leadership || 3
    if (leadership >= 4) {
      careerScores['Coaching & Development'] += 15
      careerScores['Sports Management'] += 15
    }

    const dataComfort = studentData.data_comfort || studentData.dataComfort || 3
    if (dataComfort >= 4) careerScores['Sports Science / Medicine'] += 15

    const fitnessLevel = studentData.fitness_level || studentData.fitnessLevel || 3
    const technicalSkill = studentData.technical_skill || studentData.technicalSkill || 3
    if (fitnessLevel >= 4 && technicalSkill >= 4) careerScores['High Performance Sport'] += 20

    const sortedCareers = Object.entries(careerScores).sort(([, a], [, b]) => b - a)

    const recommendations: RecommendationResult[] = sortedCareers.map(([career, score], i) => ({
      rank: i + 1,
      career,
      confidence: Math.min(score, 95),
      reason: 'Based on your interests, skills, and preferences'
    }))

    return {
      primaryPrediction: recommendations[0]?.career || 'Coaching & Development',
      allRecommendations: recommendations.slice(0, 6),
      probabilities: recommendations.slice(0, 6).map((r) => r.confidence),
      classes: recommendations.slice(0, 6).map((r) => r.career)
    }
  }

  /**
   * Get sport-specific insights
   */
  getInsightsForSport(sport: string): any {
    const sportData = this.sportCareerData[sport]

    if (!sportData) {
      return {
        hasSportData: false,
        sport,
        insights: [
          { career: 'Coaching & Development', percentage: 35.0, popularity: 'Popular' },
          { career: 'Sports Management', percentage: 30.0, popularity: 'Popular' }
        ]
      }
    }

    return {
      hasSportData: true,
      sport,
      totalStudents: sportData.totalStudents,
      insights: sportData.preferences.slice(0, 4)
    }
  }

  /**
   * Get detailed career pathway information
   */
  getCareerDetails(careerName: string): any {
    return this.careerDetails[careerName] || null
  }

  /**
   * Get all career details
   */
  getAllCareerDetails(): any[] {
    return Object.values(this.careerDetails)
  }

  /**
   * Enhance recommendations with detailed career information
   */
  enhanceRecommendationsWithDetails(recommendations: any[]): any[] {
    return recommendations.map((rec) => {
      const careerName = rec.career
      let details = null

      for (const [key, value] of Object.entries(this.careerDetails)) {
        if (key.includes(careerName) || careerName.includes(key)) {
          details = { ...value }
          break
        }
      }

      return details ? { ...rec, details } : rec
    })
  }
}

export const careerAnalysisService = new CareerAnalysisService()
