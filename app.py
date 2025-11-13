import streamlit as st
import json
import os
from datetime import datetime
import pypdf
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "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")
HF_API_URL = "https://router.huggingface.co/hf-inference/models/mistral-community/Mistral-7B-Instruct-v0.1"

# Page configuration
st.set_page_config(
    page_title="AI Research Paper Analyzer",
    page_icon="📄",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'papers' not in st.session_state:
    st.session_state.papers = []
if 'comparison_result' not in st.session_state:
    st.session_state.comparison_result = None

# Helper function to query Hugging Face API
@st.cache_data(show_spinner=False)
def query_huggingface(prompt, max_length=512):
    """Query Hugging Face API for text generation"""
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_length,
            "temperature": 0.7,
            "top_p": 0.95
        }
    }
    
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                generated_text = result[0].get('generated_text', '').strip()
                # Remove the prompt from the generated text (Mistral includes prompt in response)
                if generated_text.startswith(prompt):
                    generated_text = generated_text[len(prompt):].strip()
                return generated_text if generated_text else "No response generated"
            return "Invalid response format"
        else:
            return f"API Error: {response.status_code}"
    except Exception as e:
        return f"Error querying API: {str(e)}"

# Extract PDF text
def extract_pdf_text(pdf_file):
    try:
        pdf_reader = pypdf.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text[:5000]  # First 5000 chars
    except:
        return "Error extracting PDF text"

# Analyze paper with Hugging Face
def analyze_paper(title, text):
    st.write("🔄 Analyzing with AI...")
    
    # Create prompts for different analyses
    prompts = {
        "executive_summary": f"""Provide a brief executive summary (100-150 words) of this research paper:
Title: {title}
Content: {text[:1000]}
Summary:""",
        
        "key_findings": f"""List 3-5 key findings from this research paper in bullet points:
Title: {title}
Content: {text[:1000]}
Key Findings:""",
        
        "methodology": f"""Describe the research methodology used in this paper (50-100 words):
Title: {title}
Content: {text[:1000]}
Methodology:"""
    }
    
    results = {}
    for key, prompt in prompts.items():
        response = query_huggingface(prompt, max_length=300)
        # Clean up the response
        results[key] = response.strip() if response else "N/A"
    
    return {
        "id": len(st.session_state.papers) + 1,
        "title": title,
        "authors": ["AI Extracted"],
        "abstract": text[:300] if text else "No content",
        "year": 2024,
        "executive_summary": results.get("executive_summary", "N/A"),
        "key_findings": [f.strip() for f in results.get("key_findings", "N/A").split('\n') if f.strip()],
        "methodology": results.get("methodology", "N/A"),
        "sections": [
            {"title": "Abstract", "summary": text[:200]},
            {"title": "Methodology", "summary": results.get("methodology", "N/A")},
            {"title": "Findings", "summary": results.get("key_findings", "N/A")}
        ],
        "keywords": ["AI", "Research"],
        "category": "Computer Science",
        "status": "completed"
    }

# Compare papers with AI
def compare_papers(selected_papers):
    st.write("🔄 Comparing papers with AI...")
    
    papers_text = "\n".join([f"{p['title']}: {p['executive_summary'][:200]}" for p in selected_papers])
    
    prompts = {
        "agreements": f"""Find 2-3 areas of agreement between these research papers:
{papers_text}
Agreements:""",
        
        "contradictions": f"""Identify any contradictions or differences in these papers:
{papers_text}
Contradictions:""",
        
        "gaps": f"""What research gaps can be identified from these papers?
{papers_text}
Research Gaps:"""
    }
    
    results = {}
    for key, prompt in prompts.items():
        response = query_huggingface(prompt, max_length=400)
        results[key] = response.strip() if response else "N/A"
    
    return {
        "papers": selected_papers,
        "analysis": {
            "common_themes": ["AI", "Research", "Analysis"],
            "agreements": [
                {
                    "title": "Common Research Focus",
                    "description": results.get("agreements", "Papers share similar research interests"),
                    "papers": [p["title"] for p in selected_papers]
                }
            ],
            "contradictions": [
                {
                    "title": "Methodological Differences",
                    "description": results.get("contradictions", "Papers use different approaches"),
                    "conflicting_views": [v.strip() for v in results.get("contradictions", "").split('\n') if v.strip()]
                }
            ],
            "research_gaps": [
                {
                    "gap": results.get("gaps", "Further research needed"),
                    "potential_impact": "Addressing these gaps could advance the field"
                }
            ],
            "unique_contributions": [
                {"paper": p["title"], "contribution": p.get("executive_summary", "")[:100]} 
                for p in selected_papers
            ]
        }
    }

# Sidebar
st.sidebar.title("📚 ResearchAI")
st.sidebar.write("Powered by Hugging Face 🤗")
page = st.sidebar.radio("Navigate", ["Library", "Upload Paper", "Compare Papers"])

# LIBRARY PAGE
if page == "Library":
    st.title("📚 Research Library")
    
    if not st.session_state.papers:
        st.info("No papers yet. Upload from 'Upload Paper' tab.")
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Papers", len(st.session_state.papers))
        with col2:
            st.metric("Analyzed", len([p for p in st.session_state.papers if p["status"] == "completed"]))
        with col3:
            st.metric("Categories", len(set(p.get("category") for p in st.session_state.papers)))
        
        st.divider()
        
        for paper in st.session_state.papers:
            with st.expander(f"📄 {paper['title']}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    if paper.get('authors'):
                        st.write(f"**Authors:** {', '.join(paper['authors'])}")
                    if paper.get('year'):
                        st.write(f"**Year:** {paper['year']}")
                
                with col2:
                    st.success("✓ Analyzed") if paper['status'] == 'completed' else st.warning("⟳ Processing")
                
                if paper.get('executive_summary'):
                    st.write("**Executive Summary:**")
                    st.write(paper['executive_summary'])
                
                if paper.get('key_findings'):
                    st.write("**Key Findings:**")
                    for finding in paper['key_findings']:
                        if finding.strip():
                            st.write(f"• {finding}")

# UPLOAD PAGE
elif page == "Upload Paper":
    st.title("📤 Upload Research Papers")
    st.write("Upload PDFs for AI-powered analysis using Hugging Face")
    
    uploaded_files = st.file_uploader("Choose PDF(s)", type="pdf", accept_multiple_files=True)
    
    if uploaded_files:
        if st.button("🔍 Analyze with HF AI", type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for idx, file in enumerate(uploaded_files):
                status_text.text(f"Processing: {file.name}")
                pdf_text = extract_pdf_text(file)
                paper_data = analyze_paper(file.name.replace('.pdf', ''), pdf_text)
                st.session_state.papers.append(paper_data)
                progress_bar.progress((idx + 1) / len(uploaded_files))
            
            status_text.empty()
            progress_bar.empty()
            st.success(f"✓ Analyzed {len(uploaded_files)} paper(s) with Hugging Face!")
            st.balloons()

# COMPARE PAGE
elif page == "Compare Papers":
    st.title("🔬 Compare Research Papers")
    
    if len(st.session_state.papers) < 2:
        st.warning("Upload at least 2 papers first.")
    else:
        titles = [p['title'] for p in st.session_state.papers]
        selected_titles = st.multiselect("Select papers (2-5)", titles, max_selections=5)
        
        if len(selected_titles) >= 2:
            if st.button("🔍 Compare with AI", type="primary"):
                with st.spinner("AI is comparing papers..."):
                    selected = [p for p in st.session_state.papers if p['title'] in selected_titles]
                    st.session_state.comparison_result = compare_papers(selected)
                st.success("✓ Comparison complete!")
        
        if st.session_state.comparison_result:
            result = st.session_state.comparison_result
            analysis = result['analysis']
            
            st.divider()
            st.subheader("📈 AI Comparison Analysis")
            
            st.write("### Papers Analyzed")
            for idx, p in enumerate(result['papers'], 1):
                st.write(f"{idx}. **{p['title']}**")
            
            st.divider()
            
            if analysis.get('agreements'):
                st.write("### ✅ Areas of Agreement")
                for agreement in analysis['agreements']:
                    st.write(f"**{agreement['title']}**")
                    st.write(agreement['description'])
            
            if analysis.get('contradictions'):
                st.write("### ⚠️ Contradictions")
                for contradiction in analysis['contradictions']:
                    st.write(f"**{contradiction['title']}**")
                    st.write(contradiction['description'])
            
            if analysis.get('research_gaps'):
                st.write("### 🔍 Research Gaps")
                for gap in analysis['research_gaps']:
                    st.write(f"**{gap['gap']}**")
                    st.write(f"Impact: {gap['potential_impact']}")
            
            if st.button("🔄 New Comparison"):
                st.session_state.comparison_result = None
                st.rerun()

st.sidebar.divider()
st.sidebar.caption("AI Research Paper Analyzer v2.0 - HF Edition")
st.sidebar.caption("Powered by Mistral-7B via Hugging Face")
