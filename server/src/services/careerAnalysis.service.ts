import type { IQuestionnaireResponse } from '../models/QuestionnaireResponse.model.js'
import type { ICareerPathway } from '../models/CareerPathway.model.js'

interface SportInsight {
  pathwaySlug: string
  insights: string[]
}

/**
 * Generates sport-specific narrative insights for each recommended pathway
 * based on the athlete's questionnaire responses.
 */
export class CareerAnalysisService {
  /**
   * Build sport-specific insights for a given pathway based on the questionnaire.
   */
  getInsightsForPathway(
    pathway: Pick<ICareerPathway, 'slug' | 'title' | 'keySkills'>,
    response: IQuestionnaireResponse
  ): string[] {
    const insights: string[] = []
    const sport = response.primary_sport
    const level = response.participation_level
    const leadership = response.leadership
    const technicalSkill = response.technical_skill
    const fitnessLevel = response.fitness_level
    const motivation = response.motivation
    const yearsExp = response.participation_years

    // Sport-background opening
    insights.push(
      `Your background in ${sport} at ${level} level gives you credibility and first-hand understanding that employers in this field highly value.`
    )

    // Pathway-specific insight
    switch (pathway.slug) {
      case 'coaching-development':
        if (leadership >= 4)
          insights.push(
            `Your strong leadership rating (${leadership}/5) indicates you are well-suited to guiding athletes through complex development phases.`
          )
        if (yearsExp === '> 5')
          insights.push(
            'Over 5 years of participation means you bring a depth of experiential knowledge that new coaches without your athletic background simply cannot replicate.'
          )
        break

      case 'sports-management':
        if (response.data_comfort >= 4)
          insights.push(
            `Your data comfort (${response.data_comfort}/5) will help you make evidence-based decisions in commercial and operational sports management contexts.`
          )
        insights.push(
          `Experience managing the pressures of competitive ${sport} has built the resilience and strategic thinking sports management demands.`
        )
        break

      case 'high-performance-sport':
        if (fitnessLevel >= 4)
          insights.push(
            `Your high fitness awareness (${fitnessLevel}/5) and elite-level exposure in ${sport} mean you deeply understand the demands placed on high-performance athletes.`
          )
        if (technicalSkill >= 4)
          insights.push(
            `High technical skill (${technicalSkill}/5) suggests you have an analytical eye for performance detail — critical in elite-level analysis and S&C roles.`
          )
        break

      case 'sports-science-medicine':
        insights.push(
          `Your personal experience with athletic training and ${
            response.injury_history !== 'No injuries' ? 'injury' : 'injury prevention'
          } in ${sport} gives you a unique empathetic perspective as a practitioner.`
        )
        if (response.data_comfort >= 3)
          insights.push(
            'Your comfort with data is an asset in lab-based and evidence-driven sport science environments.'
          )
        break

      case 'recreational-fitness-industry':
        if (motivation === 'Health')
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
        if (motivation === 'Fame')
          insights.push(
            'Your motivation aligns with building a public profile — a media career rewards those who can communicate and connect with large audiences.'
          )
        break

      default:
        insights.push(
          `Your experience in ${sport} has built transferable skills — discipline, teamwork, and resilience — that are highly valued in this career pathway.`
        )
    }

    // Work environment alignment
    if (
      (pathway.slug === 'sports-science-medicine' && response.work_environment === 'Lab') ||
      (pathway.slug === 'sports-management' && response.work_environment === 'Office') ||
      (pathway.slug === 'coaching-development' && response.work_environment === 'Field')
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
      Coaching: {
        slug: 'coaching-development',
        reason:
          'Your primary motivation to coach aligns directly with a career in Coaching & Development, where you can have daily impact on athletes at all levels.'
      },
      Health: {
        slug: 'sports-science-medicine',
        reason:
          'Your motivation around health and wellbeing makes Sports Science & Medicine an ideal pathway, combining scientific rigour with athlete welfare.'
      },
      Competition: {
        slug: 'high-performance-sport',
        reason:
          'Your competitive drive makes you well-suited to high-performance environments where marginal gains and winning culture are paramount.'
      },
      Academic: {
        slug: 'sports-science-medicine',
        reason:
          'Your academic motivation aligns with research-driven roles in Sports Science & Medicine, where evidence and intellectual rigour are central.'
      },
      Fame: {
        slug: 'sports-media-journalism',
        reason:
          'Your aspiration for visibility and public impact makes Sports Media & Journalism a natural pathway to build a recognisable personal brand.'
      }
    }

    const match = motivationMap[motivation]
    const pathway = availablePathways.find((p) => p.slug === match?.slug)

    if (match && pathway) {
      return {
        pathwaySlug: pathway.slug,
        pathwayName: pathway.title,
        reason: match.reason
      }
    }

    // Fallback
    return {
      pathwaySlug: 'coaching-development',
      pathwayName: 'Coaching & Development',
      reason:
        'Based on your profile, Coaching & Development offers a strong blend of athlete interaction, leadership, and career growth.'
    }
  }
}

export const careerAnalysisService = new CareerAnalysisService()
