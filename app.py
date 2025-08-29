# # artemis_hf_api.py
# import streamlit as st
# import os, json, docx, PyPDF2, re
# from dotenv import load_dotenv
# from huggingface_hub import InferenceClient

# # -------------------
# # Load environment variables
# # -------------------
# print("🔹 Loading environment variables...")
# load_dotenv()

# st.set_page_config(page_title="Artemis - Free Online Career Assistant", layout="wide")
# st.title("🚀 Artemis - Free Online Career Assistant")

# # -------------------
# # Get HF API key
# # -------------------
# HF_API_KEY = os.getenv("HF_API_KEY")
# print(f"🔹 HF_API_KEY found: {'YES' if HF_API_KEY else 'NO'}")

# if not HF_API_KEY:
#     st.error("❌ Hugging Face API key not found. Please set it in your .env file.")

# # HuggingFace client
# client = InferenceClient(api_key=HF_API_KEY)
# MODEL_ID = "HuggingFaceTB/SmolLM3-3B"
# print(f"🔹 Using model: {MODEL_ID}")

# # -------------------
# # Inputs
# # -------------------
# company_name = st.text_input("Company Name")
# job_description = st.text_area("Job Description")

# # -------------------
# # Resume upload
# # -------------------
# uploaded_file = st.file_uploader("Upload Candidate Resume (PDF or DOCX)", type=["pdf", "docx"])
# resume_text = ""

# if uploaded_file:
#     print(f"🔹 Uploaded file type: {uploaded_file.type}")
#     if uploaded_file.type == "application/pdf":
#         pdf_reader = PyPDF2.PdfReader(uploaded_file)
#         resume_text = "\n".join(
#             page.extract_text() for page in pdf_reader.pages if page.extract_text()
#         )
#         print("🔹 Extracted text from PDF resume")
#     elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
#         doc = docx.Document(uploaded_file)
#         resume_text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
#         print("🔹 Extracted text from DOCX resume")
#     else:
#         st.error("Unsupported file format!")
#         print("❌ Unsupported file format")

# # -------------------
# # Helpers
# # -------------------
# def truncate_text(text: str, max_chars: int = 4000) -> str:
#     return text[:max_chars] + ("..." if len(text) > max_chars else "")

# # -------------------
# # Strict JSON Schema (fixed for CoverLetter)
# # -------------------
# STRICT_SCHEMA = {
#     "type": "json_schema",
#     "json_schema": {
#         "name": "artemis_resume_output",
#         "schema": {
#             "type": "object",
#             "additionalProperties": False,
#             "properties": {
#                 "ResumeSuggestions": {
#                     "type": "object",
#                     "additionalProperties": False,
#                     "properties": {
#                         "Projects": {
#                             "type": "array",
#                             "items": {
#                                 "type": "object",
#                                 "properties": {
#                                     "current": {"type": "string"},
#                                     "change": {"type": "string", "maxLength": 120}
#                                 },
#                                 "required": ["current", "change"]
#                             }
#                         },
#                         "Experience": {
#                             "type": "array",
#                             "items": {
#                                 "type": "object",
#                                 "properties": {
#                                     "current": {"type": "string"},
#                                     "change": {"type": "string", "maxLength": 120}
#                                 },
#                                 "required": ["current", "change"]
#                             }
#                         }
#                     },
#                     "required": ["Projects", "Experience"]
#                 },
#                 "CoverLetter": {"type": "string"},   # relaxed
#                 "Summary": {"type": "string"}        # relaxed
#             },
#             "required": ["ResumeSuggestions", "CoverLetter", "Summary"]
#         }
#     }
# }

# # -------------------
# # Generate Suggestions
# # -------------------
# if st.button("Generate Suggestions"):
#     print("🔹 Generate Suggestions button clicked")
#     if not (company_name and job_description and resume_text):
#         st.error("Please fill all fields and upload a resume!")
#         print("❌ Missing input fields")
#     else:
#         with st.spinner("Generating suggestions online..."):
#             print("🔹 Building prompt...")

#             # -------------------
#             # Prompt Template
#             # -------------------
#             prompt = f"""
#             You are Artemis, an intelligent AI career assistant.
#             Your task is to improve the candidate's resume and provide a tailored cover letter + summary.
            
#             **Rules for ResumeSuggestions**:
#             - Output ONLY JSON (no prose).
#             - For each suggestion, map: current resume line/phrase -> a direct, short change (≤20 words).
#             - Prefer concrete metrics, stacks, and scope (e.g., accuracies, speedups, user counts, tech used).
#             - Do NOT invent unverifiable employers; use placeholders like "X%" if numbers are missing.
#             - Keep language concise, factual, and ATS-friendly.
#             - At least 3 crisp suggestions each for Projects and Experience (if relevant content exists).
            
#             **Rules for CoverLetter**:
#             - Write a one-page, professional cover letter tailored to the company and role.
#             - Use a formal, confident, yet approachable tone (avoid clichés like "I am excited").
#             - Focus on skills, impact, and how the candidate fits the JD.
#             - Highlight relevant achievements from the resume (numbers, metrics, scope).
#             - Make it ATS-friendly: simple language, no unnecessary formatting.
#             - Structure:
#               1. Greeting + intent.
#               2. How the candidate’s skills/experience align with the role.
#               3. Why they want to join this company (align with JD).
#               4. Closing with call-to-action.
            
#             **Rules for Summary**:
#             - Write 1–2 lines maximum.
#             - Explain the rationale behind the suggested resume changes.
#             - Be precise, action-oriented, and focused on *alignment with the job description*.
            
#             **Context**:
#             - Company: {company_name}
#             - Job Description: {truncate_text(job_description)}
#             - Candidate Resume: {truncate_text(resume_text)}
            
#             **Final Output Schema (STRICT)**:
#             {{
#               "ResumeSuggestions": {{
#                 "Projects": [{{"current": "string", "change": "string (<20 words)"}}, ...],
#                 "Experience": [{{"current": "string", "change": "string (<20 words)"}}, ...]
#               }},
#               "CoverLetter": "string (full professional cover letter based on resume + JD)",
#               "Summary": "string (one-line rationale of changes)"
#             }}
#             """


#             parsed_output = None
#             raw_output = ""

#             # 1) Try strict JSON schema
#             try:
#                 completion = client.chat.completions.create(
#                     model=MODEL_ID,
#                     messages=[{"role": "user", "content": prompt}],
#                     max_tokens=1200,
#                     response_format=STRICT_SCHEMA,  # strict schema
#                 )
#                 raw_output = completion.choices[0].message.content
#                 print("🔹 Raw model output (schema):", raw_output[:500], "...")
#                 parsed_output = json.loads(raw_output)
#                 print("🔹 Successfully parsed JSON output (schema)")
#             except Exception as e:
#                 print(f"⚠️ Schema-enforced generation failed: {e}")

#                 # 2) Fallback to json_object
#                 if not parsed_output:
#                     try:
#                         completion = client.chat.completions.create(
#                             model=MODEL_ID,
#                             messages=[{"role": "user", "content": prompt}],
#                             max_tokens=1200,
#                             response_format={"type": "json_object"},
#                         )
#                         raw_output = completion.choices[0].message.content
#                         print("🔹 Raw model output (json_object):", raw_output[:500], "...")
#                         parsed_output = json.loads(raw_output)
#                         print("🔹 Successfully parsed JSON output (json_object)")
#                     except Exception as e2:
#                         print(f"⚠️ Direct JSON parsing failed: {e2}")
#                         # 3) Regex fallback
#                         if raw_output:
#                             match = re.search(r"\{.*\}", raw_output, re.DOTALL)
#                             if match:
#                                 try:
#                                     parsed_output = json.loads(match.group(0))
#                                     print("🔹 Successfully extracted JSON via regex")
#                                 except Exception as e3:
#                                     print(f"❌ Regex JSON parse failed: {e3}")

#             # -------------------
#             # Fallback for missing CoverLetter
#             # -------------------
#             if parsed_output and not parsed_output.get("CoverLetter"):
#                 try:
#                     print("⚠️ CoverLetter missing, regenerating...")
#                     cover_prompt = f"""
#                     Write a professional one-page cover letter for:
#                     - Candidate Resume: {truncate_text(resume_text, 3000)}
#                     - Job Description: {truncate_text(job_description, 1500)}
#                     - Company: {company_name}
#                     Keep it ATS-friendly, concise, and aligned with the JD.
#                     """
#                     cover_completion = client.chat.completions.create(
#                         model=MODEL_ID,
#                         messages=[{"role": "user", "content": cover_prompt}],
#                         max_tokens=600
#                     )
#                     parsed_output["CoverLetter"] = cover_completion.choices[0].message.content.strip()
#                 except Exception as e4:
#                     print(f"❌ Fallback CoverLetter generation failed: {e4}")

#             # -------------------
#             # Display
#             # -------------------
#             if not parsed_output:
#                 st.warning("⚠️ Could not parse as JSON. Showing raw output:")
#                 st.code(raw_output if raw_output else "No output")
#             else:
#                 st.success("Suggestions Generated ✅")

#                 with st.expander("🔍 Raw JSON Preview"):
#                     st.code(json.dumps(parsed_output, indent=2))

#                 # Resume Suggestions - CRISP (Projects / Experience only)
#                 with st.expander("📄 Resume Suggestions", expanded=True):
#                     def render_section(title: str, items: list):
#                         st.subheader(title)
#                         if not items:
#                             st.write("- No suggestions.")
#                             return
#                         for item in items:
#                             current = item.get("current", "").strip()
#                             change = item.get("change", "").strip()
#                             if current:
#                                 st.write(f"➡️ **{current}**")
#                             if change:
#                                 st.write(f"🔹 **Change:** {change}")
#                             st.markdown("---")

#                     rs = parsed_output.get("ResumeSuggestions", {})
#                     render_section("Projects", rs.get("Projects", []))
#                     render_section("Experience", rs.get("Experience", []))

#                 # Cover Letter
#                 with st.expander("✉️ Generated Cover Letter"):
#                     st.write(parsed_output.get("CoverLetter", ""))

#                 # Summary
#                 with st.expander("📝 Summary / Feedback"):
#                     st.write(parsed_output.get("Summary", ""))

# artemis_hf_api.py
import streamlit as st
import os, json, docx, PyPDF2, re
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# -------------------
# Load environment variables
# -------------------
print("🔹 Loading environment variables...")
load_dotenv()

st.set_page_config(page_title="Artemis - Free Online Career Assistant", layout="wide")
st.title("🚀 Artemis - Free Online Career Assistant")

# -------------------
# Get HF API key
# -------------------
HF_API_KEY = os.getenv("HF_API_KEY")
print(f"🔹 HF_API_KEY found: {'YES' if HF_API_KEY else 'NO'}")

if not HF_API_KEY:
    st.error("❌ Hugging Face API key not found. Please set it in your .env file.")

# HuggingFace client
client = InferenceClient(api_key=HF_API_KEY)
MODEL_ID = "HuggingFaceTB/SmolLM3-3B"
print(f"🔹 Using model: {MODEL_ID}")

# -------------------
# Inputs
# -------------------
company_name = st.text_input("Company Name")
job_description = st.text_area("Job Description")

# -------------------
# Resume upload
# -------------------
uploaded_file = st.file_uploader("Upload Candidate Resume (PDF or DOCX)", type=["pdf", "docx"])
resume_text = ""

if uploaded_file:
    print(f"🔹 Uploaded file type: {uploaded_file.type}")
    if uploaded_file.type == "application/pdf":
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        resume_text = "\n".join(
            page.extract_text() for page in pdf_reader.pages if page.extract_text()
        )
        print("🔹 Extracted text from PDF resume")
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(uploaded_file)
        resume_text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        print("🔹 Extracted text from DOCX resume")
    else:
        st.error("Unsupported file format!")
        print("❌ Unsupported file format")

# -------------------
# Helpers
# -------------------
def truncate_text(text: str, max_chars: int = 4000) -> str:
    return text[:max_chars] + ("..." if len(text) > max_chars else "")

# -------------------
# Enhanced JSON Schema for Resume Suggestions
# -------------------
STRICT_SCHEMA = {
    "type": "json_schema",
    "json_schema": {
        "name": "artemis_resume_output",
        "schema": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "ResumeSuggestions": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "Projects": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "current": {"type": "string"},
                                    "change": {
                                        "type": "string",
                                        "maxLength": 120,
                                        "description": "Rewrite with metrics, skills, and action verbs (≤20 words)."
                                    },
                                    "rationale": {
                                        "type": "string",
                                        "maxLength": 60,
                                        "description": "Why this change improves ATS impact."
                                    }
                                },
                                "required": ["current", "change", "rationale"]
                            }
                        },
                        "Experience": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "current": {"type": "string"},
                                    "change": {
                                        "type": "string",
                                        "maxLength": 120,
                                        "description": "Rewrite with measurable results and strong verbs (≤20 words)."
                                    },
                                    "rationale": {
                                        "type": "string",
                                        "maxLength": 60,
                                        "description": "Justify why the change matters (impact, clarity, ATS)."
                                    }
                                },
                                "required": ["current", "change", "rationale"]
                            }
                        }
                    },
                    "required": ["Projects", "Experience"]
                },
                "CoverLetter": {"type": "string"},
                "Summary": {"type": "string"}
            },
            "required": ["ResumeSuggestions", "CoverLetter", "Summary"]
        }
    }
}

# -------------------
# Generate Suggestions
# -------------------
if st.button("Generate Suggestions"):
    print("🔹 Generate Suggestions button clicked")
    if not (company_name and job_description and resume_text):
        st.error("Please fill all fields and upload a resume!")
        print("❌ Missing input fields")
    else:
        with st.spinner("Generating suggestions online..."):
            print("🔹 Building prompt...")

            # -------------------
            # Prompt Template
            # -------------------
            prompt = f"""
            You are Artemis, an intelligent AI career assistant.
            Your task is to improve the candidate's resume and provide a tailored cover letter + summary.
            
            **Rules for ResumeSuggestions**:
            - Output ONLY JSON (no prose).
            - For each suggestion, map: current resume line/phrase -> a direct, short change (≤20 words).
            - Always add 'rationale' (≤60 chars) explaining why the change improves ATS/clarity/impact.
            - Prefer concrete metrics, stacks, and scope (e.g., accuracies, speedups, user counts, tech used).
            - Do NOT invent unverifiable employers; use placeholders like "X%" if numbers are missing.
            - Keep language concise, factual, and ATS-friendly.
            - At least 3 crisp suggestions each for Projects and Experience (if relevant content exists).
            
            **Rules for CoverLetter**:
            - Write a one-page, professional cover letter tailored to the company and role.
            - Use a formal, confident, yet approachable tone (avoid clichés).
            - Focus on skills, impact, and how the candidate fits the JD.
            - Highlight relevant achievements from the resume (numbers, metrics, scope).
            - Structure:
              1. Greeting + intent.
              2. Skills/experience aligning with the role.
              3. Why they want to join this company (based on JD).
              4. Closing with call-to-action.
            
            **Rules for Summary**:
            - Write 1–2 lines maximum.
            - Explain the rationale behind the suggested resume changes.
            - Be precise, action-oriented, and focused on *alignment with the job description*.
            
            **Context**:
            - Company: {company_name}
            - Job Description: {truncate_text(job_description)}
            - Candidate Resume: {truncate_text(resume_text)}
            
            **Final Output Schema (STRICT)**:
            {{
              "ResumeSuggestions": {{
                "Projects": [{{"current": "string", "change": "string (<20 words)", "rationale": "string (<60 chars)"}}, ...],
                "Experience": [{{"current": "string", "change": "string (<20 words)", "rationale": "string (<60 chars)"}}, ...]
              }},
              "CoverLetter": "string",
              "Summary": "string"
            }}
            """

            parsed_output = None
            raw_output = ""

            # 1) Try strict JSON schema
            try:
                completion = client.chat.completions.create(
                    model=MODEL_ID,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1200,
                    response_format=STRICT_SCHEMA,
                )
                raw_output = completion.choices[0].message.content
                print("🔹 Raw model output (schema):", raw_output[:500], "...")
                parsed_output = json.loads(raw_output)
                print("🔹 Successfully parsed JSON output (schema)")
            except Exception as e:
                print(f"⚠️ Schema-enforced generation failed: {e}")

                # 2) Fallback to json_object
                if not parsed_output:
                    try:
                        completion = client.chat.completions.create(
                            model=MODEL_ID,
                            messages=[{"role": "user", "content": prompt}],
                            max_tokens=1200,
                            response_format={"type": "json_object"},
                        )
                        raw_output = completion.choices[0].message.content
                        print("🔹 Raw model output (json_object):", raw_output[:500], "...")
                        parsed_output = json.loads(raw_output)
                        print("🔹 Successfully parsed JSON output (json_object)")
                    except Exception as e2:
                        print(f"⚠️ Direct JSON parsing failed: {e2}")
                        # 3) Regex fallback
                        if raw_output:
                            match = re.search(r"\{.*\}", raw_output, re.DOTALL)
                            if match:
                                try:
                                    parsed_output = json.loads(match.group(0))
                                    print("🔹 Successfully extracted JSON via regex")
                                except Exception as e3:
                                    print(f"❌ Regex JSON parse failed: {e3}")

            # -------------------
            # Fallback for missing CoverLetter
            # -------------------
            if parsed_output and not parsed_output.get("CoverLetter"):
                try:
                    print("⚠️ CoverLetter missing, regenerating...")
                    cover_prompt = f"""
                    Write a professional one-page cover letter for:
                    - Candidate Resume: {truncate_text(resume_text, 3000)}
                    - Job Description: {truncate_text(job_description, 1500)}
                    - Company: {company_name}
                    Keep it ATS-friendly, concise, and aligned with the JD.
                    """
                    cover_completion = client.chat.completions.create(
                        model=MODEL_ID,
                        messages=[{"role": "user", "content": cover_prompt}],
                        max_tokens=600
                    )
                    parsed_output["CoverLetter"] = cover_completion.choices[0].message.content.strip()
                except Exception as e4:
                    print(f"❌ Fallback CoverLetter generation failed: {e4}")

            # -------------------
            # Display
            # -------------------
            if not parsed_output:
                st.warning("⚠️ Could not parse as JSON. Showing raw output:")
                st.code(raw_output if raw_output else "No output")
            else:
                st.success("Suggestions Generated ✅")

                with st.expander("🔍 Raw JSON Preview"):
                    st.code(json.dumps(parsed_output, indent=2))

                # Resume Suggestions
                with st.expander("📄 Resume Suggestions", expanded=True):
                    def render_section(title: str, items: list):
                        st.subheader(title)
                        if not items:
                            st.write("- No suggestions.")
                            return
                        for item in items:
                            current = item.get("current", "").strip()
                            change = item.get("change", "").strip()
                            rationale = item.get("rationale", "").strip()
                            if current:
                                st.write(f"➡️ **{current}**")
                            if change:
                                st.write(f"🔹 **Change:** {change}")
                            if rationale:
                                st.caption(f"💡 {rationale}")
                            st.markdown("---")

                    rs = parsed_output.get("ResumeSuggestions", {})
                    render_section("Projects", rs.get("Projects", []))
                    render_section("Experience", rs.get("Experience", []))

                # Cover Letter
                with st.expander("✉️ Generated Cover Letter"):
                    st.write(parsed_output.get("CoverLetter", ""))

                # Summary
                with st.expander("📝 Summary / Feedback"):
                    st.write(parsed_output.get("Summary", ""))
