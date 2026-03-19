import { ref, type Ref } from 'vue'

interface UseFetchReturn<T> {
  data: Ref<T | null>
  error: Ref<string | null>
  loading: Ref<boolean>
  execute: (...args: unknown[]) => Promise<unknown>
}

export function useFetch<T>(fn: (...args: unknown[]) => Promise<{ data: T }>): UseFetchReturn<T> {
  const data = ref<T | null>(null) as Ref<T | null>
  const error = ref<string | null>(null)
  const loading = ref(false)

  async function execute(...args: unknown[]) {
    loading.value = true
    error.value = null
    try {
      const result = await fn(...args)
      data.value = result.data
      return result
    } catch (err: unknown) {
      const axiosErr = err as { response?: { data?: { message?: string } }; message?: string }
      error.value = axiosErr.response?.data?.message ?? axiosErr.message ?? 'Unknown error'
      throw err
    } finally {
      loading.value = false
    }
  }

  return { data, error, loading, execute }
}
