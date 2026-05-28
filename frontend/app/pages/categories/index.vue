<script setup lang="ts">
import { CATEGORIES } from '~/utils/categories'

useSeoMeta({
  title: 'Catégories — Vanlife Comparateur',
  description: 'Toutes les catégories de matériel vanlife : énergie, cuisine, confort, sécurité, aménagement.',
})

const { data: articles } = await useAsyncData('all-articles-for-cats', () =>
  queryCollection('articles').where('draft', '=', false).all(),
)

const articlesCountByCategory = computed(() => {
  const counts: Record<string, number> = {}
  for (const cat of CATEGORIES) counts[cat.slug] = 0
  for (const article of (articles.value || [])) {
    if (article.category && counts[article.category] !== undefined) {
      counts[article.category]++
    }
  }
  return counts
})
</script>

<template>
  <div>
    <h1 class="font-serif text-4xl sm:text-5xl font-bold text-anthracite-900 mb-3">
      Catégories
    </h1>
    <p class="text-lg text-anthracite-700 mb-10">
      Tous les comparatifs et guides d'achat, regroupés par usage vanlife.
    </p>

    <div class="grid gap-5 md:grid-cols-2 lg:grid-cols-3">
      <CategoryCard
        v-for="cat in CATEGORIES"
        :key="cat.slug"
        :slug="cat.slug"
        :label="cat.label"
        :description="cat.description"
        :articles-count="articlesCountByCategory[cat.slug]"
      />
    </div>
  </div>
</template>
