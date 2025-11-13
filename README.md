# 📚 AI Research Paper Analyzer

An intelligent web application built with Streamlit that allows users to upload research papers (PDFs), extract AI-powered summaries at multiple levels, and compare multiple papers to identify agreements, contradictions, and research gaps.

## 🎯 Features

### 📤 Upload Paper
- Upload multiple research PDFs at once
- Automatic text extraction from PDFs
- Mock AI analysis pipeline (ready for API integration)
- Processing status tracking with progress bar

### 📚 Research Library
- View all uploaded papers with metadata
- Display statistics (total papers, analyzed count, categories)
- Executive summaries of each paper
- Section-wise breakdowns (Introduction, Methods, Results, Discussion)
- Key findings extraction
- Paper metadata (authors, year, category)

### 🔬 Compare Papers
- Select 2-5 papers for side-by-side analysis
- Identify common themes across papers
- Find areas of agreement
- Detect contradictions with conflicting viewpoints
- Highlight research gaps with potential impact assessment
- Display unique contributions from each paper

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/UrjaSahni/ai-research.git
cd ai-research
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
ai-research/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── .streamlit/
│   └── config.toml          # Streamlit configuration
└── README.md                # This file
```

## 📦 Dependencies

- **streamlit** - Web framework for data apps
- **PyPDF2** - PDF text extraction
- **pandas** - Data manipulation
- **numpy** - Numerical computations
- **requests** - HTTP library
- **python-dotenv** - Environment variable management

## 🛠️ Configuration

The application settings are defined in `.streamlit/config.toml`:
- Theme colors (primary, background, secondary)
- Upload size limits (200MB)
- Server settings
- Logger configuration

## 📝 Usage

### Uploading Papers
1. Go to "Upload Paper" tab
2. Select one or multiple PDF files
3. Click "Analyze Papers"
4. Wait for processing to complete

### Viewing Library
1. Go to "Library" tab
2. See all uploaded papers with statistics
3. Click on any paper to expand and view details
4. View executive summary, key findings, and sections

### Comparing Papers
1. Go to "Compare Papers" tab
2. Select 2-5 papers from the multi-select dropdown
3. Click "Compare Selected Papers"
4. View analysis results including:
   - Common themes
   - Agreements
   - Contradictions
   - Research gaps
   - Unique contributions

## 🔌 API Integration

The application currently uses mock AI analysis functions. To integrate with real AI APIs:

1. Update `analyze_paper()` function in `app.py` to call your LLM API (OpenAI, Hugging Face, etc.)
2. Update `compare_papers()` function for paper comparison logic
3. Add your API keys to environment variables

### Example with OpenAI:
```python
import openai

def analyze_paper(title, text):
    # Use OpenAI API for paper analysis
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"Analyze this paper: {text}"}]
    )
    return parse_response(response)
```

### Hugging Face Integration (Current Setup):

This application now uses **Hugging Face Mistral-7B** for AI-powered paper analysis.

#### Setup Instructions:

1. **Get your Hugging Face API key:**
   - Visit [Hugging Face](https://huggingface.co/settings/tokens)
   - Create a new access token (read-only is sufficient)
   - Copy your token

2. **Configure environment variables:**
   - Create a `.env` file in the root directory (see `.env.example` for reference)
   - Add your API key:
     ```
     HUGGINGFACE_API_KEY=your_token_here
     ```

3. **Run the application:**
   ```bash
   pip install -r requirements.txt
   streamlit run app.py
   ```

#### Features:

- **Executive Summaries**: Concise 100-150 word summaries of research papers
- **Key Findings**: Extraction of 3-5 main findings from each paper
- **Methodology Analysis**: 50-100 word breakdown of research methods
- **Paper Comparison**: AI-powered identification of agreements, contradictions, and research gaps

#### API Details:

- **Model**: Mistral-7B-Instruct-v0.1
- **Provider**: Hugging Face Inference API
- **Response Time**: ~30 seconds per paper (may vary)
- **Rate Limits**: Depends on your Hugging Face account tier

#### Troubleshooting:

- **Invalid API Key**: Ensure your token is correctly set in `.env` file
- **API Timeout**: Check your internet connection and Hugging Face service status
- **Rate Limit Exceeded**: Wait before making new requests or upgrade your HF account

## 🌐 Deployment

### Deploy on Streamlit Cloud

1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://share.streamlit.io/)
3. Click "New app"
4. Select your repository, branch, and `app.py`
5. Click "Deploy"

### Deploy on Other Platforms

The app can also be deployed on:
- Heroku
- AWS
- Google Cloud Platform
- Railway
- PythonAnywhere

## 📊 Session State Management

The application uses Streamlit's session state to maintain:
- Uploaded papers list
- Comparison results
- User selections across page navigation

## ⚙️ Key Functions

### `extract_pdf_text(pdf_file)`
Extracts text from uploaded PDF files

### `analyze_paper(title, text)`
Generates analysis for a single paper (mock function - replace with API call)

### `compare_papers(selected_papers)`
Performs comparative analysis on multiple papers

## 🎨 UI Components

- **Sidebar Navigation**: Easy page switching with radio buttons
- **Expandable Sections**: View paper details without clutter
- **Multi-select Dropdowns**: Select multiple papers for comparison
- **Progress Bars**: Visual feedback during processing
- **Metrics**: Display key statistics
- **Columns**: Responsive layout for different content types

## 🚨 Error Handling

- PDF extraction errors are caught and logged
- User-friendly error messages for failed uploads
- Validation of paper selection (minimum 2 papers required)

## 📝 Future Enhancements

- [ ] Database integration for paper persistence
- [ ] User authentication and roles
- [ ] Advanced filtering and search
- [ ] Export results to PDF/CSV
- [ ] Integration with research databases
- [ ] Real-time collaboration features
- [ ] Advanced NLP for better paper analysis
- [ ] Citation network visualization

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Urja Sahni**
- GitHub: [@UrjaSahni](https://github.com/UrjaSahni)
- TIET Student (BTech ECE)

## 🙏 Acknowledgments

- Streamlit team for the amazing framework
- PyPDF2 for PDF handling
- All contributors and testers

## 📧 Support

For questions, issues, or suggestions, please open an issue on GitHub or contact the maintainer.

---

**Last Updated**: November 2025
**Version**: 1.0
