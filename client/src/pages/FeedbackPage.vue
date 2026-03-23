<template>
  <div class="space-y-6">
    <!-- Header -->
    <div>
      <h2 class="text-2xl font-bold text-slate-800">Submit Feedback</h2>
      <p class="text-slate-500 mt-1">Rate your career recommendations to help us improve your results.</p>
    </div>

    <!-- Loading recommendations -->
    <div v-if="loadingRecs" class="flex items-center justify-center py-12">
      <div class="w-8 h-8 border-2 border-primary-500 border-t-transparent rounded-full animate-spin" />
    </div>

    <template v-else>
      <!-- No recommendations yet -->
      <div v-if="!recommendations.length" class="bg-slate-50 border border-slate-200 rounded-xl p-8 text-center space-y-3">
        <div class="mx-auto w-14 h-14 rounded-2xl bg-slate-100 flex items-center justify-center text-slate-400">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="w-7 h-7">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
          </svg>
        </div>
        <p class="font-medium text-slate-700">No recommendations to review yet</p>
        <p class="text-sm text-slate-500">Complete the career assessment first to get personalised recommendations.</p>
        <router-link
          to="/app/questionnaire"
          class="inline-block mt-1 py-2 px-5 bg-primary-600 hover:bg-primary-700 text-white text-sm font-medium rounded-lg transition-colors"
        >
          Take Assessment
        </router-link>
      </div>

      <template v-else>
        <!-- Success message -->
        <div v-if="submitted" class="bg-green-50 border border-green-200 rounded-xl p-5 flex gap-3">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-5 h-5 text-green-600 shrink-0 mt-0.5">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
          <div>
            <p class="text-sm font-semibold text-green-800">Feedback submitted — thank you!</p>
            <p class="text-sm text-green-700 mt-0.5">Your input helps improve career recommendations for all athletes.</p>
          </div>
        </div>

        <!-- Feedback form -->
        <form class="bg-white border border-slate-200 rounded-xl p-6 space-y-6" @submit.prevent="handleSubmit">
          <!-- Select recommendation -->
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1.5">Assessment to review</label>
            <select
              v-model="form.recommendationId"
              required
              class="w-full px-3 py-2.5 border border-slate-200 rounded-lg text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-primary-500/30 focus:border-primary-400 bg-white"
              @change="updatePathwayOptions"
            >
              <option value="">Select an assessment…</option>
              <option
                v-for="rec in recommendations"
                :key="rec._id"
                :value="rec._id"
              >
                {{ formatDate(rec.createdAt) }} — {{ rec.recommendations[0]?.pathwayName }}
              </option>
            </select>
          </div>

          <!-- Select pathway -->
          <div v-if="form.recommendationId">
            <label class="block text-sm font-medium text-slate-700 mb-1.5">Which pathway are you rating?</label>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
              <label
                v-for="item in currentPathways"
                :key="item.slug"
                :class="[
                  'flex items-center gap-3 p-3 border rounded-lg cursor-pointer transition-all text-sm',
                  form.pathwaySlug === item.slug
                    ? 'border-primary-400 bg-primary-50 text-primary-700'
                    : 'border-slate-200 hover:border-slate-300 text-slate-700'
                ]"
              >
                <input
                  v-model="form.pathwaySlug"
                  type="radio"
                  :value="item.slug"
                  class="sr-only"
                  required
                />
                <div class="flex items-center gap-2 flex-1 min-w-0">
                  <span
                    :class="[
                      'w-5 h-5 rounded-full border-2 flex items-center justify-center shrink-0',
                      form.pathwaySlug === item.slug ? 'border-primary-500' : 'border-slate-300'
                    ]"
                  >
                    <span v-if="form.pathwaySlug === item.slug" class="w-2.5 h-2.5 rounded-full bg-primary-500" />
                  </span>
                  <span class="truncate font-medium">{{ item.name }}</span>
                  <span class="ml-auto shrink-0 text-xs text-slate-400">#{{ item.rank }}</span>
                </div>
              </label>
            </div>
          </div>

          <!-- Rating -->
          <div v-if="form.pathwaySlug">
            <label class="block text-sm font-medium text-slate-700 mb-2">How accurate was this recommendation?</label>
            <div class="flex gap-2">
              <button
                v-for="n in 5"
                :key="n"
                type="button"
                :class="[
                  'w-10 h-10 rounded-lg border-2 text-sm font-bold transition-all',
                  form.rating >= n
                    ? 'border-amber-400 bg-amber-400 text-white'
                    : 'border-slate-200 text-slate-400 hover:border-amber-300'
                ]"
                @click="form.rating = n"
              >{{ n }}</button>
              <span class="ml-2 self-center text-sm text-slate-500">
                {{ ratingLabel }}
              </span>
            </div>
          </div>

          <!-- Interested -->
          <div v-if="form.rating > 0">
            <label class="block text-sm font-medium text-slate-700 mb-2">Are you interested in pursuing this pathway?</label>
            <div class="flex gap-3">
              <label
                v-for="opt in [{ value: true, label: 'Yes, interested' }, { value: false, label: 'Not for me' }]"
                :key="String(opt.value)"
                :class="[
                  'flex items-center gap-2 px-4 py-2.5 border rounded-lg cursor-pointer text-sm font-medium transition-all',
                  form.interested === opt.value
                    ? 'border-primary-400 bg-primary-50 text-primary-700'
                    : 'border-slate-200 text-slate-600 hover:border-slate-300'
                ]"
              >
                <input v-model="form.interested" type="radio" :value="opt.value" class="sr-only" />
                {{ opt.label }}
              </label>
            </div>
          </div>

          <!-- Comment -->
          <div v-if="form.rating > 0">
            <label class="block text-sm font-medium text-slate-700 mb-1.5">
              Additional comments <span class="text-slate-400 font-normal">(optional)</span>
            </label>
            <textarea
              v-model="form.comment"
              rows="3"
              maxlength="500"
              placeholder="What did you like or dislike about this recommendation?"
              class="w-full px-3 py-2.5 border border-slate-200 rounded-lg text-sm text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-primary-500/30 focus:border-primary-400 resize-none"
            />
            <p class="text-xs text-slate-400 text-right mt-1">{{ form.comment?.length ?? 0 }}/500</p>
          </div>

          <!-- Submit -->
          <div v-if="form.rating > 0" class="flex items-center gap-3 pt-2">
            <button
              type="submit"
              :disabled="submitting || !isFormValid"
              class="py-2.5 px-6 bg-primary-600 hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed text-white text-sm font-medium rounded-lg transition-colors"
            >
              <span v-if="submitting" class="flex items-center gap-2">
                <span class="w-4 h-4 border-2 border-white/40 border-t-white rounded-full animate-spin" />
                Submitting…
              </span>
              <span v-else>Submit Feedback</span>
            </button>
            <p v-if="submitError" class="text-sm text-red-600">{{ submitError }}</p>
          </div>
        </form>

        <!-- History -->
        <section v-if="historyList.length">
          <h3 class="text-sm font-semibold text-slate-600 uppercase tracking-wide mb-3">Past Feedback</h3>
          <div class="space-y-3">
            <div
              v-for="fb in historyList"
              :key="fb._id"
              class="bg-white border border-slate-200 rounded-xl p-4 flex items-start justify-between gap-4"
            >
              <div class="flex-1 min-w-0">
                <p class="text-sm font-medium text-slate-700">{{ fb.pathwaySlug.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase()) }}</p>
                <p v-if="fb.comment" class="text-xs text-slate-500 mt-1 line-clamp-2">{{ fb.comment }}</p>
                <p class="text-xs text-slate-400 mt-1">{{ formatDate(fb.createdAt) }}</p>
              </div>
              <div class="shrink-0 flex items-center gap-1">
                <span
                  v-for="n in 5"
                  :key="n"
                  :class="['text-base', n <= fb.rating ? 'text-amber-400' : 'text-slate-200']"
                >★</span>
              </div>
            </div>
          </div>
        </section>
      </template>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import feedbackService from '@/services/feedback.service'
import careerService, { type CareerRecommendation } from '@/services/career.service'

const loadingRecs = ref(false)
const submitting = ref(false)
const submitted = ref(false)
const submitError = ref('')

type FeedbackRecord = { _id: string; recommendationId: string; pathwaySlug: string; rating: number; interested: boolean; comment?: string; createdAt: string }

const recommendations = ref<CareerRecommendation[]>([])
const historyList = ref<FeedbackRecord[]>([])

const form = ref({
  recommendationId: '',
  pathwaySlug: '',
  rating: 0,
  interested: true as boolean,
  comment: ''
})

const currentPathways = computed<{ slug: string; name: string; rank: number }[]>(() => {
  if (!form.value.recommendationId) return []
  const rec = recommendations.value.find(r => r._id === form.value.recommendationId)
  return rec?.recommendations.map(r => ({ slug: r.pathwaySlug, name: r.pathwayName, rank: r.rank })) ?? []
})

const ratingLabel = computed(() => {
  const labels = ['', 'Very inaccurate', 'Somewhat inaccurate', 'Neutral', 'Somewhat accurate', 'Very accurate']
  return labels[form.value.rating] ?? ''
})

const isFormValid = computed(() =>
  form.value.recommendationId &&
  form.value.pathwaySlug &&
  form.value.rating > 0
)

function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString('en-AU', { day: 'numeric', month: 'short', year: 'numeric' })
}

function updatePathwayOptions() {
  form.value.pathwaySlug = ''
  form.value.rating = 0
}

async function handleSubmit() {
  if (!isFormValid.value) return
  submitting.value = true
  submitError.value = ''
  try {
    await feedbackService.submit({
      recommendationId: form.value.recommendationId,
      pathwaySlug: form.value.pathwaySlug,
      rating: form.value.rating,
      interested: form.value.interested,
      comment: form.value.comment || undefined
    })
    submitted.value = true
    form.value = { recommendationId: '', pathwaySlug: '', rating: 0, interested: true, comment: '' }
    // refresh history
    const hRes = await feedbackService.getHistory()
    historyList.value = hRes.data.data.feedback
  } catch (e: unknown) {
    const err = e as { response?: { data?: { message?: string } } }
    submitError.value = err.response?.data?.message ?? 'Failed to submit. Please try again.'
  } finally {
    submitting.value = false
  }
}

onMounted(async () => {
  loadingRecs.value = true
  try {
    const [recsRes, histRes] = await Promise.all([
      careerService.getRecommendations(),
      feedbackService.getHistory()
    ])
    recommendations.value = recsRes.data.data.recommendations ?? []
    historyList.value = histRes.data.data.feedback ?? []
  } catch {
    // silent — show empty state
  } finally {
    loadingRecs.value = false
  }
})
</script>
