"""
Complete tokenizer training and analysis for both domains
"""
import sys
import os
from pathlib import Path
import json
import time

# Add nanochat to path
sys.path.insert(0, '/Users/abeen/Documents/Fall_Quarter/DLS_LAB2_REAL/nanochat')

from nanochat.tokenizer import HuggingFaceTokenizer
import tiktoken

def train_domain_tokenizer(domain_name, data_file, vocab_size=4096):
    """Train a tokenizer for a specific domain"""
    print(f"\n{'='*60}")
    print(f"Training tokenizer for {domain_name}")
    print(f"{'='*60}")
    
    # Read the data
    with open(data_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    print(f"Data size: {len(text):,} characters ({len(text)/1024/1024:.2f} MB)")
    
    # Create text iterator
    chunk_size = 10000
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    
    print(f"Training on {len(chunks)} chunks...")
    
    def text_iterator():
        for chunk in chunks:
            yield chunk
    
    # Train the tokenizer using HuggingFace implementation
    t0 = time.time()
    tokenizer = HuggingFaceTokenizer.train_from_iterator(text_iterator(), vocab_size)
    train_time = time.time() - t0
    
    print(f"Training completed in {train_time:.2f} seconds")
    
    # Save the tokenizer
    output_dir = Path(f"/Users/abeen/Documents/Fall_Quarter/DLS_LAB2_REAL/outputs/{domain_name}_tokenizer")
    tokenizer.save(str(output_dir))
    print(f"Saved to: {output_dir}")
    
    return tokenizer, text

def analyze_tokenization(tokenizer, text, name):
    """Analyze tokenization performance"""
    print(f"\nAnalyzing {name}...")
    
    # Encode the text (use subset for analysis)
    test_text = text[:100000] if len(text) > 100000 else text
    t0 = time.time()
    tokens = tokenizer.encode(test_text)
    encode_time = time.time() - t0
    
    # Calculate compression ratio
    original_bytes = len(test_text.encode('utf-8'))
    num_tokens = len(tokens)
    compression_ratio = original_bytes / num_tokens
    
    print(f"  Original bytes: {original_bytes:,}")
    print(f"  Number of tokens: {num_tokens:,}")
    print(f"  Compression ratio: {compression_ratio:.2f} bytes/token")
    print(f"  Encoding time: {encode_time:.4f} seconds")
    
    # Get token statistics
    vocab_size = tokenizer.get_vocab_size()
    print(f"  Vocabulary size: {vocab_size:,}")
    
    return {
        'name': name,
        'original_bytes': original_bytes,
        'num_tokens': num_tokens,
        'compression_ratio': compression_ratio,
        'encode_time': encode_time,
        'vocab_size': vocab_size
    }, tokens

def get_frequent_tokens(tokenizer, tokens, top_n=30):
    """Get the most frequent tokens"""
    from collections import Counter
    
    token_counts = Counter(tokens)
    most_common = token_counts.most_common(top_n)
    
    frequent_tokens = []
    for token_id, count in most_common:
        token_str = tokenizer.decode([token_id])
        token_repr = repr(token_str)
        frequent_tokens.append({
            'token_id': token_id,
            'token': token_str,
            'token_repr': token_repr,
            'count': count,
            'percentage': count / len(tokens) * 100
        })
    
    return frequent_tokens

def compare_with_standard_tokenizers(text, domain_name):
    """Compare with standard tokenizers"""
    print(f"\n{'='*60}")
    print(f"Comparing with standard tokenizers for {domain_name}")
    print(f"{'='*60}")
    
    results = []
    
    # Test with first 100k characters
    test_text = text[:100000] if len(text) > 100000 else text
    original_bytes = len(test_text.encode('utf-8'))
    
    # 1. GPT-2 tokenizer
    try:
        enc_gpt2 = tiktoken.get_encoding("gpt2")
        tokens_gpt2 = enc_gpt2.encode(test_text)
        results.append({
            'name': 'GPT-2 (tiktoken)',
            'original_bytes': original_bytes,
            'num_tokens': len(tokens_gpt2),
            'compression_ratio': original_bytes / len(tokens_gpt2),
            'vocab_size': enc_gpt2.n_vocab
        })
        print(f"✓ GPT-2: {len(tokens_gpt2):,} tokens, ratio: {original_bytes/len(tokens_gpt2):.2f}")
    except Exception as e:
        print(f"✗ GPT-2 failed: {e}")
    
    # 2. cl100k_base (GPT-3.5/4)
    try:
        enc_cl100k = tiktoken.get_encoding("cl100k_base")
        tokens_cl100k = enc_cl100k.encode(test_text)
        results.append({
            'name': 'cl100k_base (GPT-3.5/4)',
            'original_bytes': original_bytes,
            'num_tokens': len(tokens_cl100k),
            'compression_ratio': original_bytes / len(tokens_cl100k),
            'vocab_size': enc_cl100k.n_vocab
        })
        print(f"✓ cl100k_base: {len(tokens_cl100k):,} tokens, ratio: {original_bytes/len(tokens_cl100k):.2f}")
    except Exception as e:
        print(f"✗ cl100k_base failed: {e}")
    
    # 3. o200k_base (GPT-4o)
    try:
        enc_o200k = tiktoken.get_encoding("o200k_base")
        tokens_o200k = enc_o200k.encode(test_text)
        results.append({
            'name': 'o200k_base (GPT-4o)',
            'original_bytes': original_bytes,
            'num_tokens': len(tokens_o200k),
            'compression_ratio': original_bytes / len(tokens_o200k),
            'vocab_size': enc_o200k.n_vocab
        })
        print(f"✓ o200k_base: {len(tokens_o200k):,} tokens, ratio: {original_bytes/len(tokens_o200k):.2f}")
    except Exception as e:
        print(f"✗ o200k_base failed: {e}")
    
    return results

def analyze_token_patterns(tokenizer, tokens, text, domain_name, top_n=50):
    """Analyze and categorize token patterns"""
    from collections import Counter
    
    print(f"\n{'='*60}")
    print(f"Token Pattern Analysis for {domain_name}")
    print(f"{'='*60}")
    
    # Get token frequency
    token_counts = Counter(tokens)
    most_common = token_counts.most_common(top_n)
    
    # Decode tokens and categorize
    patterns = {
        'single_char': [],
        'whitespace': [],
        'multi_char': [],
        'special': []
    }
    
    for token_id, count in most_common:
        token_str = tokenizer.decode([token_id])
        token_len = len(token_str)
        
        if token_len == 1:
            if token_str.isspace():
                patterns['whitespace'].append((token_str, count))
            else:
                patterns['single_char'].append((token_str, count))
        elif token_len > 1:
            patterns['multi_char'].append((token_str, count))
    
    # Print analysis
    print(f"\nTop {min(20, len(most_common))} most frequent tokens:\n")
    for i, (token_id, count) in enumerate(most_common[:20], 1):
        token_str = tokenizer.decode([token_id])
        pct = count / len(tokens) * 100
        display_token = repr(token_str) if len(token_str) <= 15 else repr(token_str[:15]) + "..."
        print(f"  {i:2d}. {display_token:40s} | Count: {count:8,} ({pct:5.2f}%) | ID: {token_id}")
    
    print(f"\nPattern categories:")
    print(f"  Single characters: {len(patterns['single_char'])}")
    print(f"  Whitespace tokens: {len(patterns['whitespace'])}")
    print(f"  Multi-character tokens: {len(patterns['multi_char'])}")
    
    if patterns['multi_char']:
        print(f"\nTop 10 multi-character combinations:")
        for token_str, count in patterns['multi_char'][:10]:
            display_token = repr(token_str)
            print(f"    {display_token}: {count:,} occurrences")
    
    return patterns

def main():
    # Movie Scripts domain
    print("\n" + "="*80)
    print("DOMAIN 1: MOVIE SCRIPTS")
    print("="*80)
    
    scripts_file = Path("/Users/abeen/Documents/Fall_Quarter/DLS_LAB2_REAL/data/movie_scripts/movie_scripts_corpus.txt")
    scripts_tokenizer, scripts_text = train_domain_tokenizer("movie_scripts", scripts_file, vocab_size=4096)
    
    # Analyze movie scripts tokenization
    scripts_result, scripts_tokens = analyze_tokenization(scripts_tokenizer, scripts_text, "Movie Scripts (nanochat)")
    scripts_frequent = get_frequent_tokens(scripts_tokenizer, scripts_tokens, top_n=30)
    scripts_patterns = analyze_token_patterns(scripts_tokenizer, scripts_tokens, scripts_text, "Movie Scripts", top_n=50)
    
    # Compare with standard tokenizers
    scripts_standard_results = compare_with_standard_tokenizers(scripts_text, "Movie Scripts")
    
    # Python Code domain
    print("\n" + "="*80)
    print("DOMAIN 2: PYTHON CODE")
    print("="*80)
    
    python_file = Path("/Users/abeen/Documents/Fall_Quarter/DLS_LAB2_REAL/data/python_code/python_code_corpus.txt")
    python_tokenizer, python_text = train_domain_tokenizer("python_code", python_file, vocab_size=4096)
    
    # Analyze Python code tokenization
    python_result, python_tokens = analyze_tokenization(python_tokenizer, python_text, "Python Code (nanochat)")
    python_frequent = get_frequent_tokens(python_tokenizer, python_tokens, top_n=30)
    python_patterns = analyze_token_patterns(python_tokenizer, python_tokens, python_text, "Python Code", top_n=50)
    
    # Compare with standard tokenizers
    python_standard_results = compare_with_standard_tokenizers(python_text, "Python Code")
    
    # Save all results
    results = {
        'movie_scripts': {
            'nanochat_result': scripts_result,
            'standard_results': scripts_standard_results,
            'frequent_tokens': scripts_frequent,
            'patterns': {k: [(t, c) for t, c in v[:10]] for k, v in scripts_patterns.items()}
        },
        'python_code': {
            'nanochat_result': python_result,
            'standard_results': python_standard_results,
            'frequent_tokens': python_frequent,
            'patterns': {k: [(t, c) for t, c in v[:10]] for k, v in python_patterns.items()}
        }
    }
    
    # Save to JSON
    output_file = Path("/Users/abeen/Documents/Fall_Quarter/DLS_LAB2_REAL/outputs/tokenizer_analysis_results.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✓ Results saved to: {output_file}")
    
    # Print summary comparison
    print("\n" + "="*80)
    print("COMPRESSION RATIO COMPARISON SUMMARY")
    print("="*80)
    
    print("\nMovie Scripts:")
    print(f"  nanochat:       {scripts_result['compression_ratio']:.3f} bytes/token")
    for r in scripts_standard_results:
        print(f"  {r['name']:15s}: {r['compression_ratio']:.3f} bytes/token")
    
    print("\nPython Code:")
    print(f"  nanochat:       {python_result['compression_ratio']:.3f} bytes/token")
    for r in python_standard_results:
        print(f"  {r['name']:15s}: {r['compression_ratio']:.3f} bytes/token")
    
    print("\n" + "="*80)
    print("Analysis complete!")
    print("="*80)

if __name__ == "__main__":
    main()

