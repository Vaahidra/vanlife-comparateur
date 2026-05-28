# 📊 STATUS Vanlife Comparateur

> Dernière mise à jour : 2026-05-28
> Lis ce fichier en 5 minutes pour savoir où on en est.

---

## 🎯 C'est quoi ce projet ?

Site de **comparaison + affiliation matériel vanlife** (batteries, panneaux solaires, frigos 12V, chauffages, etc.). Le but : générer des revenus passifs via Amazon Partenaires + Awin + AdSense en publiant des comparatifs honnêtes.

**Stack** : Nuxt 4 (frontend) déployé sur Vercel + pipeline Python qui génère les articles via Gemini IA.

**Marché** : vanlife FR en croissance forte. Panier moyen 200-2000€. Audience CSP+ qui achète.

---

## ✅ Ce qui marche aujourd'hui

| Truc | Status | Détail |
|------|--------|--------|
| 🌐 Site live | ✅ | https://frontend-delta-nine-55.vercel.app |
| 📦 GitHub repo | ✅ | https://github.com/Vaahidra/vanlife-comparateur (public) |
| ☁️ Vercel deploy | ✅ | Premier deploy fait. Build OK. |
| 🎨 Design | ✅ | Palette vanlife (sable + anthracite + serif Crimson Pro). Header/footer/grid catégories. |
| 📝 Articles test | ✅ | 7 articles (6 manuels + 1 IA généré en draft) |
| 🤖 Pipeline IA | ✅ | Gemini 2.5 Flash structured output. 2500-3000 mots/article. |
| ✔️ Quality checks | ✅ | Longueur, H2, FAQ, markers IA, **anti-anecdote EEAT** |
| 🖼️ Image handler | ✅ Code | Pexels API ready (besoin clé pour activer) |
| 🛒 Affiliation Amazon | ✅ Code | Composant AmazonCta + runtimeConfig. Besoin tag pour activer. |
| 📜 Pages légales | ✅ | mentions, contact, RGPD, politique affiliation |

---

## ⏳ Ce qui reste (priorité)

### 🔴 URGENT (toi, pas moi) — débloque les revenus

1. **Désactiver Vercel Authentication**
   - URL: https://vercel.com/vaahidras-projects/vanlife-comparateur/settings/deployment-protection
   - Mettre "Disabled" + Save
   - **Sans ça**: Googlebot bloqué = site jamais indexé = jamais de visiteur = 0€

2. **Connecter GitHub → Vercel** (auto-deploy sur git push)
   - URL: https://vercel.com/vaahidras-projects/vanlife-comparateur/settings/git
   - "Connect Git Repository" → `Vaahidra/vanlife-comparateur`
   - Settings → General → Root Directory = `frontend`
   - **Sans ça**: tu dois deploy manuellement à chaque article

3. **S'inscrire Amazon Partenaires France**
   - URL: https://partenaires.amazon.fr
   - Récupérer ton `partner_tag` (format `xxx-21`)
   - Le mettre dans Vercel: Settings → Environment Variables → `NUXT_PUBLIC_AMAZON_PARTNER_TAG`
   - **Sans ça**: liens vers Amazon = pas de commission

### 🟠 IMPORTANT (toi, 5 min) — débloque vraies photos

4. **Pexels API key** (gratuit, 20k req/mois)
   - URL: https://www.pexels.com/api/
   - Paste-moi la clé ou l'ajouter à `pipeline/.env`
   - **Sans ça**: articles auto-générés ont SVG placeholder au lieu de vraies photos vanlife

### 🟢 OPTIONNEL (je code, toi rien)

| Phase | Effort | Impact |
|-------|--------|--------|
| 8 — Scheduler cron | 30 min | Pipeline run auto 2x/sem. Plus rien à faire. |
| 9 — SEO indexation | 1h | Sitemap submit Google Search Console + Indexing API + GA4 |
| 10 — Monitoring | 1h | Dashboard Telegram revenus + trafic |
| migrate google.genai | 15 min | Sort deprecation warning |

---

## 🚀 Comment utiliser la pipeline

### Générer 1 article IA

```bash
cd /Users/vaahidra/vanlife-comparateur/pipeline
.venv/bin/python pipeline.py --count 1
```

→ Pop topic queue → Gemini → quality check → `.md` écrit dans `frontend/content/articles/{slug}.md` en draft.

### Relire + publier

```bash
# Édite le fichier .md, corrige ce qui te plaît pas
# Quand prêt:
sed -i '' 's/^draft: true/draft: false/' frontend/content/articles/SLUG.md
git add . && git commit -m "publish: SLUG" && git push
# Si Vercel connecté à GitHub → deploy auto en ~2 min
```

### Sujet ad-hoc

```bash
.venv/bin/python pipeline.py --keyword "test webasto airtop 2000" --type test_produit --category confort
```

### Re-seed la queue

```bash
.venv/bin/python pipeline.py --seed   # ajoute 10 topics si queue vide
```

---

## 🧰 Cheatsheet commands

```bash
# Dev server frontend (vois le site en local)
cd frontend && npm run dev          # http://localhost:3000

# Tests Python pipeline
cd pipeline && .venv/bin/python -m pytest tests/ -v

# Status Git + push
git status && git push

# Voir les Vercel deployments
cd frontend && vercel ls --prod
```

---

## 💰 Quand argent commence à rentrer ?

Honnête réaliste :

| Mois | Articles publiés | Trafic | Revenu |
|------|------------------|--------|--------|
| 1-2 | 5-10 | < 200 visites/mois | **0€** (Google pas encore indexé) |
| 3 | 15 | 500-1000 | 5-20€ (premières commissions test) |
| 6 | 30 | 3000-8000 | 50-200€ |
| 9 | 50 | 8000-20000 | 200-800€ |
| 12 | 70+ | 15000-50000 | **500-3000€/mois** (objectif réaliste) |

**Ce qui peut tuer ce chiffre** :
- Pas publier régulièrement (2 articles/sem minimum, sinon Google déclasse)
- Pas relire les articles IA (anecdotes inventées, infos fausses = pénalité EEAT)
- Pas désactiver Vercel Protection (Googlebot bloqué = 0 indexation)
- Pas s'inscrire Amazon (liens = pas de commission)

**Ce qui peut booster** :
- Acheter 2-3 produits pour photos réelles + tests vrais (boost EEAT massif)
- Réseaux sociaux (Instagram vanlife, TikTok = trafic complémentaire)
- Newsletter (~mois 6, vidéos YouTube ~mois 9-12)

---

## 📎 Liens importants

| Truc | URL |
|------|-----|
| Site live | https://frontend-delta-nine-55.vercel.app |
| GitHub repo | https://github.com/Vaahidra/vanlife-comparateur |
| Vercel dashboard | https://vercel.com/vaahidras-projects/vanlife-comparateur |
| Setup affiliation guide | [SETUP_PHASE6_AFFILIATION.md](./SETUP_PHASE6_AFFILIATION.md) |
| Article exemple IA | frontend/content/articles/convertisseur-pur-sinus-12v-220v-vanlife-comparatif.md |

---

## 🗂️ Architecture rapide

```
vanlife-comparateur/
├── frontend/                       # Nuxt 4 app (déployé Vercel)
│   ├── app/
│   │   ├── pages/                  # index, /about, /articles, /categories, etc.
│   │   ├── layouts/default.vue     # header + footer
│   │   ├── components/             # ArticleCard, AmazonCta, PlaceholderImage, ...
│   │   └── assets/css/main.css     # Tailwind v4 + thème vanlife
│   ├── content/articles/           # 7 articles .md (édités à la main OU générés)
│   ├── public/admin/               # Decap CMS UI
│   └── nuxt.config.ts
│
├── pipeline/                       # Python automation (run en local pour l'instant)
│   ├── modules/
│   │   ├── content_writer.py       # Appel Gemini → article structuré
│   │   ├── image_handler.py        # Pexels search + download
│   │   ├── quality_check.py        # Checks longueur/H2/anecdotes EEAT
│   │   ├── nuxt_publisher.py       # .md + frontmatter YAML
│   │   ├── topics.py               # Queue management
│   │   ├── affiliate_linker.py     # Amazon + Awin links
│   │   └── notify.py               # Telegram notifs
│   ├── pipeline.py                 # Orchestration CLI
│   ├── data/
│   │   ├── topics_queue.json       # 8 topics en attente
│   │   └── topics_done.json        # 2 topics traités
│   ├── .env                        # Secrets (gitignored, GEMINI_API_KEY dedans)
│   └── requirements.txt
│
├── README.md
├── SETUP_PHASE6_AFFILIATION.md     # Guide inscription Amazon/Awin/AdSense
└── STATUS.md                       # Tu lis là
```

---

## 🤔 TL;DR

**Si t'as 15 min** : fais les 3 actions 🔴 URGENT ci-dessus.

**Si t'as 5 min** : fais l'action #4 Pexels.

**Si t'as rien à faire** : me dire "phase 8" et je continue à coder.

**Si t'as plein de temps** : fais 🔴 + 🟠 + paste-moi les clés, je termine Phase 5 + génère 3 articles bout en bout + push pour validation visuelle.
