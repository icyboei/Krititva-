"""
Krititva In-Memory Store & Domain Services
Powering the Micro-Storefront & SaaS Platform for Artisans, Vendors & Side Hustlers.
"""

from datetime import datetime
import uuid

# Pre-seeded Users (Vendors and Clients)
USERS_DB = {
    "maya-ceramics": {
        "id": "usr-1",
        "username": "maya-ceramics",
        "email": "maya@mitticlay.com",
        "password": "password123",
        "name": "Maya Sharma",
        "role": "vendor",
        "business_name": "Mitti & Clay Studio",
        "tagline": "Wheel-thrown terracotta & stoneware ceramics crafted with mindful intention",
        "category": "Handmade Crafts & Pottery",
        "bio": "Instead of spending months building and maintaining a custom website, Krititva lets me showcase seasonal ceramic drops, book weekend studio workshops, and collect verified reviews from art lovers across India.",
        "location": "Jaipur, Rajasthan (Pan-India Shipping)",
        "phone": "+91 98201 54321",
        "whatsapp": "+91 98201 54321",
        "instagram": "@mitticlay.studio",
        "avatar_initials": "MS",
        "verified": True,
        "badge": "Master Artisan",
        "joined_date": "Aug 2026",
        "response_time": "< 2 hours",
        "cover_theme": "terracotta"
    },
    "rohan-leather": {
        "id": "usr-2",
        "username": "rohan-leather",
        "email": "rohan@heritagetannery.in",
        "password": "password123",
        "name": "Rohan Mehra",
        "role": "vendor",
        "business_name": "Heritage Tannery & Goods",
        "tagline": "Hand-stitched full-grain vegetable-tanned leather goods built to outlive trends",
        "bio": "Part-time leather crafter and weekend side-hustler. Every piece is hand-cut, saddle-stitched with waxed linen thread, and edged with beeswax. Krititva gives me an instant, elegant storefront to list bespoke items.",
        "location": "Bengaluru, Karnataka",
        "phone": "+91 97412 88901",
        "whatsapp": "+91 97412 88901",
        "instagram": "@heritagetannery",
        "avatar_initials": "RM",
        "verified": True,
        "badge": "Bespoke Crafter",
        "joined_date": "Jul 2026",
        "response_time": "< 1 hour",
        "cover_theme": "leather"
    },
    "ananya-bakes": {
        "id": "usr-3",
        "username": "ananya-bakes",
        "email": "ananya@sourdoughloft.in",
        "password": "password123",
        "name": "Chef Ananya Rao",
        "role": "vendor",
        "business_name": "The Sourdough Loft",
        "tagline": "36-hour slow-fermented wild sourdough loaves, artisanal babkas & weekend pastry drops",
        "bio": "Micro-bakery operated from home on a strict pre-order schedule. Using heritage organic stoneground wheat and wild starters. Krititva replaces chaotic WhatsApp DMs with an organized catalog and customer reviews.",
        "location": "Bandra West, Mumbai",
        "phone": "+91 99304 11234",
        "whatsapp": "+91 99304 11234",
        "instagram": "@thesourdoughloft",
        "avatar_initials": "AR",
        "verified": True,
        "badge": "Boutique Baker",
        "joined_date": "May 2026",
        "response_time": "< 30 mins",
        "cover_theme": "baking"
    },
    "kabir-visuals": {
        "id": "usr-4",
        "username": "kabir-visuals",
        "email": "kabir@studiokanso.design",
        "password": "password123",
        "name": "Kabir Sen",
        "role": "vendor",
        "business_name": "Studio Kanso Design",
        "tagline": "Warm minimalist brand identities, handcrafted packaging & packaging collateral",
        "bio": "Independent creative lead collaborating with makers, indie cafes, and boutique D2C startups to establish memorable visual presence without heavy agency retainers.",
        "location": "Pune, Maharashtra / Remote",
        "phone": "+91 98902 33456",
        "whatsapp": "+91 98902 33456",
        "instagram": "@studiokanso",
        "avatar_initials": "KS",
        "verified": True,
        "badge": "Brand Designer",
        "joined_date": "Sep 2026",
        "response_time": "< 3 hours",
        "cover_theme": "design"
    },
    "aarav-client": {
        "id": "usr-client",
        "username": "aarav-client",
        "email": "aarav.kapoor@gmail.com",
        "password": "password123",
        "name": "Aarav Kapoor",
        "role": "client",
        "business_name": "Independent Art Patron",
        "tagline": "Passionate collector of handmade Indian crafts & specialty coffee wares",
        "category": "Art Collector & Patron",
        "bio": "Regular patron of homegrown creators and craftspeople. Always looking for authenticity and high craftsmanship.",
        "location": "New Delhi",
        "avatar_initials": "AK",
        "verified": True,
        "joined_date": "Jun 2026"
    }
}

# Pre-seeded Activities & Offerings (Listed by Vendors with appropriate charges)
ACTIVITIES_DB = [
    {
        "id": "act-1",
        "vendor_username": "maya-ceramics",
        "title": "Hand-Thrown Terracotta Coffee Mugs (Set of 2)",
        "category": "Handmade Crafts & Pottery",
        "type": "Handmade Craftable",
        "charges_display": "₹1,250",
        "charges_amount": 1250,
        "pricing_unit": "Set of 2 Mugs",
        "pricing_model": "Fixed Price",
        "turnaround": "Dispatched in 3-4 Days",
        "description": "Authentic wheel-thrown terracotta mugs with a tactile unglazed rustic grip and food-safe caramel glazed interior. Keeps pour-overs and filter coffees warm while feeling soothing in hand.",
        "inclusions": [
            "2x Handcrafted Terracotta Mugs (320ml volume)",
            "Non-toxic, food-grade high-fire glazed interior",
            "Plastic-free honeycomb paper & jute gift box",
            "Ceramic care & seasoning instructional postcard"
        ],
        "tags": ["Pottery", "Coffee", "Terracotta", "Gift"],
        "status": "In Stock",
        "featured": True,
        "order_count": 38,
        "rating": 4.95,
        "review_count": 8,
        "theme_icon": "☕"
    },
    {
        "id": "act-2",
        "vendor_username": "maya-ceramics",
        "title": "Wabi-Sabi Sculptural Ikebana Flower Vessel",
        "category": "Handmade Crafts & Pottery",
        "type": "Handmade Craftable",
        "charges_display": "₹1,850",
        "charges_amount": 1850,
        "pricing_unit": "Per Single Piece",
        "pricing_model": "Fixed Price",
        "turnaround": "Made to order in 5-6 Days",
        "description": "Hand-pinched asymmetric stoneware vase celebrating natural imperfections. Features a speckled river-sand slip and watertight interior coating for fresh botanicals.",
        "inclusions": [
            "1x Sculptural Stoneware Vessel (Height: 18cm, Width: 12cm)",
            "Integrated inner ceramic kenzan frog anchor",
            "Hand-stamped studio authenticity mark on bottom"
        ],
        "tags": ["Ikebana", "Home Decor", "Wabi-Sabi", "Stoneware"],
        "status": "Made to Order",
        "featured": True,
        "order_count": 19,
        "rating": 5.0,
        "review_count": 4,
        "theme_icon": "🏺"
    },
    {
        "id": "act-3",
        "vendor_username": "maya-ceramics",
        "title": "Weekend Wheel-Throwing & Pottery Masterclass",
        "category": "Tutoring & Workshops",
        "type": "Studio Experience / Workshop",
        "charges_display": "₹2,400",
        "charges_amount": 2400,
        "pricing_unit": "Per Participant (2.5 Hours)",
        "pricing_model": "Session Fee",
        "turnaround": "Weekend Slots (Sat & Sun 10 AM / 3 PM)",
        "description": "Intimate hands-on 1-on-1 pottery session in our sunlit studio in Jaipur. Learn clay wedging, wheel centering, pulling cylinders, and shaping your own vessels.",
        "inclusions": [
            "2.5 Hours guided private wheel instruction",
            "Unlimited clay, shaping tools, and studio apron provided",
            "Studio bisque & glaze firing of your 2 best creations (ready in 10 days)",
            "Artisanal masala chai and refreshments included"
        ],
        "tags": ["Workshop", "Pottery", "Experience", "Jaipur"],
        "status": "Booking Open",
        "featured": False,
        "order_count": 27,
        "rating": 4.9,
        "review_count": 3,
        "theme_icon": "🎨"
    },
    {
        "id": "act-4",
        "vendor_username": "rohan-leather",
        "title": "Hand-Stitched Full-Grain Bifold Leather Wallet",
        "category": "Artisanal Leather & Goods",
        "type": "Bespoke Craftable",
        "charges_display": "₹1,950",
        "charges_amount": 1950,
        "pricing_unit": "Per Wallet (Free Monogram)",
        "pricing_model": "Fixed Price",
        "turnaround": "Handcrafted in 4 Days",
        "description": "Cut from 1.4mm vegetable-tanned full-grain leather. Hand-saddle-stitched using 0.6mm Japanese waxed polyester thread that will never unravel like machine stitches.",
        "inclusions": [
            "Capacity: 6 dedicated card slots + 2 hidden compartments + full cash billfold",
            "Free custom heat-debossed initials (up to 3 characters)",
            "Complimentary 15ml natural beeswax leather conditioner tin",
            "Lifetime stitching repair guarantee"
        ],
        "tags": ["Leather", "Saddle Stitch", "Wallet", "Everyday Carry"],
        "status": "In Stock",
        "featured": True,
        "order_count": 45,
        "rating": 4.92,
        "review_count": 7,
        "theme_icon": "👛"
    },
    {
        "id": "act-5",
        "vendor_username": "rohan-leather",
        "title": "Refillable A5 Leather Journal Cover with Brass Pen Loop",
        "category": "Artisanal Leather & Goods",
        "type": "Bespoke Craftable",
        "charges_display": "₹2,650",
        "charges_amount": 2650,
        "pricing_unit": "Per Cover + Journal",
        "pricing_model": "Fixed Price",
        "turnaround": "Handcrafted in 3-5 Days",
        "description": "Crafted from rich pull-up leather that develops a magnificent golden patina with age. Designed to snugly house standard A5 Leuchtturm, Moleskine, or Midori notebooks.",
        "inclusions": [
            "Full-grain leather outer shell with burnished hand-waxed edges",
            "Includes 1x 160 GSM dot-grid fountain-pen friendly A5 notebook",
            "Elastic band closure with solid raw brass hardware bead"
        ],
        "tags": ["Journal", "Stationery", "Leather", "Writer"],
        "status": "In Stock",
        "featured": True,
        "order_count": 22,
        "rating": 5.0,
        "review_count": 4,
        "theme_icon": "📓"
    },
    {
        "id": "act-6",
        "vendor_username": "ananya-bakes",
        "title": "Heritage 36-Hr Wild Sourdough Boule (850g)",
        "category": "Boutique Gourmet & Baking",
        "type": "Fresh Artisan Bake",
        "charges_display": "₹420",
        "charges_amount": 420,
        "pricing_unit": "Per 850g Loaf",
        "pricing_model": "Pre-order Rate",
        "turnaround": "Bake Days: Wed & Sat 8:00 AM",
        "description": "Naturally leavened loaf fermented slowly over 36 hours. Blistered blistered mahogany crust, airy custard-like crumb with gentle probiotic acidity.",
        "inclusions": [
            "Baked using 100% stoneground indigenous Emmer and Khapli wheat",
            "No commercial yeast, no preservatives, no added sugars",
            "Packaged in breathable unbleached baker linen bags"
        ],
        "tags": ["Sourdough", "Bakery", "Artisan Bread", "Organic"],
        "status": "Pre-orders Open",
        "featured": True,
        "order_count": 110,
        "rating": 5.0,
        "review_count": 14,
        "theme_icon": "🍞"
    },
    {
        "id": "act-7",
        "vendor_username": "ananya-bakes",
        "title": "Valrhona Dark Chocolate Babka Loaf",
        "category": "Boutique Gourmet & Baking",
        "type": "Fresh Artisan Bake",
        "charges_display": "₹650",
        "charges_amount": 650,
        "pricing_unit": "Per Loaf (Serves 6-8)",
        "pricing_model": "Pre-order Rate",
        "turnaround": "Weekend Morning Fresh Dispatch",
        "description": "Rich brioche dough layered with ribbons of 70% dark Valrhona chocolate fudge, roasted cinnamon sugar, and topped with flaky Maldon sea salt syrup.",
        "inclusions": [
            "Generous 550g braided chocolate babka",
            "Pure French butter and single-origin dark chocolate",
            "Reheating instruction card for breakfast toastiness"
        ],
        "tags": ["Babka", "Chocolate", "Pastry", "Gourmet"],
        "status": "Pre-orders Open",
        "featured": False,
        "order_count": 64,
        "rating": 4.95,
        "review_count": 7,
        "theme_icon": "🥐"
    },
    {
        "id": "act-8",
        "vendor_username": "kabir-visuals",
        "title": "Micro-Business Brand Identity & Storefront Kit",
        "category": "Visual Arts & Brand Identity",
        "type": "Creative Service",
        "charges_display": "₹16,500",
        "charges_amount": 16500,
        "pricing_unit": "Complete Package",
        "pricing_model": "Fixed Project Fee",
        "turnaround": "Delivered in 7 Business Days",
        "description": "Designed specifically for indie makers, bakers, and boutique service providers. Includes everything needed to look professional online and on product packaging without paying agency prices.",
        "inclusions": [
            "Primary Wordmark + Secondary Monogram / Stamp (.AI, .SVG, .PNG)",
            "Curated earthy color palette (HEX, RGB, CMYK) & typography rules",
            "5x Reusable Canva social media & story promotional templates",
            "Custom print-ready packaging sticker & thank-you note layout",
            "Direct 1-on-1 Figma handover call and brand guide sheet"
        ],
        "tags": ["Branding", "Identity", "Logo", "Side-Hustle"],
        "status": "2 Slots Open This Month",
        "featured": True,
        "order_count": 14,
        "rating": 4.9,
        "review_count": 5,
        "theme_icon": "📐"
    }
]

# Pre-seeded Client Reviews & Ratings
REVIEWS_DB = [
    {
        "id": "rev-1",
        "vendor_username": "maya-ceramics",
        "client_name": "Aarav Kapoor",
        "client_avatar": "AK",
        "rating": 5,
        "date": "Oct 14, 2026",
        "activity_title": "Hand-Thrown Terracotta Coffee Mugs",
        "review_title": "Elevated my morning filter coffee ritual",
        "comment": "The craftsmanship is astonishing. You can genuinely feel the artisanal wheel marks on the handle. It stays hot, the unglazed rim gives a wonderful tactile sip, and the packaging was 100% plastic-free. Having this direct storefront link made ordering so simple!",
        "verified_buyer": True
    },
    {
        "id": "rev-2",
        "vendor_username": "maya-ceramics",
        "client_name": "Shreya Venkataraman",
        "client_avatar": "SV",
        "rating": 5,
        "date": "Oct 11, 2026",
        "activity_title": "Wabi-Sabi Sculptural Ikebana Flower Vessel",
        "review_title": "The centerpiece of my dining space",
        "comment": "Maya sent updates as she fired the piece in the kiln. The speckled sand glaze has an organic soul that factory ceramics could never replicate. She has built an incredible storefront here on Krititva.",
        "verified_buyer": True
    },
    {
        "id": "rev-3",
        "vendor_username": "maya-ceramics",
        "client_name": "Divya Nambiar",
        "client_avatar": "DN",
        "rating": 5,
        "date": "Oct 04, 2026",
        "activity_title": "Weekend Wheel-Throwing & Pottery Masterclass",
        "review_title": "Therapeutic, patient, and memorable workshop",
        "comment": "Booked this through Krititva for my partner's birthday. Maya is so warm and knowledgeable. We learned how to center clay and our finished glazed bowls arrived safely at our door 10 days later. Highly recommended!",
        "verified_buyer": True
    },
    {
        "id": "rev-4",
        "vendor_username": "rohan-leather",
        "client_name": "Aarav Kapoor",
        "client_avatar": "AK",
        "rating": 5,
        "date": "Oct 12, 2026",
        "activity_title": "Hand-Stitched Full-Grain Bifold Leather Wallet",
        "review_title": "Unmatched saddle stitching craftsmanship",
        "comment": "The rich leather smell hit me the second I opened the box. The saddle stitches are razor-precise and the free monogram adds that heirloom feel. Rohan is a genuine craftsman.",
        "verified_buyer": True
    },
    {
        "id": "rev-5",
        "vendor_username": "rohan-leather",
        "client_name": "Meera Joshi",
        "client_avatar": "MJ",
        "rating": 5,
        "date": "Sep 28, 2026",
        "activity_title": "Refillable A5 Leather Journal Cover",
        "review_title": "My daily writer companion",
        "comment": "The pull-up leather already shows a beautiful patina after 3 weeks of daily cafe journaling. The raw brass bead gives it an antique finish.",
        "verified_buyer": True
    },
    {
        "id": "rev-6",
        "vendor_username": "ananya-bakes",
        "client_name": "Aarav Kapoor",
        "client_avatar": "AK",
        "rating": 5,
        "date": "Oct 15, 2026",
        "activity_title": "Heritage 36-Hr Wild Sourdough Boule",
        "review_title": "Best sourdough crust in Mumbai",
        "comment": "Ananya's country boule has that blistered crust and tangy moist open crumb that you usually only find in European artisanal bakeries. Pre-ordering through her Krititva profile took 10 seconds.",
        "verified_buyer": True
    },
    {
        "id": "rev-7",
        "vendor_username": "ananya-bakes",
        "client_name": "Tanya Chawla",
        "client_avatar": "TC",
        "rating": 5,
        "date": "Oct 08, 2026",
        "activity_title": "Valrhona Dark Chocolate Babka Loaf",
        "review_title": "Decadent and buttery to perfection",
        "comment": "Warmed a thick slice for Sunday brunch. The chocolate swirls are luscious and the sea salt flakes cut through the sweetness brilliantly. Ordering weekly now!",
        "verified_buyer": True
    },
    {
        "id": "rev-8",
        "vendor_username": "kabir-visuals",
        "client_name": "Pooja Hegde (Indie Soap Maker)",
        "client_avatar": "PH",
        "rating": 5,
        "date": "Oct 09, 2026",
        "activity_title": "Micro-Business Brand Identity & Storefront Kit",
        "review_title": "Transformed our hobby into a legit brand",
        "comment": "Kabir understood our earthy brand ethos in the first 15 minutes. The logo mark and packaging label templates made our retail launch at the farmers market look so professional. Worth every single rupee.",
        "verified_buyer": True
    }
]

# Client Inquiries & Booking Requests
INQUIRIES_DB = [
    {
        "id": "inq-1",
        "vendor_username": "maya-ceramics",
        "client_name": "Radhika Menon",
        "client_email": "radhika.m@gmail.com",
        "client_phone": "+91 98112 33445",
        "activity_title": "Hand-Thrown Terracotta Coffee Mugs",
        "message": "Hi Maya! Can I request a customized set of 4 mugs with our home initials etched on the bottom? Would love to know if that is possible.",
        "date": "Oct 16, 2026",
        "status": "Responded"
    }
]


# =========================================================================
# HELPER DOMAIN FUNCTIONS
# =========================================================================

def get_user_by_username(username: str):
    """Retrieve user dictionary by username."""
    if not username:
        return None
    return USERS_DB.get(username.strip().lower())


def get_user_by_email(email: str):
    """Retrieve user dictionary by email."""
    if not email:
        return None
    email_clean = email.strip().lower()
    for user in USERS_DB.values():
        if user.get("email", "").lower() == email_clean:
            return user
    return None


def authenticate_user(identifier: str, password: str):
    """Authenticates by username or email."""
    user = get_user_by_username(identifier) or get_user_by_email(identifier)
    if user and user.get("password") == password:
        return user
    return None


def register_user(name: str, email: str, username: str, password: str, role: str = "vendor",
                  business_name: str = "", category: str = "", tagline: str = "", location: str = ""):
    """Registers a new vendor or client."""
    username = username.strip().lower().replace(" ", "-")
    if username in USERS_DB:
        raise ValueError(f"Username '{username}' is already taken.")
    if get_user_by_email(email):
        raise ValueError(f"An account with email '{email}' already exists.")

    initials = "".join([part[0].upper() for part in name.strip().split()[:2]]) or "KT"

    new_user = {
        "id": f"usr-{uuid.uuid4().hex[:6]}",
        "username": username,
        "email": email.strip().lower(),
        "password": password,
        "name": name.strip(),
        "role": role,
        "business_name": business_name.strip() or f"{name.strip()}'s Showcase",
        "tagline": tagline.strip() or "Artisanal offerings & independent professional services",
        "category": category.strip() or "Independent Creator",
        "bio": f"Welcome to {business_name or name.strip()}'s official micro-storefront on Krititva. Discover our handcrafted creations, book activities, and explore genuine client reviews.",
        "location": location.strip() or "India / Remote Delivery",
        "phone": "+91 90000 00000",
        "whatsapp": "+91 90000 00000",
        "instagram": f"@{username}",
        "avatar_initials": initials,
        "verified": True,
        "badge": "New Creator" if role == "vendor" else "Active Member",
        "joined_date": datetime.now().strftime("%b %Y"),
        "response_time": "< 4 hours",
        "cover_theme": "terracotta"
    }
    USERS_DB[username] = new_user
    return new_user


def get_all_vendors():
    """Returns list of all registered vendor profiles with computed stats."""
    vendors = []
    for user in USERS_DB.values():
        if user.get("role") == "vendor":
            profile = get_vendor_profile(user["username"])
            vendors.append(profile)
    return vendors


def get_vendor_profile(username: str):
    """
    Returns full vendor profile enriched with:
    - listed activities
    - reviews and ratings summary (avg rating, count, star breakdown)
    """
    user = get_user_by_username(username)
    if not user:
        return None

    username_key = user["username"]
    activities = [a for a in ACTIVITIES_DB if a.get("vendor_username") == username_key]
    reviews = [r for r in REVIEWS_DB if r.get("vendor_username") == username_key]

    # Calculate Ratings & Star Breakdown
    star_breakdown = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
    if reviews:
        total_rating = sum(r.get("rating", 5) for r in reviews)
        avg_rating = round(total_rating / len(reviews), 2)
        for r in reviews:
            star = int(round(r.get("rating", 5)))
            star = max(1, min(5, star))
            star_breakdown[star] += 1
    else:
        avg_rating = 5.0

    profile = dict(user)
    profile["activities"] = activities
    profile["activities_count"] = len(activities)
    profile["reviews"] = reviews
    profile["reviews_count"] = len(reviews)
    profile["avg_rating"] = avg_rating
    profile["star_breakdown"] = star_breakdown
    profile["storefront_path"] = f"/profile/{username_key}"
    return profile


def get_vendor_listings(username: str):
    """Retrieve all activities listed by a specific vendor."""
    username = username.strip().lower()
    return [a for a in ACTIVITIES_DB if a.get("vendor_username") == username]


def get_all_listings(category: str = "all", query: str = ""):
    """Retrieve marketplace listings filtered by category and search keyword."""
    results = ACTIVITIES_DB
    if category and category != "all":
        results = [a for a in results if category.lower() in a.get("category", "").lower()]

    if query:
        q = query.strip().lower()
        filtered = []
        for a in results:
            vendor = get_user_by_username(a.get("vendor_username", ""))
            vendor_name = vendor.get("name", "").lower() if vendor else ""
            vendor_biz = vendor.get("business_name", "").lower() if vendor else ""
            if (q in a.get("title", "").lower() or
                q in a.get("description", "").lower() or
                q in a.get("category", "").lower() or
                q in vendor_name or
                q in vendor_biz or
                any(q in tag.lower() for tag in a.get("tags", []))):
                filtered.append(a)
        results = filtered

    # Enrich each listing with vendor info
    enriched = []
    for a in results:
        vendor = get_user_by_username(a.get("vendor_username", ""))
        item = dict(a)
        item["vendor"] = vendor
        enriched.append(item)
    return enriched


def create_listing(vendor_username: str, title: str, category: str, charges_display: str,
                   charges_amount: float, pricing_model: str, turnaround: str,
                   description: str, inclusions: list, tags: list = None,
                   type_name: str = "Handmade Craftable", theme_icon: str = "✨"):
    """Creates and publishes a new listing for a vendor."""
    vendor = get_user_by_username(vendor_username)
    if not vendor:
        raise ValueError("Vendor does not exist")

    new_activity = {
        "id": f"act-{len(ACTIVITIES_DB) + 1}",
        "vendor_username": vendor_username,
        "title": title.strip(),
        "category": category.strip() or vendor.get("category", "Handmade Crafts"),
        "type": type_name.strip() or "Handmade Craftable",
        "charges_display": charges_display.strip(),
        "charges_amount": float(charges_amount) if charges_amount else 1000.0,
        "pricing_unit": pricing_model.strip() or "Fixed Price",
        "pricing_model": pricing_model.strip() or "Fixed Price",
        "turnaround": turnaround.strip() or "Standard Delivery (3-5 Days)",
        "description": description.strip(),
        "inclusions": [inc.strip() for inc in inclusions if inc.strip()] if isinstance(inclusions, list) else [inclusions],
        "tags": tags or [category, "Handmade"],
        "status": "Available",
        "featured": True,
        "order_count": 0,
        "rating": 5.0,
        "review_count": 0,
        "theme_icon": theme_icon
    }
    ACTIVITIES_DB.insert(0, new_activity)
    return new_activity


def add_vendor_review(vendor_username: str, client_name: str, rating: float,
                      review_title: str, comment: str, activity_title: str = "Artisanal Service"):
    """
    Submits a client review & rating for a vendor.
    Recalculates aggregate scores and updates the database.
    """
    vendor = get_user_by_username(vendor_username)
    if not vendor:
        raise ValueError(f"Vendor '{vendor_username}' does not exist.")

    client_initials = "".join([p[0].upper() for p in client_name.strip().split()[:2]]) or "CL"
    new_review = {
        "id": f"rev-{len(REVIEWS_DB) + 1}",
        "vendor_username": vendor_username,
        "client_name": client_name.strip() or "Verified Patron",
        "client_avatar": client_initials,
        "rating": max(1, min(5, int(round(float(rating))))),
        "date": datetime.now().strftime("%b %d, %Y"),
        "activity_title": activity_title.strip() or "Custom Craft / Service",
        "review_title": review_title.strip() or "Verified Customer Experience",
        "comment": comment.strip(),
        "verified_buyer": True
    }
    REVIEWS_DB.insert(0, new_review)

    # Return updated profile summary
    updated_profile = get_vendor_profile(vendor_username)
    return {
        "review": new_review,
        "new_avg_rating": updated_profile["avg_rating"],
        "total_reviews": updated_profile["reviews_count"],
        "star_breakdown": updated_profile["star_breakdown"]
    }


def create_inquiry(vendor_username: str, client_name: str, client_email: str,
                   client_phone: str, activity_title: str, message: str):
    """Records a new order/commission inquiry for a vendor."""
    vendor = get_user_by_username(vendor_username)
    if not vendor:
        raise ValueError("Vendor does not exist")

    inq = {
        "id": f"inq-{len(INQUIRIES_DB) + 1}",
        "vendor_username": vendor_username,
        "client_name": client_name.strip(),
        "client_email": client_email.strip(),
        "client_phone": client_phone.strip(),
        "activity_title": activity_title.strip(),
        "message": message.strip(),
        "date": datetime.now().strftime("%b %d, %Y"),
        "status": "New Inquiry"
    }
    INQUIRIES_DB.insert(0, inq)
    return inq


def get_vendor_inquiries(vendor_username: str):
    """Retrieve all inquiries for a vendor."""
    return [i for i in INQUIRIES_DB if i.get("vendor_username") == vendor_username]
