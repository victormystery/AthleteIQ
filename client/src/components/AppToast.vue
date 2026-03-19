<template>
  <Teleport to="body">
    <div class="fixed bottom-6 right-6 z-[100] flex flex-col gap-2 w-full max-w-sm" aria-live="polite">
      <TransitionGroup name="toast">
        <div
          v-for="toast in toasts"
          :key="toast.id"
          :class="[
            'flex items-start gap-3 px-4 py-3.5 rounded-xl bg-white shadow-xl text-sm border-l-4',
            {
              'border-green-500': toast.type === 'success',
              'border-red-500':   toast.type === 'error',
              'border-primary-500': toast.type === 'info',
              'border-amber-500': toast.type === 'warning'
            }
          ]"
        >
          <div class="flex-1 min-w-0">
            <p v-if="toast.title" class="font-semibold text-slate-800 mb-0.5">{{ toast.title }}</p>
            <p class="text-slate-600">{{ toast.message }}</p>
          </div>
          <button
            class="shrink-0 text-slate-400 hover:text-slate-700 transition-colors p-0.5 rounded"
            @click="remove(toast.id)"
            aria-label="Close"
          >
            <svg viewBox="0 0 20 20" fill="currentColor" class="w-3.5 h-3.5">
              <path d="M6.28 5.22a.75.75 0 0 0-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 1 0 1.06 1.06L10 11.06l3.72 3.72a.75.75 0 1 0 1.06-1.06L11.06 10l3.72-3.72a.75.75 0 0 0-1.06-1.06L10 8.94 6.28 5.22z"/>
            </svg>
          </button>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { useToastStore } from '@/stores/toastStore'
import { storeToRefs } from 'pinia'

const store = useToastStore()
const { toasts } = storeToRefs(store)
const { remove } = store
</script>
