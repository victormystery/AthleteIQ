export interface Stat {
  value: string
  label: string
}

export interface Feature {
  title: string
  description: string
  icon: string
  iconBg: string
  iconColor: string
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
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/></svg>',
    iconBg: 'bg-primary-50',
    iconColor: 'text-primary-600'
  },
  {
    title: 'Personalised Roadmaps',
    description:
      'Get step-by-step milestone roadmaps with certifications, estimated costs, and curated resources for each recommended pathway.',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"/></svg>',
    iconBg: 'bg-emerald-50',
    iconColor: 'text-emerald-600'
  },
  {
    title: 'Progress Tracking',
    description:
      'Track your journey through each milestone, update your status, and see your overall progress percentage as you advance.',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 8v8m-8-5v5M8 3v1m8-1v1M3 9h1m16 0h1m-3.5-4.5l-.707.707M6.207 5.207l-.707-.707M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>',
    iconBg: 'bg-amber-50',
    iconColor: 'text-amber-600'
  }
]

export const steps: Step[] = [
  {
    title: 'Create your account',
    description: 'Sign up in under a minute with just your name, email, and sport.',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 21v-2a4 4 0 00-4-4H6a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"/></svg>'
  },
  {
    title: 'Complete the questionnaire',
    description: 'Answer 14 questions covering your sport, academics, leadership, and career motivation.',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/></svg>'
  },
  {
    title: 'Get your recommendations',
    description: 'Our ML model processes your profile and returns ranked career pathways with confidence scores.',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>'
  },
  {
    title: 'Follow your roadmap',
    description: 'Access detailed milestone roadmaps, resources, and track your progress toward your new career.',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>'
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
