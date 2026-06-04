import subprocess
import sys
import time
import os

def send_to_agent(session_name, message):
    print(f"\n⏳ [{session_name} is thinking...]")
    # Run openclaw CLI. --to creates or targets a persistent named session.
    # We use capture_output=True to grab stdout, removing trailing whitespace.
    result = subprocess.run(
        ["openclaw", "agent", "--to", session_name, "--message", message],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"\n❌ Error from {session_name}:")
        print(result.stderr)
        sys.exit(1)
    
    # OpenClaw might output some ANSI or logs depending on config, but stdout 
    # typically contains the clean assistant reply. 
    return result.stdout.strip()

def main():
    print("🚀 Starting E2E Test for fulcra-onboarding (Semi-Automated Mode)")
    
    # 1. Load the rubric
    try:
        with open("onboarding-test-plan.md", "r") as f:
            rubric = f.read()
    except FileNotFoundError:
        print("Error: onboarding-test-plan.md not found.")
        sys.exit(1)

    # 2. Generate unique session IDs so we start clean every run
    run_id = int(time.time())
    target_session = f"test-target-{run_id}"
    tester_session = f"test-tester-{run_id}"

    # 3. Initialize Tester Agent (The Simulated User)
    tester_system_prompt = f"""You are 'Tester Agent', acting as a new user going through a software onboarding flow.
Your goal is to naturally interact with the onboarding agent, while silently keeping track of this rubric:
{rubric}

Rules for you:
1. Reply naturally as a human user. Keep your responses short (1-2 sentences).
2. Do NOT tell the agent what to do, do NOT mention the checklist, and do NOT guide the agent.
3. If the agent asks what you want to track, give a realistic human answer based on your own 'persona' (e.g., you are a software engineer who wants to track focus time, or a runner tracking miles).
4. If the agent gives you an auth link and device code, reply EXACTLY with the phrase "AUTH_PAUSE". Do not say anything else.
5. When the agent presents the final HTML dashboard at the end of the flow, reply EXACTLY with the phrase "TEST_COMPLETE".

Acknowledge these instructions by saying "READY". Do not say anything else."""

    print("\n[1/2] Booting up Tester Agent (LLM-as-a-judge)...")
    tester_reply = send_to_agent(tester_session, tester_system_prompt)
    if "READY" not in tester_reply.upper():
        print(f"Warning: Tester agent gave unexpected readiness reply: {tester_reply}")

    # 4. Initialize Target Agent (The one running the skill)
    # We explicitly point it to the local workspace repo so it uses our bleeding-edge branch.
    print("\n[2/2] Booting up Target Agent (running fulcra-onboarding)...")
    initial_target_prompt = "Hi, I want to run the fulcra-onboarding skill. Please read and execute the skill starting directly from `/home/gregoryklein/.openclaw/workspace/agent-skills/skills/fulcra-onboarding/SKILL.md`."
    target_reply = send_to_agent(target_session, initial_target_prompt)
    
    # 5. The Execution Loop
    turn = 1
    max_turns = 15
    
    while turn <= max_turns:
        print(f"\n" + "-"*50)
        print(f"Turn {turn}")
        print("-"*50)
        print(f"\n🎯 Target Agent:\n{target_reply}\n")
        
        # Pass Target's reply to Tester
        tester_prompt = f"The onboarding agent just said:\n\n---\n{target_reply}\n---\n\nWhat is your reply as the user?"
        tester_reply = send_to_agent(tester_session, tester_prompt)
        
        # Handle Special Directives from Tester Agent
        if "AUTH_PAUSE" in tester_reply:
            print("\n" + "="*50)
            print("🛑 AUTHENTICATION PAUSE 🛑")
            print("The agent needs you to log in.")
            print("Look at the Target Agent's message above, click the link, and enter the device code.")
            input("Press ENTER here in the terminal when you have successfully authorized in your browser...")
            print("="*50 + "\n")
            
            # Resume with simulated user confirmation
            tester_reply = "I've completed the login process. What's next?"
            print(f"\n🧪 Tester Agent (Simulated User):\n{tester_reply}\n")
            
        elif "TEST_COMPLETE" in tester_reply:
            print(f"\n🧪 Tester Agent (Simulated User):\n{tester_reply}\n")
            print("\n✅ Test completed! Generating final report...")
            break
            
        else:
            print(f"\n🧪 Tester Agent (Simulated User):\n{tester_reply}\n")
        
        # Send Tester's reply back to Target
        target_reply = send_to_agent(target_session, tester_reply)
        turn += 1

    if turn > max_turns:
        print("\n⚠️ Test reached maximum turns without completing. Generating partial report...")

    # 6. Generate the Report
    print("\n📊 Requesting final graded rubric from Tester Agent...")
    report_prompt = "The test is complete. Please output the final Markdown rubric with the checkboxes filled ([x]) for the steps the agent successfully completed, and empty ([ ]) for the ones it failed. Add a brief 1-sentence note next to any failed boxes explaining why it failed."
    final_report = send_to_agent(tester_session, report_prompt)
    
    print("\n\n" + "*"*50)
    print("FINAL TEST REPORT")
    print("*"*50)
    print(final_report)
    
    # Save report to disk
    report_filename = f"test-report-{run_id}.md"
    with open(report_filename, "w") as f:
        f.write(final_report)
    print(f"\nReport saved to {report_filename}")

if __name__ == "__main__":
    main()
