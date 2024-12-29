import os
import streamlit as st
from txt_parser import file_parser
from zebra_pdf import generate_pdf
from concat_pdf import merge_pdf


def main():
    # make sure the directories exist
    os.makedirs('queue', exist_ok=True)
    os.makedirs('zebras_pdf', exist_ok=True)
    # Configure the Streamlit page
    st.set_page_config(page_title="Zebra Label", page_icon=":zebra_face:", layout="wide")
    
    # Add a title and description
    st.title("Zebra Label PDF Generator")
    st.write("Upload a `.txt` file containing Zebra label data to generate a PDF.")

    # File uploader to upload the `.txt` file
    uploaded_file = st.file_uploader("Upload your Zebra Label .txt file", type=["txt"], accept_multiple_files=False)
    
    # Check if a file is uploaded
    if uploaded_file is not None:
        st.success("File uploaded successfully!")
        
        # Read and display the content of the file
        file_content = uploaded_file.read().decode("utf-8")

        # Verify if the file content is correct
        for line in file_content:
            if '^XA' in line:
                st.success("File content is correct!")
                break
        
        batch_files, now = file_parser(file_content)

        with st.spinner("Generating PDF..."):

            batch_files_pdf, now = generate_pdf(batch_files, now)

            merge_pdf(batch_files_pdf, now)

        st.success("PDF generated successfully!")
        with open(f"zebras_pdf/{now}_zebra_labels.pdf", "rb") as pdf_file:
            st.download_button(
                label="Download PDF",
                data=pdf_file,
                file_name=f"{now}_zebra_labels.pdf",
                mime="application/pdf"
            )

            # Delete the txt and pdf files that start with the same timestamp of now
            for file in os.listdir("queue"):
                if file.startswith(str(now)):
                    os.remove(f"queue/{file}")
            for file in os.listdir("zebras_pdf"):
                if file.startswith(str(now)):
                    os.remove(f"zebras_pdf/{file}")


if __name__ == "__main__":
    main()