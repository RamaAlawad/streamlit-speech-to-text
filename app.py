import streamlit as st
import speech_recognition as sr
import tempfile
import os
from st_audiorec import st_audiorec
import wave

def main():
    st.set_page_config(
        page_title="🎤 Transformation of Speach to text ",
        page_icon="🎤",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    #  CSS
    st.markdown("""
<style>
.main-header {
    text-align: center;
    color: #EAEAEA; /* لون الخط فاتح */
    font-size: 3rem;
    margin-bottom: 2rem;
}

/* صندوق النتائج */
.result-box {
    background-color: #1e2a38; /* داكن أزرق رمادي */
    color: #EAEAEA; /* نص فاتح */
    padding: 1.5rem;
    border-radius: 10px;
    border-left: 5px solid #4FC3F7; /* أزرق سماوي */
    margin: 1rem 0;
    direction: rtl;
    text-align: right;
}

/* صندوق النجاح */
.success-box {
    background-color: #1b3b2f; /* أخضر داكن */
    color: #d4f7e1; /* أخضر فاتح للنص */
    padding: 1rem;
    border-radius: 5px;
    border: 1px solid #28a745; /* أخضر لامع */
}

/* صندوق الخطأ */
.error-box {
    background-color: #3b1e1e; /* أحمر داكن */
    color: #f8d7da; /* نص وردي فاتح */
    padding: 1rem;
    border-radius: 5px;
    border: 1px solid #dc3545; /* أحمر لامع */
}

/* تعليمات */
.instructions {
    background-color: #263238; /* رمادي مائل للأزرق */
    color: #EAEAEA; /* نص فاتح */
    padding: 1rem;
    border-radius: 8px;
    margin: 1rem 0;
    border-left: 4px solid #4FC3F7; /* أزرق سماوي */
}
</style>
""", unsafe_allow_html=True)

    
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        language = st.selectbox(
            "🌍 Choose Laguage:",
            options=["ar-SA", "en-US"],
            format_func=lambda x: "🇸🇦 العربية" if x == "ar-SA" else "🇺🇸 English",
            index=0
        )
    
    st.markdown("---")
    
    # تسجيل الصوت
    st.markdown("### 🎙️record your voice:")
    
    # use st_audiorec library
    wav_audio_data = st_audiorec()
    
    # Procces the audio
    if wav_audio_data is not None:
        # show the record
        st.audio(wav_audio_data, format='audio/wav')
        
        # transformation the audio
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Transformat the audio", 
                         type="primary", 
                         use_container_width=True):
                
                with st.spinner("⏳ Converting audio to text..."):
                    result = transcribe_audio(wav_audio_data, language)
                    
                    if result["success"]:
                        st.markdown('''
                        <div class="success-box">
                            <h4>Transfer successful!✅ </h4>
                        </div>
                        ''', unsafe_allow_html=True)
                        
                        st.markdown(f'''
                        <div class="result-box">
                            <h4>Converted text:📝 </h4>
                            <p style="font-size: 1.3rem; line-height: 2; font-weight: 500;">{result["text"]}</p>
                        </div>
                        ''', unsafe_allow_html=True)
                        
                        #copy the text choice
                        st.text_area("copy the text📋", value=result["text"], height=100)
                        
                    else:
                        st.markdown(f'''
                        <div class="error-box">
                            <h4>An error occurred:❌</h4>
                            <p>{result["error"]}</p>
                        </div>
                        ''', unsafe_allow_html=True)
    
    # Additional Information
    with st.expander("ℹ️ Important Tips and Information"):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            **🎯 Tips for Best Results:**
            - Speak clearly and slowly
            - Avoid ambient noise
            - Use a good-quality microphone
            - Move closer to the microphone
            - Use short, clear sentences
            """)

        with col2:
            st.markdown("""
            **🛠️ Technical Information:**
            - 🌍 Arabic and English Support
            - 🔗 Requires an Internet connection
            - 🎤 Works with all types of microphones
            - 🖥️ Compatible with all modern browsers
            - 🔒 Secure - Recordings are not saved
            """)

def transcribe_audio(audio_data, language):
    """
        Translate audio to text using Google Speech Recognition
    """
    try:
       
        recognizer = sr.Recognizer()
        
        # Temporarily save the audio file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            temp_file.write(audio_data)
            temp_file_path = temp_file.name
        
        try:
            # Read the audio file
            with sr.AudioFile(temp_file_path) as source:
                # Improve sound quality
                recognizer.adjust_for_ambient_noise(source, duration=1.0)
                
                # Audio recording
                audio = recognizer.record(source)
                
               # Convert audio to text
                if language == "ar-SA":
                    text = recognizer.recognize_google(audio, language="ar-SA")
                else:
                    text = recognizer.recognize_google(audio, language="en-US")
                
                return {
                    "success": True,
                    "text": text,
                    "language": language
                }
                
        finally:
            # Delete the temroarily audio
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
        
    except sr.UnknownValueError:
        return {
            "success": False,
            "error": "😕 The speech was not recognized clearly. Try again and make sure the audio is clear."
        }
    except sr.RequestError as e:
        return {
            "success": False,
            "error": f"🌐 خطأ في الاتصال بخدمة التعرف على الكلام. تأكد من اتصال الإنترنت: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"⚠️ An unexpected error occurred: {str(e)}"
        }

if __name__ == "__main__":
    main()