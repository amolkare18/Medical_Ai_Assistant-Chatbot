from utils.api import upload_pdfs
import streamlit as st

def render_uploader():
    st.sidebar.subheader("Upload your Medical PDF documents:")
    uploaded_files = st.sidebar.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)

    if st.sidebar.button("Upload PDFs") and uploaded_files is not None:
        if uploaded_files:
            response = upload_pdfs(uploaded_files)
            if response.status_code == 200:
                st.sidebar.success("Files uploaded successfully!")
            else:
                st.sidebar.error(f"Error uploading files: {response.text}")
        else:
            st.warning("Please select at least one PDF file to upload.")
