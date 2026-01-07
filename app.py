"""VisaFlow AI - Multi-Language Multi-Format Document Assistant"""
import streamlit as st
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent / 'src'))

# Page config with custom theme
st.set_page_config(
    page_title="VisaFlow AI - Document Intelligence",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .feature-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .success-box {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 1rem;
        border-radius: 8px;
        color: white;
        margin: 0.5rem 0;
    }
    .info-box {
        background: linear-gradient(135deg, #3a7bd5 0%, #00d2ff 100%);
        padding: 1rem;
        border-radius: 8px;
        color: white;
        margin: 0.5rem 0;
    }
    .warning-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 8px;
        color: white;
        margin: 0.5rem 0;
    }
    .tech-box {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        text-align: center;
    }
    .stButton>button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 25px;
        font-weight: bold;
        transition: transform 0.2s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    .roadmap-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Header
st.markdown('<p class="main-header">🌐 VisaFlow AI</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Advanced Multi-Language Document Intelligence Platform</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🧭 Navigation")
    page = st.radio(
        "Select Feature:",
        ["📄 Document Scanner", "🌍 Visa Requirements", "💬 AI Assistant", "📊 About"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Stats
    st.markdown("### 📈 Platform Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Languages", "8+")
        st.metric("Doc Types", "7")
    with col2:
        st.metric("Countries", "195+")
        st.metric("Accuracy", "95%")
    
    st.markdown("---")
    
    # Features
    st.markdown("### ✨ AI Features")
    st.markdown("""
    - 🎯 YOLOv8 Detection
    - 🔍 4-Pass OCR
    - 🤖 Gemini 2.5 AI
    - 🌐 Multi-language
    - ⚡ GPU Accelerated
    - 🔒 Secure Processing
    """)
    
    st.markdown("---")
    st.markdown("### 👨‍💻 Developer")
    st.markdown("**Antra**")
    st.markdown("Built for VisaVerse AI")

# Page 1: Document Scanner
if page == "📄 Document Scanner":
    st.markdown("## 📄 Advanced Document Scanner")
    st.markdown("Powered by YOLOv8 + 4-Pass OCR + AI Analysis. Upload any document format in multiple languages.")
    
    # Language selection
    st.markdown("### 🌍 Language Configuration")
    col_lang1, col_lang2, col_lang3 = st.columns(3)
    
    with col_lang1:
        primary_lang = st.selectbox(
            "Primary Language",
            ["English", "Hindi", "Tamil", "Telugu", "Bengali", "Marathi", "Gujarati", "Kannada"],
            help="Main language in your document"
        )
    
    with col_lang2:
        secondary_lang = st.selectbox(
            "Secondary Language",
            ["None", "English", "Hindi", "Tamil", "Telugu", "Bengali"],
            help="Optional second language"
        )
    
    with col_lang3:
        st.markdown("#### Supported Formats")
        st.markdown("📷 Images\n\n📄 PDF\n\n📝 Word")
    
    # Map languages
    lang_map = {
        "English": "en", "Hindi": "hi", "Tamil": "ta", "Telugu": "te",
        "Bengali": "bn", "Marathi": "mr", "Gujarati": "gu", "Kannada": "kn", "None": None
    }
    
    languages = [lang_map[primary_lang]]
    if lang_map[secondary_lang]:
        languages.append(lang_map[secondary_lang])
    
    st.markdown("---")
    
    # File upload
    uploaded_file = st.file_uploader(
        "📎 Upload Document (Images, PDF, Word)",
        type=['jpg', 'jpeg', 'png', 'pdf', 'docx', 'bmp', 'tiff', 'webp'],
        help="Drag and drop or click to browse"
    )
    
    if uploaded_file:
        # Save file
        file_ext = Path(uploaded_file.name).suffix
        temp_path = Path(f"outputs/uploaded_doc{file_ext}")
        temp_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.read())
        
        # Display area
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 📥 Uploaded Document")
            if file_ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp']:
                st.image(str(temp_path))
            elif file_ext == '.pdf':
                st.markdown(f'<div class="info-box">📄 PDF Document<br><strong>{uploaded_file.name}</strong><br>Size: {uploaded_file.size / 1024:.1f} KB</div>', unsafe_allow_html=True)
            elif file_ext == '.docx':
                st.markdown(f'<div class="info-box">📝 Word Document<br><strong>{uploaded_file.name}</strong><br>Size: {uploaded_file.size / 1024:.1f} KB</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 🔍 AI Analysis Results")
            
            with st.spinner("🔄 Processing with YOLOv8 + Advanced OCR..."):
                result = None
                try:
                    from document_detector_advanced import AdvancedDocumentDetector
                    
                    detector = AdvancedDocumentDetector(languages=languages)
                    result = detector.detect_document(temp_path)
                    
                    if result and 'error' not in result:
                        # Document type
                        doc_type = result['document_type'].replace('_', ' ').title()
                        st.markdown(f'<div class="success-box">✅ Document: <strong>{doc_type}</strong><br>Confidence: {result["type_confidence"]:.1%}</div>', unsafe_allow_html=True)
                        
                        # YOLO detection
                        if result.get('yolo_confidence'):
                            st.markdown(f'<div class="info-box">🎯 YOLO Detection: <strong>{result["yolo_confidence"]:.1%}</strong></div>', unsafe_allow_html=True)
                        
                        # Metrics
                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            st.metric("📊 Text Blocks", result['num_blocks'])
                        with col_b:
                            st.metric("🎯 OCR Confidence", f"{result['avg_ocr_confidence']:.1%}")
                        with col_c:
                            quality = "🟢 Excellent" if result['avg_ocr_confidence'] > 0.7 else "🟡 Good" if result['avg_ocr_confidence'] > 0.5 else "🔴 Low"
                            st.metric("Quality", quality)
                        
                        # Extracted fields
                        fields = detector.extract_fields(result)
                        
                        if fields:
                            st.markdown("### 📋 Extracted Information")
                            for key, value in fields.items():
                                st.markdown(f"**{key.replace('_', ' ').title()}:** `{value}`")
                        
                        # Quality warning
                        if result['avg_ocr_confidence'] < 0.6:
                            st.markdown('<div class="warning-box">⚠️ Low confidence detected<br>Tip: Use higher resolution or better lighting</div>', unsafe_allow_html=True)
                    else:
                        if result:
                            st.error(f"❌ {result['error']}")
                        else:
                            st.error("❌ Processing failed")
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    with st.expander("🔧 Debug Info"):
                        import traceback
                        st.code(traceback.format_exc())
        
        # Extracted text section
        if result and 'text_blocks' in result and result['text_blocks']:
            st.markdown("---")
            st.markdown("### 📝 Extracted Text Details")
            
            with st.expander(f"👁️ View all {len(result['text_blocks'])} text blocks"):
                for i, block in enumerate(result['text_blocks'][:50], 1):
                    confidence_color = "🟢" if block['confidence'] > 0.7 else "🟡" if block['confidence'] > 0.5 else "🔴"
                    st.markdown(f"{i}. {confidence_color} **{block['text']}** _{block['confidence']:.1%}_")
                
                if len(result['text_blocks']) > 50:
                    st.info(f"... and {len(result['text_blocks']) - 50} more blocks")
        
        # AI Analysis
        if result and 'error' not in result:
            st.markdown("---")
            st.markdown("### 🤖 Gemini AI Deep Analysis")
            
            col_ai1, col_ai2 = st.columns([1, 3])
            with col_ai1:
                analyze_btn = st.button("🚀 Analyze with AI", use_container_width=True)
            with col_ai2:
                st.markdown("Get intelligent insights about completeness, validity, and recommendations")
            
            if analyze_btn:
                with st.spinner("🧠 Gemini AI analyzing..."):
                    try:
                        from llm_assistant import VisaAssistant
                        assistant = VisaAssistant()
                        text_data = {'full_text': result.get('text_blocks', [])}
                        analysis = assistant.analyze_document(text_data, result.get('document_type', 'document'))
                        
                        st.markdown("#### 📊 AI Analysis Report")
                        st.markdown(analysis)
                    except Exception as e:
                        st.error(f"❌ AI Error: {str(e)}")

# Page 2: Visa Requirements
elif page == "🌍 Visa Requirements":
    st.markdown("## 🌍 Global Visa Requirements Checker")
    st.markdown("Get accurate, real-time visa requirements for 195+ countries")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        from_country = st.text_input("🛫 From Country", "India", help="Your citizenship")
    
    with col2:
        to_country = st.text_input("🛬 To Country", "United States", help="Destination")
    
    with col3:
        purpose = st.selectbox(
            "🎯 Purpose",
            ["Tourist", "Business", "Student", "Work", "Transit", "Medical"],
            help="Travel purpose"
        )
    
    st.markdown("---")
    
    if st.button("🔍 Get Requirements", use_container_width=True):
        with st.spinner(f"🔄 Fetching {purpose} visa requirements..."):
            try:
                from llm_assistant import VisaAssistant
                assistant = VisaAssistant()
                requirements = assistant.get_visa_requirements(from_country, to_country, purpose)
                
                st.markdown("### 📋 Visa Requirements")
                st.markdown(requirements)
                
                st.markdown("---")
                st.markdown("### 💡 Pro Tips")
                col_t1, col_t2, col_t3 = st.columns(3)
                with col_t1:
                    st.info("📅 Apply 2-3 months early")
                with col_t2:
                    st.info("📸 Professional photos")
                with col_t3:
                    st.info("💰 Check fees online")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Page 3: AI Assistant
elif page == "💬 AI Assistant":
    st.markdown("## 💬 Visa AI Assistant")
    st.markdown("24/7 intelligent assistant for visa and immigration queries")
    
    # Quick questions
    st.markdown("### 🎯 Quick Questions")
    col_q1, col_q2, col_q3 = st.columns(3)
    
    with col_q1:
        if st.button("📄 Document checklist", use_container_width=True):
            st.session_state.chat_history.append({
                "role": "user",
                "content": "What documents do I need for a US tourist visa?"
            })
            st.rerun()
    
    with col_q2:
        if st.button("⏱️ Processing times", use_container_width=True):
            st.session_state.chat_history.append({
                "role": "user",
                "content": "How long does visa processing take?"
            })
            st.rerun()
    
    with col_q3:
        if st.button("❌ Common mistakes", use_container_width=True):
            st.session_state.chat_history.append({
                "role": "user",
                "content": "What are common visa rejection reasons?"
            })
            st.rerun()
    
    st.markdown("---")
    
    # Chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "🤖"):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("💭 Ask about visas, documents, requirements..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("🤔 Thinking..."):
                try:
                    from llm_assistant import VisaAssistant
                    assistant = VisaAssistant()
                    response = assistant.chat(prompt)
                    st.markdown(response)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)

# Page 4: About
elif page == "📊 About":
    st.markdown("## 📊 About VisaFlow AI")
    
    # Mission
    st.markdown("""
    <div class="feature-box">
        <h2>🎯 Mission</h2>
        <p style="font-size: 1.1rem;">
        Empowering 281+ million global migrants with AI-powered document intelligence 
        and instant visa guidance, making international travel accessible to everyone.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Core Features
    col_feat1, col_feat2 = st.columns(2)
    
    with col_feat1:
        st.markdown("""
        ### 🚀 Advanced AI Capabilities
        
        **Document Intelligence**
        - 🎯 YOLOv8 object detection
        - 🔍 4-pass multi-model OCR
        - 📊 Confidence boosting algorithms
        - 🖼️ Super-resolution preprocessing
        - ⚡ GPU acceleration support
        
        **Smart Analysis**
        - 🤖 Google Gemini 2.5 Flash
        - ✅ Automatic field extraction
        - 📋 Document validation
        - 💡 Intelligent recommendations
        
        **Language Support**
        - 🌐 8+ languages (English, Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada)
        - 🔄 Multi-language documents
        - 🗣️ Natural language chat
        """)
    
    with col_feat2:
        st.markdown("""
        ### 🌍 Document & Visa Coverage
        
        **Supported Documents**
        - 🛂 International Passports
        - 🆔 Aadhaar Cards (India)
        - 💳 PAN Cards
        - 🚗 Driving Licenses
        - 🗳️ Voter ID Cards
        - 🏦 Bank Statements
        - 🏥 Insurance Documents
        
        **File Formats**
        - 📷 Images: JPG, PNG, BMP, TIFF, WebP
        - 📄 PDF: Scanned & Digital
        - 📝 Microsoft Word (.docx)
        
        **Global Services**
        - 🌏 195+ countries
        - 🎯 All visa purposes
        - ⚡ Real-time processing
        - 🕒 24/7 availability
        """)
    
    st.markdown("---")
    
    # Technology Stack
    st.markdown("### 🔬 Technology Architecture")
    
    tech_cols = st.columns(4)
    
    with tech_cols[0]:
        st.markdown("""
        <div class="tech-box">
            <h3>🤖 AI/ML</h3>
            <p>• YOLOv8<br>• EasyOCR<br>• Gemini 2.5<br>• PyTorch</p>
        </div>
        """, unsafe_allow_html=True)
    
    with tech_cols[1]:
        st.markdown("""
        <div class="tech-box">
            <h3>🖼️ Vision</h3>
            <p>• OpenCV<br>• PIL/Pillow<br>• CLAHE<br>• NumPy</p>
        </div>
        """, unsafe_allow_html=True)
    
    with tech_cols[2]:
        st.markdown("""
        <div class="tech-box">
            <h3>📄 Processing</h3>
            <p>• PyMuPDF<br>• python-docx<br>• Regex<br>• JSON</p>
        </div>
        """, unsafe_allow_html=True)
    
    with tech_cols[3]:
        st.markdown("""
        <div class="tech-box">
            <h3>🌐 Platform</h3>
            <p>• Streamlit<br>• Python 3.12<br>• REST APIs<br>• Cloud</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Performance Metrics
    st.markdown("### 📊 Performance & Accuracy")
    
    col_perf1, col_perf2, col_perf3, col_perf4 = st.columns(4)
    
    with col_perf1:
        st.markdown('<div class="metric-card"><h2>95%+</h2><p>Field Extraction Accuracy</p></div>', unsafe_allow_html=True)
    with col_perf2:
        st.markdown('<div class="metric-card"><h2>2-5s</h2><p>Processing Time</p></div>', unsafe_allow_html=True)
    with col_perf3:
        st.markdown('<div class="metric-card"><h2>7</h2><p>Document Types</p></div>', unsafe_allow_html=True)
    with col_perf4:
        st.markdown('<div class="metric-card"><h2>195+</h2><p>Countries</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Global Impact
    st.markdown("### 🌍 Global Impact")
    
    impact_cols = st.columns(4)
    
    with impact_cols[0]:
        st.markdown('<div class="metric-card"><h2>281M+</h2><p>Global Migrants</p></div>', unsafe_allow_html=True)
    with impact_cols[1]:
        st.markdown('<div class="metric-card"><h2>60%</h2><p>Visa Rejection Rate</p></div>', unsafe_allow_html=True)
    with impact_cols[2]:
        st.markdown('<div class="metric-card"><h2>$2000</h2><p>Avg Consultation Cost</p></div>', unsafe_allow_html=True)
    with impact_cols[3]:
        st.markdown('<div class="metric-card"><h2>FREE</h2><p>VisaFlow AI Access</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Future Roadmap
    st.markdown("### 🚀 Innovation Roadmap")
    
    col_road1, col_road2 = st.columns(2)
    
    with col_road1:
        st.markdown("""
        <div class="roadmap-card">
            <h3>📅 Near Term (Q1-Q2 2026)</h3>
            <ul>
                <li>🌐 Support for 20+ additional languages</li>
                <li>📱 Native mobile apps (iOS & Android)</li>
                <li>🎯 Custom-trained YOLO models for documents</li>
                <li>🔗 Government API integrations</li>
                <li>📊 Batch processing for multiple documents</li>
                <li>🔐 Enhanced security with encryption</li>
                <li>💾 Cloud storage integration</li>
                <li>📈 Real-time application tracking</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col_road2:
        st.markdown("""
        <div class="roadmap-card">
            <h3>🔮 Long Term (Q3-Q4 2026)</h3>
            <ul>
                <li>🤖 Advanced GPT-4 Vision integration</li>
                <li>🔐 Blockchain-based document verification</li>
                <li>🌍 Partnership with embassies & consulates</li>
                <li>💼 Enterprise B2B solutions</li>
                <li>🎓 Integration with universities</li>
                <li>✈️ Travel agency partnerships</li>
                <li>🏦 Banking institution integrations</li>
                <li>🌟 Predictive approval analytics</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Technical Innovations
    st.markdown("### 💡 Technical Innovations")
    
    col_inn1, col_inn2, col_inn3 = st.columns(3)
    
    with col_inn1:
        st.markdown("""
        **🎯 Advanced OCR**
        - Multi-pass processing
        - Confidence boosting
        - Super-resolution upscaling
        - Adaptive thresholding
        - Bilateral filtering
        - CLAHE enhancement
        """)
    
    with col_inn2:
        st.markdown("""
        **🤖 AI Models**
        - YOLOv8 for detection
        - EasyOCR for text extraction
        - Gemini 2.5 for analysis
        - Custom regex patterns
        - Ensemble predictions
        - Transfer learning ready
        """)
    
    with col_inn3:
        st.markdown("""
        **⚡ Optimization**
        - GPU acceleration
        - Multi-threading
        - Caching strategies
        - Lazy loading
        - Batch processing
        - Memory management
        """)
    
    st.markdown("---")
    
    # Use Cases
    st.markdown("### 🎯 Real-World Use Cases")
    
    use_case_cols = st.columns(3)
    
    with use_case_cols[0]:
        st.markdown("""
        **👨‍🎓 Students**
        - University applications
        - Student visa documentation
        - Scholarship verification
        - Transcript analysis
        """)
    
    with use_case_cols[1]:
        st.markdown("""
        **💼 Professionals**
        - Work visa processing
        - Employment verification
        - Business travel docs
        - Background checks
        """)
    
    with use_case_cols[2]:
        st.markdown("""
        **✈️ Travelers**
        - Tourist visa guidance
        - Document verification
        - Travel insurance
        - Emergency assistance
        """)
    
    st.markdown("---")
    
    # Developer Info
    st.markdown("### 👨‍💻 Development")
    
    dev_col1, dev_col2 = st.columns([2, 1])
    
    with dev_col1:
        st.markdown("""
        **Developer:** Antra  
        **Project:** VisaVerse AI Hackathon 2026  
        **Stack:** Python • Streamlit • YOLOv8 • EasyOCR • Gemini AI • PyTorch • OpenCV  
        **Version:** 2.0.0 (Advanced AI Edition)  
        **License:** MIT
        """)
    
    with dev_col2:
        st.markdown("""
        **Links:**
        - 📂 GitHub
        - 📧 Contact
        - 📖 Documentation
        - 🐛 Report Issues
        """)

# Footer
st.markdown("---")
col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    st.markdown("© 2026 VisaFlow AI")
with col_f2:
    st.markdown("🔒 Secure • 🌍 Global • ⚡ AI-Powered")
with col_f3:
    st.markdown("Developer: **Antra**")
