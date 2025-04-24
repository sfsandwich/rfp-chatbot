import streamlit as st
import pandas as pd

# --- Load example RFP data files ---
engagement_rfp = pd.read_csv("/mnt/data/Engagement RFP Template - RFP Template.csv")
site_search_rfp = pd.read_csv("/mnt/data/RFP Questions_AI-Powered Site Search LM - Scalability and Redundancy.csv")

# --- Function to generate RFP spreadsheet ---
def generate_rfp_for_tool(tool_type: str) -> pd.DataFrame:
    if tool_type.lower() == "engagement":
        questions = engagement_rfp.iloc[2:, 0].dropna().reset_index(drop=True)
    elif tool_type.lower() in ["site search", "search"]:
        questions = site_search_rfp.iloc[:, 0].dropna().reset_index(drop=True)
    else:
        return pd.DataFrame({"Error": ["Unknown tool type specified."]})

    return pd.DataFrame({
        "Question": questions,
        "Self Score (0-4)": "",
        "Experience (0-4)": "",
        "Detailed Answer": "",
        "Attachments": ""
    })

# --- Streamlit Chatbot-style UI ---
st.title("RFP Chatbot Assistant")
st.write("Chat with the assistant to generate a custom RFP template based on the type of tool you're sourcing.")

# Initialize session state for conversation
if "step" not in st.session_state:
    st.session_state.step = 0
if "tool_type" not in st.session_state:
    st.session_state.tool_type = ""

# Step 1: Ask for tool type
if st.session_state.step == 0:
    st.subheader("What kind of tool are you sourcing?")
    tool_input = st.text_input("Example: Engagement, Site Search, CDP, ESP")
    if st.button("Next") and tool_input:
        st.session_state.tool_type = tool_input
        st.session_state.step = 1
        st.experimental_rerun()

# Step 2: Show RFP output
elif st.session_state.step == 1:
    st.subheader(f"Generating RFP for: {st.session_state.tool_type}")
    rfp_df = generate_rfp_for_tool(st.session_state.tool_type)

    if "Error" in rfp_df.columns:
        st.error(rfp_df["Error"].iloc[0])
    else:
        st.dataframe(rfp_df)
        st.download_button(
            label="Download RFP as CSV",
            data=rfp_df.to_csv(index=False),
            file_name=f"{st.session_state.tool_type}_rfp.csv",
            mime="text/csv"
        )

    if st.button("Start Over"):
        st.session_state.step = 0
        st.session_state.tool_type = ""
        st.experimental_rerun()
