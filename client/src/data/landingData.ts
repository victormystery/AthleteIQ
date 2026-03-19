export interface Stat {
  value: string
  label: string
}

export interface Feature {
  title: string
  description: string
  icon: string
  iconBg: string
}

export interface Step {
  title: string
  description: string
  icon: string
}

export interface Pathway {
  emoji: string
  title: string
  salary: string
  description: string
  tags: string[]
  bg: string
}

export interface Metric {
  value: string
  label: string
}

export interface Testimonial {
  quote: string
  name: string
  role: string
}

export interface SidebarItem {
  label: string
  active: boolean
  icon: string
}

export interface DashboardRec {
  emoji: string
  title: string
  score: number
  featured: boolean
  bg: string
}

export const stats: Stat[] = [
  { value: '11', label: 'Career pathways' },
  { value: '14', label: 'Assessed dimensions' },
  { value: '95%', label: 'Satisfaction rate' }
]

export const sidebarItems: SidebarItem[] = [
  {
    label: 'Dashboard',
    active: true,
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>'
  },
  {
    label: 'Pathways',
    active: false,
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"/></svg>'
  },
  {
    label: 'Roadmap',
    active: false,
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>'
  },
  {
    label: 'Profile',
    active: false,
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>'
  }
]

export const dashboardRecs: DashboardRec[] = [
  { emoji: '📊', title: 'Sports Analytics', score: 91, featured: true, bg: 'bg-primary-50' },
  { emoji: '🏋️', title: 'High Performance Sport', score: 78, featured: false, bg: 'bg-amber-50' },
  { emoji: '🧬', title: 'Sports Science & Medicine', score: 65, featured: false, bg: 'bg-red-50' }
]

export const features: Feature[] = [
  {
    title: 'AI-Powered Matching',
    description:
      'Our ML model analyses 14 dimensions of your athletic profile to surface the career pathways where you are most likely to succeed.',
    icon: '🧠',
    iconBg: 'bg-gradient-to-br from-primary-100 to-orange-50 shadow-lg shadow-primary-100/60 ring-1 ring-primary-200/50'
  },
  {
    title: 'Personalised Roadmaps',
    description:
      'Get step-by-step milestone roadmaps with certifications, estimated costs, and curated resources for each recommended pathway.',
    icon: '🗺️',
    iconBg: 'bg-gradient-to-br from-emerald-100 to-teal-50 shadow-lg shadow-emerald-100/60 ring-1 ring-emerald-200/50'
  },
  {
    title: 'Progress Tracking',
    description:
      'Track your journey through each milestone, update your status, and see your overall progress percentage as you advance.',
    icon: '📈',
    iconBg: 'bg-gradient-to-br from-amber-100 to-yellow-50 shadow-lg shadow-amber-100/60 ring-1 ring-amber-200/50'
  }
]

export const steps: Step[] = [
  {
    title: 'Create your account',
    description: 'Sign up in under a minute with just your name, email, and sport.',
    icon: '🔑'
  },
  {
    title: 'Complete the questionnaire',
    description: 'Answer 14 questions covering your sport, academics, leadership, and career motivation.',
    icon: '📝'
  },
  {
    title: 'Get your recommendations',
    description: 'Our ML model processes your profile and returns ranked career pathways with confidence scores.',
    icon: '🏆'
  },
  {
    title: 'Follow your roadmap',
    description: 'Access detailed milestone roadmaps, resources, and track your progress toward your new career.',
    icon: '🚀'
  }
]

export const pathways: Pathway[] = [
  {
    emoji: '🏋️',
    title: 'High Performance Sport',
    salary: '$55k – $120k',
    description: 'Coaching, performance analysis, and athlete development roles within elite programs.',
    tags: ['Coaching', 'Analysis', 'Leadership'],
    bg: 'bg-amber-50'
  },
  {
    emoji: '📊',
    title: 'Sports Analytics',
    salary: '$65k – $130k',
    description: 'Data-driven roles using statistics and ML to optimise team and athlete performance.',
    tags: ['Data', 'Python', 'Statistics'],
    bg: 'bg-amber-50'
  },
  {
    emoji: '🏢',
    title: 'Sports Management',
    salary: '$50k – $100k',
    description: 'Operations, events, sponsorship, and commercial roles within sports organisations.',
    tags: ['Operations', 'Business', 'Events'],
    bg: 'bg-green-50'
  },
  {
    emoji: '🧬',
    title: 'Sports Science & Medicine',
    salary: '$60k – $115k',
    description: 'Exercise physiology, biomechanics, physiotherapy, and sports nutrition research.',
    tags: ['Physiology', 'Research', 'Medicine'],
    bg: 'bg-red-50'
  },
  {
    emoji: '📺',
    title: 'Sports Media & Journalism',
    salary: '$45k – $90k',
    description: 'Broadcasting, writing, podcasting, and content creation for sports audiences.',
    tags: ['Media', 'Writing', 'Content'],
    bg: 'bg-purple-50'
  },
  {
    emoji: '⚖️',
    title: 'Sports Law & Ethics',
    salary: '$70k – $150k',
    description: 'Contract negotiation, regulatory compliance, and athlete rights representation.',
    tags: ['Law', 'Compliance', 'Contracts'],
    bg: 'bg-slate-100'
  }
]

export const metrics: Metric[] = [
  { value: '11', label: 'Career pathways mapped' },
  { value: '14', label: 'Profile dimensions' },
  { value: '6', label: 'Milestones per pathway' },
  { value: '3', label: 'User roles supported' }
]

export const testimonials: Testimonial[] = [
  {
    quote:
      "The questionnaire identified sports analytics as my top match. Two years later, I'm a performance analyst for a professional rugby club.",
    name: 'James Okonkwo',
    role: 'Former sprinter → Performance Analyst'
  },
  {
    quote:
      'I had no idea my captaincy experience translated so directly to sports management. AthleteIQ showed me the connection.',
    name: 'Sarah Mitchell',
    role: 'Former swimmer → Sports Manager'
  }
]
