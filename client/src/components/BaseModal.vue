<template>
  <Teleport to="body">
    <Transition name="fade">
      <div
        v-if="modelValue"
        class="fixed inset-0 bg-slate-900/50 flex items-center justify-center p-4 z-50 backdrop-blur-sm"
        @click.self="onOverlayClick"
      >
        <Transition name="slide-in" appear>
          <div
            v-if="modelValue"
            class="bg-white rounded-xl shadow-2xl w-full flex flex-col overflow-hidden max-h-[calc(100vh-4rem)]"
            :style="{ maxWidth: width }"
            role="dialog"
            aria-modal="true"
            :aria-labelledby="titleId"
          >
            <div class="flex items-center justify-between px-6 py-4 border-b border-slate-200 shrink-0">
              <h2 :id="titleId" class="text-lg font-semibold text-slate-800">{{ title }}</h2>
              <button
                class="flex text-slate-400 hover:text-slate-700 p-1 rounded transition-colors"
                @click="$emit('update:modelValue', false)"
                aria-label="Close"
              >
                <svg viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5">
                  <path d="M6.28 5.22a.75.75 0 0 0-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 1 0 1.06 1.06L10 11.06l3.72 3.72a.75.75 0 1 0 1.06-1.06L11.06 10l3.72-3.72a.75.75 0 0 0-1.06-1.06L10 8.94 6.28 5.22z"/>
                </svg>
              </button>
            </div>
            <div class="p-6 overflow-y-auto flex-1">
              <slot />
            </div>
            <div v-if="$slots.footer" class="px-6 py-4 border-t border-slate-200 flex justify-end gap-3 shrink-0">
              <slot name="footer" />
            </div>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'

const props = defineProps<{
  modelValue: boolean
  title: string
  width?: string
  persistent?: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
}>()

const titleId = `modal-title-${Math.random().toString(36).slice(2, 7)}`

function onOverlayClick() {
  if (!props.persistent) emit('update:modelValue', false)
}

function onKeydown(e: KeyboardEvent) {
  if (e.key === 'Escape' && props.modelValue && !props.persistent) {
    emit('update:modelValue', false)
  }
}

onMounted(() => document.addEventListener('keydown', onKeydown))
onUnmounted(() => document.removeEventListener('keydown', onKeydown))
</script>
