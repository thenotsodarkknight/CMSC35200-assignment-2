"""
Collect real legal documents from public APIs and sources
Using U.S. Supreme Court opinions and case law
"""
import requests
from pathlib import Path
import time
import json

def collect_legal_documents():
    """Collect legal documents from public sources"""
    
    output_dir = Path("/Users/abeen/Documents/Fall_Quarter/DLS_LAB2_REAL/data/legal_documents")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    all_documents = []
    metadata = []
    
    print("Collecting U.S. Supreme Court opinions from Case.law API...")
    
    # Case.law API - free access to U.S. case law
    # Fetching recent Supreme Court cases
    base_url = "https://api.case.law/v1/cases/"
    
    params = {
        'jurisdiction': 'us',
        'court': 'supreme-court-us',
        'page_size': 100,  # Get 100 cases
    }
    
    headers = {
        'User-Agent': 'Educational Research Project',
    }
    
    try:
        print("  Fetching from Case.law API...")
        response = requests.get(base_url, params=params, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            cases = data.get('results', [])
            
            print(f"  Found {len(cases)} Supreme Court cases")
            
            for i, case in enumerate(cases, 1):
                case_name = case.get('name_abbreviation', f'Case_{i}')
                case_text = case.get('casebody', {}).get('data', {})
                
                # Extract opinions text
                opinions = case_text.get('opinions', [])
                
                for opinion in opinions:
                    opinion_text = opinion.get('text', '')
                    if opinion_text:
                        doc = f"\n{'='*80}\n"
                        doc += f"CASE: {case_name}\n"
                        doc += f"CITATION: {case.get('citations', [{}])[0].get('cite', 'N/A')}\n"
                        doc += f"DECISION DATE: {case.get('decision_date', 'N/A')}\n"
                        doc += f"COURT: {case.get('court', {}).get('name', 'N/A')}\n"
                        doc += f"{'='*80}\n\n"
                        doc += opinion_text + "\n"
                        
                        all_documents.append(doc)
                        
                        metadata.append({
                            'case_name': case_name,
                            'citation': case.get('citations', [{}])[0].get('cite', 'N/A'),
                            'date': case.get('decision_date', 'N/A'),
                            'length': len(opinion_text)
                        })
                
                if i % 10 == 0:
                    print(f"    Processed {i}/{len(cases)} cases...")
            
            print(f"  ✓ Collected {len(all_documents)} opinions from Case.law")
            
        else:
            print(f"  ✗ Case.law API returned status {response.status_code}")
            
    except Exception as e:
        print(f"  ✗ Error with Case.law API: {e}")
    
    # If we didn't get enough, try CourtListener API
    if len(all_documents) < 50:
        print("\n  Fetching from CourtListener...")
        try:
            courtlistener_url = "https://www.courtlistener.com/api/rest/v3/opinions/"
            params = {
                'court': 'scotus',
                'page_size': 50,
            }
            
            response = requests.get(courtlistener_url, params=params, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                opinions = data.get('results', [])
                
                for opinion in opinions:
                    opinion_text = opinion.get('plain_text', '') or opinion.get('html', '')
                    if opinion_text and len(opinion_text) > 500:
                        doc = f"\n{'='*80}\n"
                        doc += f"OPINION ID: {opinion.get('id', 'N/A')}\n"
                        doc += f"TYPE: {opinion.get('type', 'N/A')}\n"
                        doc += f"DATE: {opinion.get('date_created', 'N/A')[:10]}\n"
                        doc += f"{'='*80}\n\n"
                        doc += opinion_text + "\n"
                        
                        all_documents.append(doc)
                
                print(f"  ✓ Collected {len(opinions)} additional opinions from CourtListener")
                
        except Exception as e:
            print(f"  ✗ Error with CourtListener: {e}")
    
    # Fetch some public legal texts from Cornell LII
    print("\n  Fetching from Cornell Legal Information Institute...")
    
    # Constitution and Amendments (public domain)
    constitution_sections = [
        "https://www.law.cornell.edu/constitution/articlei",
        "https://www.law.cornell.edu/constitution/articleii",
        "https://www.law.cornell.edu/constitution/articleiii",
        "https://www.law.cornell.edu/constitution/billofrights",
    ]
    
    for url in constitution_sections:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                # Simple text extraction (would need beautifulsoup for better parsing)
                content = response.text
                # Extract text between body tags as rough approximation
                if '<body' in content and '</body>' in content:
                    body_start = content.find('<body')
                    body_end = content.find('</body>')
                    body_content = content[body_start:body_end]
                    # Remove HTML tags (simple approach)
                    import re
                    text = re.sub('<[^<]+?>', '', body_content)
                    text = text.replace('&nbsp;', ' ').replace('&amp;', '&')
                    
                    if len(text) > 1000:
                        all_documents.append(f"\n{'='*80}\n")
                        all_documents.append(f"SOURCE: {url}\n")
                        all_documents.append(f"{'='*80}\n\n")
                        all_documents.append(text + "\n")
            
            time.sleep(1)
        except Exception as e:
            print(f"    ✗ Error fetching {url}: {e}")
    
    # Save all documents
    output_file = output_dir / "legal_documents_corpus.txt"
    full_corpus = "\n".join(all_documents)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_corpus)
    
    # Save metadata
    metadata_file = output_dir / "metadata.json"
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    # Calculate statistics
    total_chars = len(full_corpus)
    total_lines = full_corpus.count('\n')
    num_documents = len(all_documents)
    
    stats = {
        'num_documents': num_documents,
        'total_chars': total_chars,
        'total_lines': total_lines,
        'total_size_mb': total_chars / (1024 * 1024),
        'avg_chars_per_doc': total_chars / num_documents if num_documents > 0 else 0,
        'source': 'Case.law API, CourtListener, Cornell LII'
    }
    
    # Save statistics
    stats_file = output_dir / "statistics.txt"
    with open(stats_file, 'w') as f:
        f.write("Legal Documents Corpus Statistics\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Number of documents: {stats['num_documents']}\n")
        f.write(f"Total characters: {stats['total_chars']:,}\n")
        f.write(f"Total lines: {stats['total_lines']:,}\n")
        f.write(f"Total size: {stats['total_size_mb']:.2f} MB\n")
        f.write(f"Average chars per document: {stats['avg_chars_per_doc']:,.0f}\n")
        f.write(f"Data source: {stats['source']}\n")
    
    print(f"\n✓ Legal documents collection complete!")
    print(f"  - Saved to: {output_file}")
    print(f"  - Number of documents: {num_documents}")
    print(f"  - Total size: {stats['total_size_mb']:.2f} MB")
    print(f"  - Statistics saved to: {stats_file}")
    
    return stats

if __name__ == "__main__":
    collect_legal_documents()

