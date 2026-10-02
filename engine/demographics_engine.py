"""
NETRA Social Intelligence Platform
Demographics Engine

Infers anonymized audience demographics from social media post data,
including age brackets, language, professional interests, and persona.
"""

from collections import defaultdict, Counter


class DemographicsEngine:
    """
    Infers anonymized audience demographics from post data.

    Provides per-post demographic profiling and aggregate analytics across
    a collection of posts, including age, language, interests, and persona.
    """

    # --- Age Bracket Vocabulary Signals ---
    AGE_SIGNALS = {
        '18-24': [
            'bro', 'literally', 'ngl', 'tbh', 'lowkey', 'vibe', 'slay',
            'no cap', 'fam', 'sus', 'rizz', 'bet', 'mid'
        ],
        '25-34': [
            'startup', 'vc', 'funding', 'hustle', 'grind', 'saas',
            'remote work', 'productivity', 'ux', 'agile'
        ],
        '35-44': [
            'mortgage', 'management', 'enterprise', 'roi', 'stakeholder',
            'strategic', 'portfolio', 'quarterly'
        ],
        '45+': [
            'retirement', 'pension', 'decades', 'traditional', 'legacy',
            'veteran', 'established'
        ],
    }

    # --- Language Detection Signals ---
    LANGUAGE_SIGNALS = {
        'Hindi':   ['hai', 'nahi', 'kya', 'aur', 'ke', 'se', 'mein', 'hain', 'bahut'],
        'Tamil':   ['enna', 'epdi', 'nalla', 'sollu', 'inge'],
        'Telugu':  ['emito', 'cheppandi', 'undi', 'ledu'],
        'Bengali': ['ami', 'tumi', 'ache', 'hobe'],
        'Marathi': ['ahe', 'kay', 'mhanje', 'zhala'],
    }

    # --- Professional Interest Keywords ---
    INTEREST_KEYWORDS = {
        'Technology & Cybersecurity': [
            'cyber', 'hack', 'malware', 'ai', 'ml', 'code', 'software',
            'blockchain', 'api', 'cloud'
        ],
        'Finance & Economy': [
            'market', 'stock', 'crypto', 'bitcoin', 'inflation', 'gdp',
            'rbi', 'sebi', 'investment'
        ],
        'Politics & Governance': [
            'government', 'parliament', 'election', 'minister', 'policy',
            'modi', 'lok sabha'
        ],
        'Defence & Security': [
            'army', 'military', 'isro', 'drdo', 'cert-in', 'nciipc',
            'border', 'intelligence'
        ],
        'Media & Journalism': [
            'breaking', 'journalist', 'reporter', 'news', 'media',
            'press', 'exclusive'
        ],
        'Health & Science': [
            'vaccine', 'covid', 'health', 'research', 'clinical',
            'hospital', 'who', 'disease'
        ],
        'Social Issues': [
            'protest', 'rights', 'equality', 'discrimination', 'awareness',
            'community', 'welfare'
        ],
    }

    # --- Persona Rules (evaluated in priority order; first match wins) ---
    PERSONA_RULES = [
        ('Bot-Risk',       lambda p, ba: ba.get('is_bot', False)),
        ('Power User',     lambda p, ba: p.get('followers', 0) > 50000 and p.get('retweets', 0) > 100),
        ('Influencer',     lambda p, ba: p.get('followers', 0) > 10000 and p.get('likes', 0) > 200),
        ('Active Citizen', lambda p, ba: 1000 < p.get('followers', 0) <= 10000),
        ('Casual User',    lambda p, ba: p.get('followers', 0) <= 1000),
    ]

    # -------------------------------------------------------------------------
    # Internal Helpers
    # -------------------------------------------------------------------------

    def _tokenize(self, text: str) -> str:
        """Lowercase text for signal matching."""
        return text.lower() if text else ''

    def _infer_age_bracket(self, text: str) -> str:
        """Return the best-matching age bracket based on vocabulary signals."""
        lowered = self._tokenize(text)
        scores = {bracket: 0 for bracket in self.AGE_SIGNALS}
        for bracket, signals in self.AGE_SIGNALS.items():
            for signal in signals:
                if signal in lowered:
                    scores[bracket] += 1
        best = max(scores, key=scores.get)
        return best if scores[best] > 0 else '25-34'

    def _detect_language(self, text: str) -> str:
        """Detect language from vocabulary signals; defaults to English."""
        lowered = self._tokenize(text)
        tokens = set(lowered.split())
        scores = {}
        for lang, signals in self.LANGUAGE_SIGNALS.items():
            scores[lang] = sum(1 for s in signals if s in tokens)
        best_lang = max(scores, key=scores.get)
        return best_lang if scores[best_lang] > 0 else 'English'

    def _classify_interests(self, text: str, top_n: int = 2) -> list:
        """Return the top-N professional interest categories matching the text."""
        lowered = self._tokenize(text)
        scores = {}
        for category, keywords in self.INTEREST_KEYWORDS.items():
            scores[category] = sum(1 for kw in keywords if kw in lowered)
        ranked = sorted(scores, key=scores.get, reverse=True)
        top = [cat for cat in ranked if scores[cat] > 0][:top_n]
        return top if top else ['General']

    def _classify_persona(self, post: dict) -> str:
        """Return the audience persona label for a single post."""
        bot_analysis = post.get('bot_analysis', {}) or {}
        for persona, rule in self.PERSONA_RULES:
            if rule(post, bot_analysis):
                return persona
        return 'Casual User'

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------

    def infer_post_demographics(self, post: dict) -> dict:
        """
        Infer demographics for a single post.

        Parameters
        ----------
        post : dict
            A NETRA-format post dict. Expected fields: 'content', 'followers',
            'likes', 'retweets', 'bot_analysis' (optional).

        Returns
        -------
        dict
            Keys: age_bracket, language, interests (list), persona.
        """
        content = post.get('content', '') or ''
        return {
            'age_bracket': self._infer_age_bracket(content),
            'language':    self._detect_language(content),
            'interests':   self._classify_interests(content, top_n=2),
            'persona':     self._classify_persona(post),
        }

    def aggregate_demographics(self, posts: list) -> dict:
        """
        Aggregate demographics across a collection of posts.

        Parameters
        ----------
        posts : list[dict]
            List of NETRA-format post dicts.

        Returns
        -------
        dict
            Keys:
              - age_distribution       : list of {name, count, pct}
              - language_distribution  : list of {name, count, pct}
              - interest_distribution  : list of {name, count, pct} (top 7)
              - persona_distribution   : list of {name, count, pct}
              - total_profiled         : int
              - sentiment_by_age       : dict mapping age bracket to avg sentiment score
              - top_locations          : list of top-5 location strings
        """
        total = len(posts)
        if total == 0:
            return {
                'age_distribution':      [],
                'language_distribution': [],
                'interest_distribution': [],
                'persona_distribution':  [],
                'total_profiled':        0,
                'sentiment_by_age':      {},
                'top_locations':         [],
            }

        age_counts      = Counter()
        lang_counts     = Counter()
        interest_counts = Counter()
        persona_counts  = Counter()
        location_counts = Counter()
        sentiment_by_age = defaultdict(list)

        for post in posts:
            demo = self.infer_post_demographics(post)

            bracket  = demo['age_bracket']
            language = demo['language']
            persona  = demo['persona']

            age_counts[bracket]   += 1
            lang_counts[language] += 1
            persona_counts[persona] += 1

            for interest in demo['interests']:
                interest_counts[interest] += 1

            loc = post.get('location') or ''
            if loc:
                location_counts[loc.strip()] += 1

            sentiment = post.get('sentiment') or {}
            score = sentiment.get('score')
            if score is not None:
                try:
                    sentiment_by_age[bracket].append(float(score))
                except (TypeError, ValueError):
                    pass

        def _to_pct_list(counter, top_n=None):
            items = counter.most_common(top_n) if top_n else counter.most_common()
            return [
                {'name': name, 'count': count, 'pct': round(count / total * 100, 2)}
                for name, count in items
            ]

        avg_sentiment = {
            bracket: round(sum(scores) / len(scores), 4)
            for bracket, scores in sentiment_by_age.items()
            if scores
        }

        top_locations = [loc for loc, _ in location_counts.most_common(5)]

        return {
            'age_distribution':      _to_pct_list(age_counts),
            'language_distribution': _to_pct_list(lang_counts),
            'interest_distribution': _to_pct_list(interest_counts, top_n=7),
            'persona_distribution':  _to_pct_list(persona_counts),
            'total_profiled':        total,
            'sentiment_by_age':      avg_sentiment,
            'top_locations':         top_locations,
        }
