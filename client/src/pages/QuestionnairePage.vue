<template>
  <div class="max-w-3xl mx-auto">

    <BaseAlert type="info" :show="true" class="mb-6">
      This questionnaire explores your sports participation, skills, motivations, and career interests. Responses are confidential and used for academic research and pathway recommendations.
    </BaseAlert>

    <!-- ── Step Indicator ───────────────────────────────────────────────── -->
    <div class="mb-8 px-1">
      <div class="flex items-center">
        <template v-for="(title, i) in stepTitles" :key="i">
          <!-- Circle -->
          <div class="flex flex-col items-center">
            <div :class="[
              'w-9 h-9 rounded-full flex items-center justify-center text-sm font-bold transition-all duration-300 relative z-10 shrink-0',
              i + 1 < currentStep
                ? 'bg-primary-500 text-white shadow-sm shadow-primary-200'
                : i + 1 === currentStep
                  ? 'bg-primary-500 text-white ring-4 ring-primary-100 shadow-sm shadow-primary-200'
                  : 'bg-white border-2 border-slate-200 text-slate-400'
            ]">
              <svg v-if="i + 1 < currentStep" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="w-4 h-4">
                <polyline points="20 6 9 17 4 12"/>
              </svg>
              <span v-else class="leading-none">{{ i + 1 }}</span>
            </div>
            <span :class="[
              'hidden sm:block mt-2 text-[11px] font-semibold text-center whitespace-nowrap',
              i + 1 === currentStep ? 'text-primary-600' : i + 1 < currentStep ? 'text-slate-500' : 'text-slate-400'
            ]">{{ title }}</span>
          </div>
          <!-- Connector line -->
          <div v-if="i < stepTitles.length - 1" class="flex-1 h-0.5 mx-2 mb-0 sm:mb-5 relative">
            <div class="absolute inset-0 bg-slate-200 rounded-full" />
            <div
              class="absolute inset-0 rounded-full bg-primary-400 transition-all duration-500"
              :style="{ opacity: i + 1 < currentStep ? 1 : 0 }"
            />
          </div>
        </template>
      </div>
      <!-- Mobile label -->
      <p class="sm:hidden mt-3 text-center text-sm font-semibold text-primary-600">
        Step {{ currentStep }} of {{ totalSteps }}: {{ stepTitles[currentStep - 1] }}
      </p>
    </div>

    <!-- ── Card ─────────────────────────────────────────────────────────── -->
    <div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">

      <!-- Step header strip -->
      <div class="bg-gradient-to-r from-primary-600 to-primary-400 px-6 py-5">
        <div class="flex items-center gap-4">
          <div class="w-12 h-12 rounded-xl bg-white/15 flex items-center justify-center text-2xl shrink-0 backdrop-blur-sm">
            {{ stepIcons[currentStep - 1] }}
          </div>
          <div>
            <h2 class="text-lg font-bold text-white leading-snug">{{ stepTitles[currentStep - 1] }}</h2>
            <p class="text-sm text-primary-100 mt-0.5">{{ stepDescriptions[currentStep - 1] }}</p>
          </div>
        </div>
      </div>

      <!-- Step content -->
      <div class="p-6 lg:p-8">

        <!-- ── Step 1: Athletic Background ─────────────────────────────── -->
        <div v-if="currentStep === 1" class="flex flex-col gap-7">

          <!-- Primary sport -->
          <div>
            <label class="block text-sm font-semibold text-slate-700 mb-1.5">
              Primary Sport <span class="text-red-500">*</span>
            </label>
            <div class="grid grid-cols-2 sm:grid-cols-3 gap-2">
              <button
                v-for="opt in primarySportOptions" :key="opt"
                type="button"
                :class="[
                  'relative px-3 py-2.5 rounded-xl border text-sm font-medium transition-all text-center',
                  form.primary_sport === opt
                    ? 'border-primary-400 bg-primary-50 text-primary-700 shadow-sm'
                    : 'border-slate-200 text-slate-600 hover:border-primary-200 hover:bg-slate-50'
                ]"
                @click="form.primary_sport = opt"
              >
                <span v-if="form.primary_sport === opt" class="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-primary-400" />
                {{ opt }}
              </button>
            </div>
            <input
              v-if="form.primary_sport === 'Other'"
              v-model="otherSport"
              type="text"
              placeholder="Please specify your sport"
              class="mt-2 w-full rounded-xl border border-slate-200 px-4 py-3 text-sm text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent transition-shadow"
            />
            <p v-if="errors.primary_sport" class="mt-1.5 flex items-center gap-1 text-xs text-red-500">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-3.5 h-3.5 shrink-0"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
              {{ errors.primary_sport }}
            </p>
          </div>

          <!-- Academic level -->
          <div>
            <label class="block text-sm font-semibold text-slate-700 mb-2.5">
              Academic Level <span class="text-red-500">*</span>
            </label>
            <div class="grid grid-cols-2 sm:grid-cols-3 gap-2">
              <button
                v-for="opt in academicLevels" :key="opt"
                type="button"
                :class="[
                  'relative px-3 py-2.5 rounded-xl border text-sm font-medium transition-all text-center',
                  form.academic_level === opt
                    ? 'border-primary-400 bg-primary-50 text-primary-700 shadow-sm'
                    : 'border-slate-200 text-slate-600 hover:border-primary-200 hover:bg-slate-50'
                ]"
                @click="form.academic_level = opt"
              >
                <span v-if="form.academic_level === opt" class="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-primary-400" />
                {{ opt }}
              </button>
            </div>
            <p v-if="errors.academic_level" class="mt-1.5 flex items-center gap-1 text-xs text-red-500">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-3.5 h-3.5 shrink-0"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
              {{ errors.academic_level }}
            </p>
          </div>

          <!-- Years of participation -->
          <div>
            <label class="block text-sm font-semibold text-slate-700 mb-2.5">
              Years of Participation <span class="text-red-500">*</span>
            </label>
            <div class="flex gap-2">
              <button
                v-for="opt in participationYears" :key="opt"
                type="button"
                :class="[
                  'flex-1 py-2.5 rounded-xl border text-sm font-semibold transition-all',
                  form.participation_years === opt
                    ? 'border-primary-400 bg-primary-500 text-white shadow-sm'
                    : 'border-slate-200 text-slate-600 hover:border-primary-200 hover:bg-slate-50'
                ]"
                @click="form.participation_years = opt"
              >{{ opt }}</button>
            </div>
            <p v-if="errors.participation_years" class="mt-1.5 flex items-center gap-1 text-xs text-red-500">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-3.5 h-3.5 shrink-0"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
              {{ errors.participation_years }}
            </p>
          </div>

          <!-- Participation level -->
          <div>
            <label class="block text-sm font-semibold text-slate-700 mb-2.5">
              Participation Level <span class="text-red-500">*</span>
            </label>
            <div class="grid grid-cols-2 sm:grid-cols-3 gap-2">
              <button
                v-for="opt in participationLevels" :key="opt"
                type="button"
                :class="[
                  'relative px-3 py-2.5 rounded-xl border text-sm font-medium transition-all text-center',
                  form.participation_level === opt
                    ? 'border-primary-400 bg-primary-50 text-primary-700 shadow-sm'
                    : 'border-slate-200 text-slate-600 hover:border-primary-200 hover:bg-slate-50'
                ]"
                @click="form.participation_level = opt"
              >
                <span v-if="form.participation_level === opt" class="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-primary-400" />
                {{ opt }}
              </button>
            </div>
            <p v-if="errors.participation_level" class="mt-1.5 flex items-center gap-1 text-xs text-red-500">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-3.5 h-3.5 shrink-0"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
              {{ errors.participation_level }}
            </p>
          </div>
        </div>

        <!-- ── Step 2: Skills & Abilities ──────────────────────────────── -->
        <div v-else-if="currentStep === 2" class="flex flex-col gap-7">
          <div v-for="skill in skillFields" :key="skill.key" class="flex flex-col gap-3">
            <div class="flex items-start justify-between gap-2">
              <div>
                <p class="text-sm font-semibold text-slate-700">{{ skill.label }}</p>
                <p class="text-xs text-slate-400 mt-0.5">{{ skill.hint }}</p>
              </div>
              <div :class="[
                'shrink-0 w-10 h-10 rounded-xl flex items-center justify-center text-base font-bold transition-colors',
                (form as any)[skill.key] >= 4 ? 'bg-primary-500 text-white' : 'bg-slate-100 text-slate-600'
              ]">
                {{ (form as any)[skill.key] }}
              </div>
            </div>
            <!-- Rating buttons -->
            <div class="flex gap-1.5">
              <button
                v-for="n in 5" :key="n"
                type="button"
                :class="[
                  'flex-1 py-3 rounded-xl border text-sm font-bold transition-all',
                  (form as any)[skill.key] >= n
                    ? 'border-primary-500 bg-primary-500 text-white shadow-sm'
                    : 'border-slate-200 text-slate-400 hover:border-primary-200 hover:bg-primary-50 hover:text-primary-500'
                ]"
                @click="(form as any)[skill.key] = n"
              >{{ n }}</button>
            </div>
            <div class="flex justify-between text-[10px] font-medium text-slate-400 px-0.5">
              <span>{{ skill.minLabel }}</span>
              <span>{{ skill.maxLabel }}</span>
            </div>
          </div>
        </div>

        <!-- ── Step 3: Career Aspirations ──────────────────────────────── -->
        <div v-else-if="currentStep === 3" class="flex flex-col gap-7">

          <!-- Motivation -->
          <div>
            <label class="block text-sm font-semibold text-slate-700 mb-2.5">
              Primary Motivation <span class="text-red-500">*</span>
            </label>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
              <button
                v-for="opt in motivations" :key="opt.value"
                type="button"
                :class="[
                  'relative flex items-center gap-3 px-4 py-3.5 rounded-xl border text-left transition-all',
                  form.motivation === opt.value
                    ? 'border-primary-400 bg-primary-50 shadow-sm'
                    : 'border-slate-200 hover:border-primary-200 hover:bg-slate-50'
                ]"
                @click="form.motivation = opt.value"
              >
                <span class="text-2xl shrink-0 leading-none">{{ opt.icon }}</span>
                <div>
                  <p :class="['text-sm font-semibold', form.motivation === opt.value ? 'text-primary-700' : 'text-slate-700']">{{ opt.label }}</p>
                  <p class="text-xs text-slate-400 mt-0.5">{{ opt.description }}</p>
                </div>
                <span v-if="form.motivation === opt.value" class="absolute top-2.5 right-2.5 w-2 h-2 rounded-full bg-primary-400" />
              </button>
            </div>
            <p v-if="errors.motivation" class="mt-1.5 flex items-center gap-1 text-xs text-red-500">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-3.5 h-3.5 shrink-0"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
              {{ errors.motivation }}
            </p>
          </div>

          <!-- Career importance -->
          <div>
            <label class="block text-sm font-semibold text-slate-700 mb-2.5">
              Career Importance for Your Future Plans <span class="text-red-500">*</span>
            </label>
            <div class="flex flex-col gap-2">
              <button
                v-for="opt in careerImportance" :key="opt.value"
                type="button"
                :class="[
                  'relative flex items-center gap-3 px-4 py-3 rounded-xl border text-left transition-all',
                  form.career_importance === opt.value
                    ? 'border-primary-400 bg-primary-50 shadow-sm'
                    : 'border-slate-200 hover:border-primary-200 hover:bg-slate-50'
                ]"
                @click="form.career_importance = opt.value"
              >
                <span class="text-lg shrink-0 leading-none">{{ opt.icon }}</span>
                <span :class="['text-sm font-medium', form.career_importance === opt.value ? 'text-primary-700' : 'text-slate-700']">{{ opt.label }}</span>
                <span v-if="form.career_importance === opt.value" class="ml-auto shrink-0 w-5 h-5 rounded-full bg-primary-500 flex items-center justify-center">
                  <svg viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" class="w-3 h-3"><polyline points="20 6 9 17 4 12"/></svg>
                </span>
              </button>
            </div>
            <p v-if="errors.career_importance" class="mt-1.5 flex items-center gap-1 text-xs text-red-500">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-3.5 h-3.5 shrink-0"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
              {{ errors.career_importance }}
            </p>
          </div>

          <!-- Work environment -->
          <div>
            <label class="block text-sm font-semibold text-slate-700 mb-2.5">
              Preferred Work Environment <span class="text-red-500">*</span>
            </label>
            <div class="grid grid-cols-3 sm:grid-cols-5 gap-2">
              <button
                v-for="opt in workEnvironments" :key="opt.value"
                type="button"
                :class="[
                  'flex flex-col items-center gap-2 px-2 py-4 rounded-xl border transition-all',
                  form.work_environment === opt.value
                    ? 'border-primary-400 bg-primary-50 shadow-sm'
                    : 'border-slate-200 hover:border-primary-200 hover:bg-slate-50'
                ]"
                @click="form.work_environment = opt.value"
              >
                <span class="text-2xl leading-none">{{ opt.icon }}</span>
                <span :class="['text-xs font-semibold', form.work_environment === opt.value ? 'text-primary-700' : 'text-slate-600']">{{ opt.label }}</span>
              </button>
            </div>
            <p v-if="errors.work_environment" class="mt-1.5 flex items-center gap-1 text-xs text-red-500">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-3.5 h-3.5 shrink-0"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
              {{ errors.work_environment }}
            </p>
          </div>

          <!-- Education/training willingness -->
          <div>
            <label class="block text-sm font-semibold text-slate-700 mb-2.5">
              Education or Training You Can Realistically Pursue (Next 3-5 Years) <span class="text-red-500">*</span>
            </label>
            <div class="flex flex-col gap-2">
              <button
                v-for="opt in educationTrainingLevels" :key="opt"
                type="button"
                :class="[
                  'relative flex items-center gap-3 px-4 py-3 rounded-xl border text-left transition-all',
                  form.education_training_level === opt
                    ? 'border-primary-400 bg-primary-50 shadow-sm'
                    : 'border-slate-200 hover:border-primary-200 hover:bg-slate-50'
                ]"
                @click="form.education_training_level = opt"
              >
                <span :class="['text-sm font-medium', form.education_training_level === opt ? 'text-primary-700' : 'text-slate-700']">{{ opt }}</span>
                <span v-if="form.education_training_level === opt" class="ml-auto shrink-0 w-5 h-5 rounded-full bg-primary-500 flex items-center justify-center">
                  <svg viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" class="w-3 h-3"><polyline points="20 6 9 17 4 12"/></svg>
                </span>
              </button>
            </div>
            <p v-if="errors.education_training_level" class="mt-1.5 flex items-center gap-1 text-xs text-red-500">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-3.5 h-3.5 shrink-0"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
              {{ errors.education_training_level }}
            </p>
          </div>
        </div>

        <!-- ── Step 4: Context & Interests ─────────────────────────────── -->
        <div v-else-if="currentStep === 4" class="flex flex-col gap-7">

          <!-- Biggest challenge -->
          <div>
            <label class="block text-sm font-semibold text-slate-700 mb-2.5">
              Biggest Challenge <span class="text-red-500">*</span>
            </label>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
              <button
                v-for="opt in biggestChallenges" :key="opt.value"
                type="button"
                :class="[
                  'relative flex items-center gap-3 px-4 py-3 rounded-xl border text-left transition-all',
                  form.biggest_challenge === opt.value
                    ? 'border-primary-400 bg-primary-50 shadow-sm'
                    : 'border-slate-200 hover:border-primary-200 hover:bg-slate-50'
                ]"
                @click="form.biggest_challenge = opt.value"
              >
                <span class="text-xl shrink-0 leading-none">{{ opt.icon }}</span>
                <span :class="['text-sm font-medium', form.biggest_challenge === opt.value ? 'text-primary-700' : 'text-slate-700']">{{ opt.label }}</span>
                <span v-if="form.biggest_challenge === opt.value" class="absolute top-2.5 right-2.5 w-2 h-2 rounded-full bg-primary-400" />
              </button>
            </div>
            <p v-if="errors.biggest_challenge" class="mt-1.5 flex items-center gap-1 text-xs text-red-500">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-3.5 h-3.5 shrink-0"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
              {{ errors.biggest_challenge }}
            </p>
          </div>

          <!-- Injury history -->
          <div>
            <label class="block text-sm font-semibold text-slate-700 mb-2.5">
              Injury History <span class="text-red-500">*</span>
            </label>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
              <button
                v-for="opt in injuryOptions" :key="opt.value"
                type="button"
                :class="[
                  'relative flex items-center gap-3 px-4 py-3 rounded-xl border text-left transition-all',
                  form.injury_history === opt.value
                    ? 'border-primary-400 bg-primary-50 shadow-sm'
                    : 'border-slate-200 hover:border-primary-200 hover:bg-slate-50'
                ]"
                @click="form.injury_history = opt.value"
              >
                <span class="text-xl shrink-0 leading-none">{{ opt.icon }}</span>
                <span :class="['text-sm font-medium', form.injury_history === opt.value ? 'text-primary-700' : 'text-slate-700']">{{ opt.label }}</span>
                <span v-if="form.injury_history === opt.value" class="absolute top-2.5 right-2.5 w-2 h-2 rounded-full bg-primary-400" />
              </button>
            </div>
            <p v-if="errors.injury_history" class="mt-1.5 flex items-center gap-1 text-xs text-red-500">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-3.5 h-3.5 shrink-0"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
              {{ errors.injury_history }}
            </p>
          </div>

          <!-- Career interests -->
          <div>
            <div class="flex items-baseline justify-between mb-2.5">
              <label class="text-sm font-semibold text-slate-700">
                Career Interests <span class="text-red-500">*</span>
              </label>
              <span class="text-xs text-slate-400 font-medium">
                {{ form.career_interests.length }}/3 selected
              </span>
            </div>
            <!-- Mini progress bar for selections -->
            <div class="w-full h-1 bg-slate-100 rounded-full mb-3 overflow-hidden">
              <div
                class="h-full bg-primary-400 rounded-full transition-all duration-300"
                :style="{ width: `${(form.career_interests.length / 3) * 100}%` }"
              />
            </div>
            <div class="grid grid-cols-2 gap-2">
              <button
                v-for="opt in careerInterestOptions" :key="opt"
                type="button"
                :disabled="!form.career_interests.includes(opt) && form.career_interests.length >= 3"
                :class="[
                  'relative flex items-center gap-2 px-3 py-2.5 rounded-xl border text-sm font-medium text-left transition-all',
                  form.career_interests.includes(opt)
                    ? 'border-primary-400 bg-primary-50 text-primary-700 shadow-sm'
                    : 'border-slate-200 text-slate-600 hover:border-primary-200 hover:bg-slate-50',
                  !form.career_interests.includes(opt) && form.career_interests.length >= 3
                    ? 'opacity-40 cursor-not-allowed'
                    : ''
                ]"
                @click="toggleInterest(opt)"
              >
                <span v-if="form.career_interests.includes(opt)" class="shrink-0 w-4 h-4 rounded-full bg-primary-500 flex items-center justify-center">
                  <svg viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" class="w-2.5 h-2.5"><polyline points="20 6 9 17 4 12"/></svg>
                </span>
                <span v-else class="shrink-0 w-4 h-4 rounded-full border-2 border-slate-200" />
                {{ opt }}
              </button>
            </div>
            <p v-if="errors.career_interests" class="mt-1.5 flex items-center gap-1 text-xs text-red-500">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-3.5 h-3.5 shrink-0"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
              {{ errors.career_interests }}
            </p>
          </div>
        </div>

        <!-- ── Step 5: Review & Submit ───────────────────────────────────── -->
        <div v-else-if="currentStep === 5" class="flex flex-col gap-6">

          <!-- Section: Background -->
          <div>
            <div class="flex items-center justify-between mb-3">
              <p class="text-xs font-bold uppercase tracking-widest text-slate-400">Background</p>
              <button type="button" class="text-xs font-semibold text-primary-500 hover:text-primary-700 transition-colors" @click="currentStep = 1">Edit</button>
            </div>
            <div class="bg-slate-50 rounded-xl border border-slate-100 divide-y divide-slate-100">
              <div v-for="item in reviewSections.background" :key="item.label" class="flex items-center justify-between px-4 py-2.5 gap-4">
                <span class="text-xs font-semibold text-slate-500 w-32 shrink-0">{{ item.label }}</span>
                <span class="text-sm text-slate-800 text-right font-medium">{{ item.value }}</span>
              </div>
            </div>
          </div>

          <!-- Section: Skills -->
          <div>
            <div class="flex items-center justify-between mb-3">
              <p class="text-xs font-bold uppercase tracking-widest text-slate-400">Skills</p>
              <button type="button" class="text-xs font-semibold text-primary-500 hover:text-primary-700 transition-colors" @click="currentStep = 2">Edit</button>
            </div>
            <div class="grid grid-cols-2 gap-2">
              <div
                v-for="item in reviewSections.skills" :key="item.label"
                class="bg-slate-50 rounded-xl border border-slate-100 px-4 py-3"
              >
                <p class="text-xs font-semibold text-slate-500 mb-1">{{ item.label }}</p>
                <div class="flex items-center gap-1">
                  <div
                    v-for="n in 5" :key="n"
                    :class="['h-1.5 flex-1 rounded-full transition-colors', item.numValue >= n ? 'bg-primary-400' : 'bg-slate-200']"
                  />
                </div>
                <p class="mt-1 text-sm font-bold text-slate-700">{{ item.value }}</p>
              </div>
            </div>
          </div>

          <!-- Section: Aspirations -->
          <div>
            <div class="flex items-center justify-between mb-3">
              <p class="text-xs font-bold uppercase tracking-widest text-slate-400">Aspirations</p>
              <button type="button" class="text-xs font-semibold text-primary-500 hover:text-primary-700 transition-colors" @click="currentStep = 3">Edit</button>
            </div>
            <div class="bg-slate-50 rounded-xl border border-slate-100 divide-y divide-slate-100">
              <div v-for="item in reviewSections.aspirations" :key="item.label" class="flex items-center justify-between px-4 py-2.5 gap-4">
                <span class="text-xs font-semibold text-slate-500 w-32 shrink-0">{{ item.label }}</span>
                <span class="text-sm text-slate-800 text-right font-medium">{{ item.value }}</span>
              </div>
            </div>
          </div>

          <!-- Section: Context -->
          <div>
            <div class="flex items-center justify-between mb-3">
              <p class="text-xs font-bold uppercase tracking-widest text-slate-400">Context</p>
              <button type="button" class="text-xs font-semibold text-primary-500 hover:text-primary-700 transition-colors" @click="currentStep = 4">Edit</button>
            </div>
            <div class="bg-slate-50 rounded-xl border border-slate-100 divide-y divide-slate-100">
              <div v-for="item in reviewSections.context" :key="item.label" class="flex items-center justify-between px-4 py-2.5 gap-4">
                <span class="text-xs font-semibold text-slate-500 w-32 shrink-0">{{ item.label }}</span>
                <span class="text-sm text-slate-800 text-right font-medium">{{ item.value }}</span>
              </div>
            </div>
          </div>

          <!-- Error alert -->
          <BaseAlert v-if="submitError" type="error" :show="!!submitError">{{ submitError }}</BaseAlert>
        </div>
      </div>

      <!-- ── Navigation footer ─────────────────────────────────────────── -->
      <div class="flex items-center justify-between px-6 lg:px-8 py-4 bg-slate-50 border-t border-slate-100">
        <button
          v-if="currentStep > 1"
          type="button"
          class="flex items-center gap-1.5 px-4 py-2 rounded-lg text-sm font-semibold text-slate-600 border border-slate-200 bg-white hover:bg-slate-50 transition-colors"
          @click="currentStep--"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-4 h-4">
            <polyline points="15 18 9 12 15 6"/>
          </svg>
          Back
        </button>
        <div v-else />

        <div class="flex items-center gap-3">
          <!-- Step counter (mobile) -->
          <span class="sm:hidden text-xs text-slate-400 font-medium">{{ currentStep }}/{{ totalSteps }}</span>

          <button
            v-if="currentStep < totalSteps"
            type="button"
            class="flex items-center gap-1.5 px-5 py-2 rounded-lg text-sm font-semibold bg-primary-500 text-white hover:bg-primary-600 transition-colors shadow-sm shadow-primary-200"
            @click="nextStep"
          >
            Continue
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-4 h-4">
              <polyline points="9 18 15 12 9 6"/>
            </svg>
          </button>
          <button
            v-else
            type="button"
            :disabled="submitting"
            class="flex items-center gap-2 px-6 py-2.5 rounded-lg text-sm font-semibold bg-gradient-to-r from-primary-600 to-primary-500 text-white hover:from-primary-700 hover:to-primary-600 transition-all shadow-sm shadow-primary-200 disabled:opacity-60 disabled:cursor-not-allowed"
            @click="handleSubmit"
          >
            <svg v-if="submitting" class="w-4 h-4 animate-spin" viewBox="0 0 24 24" fill="none">
              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="3" stroke-dasharray="40" stroke-dashoffset="10" stroke-linecap="round"/>
            </svg>
            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-4 h-4">
              <path d="M22 2L11 13"/><path d="M22 2L15 22 11 13 2 9l20-7z"/>
            </svg>
            {{ submitting ? 'Analysing…' : 'Get My Recommendations' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import questionnaireService from '@/services/questionnaire.service'
import BaseAlert from '@/components/BaseAlert.vue'

const router = useRouter()

const totalSteps = 5
const currentStep = ref(1)
const submitting = ref(false)
const submitError = ref('')
const otherSport = ref('')

const stepTitles = [
  'Athletic Background',
  'Skills & Abilities',
  'Career Aspirations',
  'Context & Interests',
  'Review & Submit'
]

const stepIcons = ['🏅', '📊', '🎯', '🔍', '✅']

const stepDescriptions = [
  'Tell us about your sport and experience level.',
  'Rate yourself honestly — this helps us match you accurately.',
  'What drives you, your career focus, and preferred work environment.',
  'Help us understand your situation and specific interests.',
  'Everything look right? Submit to get your personalised recommendations.'
]

// ── Form state ─────────────────────────────────────────────────────────────
const form = reactive({
  primary_sport: '',
  academic_level: '',
  participation_years: '',
  participation_level: '',
  fitness_level: 3,
  technical_skill: 3,
  leadership: 3,
  data_comfort: 3,
  motivation: '',
  career_importance: '',
  work_environment: '',
  education_training_level: '',
  biggest_challenge: '',
  injury_history: '',
  career_interests: [] as string[]
})

const errors = reactive<Record<string, string>>({})

// ── Options ────────────────────────────────────────────────────────────────
const academicLevels = ['Year 1', 'Year 2', 'Year 3', 'Year 4', 'Postgraduate']
const primarySportOptions = ['Football (Soccer)', 'Basketball', 'Athletics / Track & Field', 'Volleyball', 'Rugby', 'Other']
const participationYears = ['Less than 1 year', '1-2 years', '3-5 years', 'More than 5 years']
const participationLevels = ['Not active', 'Recreational', 'University/School team', 'Club or academy', 'Elite/competitive pathway']

const skillFields = [
  { key: 'fitness_level', label: 'Fitness Level', hint: 'Your overall physical conditioning and endurance.', minLabel: 'Very low', maxLabel: 'Elite' },
  { key: 'technical_skill', label: 'Technical Skill', hint: 'Your mastery of sport-specific techniques and tactics.', minLabel: 'Beginner', maxLabel: 'Elite' },
  { key: 'leadership', label: 'Leadership', hint: 'Your ability to lead, motivate and mentor others.', minLabel: 'Prefer to follow', maxLabel: 'Natural leader' },
  { key: 'data_comfort', label: 'Data & Analytics Comfort', hint: 'How comfortable you are working with numbers and data.', minLabel: 'Avoid data', maxLabel: 'Love data' }
]

const motivations = [
  { value: 'Competition and performance', label: 'Competition and performance', icon: '🥇', description: 'Chasing results and high-level outcomes' },
  { value: 'Health and fitness', label: 'Health and fitness', icon: '💚', description: 'Building lifelong physical wellbeing' },
  { value: 'Helping or coaching others', label: 'Helping or coaching others', icon: '🏋️', description: 'Supporting athlete development' },
  { value: 'Academic or career opportunity', label: 'Academic or career opportunity', icon: '🎓', description: 'Using sport as a career pathway' },
  { value: 'Fame, media, or recognition', label: 'Fame, media, or recognition', icon: '🎙️', description: 'Visibility, influence, and public impact' }
]

const careerImportance = [
  { value: 'Not important', label: 'Not important', icon: '▫️' },
  { value: 'Slightly important', label: 'Slightly important', icon: '◽' },
  { value: 'Moderately important', label: 'Moderately important', icon: '◻️' },
  { value: 'Very important', label: 'Very important', icon: '🔷' },
  { value: 'My main career focus', label: 'My main career focus', icon: '🎯' }
]

const workEnvironments = [
  { value: 'On-field / practical', label: 'On-field', icon: '⚽' },
  { value: 'Office / management', label: 'Office', icon: '💼' },
  { value: 'Laboratory / science / clinical', label: 'Lab/Clinical', icon: '🔬' },
  { value: 'Media / creative', label: 'Media', icon: '🎬' },
  { value: 'A mix of environments', label: 'Mixed', icon: '🔄' }
]

const educationTrainingLevels = [
  'Short courses or certifications only',
  'Diploma',
  "Bachelor's degree or add-on program",
  "Master's degree",
  'Medical/clinical or doctoral pathway'
]

const biggestChallenges = [
  { value: 'Academic workload', label: 'Academic workload', icon: '📚' },
  { value: 'Time management', label: 'Time management', icon: '⏱️' },
  { value: 'Financial constraints', label: 'Financial constraints', icon: '💸' },
  { value: 'Injury risk or health', label: 'Injury risk or health', icon: '🩹' },
  { value: 'Lack of facilities or coaching', label: 'Lack of facilities or coaching', icon: '🏟️' },
  { value: 'Motivation', label: 'Motivation', icon: '🧭' }
]

const injuryOptions = [
  { value: 'None', label: 'None', icon: '✅' },
  { value: 'Minor (short recovery)', label: 'Minor (short recovery)', icon: '🟡' },
  { value: 'Moderate (missed competitions)', label: 'Moderate (missed competitions)', icon: '🟠' },
  { value: 'Severe (long-term impact)', label: 'Severe (long-term impact)', icon: '🔴' }
]

const careerInterestOptions = [
  'Professional athlete',
  'Coach / Coaching education',
  'Strength & conditioning / Fitness coach',
  'Sports science / Performance science',
  'Sports physiotherapy / Rehabilitation',
  'Sports analytics / Performance analysis',
  'Sports management / Administration',
  'Sports media / Journalism / Content creation',
  'Officiating / Refereeing',
  'Community sports development'
]

// ── Helpers ────────────────────────────────────────────────────────────────
function toggleInterest(opt: string) {
  const idx = form.career_interests.indexOf(opt)
  if (idx > -1) {
    form.career_interests.splice(idx, 1)
  } else if (form.career_interests.length < 3) {
    form.career_interests.push(opt)
  }
}

// ── Validation ─────────────────────────────────────────────────────────────
function validateStep(step: number): boolean {
  Object.keys(errors).forEach(k => delete errors[k])

  if (step === 1) {
    if (!form.primary_sport) {
      errors.primary_sport = 'Please select your primary sport'
    } else if (form.primary_sport === 'Other' && (!otherSport.value.trim() || otherSport.value.trim().length < 2)) {
      errors.primary_sport = 'Please specify your sport'
    }
    if (!form.academic_level) errors.academic_level = 'Please select your academic level'
    if (!form.participation_years) errors.participation_years = 'Please select years of participation'
    if (!form.participation_level) errors.participation_level = 'Please select your participation level'
  }

  if (step === 3) {
    if (!form.motivation) errors.motivation = 'Please select your motivation'
    if (!form.career_importance) errors.career_importance = 'Please select career importance'
    if (!form.work_environment) errors.work_environment = 'Please select a work environment'
    if (!form.education_training_level) errors.education_training_level = 'Please select your education/training level'
  }

  if (step === 4) {
    if (!form.biggest_challenge) errors.biggest_challenge = 'Please select your biggest challenge'
    if (!form.injury_history) errors.injury_history = 'Please select your injury history'
    if (form.career_interests.length === 0) errors.career_interests = 'Please select at least one career interest'
  }

  return Object.keys(errors).length === 0
}

function nextStep() {
  if (validateStep(currentStep.value)) {
    currentStep.value++
  }
}

// ── Review summary ─────────────────────────────────────────────────────────
const reviewSections = computed(() => ({
  background: [
    { label: 'Sport', value: form.primary_sport === 'Other' ? otherSport.value : form.primary_sport },
    { label: 'Academic Level', value: form.academic_level },
    { label: 'Years Active', value: form.participation_years },
    { label: 'Level', value: form.participation_level }
  ],
  skills: [
    { label: 'Fitness', value: `${form.fitness_level}/5`, numValue: form.fitness_level },
    { label: 'Technical Skill', value: `${form.technical_skill}/5`, numValue: form.technical_skill },
    { label: 'Leadership', value: `${form.leadership}/5`, numValue: form.leadership },
    { label: 'Data Comfort', value: `${form.data_comfort}/5`, numValue: form.data_comfort }
  ],
  aspirations: [
    { label: 'Motivation', value: form.motivation },
    { label: 'Career Priority', value: form.career_importance },
    { label: 'Work Environment', value: form.work_environment },
    { label: 'Education/Training', value: form.education_training_level }
  ],
  context: [
    { label: 'Biggest Challenge', value: form.biggest_challenge },
    { label: 'Injury History', value: form.injury_history },
    { label: 'Interests', value: form.career_interests.join(', ') }
  ]
}))

// ── Submit ─────────────────────────────────────────────────────────────────
async function handleSubmit() {
  submitting.value = true
  submitError.value = ''
  try {
    const payload = {
      primary_sport: form.primary_sport,
      academic_level: form.academic_level,
      participation_years: form.participation_years,
      participation_level: form.participation_level,
      fitness_level: form.fitness_level,
      technical_skill: form.technical_skill,
      leadership: form.leadership,
      data_comfort: form.data_comfort,
      motivation: form.motivation,
      career_importance: form.career_importance,
      work_environment: form.work_environment,
      education_training_level: form.education_training_level,
      biggest_challenge: form.biggest_challenge,
      injury_history: form.injury_history,
      career_interests: form.career_interests
    }
    if (payload.primary_sport === 'Other') {
      payload.primary_sport = otherSport.value.trim()
    }
    const { data } = await questionnaireService.submit(payload)
    router.push({ name: 'Results', state: { recommendation: JSON.stringify(data.data.recommendation) } })
  } catch (err: unknown) {
    const e = err as { response?: { data?: { message?: string } }; message?: string }
    submitError.value = e.response?.data?.message ?? e.message ?? 'Submission failed. Please try again.'
  } finally {
    submitting.value = false
  }
}
</script>
