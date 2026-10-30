import streamlit as st
import requests

st.set_page_config(
    page_title="Language Translation Tool",
    page_icon="🌍"
)

st.title("🌍 Language Translation Tool")
st.write("Translate text into different languages.")

languages = {
    "English": "en",
    "Kannada": "kn",
    "Hindi": "hi",
    "Tamil": "ta",
    "Telugu": "te",
    "Malayalam": "ml",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Japanese": "ja"
}

text = st.text_area("Enter your text")

source_language = st.selectbox(
    "Translate from",
    list(languages.keys()),
    index=0
)

target_language = st.selectbox(
    "Translate into",
    list(languages.keys()),
    index=1
)

if st.button("Translate"):
    if not text.strip():
        st.warning("Please enter some text.")

    elif source_language == target_language:
        st.warning("Choose a different target language.")

    else:
        try:
            with st.spinner("Translating..."):
                response = requests.get(
                    "https://api.mymemory.translated.net/get",
                    params={
                        "q": text,
                        "langpair": (
                            f"{languages[source_language]}|"
                            f"{languages[target_language]}"
                        )
                    },
                    timeout=20
                )

                response.raise_for_status()
                data = response.json()

            if data.get("responseStatus") == 200:
                translated_text = data.get(
                    "responseData", {}
                ).get("translatedText", "")

                if translated_text:
                    st.success("Translation completed!")
                    st.subheader("Translated Text")
                    st.write(translated_text)

                    st.download_button(
                        "Download Translation",
                        data=translated_text,
                        file_name="translated_text.txt",
                        mime="text/plain"
                    )
                else:
                    st.warning("No translated text was returned.")
            else:
                st.error(
                    data.get(
                        "responseDetails",
                        "The translation service could not translate this text."
                    )
                )

        except requests.exceptions.Timeout:
            st.error("The translation service took too long. Try again later.")

        except requests.exceptions.RequestException as error:
            st.error("Could not connect to the translation service.")
            st.caption(str(error))

        except (ValueError, KeyError) as error:
            st.error("The translation service returned an unexpected response.")
            st.caption(str(error))

st.divider()
st.caption(
    "CodeAlpha AI Internship Project | Language Translation Tool"
)