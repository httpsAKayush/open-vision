Structure
```
backend/
│
├── manage.py
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   ├── wsgi.py
│   └── celery.py
│
├── apps/
│   │
│   ├── users/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── services.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── tests.py
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── services.py
│   │   ├── analyzers.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── tests.py
│   │
│   ├── issues/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── services.py
│   │   ├── difficulty_engine.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── tests.py
│   │
│   ├── matching/
│   │   ├── __init__.py
│   │   ├── matching_engine.py
│   │   ├── growth_engine.py
│   │   ├── services.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests.py
│   │
│   └── embeddings/
│       ├── __init__.py
│       ├── embedding_service.py
│       ├── vector_store.py
│       ├── model_registry.py
│       └── tests.py
│
├── requirements.txt
└── Dockerfile


frontend/
│
├── app/
│   ├── page.tsx
│   │
│   ├── dashboard/
│   │   └── page.tsx
│   │
│   ├── recommend/
│   │   └── page.tsx
│   │
│   ├── progress/
│   │   └── page.tsx
│   │
│   └── submit/
│       └── page.tsx
│
├── components/
│   ├── SkillLevelMeter.tsx
│   ├── DomainRadarChart.tsx
│   ├── RepoRecommendationCard.tsx
│   ├── IssueRecommendationCard.tsx
│   ├── ProgressTimelineChart.tsx
│   └── DifficultyBadge.tsx
│
├── lib/
│   └── api.ts
│
├── styles/
│   └── globals.css
│
├── package.json
└── tailwind.config.ts
```


```
What It Still Needs To Be Elite

To reach top-tier level:

Real model evaluation metrics

Ablation testing

Drift detection

Cold-start handling strategy

Scalable embedding storage (FAISS, Pinecone, etc.)

API rate-limit resilience

Logging + monitoring layer

Offline evaluation benchmarks

Add these and this becomes research-level.
```


# LAYER!: user profiling 
```
apps/users/models.py        → UserProfile model
apps/users/services.py      → GitHub API fetcher
apps/users/serializers.py   → DRF serializer
apps/users/views.py         → API endpoint
apps/users/urls.py          → URL routing
config/urls.py              → Wire it in
```

# LAYER2: repository intelligence


# LAYER3: Issue difficulty engine


