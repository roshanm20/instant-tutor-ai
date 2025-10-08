"""
Kerala-specific features for Instant Tutor AI
Includes Malayalam support, local curriculum, and Kerala market customization
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/kerala", tags=["Kerala Features"])

# Kerala curriculum mapping
KERALA_CURRICULUM = {
    "scert": {
        "name": "SCERT Kerala",
        "subjects": [
            "Mathematics", "Physics", "Chemistry", "Biology",
            "Social Science", "Malayalam", "English", "Hindi",
            "Arabic", "Sanskrit", "Computer Science"
        ],
        "classes": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
        "languages": ["Malayalam", "English", "Hindi", "Arabic", "Sanskrit"]
    },
    "cbse": {
        "name": "CBSE",
        "subjects": [
            "Mathematics", "Physics", "Chemistry", "Biology",
            "Social Science", "English", "Hindi", "Computer Science",
            "Economics", "Business Studies", "Accountancy"
        ],
        "classes": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
        "languages": ["English", "Hindi", "Sanskrit"]
    },
    "icse": {
        "name": "ICSE",
        "subjects": [
            "Mathematics", "Physics", "Chemistry", "Biology",
            "History", "Geography", "English", "Hindi",
            "Computer Science", "Economics", "Commerce"
        ],
        "classes": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
        "languages": ["English", "Hindi", "Sanskrit"]
    }
}

# Malayalam language support
MALAYALAM_SUPPORT = {
    "greetings": {
        "hello": "നമസ്കാരം",
        "good_morning": "സുപ്രഭാതം",
        "good_evening": "സുസന്ധ്യ",
        "thank_you": "നന്ദി",
        "welcome": "സ്വാഗതം"
    },
    "subjects": {
        "mathematics": "ഗണിതം",
        "physics": "ഭൗതികശാസ്ത്രം",
        "chemistry": "രസതന്ത്രം",
        "biology": "ജീവശാസ്ത്രം",
        "english": "ഇംഗ്ലീഷ്",
        "malayalam": "മലയാളം",
        "hindi": "ഹിന്ദി"
    },
    "common_phrases": {
        "how_are_you": "എങ്ങനെയുണ്ട്?",
        "what_is_your_name": "നിങ്ങളുടെ പേരെന്താണ്?",
        "where_are_you_from": "നിങ്ങൾ എവിടെനിന്നാണ്?",
        "nice_to_meet_you": "നിങ്ങളെ കാണാനായി സന്തോഷം"
    }
}

# Kerala market pricing (in INR)
KERALA_PRICING = {
    "student_monthly": 299,
    "student_yearly": 2999,
    "instructor_monthly": 599,
    "instructor_yearly": 5999,
    "school_license": 9999,
    "university_license": 19999
}

# KSUM (Kerala Startup Mission) alignment
KSUM_FEATURES = {
    "startup_support": [
        "Incubation support",
        "Mentorship programs",
        "Funding opportunities",
        "Networking events",
        "Technology transfer"
    ],
    "government_schemes": [
        "Kerala Startup Mission",
        "Digital Kerala",
        "IT Mission Kerala",
        "Kerala Development and Innovation Strategic Council"
    ],
    "local_integration": [
        "Kerala State IT Mission",
        "Kerala State Council for Science, Technology and Environment",
        "Kerala State Higher Education Council"
    ]
}

@router.get("/features")
async def get_kerala_features():
    """Get all Kerala-specific features and capabilities"""
    return {
        "curriculum_support": KERALA_CURRICULUM,
        "malayalam_support": MALAYALAM_SUPPORT,
        "pricing": KERALA_PRICING,
        "ksum_alignment": KSUM_FEATURES,
        "local_benefits": {
            "cost_effective": "Pricing optimized for Kerala market",
            "language_support": "Full Malayalam, English, Hindi support",
            "curriculum_aligned": "SCERT, CBSE, ICSE curriculum support",
            "local_integration": "KSUM and government scheme alignment"
        }
    }

@router.get("/curriculum/{curriculum_type}")
async def get_curriculum_info(curriculum_type: str):
    """Get specific curriculum information"""
    if curriculum_type not in KERALA_CURRICULUM:
        raise HTTPException(
            status_code=404,
            detail=f"Curriculum type '{curriculum_type}' not found. Available: {list(KERALA_CURRICULUM.keys())}"
        )
    
    return {
        "curriculum": KERALA_CURRICULUM[curriculum_type],
        "supported_features": [
            "Multi-language support",
            "Local content integration",
            "Kerala-specific examples",
            "Cultural context awareness"
        ]
    }

@router.get("/languages")
async def get_supported_languages():
    """Get all supported languages with Malayalam focus"""
    return {
        "primary_languages": ["Malayalam", "English", "Hindi"],
        "language_features": {
            "malayalam": {
                "script": "Malayalam script",
                "romanization": "Supported",
                "voice_support": "Coming soon",
                "translation": "Bidirectional with English"
            },
            "english": {
                "script": "Latin script",
                "voice_support": "Available",
                "translation": "Primary language"
            },
            "hindi": {
                "script": "Devanagari script",
                "romanization": "Supported",
                "voice_support": "Coming soon",
                "translation": "Bidirectional with English"
            }
        },
        "translation_capabilities": [
            "Real-time translation",
            "Context-aware translation",
            "Educational terminology support",
            "Cultural adaptation"
        ]
    }

@router.get("/pricing")
async def get_kerala_pricing():
    """Get Kerala market-optimized pricing"""
    return {
        "pricing": KERALA_PRICING,
        "currency": "INR",
        "payment_methods": [
            "UPI",
            "Net Banking",
            "Credit/Debit Cards",
            "Wallets (Paytm, PhonePe, Google Pay)",
            "EMI options"
        ],
        "discounts": {
            "student_discount": "20% off for verified students",
            "bulk_discount": "30% off for schools/colleges",
            "ksum_discount": "15% off for KSUM registered startups"
        }
    }

@router.get("/ksum")
async def get_ksum_alignment():
    """Get KSUM (Kerala Startup Mission) alignment features"""
    return {
        "ksum_features": KSUM_FEATURES,
        "startup_benefits": [
            "Incubation support through KSUM",
            "Mentorship from industry experts",
            "Access to government funding",
            "Networking with other edtech startups",
            "Technology transfer opportunities"
        ],
        "government_support": [
            "Kerala State IT Mission support",
            "Digital Kerala initiative alignment",
            "Higher Education Council integration",
            "Science and Technology Council support"
        ]
    }

@router.post("/translate")
async def translate_content(
    text: str,
    source_language: str = "english",
    target_language: str = "malayalam"
):
    """Translate educational content between languages"""
    # This would integrate with a translation service
    # For demo purposes, returning mock translation
    
    if target_language == "malayalam":
        mock_translation = f"[Malayalam Translation] {text}"
    elif target_language == "hindi":
        mock_translation = f"[Hindi Translation] {text}"
    else:
        mock_translation = text
    
    return {
        "original_text": text,
        "translated_text": mock_translation,
        "source_language": source_language,
        "target_language": target_language,
        "confidence": 0.85,
        "translation_service": "Kerala EdTech Translation API"
    }

@router.get("/local-content")
async def get_local_content_support():
    """Get information about local content integration"""
    return {
        "kerala_content": {
            "local_examples": [
                "Kerala geography and history",
                "Local scientific institutions",
                "Kerala-specific case studies",
                "Cultural context integration"
            ],
            "institutions": [
                "IISER Thiruvananthapuram",
                "CUSAT",
                "Kerala University",
                "Cochin University of Science and Technology"
            ],
            "local_scientists": [
                "Dr. C.V. Raman (Nobel Prize in Physics)",
                "Dr. K.S. Krishnan",
                "Dr. E.C.G. Sudarshan"
            ]
        },
        "content_adaptation": {
            "cultural_sensitivity": "Content adapted for Kerala context",
            "local_relevance": "Examples from Kerala's educational landscape",
            "language_nuances": "Malayalam language subtleties",
            "regional_focus": "South Indian educational context"
        }
    }

@router.get("/market-analysis")
async def get_kerala_market_analysis():
    """Get Kerala education market analysis"""
    return {
        "market_size": {
            "total_students": "4.5 million",
            "higher_education": "500,000 students",
            "schools": "15,000+ schools",
            "colleges": "1,000+ colleges"
        },
        "digital_adoption": {
            "internet_penetration": "85%",
            "smartphone_usage": "90%",
            "digital_literacy": "78%",
            "online_learning_adoption": "65%"
        },
        "opportunities": [
            "High digital adoption rate",
            "Strong government support for edtech",
            "Growing middle class with education focus",
            "Multi-language market potential",
            "Government school digitization initiatives"
        ],
        "challenges": [
            "Rural-urban digital divide",
            "Language diversity management",
            "Cost sensitivity",
            "Infrastructure limitations in rural areas"
        ]
    }
