<template>
  <div>
    <!-- Page header -->
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-slate-800">My Profile</h1>
      <p class="mt-0.5 text-sm text-slate-500">Manage your personal information and account settings.</p>
    </div>

    <!-- Loading -->
    <div v-if="loading && !profile" class="flex justify-center py-20">
      <AppSpinner size="lg" />
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-[260px_1fr] gap-6 items-start">
      <!-- Profile card (left) -->
      <div class="flex flex-col gap-4">
        <BaseCard>
          <div class="flex flex-col items-center text-center pt-2 pb-5 border-b border-slate-100 mb-4">
            <div class="relative mb-4">
              <UserAvatar :name="form.name || user?.name || ''" size="xl" />
              <div class="absolute -bottom-1 -right-1 w-6 h-6 bg-green-400 rounded-full border-2 border-white" title="Active" />
            </div>
            <h2 class="text-lg font-bold text-slate-800">{{ profile?.name ?? user?.name ?? 'Athlete' }}</h2>
            <p class="text-sm text-slate-400 mt-0.5">{{ profile?.email ?? user?.email ?? '' }}</p>
            <span :class="roleBadgeClass(profile?.role ?? user?.role ?? '')" class="inline-flex items-center mt-3 text-xs px-3 py-1 rounded-full font-semibold capitalize border">
              {{ formatRole(profile?.role ?? user?.role ?? '') }}
            </span>
          </div>

          <div class="space-y-3">
            <div class="flex justify-between items-center">
              <span class="text-xs text-slate-500">Member since</span>
              <span class="text-xs font-semibold text-slate-700">{{ memberSince }}</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-xs text-slate-500">Account type</span>
              <span class="text-xs font-semibold text-slate-700 capitalize">{{ formatRole(profile?.role ?? user?.role ?? '') }}</span>
            </div>
          </div>
        </BaseCard>

        <!-- Tips card -->
        <div class="bg-primary-50 border border-primary-100 rounded-xl p-4">
          <div class="flex items-start gap-2.5">
            <div class="w-7 h-7 rounded-lg bg-primary-100 flex items-center justify-center shrink-0 mt-0.5">
              <svg viewBox="0 0 24 24" fill="none" stroke="#ea580c" stroke-width="2" class="w-4 h-4">
                <circle cx="12" cy="12" r="10"/>
                <path d="M12 8v4M12 16h.01"/>
              </svg>
            </div>
            <div>
              <p class="text-xs font-semibold text-primary-800">Profile tip</p>
              <p class="text-xs text-primary-700/80 mt-0.5 leading-relaxed">Keep your profile up to date to get more accurate career recommendations.</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Right column -->
      <div class="flex flex-col gap-5">
        <!-- Personal Information -->
        <BaseCard title="Personal Information" subtitle="Update your display name and account details.">
          <form @submit.prevent="handleSave" class="flex flex-col gap-4" novalidate>
            <BaseAlert v-if="saveError" type="error" :show="!!saveError" dismissible @dismiss="saveError = ''">
              {{ saveError }}
            </BaseAlert>
            <BaseAlert v-if="saveSuccess" type="success" :show="saveSuccess" dismissible @dismiss="saveSuccess = false">
              Your profile has been updated successfully.
            </BaseAlert>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
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
            </div>

            <div class="flex justify-end gap-3 pt-1 border-t border-slate-100 mt-1">
              <BaseButton variant="secondary" type="button" @click="resetForm">
                Discard changes
              </BaseButton>
              <BaseButton type="submit" :loading="saving">
                Save changes
              </BaseButton>
            </div>
          </form>
        </BaseCard>

        <!-- Danger Zone -->
        <BaseCard>
          <div class="flex items-start justify-between gap-4 flex-wrap">
            <div>
              <h3 class="text-sm font-semibold text-red-700">Danger Zone</h3>
              <p class="text-sm text-slate-500 mt-1 max-w-sm">
                Permanently delete your account and all associated data. This action is irreversible.
              </p>
            </div>
            <BaseButton variant="danger" size="sm" class="shrink-0" @click="showDeleteModal = true">
              <svg viewBox="0 0 20 20" fill="currentColor" class="w-3.5 h-3.5">
                <path fill-rule="evenodd" d="M8.75 1A2.75 2.75 0 0 0 6 3.75v.443c-.795.077-1.584.176-2.365.298a.75.75 0 1 0 .23 1.482l.149-.022.841 10.518A2.75 2.75 0 0 0 7.596 19h4.807a2.75 2.75 0 0 0 2.742-2.53l.841-10.519.149.023a.75.75 0 0 0 .23-1.482A41.03 41.03 0 0 0 14 4.193V3.75A2.75 2.75 0 0 0 11.25 1h-2.5zM10 4c.84 0 1.673.025 2.5.075V3.75c0-.69-.56-1.25-1.25-1.25h-2.5c-.69 0-1.25.56-1.25 1.25v.325C8.327 4.025 9.16 4 10 4zM8.58 7.72a.75.75 0 0 0-1.5.06l.3 7.5a.75.75 0 1 0 1.5-.06l-.3-7.5zm4.34.06a.75.75 0 1 0-1.5-.06l-.3 7.5a.75.75 0 1 0 1.5.06l.3-7.5z" clip-rule="evenodd"/>
              </svg>
              Delete account
            </BaseButton>
          </div>
        </BaseCard>
      </div>
    </div>

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
        <BaseButton variant="secondary" @click="showDeleteModal = false">Cancel</BaseButton>
        <BaseButton variant="danger" :disabled="deleteConfirm !== 'DELETE'" @click="handleDelete">
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

const memberSince = computed(() => formatDate(profile.value?.createdAt ?? null))

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
})

function resetForm() {
  form.name = profile.value?.name ?? user.value?.name ?? ''
  errors.name = ''
  saveError.value = ''
  saveSuccess.value = false
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
