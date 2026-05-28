<script setup lang="ts">
interface Props {
  slug: string
  label: string
  description: string
  articlesCount?: number
}
defineProps<Props>()
</script>

<template>
  <NuxtLink
    :to="`/categories/${slug}`"
    class="group block p-6 bg-white border border-sand-200 rounded-lg hover:border-sand-400 hover:shadow-md transition-all no-underline"
  >
    <h3 class="font-serif text-2xl font-bold text-anthracite-900 mb-2 group-hover:text-sand-800 transition-colors">
      {{ label }}
    </h3>
    <p class="text-sm text-anthracite-700 leading-relaxed mb-3">
      {{ description }}
    </p>
    <p class="text-xs text-anthracite-500 font-medium">
      <span v-if="articlesCount && articlesCount > 0">
        {{ articlesCount }} article{{ articlesCount > 1 ? 's' : '' }}
      </span>
      <span v-else class="italic">Bientôt disponible</span>
      <span class="ml-1 group-hover:translate-x-1 inline-block transition-transform">→</span>
    </p>
  </NuxtLink>
</template>
