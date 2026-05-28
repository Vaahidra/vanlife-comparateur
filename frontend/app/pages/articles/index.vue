<script setup lang="ts">
useSeoMeta({
  title: 'Tous les articles — Vanlife Comparateur',
  description: 'Tous les comparatifs, tests produit et guides d\'achat vanlife.',
})

const { data: articles } = await useAsyncData('all-articles', () =>
  queryCollection('articles')
    .where('draft', '=', false)
    .order('published_at', 'DESC')
    .all(),
)
</script>

<template>
  <div>
    <h1 class="font-serif text-4xl sm:text-5xl font-bold text-anthracite-900 mb-3">
      Tous les articles
    </h1>
    <p class="text-lg text-anthracite-700 mb-10">
      Comparatifs, tests produit et guides d'achat vanlife. Triés du plus récent au plus ancien.
    </p>

    <div v-if="articles && articles.length > 0" class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      <ArticleCard
        v-for="article in articles"
        :key="article.path"
        :article="article as any"
      />
    </div>

    <EmptyState v-else />
  </div>
</template>
