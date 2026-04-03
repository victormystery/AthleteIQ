"""
Comprehensive Roadmap Data Service
Loads and manages career pathway roadmap data from JSON
"""
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)


class RoadmapDataService:
    """
    Service for loading and accessing comprehensive career roadmap data.
    Provides structured roadmap steps for all career pathways.
    """
    
    def __init__(self):
        self.roadmaps_data: Dict[str, Any] = {}
        self._load_roadmaps()
    
    def _load_roadmaps(self) -> None:
        """Load roadmap data from JSON file"""
        try:
            data_file = Path(__file__).parent.parent / "data" / "comprehensive_roadmaps.json"
            
            if not data_file.exists():
                logger.warning(f"Roadmap data file not found: {data_file}")
                return
            
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.roadmaps_data = data.get('roadmaps', {})
            
            logger.info(f"✅ Loaded {len(self.roadmaps_data)} career roadmaps from JSON")
        
        except Exception as e:
            logger.error(f"❌ Error loading roadmap data: {str(e)}")
            self.roadmaps_data = {}
    
    def get_roadmap_by_slug(self, pathway_slug: str) -> Optional[Dict[str, Any]]:
        """
        Get roadmap data for a specific pathway slug
        
        Args:
            pathway_slug: Unique pathway identifier (e.g., 'professional-athlete')
        
        Returns:
            Roadmap dictionary with steps, or None if not found
        """
        return self.roadmaps_data.get(pathway_slug)
    
    def get_all_roadmaps(self) -> Dict[str, Any]:
        """
        Get all available roadmap data
        
        Returns:
            Dictionary of all roadmaps keyed by pathway slug
        """
        return self.roadmaps_data
    
    def get_roadmap_steps(self, pathway_slug: str) -> List[Dict[str, Any]]:
        """
        Get just the steps for a specific pathway
        
        Args:
            pathway_slug: Unique pathway identifier
        
        Returns:
            List of roadmap step dictionaries
        """
        roadmap = self.get_roadmap_by_slug(pathway_slug)
        if roadmap:
            return roadmap.get('steps', [])
        return []
    
    def get_roadmap_metadata(self, pathway_slug: str) -> Dict[str, Any]:
        """
        Get metadata for a roadmap (title, time to entry, cost, etc.)
        
        Args:
            pathway_slug: Unique pathway identifier
        
        Returns:
            Dictionary with metadata fields
        """
        roadmap = self.get_roadmap_by_slug(pathway_slug)
        if roadmap:
            return {
                'pathway_slug': roadmap.get('pathway_slug'),
                'pathway_title': roadmap.get('pathway_title'),
                'time_to_entry': roadmap.get('time_to_entry'),
                'cost_level': roadmap.get('cost_level'),
                'total_steps': len(roadmap.get('steps', []))
            }
        return {}
    
    def get_required_steps(self, pathway_slug: str) -> List[Dict[str, Any]]:
        """
        Get only the required steps for a pathway
        
        Args:
            pathway_slug: Unique pathway identifier
        
        Returns:
            List of required step dictionaries
        """
        steps = self.get_roadmap_steps(pathway_slug)
        return [step for step in steps if step.get('priority') == 'required']
    
    def get_recommended_steps(self, pathway_slug: str) -> List[Dict[str, Any]]:
        """
        Get recommended (but not required) steps for a pathway
        
        Args:
            pathway_slug: Unique pathway identifier
        
        Returns:
            List of recommended step dictionaries
        """
        steps = self.get_roadmap_steps(pathway_slug)
        return [step for step in steps if step.get('priority') == 'recommended']
    
    def get_steps_by_type(self, pathway_slug: str, step_type: str) -> List[Dict[str, Any]]:
        """
        Filter steps by type (academic, certification, experience, etc.)
        
        Args:
            pathway_slug: Unique pathway identifier
            step_type: Type of step ('academic', 'certification', 'experience', 'course', 'skill', 'networking')
        
        Returns:
            List of matching step dictionaries
        """
        steps = self.get_roadmap_steps(pathway_slug)
        return [step for step in steps if step.get('type') == step_type]
    
    def estimate_total_cost(self, pathway_slug: str) -> Dict[str, Any]:
        """
        Estimate the total cost range for a pathway
        
        Args:
            pathway_slug: Unique pathway identifier
        
        Returns:
            Dictionary with min/max cost estimates
        """
        steps = self.get_roadmap_steps(pathway_slug)
        
        min_cost = 0
        max_cost = 0
        
        for step in steps:
            cost_str = step.get('cost', '')
            
            # Parse cost strings like "£400-£800", "Free", "£9,250/year"
            if cost_str.lower() in ['free', 'free (employment)', 'free (voluntary)']:
                continue
            
            # Extract numeric values
            import re
            numbers = re.findall(r'[\d,]+', cost_str)
            
            if numbers:
                # Clean numbers (remove commas)
                nums = [int(n.replace(',', '')) for n in numbers]
                
                # Check if it's per year and multiply
                multiplier = 3 if '/year' in cost_str else 1
                
                if len(nums) >= 2:
                    min_cost += nums[0] * multiplier
                    max_cost += nums[1] * multiplier
                else:
                    min_cost += nums[0] * multiplier
                    max_cost += nums[0] * multiplier
        
        return {
            'min_cost': min_cost,
            'max_cost': max_cost,
            'currency': 'GBP',
            'note': 'Estimated total for all required and recommended steps'
        }
    
    def estimate_total_duration(self, pathway_slug: str) -> Dict[str, Any]:
        """
        Estimate total duration for completing a pathway
        
        Args:
            pathway_slug: Unique pathway identifier
        
        Returns:
            Dictionary with duration estimates
        """
        steps = self.get_roadmap_steps(pathway_slug)
        
        # This is a simplified calculation - in reality, many steps can overlap
        durations = []
        for step in steps:
            duration_str = step.get('duration', '')
            # For simplicity, just collect the durations
            durations.append(duration_str)
        
        roadmap = self.get_roadmap_by_slug(pathway_slug)
        time_to_entry = roadmap.get('time_to_entry', 'Unknown') if roadmap else 'Unknown'
        
        return {
            'time_to_entry': time_to_entry,
            'total_steps': len(steps),
            'note': 'Many steps can be completed in parallel or overlap in time'
        }
    
    def search_roadmaps(self, query: str) -> List[Dict[str, Any]]:
        """
        Search across all roadmaps for matching pathways
        
        Args:
            query: Search term to match against pathway titles
        
        Returns:
            List of matching roadmap metadata
        """
        results = []
        query_lower = query.lower()
        
        for slug, roadmap in self.roadmaps_data.items():
            title = roadmap.get('pathway_title', '').lower()
            if query_lower in title or query_lower in slug:
                results.append(self.get_roadmap_metadata(slug))
        
        return results
    
    def get_available_pathways(self) -> List[Dict[str, str]]:
        """
        Get list of all available pathways with basic info
        
        Returns:
            List of dictionaries with slug and title
        """
        pathways = []
        for slug, roadmap in self.roadmaps_data.items():
            pathways.append({
                'slug': slug,
                'title': roadmap.get('pathway_title', ''),
                'time_to_entry': roadmap.get('time_to_entry', ''),
                'cost_level': roadmap.get('cost_level', ''),
                'total_steps': len(roadmap.get('steps', []))
            })
        return pathways


# Singleton instance
roadmap_data_service = RoadmapDataService()
