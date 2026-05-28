# Vanlife Comparateur

Site de comparaison/affiliation pour matériel vanlife (batteries, panneaux solaires, frigos 12V, etc.).
Monétisation : Amazon Partenaires + Awin + AdSense.

## Stack

- **Frontend** : Nuxt 3 + `@nuxt/content` (articles Markdown) + Decap CMS (admin web)
- **Hébergement** : Vercel (Hobby gratuit, `.vercel.app` en MVP)
- **Pipeline** : Python 3.11 + Gemini 2.5 Flash (génération) + Groq Llama 3.3 (fallback)
- **Publication** : `.md` push vers git → rebuild Vercel automatique

## Arborescence

```
vanlife-comparateur/
├── frontend/               # Nuxt 3 app
│   ├── content/articles/   # articles .md
│   └── public/admin/       # Decap CMS UI
├── pipeline/               # Python orchestration
│   ├── modules/            # scripts métier
│   ├── data/               # queue topics, db produits
│   └── outputs/            # articles générés avant push
└── .gitignore
```

## Setup local

### 1. Pipeline Python

```bash
cd pipeline
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# remplir .env avec les clés API
python config.py  # valide que les clés sont présentes
```

### 2. Frontend Nuxt

```bash
cd frontend
npm install
npm run dev          # http://localhost:3000
```

### 3. Decap CMS (admin)

Accessible sur `http://localhost:3000/admin/` après `npm run dev`.
Auth : GitHub OAuth (à configurer en Phase 1).

## Phases du projet

- [x] **Phase 0** : Setup environnement (scaffold)
- [ ] **Phase 1** : Setup Vercel + GitHub + Decap auth
- [ ] **Phase 2** : Recherche mots-clés + topics_queue.json
- [ ] **Phase 3** : Recherche produits + specs (products_db.json)
- [ ] **Phase 4** : Génération articles IA
- [ ] **Phase 5** : Images & médias
- [ ] **Phase 6** : Affiliation (Amazon Partenaires, Awin, AdSense)
- [ ] **Phase 7** : Publication automatique (push git)
- [ ] **Phase 8** : Scheduler production (2 articles/sem)
- [ ] **Phase 9** : SEO on-page & technique
- [ ] **Phase 10** : Monitoring & itération

## Cadre légal & qualité

- Tous liens affiliés en `rel="sponsored nofollow"`
- Mention transparence visible sur chaque article comparatif
- Bio auteur honnête (pas de persona fictif "expert")
- Relecture humaine OBLIGATOIRE avant publication (anti-désindexation Google)
- Déclaration revenus en micro-BNC ou micro-BIC dès le 1er euro

## TODO migration domaine

- [ ] Acheter `.fr` dédié dès 1er revenu (subdomain wr-consulting.fr déconseillé pour SEO/brand/fiscal)
