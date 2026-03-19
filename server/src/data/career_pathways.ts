/**
 * Seed data for career pathways.
 * Imported by seed.ts and used at runtime by CareerPathwayService.
 */

export const careerPathwaysSeedData = [
  {
    title: 'Coaching & Development',
    slug: 'coaching-development',
    icon: '🏋️',
    colour: '#F59E0B',
    category: 'Sport Performance',
    description:
      'Guide athletes and teams to reach their full potential. Coaching combines technical expertise, leadership, and psychology to drive performance improvement at all levels — from grassroots to elite sport.',
    workEnvironment: ['Field', 'Gym', 'Training facility', 'Classroom'],
    jobOutlook: 'Growing',
    salaryRange: { min: 35000, max: 120000, currency: 'USD' },
    educationRequirements: [
      "Bachelor's in Sports Science, Kinesiology, or related field",
      'Coaching certification (NCSA, UEFA, FA, etc.)',
      'First Aid / CPR certification'
    ],
    keySkills: [
      'Athlete development',
      'Performance analysis',
      'Motivational communication',
      'Session planning',
      'Injury prevention',
      'Leadership'
    ],
    certifications: [
      'NCSA Strength & Conditioning Specialist (CSCS)',
      'UEFA Coaching Licences (A/B/Pro)',
      'Level 1–4 National Coaching Certifications',
      'UK Coaching Certificate'
    ],
    careerProgressionSteps: [
      {
        level: 'Entry',
        title: 'Assistant Coach / Volunteer',
        yearsExperience: '0–2',
        description: 'Support lead coaches in training sessions, help with admin and athlete welfare.'
      },
      {
        level: 'Mid',
        title: 'Head Coach (Club / School)',
        yearsExperience: '3–6',
        description: 'Lead training programmes, manage athlete development plans, and represent the club.'
      },
      {
        level: 'Senior',
        title: 'Elite / National Team Coach',
        yearsExperience: '7+',
        description: 'Coach at the highest level, oversee performance staff, and drive medal/trophy ambitions.'
      }
    ],
    successStories: [
      {
        name: 'Alex Morgan',
        sport: 'Football',
        career: 'Women\'s Football Coach',
        quote: 'My playing career gave me the foundation — coaching let me multiply that impact across hundreds of athletes.'
      }
    ]
  },
  {
    title: 'Sports Management',
    slug: 'sports-management',
    icon: '📊',
    colour: '#3B82F6',
    category: 'Business & Administration',
    description:
      'Run the business side of sport — from managing clubs and events to marketing, sponsorships, and governance. Sports managers ensure organisations operate efficiently and achieve commercial success.',
    workEnvironment: ['Office', 'Stadium', 'Conference venues', 'Mixed'],
    jobOutlook: 'Growing',
    salaryRange: { min: 42000, max: 150000, currency: 'USD' },
    educationRequirements: [
      "Bachelor's in Sports Management, Business Administration, or related",
      'MBA with Sports Management concentration (advantage)',
      'Project Management certification (PMP, Prince2)'
    ],
    keySkills: [
      'Business strategy',
      'Sponsorship & partnerships',
      'Event management',
      'Financial management',
      'Marketing & PR',
      'Stakeholder relations'
    ],
    certifications: [
      'Certified Sports Manager (CSM)',
      'PMP — Project Management Professional',
      'Google Analytics / Digital Marketing',
      'FIFA / UEFA Administration Diplomas'
    ],
    careerProgressionSteps: [
      {
        level: 'Entry',
        title: 'Sports Administrator / Coordinator',
        yearsExperience: '0–2',
        description: 'Coordinate events, manage schedules, support operations teams.'
      },
      {
        level: 'Mid',
        title: 'Sports Manager / Marketing Manager',
        yearsExperience: '3–6',
        description: 'Oversee departments, manage budgets, drive commercial partnerships.'
      },
      {
        level: 'Senior',
        title: 'General Manager / CEO',
        yearsExperience: '8+',
        description: 'Lead entire organisations, set strategy, interface with boards and governing bodies.'
      }
    ],
    successStories: [
      {
        name: 'LeBron James',
        sport: 'Basketball',
        career: 'Athlete turned Sports Executive & Media Owner',
        quote: 'I always knew the game was bigger than basketball. Understanding the business is as important as winning on the court.'
      }
    ]
  },
  {
    title: 'High Performance Sport',
    slug: 'high-performance-sport',
    icon: '🥇',
    colour: '#EF4444',
    category: 'Sport Performance',
    description:
      'Work at the cutting edge of elite sport — supporting national squads, professional clubs, and Olympic athletes through performance science, analytics, and integrated support teams.',
    workEnvironment: ['Field', 'Lab', 'Training centres', 'Away venues'],
    jobOutlook: 'Stable',
    salaryRange: { min: 45000, max: 130000, currency: 'USD' },
    educationRequirements: [
      "Master's in Sport Science, Strength & Conditioning, or Performance Analysis",
      'Relevant professional accreditations',
      'Experience in elite sport environment'
    ],
    keySkills: [
      'Performance analysis',
      'Periodisation & programming',
      'Data interpretation',
      'Recovery science',
      'Athlete monitoring',
      'Interdisciplinary collaboration'
    ],
    certifications: [
      'CSCS — Certified Strength and Conditioning Specialist',
      'UKSCA Accreditation',
      'ISAK — International Society for Advancement of Kinanthropometry',
      'BASES Accreditation'
    ],
    careerProgressionSteps: [
      {
        level: 'Entry',
        title: 'Performance Analyst / S&C Assistant',
        yearsExperience: '0–3',
        description: 'Collect and analyse data, assist in delivery of training programmes.'
      },
      {
        level: 'Mid',
        title: 'Lead Analyst / S&C Coach',
        yearsExperience: '3–7',
        description: 'Lead athlete monitoring, design periodised programmes, report to head of performance.'
      },
      {
        level: 'Senior',
        title: 'Head of Performance / Performance Director',
        yearsExperience: '8+',
        description: 'Oversee entire performance department, shape organisational culture, interface with national bodies.'
      }
    ],
    successStories: [
      {
        name: 'Bill Knowles',
        sport: 'Ice Hockey (Former Player)',
        career: 'High Performance & Rehab Specialist',
        quote: 'My injury forced me to understand performance science deeply — now I help athletes avoid what I went through.'
      }
    ]
  },
  {
    title: 'Sports Science / Medicine',
    slug: 'sports-science-medicine',
    icon: '🔬',
    colour: '#10B981',
    category: 'Health & Science',
    description:
      'Apply scientific principles to optimise human performance, prevent injury, and accelerate recovery. Sports scientists and medics work across biomechanics, physiology, nutrition, and psychology.',
    workEnvironment: ['Lab', 'Clinic', 'Training facilities', 'Hospital'],
    jobOutlook: 'Growing',
    salaryRange: { min: 40000, max: 160000, currency: 'USD' },
    educationRequirements: [
      "Bachelor's in Sports Science, Exercise Physiology, or Medicine (MBBS)",
      "Master's or PhD for research roles",
      'HCPC Registration (Sports Therapist/Physiotherapist)',
      'GMC Registration (Sports Physician)'
    ],
    keySkills: [
      'Exercise physiology',
      'Biomechanical analysis',
      'Injury assessment & rehabilitation',
      'Research methodology',
      'Data analysis (SPSS, R)',
      'Clinical communication'
    ],
    certifications: [
      'BASES Accreditation',
      'HCPC — Health & Care Professions Council',
      'ACSM Certification',
      'BASRaT — British Association of Sport Rehabilitation & Trainers'
    ],
    careerProgressionSteps: [
      {
        level: 'Entry',
        title: 'Sports Science Graduate / Intern',
        yearsExperience: '0–2',
        description: 'Assist in physiological testing, data collection, and lab operations.'
      },
      {
        level: 'Mid',
        title: 'Sports Scientist / Physiotherapist',
        yearsExperience: '2–6',
        description: 'Lead testing protocols, deliver rehabilitation programmes, consult with coaches.'
      },
      {
        level: 'Senior',
        title: 'Consultant / Research Lead / Team Physician',
        yearsExperience: '7+',
        description: 'Advise at the highest levels, publish research, or serve as team medical director.'
      }
    ],
    successStories: [
      {
        name: 'Megan Anderson',
        sport: 'Athletics (Sprinter)',
        career: 'Sports Physiologist — Olympic Programme',
        quote: 'Every millisecond counts at the top. My science background lets me find the marginal gains others miss.'
      }
    ]
  },
  {
    title: 'Recreational / Fitness Industry',
    slug: 'recreational-fitness-industry',
    icon: '💪',
    colour: '#8B5CF6',
    category: 'Health & Wellness',
    description:
      'Help everyday people improve their health, fitness, and quality of life. This broad sector includes personal training, group fitness, wellness coaching, and community sport development.',
    workEnvironment: ['Gym', 'Community centres', 'Outdoor', 'Online'],
    jobOutlook: 'Growing',
    salaryRange: { min: 28000, max: 90000, currency: 'USD' },
    educationRequirements: [
      'Level 2–4 Fitness Instructor / Personal Trainer Qualification',
      "Bachelor's in Exercise Science or Kinesiology (advantage)",
      'First Aid certification'
    ],
    keySkills: [
      'Exercise prescription',
      'Client motivation',
      'Programme design',
      'Nutrition basics',
      'Business development',
      'Community engagement'
    ],
    certifications: [
      'ACE — American Council on Exercise',
      'NASM — National Academy of Sports Medicine',
      'REPs / CIMSPA Registration',
      'Yoga / Pilates Instructor Certification'
    ],
    careerProgressionSteps: [
      {
        level: 'Entry',
        title: 'Fitness Instructor / PT',
        yearsExperience: '0–2',
        description: 'Deliver group classes and 1-to-1 sessions, build a client base.'
      },
      {
        level: 'Mid',
        title: 'Senior PT / Wellness Coach',
        yearsExperience: '2–5',
        description: 'Specialise in a niche (weight loss, rehabilitation, sport), grow income streams.'
      },
      {
        level: 'Senior',
        title: 'Gym Owner / Fitness Director',
        yearsExperience: '5+',
        description: 'Operate own facility or lead a team across a multi-site gym chain.'
      }
    ],
    successStories: [
      {
        name: 'Joe Wicks',
        sport: 'Football & Athletics',
        career: 'Wellness Coach & Entrepreneur',
        quote: 'I turned my passion for fitness into a global brand — it starts with caring about people\'s health.'
      }
    ]
  },
  {
    title: 'Sports Media & Journalism',
    slug: 'sports-media-journalism',
    icon: '🎙️',
    colour: '#F97316',
    category: 'Media & Communications',
    description:
      'Tell the stories behind sport — through broadcasting, writing, podcasting, and digital content creation. Sports journalists and media professionals bring the emotion and analysis of sport to millions of fans.',
    workEnvironment: ['Media studio', 'Press box', 'Remote/online', 'On location'],
    jobOutlook: 'Evolving',
    salaryRange: { min: 30000, max: 110000, currency: 'USD' },
    educationRequirements: [
      "Bachelor's in Journalism, Media Studies, or Communications",
      'Portfolio of published/broadcast work',
      'Social media & content creation skills'
    ],
    keySkills: [
      'Storytelling & writing',
      'Broadcasting & presenting',
      'Social media management',
      'Video production',
      'Sports knowledge & analysis',
      'Interviewing'
    ],
    certifications: [
      'NCTJ Diploma in Journalism',
      'Google Digital Journalism',
      'Podcast Production Certification',
      'Sports Broadcasting Programmes (Sky, BBC academies)'
    ],
    careerProgressionSteps: [
      {
        level: 'Entry',
        title: 'Junior Reporter / Content Creator',
        yearsExperience: '0–2',
        description: 'Write match reports, run social media, assist senior journalists.'
      },
      {
        level: 'Mid',
        title: 'Sports Journalist / Broadcaster',
        yearsExperience: '2–6',
        description: 'Cover major events, build audience, develop signature style.'
      },
      {
        level: 'Senior',
        title: 'Lead Presenter / Sports Editor',
        yearsExperience: '6+',
        description: 'Lead editorial direction, anchor flagship programmes, represent the brand.'
      }
    ],
    successStories: [
      {
        name: 'Gary Neville',
        sport: 'Football (Professional Player)',
        career: 'Sports Broadcaster & Pundit',
        quote: 'Playing gave me the credibility. Media training gave me the platform. Both together created my second career.'
      }
    ]
  },
  {
    title: 'Sports Analytics',
    slug: 'sports-analytics',
    icon: '📈',
    colour: '#06B6D4',
    category: 'Technology & Data',
    description:
      'Leverage data, statistics, and machine learning to gain competitive advantage in sport. Sports analysts work with teams, broadcasters, and gambling companies to extract actionable insights.',
    workEnvironment: ['Office', 'Remote', 'Training facilities', 'Media'],
    jobOutlook: 'Rapidly growing',
    salaryRange: { min: 50000, max: 180000, currency: 'USD' },
    educationRequirements: [
      "Bachelor's in Statistics, Computer Science, Mathematics, or Sport Science",
      "Master's in Data Science or Sport Analytics",
      'Strong programming skills (Python, R, SQL)'
    ],
    keySkills: [
      'Statistical modelling',
      'Python / R / SQL',
      'Machine learning',
      'Data visualisation (Tableau, Power BI)',
      'Video analysis software',
      'Domain sport knowledge'
    ],
    certifications: [
      'Google Data Analytics Certificate',
      'MIT Sloan Sports Analytics Certificate',
      'Coursera / edX Data Science Specialisations',
      'Tableau / Power BI Certifications'
    ],
    careerProgressionSteps: [
      {
        level: 'Entry',
        title: 'Junior Analyst / Data Intern',
        yearsExperience: '0–2',
        description: 'Clean data, build dashboards, support senior analysts with reporting.'
      },
      {
        level: 'Mid',
        title: 'Sports Data Analyst',
        yearsExperience: '2–5',
        description: 'Build predictive models, present insights to coaches, integrate video & tracking data.'
      },
      {
        level: 'Senior',
        title: 'Head of Analytics / Data Science Lead',
        yearsExperience: '5+',
        description: 'Define analytical strategy, manage data infrastructure, advise at board level.'
      }
    ],
    successStories: [
      {
        name: 'Sam Borger',
        sport: 'Rowing (University)',
        career: 'Lead Data Scientist — Premier League Club',
        quote: 'Sport gave me the passion. Mathematics gave me the tools. Analytics let me combine them both at the highest level.'
      }
    ]
  },
  {
    title: 'Sports Nutrition',
    slug: 'sports-nutrition',
    icon: '🥗',
    colour: '#84CC16',
    category: 'Health & Science',
    description:
      'Optimise athlete performance and recovery through evidence-based nutrition strategies. Sports nutritionists work with individuals and teams to design fuelling plans tailored to training loads and competition demands.',
    workEnvironment: ['Clinic', 'Training facilities', 'Remote consultations', 'Lab'],
    jobOutlook: 'Growing',
    salaryRange: { min: 35000, max: 95000, currency: 'USD' },
    educationRequirements: [
      "Bachelor's in Nutrition & Dietetics or Sport Science",
      "Master's in Sport Nutrition (advantage)",
      'SENr or AND/BDA registration'
    ],
    keySkills: [
      'Macronutrient periodisation',
      'Supplement knowledge',
      'Body composition assessment',
      'Dietary analysis',
      'Client counselling',
      'Research literacy'
    ],
    certifications: [
      'SENr — Sport and Exercise Nutrition Register',
      'IOC Sports Nutrition Diploma',
      'ISAK Level 1 (body composition)',
      'Precision Nutrition Level 1 & 2'
    ],
    careerProgressionSteps: [
      {
        level: 'Entry',
        title: 'Nutritional Assistant / Graduate',
        yearsExperience: '0–2',
        description: 'Assist senior nutritionists, conduct dietary assessments, educate athletes on basics.'
      },
      {
        level: 'Mid',
        title: 'Sports Nutritionist',
        yearsExperience: '2–5',
        description: 'Design individual and team nutrition plans, monitor outcomes, advise on supplements.'
      },
      {
        level: 'Senior',
        title: 'Lead Nutritionist / Head of Nutrition',
        yearsExperience: '6+',
        description: 'Oversee nutrition department, publish research, consult for national teams.'
      }
    ],
    successStories: [
      {
        name: 'Dr. James Morton',
        sport: 'Cycling',
        career: 'Team Sky / INEOS Chief Nutritionist',
        quote: 'The marginal gains philosophy extends to every meal. Nutrition is training — it just happens off the bike.'
      }
    ]
  },
  {
    title: 'Physical Education & Teaching',
    slug: 'physical-education-teaching',
    icon: '🏫',
    colour: '#EC4899',
    category: 'Education',
    description:
      'Inspire the next generation of athletes and active citizens through quality physical education. PE teachers and sports educators shape lifelong habits, athletic skills, and a love of sport in young people.',
    workEnvironment: ['School', 'University', 'Community facilities', 'Classroom & field'],
    jobOutlook: 'Stable',
    salaryRange: { min: 30000, max: 75000, currency: 'USD' },
    educationRequirements: [
      "Bachelor's in Physical Education or Sport Science",
      'Qualified Teacher Status (QTS) / Teaching credential',
      'Safeguarding / DBS/Disclosure checks'
    ],
    keySkills: [
      'Curriculum delivery',
      'Behaviour management',
      'Differentiated instruction',
      'Sport skills across multiple disciplines',
      'Pastoral care',
      'Assessment & reporting'
    ],
    certifications: [
      'QTS — Qualified Teacher Status (UK)',
      'State Teaching License (US)',
      'Safeguarding & Child Protection',
      'First Aid / Emergency Action Plan'
    ],
    careerProgressionSteps: [
      {
        level: 'Entry',
        title: 'Newly Qualified Teacher (NQT)',
        yearsExperience: '0–2',
        description: 'Teach PE curriculum, assist with extra-curricular sport, complete induction year.'
      },
      {
        level: 'Mid',
        title: 'PE Teacher / Head of Sport',
        yearsExperience: '2–6',
        description: 'Lead PE department, manage sporting events and teams, mentor junior staff.'
      },
      {
        level: 'Senior',
        title: 'Head of PE / Director of Sport',
        yearsExperience: '6+',
        description: 'Set school sport vision, oversee all sport programmes, build community partnerships.'
      }
    ],
    successStories: [
      {
        name: 'Denise Lewis OBE',
        sport: 'Athletics (Olympic Heptathlon)',
        career: 'Sports Educator & Ambassador',
        quote: 'Every child deserves a teacher who shows them what their body can do. That\'s why I chose education.'
      }
    ]
  },
  {
    title: 'Sports Psychology',
    slug: 'sports-psychology',
    icon: '🧠',
    colour: '#7C3AED',
    category: 'Psychology & Wellbeing',
    description:
      'Help athletes perform under pressure, overcome adversity, and maintain mental health through the rigours of elite sport. Sports psychologists are increasingly central to high-performance teams.',
    workEnvironment: ['Office', 'Training facilities', 'Remote consultations', 'Competition venues'],
    jobOutlook: 'Growing',
    salaryRange: { min: 42000, max: 120000, currency: 'USD' },
    educationRequirements: [
      "Bachelor's in Psychology",
      "Master's in Sport Psychology",
      'BPS Chartered Psychologist / HCPC Registration',
      'BASES Accreditation (Sport & Exercise Psychologist)'
    ],
    keySkills: [
      'Mental performance coaching',
      'Cognitive-behavioural techniques',
      'Mindfulness & imagery',
      'Group dynamics',
      'Crisis counselling',
      'Performance profiling'
    ],
    certifications: [
      'BPS — British Psychological Society Chartership',
      'AASP — Certified Mental Performance Consultant (CMPC)',
      'BASES Accreditation',
      'Trauma-Informed Practice Certification'
    ],
    careerProgressionSteps: [
      {
        level: 'Entry',
        title: 'Trainee Sport Psychologist',
        yearsExperience: '0–3',
        description: 'Work under supervision, deliver mental skills workshops, build case experience.'
      },
      {
        level: 'Mid',
        title: 'Sport Psychologist',
        yearsExperience: '3–7',
        description: 'Work 1-to-1 with athletes, consult to teams, contribute to performance plans.'
      },
      {
        level: 'Senior',
        title: 'Lead / Consultant Sport Psychologist',
        yearsExperience: '7+',
        description: 'Advise Olympic programmes, publish research, train next-generation practitioners.'
      }
    ],
    successStories: [
      {
        name: 'Dr. Steve Peters',
        sport: 'Cycling (Medical Background)',
        career: 'Sports Psychologist — Team GB Cycling',
        quote: 'The Chimp Paradox changed how athletes understand their minds. Sport psychology can be the final frontier of performance.'
      }
    ]
  },
  {
    title: 'Sports Law & Ethics',
    slug: 'sports-law-ethics',
    icon: '⚖️',
    colour: '#64748B',
    category: 'Law & Governance',
    description:
      'Navigate the complex legal landscape of professional sport — contracts, doping disputes, governance, player rights, and integrity. Sports lawyers advise clubs, governing bodies, and athletes.',
    workEnvironment: ['Law office', 'Tribunal', 'Remote', 'Sports organisations'],
    jobOutlook: 'Stable',
    salaryRange: { min: 50000, max: 200000, currency: 'USD' },
    educationRequirements: [
      "Bachelor's degree + LLB / LLM in Law",
      'Bar/Solicitor qualification',
      'Sports Law specialism or LLM in Sports Law',
      'Advocacy experience'
    ],
    keySkills: [
      'Contract negotiation',
      'Dispute resolution & arbitration',
      'Doping regulation knowledge',
      'Governance & compliance',
      'Agent/player representation',
      'Legal research & writing'
    ],
    certifications: [
      'Solicitor Qualifying Exam (SQE)',
      'Bar Professional Training Course (BPTC)',
      'CAS — Court of Arbitration for Sport accreditation',
      'WADA Anti-Doping Rules compliance'
    ],
    careerProgressionSteps: [
      {
        level: 'Entry',
        title: 'Trainee Solicitor / Sports Law Intern',
        yearsExperience: '0–2',
        description: 'Work at sports law firms or governing bodies, research cases, draft documents.'
      },
      {
        level: 'Mid',
        title: 'Sports Solicitor / In-house Counsel',
        yearsExperience: '3–7',
        description: 'Handle contract negotiations, disciplinary hearings, and governance matters.'
      },
      {
        level: 'Senior',
        title: 'Partner / Legal Director / Arbitrator',
        yearsExperience: '8+',
        description: 'Lead complex disputes, advise governing bodies, represent elite athletes at CAS.'
      }
    ],
    successStories: [
      {
        name: 'Anita White MBE',
        sport: 'Gymnastics (Coach & Administrator)',
        career: 'Sports Governance & Ethics Lead',
        quote: 'Sport deserves integrity at every level. Legal expertise ensures the rules are fair and applied consistently.'
      }
    ]
  }
]
