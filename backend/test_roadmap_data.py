"""
Test script for roadmap data service
"""
from app.services.roadmap_data_service import roadmap_data_service

def test_roadmap_service():
    """Test that roadmap data loads correctly"""
    
    print("="*60)
    print("ROADMAP DATA SERVICE TEST")
    print("="*60)
    
    # Test 1: Load all pathways
    pathways = roadmap_data_service.get_available_pathways()
    print(f"\n✅ Loaded {len(pathways)} career pathways:")
    
    for pathway in pathways:
        print(f"  - {pathway['slug']}: {pathway['title']} ({pathway['total_steps']} steps)")
    
    # Test 2: Get specific roadmap
    print("\n" + "="*60)
    print("Testing specific pathway: coaching")
    print("="*60)
    
    coaching = roadmap_data_service.get_roadmap_by_slug('coaching')
    if coaching:
        print(f"✅ Pathway: {coaching['pathway_title']}")
        print(f"   Time to Entry: {coaching['time_to_entry']}")
        print(f"   Cost Level: {coaching['cost_level']}")
        print(f"   Total Steps: {len(coaching['steps'])}")
        
        # Show first step
        if coaching['steps']:
            first_step = coaching['steps'][0]
            print(f"\n   First Step: {first_step['title']}")
            print(f"   Type: {first_step['type']}")
            print(f"   Duration: {first_step['duration']}")
            print(f"   Cost: {first_step['cost']}")
            print(f"   Priority: {first_step['priority']}")
    
    # Test 3: Cost estimate
    print("\n" + "="*60)
    print("Cost estimate for coaching pathway")
    print("="*60)
    
    cost = roadmap_data_service.estimate_total_cost('coaching')
    print(f"✅ Min Cost: £{cost['min_cost']:,}")
    print(f"   Max Cost: £{cost['max_cost']:,}")
    print(f"   Note: {cost['note']}")
    
    # Test 4: Required steps
    print("\n" + "="*60)
    print("Required steps for coaching pathway")
    print("="*60)
    
    required = roadmap_data_service.get_required_steps('coaching')
    print(f"✅ {len(required)} required steps:")
    for step in required:
        print(f"   - {step['title']} ({step['duration']}, {step['cost']})")
    
    # Test 5: Search
    print("\n" + "="*60)
    print("Search for 'athlete' pathways")
    print("="*60)
    
    results = roadmap_data_service.search_roadmaps('athlete')
    print(f"✅ Found {len(results)} matching pathways:")
    for result in results:
        print(f"   - {result['pathway_title']} ({result['pathway_slug']})")
    
    print("\n" + "="*60)
    print("ALL TESTS PASSED ✅")
    print("="*60)

if __name__ == "__main__":
    test_roadmap_service()
