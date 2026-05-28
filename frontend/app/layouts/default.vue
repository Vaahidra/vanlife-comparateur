<script setup lang="ts">
import { CATEGORIES } from '~/utils/categories'
const categories = CATEGORIES

const currentYear = new Date().getFullYear()
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <!-- Header -->
    <header class="border-b border-sand-200 bg-sand-50/95 backdrop-blur sticky top-0 z-10">
      <div class="article-container py-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <NuxtLink
          to="/"
          class="font-serif text-2xl font-bold text-anthracite-900 hover:text-sand-700 transition-colors no-underline"
        >
          Vanlife Comparateur
        </NuxtLink>

        <nav class="flex flex-wrap items-center gap-x-5 gap-y-2 text-sm font-medium">
          <NuxtLink
            v-for="cat in categories"
            :key="cat.slug"
            :to="`/categories/${cat.slug}`"
            class="text-anthracite-700 hover:text-sand-700 transition-colors"
          >
            {{ cat.label }}
          </NuxtLink>
          <NuxtLink
            to="/articles"
            class="text-anthracite-700 hover:text-sand-700 transition-colors border-l border-sand-300 pl-5"
          >
            Articles
          </NuxtLink>
          <NuxtLink
            to="/about"
            class="text-anthracite-700 hover:text-sand-700 transition-colors"
          >
            À propos
          </NuxtLink>
        </nav>
      </div>
    </header>

    <!-- Main -->
    <main class="flex-1 article-container py-10 sm:py-16">
      <article class="prose prose-lg max-w-none">
        <slot />
      </article>
    </main>

    <!-- Footer -->
    <footer class="border-t border-sand-200 bg-anthracite-900 text-sand-100">
      <div class="article-container py-10 grid gap-8 md:grid-cols-3 text-sm">
        <div>
          <p class="font-serif text-xl font-bold text-sand-50 mb-3">Vanlife Comparateur</p>
          <p class="text-sand-300 leading-relaxed">
            Comparatifs honnêtes et guides d'achat pour équiper ton fourgon aménagé.
          </p>
        </div>

        <div>
          <p class="font-semibold text-sand-50 mb-3">Catégories</p>
          <ul class="space-y-1.5">
            <li v-for="cat in categories" :key="cat.slug">
              <NuxtLink
                :to="`/categories/${cat.slug}`"
                class="text-sand-300 hover:text-sand-100 transition-colors"
              >
                {{ cat.label }}
              </NuxtLink>
            </li>
          </ul>
        </div>

        <div>
          <p class="font-semibold text-sand-50 mb-3">Le site</p>
          <ul class="space-y-1.5">
            <li>
              <NuxtLink to="/about" class="text-sand-300 hover:text-sand-100 transition-colors">
                À propos
              </NuxtLink>
            </li>
            <li>
              <NuxtLink to="/mentions-legales" class="text-sand-300 hover:text-sand-100 transition-colors">
                Mentions légales
              </NuxtLink>
            </li>
            <li>
              <NuxtLink to="/contact" class="text-sand-300 hover:text-sand-100 transition-colors">
                Contact
              </NuxtLink>
            </li>
          </ul>
        </div>
      </div>

      <div class="border-t border-anthracite-800">
        <div class="article-container py-5 text-xs text-sand-400 text-center">
          <p class="mb-2 italic">
            Certains liens de ce site sont affiliés. Si tu achètes via ces liens, je touche une petite commission
            sans surcoût pour toi. Mention obligatoire ARPP/DGCCRF.
          </p>
          <p>© {{ currentYear }} Vanlife Comparateur — Tous droits réservés</p>
        </div>
      </div>
    </footer>
  </div>
</template>
