#!/usr/bin/env python3
"""
DOMYH Agent v4.0 — Semantic Skill Selector
Generates TF-IDF embeddings for skill selection without external APIs.

Usage:
    python semantic_selector.py --generate   # Generate embeddings
    python semantic_selector.py --query "your query"  # Test selection
"""

import os
import json
import re
import math
from pathlib import Path
from collections import Counter
from typing import List, Dict, Tuple, Optional

# Configuration
BASE_PATH = Path(__file__).parent.parent
SKILLS_PATH = BASE_PATH / "skills"
EMBEDDINGS_FILE = BASE_PATH / "core" / "embeddings.json"
TOP_K = 5
MIN_SCORE = 0.30

# Stopwords for better matching
STOPWORDS = {
    'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
    'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'dare',
    'for', 'and', 'nor', 'but', 'or', 'yet', 'so', 'in', 'on', 'at',
    'to', 'from', 'by', 'with', 'about', 'into', 'through', 'of', 'as',
    'this', 'that', 'these', 'those', 'it', 'its', 'what', 'which', 'who',
    'whom', 'whose', 'how', 'when', 'where', 'why', 'all', 'each', 'every',
    'both', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'not'
}


def tokenize(text: str) -> List[str]:
    """Tokenize text, removing stopwords and short tokens."""
    text = text.lower()
    tokens = re.findall(r'\b[a-z][a-z0-9+#]*\b', text)
    return [t for t in tokens if t not in STOPWORDS and len(t) > 1]


def load_skill_meta(skill_id: str) -> Dict:
    """Load META.yaml for a skill."""
    import yaml
    meta_path = SKILLS_PATH / skill_id / "META.yaml"
    if not meta_path.exists():
        return {}
    with open(meta_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


def load_skill_content(skill_id: str) -> str:
    """Load SKILL.md content for a skill."""
    skill_path = SKILLS_PATH / skill_id / "SKILL.md"
    if not skill_path.exists():
        return ""
    with open(skill_path, 'r', encoding='utf-8') as f:
        return f.read()


def extract_skill_terms(skill_id: str) -> Dict[str, float]:
    """Extract weighted terms from a skill."""
    meta = load_skill_meta(skill_id)
    content = load_skill_content(skill_id)
    
    terms = {}
    
    # Keywords from META.yaml (weight: 3.0)
    keywords = meta.get('keywords', [])
    for kw in keywords:
        for token in tokenize(kw):
            terms[token] = terms.get(token, 0) + 3.0
    
    # Description from META.yaml (weight: 2.0)
    description = meta.get('description', '')
    for token in tokenize(description):
        terms[token] = terms.get(token, 0) + 2.0
    
    # Capabilities from META.yaml (weight: 2.5)
    capabilities = meta.get('capabilities', [])
    for cap in capabilities:
        for token in tokenize(cap):
            terms[token] = terms.get(token, 0) + 2.5
    
    # Content from SKILL.md (weight: 1.0)
    for token in tokenize(content):
        terms[token] = terms.get(token, 0) + 1.0
    
    # Normalize
    if terms:
        max_weight = max(terms.values())
        terms = {k: v / max_weight for k, v in terms.items()}
    
    return terms


def compute_idf(all_skill_terms: Dict[str, Dict[str, float]]) -> Dict[str, float]:
    """Compute IDF scores across all skills."""
    doc_count = len(all_skill_terms)
    term_doc_freq = Counter()
    
    for skill_terms in all_skill_terms.values():
        for term in skill_terms.keys():
            term_doc_freq[term] += 1
    
    idf = {}
    for term, freq in term_doc_freq.items():
        idf[term] = math.log(doc_count / freq) + 1
    
    return idf


def generate_embeddings() -> Dict:
    """Generate TF-IDF style embeddings for all skills."""
    index_path = SKILLS_PATH / "index.json"
    with open(index_path, 'r', encoding='utf-8') as f:
        index = json.load(f)
    
    all_terms = {}
    skills_data = {}
    
    print("📊 Extracting terms from skills...")
    for skill in index['skills']:
        skill_id = skill['id']
        terms = extract_skill_terms(skill_id)
        all_terms[skill_id] = terms
        
        meta = load_skill_meta(skill_id)
        skills_data[skill_id] = {
            'name': meta.get('display_name', skill_id),
            'category': skill.get('category', 'unknown'),
            'keywords': meta.get('keywords', []),
            'terms': terms
        }
        print(f"  ✓ {skill_id}: {len(terms)} terms")
    
    # Compute IDF
    print("\n📈 Computing IDF scores...")
    idf = compute_idf(all_terms)
    
    # Apply TF-IDF
    print("\n🔢 Generating TF-IDF vectors...")
    for skill_id, data in skills_data.items():
        tfidf = {}
        for term, tf in data['terms'].items():
            tfidf[term] = tf * idf.get(term, 1.0)
        data['tfidf'] = tfidf
        # Keep only top 50 terms per skill
        top_terms = sorted(tfidf.items(), key=lambda x: -x[1])[:50]
        data['tfidf'] = dict(top_terms)
        del data['terms']  # Remove raw terms to save space
    
    embeddings = {
        'version': '4.0.0',
        'algorithm': 'tfidf',
        'skills': skills_data,
        'idf': dict(sorted(idf.items(), key=lambda x: -x[1])[:500]),  # Top 500 IDF terms
        'config': {
            'top_k': TOP_K,
            'min_score': MIN_SCORE
        }
    }
    
    return embeddings


def cosine_similarity(vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
    """Compute cosine similarity between two sparse vectors."""
    common_keys = set(vec1.keys()) & set(vec2.keys())
    if not common_keys:
        return 0.0
    
    dot_product = sum(vec1[k] * vec2[k] for k in common_keys)
    norm1 = math.sqrt(sum(v * v for v in vec1.values()))
    norm2 = math.sqrt(sum(v * v for v in vec2.values()))
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    return dot_product / (norm1 * norm2)


def select_skills(query: str, embeddings: Dict, top_k: int = TOP_K) -> List[Tuple[str, float]]:
    """Select top-K relevant skills for a query."""
    # Tokenize query
    query_tokens = tokenize(query)
    if not query_tokens:
        return []
    
    # Build query vector using IDF
    idf = embeddings.get('idf', {})
    query_vec = {}
    token_counts = Counter(query_tokens)
    for token, count in token_counts.items():
        tf = count / len(query_tokens)
        query_vec[token] = tf * idf.get(token, 1.0)
    
    # Score each skill
    scores = []
    for skill_id, skill_data in embeddings['skills'].items():
        tfidf = skill_data.get('tfidf', {})
        score = cosine_similarity(query_vec, tfidf)
        
        # Keyword exact match boost
        keywords = [kw.lower() for kw in skill_data.get('keywords', [])]
        for token in query_tokens:
            if token in keywords:
                score += 0.15  # Boost for exact keyword match
        
        # Category boost
        category = skill_data.get('category', '')
        if category == 'core':
            score += 0.10
        
        if score > 0:
            scores.append((skill_id, score))
    
    # Sort and return top-K
    scores.sort(key=lambda x: -x[1])
    return scores[:top_k]


def main():
    import argparse
    parser = argparse.ArgumentParser(description='DOMYH Semantic Skill Selector')
    parser.add_argument('--generate', action='store_true', help='Generate embeddings')
    parser.add_argument('--query', type=str, help='Test query for skill selection')
    args = parser.parse_args()
    
    if args.generate:
        print("🚀 Generating semantic embeddings...\n")
        embeddings = generate_embeddings()
        
        # Save embeddings
        os.makedirs(EMBEDDINGS_FILE.parent, exist_ok=True)
        with open(EMBEDDINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(embeddings, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Embeddings saved to: {EMBEDDINGS_FILE}")
        print(f"   Skills indexed: {len(embeddings['skills'])}")
        print(f"   IDF terms: {len(embeddings['idf'])}")
    
    elif args.query:
        if not EMBEDDINGS_FILE.exists():
            print("❌ Embeddings not found. Run with --generate first.")
            return
        
        with open(EMBEDDINGS_FILE, 'r', encoding='utf-8') as f:
            embeddings = json.load(f)
        
        print(f"🔍 Query: {args.query}\n")
        results = select_skills(args.query, embeddings)
        
        print("📋 Top skills:")
        for skill_id, score in results:
            skill_data = embeddings['skills'][skill_id]
            status = "✓" if score >= MIN_SCORE else "○"
            print(f"  {status} {skill_id}: {score:.3f} ({skill_data['name']})")
        
        selected = [s for s, score in results if score >= MIN_SCORE]
        print(f"\n🎯 Selected ({len(selected)}): {', '.join(selected)}")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
