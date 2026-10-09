"""
Gender-Coded Lexicon Database for Job Description Bias Analysis.

Based on academic research on gendered language in recruitment:
Gaucher, D., Friesen, J., & Kay, A. C. (2011).
'Evidence That Gendered Wording in Job Advertisements Exists and Sustains Gender Inequality.'
Journal of Personality and Social Psychology, 101(1), 109-128.

Enhanced with modern tech-industry tropes (e.g. 'rockstar', 'ninja', 'guru').
"""

MASCULINE_WORDS = {
    # Tech slang & aggressive tropes
    "rockstar": {
        "replacements": ["skilled professional", "experienced developer", "high performer"],
        "reason": "Exclusionary tech-bro trope that discourages women and underrepresented groups."
    },
    "ninja": {
        "replacements": ["expert engineer", "talented specialist", "proficient developer"],
        "reason": "Hyper-masculine jargon that implies extreme individualism and informal bravado."
    },
    "guru": {
        "replacements": ["subject matter expert", "advisor", "senior specialist"],
        "reason": "Informal jargon often associated with male tech culture."
    },
    "hacker": {
        "replacements": ["creative problem solver", "software engineer", "builder"],
        "reason": "Subculture term historically perceived as male-dominated and aggressive."
    },
    "crush": {
        "replacements": ["achieve", "exceed", "successfully deliver"],
        "reason": "Combative, high-pressure framing that alienates collaborative candidates."
    },
    "kill": {
        "replacements": ["resolve", "complete", "accomplish"],
        "reason": "Violent, aggressive metaphor unnecessary in professional settings."
    },
    "workaholic": {
        "replacements": ["dedicated professional", "committed contributor"],
        "reason": "Promotes toxic overwork culture, disproportionately impacting caregivers."
    },

    # Research-backed masculine coded terms
    "dominant": {
        "replacements": ["leading", "influential", "prominent"],
        "reason": "Implies aggressive control rather than cooperative leadership."
    },
    "dominate": {
        "replacements": ["lead", "excel in", "pioneer"],
        "reason": "Combative framing that deters relationship-oriented applicants."
    },
    "competitive": {
        "replacements": ["growth-oriented", "motivated", "market-leading"],
        "reason": "Signals an antagonistic environment rather than a supportive team."
    },
    "competition": {
        "replacements": ["market dynamics", "industry landscape", "benchmarking"],
        "reason": "Emphasizes zero-sum contest over teamwork."
    },
    "enforce": {
        "replacements": ["maintain", "uphold", "ensure compliance with"],
        "reason": "Authoritarian framing that emphasizes policing over partnership."
    },
    "aggressive": {
        "replacements": ["proactive", "ambitious", "determined"],
        "reason": "Historically associated with male aggression; penalizes assertive women."
    },
    "ambitious": {
        "replacements": ["growth-minded", "goal-oriented", "purpose-driven"],
        "reason": "Can be interpreted as prioritizing individual status over team success."
    },
    "assertive": {
        "replacements": ["confident", "clear", "direct"],
        "reason": "Masculine-stereotyped communication trait."
    },
    "decisive": {
        "replacements": ["action-oriented", "solution-focused", "deliberate"],
        "reason": "Often stereotyped as swift male decision-making disregarding consensus."
    },
    "driven": {
        "replacements": ["motivated", "dedicated", "mission-oriented"],
        "reason": "Can imply relentless solitary effort over balanced teamwork."
    },
    "independent": {
        "replacements": ["autonomous", "self-directed", "initiative-taking"],
        "reason": "Discourages collaborative applicants who value mutual support."
    },
    "independently": {
        "replacements": ["autonomously", "with initiative", "with minimal supervision"],
        "reason": "Over-emphasizes isolated working styles."
    },
    "lead": {
        "replacements": ["guide", "facilitate", "coordinate", "mentor"],
        "reason": "Hierarchical framing; consider cooperative alternatives where applicable."
    },
    "leader": {
        "replacements": ["guide", "coordinator", "facilitator"],
        "reason": "Can evoke traditional masculine hierarchical leadership paradigms."
    },
    "outperform": {
        "replacements": ["surpass goals", "excel", "achieve targets"],
        "reason": "Hierarchical competition metric."
    },
    "superior": {
        "replacements": ["high quality", "exceptional", "rigorous"],
        "reason": "Elitist language that can signal exclusionary hierarchy."
    },
    "tackle": {
        "replacements": ["address", "resolve", "handle", "manage"],
        "reason": "Sports/combat metaphor common in male-centric job postings."
    },
    "relentless": {
        "replacements": ["persistent", "tenacious", "steadfast", "thorough"],
        "reason": "Suggests unsustainable work pace and lack of work-life balance."
    },
    "fearless": {
        "replacements": ["bold", "innovative", "calculated risk-taker"],
        "reason": "Heroic male trope that discourages thoughtful, risk-aware applicants."
    },
    "authoritative": {
        "replacements": ["knowledgeable", "trusted", "credible"],
        "reason": "Signals top-down dominance rather than earned trust."
    },
    "command": {
        "replacements": ["orchestrate", "direct", "oversee"],
        "reason": "Militaristic command-and-control terminology."
    },
    "champion": {
        "replacements": ["advocate for", "promote", "sponsor"],
        "reason": "Combative metaphor; advocacy is more inclusive."
    },
    "headstrong": {
        "replacements": ["purposeful", "determined", "principled"],
        "reason": "Masculine-coded trait associated with stubbornness."
    },
    "analytical": {
        "replacements": ["systematic", "thoughtful", "data-informed"],
        "reason": "Historically culturally coded masculine in psychological tests."
    },
    "boast": {
        "replacements": ["demonstrate", "showcase", "highlight"],
        "reason": "Self-promotional masculine trait."
    },
    "standout": {
        "replacements": ["exemplary", "notable", "distinguished"],
        "reason": "Individualistic spotlight term."
    },
    "forceful": {
        "replacements": ["persuasive", "compelling", "impactful"],
        "reason": "Associated with coercion rather than collaborative consensus."
    },
    "cutthroat": {
        "replacements": ["dynamic", "rigorous", "fast-paced"],
        "reason": "Hostile, high-turnover environment indicator."
    },
    "lone wolf": {
        "replacements": ["self-directed specialist", "autonomous contributor"],
        "reason": "Exclusionary individualism rejecting team alignment."
    },
}

FEMININE_WORDS = {
    # Relationship and care-oriented terms
    "nurturing": {
        "replacements": ["fostering", "developing", "mentoring", "cultivating"],
        "reason": "Culturally coded feminine; can reduce perceived rigor of technical roles."
    },
    "nurture": {
        "replacements": ["foster", "cultivate", "grow", "develop"],
        "reason": "Maternal stereotype language that may deter male applicants."
    },
    "supportive": {
        "replacements": ["collaborative", "enabling", "constructive"],
        "reason": "Often associated with subordinate or caregiving roles rather than technical peer."
    },
    "support": {
        "replacements": ["assist", "partner with", "facilitate", "enable"],
        "reason": "Can unintentionally frame technical work as administrative support."
    },
    "collaborative": {
        "replacements": ["cooperative", "cross-functional", "team-aligned"],
        "reason": "Heavily feminine-coded in linguistic balance studies."
    },
    "interpersonal": {
        "replacements": ["communication", "stakeholder management", "relational"],
        "reason": "Stereotyped as emotional labor rather than core strategic skill."
    },
    "compassionate": {
        "replacements": ["empathetic", "user-focused", "thoughtful"],
        "reason": "Emotionally loaded term rarely found in neutral job requirements."
    },
    "empathy": {
        "replacements": ["user-centered understanding", "user insight", "client awareness"],
        "reason": "Can be perceived as emotional soft skill rather than technical requirement."
    },
    "empathize": {
        "replacements": ["understand user needs", "connect with user perspectives"],
        "reason": "Emotional framing; translate to user-research terminology."
    },
    "honest": {
        "replacements": ["transparent", "candid", "ethical"],
        "reason": "Communal virtue culturally associated with feminine virtue framing."
    },
    "loyal": {
        "replacements": ["committed", "dedicated", "dependable"],
        "reason": "Communal attribute implying submissive devotion."
    },
    "responsive": {
        "replacements": ["adaptable", "attentive", "agile"],
        "reason": "Can imply reactive accommodation rather than proactive leadership."
    },
    "trust": {
        "replacements": ["integrity", "reliability", "credibility"],
        "reason": "Communal value that can appear in paternalistic workplace descriptions."
    },
    "understanding": {
        "replacements": ["perceptive", "insightful", "comprehending"],
        "reason": "Communal accommodating trait."
    },
    "sensitive": {
        "replacements": ["attuned", "aware", "context-conscious"],
        "reason": "Stereotyped feminine emotional trait."
    },
    "cooperative": {
        "replacements": ["cross-functional", "collaborative", "synergistic"],
        "reason": "Communal behavioral trait."
    },
    "connect": {
        "replacements": ["interface with", "liaise with", "coordinate"],
        "reason": "Relational framing rather than operational."
    },
    "committed": {
        "replacements": ["dedicated", "reliable", "accountable"],
        "reason": "Communal loyalty attribute."
    },
    "kind": {
        "replacements": ["respectful", "professional", "considerate"],
        "reason": "Personal moral virtue rather than professional competence."
    },
    "gentle": {
        "replacements": ["measured", "patient", "thoughtful"],
        "reason": "Stereotypically feminine softness."
    },
    "warm": {
        "replacements": ["welcoming", "approachable", "engaging"],
        "reason": "Emotional climate descriptor."
    },
    "pleasant": {
        "replacements": ["constructive", "positive", "collegial"],
        "reason": "Superficial communal attribute."
    },
    "sympathetic": {
        "replacements": ["receptive", "mindful", "open-minded"],
        "reason": "Communal emotional reaction."
    },
    "dependable": {
        "replacements": ["reliable", "consistent", "accountable"],
        "reason": "Communal service virtue."
    },
    "caring": {
        "replacements": ["attentive", "user-focused", "diligent"],
        "reason": "Maternal caregiving coding."
    },
    "modest": {
        "replacements": ["grounded", "practical", "measured"],
        "reason": "Self-effacing feminine cultural expectation."
    },
    "polite": {
        "replacements": ["courteous", "respectful", "professional"],
        "reason": "Deference indicator."
    },
    "inclusive": {
        "replacements": ["equitable", "broad-access", "accessible"],
        "reason": "While positive, heavy reliance without operational definitions creates communal skew."
    },
}

# Pre-packaged sample job descriptions for quick testing by beginners
SAMPLE_JOB_DESCRIPTIONS = {
    "masculine_tech": {
        "title": "Senior Rockstar Full-Stack Engineer (High Masculine Bias)",
        "text": """We are looking for a relentless Rockstar Ninja Engineer to dominate our backend architecture and crush technical debt! 

As an aggressive, fearless problem solver, you will tackle our most challenging scalability roadblocks and enforce superior engineering standards. You must be an independent, ambitious individual who takes charge and outperforms the competition. 

Key Responsibilities:
- Command system redesigns and independently lead high-stakes deployments.
- Be a decisive champion who drives aggressive deadlines without hesitation.
- Tackle complex microservice bugs with a killer instinct.
- Dominate cross-functional discussions with authoritative analytical rigor.

Are you a true workaholic hacker ready to boast world-class code? Apply now!"""
    },
    "feminine_care": {
        "title": "Product Support & Community Lead (Feminine-Skewed)",
        "text": """We are seeking a warm, gentle, and deeply caring Community Lead to nurture our growing user base. 

In this role, you will provide supportive and compassionate guidance to all our users. We are looking for someone with an honest, loyal heart who can empathize with customers and maintain a pleasant, polite, and sensitive dialogue across all channels.

Responsibilities:
- Be a dependable, nurturing listener who builds deep emotional trust with our community.
- Connect with team members in a modest, collaborative, and friendly manner.
- Provide sympathetic and caring assistance to resolve complaints gently.
- Foster an inclusive, cooperative environment where everyone feels appreciated and loved."""
    },
    "balanced_neutral": {
        "title": "Senior Software Engineer (Gender-Neutral / Inclusive)",
        "text": """We are seeking a Senior Software Engineer to join our core product engineering team. In this role, you will design, build, and maintain scalable web services alongside cross-functional partners.

Key Responsibilities:
- Design, test, and deploy reliable RESTful APIs and distributed systems.
- Partner with product managers and designers to clarify technical requirements.
- Uphold clean code quality, comprehensive unit tests, and CI/CD pipelines.
- Mentor junior engineers and participate in thoughtful code reviews.
- Communicate technical tradeoffs clearly to stakeholders.

Qualifications:
- 4+ years of professional experience with Python, Django, or modern web frameworks.
- Demonstrated ability to solve complex technical problems systematically.
- Strong written and verbal communication skills."""
    }
}
