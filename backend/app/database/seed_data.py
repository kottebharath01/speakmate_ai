from sqlalchemy.orm import Session
from app.models.entities import (
    User, LearningProfile, Situation, Lesson, Exercise,
    SentencePattern, Vocabulary
)
from app.database.situations_library import SITUATIONS_LIBRARY
from app.core.security import get_password_hash

def seed_database(db: Session):
    # 1. Seed demo user if not exists
    demo_user = db.query(User).filter(User.email == "learner@speakmate.ai").first()
    if not demo_user:
        demo_user = User(
            email="learner@speakmate.ai",
            username="learner",
            hashed_password=get_password_hash("password123"),
            full_name="English Learner",
            is_active=True
        )
        db.add(demo_user)
        db.commit()
        db.refresh(demo_user)

        profile = LearningProfile(
            user_id=demo_user.id,
            current_level="BEGINNER",
            daily_goal_minutes=20,
            streak_count=0,
            longest_streak=0,
            target_focus="Spoken English & Real Situations",
            total_points=0
        )
        db.add(profile)
        db.commit()

    # 2. Seed Situations
    if db.query(Situation).count() == 0:
        situations_data = [
            {
                "title": "Buying Clothes in a Shop",
                "category": "Shopping",
                "level": "BEGINNER",
                "telugu_explanation": "నువ్వు ఒక క్లోతింగ్ షాప్ కి వెళ్ళావు. నీకు ఒక బ్లూ కలర్ ఫార్మల్ షర్ట్ కొనాలి. షాప్‌కీపర్ నిన్ను 'ఏ టైప్ షర్ట్ కావాలి?' అని అడుగుతాడు. నీకు కాటన్ మెటీరియల్‌లో మీడియం సైజ్ కావాలని నువ్వు ఎలా వివరిస్తావు?",
                "telugu_transliteration": "Nuvvu oka clothing shop ki vellavu. Neeku oka blue colour formal shirt konali. Shopkeeper ninnu em kavali ani aduguthadu. Cotton material lo medium size kavali ani ela chepthavu?",
                "english_prompt": "How would you explain to the shopkeeper what kind of shirt you want and what size you need?",
                "context_tags": "shopping, casual, clothing, customer",
            },
            {
                "title": "Ordering Food in a Restaurant",
                "category": "Dining",
                "level": "BEGINNER",
                "telugu_explanation": "నువ్వు ఒక రెస్టారెంట్‌కు వెళ్ళావు. వేడి వెజ్ బిర్యానీ మరియు తక్కువ కారంతో ఉన్న చికెన్ సూప్ ఆర్డర్ చేయాలనుకుంటున్నావు. అలాగే ఒక బాటిల్ మంచి నీళ్ళు కూడా తీసుకురమ్మని వెయిటర్‌కు ఎలా చెబుతావు?",
                "telugu_transliteration": "Nuvvu restaurant ki vellavu. Hot veg biryani and mild spicy chicken soup order cheyyali. Alage water bottle adagali. Waiter ki ela chepthavu?",
                "english_prompt": "How would you place your order with the waiter for hot veg biryani, mild chicken soup, and a bottle of water?",
                "context_tags": "food, dining, polite, restaurant",
            },
            {
                "title": "Asking for Directions to Metro Station",
                "category": "Travel",
                "level": "BEGINNER",
                "telugu_explanation": "నువ్వు హైదరాబాద్ నగరంలో కొత్త ప్రాంతానికి వచ్చావు. దగ్గర్లోని మెట్రో స్టేషన్ ఎక్కడుందో దారి తెలియడం లేదు. రోడ్డుపై వెళ్తున్న ఒక వ్యక్తిని ఆపి మర్యాదగా దారి ఎలా అడుగుతావు?",
                "telugu_transliteration": "Nuvvu kottha chotiki vachavu. Metro station dāri theliyadhu. Dārilō unna vyakthini maryādagā ela aduguthāvu?",
                "english_prompt": "How would you politely ask someone on the street for directions to the nearest metro station?",
                "context_tags": "directions, travel, polite, stranger",
            },
            {
                "title": "Introducing Yourself at Office",
                "category": "Workplace",
                "level": "INTERMEDIATE",
                "telugu_explanation": "నువ్వు ఒక ఐటీ కంపెనీలో కొత్తగా చేరావు. ఈరోజు మొదటి టీమ్ మీటింగ్‌లో నిన్ను నువ్వు పరిచయం చేసుకోవాలి. నీ పేరు, నీ ఊరు, నీ గత అనుభవం మరియు ఈ ప్రాజెక్ట్‌లో నీ పాత్ర గురించి టీమ్ సభ్యులకు ఎలా చెబుతావు?",
                "telugu_transliteration": "Kottha IT company lo cheravu. First team meeting lo ninnu nuvvu introduce chesukovali. Ela chepthavu?",
                "english_prompt": "How would you introduce yourself to your new team members covering your background, experience, and role?",
                "context_tags": "office, introduction, professional, meeting",
            },
            {
                "title": "Asking for Sick Leave from Manager",
                "category": "Workplace",
                "level": "INTERMEDIATE",
                "telugu_explanation": "ఈరోజు ఉదయం నీకు విపరీతమైన జ్వరం మరియు తలనొప్పి వచ్చింది. ఈరోజు ఆఫీస్ వర్క్ చేయలేవు. నీ మేనేజర్‌కి కాల్ చేసి లేదా మెసేజ్ చేసి ఈరోజు సిక్ లీవ్ కావాలని, రేపు హెల్త్ ఇంప్రూవ్ అయితే లాగిన్ అవుతానని ఎలా చెబుతావు?",
                "telugu_transliteration": "Neeku fever vachindi. Ee roju sick leave kavali ani manager ki ela inform chesi request chesthavu?",
                "english_prompt": "How would you inform your manager that you are unwell with a fever and request sick leave for today?",
                "context_tags": "leave, sick leave, manager, email, professional",
            },
            {
                "title": "Discussing an API Bug with a Colleague",
                "category": "Technical",
                "level": "INTERMEDIATE",
                "telugu_explanation": "నువ్వు బ్యాకెండ్ డెవలపర్‌వి. యూజర్ లాగిన్ API 500 ఇంటర్నల్ సర్వర్ ఎర్రర్ ఇస్తోంది. డేటాబేస్ కనెక్షన్ టైమౌట్ వల్ల ఇది జరుగుతోందని నువ్వు గమనించావు. నీతో కలిసి పనిచేస్తున్న డెవలపర్‌కు ఈ సమస్యను వివరించి కలిసి డిబగ్ చేద్దాం అని ఎలా చెబుతావు?",
                "telugu_transliteration": "User login API 500 error isthondi. Database connection timeout problem ani colleague ki explain chesi kalisi fix cheddam ani ela chepthavu?",
                "english_prompt": "How would you explain the API 500 error to your colleague and suggest debugging the database connection issue together?",
                "context_tags": "technical, python, debugging, teamwork",
            },
            {
                "title": "Job Interview: Tell Me About Yourself",
                "category": "Interview",
                "level": "ADVANCED",
                "telugu_explanation": "నువ్వు పైథాన్ మరియు వెబ్ డెవలప్‌మెంట్ రోల్ కోసం జాబ్ ఇంటర్వ్యూకు హాజరయ్యావు. హెచ్‌ఆర్ లేదా టెక్నికల్ ఇంటర్వ్యూయర్ 'Can you introduce yourself and walk me through your recent project?' అని అడిగారు. కాన్ఫిడెంట్‌గా ఎలా సమాధానం చెబుతావు?",
                "telugu_transliteration": "Interview lo 'Tell me about yourself and your recent project' ani adigaru. Professional ga ela answer chesthavu?",
                "english_prompt": "Deliver a concise, confident professional introduction explaining your technical skill set, passion for software development, and key project.",
                "context_tags": "interview, hr, technical, presentation",
            },
            {
                "title": "Handling an Angry Customer on Support Call",
                "category": "Workplace",
                "level": "ADVANCED",
                "telugu_explanation": "ఒక కస్టమర్ ఆర్డర్ చేసిన ల్యాప్‌టాప్ ఇంకా డెలివరీ కాలేదు. అతను చాలా కోపంగా కస్టమర్ కేర్‌కు కాల్ చేశాడు. నువ్వు సపోర్ట్ ఎగ్జిక్యూటివ్‌వి. అతని కోపాన్ని శాంతింపజేసి, జరిగిన అసౌకర్యానికి క్షమాపణ చెప్పి, ఈరోజే ప్రాధాన్యతతో డెలివరీ చేయిస్తానని ఎలా హామీ ఇస్తావు?",
                "telugu_transliteration": "Customer product delivery late ayyindani kopamga unnadhu. Executive ga aayana ni calm chesi problem resolve chesthanani ela chepthavu?",
                "english_prompt": "How would you de-escalate the angry customer's frustration, apologize sincerely for the delay, and assure them of an expedited delivery today?",
                "context_tags": "customer service, conflict resolution, professional, empathy",
            }
        ]
        for s in situations_data:
            db.add(Situation(**s))
        db.commit()

    # Ensure expanded 15-category situation library is present
    existing_titles = {row[0] for row in db.query(Situation.title).all()}
    for s in SITUATIONS_LIBRARY:
        if s["title"] not in existing_titles:
            db.add(Situation(**s))
            existing_titles.add(s["title"])
    db.commit()

    # 3. Seed Sentence Patterns
    if db.query(SentencePattern).count() == 0:
        patterns_data = [
            {
                "pattern": "I want to + verb",
                "structure_formula": "Subject + want to / wants to + Base Verb (V1)",
                "purpose": "Used to express an immediate personal desire, wish, or intention.",
                "explanation": "Use 'I want to' followed by a first form verb (V1) whenever you want to do something right now or in the near future. Never say 'I want to going' or 'I am wanting'.",
                "level": "BEGINNER",
                "examples_json": [
                    {"sentence": "I want to learn English fluently.", "meaning": "నేను ఇంగ్లీష్ ధారాళంగా నేర్చుకోవాలనుకుంటున్నాను."},
                    {"sentence": "I want to buy a new laptop.", "meaning": "నేను కొత్త ల్యాప్‌టాప్ కొనాలనుకుంటున్నాను."},
                    {"sentence": "I want to speak with the manager.", "meaning": "నేను మేనేజర్‌తో మాట్లాడాలనుకుంటున్నాను."}
                ],
                "speaking_prompt": "Create a sentence using 'I want to' explaining what skill you wish to master this month."
            },
            {
                "pattern": "I have to + verb",
                "structure_formula": "Subject + have to / has to + Base Verb (V1)",
                "purpose": "Used to express obligation, necessity, or duty created by external rules or situations.",
                "explanation": "Use 'I have to' when something is mandatory or necessary, not just a casual wish. For third person singular (He/She/It), use 'has to'.",
                "level": "BEGINNER",
                "examples_json": [
                    {"sentence": "I have to finish this task before 5 PM.", "meaning": "నేను సాయంత్రం 5 గంటల లోపు ఈ పని పూర్తి చేయాలి."},
                    {"sentence": "I have to attend a team meeting today.", "meaning": "నేను ఈరోజు టీమ్ మీటింగ్‌కు హాజరు కావాలి."},
                    {"sentence": "He has to submit the project report tomorrow.", "meaning": "అతను రేపు ప్రాజెక్ట్ రిపోర్ట్ సబ్మిట్ చేయాలి."}
                ],
                "speaking_prompt": "Say what important task you must complete today using 'I have to'."
            },
            {
                "pattern": "I am trying to + verb",
                "structure_formula": "Subject + am/is/are + trying to + Base Verb (V1)",
                "purpose": "Used to describe an active, continuous effort to achieve a goal.",
                "explanation": "Use this pattern when you are exerting effort right now or in this phase of life. It implies persistence.",
                "level": "BEGINNER",
                "examples_json": [
                    {"sentence": "I am trying to improve my communication skills.", "meaning": "నేను నా కమ్యూనికేషన్ స్కిల్స్ మెరుగుపరుచుకోవడానికి ప్రయత్నిస్తున్నాను."},
                    {"sentence": "I am trying to fix the backend server bug.", "meaning": "నేను బ్యాకెండ్ సర్వర్ బగ్‌ను పరిష్కరించడానికి ప్రయత్నిస్తున్నాను."},
                    {"sentence": "We are trying to reach our monthly target.", "meaning": "మేము మా నెలవారీ లక్ష్యాన్ని చేరుకోవడానికి ప్రయత్నిస్తున్నాము."}
                ],
                "speaking_prompt": "Tell the tutor one personal habit or skill you are currently working on using 'I am trying to'."
            },
            {
                "pattern": "I used to + verb",
                "structure_formula": "Subject + used to + Base Verb (V1)",
                "purpose": "Used to describe past habits or repeated states that are no longer true today.",
                "explanation": "Use 'used to' for something you did regularly in the past, but do not do now. Do NOT use it for things you still do.",
                "level": "INTERMEDIATE",
                "examples_json": [
                    {"sentence": "I used to hesitate when speaking in public.", "meaning": "గతంలో పబ్లిక్‌లో మాట్లాడేటప్పుడు నేను సంకోచించేవాడిని (ఇప్పుడు కాదు)."},
                    {"sentence": "I used to play cricket every weekend during college.", "meaning": "కాలేజీ రోజుల్లో నేను ప్రతి వీకెండ్ క్రికెట్ ఆడేవాడిని."},
                    {"sentence": "She used to work in Bangalore before joining here.", "meaning": "ఆమె ఇక్కడ చేరకముందు బెంగళూరులో పనిచేసేది."}
                ],
                "speaking_prompt": "Describe a past routine or hobby that you do not do anymore using 'I used to'."
            },
            {
                "pattern": "I would like to + verb",
                "structure_formula": "Subject + would like to ('d like to) + Base Verb (V1)",
                "purpose": "A very polite and professional alternative to 'I want to'.",
                "explanation": "In corporate settings, meetings, and interviews, 'I would like to' sounds much more courteous and professional than 'I want to'.",
                "level": "INTERMEDIATE",
                "examples_json": [
                    {"sentence": "I would like to know more about the job responsibilities.", "meaning": "నేను జాబ్ బాధ్యతల గురించి మరింత తెలుసుకోవాలనుకుంటున్నాను."},
                    {"sentence": "I would like to schedule a quick call with you.", "meaning": "నేను మీతో చిన్న కాల్ షెడ్యూల్ చేయాలనుకుంటున్నాను."},
                    {"sentence": "I would like to propose a simple solution for this problem.", "meaning": "ఈ సమస్యకు నేను ఒక సులువైన పరిష్కారాన్ని ప్రతిపాదించాలనుకుంటున్నాను."}
                ],
                "speaking_prompt": "Politely ask your interviewer or colleague about the next steps using 'I would like to'."
            },
            {
                "pattern": "I have been + verb-ing",
                "structure_formula": "Subject + have/has been + Verb-ing + (for/since + time)",
                "purpose": "Present Perfect Continuous: used when an action started in the past and is still ongoing right now.",
                "explanation": "Common Telugu learner mistake: saying 'I am working here since 2 years' (incorrect). The correct form is 'I have been working here for 2 years'.",
                "level": "ADVANCED",
                "examples_json": [
                    {"sentence": "I have been learning Python for the past six months.", "meaning": "నేను గత ఆరు నెలలుగా పైథాన్ నేర్చుకుంటున్నాను (ఇప్పటికీ నేర్చుకుంటూనే ఉన్నాను)."},
                    {"sentence": "She has been waiting for the bus since 9 AM.", "meaning": "ఆమె ఉదయం 9 గంటల నుండి బస్సు కోసం వేచి చూస్తోంది."},
                    {"sentence": "We have been developing this web application for three weeks.", "meaning": "మేము మూడు వారాలుగా ఈ వెబ్ అప్లికేషన్‌ను డెవలప్ చేస్తున్నాము."}
                ],
                "speaking_prompt": "Tell the tutor how long you have been coding or learning English using 'I have been + verb-ing'."
            }
        ]
        for p in patterns_data:
            db.add(SentencePattern(**p))
        db.commit()

    # 4. Seed Grammar Academy Lessons
    if db.query(Lesson).count() == 0:
        lessons_data = [
            {
                "title": "Parts of Speech: The Building Blocks",
                "category": "grammar",
                "level": "BEGINNER",
                "description": "Understand nouns, verbs, adjectives, adverbs, pronouns, prepositions, conjunctions, and interjections with simple everyday examples.",
                "order_num": 1,
                "content_json": {
                    "definition": "Words in English are classified into eight parts of speech according to their role in a sentence.",
                    "explanation": "Just like a building needs bricks, cement, and steel, an English sentence needs nouns (names), verbs (actions), and adjectives (descriptions).",
                    "key_rules": [
                        "Nouns name people, places, things, or ideas (e.g. Hyderabad, laptop, happiness).",
                        "Verbs describe actions or states of being (e.g. speak, write, is, become).",
                        "Adjectives describe or qualify nouns (e.g. blue shirt, quick response).",
                        "Adverbs modify verbs, adjectives, or other adverbs (e.g. speak fluently, work diligently)."
                    ],
                    "common_mistakes": [
                        {"incorrect": "He speaks very fluent.", "correct": "He speaks very fluently.", "reason": "Use adverb 'fluently' to describe how he speaks, not adjective 'fluent'."}
                    ]
                }
            },
            {
                "title": "Tenses Mastery: Simple Present vs Present Continuous",
                "category": "grammar",
                "level": "BEGINNER",
                "description": "Master the difference between habits/facts (Simple Present) and actions happening right now (Present Continuous).",
                "order_num": 2,
                "content_json": {
                    "definition": "Simple Present is used for routines, facts, and habits. Present Continuous is used for actions happening right at this moment.",
                    "explanation": "In Telugu, we often say 'Nenu roju college ki velthunna' using a continuous form. But in English, for daily habits you must use Simple Present: 'I go to college every day', not 'I am going every day'.",
                    "key_rules": [
                        "Habits / Daily Routine: Subject + V1 (e.g., 'I wake up at 7 AM every day.')",
                        "Right now / At this moment: Subject + am/is/are + V-ing (e.g., 'I am listening to music right now.')",
                        "Third person singular takes -s/-es in Simple Present: 'He works', 'She codes'."
                    ],
                    "common_mistakes": [
                        {"incorrect": "I am drinking coffee every morning.", "correct": "I drink coffee every morning.", "reason": "For regular daily habits, use Simple Present."},
                        {"incorrect": "He know the answer.", "correct": "He knows the answer.", "reason": "Add 's' for third-person singular (He/She/It)."}
                    ]
                }
            },
            {
                "title": "Articles: A, An, and The Made Crystal Clear",
                "category": "grammar",
                "level": "BEGINNER",
                "description": "Learn when to use indefinite articles (a, an) based on vowel sounds, and when to use the definite article (the).",
                "order_num": 3,
                "content_json": {
                    "definition": "Articles identify whether a noun is specific or general.",
                    "explanation": "Use 'a' before consonant sounds (a car, a university). Use 'an' before vowel sounds (an apple, an hour). Use 'the' when both speaker and listener know which specific item is meant.",
                    "key_rules": [
                        "Use 'an' for vowel SOUNDS (a, e, i, o, u), not just spelling: 'an honest person' (h is silent), 'a university' (starts with 'y' sound).",
                        "Use 'the' for specific things: 'The book you gave me' vs 'A book from the library'."
                    ],
                    "common_mistakes": [
                        {"incorrect": "He is a honest man.", "correct": "He is an honest man.", "reason": "'Honest' begins with a vowel sound (o-nest)."},
                        {"incorrect": "I want to buy the shirt (when no specific shirt was mentioned).", "correct": "I want to buy a shirt.", "reason": "Use 'a' for non-specific items."}
                    ]
                }
            },
            {
                "title": "Subject-Verb Agreement",
                "category": "grammar",
                "level": "INTERMEDIATE",
                "description": "Ensure singular subjects match singular verbs, and plural subjects match plural verbs every single time.",
                "order_num": 4,
                "content_json": {
                    "definition": "A singular subject requires a singular verb, while a plural subject takes a plural verb.",
                    "explanation": "The most frequent mistake in spoken English is omitting 's' with singular verbs or mixing 'has/have'.",
                    "key_rules": [
                        "He / She / It + does / has / goes / speaks (Singular).",
                        "I / You / We / They + do / have / go / speak (Plural / Special).",
                        "Everyone / Somebody / Each is treated as singular: 'Everyone is ready', not 'Everyone are ready'."
                    ],
                    "common_mistakes": [
                        {"incorrect": "One of my friends are coming.", "correct": "One of my friends is coming.", "reason": "The subject is 'One', which is singular."},
                        {"incorrect": "He don't know about it.", "correct": "He doesn't know about it.", "reason": "Singular 'He' takes 'does not / doesn't'."}
                    ]
                }
            },
            {
                "title": "Prepositions of Time and Place: In, On, At",
                "category": "grammar",
                "level": "INTERMEDIATE",
                "description": "Clear the confusion between in, on, and at for time and location.",
                "order_num": 5,
                "content_json": {
                    "definition": "Prepositions specify relationships between nouns, pronouns, and other words in space and time.",
                    "explanation": "Think of an upside-down pyramid: IN is broadest (years, months, cities, countries), ON is medium (days, dates, streets, surfaces), AT is most specific (exact times, exact addresses, points).",
                    "key_rules": [
                        "TIME: In 2026, in November. On Monday, on my birthday. At 5 PM, at noon.",
                        "PLACE: In India, in Hyderabad. On MG Road, on the table. At the bus stop, at the door."
                    ],
                    "common_mistakes": [
                        {"incorrect": "I will meet you in Monday.", "correct": "I will meet you on Monday.", "reason": "Use 'on' for specific days."},
                        {"incorrect": "The meeting is on 10 AM.", "correct": "The meeting is at 10 AM.", "reason": "Use 'at' for specific clock times."}
                    ]
                }
            },
            {
                "title": "Conditional Sentences: If Clauses",
                "category": "grammar",
                "level": "ADVANCED",
                "description": "Construct realistic and hypothetical conditionals accurately for interviews and professional debates.",
                "order_num": 6,
                "content_json": {
                    "definition": "Conditionals express what happens or could happen if a certain condition is met.",
                    "explanation": "First conditional is for real future possibilities: If + simple present, will + V1. Second conditional is for imaginary present: If + past simple, would + V1.",
                    "key_rules": [
                        "Real Future: If it rains, I will stay home. (Never say: If it will rain...)",
                        "Imaginary: If I had more time, I would build more open-source projects."
                    ],
                    "common_mistakes": [
                        {"incorrect": "If you will call me, I will come.", "correct": "If you call me, I will come.", "reason": "Do not put 'will' inside the 'if' condition clause."}
                    ]
                }
            }
        ]
        for l in lessons_data:
            db.add(Lesson(**l))
        db.commit()

    # 5. Seed Vocabulary
    if db.query(Vocabulary).count() == 0:
        vocab_data = [
            {"word": "Recommend", "part_of_speech": "verb", "telugu_meaning": "సిఫార్సు చేయడం / సలహా ఇవ్వడం", "english_definition": "To suggest something as good, suitable, or worthy of choice.", "level": "BEGINNER", "example_sentence": "Can you recommend a good shirt for an interview?", "usage_notes": "Very useful in shops, restaurants, and tech decisions."},
            {"word": "Requirement", "part_of_speech": "noun", "telugu_meaning": "అవసరం / నిబంధన", "english_definition": "A thing that is needed or wanted.", "level": "BEGINNER", "example_sentence": "My main requirement is a lightweight cotton shirt.", "usage_notes": "Use this in client meetings and shopping."},
            {"word": "Assistance", "part_of_speech": "noun", "telugu_meaning": "సహాయం", "english_definition": "Help or support given to someone.", "level": "BEGINNER", "example_sentence": "Thank you for your assistance.", "usage_notes": "More polite and professional than 'help'."},
            {"word": "Convenient", "part_of_speech": "adjective", "telugu_meaning": "అనుకూలమైన / సౌకర్యవంతమైన", "english_definition": "Fitting in well with a person's needs, activities, and plans.", "level": "INTERMEDIATE", "example_sentence": "Is 3 PM convenient for a quick phone call?", "usage_notes": "Ideal for scheduling meetings with managers and clients."},
            {"word": "Clarify", "part_of_speech": "verb", "telugu_meaning": "స్పష్టత ఇవ్వడం / వివరించడం", "english_definition": "To make a statement or situation clear and understandable.", "level": "INTERMEDIATE", "example_sentence": "Could you please clarify this requirement?", "usage_notes": "Great in technical discussions to ask questions politely."},
            {"word": "Apologize", "part_of_speech": "verb", "telugu_meaning": "క్షమాపణ చెప్పడం", "english_definition": "To express regret for something that one has done wrong or for an inconvenience caused.", "level": "INTERMEDIATE", "example_sentence": "I apologize for the delay in sending the report.", "usage_notes": "Essential professional workplace vocabulary."},
            {"word": "Optimize", "part_of_speech": "verb", "telugu_meaning": "మరింత సమర్థవంతంగా తయారుచేయడం", "english_definition": "To make the best or most effective use of a situation or resource.", "level": "ADVANCED", "example_sentence": "We optimized the database query to reduce API response time.", "usage_notes": "Key technical keyword for software engineering interviews."},
            {"word": "Accomplish", "part_of_speech": "verb", "telugu_meaning": "విజయవంతంగా సాధించడం", "english_definition": "To achieve or complete something successfully.", "level": "ADVANCED", "example_sentence": "We accomplished our quarterly delivery targets ahead of schedule.", "usage_notes": "Use in resume and interview answers to highlight achievements."}
        ]
        for v in vocab_data:
            db.add(Vocabulary(**v))
        db.commit()
