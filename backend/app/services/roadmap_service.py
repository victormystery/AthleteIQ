"""
Roadmap Service
Generates personalized development roadmaps based on career pathway and student profile
"""
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from sqlalchemy.orm import Session

from app.services.career_analysis_service import career_analysis_service
from app.crud import pathway_crud, recommendation_crud, progress_crud, questionnaire_crud

logger = logging.getLogger(__name__)


class RoadmapService:
    """
    Service for generating personalized career development roadmaps.
    Combines career pathway data with student profile information
    to create tailored step-by-step development plans.
    """

    def __init__(self):
        self.career_service = career_analysis_service
        # Roadmap templates for each career pathway
        self.roadmap_templates = self._load_roadmap_templates()

    def _load_roadmap_templates(self) -> Dict[str, List[Dict]]:
        """
        Load roadmap step templates for each career pathway.
        These are combined with user-specific data to create personalized roadmaps.
        """
        return {
            "Coaching & Development": [
                {
                    "id": "cd-1",
                    "title": "Complete Sports Science Foundation",
                    "description": "Build a solid academic foundation in sports science, physical education, or a related field.",
                    "type": "academic",
                    "duration": "3-4 years",
                    "cost": "£9,250/year (UK tuition)",
                    "priority": "required",
                    "details": [
                        "Enrol in BSc Sports Science, Physical Education, or Sports Coaching",
                        "Focus on modules in exercise physiology, biomechanics, and sport psychology",
                        "Maintain strong academic performance (2:1 or above recommended)",
                        "Volunteer as student coaching assistant during university",
                    ],
                    "resources": [
                        {"name": "UCAS Sports Science Courses", "url": "https://www.ucas.com", "type": "course"},
                        {"name": "BASES Student Resources", "url": "https://www.bases.org.uk", "type": "article"},
                    ],
                },
                {
                    "id": "cd-2",
                    "title": "Obtain Level 1-2 Coaching Qualification",
                    "description": "Gain entry-level coaching certifications recognized by national governing bodies.",
                    "type": "certification",
                    "duration": "2-4 weeks",
                    "cost": "£150-£300",
                    "priority": "required",
                    "details": [
                        "Complete FA Level 1 or equivalent NGB coaching award",
                        "Progress to Level 2 coaching certification",
                        "Learn fundamental coaching methodologies and session planning",
                        "Gain practical experience through supervised coaching sessions",
                    ],
                    "resources": [
                        {"name": "FA Coaching Courses", "url": "https://www.thefa.com/coaching", "type": "course"},
                        {"name": "UK Coaching", "url": "https://www.ukcoaching.org", "type": "article"},
                    ],
                },
                {
                    "id": "cd-3",
                    "title": "Build Practical Coaching Experience",
                    "description": "Accumulate hands-on coaching hours working with athletes at various levels.",
                    "type": "experience",
                    "duration": "6-12 months",
                    "cost": "Free (voluntary)",
                    "priority": "required",
                    "details": [
                        "Volunteer at local sports clubs and community programmes",
                        "Assist experienced coaches at school or university level",
                        "Log at least 100 coaching hours across different age groups",
                        "Seek mentorship from an experienced Level 3+ coach",
                    ],
                    "resources": [
                        {"name": "Sport England Volunteering", "url": "https://www.sportengland.org", "type": "article"},
                    ],
                },
                {
                    "id": "cd-4",
                    "title": "Develop Core Coaching Skills",
                    "description": "Strengthen communication, leadership, and athlete management capabilities.",
                    "type": "skill",
                    "duration": "Ongoing",
                    "cost": "£50-£200 (workshops)",
                    "priority": "recommended",
                    "details": [
                        "Attend coaching workshops on communication and leadership",
                        "Study sports psychology for effective athlete motivation",
                        "Learn session planning, periodization, and programme design",
                        "Practice video analysis and performance feedback techniques",
                    ],
                    "resources": [
                        {"name": "Coaching Psychology Manual", "type": "book"},
                        {"name": "UK Coaching Workshops", "url": "https://www.ukcoaching.org", "type": "course"},
                    ],
                },
                {
                    "id": "cd-5",
                    "title": "Pursue UEFA B / Level 3 Coaching License",
                    "description": "Obtain advanced coaching qualifications to work with competitive athletes.",
                    "type": "certification",
                    "duration": "6-12 months",
                    "cost": "£800-£1,500",
                    "priority": "recommended",
                    "details": [
                        "Complete UEFA B License or Level 3 NGB coaching award",
                        "Demonstrate advanced tactical and technical coaching ability",
                        "Submit portfolio of coaching practice and reflections",
                        "Pass practical assessments with real coaching sessions",
                    ],
                    "resources": [
                        {"name": "UEFA Coaching Pathway", "url": "https://www.uefa.com", "type": "course"},
                    ],
                },
                {
                    "id": "cd-6",
                    "title": "Build Professional Network",
                    "description": "Connect with coaching professionals and join industry organizations.",
                    "type": "networking",
                    "duration": "Ongoing",
                    "cost": "£50-£150/year (membership)",
                    "priority": "recommended",
                    "details": [
                        "Join professional coaching organizations (CIMSPA, UK Coaching)",
                        "Attend coaching conferences and CPD events",
                        "Connect with coaches on LinkedIn and coaching forums",
                        "Seek employment at sports academies or development centres",
                    ],
                    "resources": [
                        {"name": "CIMSPA Membership", "url": "https://www.cimspa.co.uk", "type": "article"},
                    ],
                },
            ],
            "Sports Management": [
                {
                    "id": "sm-1",
                    "title": "Complete Business/Sports Management Degree",
                    "description": "Obtain a relevant degree in sports management, business, or a related discipline.",
                    "type": "academic",
                    "duration": "3-4 years",
                    "cost": "£9,250/year (UK tuition)",
                    "priority": "required",
                    "details": [
                        "Enrol in BA/BSc Sports Management, Business, or Event Management",
                        "Focus on modules covering sports marketing, finance, and law",
                        "Complete industry placement or year in industry if available",
                        "Develop project management and analytical skills",
                    ],
                    "resources": [
                        {"name": "UCAS Sports Management Courses", "url": "https://www.ucas.com", "type": "course"},
                    ],
                },
                {
                    "id": "sm-2",
                    "title": "Gain Event Management Experience",
                    "description": "Get hands-on experience organizing sports events at various scales.",
                    "type": "experience",
                    "duration": "6-12 months",
                    "cost": "Free (voluntary/internship)",
                    "priority": "required",
                    "details": [
                        "Volunteer at university sports events and competitions",
                        "Intern with local sports organizations or venues",
                        "Help organize community sports tournaments or charity events",
                        "Document your event portfolio with outcomes and metrics",
                    ],
                    "resources": [
                        {"name": "EventBrite Sports Jobs", "url": "https://www.eventbrite.co.uk", "type": "article"},
                    ],
                },
                {
                    "id": "sm-3",
                    "title": "Develop Business & Leadership Skills",
                    "description": "Build core competencies in management, strategy, and communication.",
                    "type": "skill",
                    "duration": "Ongoing",
                    "cost": "£100-£500 (courses)",
                    "priority": "required",
                    "details": [
                        "Study financial management and budgeting for sports organizations",
                        "Learn sports marketing, sponsorship, and brand management",
                        "Develop strategic planning and organizational leadership skills",
                        "Complete workshops on stakeholder management and communication",
                    ],
                    "resources": [
                        {"name": "FutureLearn Sports Business Courses", "url": "https://www.futurelearn.com", "type": "course"},
                    ],
                },
                {
                    "id": "sm-4",
                    "title": "Obtain Event/Sports Administration Certification",
                    "description": "Earn professional certifications to validate your expertise.",
                    "type": "certification",
                    "duration": "3-6 months",
                    "cost": "£300-£800",
                    "priority": "recommended",
                    "details": [
                        "Complete a Level 3 Event Management or Sports Administration qualification",
                        "Consider CIMSPA professional registration",
                        "Explore project management certifications (PRINCE2, Agile)",
                        "Document CPD hours for professional development",
                    ],
                    "resources": [
                        {"name": "CIMSPA Qualifications", "url": "https://www.cimspa.co.uk", "type": "course"},
                    ],
                },
                {
                    "id": "sm-5",
                    "title": "Build Industry Network & Secure Role",
                    "description": "Leverage your qualifications and experience to enter the sports management field.",
                    "type": "networking",
                    "duration": "3-6 months",
                    "cost": "£50-£200 (memberships/events)",
                    "priority": "recommended",
                    "details": [
                        "Join professional bodies (Sport & Recreation Alliance, ISRM)",
                        "Attend sports industry conferences and networking events",
                        "Apply for graduate schemes at sports organizations",
                        "Consider MSc Sports Business or MBA for career advancement",
                    ],
                    "resources": [
                        {"name": "Sport & Recreation Alliance", "url": "https://www.sportandrecreation.org.uk", "type": "article"},
                    ],
                },
            ],
            "High Performance Sport": [
                {
                    "id": "hp-1",
                    "title": "Assess Competitive Level & Set Goals",
                    "description": "Evaluate your current athletic ability and define clear performance targets.",
                    "type": "skill",
                    "duration": "1-2 months",
                    "cost": "£100-£300 (assessment)",
                    "priority": "required",
                    "details": [
                        "Complete a comprehensive fitness and performance assessment",
                        "Identify your strengths and areas for development",
                        "Set SMART performance goals with measurable targets",
                        "Research elite pathway requirements for your sport",
                    ],
                    "resources": [
                        {"name": "UK Sport Performance Pathway", "url": "https://www.uksport.gov.uk", "type": "article"},
                    ],
                },
                {
                    "id": "hp-2",
                    "title": "Join Elite Training Programme",
                    "description": "Access high-quality coaching and training facilities through academy or development programmes.",
                    "type": "experience",
                    "duration": "1-3 years",
                    "cost": "Variable (£0-£5,000/year)",
                    "priority": "required",
                    "details": [
                        "Trial for professional academy or development programme",
                        "Train with high-level coaches and alongside elite athletes",
                        "Follow structured periodization and training plans",
                        "Access sport science support (nutrition, psychology, S&C)",
                    ],
                    "resources": [
                        {"name": "English Institute of Sport", "url": "https://www.eis2win.co.uk", "type": "article"},
                    ],
                },
                {
                    "id": "hp-3",
                    "title": "Compete at National/International Level",
                    "description": "Build your competitive resume through national and international competitions.",
                    "type": "experience",
                    "duration": "Ongoing",
                    "cost": "Variable (travel/entry fees)",
                    "priority": "required",
                    "details": [
                        "Compete in national championships and qualifying events",
                        "Seek selection for representative squads and national teams",
                        "Maintain competition log and performance analytics",
                        "Work with performance analyst for tactical preparation",
                    ],
                    "resources": [
                        {"name": "British Universities & Colleges Sport", "url": "https://www.bucs.org.uk", "type": "article"},
                    ],
                },
                {
                    "id": "hp-4",
                    "title": "Develop Mental Resilience & Recovery Skills",
                    "description": "Build psychological strength and optimize recovery for sustained high performance.",
                    "type": "skill",
                    "duration": "Ongoing",
                    "cost": "£50-£200/session",
                    "priority": "recommended",
                    "details": [
                        "Work with a sport psychologist on mental toughness and focus",
                        "Implement recovery protocols (sleep, nutrition, active recovery)",
                        "Learn injury prevention and rehabilitation strategies",
                        "Develop pre-competition routines and visualization techniques",
                    ],
                    "resources": [
                        {"name": "BPS Sport & Exercise Psychology", "url": "https://www.bps.org.uk", "type": "article"},
                    ],
                },
                {
                    "id": "hp-5",
                    "title": "Plan Dual Career & Transition Strategy",
                    "description": "Prepare for life during and after competitive sport with education and career options.",
                    "type": "academic",
                    "duration": "Ongoing",
                    "cost": "Variable",
                    "priority": "recommended",
                    "details": [
                        "Maintain academic studies alongside athletic career",
                        "Explore dual career support programmes at your university",
                        "Develop transferable skills (media, coaching, business)",
                        "Plan transition pathways for post-competitive career",
                    ],
                    "resources": [
                        {"name": "TASS Dual Career Programme", "url": "https://www.tass.gov.uk", "type": "article"},
                    ],
                },
            ],
            "Sports Science / Medicine": [
                {
                    "id": "ss-1",
                    "title": "Complete BSc in Sports Science",
                    "description": "Obtain an accredited degree in sports science, exercise science, or sports therapy.",
                    "type": "academic",
                    "duration": "3-4 years",
                    "cost": "£9,250/year (UK tuition)",
                    "priority": "required",
                    "details": [
                        "Enrol in BASES-accredited BSc Sports Science or Exercise Science",
                        "Focus on physiology, biomechanics, performance analysis, and nutrition",
                        "Complete laboratory-based practical work and research projects",
                        "Achieve a 2:1 or above for postgraduate study eligibility",
                    ],
                    "resources": [
                        {"name": "BASES Accredited Courses", "url": "https://www.bases.org.uk", "type": "course"},
                    ],
                },
                {
                    "id": "ss-2",
                    "title": "Gain Research & Lab Experience",
                    "description": "Develop practical research skills through laboratory work and data collection.",
                    "type": "experience",
                    "duration": "6-12 months",
                    "cost": "Free (university lab)",
                    "priority": "required",
                    "details": [
                        "Assist academics with research projects during your degree",
                        "Learn VO2max testing, motion capture, and force plate analysis",
                        "Develop proficiency in data analysis (Excel, SPSS, Python)",
                        "Present research findings at student conferences",
                    ],
                    "resources": [
                        {"name": "BASES Student Conference", "url": "https://www.bases.org.uk", "type": "article"},
                    ],
                },
                {
                    "id": "ss-3",
                    "title": "Pursue MSc / Postgraduate Qualification",
                    "description": "Advance your academic credentials with a specialist postgraduate degree.",
                    "type": "academic",
                    "duration": "1-2 years",
                    "cost": "£8,000-£15,000",
                    "priority": "recommended",
                    "details": [
                        "Complete MSc in Sport & Exercise Science, Performance Analysis, or Physiotherapy",
                        "Conduct an original research dissertation in your area of interest",
                        "Build specialist expertise (e.g., biomechanics, nutrition, psychology)",
                        "Network with practitioners and researchers in your field",
                    ],
                    "resources": [
                        {"name": "FindAMasters Sports Science", "url": "https://www.findamasters.com", "type": "course"},
                    ],
                },
                {
                    "id": "ss-4",
                    "title": "Obtain BASES Accreditation or HCPC Registration",
                    "description": "Gain professional accreditation required for practice in sports science or therapy.",
                    "type": "certification",
                    "duration": "1-2 years (supervised)",
                    "cost": "£500-£1,500",
                    "priority": "required",
                    "details": [
                        "Apply for BASES Supervised Experience (SE) programme",
                        "Complete supervised practice hours with accredited mentor",
                        "Submit portfolio of professional practice and CPD",
                        "For physiotherapy: complete HCPC registration process",
                    ],
                    "resources": [
                        {"name": "BASES Accreditation", "url": "https://www.bases.org.uk", "type": "course"},
                        {"name": "HCPC Registration", "url": "https://www.hcpc-uk.org", "type": "article"},
                    ],
                },
                {
                    "id": "ss-5",
                    "title": "Build Professional Practice Network",
                    "description": "Establish yourself in the sports science community and secure professional roles.",
                    "type": "networking",
                    "duration": "Ongoing",
                    "cost": "£100-£300/year (memberships)",
                    "priority": "recommended",
                    "details": [
                        "Maintain BASES membership and attend annual conferences",
                        "Publish research in peer-reviewed journals",
                        "Seek employment with professional sports teams or clinics",
                        "Consider PhD for academic career or elite sport positions",
                    ],
                    "resources": [
                        {"name": "BASES Membership", "url": "https://www.bases.org.uk", "type": "article"},
                    ],
                },
            ],
            "Recreational / Fitness Industry": [
                {
                    "id": "rf-1",
                    "title": "Obtain Level 2 Fitness Instructor Qualification",
                    "description": "Earn your entry-level fitness industry qualification to work in gyms and leisure centres.",
                    "type": "certification",
                    "duration": "6-12 weeks",
                    "cost": "£400-£800",
                    "priority": "required",
                    "details": [
                        "Complete a CIMSPA-endorsed Level 2 Gym Instructor course",
                        "Learn anatomy, physiology, and exercise programming fundamentals",
                        "Pass practical assessments in exercise technique and instruction",
                        "Obtain first aid and safeguarding certifications",
                    ],
                    "resources": [
                        {"name": "CIMSPA Endorsed Courses", "url": "https://www.cimspa.co.uk", "type": "course"},
                        {"name": "Active IQ Qualifications", "url": "https://www.activeiq.co.uk", "type": "course"},
                    ],
                },
                {
                    "id": "rf-2",
                    "title": "Progress to Level 3 Personal Training",
                    "description": "Advance to personal training qualification to work independently with clients.",
                    "type": "certification",
                    "duration": "3-6 months",
                    "cost": "£1,000-£2,500",
                    "priority": "required",
                    "details": [
                        "Complete Level 3 Personal Training diploma or certificate",
                        "Develop skills in programme design and client consultation",
                        "Learn nutrition fundamentals and behaviour change techniques",
                        "Build a portfolio of training programmes and case studies",
                    ],
                    "resources": [
                        {"name": "REPs Register", "url": "https://www.exerciseregister.org", "type": "article"},
                    ],
                },
                {
                    "id": "rf-3",
                    "title": "Gain Practical Industry Experience",
                    "description": "Build your client base and practical skills in real gym environments.",
                    "type": "experience",
                    "duration": "6-12 months",
                    "cost": "Free (employment)",
                    "priority": "required",
                    "details": [
                        "Work in a gym or leisure centre to develop floor experience",
                        "Build a client base through gym floor interactions and referrals",
                        "Practice programming for diverse client populations",
                        "Collect client testimonials and track outcomes",
                    ],
                    "resources": [
                        {"name": "ukactive Job Board", "url": "https://www.ukactive.com", "type": "article"},
                    ],
                },
                {
                    "id": "rf-4",
                    "title": "Specialize with Additional Qualifications",
                    "description": "Differentiate yourself with specialist skills in high-demand areas.",
                    "type": "course",
                    "duration": "2-8 weeks per course",
                    "cost": "£200-£600 per course",
                    "priority": "recommended",
                    "details": [
                        "Choose specializations: strength & conditioning, yoga, Pilates, or group exercise",
                        "Complete sport-specific conditioning qualifications",
                        "Obtain nutrition advice certification (Level 3 Nutrition)",
                        "Consider pre/post-natal or older adult exercise qualifications",
                    ],
                    "resources": [
                        {"name": "CIMSPA CPD Hub", "url": "https://www.cimspa.co.uk", "type": "course"},
                    ],
                },
                {
                    "id": "rf-5",
                    "title": "Build Your Brand & Online Presence",
                    "description": "Establish yourself as a trusted fitness professional in your community and online.",
                    "type": "networking",
                    "duration": "Ongoing",
                    "cost": "£50-£300 (marketing/tools)",
                    "priority": "recommended",
                    "details": [
                        "Create social media profiles showcasing your expertise",
                        "Develop a website or booking platform for client management",
                        "Offer free workshops or online content to build credibility",
                        "Join CIMSPA as a registered professional",
                    ],
                    "resources": [
                        {"name": "Canva for Marketing", "url": "https://www.canva.com", "type": "article"},
                        {"name": "CIMSPA Registration", "url": "https://www.cimspa.co.uk", "type": "article"},
                    ],
                },
            ],
        }

    def generate_personalized_roadmap(
        self,
        db: Session,
        user_id: str,
        pathway_slug: str,
    ) -> Dict[str, Any]:
        """
        Generate a personalized development roadmap for a user based on their
        recommended career pathway and profile information.
        """
        from app.database.models import CareerPathway, Profile, QuestionnaireResponse

        # Get pathway info
        pathway = db.query(CareerPathway).filter(CareerPathway.slug == pathway_slug).first()
        if not pathway:
            return {"error": f"Pathway '{pathway_slug}' not found"}

        # Get user profile
        profile = db.query(Profile).filter(Profile.user_id == user_id).first()

        # Get latest questionnaire
        questionnaire = (
            db.query(QuestionnaireResponse)
            .filter(QuestionnaireResponse.user_id == user_id)
            .order_by(QuestionnaireResponse.created_at.desc())
            .first()
        )

        # Get existing progress
        user_progress = progress_crud.get_by_user_and_pathway(
            db, user_id=user_id, pathway_id=pathway.id
        )
        completed_milestones = {p.milestone for p in user_progress if str(p.status) == "completed"}

        # Find matching roadmap template
        roadmap_steps = self._get_template_steps(pathway.title)

        # Personalize steps based on user profile
        personalized_steps = self._personalize_steps(
            steps=roadmap_steps,
            profile=profile,
            questionnaire=questionnaire,
            completed_milestones=completed_milestones,
        )

        # Calculate progress
        total = len(personalized_steps)
        completed = sum(1 for s in personalized_steps if s.get("is_completed"))
        progress_pct = round((completed / total * 100), 1) if total > 0 else 0

        # Estimate total duration
        estimated_duration = self._estimate_duration(personalized_steps)

        # Build personalization context
        personalization_factors = {}
        if profile:
            personalization_factors["academic_level"] = f"Year {profile.year_of_study}" if profile.year_of_study else None
            personalization_factors["sport"] = profile.primary_sport
            personalization_factors["university"] = profile.university
        if questionnaire and questionnaire.answers:
            answers = questionnaire.answers
            personalization_factors["motivation"] = answers.get("motivation")
            personalization_factors["fitness_level"] = answers.get("fitness_level")
            personalization_factors["leadership"] = answers.get("leadership")

        return {
            "pathway_id": pathway.id,
            "pathway_title": pathway.title,
            "pathway_slug": pathway.slug,
            "student_name": profile.full_name if profile else None,
            "academic_level": f"Year {profile.year_of_study}" if profile and profile.year_of_study else None,
            "primary_sport": profile.primary_sport if profile else None,
            "total_steps": total,
            "completed_steps": completed,
            "progress_percentage": progress_pct,
            "estimated_duration": estimated_duration,
            "steps": personalized_steps,
            "generated_at": datetime.utcnow().isoformat(),
            "personalization_factors": personalization_factors,
        }

    def _get_template_steps(self, pathway_title: str) -> List[Dict]:
        """Get roadmap template steps for a pathway, with fallback to generic steps."""
        # Try exact match first
        if pathway_title in self.roadmap_templates:
            return self.roadmap_templates[pathway_title]

        # Try partial match
        for key, steps in self.roadmap_templates.items():
            if key.lower() in pathway_title.lower() or pathway_title.lower() in key.lower():
                return steps

        # Fallback generic roadmap
        return [
            {
                "id": "gen-1",
                "title": "Research Career Requirements",
                "description": "Understand the qualifications and experience needed for your chosen career.",
                "type": "academic",
                "duration": "1-2 weeks",
                "cost": "Free",
                "priority": "required",
                "details": [
                    "Research job listings and role requirements",
                    "Identify required qualifications and certifications",
                    "Speak to professionals already working in the field",
                    "Map out the typical career progression pathway",
                ],
                "resources": [{"name": "Prospects Career Advice", "url": "https://www.prospects.ac.uk", "type": "article"}],
            },
            {
                "id": "gen-2",
                "title": "Complete Relevant Education",
                "description": "Obtain the academic qualifications needed for your career path.",
                "type": "academic",
                "duration": "1-4 years",
                "cost": "Variable",
                "priority": "required",
                "details": [
                    "Enrol in relevant degree or diploma programme",
                    "Focus on applicable modules and skills",
                    "Complete placement or work experience components",
                    "Build a portfolio of relevant projects and achievements",
                ],
                "resources": [],
            },
            {
                "id": "gen-3",
                "title": "Gain Practical Experience",
                "description": "Build hands-on experience through internships, volunteering, or part-time work.",
                "type": "experience",
                "duration": "6-12 months",
                "cost": "Free",
                "priority": "required",
                "details": [
                    "Seek internships or work experience placements",
                    "Volunteer in relevant organizations",
                    "Build a track record of achievements and outcomes",
                    "Collect references and testimonials",
                ],
                "resources": [],
            },
            {
                "id": "gen-4",
                "title": "Obtain Professional Certifications",
                "description": "Earn industry-recognized certifications to enhance your credentials.",
                "type": "certification",
                "duration": "1-6 months",
                "cost": "£200-£1,500",
                "priority": "recommended",
                "details": [
                    "Identify the most valued certifications in your field",
                    "Complete certification requirements and assessments",
                    "Maintain CPD for ongoing professional development",
                ],
                "resources": [],
            },
            {
                "id": "gen-5",
                "title": "Build Professional Network",
                "description": "Connect with professionals and organizations in your target field.",
                "type": "networking",
                "duration": "Ongoing",
                "cost": "£50-£200/year",
                "priority": "recommended",
                "details": [
                    "Join professional organizations and attend events",
                    "Connect with mentors and industry contacts",
                    "Apply for entry-level positions in your target area",
                ],
                "resources": [],
            },
        ]

    def _personalize_steps(
        self,
        steps: List[Dict],
        profile,
        questionnaire,
        completed_milestones: set,
    ) -> List[Dict]:
        """Personalize roadmap steps based on user data."""
        personalized = []

        for i, step in enumerate(steps):
            p_step = {**step, "order": i + 1}

            # Mark completed based on progress tracking
            if step["title"] in completed_milestones or step["id"] in completed_milestones:
                p_step["is_completed"] = True
            else:
                p_step["is_completed"] = False

            # Add sport-specific context if available
            if profile and profile.primary_sport:
                sport = profile.primary_sport
                if step["type"] == "certification" and "coaching" in step["title"].lower():
                    p_step["description"] = step["description"].replace(
                        "national governing bodies",
                        f"national governing bodies for {sport}",
                    )
                if step["type"] == "experience":
                    for j, detail in enumerate(p_step["details"]):
                        if "local sports clubs" in detail.lower():
                            p_step["details"][j] = detail.replace(
                                "local sports clubs",
                                f"local {sport} clubs",
                            )

            # Adjust priority based on academic level
            if profile and profile.year_of_study:
                if profile.year_of_study >= 3 and step["type"] == "academic" and step["priority"] == "required":
                    # If near graduation, academic steps may be nearing completion
                    if "foundation" in step["title"].lower() or "degree" in step["title"].lower():
                        p_step["description"] = step["description"] + " (You may be completing or have completed this step.)"

            personalized.append(p_step)

        return personalized

    def _estimate_duration(self, steps: List[Dict]) -> str:
        """Estimate total duration from required steps."""
        required = [s for s in steps if s.get("priority") == "required"]
        if not required:
            return "6-12 months"

        # Simple estimation based on step count
        count = len(required)
        if count <= 2:
            return "3-6 months"
        elif count <= 4:
            return "1-3 years"
        else:
            return "3-5 years"

    def get_user_roadmap_summary(self, db: Session, user_id: str) -> Dict[str, Any]:
        """Get a summary of all roadmaps for a user based on their recommendations."""
        # Get user's recommendations
        recommendations = recommendation_crud.get_by_user(db, user_id=user_id)
        if not recommendations:
            return {
                "total_roadmaps": 0,
                "active_roadmaps": 0,
                "overall_progress": 0.0,
                "roadmaps": [],
            }

        roadmaps = []
        total_progress = 0
        for rec in recommendations[:3]:  # Top 3 recommended pathways
            if rec.pathway:
                roadmap = self.generate_personalized_roadmap(
                    db, user_id=user_id, pathway_slug=rec.pathway.slug
                )
                if "error" not in roadmap:
                    roadmaps.append({
                        "pathway_title": roadmap["pathway_title"],
                        "pathway_slug": roadmap["pathway_slug"],
                        "total_steps": roadmap["total_steps"],
                        "completed_steps": roadmap["completed_steps"],
                        "progress_percentage": roadmap["progress_percentage"],
                        "match_score": rec.match_score,
                        "rank": rec.rank,
                    })
                    total_progress += roadmap["progress_percentage"]

        avg_progress = round(total_progress / len(roadmaps), 1) if roadmaps else 0

        return {
            "total_roadmaps": len(roadmaps),
            "active_roadmaps": len([r for r in roadmaps if r["progress_percentage"] < 100]),
            "overall_progress": avg_progress,
            "roadmaps": roadmaps,
        }


# Singleton instance
roadmap_service = RoadmapService()
