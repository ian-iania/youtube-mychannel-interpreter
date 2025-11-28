# 🤖 AI Newsletter Generator

> Automated newsletter generation from YouTube AI content using Google Gemini 2.5 Flash-Lite

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![Phase](https://img.shields.io/badge/phase-2%20testing-blue.svg)]()
[![Channels](https://img.shields.io/badge/channels-103-brightgreen.svg)]()
[![Videos](https://img.shields.io/badge/videos-77%20collected-yellow.svg)]()

---

## 📋 Overview

This project automatically generates a curated AI newsletter by:
1. ✅ **Monitoring** 103 selected YouTube channels (53 Persons, 34 Companies, 16 Communities)
2. ✅ **Collecting** recent videos (last 7 days)
3. 🚧 **Analyzing** content with Google Gemini 2.5 Flash-Lite
4. 🚧 **Generating** structured summaries and takeaways
5. 🚧 **Creating** a beautiful Markdown newsletter

---

## 🎯 Current Status

### ✅ Phase 1: Channel Classification (Complete)
- **103 channels** classified from 238 subscriptions
- **Interactive classification** tool with terminal UI
- **Distribution:** 53 Persons | 34 Companies | 16 Communities

### ✅ Phase 2: Video Collection (Partial - Quota Limited)
- **9 channels** processed before quota exceeded
- **77 videos** collected (last 7 days)
- **26.5 hours** of content
- **Top channel:** AI Engineer (20 videos in 7 days!)

### 🚧 Phase 3: Video Analysis (In Progress)
- Testing Gemini API integration
- Analyzing 77 collected videos
- Generating sample newsletter

### 📅 Phase 4: Optimization (Planned)
- Implement caching system
- Add prioritization logic
- Support multiple API keys
- Process all 103 channels

---

## 📚 Documentation

### 📖 Core Documentation
- **[Pipeline Architecture](docs/PIPELINE_ARCHITECTURE.md)** - Complete system overview with Mermaid diagrams
- **[Phase 2 Implementation](docs/PHASE2_IMPLEMENTATION.md)** - Testing guide for video analysis
- **[Phase 3 Optimization](docs/PHASE3_OPTIMIZATION.md)** - Scaling strategies and optimizations
- **[Gemini Setup](docs/GEMINI_SETUP.md)** - Google Gemini API configuration

### 🎨 Visual Guides
All documentation includes beautiful Mermaid charts:
- System architecture flowcharts
- API call sequences
- Data flow diagrams
- Optimization strategies

---

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Clone repository
cd NEWSLETTER

# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env with your keys:
# - YOUTUBE_API_KEY
# - GEMINI_API_KEY
```

### 2. Classify Channels (Already Done!)

```bash
# Interactive classification (already completed)
python3 scripts/classify_channels_interactive.py

# Result: 103 channels selected
# - 53 Persons
# - 34 Companies  
# - 16 Communities
```

### 3. Collect Videos

```bash
# Collect videos from last 7 days
python3 scripts/collect_videos.py --days 7

# Note: YouTube API quota = 10,000 units/day
# Can process ~100 channels per day
```

### 4. Analyze with Gemini

```bash
# Analyze collected videos
python3 scripts/analyze_videos.py --input newsletters/2025-11-27_videos.json

# Output: newsletters/2025-11-27_analyzed.json
```

### 5. Generate Newsletter

```bash
# Generate Markdown newsletter
python3 scripts/generate_newsletter.py --input newsletters/2025-11-27_analyzed.json

# Output: newsletters/2025-11-27_newsletter.md
```

---

## 📊 Current Results

### Top 10 Channels by Posting Frequency (7 days)

| Rank | Channel | Type | Videos | Videos/Day |
|------|---------|------|--------|------------|
| 1 | AI Engineer | 👤 Person | 20 | 2.9 |
| 2 | Genspark | 🏢 Company | 18 | 2.6 |
| 3 | Inteligencia Artificial para advogados | 👤 Person | 15 | 2.1 |
| 4 | Github Awesome | 👥 Community | 9 | 1.3 |
| 5 | AICodeKing | 👤 Person | 7 | 1.0 |
| 6 | AI LABS | 👥 Community | 4 | 0.6 |
| 7 | Code with Ania Kubów | 👤 Person | 2 | 0.3 |
| 8 | 3Blue1Brown | 👤 Person | 1 | 0.1 |
| 9 | AI and Tech for Education | 👤 Person | 1 | 0.1 |

### Statistics

- 📺 **9 channels** processed (quota limited)
- 🎬 **77 videos** collected
- ✅ **60 short videos** (≤15 min) - 77.9%
- ⏱️ **17 long videos** (>15 min) - 22.1%
- ⏰ **26.5 hours** total content
- 📊 **8.6 videos** per channel average

---

## 💰 Cost Analysis

### Google Gemini 2.5 Flash-Lite vs OpenAI

| Solution | Process | Cost (50 videos) |
|----------|---------|------------------|
| **OpenAI** | Whisper (500 min) + GPT-4o-mini | **$3.15** |
| **Gemini Flash** | Direct video analysis | **$0.50** |
| **Gemini Flash-Lite** | Direct video analysis | **$0.37** |

**Savings: 88% with Gemini Flash-Lite!**

### Current Collection (77 videos)

| Component | Count | Cost |
|-----------|-------|------|
| Short videos (≤15 min) | 60 | $0.60 |
| Long videos (>15 min) | 17 | $0.017 |
| Newsletter generation | 1 | $0.0075 |
| **Total** | **77** | **$0.625** |

### Full Newsletter (103 channels, ~886 videos)

- **Estimated cost:** $7.15 per newsletter
- **Monthly (4 newsletters):** $28.60
- **Annual (52 newsletters):** $371.80

---

## 🏗️ Architecture

```
NEWSLETTER/
├── docs/                           # Documentation
│   ├── PIPELINE_ARCHITECTURE.md    # System overview + Mermaid
│   ├── PHASE2_IMPLEMENTATION.md    # Testing guide
│   ├── PHASE3_OPTIMIZATION.md      # Optimization strategies
│   └── GEMINI_SETUP.md             # API setup
│
├── scripts/                        # Python scripts
│   ├── classify_channels_interactive.py  # ✅ Channel classification
│   ├── collect_videos.py                 # ✅ Video collection
│   ├── analyze_videos.py                 # 🚧 Gemini analysis
│   ├── generate_newsletter.py            # 🚧 Markdown generation
│   ├── export_all_subscriptions.py       # Helper: export all subs
│   ├── get_channel_ids.py                # Helper: URL to ID
│   └── process_classification.py         # Helper: process manual classification
│
├── newsletters/                    # Generated newsletters
│   ├── 2025-11-27_videos.json      # Raw video data
│   ├── 2025-11-27_analyzed.json    # Analysis results
│   └── 2025-11-27_newsletter.md    # Final newsletter
│
├── cache/                          # API cache (Phase 3)
│   └── channel_cache.json
│
├── all_subscriptions.json          # All 238 subscriptions
├── newsletter_channels.json        # 103 selected channels
├── channels_to_classify.txt        # Classification working file
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

---

## 🔧 Technical Stack

- **YouTube Data API v3** - Video collection
- **Google Gemini 2.5 Flash-Lite** - Video analysis
- **OAuth 2.0** - Authentication
- **Python 3.9+** - Core language
- **JSON** - Data storage
- **Markdown** - Newsletter format

---

## 📈 Roadmap

### Phase 1: Channel Classification ✅
- [x] Export all subscriptions (238 channels)
- [x] Interactive classification tool
- [x] Select 103 channels for newsletter

### Phase 2: Video Collection ✅ (Partial)
- [x] Collect videos from selected channels
- [x] Fetch video metadata (duration, views, likes)
- [x] Categorize by duration (short/long)
- [ ] Complete collection (quota limited to 9 channels)

### Phase 3: Video Analysis 🚧
- [ ] Integrate Gemini API
- [ ] Analyze short videos (≤15 min) - Full analysis
- [ ] Analyze long videos (>15 min) - Description only
- [ ] Generate structured output (JSON)
- [ ] Test with 77 collected videos

### Phase 4: Newsletter Generation 🚧
- [ ] Group videos by channel type
- [ ] Sort by relevance
- [ ] Generate Markdown with thumbnails
- [ ] Add statistics and trending topics
- [ ] Export final newsletter

### Phase 5: Optimization 📅
- [ ] Implement caching system (50% API reduction)
- [ ] Add prioritization logic (top 50 channels first)
- [ ] Batch API requests (98% fewer calls)
- [ ] Support multiple API keys (3x quota)
- [ ] Process all 103 channels

### Phase 6: Automation 📅
- [ ] Weekly cron job
- [ ] Email distribution
- [ ] RSS feed
- [ ] Error notifications
- [ ] Analytics dashboard

### Phase 7: UI Development 📅
- [ ] Streamlit dashboard
- [ ] Interactive filters
- [ ] Export options
- [ ] User preferences
- [ ] Channel management

---

## 🐛 Known Issues

### YouTube API Quota Limitation
**Issue:** Quota exceeded after processing 9 channels

**Current:** 10,000 units/day = ~100 channels

**Solutions:**
1. ✅ Wait for daily quota reset (midnight PST)
2. ✅ Implement caching (Phase 3)
3. ✅ Use multiple API keys
4. ✅ Prioritize high-activity channels

### Missing Video Durations
**Issue:** Some videos return empty duration

**Solution:** Implemented safe fallback to 'PT0S'

---

## 🤝 Contributing

This is a personal project, but suggestions are welcome!

---

## 📝 License

MIT License - Feel free to use and modify

---

## 🙏 Acknowledgments

- **YouTube Data API** for video metadata
- **Google Gemini** for AI-powered analysis
- **103 amazing AI channels** for the content

---

## 📞 Contact

For questions or feedback, open an issue on GitHub.

---

*Last updated: November 27, 2025*
*Status: Phase 2 - Testing video analysis with 77 collected videos*
