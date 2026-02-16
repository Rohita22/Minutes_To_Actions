Minutes to Actions is an AI powered wed application that turns meeting minutes/transcript into 
1. consise summary
2. Key decisions taken
3. Action items which inclues who is incharge of what task by when.
Built as a full-stack production-ready system using React + FastAPI + Groq LLM
Can test the app @: http://fk8go8scgs0w08ccw8gc8s4g.140.245.227.129.sslip.io/

Features:
Paste raw meeting notes

AI extracts:
Summary bullets
Decisions
Action items
Structured JSON validation
Production deployment via Coolify
Secure environment variable handling
Resilient LLM error handling

Tech Stack:
Frontend
1. React
Backend
1. FastApi
2. Groq LLM (AI layer)
Deployment 
- Hosted on coolify 
- Frontend and backend deployed as seperate services
- Environment variables managed securely

LOCAL DEVELOPMENT SET UP:
1. Backend setup
cd MTA_Backend
python -m venv .venv
.\.venv\Scripts\activate  
pip install -r requirements.txt

2. Create an .env file
GROQ_API_KEY=your_groq_api_key_here

3. Run backend 
python -m uvicorn main:app --reload --port 8000
and check health 

4. Frontend setup
cd MTA_frontend
npm install
npm run dev

example meeting notes to test: Maria: “Alright team, thanks for joining. The main purpose today is to realign on the revised launch target. We’re now aiming for July 15 for the MVP release. I want to make sure that’s realistic before we lock it in.”

Kevin: “From engineering’s side, that’s achievable if we freeze the feature scope by next week. I’ll prepare a technical roadmap and share it by March 5 so everyone can see the development phases clearly.”

Anika: “I’m still refining the business requirements because a few stakeholders added new requests yesterday. I’ll consolidate everything and send the updated requirements document by March 3. After that, no additional features should be added without review.”

Liam: “That’s important. From operations, we need at least four weeks before launch to prepare support documentation and internal training. If we’re targeting July 15, I’ll start drafting the onboarding and support plan by March 10.”

Sophie: “Marketing will need a confirmed feature list before we build campaign messaging. I can start working on positioning, but I’ll present a full campaign outline by March 18 once we’re confident in the scope.”

Maria: “Good. Also, we’ve had some delays with vendor contracts. Are those resolved?”

Liam: “Not fully. I’ll follow up with procurement and provide an update by the end of this week.”

Kevin: “One more thing — we should plan for testing earlier this time. Instead of waiting until development is done, we can begin internal QA in phases starting in late May.”

Anika: “I’ll coordinate user acceptance testing sessions and identify pilot users by April 1.”

Maria: “Perfect. So to recap: Anika sends finalized requirements by March 3, Kevin shares the technical roadmap by March 5, Liam drafts the support plan by March 10 and follows up on vendor contracts this week, Sophie presents the campaign outline by March 18, and we begin phased testing in May. Let’s set biweekly check-ins on Wednesdays at 2 PM to monitor progress. If anything risks the July 15 launch, we escalate immediately.”

