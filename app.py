import streamlit as st
import json
# from openai import OpenAI  # Temporarily disabled
# from utils.io import load_examples
# from utils.processing import get_transition_from_gpt
# from utils.layout import rebuild_article_with_transitions
# from utils.display import layout_title_and_input, show_output, show_version
# from utils.version import compute_version_hash
# from utils.title_blurb import generate_title_and_blurb
from utils.validate_prompt_compliance import validate_batch

def main():
    st.title("📰 French Transition QA Tool (Milestone 1 Only)")

    st.write("This version disables GPT features so you can test the QA validator without API errors.")

    # 🧪 QA Validator Section
    run_qa_validator_ui()

def run_qa_validator_ui():
    st.header("🧪 Transition QA Validator (Milestone 1)")

    st.write("Paste a list of transition groups below (each group = list of 2–4 French transitions).")
    example = '[["Par ailleurs,", "Par contre,", "Par exemple,"], ["Enfin, une note", "Puis une autre", "Pour conclure,"]]'
    user_input = st.text_area("Input transitions (JSON list of lists)", value=example, height=200)

    if st.button("Run QA Validation"):
        try:
            batch = json.loads(user_input)
            if not isinstance(batch, list) or not all(isinstance(group, list) for group in batch):
                st.error("Please input a valid list of transition groups (list of lists).")
                return
            result = validate_batch(batch)
            st.success("Validation complete!")
            st.subheader("Summary")
            st.json(result["violations_summary"])
            st.subheader("Per Output Details")
            for detail in result["details"]:
                st.markdown(f"**Output {detail['output_id']}**")
                st.write("Transitions:", detail["transitions"])
                st.write("Violations:", detail["violations"])
                st.markdown("---")
        except json.JSONDecodeError:
            st.error("Invalid JSON. Make sure your input is a list of lists.")

if __name__ == '__main__':
    main()
