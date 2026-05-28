<script setup lang="ts">
import { CATEGORIES } from '~/utils/categories'

useSeoMeta({
  title: 'Vanlife Comparateur — Matériel fourgon aménagé sans bullshit',
  description: 'Comparatifs honnêtes et guides d\'achat pour équiper ton fourgon aménagé : batteries, panneaux solaires, frigos 12V, chauffages, douches.',
  ogTitle: 'Vanlife Comparateur',
  ogDescription: 'Comparatifs honnêtes pour équiper ton fourgon.',
  ogType: 'website',
})

// Articles publiés non-brouillon, par catégorie
const { data: articles } = await useAsyncData('home-articles', () =>
  queryCollection('articles')
    .where('draft', '=', false)
    .order('published_at', 'DESC')
    .all(),
)

// Compte articles par catégorie
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

const featuredArticles = computed(() => (articles.value || []).slice(0, 3))
</script>

<template>
  <div>
    <HeroSection
      title="Vanlife Comparateur"
      subtitle="Le matos vanlife passé au crible"
      intro="Tu prépares ton fourgon ? Tu cherches la bonne batterie, le bon panneau solaire, le bon frigo 12V sans te ruiner et sans te faire avoir par le marketing ? Ici on compare pour de vrai. Specs, prix, défauts inclus."
    />

    <AffiliateBanner />

    <!-- Articles featured -->
    <section v-if="featuredArticles.length > 0" class="my-16">
      <div class="flex items-baseline justify-between mb-6">
        <h2 class="font-serif text-3xl font-bold text-anthracite-900">Derniers comparatifs</h2>
        <NuxtLink to="/articles" class="text-sm text-sand-700 hover:text-sand-900 underline">
          Voir tous les articles →
        </NuxtLink>
      </div>
      <div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <ArticleCard
          v-for="article in featuredArticles"
          :key="article.path"
          :article="article as any"
        />
      </div>
    </section>

    <!-- Catégories -->
    <section class="my-16">
      <h2 class="font-serif text-3xl font-bold text-anthracite-900 mb-2">Par catégorie</h2>
      <p class="text-anthracite-700 mb-8">Choisis ce que tu cherches.</p>
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
    </section>

    <!-- À propos en bref -->
    <section class="my-16 p-8 bg-sand-100 rounded-lg border border-sand-200">
      <h2 class="font-serif text-2xl font-bold text-anthracite-900 mb-3">Pourquoi ce site ?</h2>
      <p class="text-anthracite-700 leading-relaxed mb-4">
        Je prépare mon propre projet d'aménagement de fourgon. Avant de claquer des milliers d'euros en matériel,
        j'ai voulu vraiment comparer ce qui existe — sans me contenter des comparatifs sponsorisés qui pullulent.
        Ce blog, c'est le résultat de mes recherches : specs croisées, prix réels, défauts assumés.
      </p>
      <NuxtLink to="/about" class="inline-block text-sm font-medium text-sand-700 hover:text-sand-900 underline">
        En savoir plus sur moi →
      </NuxtLink>
    </section>
  </div>
</template>
