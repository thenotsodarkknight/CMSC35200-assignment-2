"""
Create professional visualizations for the tokenization analysis
"""
import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Read results
with open('/Users/abeen/Documents/Fall_Quarter/DLS_LAB2_REAL/outputs/tokenizer_analysis_results.json', 'r') as f:
    results = json.load(f)

output_dir = Path('/Users/abeen/Documents/Fall_Quarter/DLS_LAB2_REAL/outputs')

# Figure 1: Compression Ratio Comparison
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Movie Scripts compression ratios
scripts_names = ['nanochat\n(4K vocab)']
scripts_ratios = [results['movie_scripts']['nanochat_result']['compression_ratio']]
for r in results['movie_scripts']['standard_results']:
    name = r['name'].split('(')[0].strip()
    vocab = r['vocab_size']
    scripts_names.append(f"{name}\n({vocab//1000}K vocab)")
    scripts_ratios.append(r['compression_ratio'])

colors = ['#2ecc71', '#3498db', '#9b59b6', '#e74c3c']
bars1 = ax1.bar(range(len(scripts_names)), scripts_ratios, color=colors)
ax1.set_xticks(range(len(scripts_names)))
ax1.set_xticklabels(scripts_names, fontsize=10)
ax1.set_ylabel('Compression Ratio (bytes/token)', fontsize=12)
ax1.set_title('Movie Scripts: Compression Ratio Comparison', fontsize=14, fontweight='bold')
ax1.grid(axis='y', alpha=0.3)

# Add value labels on bars
for bar, ratio in zip(bars1, scripts_ratios):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{ratio:.2f}',
             ha='center', va='bottom', fontsize=11, fontweight='bold')

# Python Code compression ratios
python_names = ['nanochat\n(4K vocab)']
python_ratios = [results['python_code']['nanochat_result']['compression_ratio']]
for r in results['python_code']['standard_results']:
    name = r['name'].split('(')[0].strip()
    vocab = r['vocab_size']
    python_names.append(f"{name}\n({vocab//1000}K vocab)")
    python_ratios.append(r['compression_ratio'])

bars2 = ax2.bar(range(len(python_names)), python_ratios, color=colors)
ax2.set_xticks(range(len(python_names)))
ax2.set_xticklabels(python_names, fontsize=10)
ax2.set_ylabel('Compression Ratio (bytes/token)', fontsize=12)
ax2.set_title('Python Code: Compression Ratio Comparison', fontsize=14, fontweight='bold')
ax2.grid(axis='y', alpha=0.3)

# Add value labels on bars
for bar, ratio in zip(bars2, python_ratios):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
             f'{ratio:.2f}',
             ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig(output_dir / 'compression_comparison.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved compression comparison plot")
plt.close()

# Figure 2: Top tokens visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# Movie Scripts top tokens
scripts_tokens = results['movie_scripts']['frequent_tokens'][:15]
token_labels = [t['token_repr'] for t in scripts_tokens]
token_counts = [t['count'] for t in scripts_tokens]

y_pos = np.arange(len(token_labels))
ax1.barh(y_pos, token_counts, color='#2ecc71', alpha=0.8)
ax1.set_yticks(y_pos)
ax1.set_yticklabels(token_labels, fontsize=9, family='monospace')
ax1.invert_yaxis()
ax1.set_xlabel('Frequency Count', fontsize=12)
ax1.set_title('Movie Scripts: Top 15 Most Frequent Tokens', fontsize=14, fontweight='bold')
ax1.grid(axis='x', alpha=0.3)

# Add count labels
for i, (count, pct) in enumerate(zip(token_counts, [t['percentage'] for t in scripts_tokens])):
    ax1.text(count, i, f' {count} ({pct:.1f}%)', 
             va='center', fontsize=9)

# Python Code top tokens
python_tokens = results['python_code']['frequent_tokens'][:15]
token_labels_py = [t['token_repr'] for t in python_tokens]
token_counts_py = [t['count'] for t in python_tokens]

y_pos_py = np.arange(len(token_labels_py))
ax2.barh(y_pos_py, token_counts_py, color='#e74c3c', alpha=0.8)
ax2.set_yticks(y_pos_py)
ax2.set_yticklabels(token_labels_py, fontsize=9, family='monospace')
ax2.invert_yaxis()
ax2.set_xlabel('Frequency Count', fontsize=12)
ax2.set_title('Python Code: Top 15 Most Frequent Tokens', fontsize=14, fontweight='bold')
ax2.grid(axis='x', alpha=0.3)

# Add count labels
for i, (count, pct) in enumerate(zip(token_counts_py, [t['percentage'] for t in python_tokens])):
    ax2.text(count, i, f' {count} ({pct:.1f}%)', 
             va='center', fontsize=9)

plt.tight_layout()
plt.savefig(output_dir / 'top_tokens.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved top tokens plot")
plt.close()

# Figure 3: Token pattern distribution
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

# Movie Scripts patterns
scripts_patterns = results['movie_scripts']['patterns']
pattern_types = ['Single\nChar', 'Whitespace', 'Multi-Char']
pattern_counts = [len(scripts_patterns['single_char']), 
                  len(scripts_patterns['whitespace']), 
                  len(scripts_patterns['multi_char'])]

ax1.bar(pattern_types, pattern_counts, color=['#3498db', '#f39c12', '#e74c3c'], alpha=0.8)
ax1.set_ylabel('Number of Token Types', fontsize=12)
ax1.set_title('Movie Scripts: Token Pattern Distribution', fontsize=14, fontweight='bold')
ax1.grid(axis='y', alpha=0.3)

for i, count in enumerate(pattern_counts):
    ax1.text(i, count, str(count), ha='center', va='bottom', fontsize=12, fontweight='bold')

# Python Code patterns
python_patterns = results['python_code']['patterns']
pattern_counts_py = [len(python_patterns['single_char']), 
                     len(python_patterns['whitespace']), 
                     len(python_patterns['multi_char'])]

ax2.bar(pattern_types, pattern_counts_py, color=['#3498db', '#f39c12', '#e74c3c'], alpha=0.8)
ax2.set_ylabel('Number of Token Types', fontsize=12)
ax2.set_title('Python Code: Token Pattern Distribution', fontsize=14, fontweight='bold')
ax2.grid(axis='y', alpha=0.3)

for i, count in enumerate(pattern_counts_py):
    ax2.text(i, count, str(count), ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig(output_dir / 'pattern_distribution.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved pattern distribution plot")
plt.close()

# Figure 4: Overall efficiency analysis
fig, ax = plt.subplots(figsize=(10, 6))

tokenizers_all = ['nanochat\nScripts', 'GPT-2\nScripts', 'cl100k\nScripts', 'o200k\nScripts',
                  'nanochat\nPython', 'GPT-2\nPython', 'cl100k\nPython', 'o200k\nPython']
ratios_all = scripts_ratios + python_ratios
colors_all = ['#2ecc71', '#3498db', '#9b59b6', '#e74c3c'] * 2

bars = ax.bar(range(len(tokenizers_all)), ratios_all, color=colors_all, alpha=0.7)

# Add vertical divider
ax.axvline(x=3.5, color='gray', linestyle='--', linewidth=2, alpha=0.5)
ax.text(1.5, max(ratios_all)*0.95, 'Movie Scripts', ha='center', fontsize=12, fontweight='bold')
ax.text(5.5, max(ratios_all)*0.95, 'Python Code', ha='center', fontsize=12, fontweight='bold')

ax.set_xticks(range(len(tokenizers_all)))
ax.set_xticklabels(tokenizers_all, fontsize=9, rotation=45, ha='right')
ax.set_ylabel('Compression Ratio (bytes/token)', fontsize=12)
ax.set_title('Overall Tokenization Efficiency Comparison', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)

# Add value labels
for bar, ratio in zip(bars, ratios_all):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{ratio:.2f}',
            ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig(output_dir / 'overall_efficiency.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved overall efficiency plot")
plt.close()

print("\n✅ All visualizations created successfully!")

