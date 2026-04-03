"""
Database Service
Handles database operations and data seeding
"""
import logging
from sqlalchemy.orm import Session
from typing import List

from app.database.models import CareerPathway
from app.crud.pathway import pathway_crud
from app.utils.constants import PATHWAY_TO_PROGRAMMES

logger = logging.getLogger(__name__)


def seed_career_pathways(db: Session) -> List[CareerPathway]:
    """
    Seed initial career pathway data into database
    
    Args:
        db: Database session
        
    Returns:
        List of created pathways
    """
    pathways_data = [
        # 1. Professional Athlete
        {
            "slug": "professional-athlete",
            "title": "Professional Athlete",
            "description": "Compete at elite levels in your chosen sport and represent clubs at national and international levels",
            "icon": "🏆",
            "color": "#10B981",
            "work_environment": "Training grounds, stadiums, and travel for competitions. Physically demanding with irregular hours",
            "job_outlook": "Highly competitive with limited positions. Success depends heavily on talent, dedication, and opportunity",
            "salary_range_min": 25000,
            "salary_range_max": 500000,
            "salary_currency": "GBP",
            "requirements": {
                "education": ["Academy training", "Professional development programs"],
                "skills": ["Technical excellence", "Tactical awareness", "Physical fitness", "Mental strength", "Team collaboration"],
                "certifications": ["Sports-specific qualifications", "Anti-doping education"],
                "experience": "Years of competitive experience at youth and academy levels"
            },
            "education_requirements": [
                "Academy training programmes",
                "BTEC Level 3 Extended Diploma in Sport",
                "A-Level Physical Education",
                "Professional development courses"
            ],
            "key_skills": [
                "Technical excellence",
                "Tactical awareness",
                "Physical fitness",
                "Mental strength",
                "Team collaboration"
            ],
            "certifications": [
                "Anti-doping education certification",
                "Sports psychology qualifications",
                "Performance nutrition courses"
            ],
            "career_progression": [
                {"level": "Entry", "title": "Youth Academy", "years": "16-18"},
                {"level": "Mid", "title": "Reserve/U23 Team", "years": "18-21"},
                {"level": "Senior", "title": "First Team Player", "years": "21-28"},
                {"level": "Veteran", "title": "Senior Career", "years": "28-35"}
            ]
        },
        # 2. Coaching
        {
            "slug": "coaching",
            "title": "Coach / Coaching Education",
            "description": "Shape and develop the next generation of athletes through teaching, mentoring, and tactical guidance",
            "icon": "👨‍🏫",
            "color": "#3B82F6",
            "work_environment": "Training facilities, classrooms, and match venues. Flexible hours including evenings and weekends",
            "job_outlook": "Growing demand at all levels from grassroots to professional. Increasing opportunities in women's football",
            "salary_range_min": 22000,
            "salary_range_max": 120000,
            "salary_currency": "GBP",
            "requirements": {
                "education": ["Sports coaching degree", "Physical education background"],
                "skills": ["Leadership", "Communication", "Tactical analysis", "Player development", "Motivation"],
                "certifications": ["UEFA B License", "FA Coaching Badges", "First Aid certification"],
                "experience": "1-2 years coaching experience minimum"
            },
            "education_requirements": [
                "BSc Sports Coaching",
                "BSc Physical Education",
                "Sports Science degree",
                "BSc (Hons) Psychology - RCL",
                "BSc (Hons) Psychology with Applications in Sport and Exercise - UoGM"
            ],
            "key_skills": [
                "Leadership",
                "Communication",
                "Tactical analysis",
                "Player development",
                "Motivation"
            ],
            "certifications": [
                "FA Level 1 Certificate",
                "FA Level 2 (UEFA C)",
                "UEFA B License",
                "First Aid Certification"
            ],
            "career_progression": [
                {"level": "Entry", "title": "Assistant Coach", "years": "0-3"},
                {"level": "Mid", "title": "Youth Coach", "years": "3-6"},
                {"level": "Senior", "title": "Head Coach", "years": "6-10"},
                {"level": "Lead", "title": "Director of Coaching", "years": "10+"}
            ]
        },
        # 3. Sports Science
        {
            "slug": "sports-science",
            "title": "Sports Science / Performance Science",
            "description": "Apply scientific principles to optimize athletic performance through research, testing, and data analysis",
            "icon": "🔬",
            "color": "#8B5CF6",
            "work_environment": "Laboratories, training grounds, and office settings. Regular hours with some competition travel",
            "job_outlook": "Strong growth with increasing emphasis on data-driven performance optimization in professional sport",
            "salary_range_min": 28000,
            "salary_range_max": 85000,
            "salary_currency": "GBP",
            "requirements": {
                "education": ["BSc/MSc Sports Science", "Exercise Science degree"],
                "skills": ["Research design", "Data analysis", "Laboratory skills", "Communication", "Problem-solving"],
                "certifications": ["BASES Accreditation", "Strength & Conditioning certifications"],
                "experience": "Research and applied experience required"
            },
            "education_requirements": [
                "BSc Sports Science (e.g., BSc Sport and Exercise Science at RCL)",
                "MSc Performance Analysis",
                "BSc Sport and Exercise Nutrition - RCL",
                "MSc Applied Sport and Exercise Science"
            ],
            "key_skills": [
                "Research design",
                "Data analysis",
                "Laboratory skills",
                "Communication",
                "Problem-solving"
            ],
            "certifications": [
                "BASES Accreditation",
                "Laboratory Testing Certifications"
            ],
            "career_progression": [
                {"level": "Entry", "title": "Graduate Scientist", "years": "0-2"},
                {"level": "Mid", "title": "Sports Scientist", "years": "2-5"},
                {"level": "Senior", "title": "Senior Scientist", "years": "5-10"},
                {"level": "Lead", "title": "Head of Performance", "years": "10+"}
            ]
        },
        # 4. Strength & Conditioning
        {
            "slug": "strength_conditioning",
            "title": "Strength & Conditioning Coach",
            "description": "Design and implement training programs to develop athletes' physical capabilities and prevent injuries",
            "icon": "💪",
            "color": "#F97316",
            "work_environment": "Gym facilities, training grounds, and travel with teams. Early mornings and varied schedules",
            "job_outlook": "Growing field with opportunities in professional clubs, private facilities, and national federations",
            "salary_range_min": 24000,
            "salary_range_max": 70000,
            "salary_currency": "GBP",
            "requirements": {
                "education": ["BSc Sports Science", "BSc Exercise Physiology"],
                "skills": ["Program design", "Movement analysis", "Communication", "Motivation", "Injury prevention"],
                "certifications": ["UKSCA Accreditation", "NSCA-CSCS"],
                "experience": "Practical coaching experience required"
            },
            "education_requirements": [
                "BSc Sport and Exercise Science",
                "BSc Exercise Physiology",
                "MSc Strength and Conditioning - UoGM"
            ],
            "key_skills": [
                "Program design",
                "Movement analysis",
                "Communication",
                "Motivation",
                "Injury prevention"
            ],
            "certifications": [
                "UKSCA Foundation",
                "UKSCA Accreditation",
                "NSCA-CSCS"
            ],
            "career_progression": [
                {"level": "Entry", "title": "S&C Intern", "years": "0-1"},
                {"level": "Mid", "title": "Assistant S&C Coach", "years": "1-3"},
                {"level": "Senior", "title": "S&C Coach", "years": "3-7"},
                {"level": "Lead", "title": "Head of S&C", "years": "7+"}
            ]
        },
        # 5. Physiotherapy
        {
            "slug": "physiotherapy",
            "title": "Sports Physiotherapy",
            "description": "Prevent, diagnose, and treat sports injuries to help athletes recover and perform at their best",
            "icon": "❤️",
            "color": "#EF4444",
            "work_environment": "Treatment rooms, training grounds, and match venues. Can involve unsocial hours and travel",
            "job_outlook": "Stable demand with growing awareness of injury prevention and rehabilitation importance",
            "salary_range_min": 30000,
            "salary_range_max": 75000,
            "salary_currency": "GBP",
            "requirements": {
                "education": ["BSc Physiotherapy (HCPC registered)"],
                "skills": ["Assessment", "Treatment planning", "Manual therapy", "Rehabilitation", "Communication"],
                "certifications": ["HCPC Registration", "ACPSM Membership"],
                "experience": "Clinical placements and sports-specific experience"
            },
            "education_requirements": [
                "BSc (Hons) Physiotherapy - UoGM",
                "MSc Physiotherapy (Pre-registration) - UoGM",
                "MSc Sports Rehabilitation",
                "BSc (Hons) Sport Rehabilitation - UoGM"
            ],
            "key_skills": [
                "Assessment",
                "Treatment planning",
                "Manual therapy",
                "Rehabilitation",
                "Communication"
            ],
            "certifications": [
                "HCPC Registration",
                "ACPSM Membership",
                "Sports Physiotherapy MSc"
            ],
            "career_progression": [
                {"level": "Entry", "title": "Junior Physiotherapist", "years": "0-2"},
                {"level": "Mid", "title": "Sports Physiotherapist", "years": "2-5"},
                {"level": "Senior", "title": "Senior Physiotherapist", "years": "5-10"},
                {"level": "Lead", "title": "Head of Medical Services", "years": "10+"}
            ]
        },
        # 6. Analytics
        {
            "slug": "analytics",
            "title": "Sports Analytics / Performance Analysis",
            "description": "Use data and video analysis to gain competitive advantages and inform tactical decisions",
            "icon": "📊",
            "color": "#06B6D4",
            "work_environment": "Office settings, video rooms, and some matchday attendance. Generally regular hours",
            "job_outlook": "Rapidly growing field with increasing investment in data-driven decision making across all sports",
            "salary_range_min": 26000,
            "salary_range_max": 80000,
            "salary_currency": "GBP",
            "requirements": {
                "education": ["Performance Analysis courses", "Data Science programs", "Sports Science degree"],
                "skills": ["Video analysis", "Data visualization", "Statistical modeling", "Communication", "Technical proficiency"],
                "certifications": ["Performance Analysis certification", "Software-specific qualifications"],
                "experience": "Practical analysis experience required"
            },
            "education_requirements": [
                "BSc Sports Science with Performance Analysis",
                "BSc Data Science",
                "MSc Performance Analysis"
            ],
            "key_skills": [
                "Video analysis",
                "Data visualization",
                "Statistical modeling",
                "Communication",
                "Technical proficiency"
            ],
            "certifications": [
                "ISPAS Accreditation",
                "Hudl Sportscode Certification",
                "Data Analysis Certificates"
            ],
            "career_progression": [
                {"level": "Entry", "title": "Analysis Intern", "years": "0-1"},
                {"level": "Mid", "title": "Performance Analyst", "years": "1-4"},
                {"level": "Senior", "title": "Lead Analyst", "years": "4-8"},
                {"level": "Lead", "title": "Head of Analytics", "years": "8+"}
            ]
        },
        # 7. Media/Journalism
        {
            "slug": "media",
            "title": "Sports Media / Journalism",
            "description": "Cover sports as a journalist, broadcaster, or content creator, sharing stories with audiences worldwide",
            "icon": "🎙️",
            "color": "#EC4899",
            "work_environment": "Newsrooms, studios, and stadiums. Irregular hours including evenings and weekends",
            "job_outlook": "Evolving industry with growth in digital and social media creating new opportunities",
            "salary_range_min": 20000,
            "salary_range_max": 100000,
            "salary_currency": "GBP",
            "requirements": {
                "education": ["Sports Journalism degree", "Media studies", "Broadcasting courses"],
                "skills": ["Writing", "Presenting", "Video production", "Social media", "Interviewing"],
                "certifications": ["NCTJ Diploma", "Broadcasting qualifications"],
                "experience": "Portfolio of published work"
            },
            "education_requirements": [
                "BA Journalism",
                "BA Sports Journalism",
                "BA Media Studies",
                "NCTJ Diploma"
            ],
            "key_skills": [
                "Writing",
                "Presenting",
                "Video production",
                "Social media",
                "Interviewing"
            ],
            "certifications": [
                "NCTJ Diploma in Journalism",
                "Broadcasting qualifications"
            ],
            "career_progression": [
                {"level": "Entry", "title": "Junior Reporter", "years": "0-2"},
                {"level": "Mid", "title": "Sports Journalist", "years": "2-5"},
                {"level": "Senior", "title": "Senior Writer/Presenter", "years": "5-10"},
                {"level": "Lead", "title": "Editor/Lead Presenter", "years": "10+"}
            ]
        },
        # 8. Officiating
        {
            "slug": "officiating",
            "title": "Officiating / Refereeing",
            "description": "Ensure fair play as a qualified match official, making critical decisions under pressure",
            "icon": "🚩",
            "color": "#FBBF24",
            "work_environment": "Primarily matchday work at various venues. Part-time at lower levels, full-time at elite level",
            "job_outlook": "Steady demand with opportunities at all levels. Professional refereeing is highly competitive",
            "salary_range_min": 15000,
            "salary_range_max": 70000,
            "salary_currency": "GBP",
            "requirements": {
                "education": ["Referee courses", "Laws of the game training"],
                "skills": ["Decision making", "Communication", "Fitness", "Game management", "Composure"],
                "certifications": ["FA Referee certification", "FIFA Badge (elite level)"],
                "experience": "Match officiating experience"
            },
            "education_requirements": [
                "FA Referee Course (Level 7)",
                "Laws of the Game certification"
            ],
            "key_skills": [
                "Decision making",
                "Communication",
                "Fitness",
                "Game management",
                "Composure"
            ],
            "certifications": [
                "FA Referee Course",
                "Level progression certifications",
                "FIFA Badge"
            ],
            "career_progression": [
                {"level": "Entry", "title": "Grassroots Referee", "years": "0-2"},
                {"level": "Mid", "title": "County Level", "years": "2-4"},
                {"level": "Senior", "title": "National List", "years": "4-8"},
                {"level": "Elite", "title": "FIFA Badge Holder", "years": "8+"}
            ]
        },
        # 9. Sports Management
        {
            "slug": "sports-management",
            "title": "Sports Management",
            "description": "Lead and manage sports organizations, events, and business operations",
            "icon": "💼",
            "color": "#2196F3",
            "work_environment": "Office / management",
            "job_outlook": "Stable with opportunities in growing sports sector",
            "salary_range_min": 28000,
            "salary_range_max": 80000,
            "salary_currency": "GBP",
            "requirements": {
                "education": ["Business/Sports Management degree"],
                "skills": ["Leadership", "Business acumen", "Project management", "Communication"],
                "certifications": ["Event Management", "Sports Administration"],
                "experience": "2-3 years in sports industry"
            },
            "education_requirements": [
                "Business degree (e.g., BSc Business Management at RCL)",
                "BA/BSc Sports Management",
                "MBA Sports Business",
                "MSc International Management - RCL",
                "BSc (Hons) Business Management - UoGM"
            ],
            "key_skills": [
                "Leadership",
                "Business acumen",
                "Project management",
                "Communication",
                "Strategic planning"
            ],
            "certifications": [
                "Event Management Certificate",
                "Sports Administration Diploma",
                "CIMSPA Professional Registration"
            ],
            "career_progression": [
                {"level": "Entry", "title": "Sports Administrator", "years": "0-3"},
                {"level": "Mid", "title": "Sports Manager", "years": "3-6"},
                {"level": "Senior", "title": "Operations Director", "years": "6-10"},
                {"level": "Lead", "title": "Managing Director", "years": "10+"}
            ]
        },
        # 10. Community Sports / Recreational Fitness
        {
            "slug": "community",
            "title": "Community Sports",
            "description": "Promote health and fitness in community and commercial settings",
            "icon": "🏋️",
            "color": "#F44336",
            "work_environment": "Gyms, leisure centres, and outdoor spaces. Flexible hours including early mornings and evenings",
            "job_outlook": "Strong growth in wellness sector with increasing health consciousness",
            "salary_range_min": 18000,
            "salary_range_max": 45000,
            "salary_currency": "GBP",
            "requirements": {
                "education": ["Fitness qualifications", "Sports Studies"],
                "skills": ["Motivation", "Communication", "Knowledge of exercise science"],
                "certifications": ["Level 2/3 Fitness Instructor", "Personal Training"],
                "experience": "6-12 months training"
            },
            "education_requirements": [
                "Level 2 Fitness Instructor Qualification",
                "Level 3 Personal Training",
                "Group Exercise Certifications"
            ],
            "key_skills": [
                "Motivation",
                "Communication",
                "Exercise science",
                "Customer service",
                "Program design"
            ],
            "certifications": [
                "Level 2 Fitness Instructor",
                "Level 3 Personal Training",
                "CIMSPA Registration"
            ],
            "career_progression": [
                {"level": "Entry", "title": "Gym Instructor", "years": "0-1"},
                {"level": "Mid", "title": "Personal Trainer", "years": "1-3"},
                {"level": "Senior", "title": "Senior PT/Studio Manager", "years": "3-7"},
                {"level": "Lead", "title": "Fitness Manager", "years": "7+"}
            ]
        }
    ]
    
    created_pathways = []
    
    for pathway_data in pathways_data:
        # Check if pathway already exists
        existing = pathway_crud.get_by_slug(db, slug=pathway_data["slug"])
        
        if not existing:
            # Create pathway
            from app.models.db_schemas import PathwayCreate
            pathway_create = PathwayCreate(**pathway_data)
            pathway = pathway_crud.create(db, obj_in=pathway_create)
            created_pathways.append(pathway)
            logger.info(f"✅ Created pathway: {pathway.title}")
        else:
            logger.info(f"⏭️  Pathway already exists: {existing.title}")
            created_pathways.append(existing)
    
    return created_pathways


def init_database_data(db: Session) -> None:
    """
    Initialize database with seed data
    
    Args:
        db: Database session
    """
    logger.info("Seeding database with initial data...")
    
    # Seed career pathways
    pathways = seed_career_pathways(db)
    logger.info(f"✅ Seeded {len(pathways)} career pathways")
    
    logger.info("✅ Database seeding completed")
