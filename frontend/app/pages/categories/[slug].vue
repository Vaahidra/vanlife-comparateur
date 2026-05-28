<script setup lang="ts">
import { CATEGORIES, getCategoryBySlug } from '~/utils/categories'

const route = useRoute()
const slug = computed(() => String(route.params.slug))

const category = computed(() => getCategoryBySlug(slug.value))

// 404 si catégorie inconnue
if (!category.value) {
  throw createError({ statusCode: 404, statusMessage: 'Catégorie introuvable', fatal: true })
}

const { data: articles } = await useAsyncData(
  `articles-cat-${slug.value}`,
  () => queryCollection('articles')
    .where('category', '=', slug.value)
    .where('draft', '=', false)
    .order('published_at', 'DESC')
    .all(),
)

useSeoMeta({
  title: () => `${category.value!.label} — Comparatifs vanlife`,
  description: () => category.value!.description,
})
</script>

<template>
  <div v-if="category">
    <NuxtLink to="/categories" class="text-sm text-sand-700 hover:text-sand-900 underline mb-4 inline-block">
      ← Toutes les catégories
    </NuxtLink>

    <h1 class="font-serif text-4xl sm:text-5xl font-bold text-anthracite-900 mb-3">
      {{ category.label }}
    </h1>
    <p class="text-lg text-anthracite-700 mb-10 max-w-2xl">
      {{ category.description }}
    </p>

    <div v-if="articles && articles.length > 0" class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      <ArticleCard
        v-for="article in articles"
        :key="article.path"
        :article="article as any"
      />
    </div>

    <EmptyState
      v-else
      :title="`Aucun article ${category.label.toLowerCase()} pour l'instant`"
      message="Les premiers comparatifs de cette catégorie arrivent bientôt. En attendant, explore les autres catégories."
    />
  </div>
</template>
