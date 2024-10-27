import streamlit as st
import requests
from PIL import Image
from io import BytesIO

def get_magic_loop_data(name):
    url = 'https://magicloops.dev/api/loop/run/ac4ff616-19cb-48b3-9b77-8256af33232e'
    params = {"name": name}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        # Directly return the parsed JSON response
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
        return None

def main():
    # Updated title with emoji and branding
    st.title("✨ InstaRizz Profile Generator ✨")
    st.markdown("*Generate your perfect dating profile in seconds!*")

    # Make the input more engaging
    name = st.text_input("✍️ What's your name?", placeholder="Enter your name here...")

    if st.button("✨ Generate Rizz Profile ✨"):
        if name.strip() == "":
            st.warning("🤔 Hey there! Don't forget to tell us your name.")
            return

        with st.spinner("🌟 Working on your perfect profile..."):
            data = get_magic_loop_data(name)

        if data and "loopOutput" in data:
            loop_output = data["loopOutput"]
            summary = loop_output.get("summary", "")
            opening_sentences = loop_output.get("opening_sentences", [])

            # Profile details in two columns
            col1, col2 = st.columns([1, 1])

            # Profile picture in the left column
            with col1:
                if "Matt" in name:
                    image_path = "images/Matt.jpg"  # Path to Matt's photo
                else:
                    image_path = "images/dummy.png"  # Path to the dummy profile picture

                try:
                    image = Image.open(image_path)
                    st.image(image, caption=f"✨ {name}'s Profile Picture", use_column_width=True)
                except FileNotFoundError:
                    st.warning("📸 Profile picture not found.")

            # Profile details in the right column
            with col2:
                st.subheader("👤 Profile")
                st.write(f"**Name:** {name}")

                st.write("**About Me:**")
                st.write(summary if summary else "Bio coming soon...")

                st.write("**🔥 Best Opening Lines:**")
                if opening_sentences:
                    for line in opening_sentences:
                        st.markdown(f"_{line}_")
                else:
                    st.write("Lines loading...")
        else:
            st.error("😅 Oops! Something went wrong. Let's try that again!")

if __name__ == "__main__":
    main()
