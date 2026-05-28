import { defineContentConfig, defineCollection, z } from '@nuxt/content'

export default defineContentConfig({
  collections: {
    // Pages statiques (about, mentions légales, etc.)
    pages: defineCollection({
      type: 'page',
      source: {
        include: '**/*.md',
        exclude: ['articles/**'],
      },
    }),

    // Articles (générés par le pipeline Python)
    articles: defineCollection({
      type: 'page',
      source: 'articles/**/*.md',
      schema: z.object({
        title: z.string(),
        description: z.string(),
        slug: z.string().optional(),
        type: z.enum(['comparatif', 'test_produit', 'guide_achat']).optional(),
        category: z.string().optional(),
        keyword_focus: z.string().optional(),
        draft: z.boolean().default(false),
        author: z.string().optional(),
        published_at: z.string().optional(),
        updated_at: z.string().optional(),
        featured_image: z.string().optional(),
        products_compared: z.array(z.string()).optional(),
        product_tested: z.string().optional(),
        schema: z.object({
          type: z.string(),
        }).optional(),
      }),
    }),
  },
})
