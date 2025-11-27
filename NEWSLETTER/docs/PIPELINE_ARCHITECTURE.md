# 🏗️ AI Newsletter Pipeline Architecture

## 📊 System Overview

```mermaid
graph TB
    subgraph "Phase 1: Channel Classification"
        A[YouTube Subscriptions<br/>238 channels] --> B[Interactive Classification]
        B --> C[newsletter_channels.json<br/>103 selected channels]
    end
    
    subgraph "Phase 2: Video Collection"
        C --> D[YouTube Data API v3]
        D --> E{Quota Check}
        E -->|Available| F[Fetch Videos<br/>Last 7 days]
        E -->|Exceeded| G[Wait/Use Cache]
        F --> H[videos.json<br/>77 videos collected]
    end
    
    subgraph "Phase 3: Video Analysis"
        H --> I{Video Duration}
        I -->|≤15 min| J[Gemini Full Analysis]
        I -->|>15 min| K[Gemini Description Only]
        J --> L[analyzed.json<br/>Structured data]
        K --> L
    end
    
    subgraph "Phase 4: Newsletter Generation"
        L --> M[Group by Type<br/>Person/Company/Community]
        M --> N[Sort by Relevance]
        N --> O[Generate Markdown]
        O --> P[newsletter.md<br/>Final output]
    end
    
    style A fill:#e1f5ff
    style C fill:#c8e6c9
    style H fill:#fff9c4
    style L fill:#ffccbc
    style P fill:#f8bbd0
```

---

## 🔄 Detailed Workflow

### 1️⃣ Channel Classification Pipeline

```mermaid
sequenceDiagram
    participant User
    participant Script as classify_channels_interactive.py
    participant API as YouTube API
    participant File as newsletter_channels.json
    
    User->>Script: Run classification
    Script->>API: Fetch all subscriptions (238)
    API-->>Script: Channel metadata
    Script->>User: Show channel details
    User->>Script: Classify (P/C/CM/N)
    Script->>File: Save classifications
    Note over File: 103 channels selected<br/>53 Persons, 34 Companies, 16 Communities
```

**Input:**
- `all_subscriptions.json` (238 channels)
- User interactive input

**Output:**
- `newsletter_channels.json` (103 channels)
- Classification: Person, Company, Community

**Stats:**
- 👤 53 Persons (51.5%)
- 🏢 34 Companies (33.0%)
- 👥 16 Communities (15.5%)

---

### 2️⃣ Video Collection Pipeline

```mermaid
flowchart TD
    Start([Start Collection]) --> Load[Load newsletter_channels.json]
    Load --> Loop{For each channel}
    
    Loop -->|Next| Check{Quota Available?}
    Check -->|Yes| Fetch[Fetch videos<br/>Last 7 days]
    Check -->|No| Error[Quota Exceeded<br/>Stop & Save]
    
    Fetch --> Parse[Parse video metadata]
    Parse --> Duration[Get video durations<br/>Batch API call]
    Duration --> Classify{Classify by duration}
    
    Classify -->|≤15 min| Short[Mark as SHORT<br/>Full analysis]
    Classify -->|>15 min| Long[Mark as LONG<br/>Description only]
    
    Short --> Store[Store in videos.json]
    Long --> Store
    Store --> Loop
    
    Loop -->|Done| Stats[Calculate statistics]
    Stats --> Save[Save videos.json]
    Save --> End([End])
    Error --> Save
    
    style Start fill:#4caf50,color:#fff
    style End fill:#4caf50,color:#fff
    style Error fill:#f44336,color:#fff
    style Short fill:#2196f3,color:#fff
    style Long fill:#ff9800,color:#fff
```

**API Quota Management:**
```
YouTube Data API v3 Costs:
- search.list: 100 units
- videos.list: 1 unit
- Daily quota: 10,000 units

Max channels per day: ~100 channels
(100 units × 100 channels = 10,000 units)
```

**Current Results:**
- ✅ 9 channels processed
- ✅ 77 videos collected
- ⚠️ Quota exceeded at channel #93

---

### 3️⃣ Video Analysis Pipeline

```mermaid
flowchart LR
    subgraph Input
        V[videos.json<br/>77 videos]
    end
    
    subgraph Processing
        V --> S{Duration?}
        
        S -->|≤15 min<br/>60 videos| FA[Full Analysis]
        S -->|>15 min<br/>17 videos| DA[Description Analysis]
        
        FA --> G1[Gemini 2.5 Flash-Lite]
        DA --> G2[Gemini 2.5 Flash-Lite]
        
        G1 --> R1[Rich Output:<br/>• Summary<br/>• Takeaways<br/>• Tutorial steps<br/>• Topics<br/>• Difficulty<br/>• Audience]
        
        G2 --> R2[Light Output:<br/>• Brief summary<br/>• Main topic<br/>• Audience]
    end
    
    subgraph Output
        R1 --> O[analyzed.json]
        R2 --> O
    end
    
    style FA fill:#4caf50,color:#fff
    style DA fill:#ff9800,color:#fff
    style O fill:#9c27b0,color:#fff
```

**Gemini API Configuration:**
```python
model = "gemini-2.5-flash-lite"
config = {
    "temperature": 0.7,
    "max_output_tokens": 2048,
    "top_p": 0.95,
    "top_k": 40
}
```

**Cost Breakdown (77 videos):**
| Type | Count | Cost/Video | Total |
|------|-------|------------|-------|
| Short (≤15 min) | 60 | $0.01 | $0.60 |
| Long (>15 min) | 17 | $0.001 | $0.017 |
| Newsletter Gen | 1 | $0.0075 | $0.0075 |
| **TOTAL** | **77** | - | **$0.625** |

---

### 4️⃣ Newsletter Generation Pipeline

```mermaid
flowchart TD
    Start([Start Generation]) --> Load[Load analyzed.json]
    
    Load --> Group[Group by Channel Type]
    Group --> P[👤 Persons Section]
    Group --> C[🏢 Companies Section]
    Group --> CM[👥 Communities Section]
    
    P --> Sort1[Sort by:<br/>• Views<br/>• Relevance<br/>• Date]
    C --> Sort2[Sort by:<br/>• Views<br/>• Relevance<br/>• Date]
    CM --> Sort3[Sort by:<br/>• Views<br/>• Relevance<br/>• Date]
    
    Sort1 --> Format1[Format Markdown:<br/>• Title + Link<br/>• Thumbnail<br/>• Summary<br/>• Takeaways]
    Sort2 --> Format2[Format Markdown:<br/>• Title + Link<br/>• Thumbnail<br/>• Summary<br/>• Takeaways]
    Sort3 --> Format3[Format Markdown:<br/>• Title + Link<br/>• Thumbnail<br/>• Summary<br/>• Takeaways]
    
    Format1 --> Merge[Merge Sections]
    Format2 --> Merge
    Format3 --> Merge
    
    Merge --> Header[Add Header:<br/>• Date<br/>• Stats<br/>• TOC]
    Header --> Footer[Add Footer:<br/>• Summary<br/>• Next edition]
    
    Footer --> Save[Save newsletter.md]
    Save --> End([End])
    
    style Start fill:#4caf50,color:#fff
    style End fill:#4caf50,color:#fff
    style P fill:#2196f3,color:#fff
    style C fill:#ff9800,color:#fff
    style CM fill:#9c27b0,color:#fff
```

**Newsletter Structure:**
```markdown
# 🤖 AI Newsletter - Week of Nov 27, 2025

## 📊 This Week's Stats
- 📺 77 videos from 9 channels
- ⏰ 26.5 hours of content
- 🎯 60 short-form (≤15 min)
- 📚 17 long-form (>15 min)

---

## 👤 Content Creators

### AI Engineer (20 videos)
[Video summaries with thumbnails...]

### AICodeKing (7 videos)
[Video summaries with thumbnails...]

---

## 🏢 Companies

### Genspark (18 videos)
[Video summaries with thumbnails...]

---

## 👥 Communities

### Github Awesome (9 videos)
[Video summaries with thumbnails...]

---

## 📈 Trending Topics
- Topic 1
- Topic 2
- Topic 3
```

---

## 🚀 Optimization Strategy (Phase 3)

```mermaid
graph TB
    subgraph "Current State"
        A[103 channels] --> B[Sequential processing]
        B --> C[Quota exceeded at 9%]
    end
    
    subgraph "Optimization 1: Caching"
        D[Channel metadata cache] --> E[24h TTL]
        E --> F[Reduce API calls by 50%]
    end
    
    subgraph "Optimization 2: Prioritization"
        G[Analyze posting frequency] --> H[Sort by activity]
        H --> I[Process top 50 first]
    end
    
    subgraph "Optimization 3: Batch Processing"
        J[Group similar requests] --> K[Batch video.list calls]
        K --> L[50 videos per request]
    end
    
    subgraph "Optimization 4: Multiple Keys"
        M[API Key 1] --> N[10K quota]
        O[API Key 2] --> P[10K quota]
        Q[API Key 3] --> R[10K quota]
        N --> S[Total: 30K quota]
        P --> S
        R --> S
    end
    
    subgraph "Result"
        T[Process all 103 channels] --> U[~886 videos]
        U --> V[Complete newsletter]
    end
    
    style C fill:#f44336,color:#fff
    style F fill:#4caf50,color:#fff
    style S fill:#4caf50,color:#fff
    style V fill:#4caf50,color:#fff
```

### Caching Strategy

```python
# cache/channel_cache.json structure
{
    "channel_id": {
        "metadata": {...},
        "last_video_check": "2025-11-27T18:00:00Z",
        "cached_videos": [...],
        "ttl": 86400  # 24 hours
    }
}
```

**Benefits:**
- ✅ Reduce API calls by 50%
- ✅ Faster subsequent runs
- ✅ Preserve quota for new videos

### Prioritization Algorithm

```python
# Priority score calculation
priority_score = (
    posting_frequency * 0.4 +      # Videos per week
    subscriber_count * 0.3 +        # Channel size
    avg_views * 0.2 +               # Engagement
    recency * 0.1                   # Last upload
)
```

**Top Priority Channels:**
1. AI Engineer (20 videos/week)
2. Genspark (18 videos/week)
3. Inteligencia Artificial para advogados (15 videos/week)

---

## 📈 Performance Metrics

### Current Performance
| Metric | Value |
|--------|-------|
| Channels processed | 9 / 103 (8.7%) |
| Videos collected | 77 |
| API quota used | ~9,300 units |
| Processing time | ~2 minutes |
| Success rate | 100% (until quota) |

### Target Performance (After Optimization)
| Metric | Target |
|--------|--------|
| Channels processed | 103 / 103 (100%) |
| Videos collected | ~886 (estimated) |
| API quota used | ~10,300 units (with cache) |
| Processing time | ~5 minutes |
| Success rate | 95%+ |

---

## 🔧 Technical Stack

```mermaid
graph LR
    subgraph "Data Collection"
        A[YouTube Data API v3] --> B[OAuth 2.0]
        B --> C[Python Scripts]
    end
    
    subgraph "Analysis"
        D[Google Gemini API] --> E[2.5 Flash-Lite]
        E --> F[Structured Output]
    end
    
    subgraph "Storage"
        G[JSON Files] --> H[Local filesystem]
        H --> I[Git versioning]
    end
    
    subgraph "Generation"
        J[Markdown Templates] --> K[Jinja2]
        K --> L[Final Newsletter]
    end
    
    C --> G
    F --> G
    G --> J
    
    style A fill:#ff0000,color:#fff
    style D fill:#4285f4,color:#fff
    style G fill:#ffa000,color:#fff
    style L fill:#4caf50,color:#fff
```

**Dependencies:**
```txt
google-api-python-client==2.108.0
google-generativeai==0.3.1
google-auth-oauthlib==1.2.0
python-dotenv==1.0.0
pandas==2.1.4
yt-dlp==2023.12.30
python-dateutil==2.8.2
```

---

## 📊 Data Flow

```mermaid
sequenceDiagram
    participant U as User
    participant C as Collector
    participant Y as YouTube API
    participant A as Analyzer
    participant G as Gemini API
    participant N as Newsletter Gen
    participant F as File System
    
    U->>C: Start collection
    C->>Y: Fetch videos (last 7 days)
    Y-->>C: Video metadata
    C->>F: Save videos.json
    
    U->>A: Start analysis
    A->>F: Load videos.json
    A->>G: Analyze video (≤15 min)
    G-->>A: Full analysis
    A->>G: Analyze video (>15 min)
    G-->>A: Brief analysis
    A->>F: Save analyzed.json
    
    U->>N: Generate newsletter
    N->>F: Load analyzed.json
    N->>N: Group & format
    N->>F: Save newsletter.md
    N-->>U: Newsletter ready!
```

---

## 🎯 Success Criteria

### Phase 2 (Current - Testing)
- ✅ Analyze 77 collected videos
- ✅ Generate sample newsletter
- ✅ Validate Gemini integration
- ✅ Measure actual costs
- ✅ Identify bottlenecks

### Phase 3 (Next - Optimization)
- ⏳ Implement caching system
- ⏳ Add prioritization logic
- ⏳ Support multiple API keys
- ⏳ Process all 103 channels
- ⏳ Automate weekly runs

### Phase 4 (Future - Production)
- ⏳ Streamlit UI
- ⏳ Email distribution
- ⏳ RSS feed
- ⏳ Analytics dashboard
- ⏳ User preferences

---

## 📝 Notes

**API Quotas:**
- YouTube: 10,000 units/day (resets midnight PST)
- Gemini: 1,500 requests/day (free tier)

**Cost Estimates:**
- Current (77 videos): $0.62
- Full (886 videos): $7.15
- Monthly (4 newsletters): $28.60

**Processing Time:**
- Video collection: ~2 min (with quota)
- Gemini analysis: ~15 min (77 videos)
- Newsletter generation: <1 min

---

*Last updated: Nov 27, 2025*
