# Krititva (कृतित्व)

> **"Architecting Value. Operationalizing Expertise."**  
> *A platform which helps vendors, side hustlers, service providers, art craftables sellers etc to have a platform (their own profile where they can list out their business) instead of building their own website at initial phase of their business.*

[![GitHub Repository](https://img.shields.io/badge/GitHub-Krititva--brightgreen?logo=github)](https://github.com/icyboei/Krititva-)
[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Framework-Flask_3.1-orange.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-22%20Passed-success)](tests/)

---

## 🌟 The Vision & Core Problem

At the initial phase of launching a craft, baking, pottery, bespoke leather, or freelance service business, makers and side-hustlers face a massive barrier: **building, paying for, and maintaining a custom website**.

Between domain registrations, monthly hosting fees, complex CMS setups (Shopify, WordPress, Webflow), and fragile plugin stacks, creators waste weeks and tens of thousands of rupees before making their first sale.

**Krititva replaces that friction with an instant, branded digital storefront:**
- **Zero Website Overhead:** Launch a public business profile in under 60 seconds at `krititva.com/profile/<your-handle>`.
- **List Activities with Appropriate Charges:** Showcase handcrafted items, studio workshops, hourly consultations, or services with clear pricing models (`₹ Fixed`, `₹/hr`, `Session rates`).
- **Interactive Review & 5-Star Rating System:** Clients can leave verified feedback, rate providers from 1 to 5 stars, and build genuine bilateral social proof.
- **Direct Patron Inquiries & WhatsApp:** Receive customer orders, custom commission requests, and direct chat messages with zero commission deductions.
- **Private Studio Management Hub (`/dashboard`):** Track storefront views, active offerings, customer leads, and client reviews in one intuitive portal.

---

## 🎨 Theme & Brand Aesthetics

Krititva's visual language directly reflects its handcrafted emblem logo (`static/images/krititva-emblem.jpg`):
- **Earthy Terracotta Rust (`#AD4F32`, `#964027`)** — Representing raw clay, tactile craftsmanship, and grounded warmth.
- **Burnished Copper & Honey Sand (`#B77A3D`, `#C99B5B`)** — Evoking golden metallic finishes, artisanal wax, and natural leather.
- **Handmade Ivory Linen (`#FAF6EF`, `#F2E8D8`)** — Organic, paper-textured backgrounds inspired by handmade Indian parchment.
- **Deep Warm Espresso (`#382318`)** — Legible, authoritative typography with editorial serifs (*Cormorant Garamond*), modern sans-serifs (*Plus Jakarta Sans*), and Devanagari calligraphy (*कृतित्व*).

---

## 🚀 Key Features

### 1. Dedicated Vendor Micro-Storefronts (`/profile/<username>`)
Each maker receives a personalized public profile:
- Studio banner, creator bio, verified badge, location, and response times.
- Catalog of listed activities & craftables with clear charges and turnaround times.
- 1-Click "Share Storefront" button that copies the clean URL to the clipboard.
- Direct "Chat on WhatsApp" and custom inquiry modals.

### 2. Client Review & 5-Star Rating System
- Interactive rating widget with 1 to 5 clickable gold stars and descriptive ratings.
- Real-time recalculation of aggregate scores and star breakdown meters (5★ to 1★).
- Verified client badges for authentic customer feedback.

### 3. Vendor Studio Dashboard (`/dashboard`)
- Real-time counters for Active Listings, Average Star Rating, Reviews, and Inquiries.
- Listing management with status indicators and "+ List New Activity" modal.
- Inbox for customer commission requests and direct inquiries.

### 4. Interactive Auth & 1-Click Demo Personas
- Flexible registration with dual roles: **Vendor / Maker** or **Client / Patron**.
- Instant 1-click persona switcher in the navigation bar to test the platform as:
  - 🏺 **Maya Sharma (`maya-ceramics`)** — *Mitti & Clay Studio (Pottery & Ceramics)*
  - 👜 **Rohan Mehra (`rohan-leather`)** — *Heritage Tannery & Goods (Bespoke Leather)*
  - 🥐 **Chef Ananya Rao (`ananya-bakes`)** — *The Sourdough Loft (Artisanal Breads & Babkas)*
  - 📐 **Kabir Sen (`kabir-visuals`)** — *Studio Kanso Design (Visual Brand Identity)*
  - ⭐ **Aarav Kapoor (`aarav-client`)** — *Verified Patron & Art Collector*

### 5. Multi-Tab Marketplace (`/exchange`)
- **Creator Storefronts:** Discover homegrown makers across crafts, gourmet, leather, and design.
- **Verified Capabilities:** Milestone-governed technical services and engineering architecture.
- **Client Project Briefs:** Open requests for proposals (RFPs) with escrow-ready budgets.

---

## 🛠 Tech Stack

- **Backend:** Python 3.13, Flask 3.1
- **Templating:** Jinja2 with custom context processors for global authentication state
- **Frontend:** Vanilla CSS with custom design tokens, modern typography, SVG botanical accents
- **Testing:** Pytest 9.1 with 22 unit & integration test cases
- **Repository:** Connected to [https://github.com/icyboei/Krititva-](https://github.com/icyboei/Krititva-)

---

## 💻 Running Locally

### 1. Clone the repository
```bash
git clone https://github.com/icyboei/Krititva-.git
cd Krititva-
```

### 2. Activate Virtual Environment & Install Dependencies
```bash
# On Windows
.\venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python app.py
```
Open your browser and navigate to **`http://localhost:5000`**.

### 4. Run the Pytest Test Suite
```bash
pytest
```
All 22 test cases will execute and validate authentication, storefronts, listings, ratings, and inquiries.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
