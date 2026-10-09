"""
Rule-Based NLP Analyzer for Gender Bias in Job Descriptions.

Analyzes text against research-backed gendered lexicons, computes a
Gender Neutrality Index (GNI 0-100%), determines severity level,
generates inline HTML highlights, and recommends inclusive replacements.
"""

import re
import html
from typing import Dict, Any, List
from .words_database import MASCULINE_WORDS, FEMININE_WORDS


class JobBiasAnalyzer:
    """
    Main rule-based NLP engine for job description gender-bias analysis.
    """

    def __init__(self):
        self.masculine_dict = MASCULINE_WORDS
        self.feminine_dict = FEMININE_WORDS
        self._compiled_patterns = self._build_regex_patterns()

    def _build_regex_patterns(self) -> Dict[str, Dict[str, Any]]:
        """
        Build compiled regular expressions with word boundary guards
        for both masculine and feminine dictionaries.
        Supports common English inflections (e.g., -s, -ed, -ing, -ly).
        """
        patterns = {}

        for word, meta in self.masculine_dict.items():
            # Build pattern allowing plurals and inflections
            escaped = re.escape(word)
            pattern = re.compile(rf'\b{escaped}(s|ed|ing|ly|es|ers|er)?\b', re.IGNORECASE)
            patterns[word] = {
                'category': 'masculine',
                'pattern': pattern,
                'meta': meta
            }

        for word, meta in self.feminine_dict.items():
            escaped = re.escape(word)
            pattern = re.compile(rf'\b{escaped}(s|ed|ing|ly|es|ers|er)?\b', re.IGNORECASE)
            patterns[word] = {
                'category': 'feminine',
                'pattern': pattern,
                'meta': meta
            }

        return patterns

    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Performs full bias analysis on the given job description text.

        Returns a dictionary containing:
            - total_words: int
            - masculine_count: int
            - feminine_count: int
            - masculine_density: float (percentage)
            - feminine_density: float (percentage)
            - neutrality_score: int (0 to 100)
            - severity_level: str
            - severity_color: str (Tailwind class)
            - bias_direction: str
            - flagged_terms: list of dicts (word, category, count, replacements, reason)
            - highlighted_html: safe HTML with highlighted flagged words
            - revised_text: text with top inclusive replacements applied
        """
        if not text or not text.strip():
            return self._empty_result()

        raw_text = text.strip()

        # Tokenize total words (split by whitespace & standard word characters)
        raw_words = re.findall(r'\b[A-Za-z0-9_\'-]+\b', raw_text)
        total_words = max(len(raw_words), 1)

        # Track occurrences
        masculine_matches: List[Dict[str, Any]] = []
        feminine_matches: List[Dict[str, Any]] = []
        flagged_terms_map: Dict[str, Dict[str, Any]] = {}

        # Scan text for matching terms and track slice positions for highlighting
        span_annotations = []  # list of tuples (start, end, category, word, replacements)

        for base_word, data in self._compiled_patterns.items():
            pattern = data['pattern']
            category = data['category']
            meta = data['meta']

            for match in pattern.finditer(raw_text):
                matched_str = match.group(0)
                start, end = match.span()

                item = {
                    'matched_word': matched_str,
                    'base_word': base_word,
                    'category': category,
                    'replacements': meta['replacements'],
                    'reason': meta['reason'],
                    'span': (start, end)
                }

                if category == 'masculine':
                    masculine_matches.append(item)
                else:
                    feminine_matches.append(item)

                span_annotations.append((start, end, category, matched_str, base_word, meta))

                # Aggregate by base word for the summary table
                if base_word not in flagged_terms_map:
                    flagged_terms_map[base_word] = {
                        'base_word': base_word,
                        'category': category,
                        'count': 0,
                        'examples': set(),
                        'replacements': meta['replacements'],
                        'reason': meta['reason']
                    }
                flagged_terms_map[base_word]['count'] += 1
                flagged_terms_map[base_word]['examples'].add(matched_str)

        # Convert set to sorted list for JSON serialization
        flagged_terms = []
        for term_data in flagged_terms_map.values():
            term_data['examples'] = sorted(list(term_data['examples']))
            flagged_terms.append(term_data)

        # Sort flagged terms by count descending
        flagged_terms.sort(key=lambda x: x['count'], reverse=True)

        masculine_count = len(masculine_matches)
        feminine_count = len(feminine_matches)
        total_coded = masculine_count + feminine_count

        # Density percentages
        masculine_density = round((masculine_count / total_words) * 100, 2)
        feminine_density = round((feminine_count / total_words) * 100, 2)
        total_density = round((total_coded / total_words) * 100, 2)

        # Calculate Gender Neutrality Index (GNI 0-100%)
        neutrality_score = self._calculate_neutrality_score(
            masculine_count, feminine_count, total_words
        )

        # Determine severity and direction
        severity_level, severity_color, severity_badge = self._determine_severity(neutrality_score)
        bias_direction = self._determine_direction(masculine_count, feminine_count)

        # Generate Highlighted HTML and Revised Text
        highlighted_html = self._generate_highlighted_html(raw_text, span_annotations)
        revised_text = self._generate_revised_text(raw_text, span_annotations)

        return {
            'total_words': total_words,
            'masculine_count': masculine_count,
            'feminine_count': feminine_count,
            'total_coded_words': total_coded,
            'masculine_density': masculine_density,
            'feminine_density': feminine_density,
            'total_density': total_density,
            'neutrality_score': neutrality_score,
            'severity_level': severity_level,
            'severity_color': severity_color,
            'severity_badge': severity_badge,
            'bias_direction': bias_direction,
            'flagged_terms': flagged_terms,
            'highlighted_html': highlighted_html,
            'revised_text': revised_text,
            'masculine_terms': [t for t in flagged_terms if t['category'] == 'masculine'],
            'feminine_terms': [t for t in flagged_terms if t['category'] == 'feminine'],
        }

    def _calculate_neutrality_score(
        self, masculine_count: int, feminine_count: int, total_words: int
    ) -> int:
        """
        Calculates Gender Neutrality Score on a 0-100% scale.
        
        Logic:
        - 0 gender-coded words = 100% (perfect neutrality).
        - Points deducted for gender skew / asymmetry between masculine & feminine words (up to 40 pts).
        - Points deducted for heavy concentration / density of gender-coded words (up to 60 pts).
        """
        total_coded = masculine_count + feminine_count
        if total_coded == 0:
            return 100

        # Asymmetry penalty (0.0 when perfectly balanced, 1.0 when purely one gender)
        imbalance_ratio = abs(masculine_count - feminine_count) / total_coded
        imbalance_penalty = round(imbalance_ratio * 40)

        # Density penalty (penalizes high frequency of coded terms in text)
        density = total_coded / max(total_words, 1)
        # Typically > 5% coded words is extremely dense bias
        density_penalty = min(60, round(density * 750))

        score = 100 - imbalance_penalty - density_penalty
        return max(0, min(100, score))

    def _determine_severity(self, score: int):
        """Returns qualitative label, styling colors, and badge classes."""
        if score >= 90:
            return (
                "Strongly Gender-Neutral",
                "emerald",
                "bg-emerald-100 text-emerald-800 border-emerald-300"
            )
        elif score >= 70:
            return (
                "Mild Bias (Low Risk)",
                "blue",
                "bg-blue-100 text-blue-800 border-blue-300"
            )
        elif score >= 50:
            return (
                "Moderate Bias (Revision Advised)",
                "amber",
                "bg-amber-100 text-amber-800 border-amber-300"
            )
        else:
            return (
                "High Gender Bias (Action Required)",
                "rose",
                "bg-rose-100 text-rose-800 border-rose-300"
            )

    def _determine_direction(self, masculine_count: int, feminine_count: int) -> str:
        """Determine directional lean."""
        diff = masculine_count - feminine_count
        if abs(diff) <= 1 and (masculine_count + feminine_count) > 0:
            return "Balanced (Equal Representation)"
        elif masculine_count > feminine_count:
            return f"Masculine-Skewed (+{diff} terms)"
        elif feminine_count > masculine_count:
            return f"Feminine-Skewed (+{abs(diff)} terms)"
        return "Completely Neutral (No Gender Coding)"

    def _generate_highlighted_html(self, text: str, annotations: List[tuple]) -> str:
        """
        Produces clean, XSS-safe HTML with inline styled badges for biased terms.
        Resolves overlapping spans by sorting and selecting non-overlapping matches.
        """
        if not annotations:
            # Escape raw text and preserve line breaks
            escaped = html.escape(text)
            return escaped.replace("\n", "<br>")

        # Sort annotations by starting index
        sorted_annotations = sorted(annotations, key=lambda a: a[0])

        # Filter overlapping spans
        clean_annotations = []
        last_end = -1
        for ann in sorted_annotations:
            start, end, category, matched_str, base_word, meta = ann
            if start >= last_end:
                clean_annotations.append(ann)
                last_end = end

        # Build output string
        result_parts = []
        current_idx = 0

        for start, end, category, matched_str, base_word, meta in clean_annotations:
            # Add text before match
            if start > current_idx:
                raw_chunk = text[current_idx:start]
                result_parts.append(html.escape(raw_chunk).replace("\n", "<br>"))

            # Format highlighted badge
            safe_matched = html.escape(matched_str)
            safe_base = html.escape(base_word)
            replacements_preview = ", ".join(meta['replacements'][:2])
            safe_rep = html.escape(replacements_preview)

            if category == 'masculine':
                badge_html = (
                    f'<span class="group relative inline-block mx-0.5">'
                    f'<mark class="bg-blue-100 hover:bg-blue-200 text-blue-900 border border-blue-300 '
                    f'font-medium px-1.5 py-0.5 rounded cursor-pointer transition-colors">'
                    f'{safe_matched}'
                    f'<span class="text-[10px] ml-1 uppercase font-bold text-blue-700 bg-blue-200 px-1 rounded">M</span>'
                    f'</mark>'
                    f'<span class="invisible group-hover:visible absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-56 '
                    f'p-2 bg-gray-900 text-white text-xs rounded-lg shadow-xl z-30 pointer-events-none transition-all">'
                    f'<strong class="block text-blue-300 font-semibold mb-0.5">Masculine-Coded: "{safe_base}"</strong>'
                    f'<span class="text-gray-300 block mb-1">{html.escape(meta["reason"])}</span>'
                    f'<span class="text-emerald-300 block font-medium">Try: {safe_rep}</span>'
                    f'</span>'
                    f'</span>'
                )
            else:
                badge_html = (
                    f'<span class="group relative inline-block mx-0.5">'
                    f'<mark class="bg-purple-100 hover:bg-purple-200 text-purple-900 border border-purple-300 '
                    f'font-medium px-1.5 py-0.5 rounded cursor-pointer transition-colors">'
                    f'{safe_matched}'
                    f'<span class="text-[10px] ml-1 uppercase font-bold text-purple-700 bg-purple-200 px-1 rounded">F</span>'
                    f'</mark>'
                    f'<span class="invisible group-hover:visible absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-56 '
                    f'p-2 bg-gray-900 text-white text-xs rounded-lg shadow-xl z-30 pointer-events-none transition-all">'
                    f'<strong class="block text-purple-300 font-semibold mb-0.5">Feminine-Coded: "{safe_base}"</strong>'
                    f'<span class="text-gray-300 block mb-1">{html.escape(meta["reason"])}</span>'
                    f'<span class="text-emerald-300 block font-medium">Try: {safe_rep}</span>'
                    f'</span>'
                    f'</span>'
                )

            result_parts.append(badge_html)
            current_idx = end

        # Add remaining text
        if current_idx < len(text):
            result_parts.append(html.escape(text[current_idx:]).replace("\n", "<br>"))

        return "".join(result_parts)

    def _generate_revised_text(self, text: str, annotations: List[tuple]) -> str:
        """
        Creates an improved, bias-free version of the job description
        by replacing flagged words with the top recommended neutral alternative.
        Preserves original capitalization (TitleCase, UPPERCASE, lowercase).
        """
        if not annotations:
            return text

        # Sort and deduplicate
        sorted_annotations = sorted(annotations, key=lambda a: a[0])
        clean_annotations = []
        last_end = -1
        for ann in sorted_annotations:
            start, end, category, matched_str, base_word, meta = ann
            if start >= last_end:
                clean_annotations.append(ann)
                last_end = end

        revised_parts = []
        current_idx = 0

        for start, end, category, matched_str, base_word, meta in clean_annotations:
            # Append preceding text
            if start > current_idx:
                revised_parts.append(text[current_idx:start])

            # Select primary replacement
            replacement = meta['replacements'][0] if meta['replacements'] else matched_str

            # Preserve capitalization
            if matched_str.isupper() and len(matched_str) > 1:
                replacement_formatted = replacement.upper()
            elif matched_str[0].isupper():
                replacement_formatted = replacement.capitalize()
            else:
                replacement_formatted = replacement.lower()

            revised_parts.append(replacement_formatted)
            current_idx = end

        if current_idx < len(text):
            revised_parts.append(text[current_idx:])

        return "".join(revised_parts)

    def _empty_result(self) -> Dict[str, Any]:
        """Fallback response when given blank or empty input."""
        return {
            'total_words': 0,
            'masculine_count': 0,
            'feminine_count': 0,
            'total_coded_words': 0,
            'masculine_density': 0.0,
            'feminine_density': 0.0,
            'total_density': 0.0,
            'neutrality_score': 100,
            'severity_level': "Strongly Gender-Neutral",
            'severity_color': "emerald",
            'severity_badge': "bg-emerald-100 text-emerald-800 border-emerald-300",
            'bias_direction': "Neutral (No Text Provided)",
            'flagged_terms': [],
            'highlighted_html': "<p class='text-gray-500 italic'>No text provided for analysis.</p>",
            'revised_text': "",
            'masculine_terms': [],
            'feminine_terms': [],
        }
