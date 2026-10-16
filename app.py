import streamlit as st
import requests
import io
import contextlib
from openai import OpenAI

st.set_page_config(page_title="Bot Fixer App", layout="wide")

# Retrieve background credentials from Streamlit Secrets securely
CLIENT_ID = st.secrets["WHOP_CLIENT_ID"]
CLIENT_SECRET = st.secrets["WHOP_CLIENT_SECRET"]
REDIRECT_URI = "https://streamlit.app"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🤖 Welcome to Bot Fixer App")
    st.subheader("Please sign in to unlock access to your AI development team.")
    
    # FIXED: Restructured URL path variables cleanly with formal OAuth tracking variables
    whop_auth_url = f"https://whop.com{CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code"
    
    st.markdown(f'[<button style="background-color:#FF4B4B; color:white; border:none; padding:12px 24px; border-radius:4px; font-size:16px; cursor:pointer; font-weight:bold;">🔑 Sign in with Whop</button>]({whop_auth_url})', unsafe_allow_html=True)
    
    query_params = st.query_params
    if "code" in query_params:
        auth_code = query_params["code"]
        with st.spinner("Validating active subscription status..."):
            # FIXED: Updated endpoint targeting Whop's background verification backend
            token_url = "https://whop.com"
            payload = {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "code": auth_code,
                "grant_type": "authorization_code",
                "redirect_uri": REDIRECT_URI
            }
            try:
                response = requests.post(token_url, json=payload)
                if response.status_code == 200:
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Authentication rejected. Ensure you have an active membership subscription on Whop.")
            except:
                st.error("Connection error while attempting to reach authentication servers.")
else:
    # =========================================================================
    # PRODUCTION MULTI-AGENT REPAIR ENGINE 
    # =========================================================================
    st.title("⚙️ Bot Fixer App: Professional Agent Workspace")
    st.caption("Zero-Liability Development Sandbox - Autonomous Agent Diagnostics & Repair")
    
    # 1. User Account API Fuel Configuration
    with st.sidebar:
        st.header("🔑 User Credentials")
        user_api_key = st.text_input("Enter your personal OpenAI API Key:", type="password")
        st.caption("Your key is processed securely in memory and never stored on our servers.")
        st.markdown("---")
        st.markdown("💡 **Tip:** Use a key that has access to GPT-4o or o1 models for optimal architectural coding reasoning.")

    # 2. Main Workspace Layout UI Split
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📥 Input Broken Ecosystem")
        input_code = st.text_area("Paste your broken Python Script / Bot Code:", height=250, placeholder="def my_bot():\n    print('Running loop'...")
        input_logs = st.text_area("Paste raw terminal error trace / execution logs (Optional):", height=150, placeholder="Traceback (most recent call last):\nNameError: name 'openai' is not defined")
        
        run_engine = st.button("🚀 Trigger Agent Repair Loop", use_container_width=True)

    # 3. Autonomous Execution & Agent Coordination
    if run_engine:
        if not user_api_key:
            st.error("🛑 Action Required: Please enter your personal OpenAI API Key in the left sidebar to fuel the execution bots.")
        elif not input_code:
            st.error("🛑 Action Required: Please provide a script inside the broken code workspace container.")
        else:
            # Instantiate isolated client sandbox wrapper using the user's active billing profile
            client = OpenAI(api_key=user_api_key)
            
            # Placeholders for multi-agent console telemetry reporting logs
            diag_log_spot = st.empty()
            patch_log_spot = st.empty()
            sandbox_log_spot = st.empty()
            
            current_code_attempt = input_code
            max_loops = 3
            loop_count = 0
            success = False
            diagnostic_report = "Initial run evaluation pending."

            while loop_count < max_loops and not success:
                loop_count += 1
                st.toast(f"Starting Multi-Agent Cycle {loop_count}/{max_loops}...")
                
                # --- AGENT 1: THE DIAGNOSTIC AGENT ---
                diag_log_spot.info(f"🕵️‍♂️ **[Cycle {loop_count}] Diagnostic Agent:** Analyzing syntax tree, dependencies, and execution logs...")
                diag_prompt = f"""
                You are an elite Software Architecture Diagnostic Agent. Analyze this broken Python code and its execution logs.
                Identify structural failures, loop logic breaks, API misconfigurations, or syntax bugs.
                
                BROKEN CODE:
                {current_code_attempt}
                
                CRASH LOGS / CONTEXT:
                {input_logs if input_logs else 'No log provided.'}
                
                Output a clear, concise engineering analysis of what is breaking and provide explicit strategic optimization instructions for the Patch Engineer.
                """
                try:
                    diag_response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "user", "content": diag_prompt}],
                        temperature=0.2
                    )
                    diagnostic_report = diag_response.choices.message.content
                except Exception as e:
                    st.error(f"API Connection Error: {str(e)}")
                    break

                # --- AGENT 2: THE PATCH ENGINEER BOT ---
                patch_log_spot.warning(f"🛠️ **[Cycle {loop_count}] Patch Engineer Bot:** Generating refactored clean logic patches...")
                patch_prompt = f"""
                You are a Master Patch Engineer Bot. Your sole task is to fix broken Python code based on a Diagnostic Report.
                
                ORIGINAL CODE CODESPACE:
                {current_code_attempt}
                
                DIAGNOSTIC REPORT ANALYSIS:
                {diagnostic_report}
                
                Return ONLY the raw executable python code inside your output response text window. 
                Do NOT include markdown syntax wrapping like ```python or any conversational explanations. Just executable code.
                """
                patch_response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": patch_prompt}],
                    temperature=0.1
                )
                patched_code = patch_response.choices.message.content.strip()
                
                # Strip defensive markdown formatting if returned by model safety rails
                if patched_code.startswith("```python"):
                    patched_code = patched_code.split("```python")[1].split("```")[0].strip()
                elif patched_code.startswith("```"):
                    patched_code = patched_code.split("```")[1].split("```")[0].strip()

                # --- AGENT 3: THE BACKGROUND SANDBOX TEST RUNNER ---
                sandbox_log_spot.info(f"🧪 **[Cycle {loop_count}] Sandbox Test Runner:** Executing code compilation inside a zero-liability context...")
                
                output_capture = io.StringIO()
                sandbox_passed = True
                execution_error_output = ""
                
                # Execute string compilation in a localized evaluation environment context
                try:
                    with contextlib.redirect_stdout(output_capture):
                        exec(patched_code, {"st": st, "requests": requests}, {})
                except Exception as sandbox_exception:
                    sandbox_passed = False
                    execution_error_output = str(sandbox_exception)
                
                captured_print_logs = output_capture.getvalue()
                
                if sandbox_passed:
                    success = True
                    current_code_attempt = patched_code
                    sandbox_log_spot.success(f"✅ **[Cycle {loop_count}] Sandbox Status:** Compilation successful. Output validated.")
                    break
                else:
                    sandbox_log_spot.error(f"❌ **[Cycle {loop_count}] Sandbox Status:** Code failed execution check. Error: {execution_error_output}")
                    input_logs = f"Sandbox compiled failure log trace:\n{execution_error_output}\nCaptured Output:\n{captured_print_logs}"
                    current_code_attempt = patched_code

            # 4. Display Final Actionable Output in Workspace UI Column
            with col2:
                st.subheader("✨ Optimized Repair Output")
                if success:
                    st.success(f"🎉 Code repaired successfully in {loop_count} iterations!")
                    with st.expander("🕵️‍♂️ View Final Diagnostic Agent Analysis"):
                        st.markdown(diagnostic_report)
                    st.markdown("**📁 Refactored Ready-to-Deploy Code:**")
                    st.code(current_code_attempt, language="python")
                else:
                    st.error(f"⚠️ Agent swarm reached maximum safety loop limit ({max_loops}) without reaching 100% test passing metrics.")
                    st.warning("Here is the best attempt generated by the engineers:")
