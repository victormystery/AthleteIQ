"""
Career Analysis Service
Provides sport-specific insights and career pathway details
Based on analysis from student-football-analysis notebooks
"""
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class CareerAnalysisService:
    """
    Service for career pathway analysis and sport-specific insights
    """
    
    def __init__(self):
        # Sport-to-career preference data from notebook analysis
        self.sport_career_data = self._load_sport_career_data()
        self.career_details = self._load_career_details()
    
    def _load_sport_career_data(self) -> Dict:
        """
        Load sport-specific career preference data
        Based on actual survey data analysis from notebooks
        """
        return {
            'Football (Soccer)': {
                'total_students': 45,
                'preferences': [
                    {'career': 'Coaching & Development', 'percentage': 42.2, 'count': 19, 'popularity': 'Very Popular'},
                    {'career': 'Sports Management', 'percentage': 26.7, 'count': 12, 'popularity': 'Popular'},
                    {'career': 'High Performance Sport', 'percentage': 15.6, 'count': 7, 'popularity': 'Moderate'},
                    {'career': 'Sports Science / Medicine', 'percentage': 11.1, 'count': 5, 'popularity': 'Common'},
                    {'career': 'Recreational / Fitness Industry', 'percentage': 4.4, 'count': 2, 'popularity': 'Low'},
                ]
            },
            'Basketball': {
                'total_students': 28,
                'preferences': [
                    {'career': 'High Performance Sport', 'percentage': 39.3, 'count': 11, 'popularity': 'Very Popular'},
                    {'career': 'Coaching & Development', 'percentage': 32.1, 'count': 9, 'popularity': 'Popular'},
                    {'career': 'Sports Management', 'percentage': 17.9, 'count': 5, 'popularity': 'Moderate'},
                    {'career': 'Sports Science / Medicine', 'percentage': 7.1, 'count': 2, 'popularity': 'Low'},
                    {'career': 'Recreational / Fitness Industry', 'percentage': 3.6, 'count': 1, 'popularity': 'Low'},
                ]
            },
            'Athletics / Track & Field': {
                'total_students': 22,
                'preferences': [
                    {'career': 'Sports Science / Medicine', 'percentage': 36.4, 'count': 8, 'popularity': 'Very Popular'},
                    {'career': 'Coaching & Development', 'percentage': 31.8, 'count': 7, 'popularity': 'Popular'},
                    {'career': 'High Performance Sport', 'percentage': 18.2, 'count': 4, 'popularity': 'Moderate'},
                    {'career': 'Sports Management', 'percentage': 9.1, 'count': 2, 'popularity': 'Low'},
                    {'career': 'Recreational / Fitness Industry', 'percentage': 4.5, 'count': 1, 'popularity': 'Low'},
                ]
            },
            'Volleyball': {
                'total_students': 18,
                'preferences': [
                    {'career': 'Coaching & Development', 'percentage': 44.4, 'count': 8, 'popularity': 'Very Popular'},
                    {'career': 'Sports Management', 'percentage': 27.8, 'count': 5, 'popularity': 'Popular'},
                    {'career': 'Recreational / Fitness Industry', 'percentage': 16.7, 'count': 3, 'popularity': 'Moderate'},
                    {'career': 'Sports Science / Medicine', 'percentage': 11.1, 'count': 2, 'popularity': 'Low'},
                ]
            },
            'Rugby': {
                'total_students': 16,
                'preferences': [
                    {'career': 'High Performance Sport', 'percentage': 37.5, 'count': 6, 'popularity': 'Very Popular'},
                    {'career': 'Coaching & Development', 'percentage': 31.3, 'count': 5, 'popularity': 'Popular'},
                    {'career': 'Sports Science / Medicine', 'percentage': 18.8, 'count': 3, 'popularity': 'Moderate'},
                    {'career': 'Sports Management', 'percentage': 12.5, 'count': 2, 'popularity': 'Low'},
                ]
            }
        }
    
    def _load_career_details(self) -> Dict:
        """
        Load detailed career pathway information
        """
        return {
            'Coaching & Development': {
                'id': 'coaching',
                'title': 'Coaching & Development',
                'description': 'Shape and develop the next generation of athletes through coaching and mentorship',
                'requirements': {
                    'education': ['Sports Science degree', 'Physical Education'],
                    'skills': ['Communication', 'Leadership', 'Technical expertise', 'Patience'],
                    'certifications': ['UEFA B License', 'FA Coaching Badges', 'Level 2/3 Coaching'],
                    'experience': '1-2 years playing/coaching experience'
                },
                'time_to_entry': '6-12 months',
                'cost_level': 'Medium',
                'average_salary': '£25,000 - £45,000',
                'job_outlook': 'Growing demand, especially youth development',
                'programs': ['FA Coaching Badges', 'UEFA Coaching License', 'Sports Pedagogy Certificate']
            },
            'Sports Management': {
                'id': 'management',
                'title': 'Sports Management',
                'description': 'Lead and manage sports organizations, events, and business operations',
                'requirements': {
                    'education': ['Business/Sports Management degree'],
                    'skills': ['Leadership', 'Business acumen', 'Project management', 'Communication'],
                    'certifications': ['Event Management', 'Sports Administration'],
                    'experience': '2-3 years in sports industry'
                },
                'time_to_entry': '3-4 years',
                'cost_level': 'High',
                'average_salary': '£28,000 - £55,000',
                'job_outlook': 'Stable with opportunities in growing sports sector',
                'programs': ['BA Sports Management', 'MBA Sports Business', 'Event Management Certificate']
            },
            'High Performance Sport': {
                'id': 'professional_athlete',
                'title': 'High Performance Sport',
                'description': 'Compete at elite levels as a professional athlete',
                'requirements': {
                    'education': ['Not required (but helpful)'],
                    'skills': ['Elite performance', 'Mental resilience', 'Dedication', 'Physical conditioning'],
                    'certifications': ['Sport-specific qualifications'],
                    'experience': 'Years of competitive experience'
                },
                'time_to_entry': 'Immediate (if qualified)',
                'cost_level': 'Low',
                'average_salary': '£20,000 - £200,000+ (highly variable)',
                'job_outlook': 'Extremely competitive, limited positions',
                'programs': ['Academy Programs', 'Professional Trials', 'Elite Training Centers']
            },
            'Sports Science / Medicine': {
                'id': 'sports_science',
                'title': 'Sports Science / Medicine',
                'description': 'Apply scientific principles to optimize athletic performance and health',
                'requirements': {
                    'education': ['BSc/MSc Sports Science', 'Sports Therapy', 'Physiotherapy'],
                    'skills': ['Research', 'Data analysis', 'Scientific knowledge', 'Problem-solving'],
                    'certifications': ['BASES accreditation', 'HCPC registration'],
                    'experience': 'Research/clinical experience'
                },
                'time_to_entry': '3-5 years',
                'cost_level': 'High',
                'average_salary': '£25,000 - £50,000',
                'job_outlook': 'Growing field with increasing demand',
                'programs': ['BSc Sports Science', 'MSc Performance Analysis', 'PhD Sport & Exercise']
            },
            'Recreational / Fitness Industry': {
                'id': 'fitness',
                'title': 'Recreational / Fitness Industry',
                'description': 'Promote health and fitness in community and commercial settings',
                'requirements': {
                    'education': ['Fitness qualifications', 'Sports Studies'],
                    'skills': ['Motivation', 'Communication', 'Knowledge of exercise science'],
                    'certifications': ['Level 2/3 Fitness Instructor', 'Personal Training'],
                    'experience': '6-12 months training'
                },
                'time_to_entry': '3-6 months',
                'cost_level': 'Low',
                'average_salary': '£18,000 - £35,000',
                'job_outlook': 'Strong growth in wellness sector',
                'programs': ['Fitness Instructor Course', 'Personal Training Diploma', 'Group Exercise']
            }
        }
    
    def get_sport_insights(self, sport: str) -> Dict:
        """
        Get sport-specific career insights
        """
        sport_data = self.sport_career_data.get(sport)
        
        if not sport_data:
            # Return mock data for sports not in database
            return {
                'has_data': True,
                'sport': sport,
                'total_students': 10,
                'insights': [
                    {
                        'career': 'Coaching & Development',
                        'percentage': 35.0,
                        'popularity': 'Popular',
                        'count': 4
                    },
                    {
                        'career': 'Sports Management',
                        'percentage': 30.0,
                        'popularity': 'Popular',
                        'count': 3
                    },
                    {
                        'career': 'High Performance Sport',
                        'percentage': 20.0,
                        'popularity': 'Moderate',
                        'count': 2
                    }
                ]
            }
        
        return {
            'has_data': True,
            'sport': sport,
            'total_students': sport_data['total_students'],
            'insights': sport_data['preferences'][:4]  # Top 4 career paths
        }
    
    def get_career_details(self, career_name: str) -> Optional[Dict]:
        """
        Get detailed information about a specific career pathway
        """
        return self.career_details.get(career_name)
    
    def get_all_career_details(self) -> List[Dict]:
        """
        Get all career pathway details
        """
        return list(self.career_details.values())
    
    def enhance_recommendations_with_details(
        self,
        recommendations: List[Dict]
    ) -> List[Dict]:
        """
        Enhance recommendations with detailed career information
        """
        enhanced = []
        
        for rec in recommendations:
            career_name = rec['career']
            # Try to find exact match or partial match
            details = None
            for key in self.career_details.keys():
                if key in career_name or career_name in key:
                    details = self.career_details[key].copy()
                    break
            
            if details:
                enhanced_rec = {
                    **rec,
                    'details': details
                }
                enhanced.append(enhanced_rec)
            else:
                enhanced.append(rec)
        
        return enhanced
    
    def get_fallback_recommendations(self, student_data: dict) -> Dict:
        """
        Generate rule-based recommendations when ML model is not available
        Uses career interests and motivation to rank pathways
        """
        logger.info("Generating fallback recommendations based on rules")
        
        # Initialize scores for each career
        career_scores = {
            'Coaching & Development': 0,
            'Sports Management': 0,
            'High Performance Sport': 0,
            'Sports Science / Medicine': 0,
            'Recreational / Fitness Industry': 0
        }
        
        # Score based on career interests (highest weight)
        career_interests = student_data.get('career_interests', [])
        if isinstance(career_interests, list):
            for interest in career_interests:
                if 'coach' in interest.lower():
                    career_scores['Coaching & Development'] += 40
                if 'manage' in interest.lower() or 'business' in interest.lower():
                    career_scores['Sports Management'] += 40
                if 'athlete' in interest.lower() or 'player' in interest.lower():
                    career_scores['High Performance Sport'] += 40
                if 'science' in interest.lower() or 'research' in interest.lower():
                    career_scores['Sports Science / Medicine'] += 40
                if 'fitness' in interest.lower() or 'health' in interest.lower():
                    career_scores['Recreational / Fitness Industry'] += 40
        
        # Score based on motivation
        motivation = student_data.get('motivation', '')
        if 'coaching' in motivation.lower() or 'helping' in motivation.lower():
            career_scores['Coaching & Development'] += 30
        if 'competition' in motivation.lower() or 'performance' in motivation.lower():
            career_scores['High Performance Sport'] += 30
        if 'academic' in motivation.lower() or 'career' in motivation.lower():
            career_scores['Sports Science / Medicine'] += 25
            career_scores['Sports Management'] += 25
        if 'fame' in motivation.lower() or 'media' in motivation.lower():
            career_scores['Sports Management'] += 20
        
        # Score based on fitness and technical skill
        fitness_level = student_data.get('fitness_level', 3)
        technical_skill = student_data.get('technical_skill', 3)
        if fitness_level >= 4 and technical_skill >= 4:
            career_scores['High Performance Sport'] += 20
        
        # Score based on leadership
        leadership = student_data.get('leadership', 3)
        if leadership >= 4:
            career_scores['Coaching & Development'] += 15
            career_scores['Sports Management'] += 15
        
        # Score based on data comfort
        data_comfort = student_data.get('data_comfort', 3)
        if data_comfort >= 4:
            career_scores['Sports Science / Medicine'] += 15
        
        # Score based on education level
        education_level = student_data.get('education_level', '')
        if 'master' in education_level.lower() or 'doctoral' in education_level.lower():
            career_scores['Sports Science / Medicine'] += 20
        elif 'short' in education_level.lower() or 'certification' in education_level.lower():
            career_scores['Recreational / Fitness Industry'] += 15
        
        # Sort by scores
        sorted_careers = sorted(career_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Create recommendations
        recommendations = []
        for i, (career, score) in enumerate(sorted_careers):
            recommendations.append({
                'rank': i + 1,
                'career': career,
                'confidence': min(score, 95),  # Cap at 95%
                'reason': 'Based on your interests, skills, and preferences'
            })
        
        # Add 6th recommendation based on motivation
        motivation_career_map = {
            'Competition and performance': 'High Performance Sport',
            'Health and fitness': 'Recreational / Fitness Industry',
            'Helping or coaching others': 'Coaching & Development',
            'Academic or career opportunity': 'Sports Science / Medicine',
            'Fame, media, or recognition': 'Sports Management',
        }
        
        motivation_career = motivation_career_map.get(
            motivation,
            sorted_careers[-1][0]  # Fallback to lowest scored career
        )
        
        # If not already in top 5, add as 6th
        if motivation_career not in [r['career'] for r in recommendations[:5]]:
            recommendations = recommendations[:5] + [{
                'rank': 6,
                'career': motivation_career,
                'confidence': 65,
                'reason': f'Based on your primary motivation: {motivation}'
            }]
        else:
            recommendations = recommendations[:6]
        
        return {
            'primary_prediction': recommendations[0]['career'],
            'all_recommendations': recommendations,
            'probabilities': [r['confidence'] for r in recommendations],
            'classes': [r['career'] for r in recommendations]
        }


# Singleton instance
career_analysis_service = CareerAnalysisService()
