// https://nuxt.com/docs/api/configuration/nuxt-config
import tailwindcss from '@tailwindcss/vite'

export default defineNuxtConfig({
  modules: [
    '@nuxt/content',
    '@nuxt/image',
    '@nuxtjs/seo',
  ],

  css: ['~/assets/css/main.css'],

  // Tailwind CSS v4 via Vite plugin (pas de tailwind.config.ts, config dans main.css via @theme)
  vite: {
    plugins: [tailwindcss()],
  },

  // @nuxt/image — domaines externes autorisés (placeholders MVP)
  image: {
    domains: ['picsum.photos', 'images.unsplash.com'],
  },

  devtools: { enabled: true },
  compatibilityDate: '2026-05-27',

  // SEO de base — surcharger l'URL via NUXT_PUBLIC_SITE_URL en prod
  site: {
    url: process.env.NUXT_PUBLIC_SITE_URL || 'http://localhost:3000',
    name: 'Vanlife Comparateur',
    description: 'Comparatifs honnêtes et guides d\'achat pour équiper ton fourgon aménagé.',
    defaultLocale: 'fr',
  },

  // Variables d'environnement exposées
  runtimeConfig: {
    // server-only
    githubToken: '', // NUXT_GITHUB_TOKEN (utilisé par Decap si OAuth proxy)

    public: {
      siteUrl: process.env.NUXT_PUBLIC_SITE_URL || 'http://localhost:3000',
      // Affiliation — auto-injecté par <AmazonCta>, <AwinCta>
      amazonPartnerTag: process.env.NUXT_PUBLIC_AMAZON_PARTNER_TAG || '',
      awinPublisherId: process.env.NUXT_PUBLIC_AWIN_PUBLISHER_ID || '',
    },
  },

  // Content module config (Nuxt Content v3)
  content: {
    build: {
      markdown: {
        toc: { depth: 3, searchDepth: 3 },
      },
    },
  },

  // OG Image — désactivé en MVP (évite la sélection interactive de renderer).
  // Réactiver en Phase 5+ : `enabled: true` + installer satori ou takumi.
  ogImage: {
    enabled: false,
  },

  // Performance & SEO Core Web Vitals
  experimental: {
    payloadExtraction: true,
  },

  // Hébergement : Cloudflare Pages en mode STATIC (nuxt generate)
  // → tous les routes pre-rendered au build, pas besoin de D1 runtime ni nodejs_compat.
  // Compatible CDN pure (CF Pages, GitHub Pages, Netlify, n'importe quoi).
  nitro: {
    preset: 'static',
    prerender: {
      crawlLinks: true,
      failOnError: false,
    },
  },

  app: {
    head: {
      htmlAttrs: { lang: 'fr' },
      meta: [
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'theme-color', content: '#1a1a1a' },
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
      ],
    },
  },
})
