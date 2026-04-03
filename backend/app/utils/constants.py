"""
University and Programme Constants
Based on Regent College London (RCL) and University of Greater Manchester (UoGM) offerings
"""

# University options
UK_UNIVERSITIES = [
    "Regent College London (RCL)",
    "University of Greater Manchester (UoGM)",
    "Other University"
]

# Regent College London Contact Information
RCL_CONTACT = {
    "name": "Regent College London",
    "address": "Carmine Court, 202 Imperial Drive, Harrow, HA2 7HG, London",
    "phone": "+44 (0) 203 870 6666",
    "email": "info@rcl.ac.uk",
    "website": "https://www.rcl.ac.uk",
    "campus_locations": "5 locations across London"
}

# University of Greater Manchester Contact Information
UOGM_CONTACT = {
    "name": "University of Greater Manchester",
    "address": "Deane Road, Bolton, BL3 5AB",
    "phone": "+44 (0)1204 900 600",
    "email": "enquiries@greatermanchester.ac.uk",
    "website": "https://www.greatermanchester.ac.uk",
    "campus_locations": "Bolton campus with multiple partner locations"
}

# RCL Schools
RCL_SCHOOLS = [
    "School of Business",
    "School of Engineering and Computing",
    "School of Health and Sports Science",
    "School of Law"
]

# Sports-related programmes at RCL and UoGM
SPORTS_PROGRAMMES = [
    # RCL - Health and Sports Science
    "BSc (Hons) Sport and Exercise Science (RCL)",
    "BSc (Hons) Sport and Exercise Science with Foundation Year (RCL)",
    "BSc (Hons) Sport and Exercise Nutrition (RCL)",
    "BSc (Hons) Sport and Exercise Nutrition with Foundation Year (RCL)",
    "BSc (Hons) Health and Social Care (RCL)",
    "BSc (Hons) Health and Social Care with Foundation Year (RCL)",
    "BSc (Hons) Health and Social Care Top-up (RCL)",
    "BSc (Hons) Psychology (RCL)",
    "BSc (Hons) Psychology with Foundation Year (RCL)",
    "BSc (Hons) Health and Social Science with Foundation Year (RCL)",
    "MSc Psychology (RCL)",
    "MSc Social Care, Health and Wellbeing (RCL)",
    
    # UoGM - Sport and Exercise programmes
    "BSc (Hons) Psychology with Applications in Sport and Exercise (UoGM)",
    "BSc (Hons) Psychology with Applications in Sport and Exercise with Foundation Year (UoGM)",
    "BSc (Hons) Sport Rehabilitation (UoGM)",
    "BSc (Hons) Sport Rehabilitation with Foundation Year (UoGM)",
    "MSc Applied Sport and Exercise Psychology (UoGM)",
    "MSc Sports Medicine (UoGM)",
    "MSc Strength and Conditioning (UoGM)",
    "MSc Physiotherapy (Pre-registration) (UoGM)",
    "BSc (Hons) Physiotherapy (UoGM)",
    
    # RCL - Business programmes (relevant for sports management/marketing)
    "BSc (Hons) Business Management (RCL)",
    "BSc (Hons) Business Management with Foundation Year (RCL)",
    "BSc (Hons) Business Management Top-up (RCL)",
    "BA (Hons) Business Management with Foundation Year (RCL)",
    "BA (Hons) Marketing with Foundation Year (RCL)",
    "Pearson BTEC Level 4 HNC in Business (RCL)",
    "MBA (Master of Business Administration) (RCL)",
    "MSc International Management (RCL)",
    
    # UoGM - Business programmes
    "BSc (Hons) Business Management (UoGM)",
    "BSc (Hons) Business Management with Foundation Year (UoGM)",
    "MBA (Master of Business Administration) (UoGM)",
    "MBA International (Graduate Entry) (UoGM)",
    "MSc International Management (UoGM)",
    
    # Other programmes  
    "BEng (Hons) Software Engineering (RCL)",
    "BSc (Hons) Computer Science (UoGM)",
    "Other Programme"
]

# Year of study options
YEAR_OF_STUDY_OPTIONS = {
    0: "Foundation Year",
    1: "Year 1",
    2: "Year 2",
    3: "Year 3",
    4: "Year 4",
    5: "Postgraduate",
    6: "Professional / Working"
}

# Map career pathways to relevant RCL and UoGM programmes
PATHWAY_TO_PROGRAMMES = {
    "player": [
        "BSc (Hons) Sport and Exercise Science (RCL)",
        "BSc (Hons) Sport and Exercise Nutrition (RCL)",
        "BSc (Hons) Psychology (RCL)",
        "BSc (Hons) Psychology with Applications in Sport and Exercise (UoGM)",
        "BSc (Hons) Sport Rehabilitation (UoGM)"
    ],
    "coaching": [
        "BSc (Hons) Sport and Exercise Science (RCL)",
        "BSc (Hons) Psychology (RCL)",
        "BSc (Hons) Health and Social Care (RCL)",
        "BSc (Hons) Psychology with Applications in Sport and Exercise (UoGM)",
        "MSc Applied Sport and Exercise Psychology (UoGM)"
    ],
    "sports-medicine": [
        "BSc (Hons) Sport and Exercise Nutrition (RCL)",
        "BSc (Hons) Health and Social Care (RCL)",
        "MSc Social Care, Health and Wellbeing (RCL)",
        "BSc (Hons) Sport Rehabilitation (UoGM)",
        "MSc Sports Medicine (UoGM)",
        "MSc Physiotherapy (Pre-registration) (UoGM)",
        "BSc (Hons) Physiotherapy (UoGM)"
    ],
    "performance-analyst": [
        "BSc (Hons) Sport and Exercise Science (RCL)",
        "BEng (Hons) Software Engineering (RCL)",
        "BSc (Hons) Business Management (RCL)",
        "BSc (Hons) Psychology with Applications in Sport and Exercise (UoGM)",
        "MSc Applied Sport and Exercise Psychology (UoGM)"
    ],
    "sports-management": [
        "BSc (Hons) Business Management (RCL)",
        "MBA (Master of Business Administration) (RCL)",
        "MSc International Management (RCL)",
        "BSc (Hons) Business Management (UoGM)",
        "MBA (Master of Business Administration) (UoGM)",
        "MSc International Management (UoGM)"
    ],
    "journalism": [
        "BA (Hons) Marketing with Foundation Year (RCL)",
        "BSc (Hons) Business Management (RCL)",
        "BA (Hons) Business Management with Foundation Year (RCL)",
        "BSc (Hons) Business Management (UoGM)"
    ]
}
