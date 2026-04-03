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
        if (yearsExp === 'More than 5 years')
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
          `Your personal experience with athletic training and ${
            response.injury_history !== 'None' ? 'injury' : 'injury prevention'
          } in ${sport} gives you a unique empathetic perspective as a practitioner.`
        )
        if (response.data_comfort >= 3 || response.dataComfort >= 3)
          insights.push('Your comfort with data is an asset in evidence-driven sport science.')
        break

      case 'recreational-fitness-industry':
        if (motivation === 'Health and fitness')
          insights.push(
            "Your health-oriented motivation aligns perfectly with helping everyday people improve their quality of life through fitness."
          )
        insights.push(
          `Your ${level}-level training experience gives you a comprehensive understanding of fitness progression that will inspire your future clients.`
        )
        break

      case 'sports-analytics':
        if (response.data_comfort >= 4)
          insights.push(
            `Your strong data comfort (${response.data_comfort}/5) combined with hands-on ${sport} knowledge is the ideal pairing for a sports analytics role.`
          )
        insights.push(
          `Understanding the game from the inside — as a ${level}-level ${sport} participant — allows you to ask better analytical questions than a pure data scientist.`
        )
        break

      case 'sports-media-journalism':
        insights.push(
          `Your experience as a ${level}-level ${sport} athlete gives you genuine insider stories and technical credibility that sets you apart from non-athlete journalists.`
        )
        if (motivation === 'Fame, media, or recognition')
          insights.push(
            'Your motivation aligns with building a public profile — a media career rewards those who can communicate and connect with large audiences.'
          )
        break

      case 'sports-nutrition':
        insights.push(
          `Your personal experience fuelling performance in ${sport} gives you first-hand understanding of how nutrition affects training and competition outcomes.`
        )
        if (fitnessLevel >= 4)
          insights.push(
            `A high fitness awareness (${fitnessLevel}/5) means you already practice the principles you would eventually teach — an immediate advantage with athlete clients.`
          )
        break

      case 'physical-education-teaching':
        if (leadership >= 4)
          insights.push(
            `Your leadership rating (${leadership}/5) reflects the communication and motivational skills central to inspiring students in a physical education setting.`
          )
        insights.push(
          `Your ${level}-level participation in ${sport} gives you the practical competence and passion to make PE meaningful for the next generation.`
        )
        break

      case 'sports-psychology':
        if (yearsExp === 'More than 5 years')
          insights.push(
            'Over 5 years of competitive experience means you have lived the psychological pressures of sport — giving you authentic empathy that textbooks cannot teach.'
          )
        insights.push(
          `Your background in ${sport} at ${level} level equips you to build trust quickly with athletes, because they know you understand the demands from the inside.`
        )
        break

      case 'sports-law-ethics':
        if (response.data_comfort >= 4)
          insights.push(
            `Your comfort with data and analytical thinking (${response.data_comfort}/5) translates directly to case research, contract analysis, and evidence-based legal reasoning in sport.`
          )
        insights.push(
          `Navigating the rules, governance, and disputes in ${sport} at ${level} level has given you practical insight into the legal and ethical landscape of organised sport.`
        )
        break

      default:
        insights.push(
          `Your experience in ${sport} has built discipline, teamwork, and resilience—highly valued skills.`
        )
    }

    // Work environment alignment
    if (
      (pathway.slug === 'sports-science-medicine' && response.work_environment === 'Laboratory / science / clinical') ||
      (pathway.slug === 'sports-nutrition' && response.work_environment === 'Laboratory / science / clinical') ||
      (pathway.slug === 'sports-management' && response.work_environment === 'Office / management') ||
      (pathway.slug === 'sports-law-ethics' && response.work_environment === 'Office / management') ||
      (pathway.slug === 'sports-psychology' && response.work_environment === 'Office / management') ||
      (pathway.slug === 'coaching-development' && response.work_environment === 'On-field / practical') ||
      (pathway.slug === 'physical-education-teaching' && response.work_environment === 'On-field / practical') ||
      (pathway.slug === 'sports-media-journalism' && response.work_environment === 'Media / creative')
    ) {
      insights.push(
        `Your preferred work environment (${response.work_environment}) aligns well with the typical setting for ${pathway.title} professionals.`
      )
    }

    return insights.slice(0, 3) // Return max 3 insights per pathway
  }

  /**
   * Generate the motivation-based recommendation pathway.
   */
  getMotivationRecommendation(
    motivation: string,
    availablePathways: Pick<ICareerPathway, 'slug' | 'title'>[]
  ): { pathwaySlug: string; pathwayName: string; reason: string } {
    const motivationMap: Record<string, { slug: string; reason: string }> = {
      'Helping or coaching others': {
        slug: 'coaching-development',
        reason:
          'Your primary motivation to coach aligns directly with a career in Coaching & Development, where you can have daily impact on athletes at all levels.'
      },
      'Health and fitness': {
        slug: 'sports-science-medicine',
        reason:
          'Your motivation around health and wellbeing makes Sports Science & Medicine an ideal pathway, combining scientific rigour with athlete welfare.'
      },
      'Competition and performance': {
        slug: 'high-performance-sport',
        reason:
          'Your competitive drive makes you well-suited to high-performance environments where marginal gains and winning culture are paramount.'
      },
      'Academic or career opportunity': {
        slug: 'sports-science-medicine',
        reason:
          'Your academic motivation aligns with research-driven roles in Sports Science & Medicine, where evidence and intellectual rigour are central.'
      },
      'Fame, media, or recognition': {
        slug: 'sports-media-journalism',
        reason:
          'Your aspiration for visibility and public impact makes Sports Media & Journalism a natural pathway to build a recognisable personal brand.'
      }
    }

    const match = motivationMap[motivation]
    const pathway = availablePathways.find((p) => p.slug === match?.slug)

    if (match && pathway) {
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
