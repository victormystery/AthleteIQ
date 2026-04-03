<template>
  <div class="flex flex-col gap-6">
    <!-- Loading -->
    <div v-if="loading && !profile" class="flex justify-center py-20">
      <AppSpinner size="lg" />
    </div>

    <template v-else>
      <!-- ── Hero card ──────────────────────────────────── -->
      <div class="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">
        <!-- Gradient banner -->
        <div class="h-24 bg-gradient-to-br from-primary-700 via-primary-500 to-orange-400 relative">
          <div
            class="absolute inset-0 opacity-[0.07]"
            style="background-image: repeating-linear-gradient(45deg, #fff 0, #fff 1px, transparent 0, transparent 50%); background-size: 14px 14px;"
          />
        </div>

        <div class="px-6 pb-6">
          <!-- Avatar + identity -->
          <div class="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4 -mt-10">
            <div class="flex items-end gap-4">
              <div class="relative">
                <div class="rounded-2xl ring-4 ring-white shadow-lg overflow-hidden">
                  <UserAvatar :name="form.name || user?.name || ''" size="xl" />
                </div>
                <div class="absolute -bottom-1 -right-1 w-4 h-4 bg-green-400 rounded-full border-2 border-white" title="Active" />
              </div>
              <div class="mb-1">
                <h2 class="text-xl font-bold text-slate-800 leading-tight">
                  {{ profile?.name ?? user?.name ?? 'Athlete' }}
                </h2>
                <p class="text-sm text-slate-500 mt-0.5">{{ profile?.email ?? user?.email ?? '' }}</p>
              </div>
            </div>
            <span
              :class="roleBadgeClass(profile?.role ?? user?.role ?? '')"
              class="inline-flex items-center self-start sm:self-auto mb-1 text-xs px-3 py-1.5 rounded-full font-semibold capitalize border"
            >
              {{ formatRole(profile?.role ?? user?.role ?? '') }}
            </span>
          </div>

          <!-- Stats row -->
          <div class="mt-5 pt-5 border-t border-slate-100 grid grid-cols-2 sm:grid-cols-4 gap-5">
            <div>
              <p class="text-xs text-slate-400 mb-0.5">Member since</p>
              <p class="text-sm font-semibold text-slate-700">{{ memberSince }}</p>
            </div>
            <div>
              <p class="text-xs text-slate-400 mb-0.5">Sport</p>
              <p class="text-sm font-semibold text-slate-700">{{ extProfile?.primarySport || '—' }}</p>
            </div>
            <div>
              <p class="text-xs text-slate-400 mb-0.5">Year of study</p>
              <p class="text-sm font-semibold text-slate-700">{{ extProfile?.yearOfStudy || '—' }}</p>
            </div>
            <div>
              <p class="text-xs text-slate-400 mb-1">Profile completion</p>
              <div class="flex items-center gap-2">
                <div class="flex-1 h-1.5 bg-slate-100 rounded-full overflow-hidden">
                  <div
                    class="h-full bg-primary-500 rounded-full transition-all duration-500"
                    :style="{ width: profileCompletion + '%' }"
                  />
                </div>
                <span class="text-xs font-semibold text-slate-600 shrink-0">{{ profileCompletion }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ── Forms row ──────────────────────────────────── -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Account settings -->
        <BaseCard>
          <template #header>
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 rounded-lg bg-slate-100 flex items-center justify-center shrink-0">
                <svg class="w-4 h-4 text-slate-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                  <circle cx="12" cy="7" r="4" />
                </svg>
              </div>
              <div>
                <h3 class="text-base font-semibold text-slate-800">Account</h3>
                <p class="text-sm text-slate-500">Your display name and login details.</p>
              </div>
            </div>
          </template>

          <form @submit.prevent="handleSave" class="flex flex-col gap-4" novalidate>
            <BaseAlert v-if="saveError" type="error" :show="!!saveError" dismissible @dismiss="saveError = ''">
              {{ saveError }}
            </BaseAlert>
            <BaseAlert v-if="saveSuccess" type="success" :show="saveSuccess" dismissible @dismiss="saveSuccess = false">
              Profile updated successfully.
            </BaseAlert>

            <BaseInput
              v-model="form.name"
              label="Full name"
              placeholder="Your full name"
              :error="errors.name"
              required
              @blur="validateName"
            />
            <BaseInput
              :model-value="profile?.email ?? user?.email ?? ''"
              label="Email address"
              type="email"
              :disabled="true"
              hint="Email address cannot be changed"
            />

            <div class="flex justify-end gap-2 pt-3 border-t border-slate-100">
              <BaseButton tag="button" variant="secondary" size="sm" type="button" @click="resetForm">Discard</BaseButton>
              <BaseButton tag="button" size="sm" type="submit" :loading="saving">Save changes</BaseButton>
            </div>
          </form>
        </BaseCard>

        <!-- Athletic details -->
        <BaseCard>
          <template #header>
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 rounded-lg bg-primary-50 flex items-center justify-center shrink-0">
                <svg class="w-4 h-4 text-primary-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M6 18 17.94 6M17.94 6H9M17.94 6V14" />
                </svg>
              </div>
              <div>
                <h3 class="text-base font-semibold text-slate-800">Athletic Profile</h3>
                <p class="text-sm text-slate-500">Sport background and academic details.</p>
              </div>
            </div>
          </template>

          <form @submit.prevent="handleSaveExtended" class="flex flex-col gap-4" novalidate>
            <BaseAlert v-if="extSaveError" type="error" :show="!!extSaveError" dismissible @dismiss="extSaveError = ''">
              {{ extSaveError }}
            </BaseAlert>
            <BaseAlert v-if="extSaveSuccess" type="success" :show="extSaveSuccess" dismissible @dismiss="extSaveSuccess = false">
              Athletic profile updated!
            </BaseAlert>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <BaseInput
                v-model="extForm.primarySport"
                label="Primary sport"
                placeholder="e.g. Basketball"
              />
              <div class="flex flex-col gap-1.5">
                <label class="text-sm font-medium text-slate-700">Year of study</label>
                <select
                  v-model="extForm.yearOfStudy"
                  class="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm text-slate-800 bg-white outline-none transition-all duration-150 focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500"
                >
                  <option value="">Select year…</option>
                  <option value="Year 1">Year 1</option>
                  <option value="Year 2">Year 2</option>
                  <option value="Year 3">Year 3</option>
                  <option value="Year 4">Year 4</option>
                  <option value="Postgraduate">Postgraduate</option>
                  <option value="Professional">Professional</option>
                </select>
              </div>
              <BaseInput
                v-model="extForm.university"
                label="University / Institution"
                placeholder="e.g. University of Melbourne"
              />
              <BaseInput
                v-model="extForm.programOfStudy"
                label="Program of study"
                placeholder="e.g. Sports Science"
              />
            </div>

            <div class="flex justify-end gap-2 pt-3 border-t border-slate-100">
              <BaseButton tag="button" variant="secondary" size="sm" type="button" @click="resetExtForm">Discard</BaseButton>
              <BaseButton tag="button" size="sm" type="submit" :loading="savingExt">Save profile</BaseButton>
            </div>
          </form>
        </BaseCard>
      </div>

      <!-- ── Bio card ───────────────────────────────────── -->
      <BaseCard>
        <template #header>
          <div>
            <h3 class="text-base font-semibold text-slate-800">Bio</h3>
            <p class="text-sm text-slate-500">Tell us about your athletic journey and goals.</p>
          </div>
        </template>

        <form @submit.prevent="handleSaveExtended" class="flex flex-col gap-3" novalidate>
          <textarea
            v-model="extForm.bio"
            rows="4"
            maxlength="500"
            placeholder="A short bio about your athletic journey, goals, or achievements…"
            class="w-full px-3 py-2.5 border border-slate-300 rounded-lg text-sm text-slate-800 placeholder-slate-400 outline-none resize-none transition-all duration-150 focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500"
          />
          <div class="flex items-center justify-between">
            <span class="text-xs text-slate-400">{{ extForm.bio?.length ?? 0 }} / 500 characters</span>
            <BaseButton tag="button" size="sm" type="submit" :loading="savingExt">Save bio</BaseButton>
          </div>
        </form>
      </BaseCard>

      <!-- ── Danger zone ────────────────────────────────── -->
      <div class="bg-red-50 border border-red-100 rounded-xl p-5 flex items-start justify-between gap-4 flex-wrap">
        <div>
          <h3 class="text-sm font-semibold text-red-700">Danger Zone</h3>
          <p class="text-sm text-slate-500 mt-1 max-w-sm">
            Permanently delete your account and all associated data. This action is irreversible.
          </p>
        </div>
        <BaseButton tag="button" variant="danger" size="sm" class="shrink-0" @click="showDeleteModal = true">
          <svg viewBox="0 0 20 20" fill="currentColor" class="w-3.5 h-3.5">
            <path fill-rule="evenodd" d="M8.75 1A2.75 2.75 0 0 0 6 3.75v.443c-.795.077-1.584.176-2.365.298a.75.75 0 1 0 .23 1.482l.149-.022.841 10.518A2.75 2.75 0 0 0 7.596 19h4.807a2.75 2.75 0 0 0 2.742-2.53l.841-10.519.149.023a.75.75 0 0 0 .23-1.482A41.03 41.03 0 0 0 14 4.193V3.75A2.75 2.75 0 0 0 11.25 1h-2.5zM10 4c.84 0 1.673.025 2.5.075V3.75c0-.69-.56-1.25-1.25-1.25h-2.5c-.69 0-1.25.56-1.25 1.25v.325C8.327 4.025 9.16 4 10 4zM8.58 7.72a.75.75 0 0 0-1.5.06l.3 7.5a.75.75 0 1 0 1.5-.06l-.3-7.5zm4.34.06a.75.75 0 1 0-1.5-.06l-.3 7.5a.75.75 0 1 0 1.5.06l.3-7.5z" clip-rule="evenodd" />
          </svg>
          Delete account
        </BaseButton>
      </div>
    </template>

    <!-- Delete confirmation modal -->
    <BaseModal v-model="showDeleteModal" title="Delete Account" :persistent="true">
      <div class="flex flex-col gap-4">
        <BaseAlert type="error" :show="true">
          This action is permanent and cannot be undone. All your data will be deleted immediately.
        </BaseAlert>
        <p class="text-sm text-slate-600">
          Type <strong class="font-bold text-slate-800 tracking-wide">DELETE</strong> below to confirm:
        </p>
        <BaseInput v-model="deleteConfirm" placeholder="DELETE" />
      </div>
      <template #footer>
        <BaseButton tag="button" variant="secondary" @click="showDeleteModal = false">Cancel</BaseButton>
        <BaseButton tag="button" variant="danger" :disabled="deleteConfirm !== 'DELETE'" @click="handleDelete">
          Delete permanently
        </BaseButton>
      </template>
    </BaseModal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useUserStore } from '@/stores/userStore'
import { useAuthStore } from '@/stores/authStore'
import { useToast } from '@/composables/useToast'
import { formatDate } from '@/utils/formatDate'
import { required } from '@/utils/validators'
import profileService, { type UserProfile } from '@/services/profile.service'
import BaseCard from '@/components/BaseCard.vue'
import BaseInput from '@/components/BaseInput.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseAlert from '@/components/BaseAlert.vue'
import BaseModal from '@/components/BaseModal.vue'
import UserAvatar from '@/components/UserAvatar.vue'
import AppSpinner from '@/components/AppSpinner.vue'

const userStore = useUserStore()
const authStore = useAuthStore()
const toast = useToast()

const { profile, loading } = storeToRefs(userStore)
const { user } = storeToRefs(authStore)

const form = reactive({ name: '' })
const errors = reactive({ name: '' })
const saving = ref(false)
const saveError = ref('')
const saveSuccess = ref(false)
const showDeleteModal = ref(false)
const deleteConfirm = ref('')

// Extended athletic profile
const extProfile = ref<UserProfile | null>(null)
const extForm = reactive({
  primarySport: '',
  yearOfStudy: '',
  university: '',
  programOfStudy: '',
  bio: ''
})
const savingExt = ref(false)
const extSaveError = ref('')
const extSaveSuccess = ref(false)

const memberSince = computed(() => formatDate(profile.value?.createdAt ?? null))

const profileCompletion = computed(() => {
  const fields = [
    profile.value?.name || user.value?.name,
    extProfile.value?.primarySport,
    extProfile.value?.yearOfStudy,
    extProfile.value?.university,
    extProfile.value?.programOfStudy,
    extProfile.value?.bio
  ]
  const filled = fields.filter(Boolean).length
  return Math.round((filled / fields.length) * 100)
})

function formatRole(role: string): string {
  const labels: Record<string, string> = {
    student: 'Student',
    career_advisor: 'Career Advisor',
    admin: 'Admin'
  }
  return labels[role] ?? role
}

function roleBadgeClass(role: string): string {
  const map: Record<string, string> = {
    student: 'bg-emerald-50 text-emerald-700 border-emerald-100',
    career_advisor: 'bg-blue-50 text-blue-700 border-blue-100',
    admin: 'bg-amber-50 text-amber-700 border-amber-100'
  }
  return map[role] ?? 'bg-slate-100 text-slate-600 border-slate-200'
}

onMounted(async () => {
  await userStore.fetchProfile().catch(() => {})
  resetForm()
  try {
    const res = await profileService.getProfile()
    extProfile.value = res.data.data.profile
    resetExtForm()
  } catch {
    // profile may not exist yet — form starts empty
  }
})

function resetForm() {
  form.name = profile.value?.name ?? user.value?.name ?? ''
  errors.name = ''
  saveError.value = ''
  saveSuccess.value = false
}

function resetExtForm() {
  const p = extProfile.value
  extForm.primarySport = p?.primarySport ?? ''
  extForm.yearOfStudy = p?.yearOfStudy ?? ''
  extForm.university = p?.university ?? ''
  extForm.programOfStudy = p?.programOfStudy ?? ''
  extForm.bio = p?.bio ?? ''
  extSaveError.value = ''
  extSaveSuccess.value = false
}

async function handleSaveExtended() {
  savingExt.value = true
  extSaveError.value = ''
  extSaveSuccess.value = false
  try {
    const res = await profileService.updateProfile({
      primarySport: extForm.primarySport,
      yearOfStudy: extForm.yearOfStudy,
      university: extForm.university,
      programOfStudy: extForm.programOfStudy,
      bio: extForm.bio
    })
    extProfile.value = res.data.data.profile
    extSaveSuccess.value = true
    toast.success('Athletic profile updated!')
  } catch (err: unknown) {
    const axiosErr = err as { response?: { data?: { message?: string } } }
    extSaveError.value = axiosErr.response?.data?.message ?? 'Failed to save changes'
  } finally {
    savingExt.value = false
  }
}

function validateName() {
  errors.name = required(form.name) ? '' : 'Name is required'
}

async function handleSave() {
  validateName()
  if (errors.name) return
  saving.value = true
  saveError.value = ''
  saveSuccess.value = false
  try {
    await userStore.updateProfile({ name: form.name })
    saveSuccess.value = true
    toast.success('Profile updated!')
  } catch (err: unknown) {
    const axiosErr = err as { response?: { data?: { message?: string } } }
    saveError.value = axiosErr.response?.data?.message ?? 'Failed to save changes'
  } finally {
    saving.value = false
  }
}

function handleDelete() {
  authStore.logout()
  toast.info('Account deleted. Goodbye!')
  showDeleteModal.value = false
}
</script>
