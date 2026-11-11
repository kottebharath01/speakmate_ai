from sqlalchemy.orm import Session
from app.models.words_expressions import WordItem, WordExercise

def seed_words_expressions(db: Session):
    """Seed comprehensive initial content across all 4 sections if not already seeded."""
    if db.query(WordItem).count() > 0:
        return

    items_to_add = []

    # =========================================================================
    # SECTION 1: INDIVIDUAL WORDS (15 Categories)
    # =========================================================================

    # 1. Daily Use Words
    items_to_add.append({
        "section": "words",
        "category": "Daily Use Words",
        "level": "BEGINNER",
        "telugu_text": "సౌకర్యవంతమైన",
        "telugu_transliteration": "Saukarryavanthamaina",
        "english_text": "Convenient",
        "pronunciation": "/kənˈviː.ni.ənt/",
        "part_of_speech": "Adjective",
        "english_definition": "Fitting in well with a person's needs, activities, and plans; easy to do.",
        "when_to_use": "Use when scheduling meetings, calls, or choosing a time or location that suits you or someone else.",
        "examples_json": [
            {"english": "Is 4 PM convenient for a quick phone call?", "telugu": "సాయంత్రం 4 గంటలకు మాట్లాడటానికి మీకు అనుకూలమేనా?"},
            {"english": "Online grocery delivery is very convenient.", "telugu": "ఆన్‌లైన్ కిరాణా డెలివరీ చాలా సౌకర్యవంతంగా ఉంటుంది."},
            {"english": "Let's meet whenever it is convenient for you.", "telugu": "మీకు ఎప్పుడు అనుకూలంగా ఉంటే అప్పుడు కలుద్దాం."}
        ],
        "common_mistakes_json": [
            {"incorrect": "Are you convenient tomorrow?", "correct": "Is tomorrow convenient for you?", "reason": "'Convenient' describes the time or situation, not the person directly."}
        ],
        "synonyms_json": ["Suitable", "Handy", "Accessible", "Favorable"]
    })

    items_to_add.append({
        "section": "words",
        "category": "Daily Use Words",
        "level": "BEGINNER",
        "telugu_text": "సంకోచించడం / తటపటాయించడం",
        "telugu_transliteration": "Sankochinchadam",
        "english_text": "Hesitate",
        "pronunciation": "/ˈhez.ɪ.teɪt/",
        "part_of_speech": "Verb",
        "english_definition": "To pause before saying or doing something, especially because you are unsure or nervous.",
        "when_to_use": "Encourage someone to speak up or ask questions without fear, especially in office or learning environments.",
        "examples_json": [
            {"english": "Please do not hesitate to ask if you have any questions.", "telugu": "మీకు ఏవైనా ప్రశ్నలు ఉంటే దయచేసి సంకోచించకుండా అడగండి."},
            {"english": "I hesitated for a moment before answering.", "telugu": "సమాధానం చెప్పేముందు నేను ఒక్క క్షణం సంకోచించాను."},
            {"english": "Never hesitate to clarify your doubts.", "telugu": "సందేహాలు నివృత్తి చేసుకోవడానికి ఎప్పుడూ సంకోచించకండి."}
        ],
        "common_mistakes_json": [
            {"incorrect": "Don't hesitate for ask.", "correct": "Don't hesitate to ask.", "reason": "Follow 'hesitate' with the infinitive 'to + verb'."}
        ],
        "synonyms_json": ["Pause", "Waver", "Hold back"]
    })

    # 2. Home and Household Words
    items_to_add.append({
        "section": "words",
        "category": "Home and Household Words",
        "level": "BEGINNER",
        "telugu_text": "ఇంటి పాత్రలు / వంట సామాగ్రి",
        "telugu_transliteration": "Utensils",
        "english_text": "Utensils",
        "pronunciation": "/juːˈten.sɪlz/",
        "part_of_speech": "Noun (Plural)",
        "english_definition": "Tools or containers that you use in the kitchen, like spoons, pots, and pans.",
        "when_to_use": "Use when talking about cooking items, cleaning dishes, or shopping for kitchen items.",
        "examples_json": [
            {"english": "I need to wash the kitchen utensils after dinner.", "telugu": "డిన్నర్ తర్వాత నేను కిచెన్ పాత్రలను కడగాలి."},
            {"english": "Stainless steel utensils last for years.", "telugu": "స్టెయిన్‌లెస్ స్టీల్ పాత్రలు ఏళ్ల తరబడి మన్నుతాయి."}
        ],
        "common_mistakes_json": [
            {"incorrect": "I bought a kitchen utensil (when referring to several).", "correct": "I bought kitchen utensils.", "reason": "Use plural 'utensils' when referring to multiple items."}
        ],
        "synonyms_json": ["Cookware", "Kitchenware", "Cutlery"]
    })

    items_to_add.append({
        "section": "words",
        "category": "Home and Household Words",
        "level": "INTERMEDIATE",
        "telugu_text": "అస్తవ్యస్తంగా పడి ఉన్న వస్తువులు / చెల్లాచెదురు",
        "telugu_transliteration": "Clutter",
        "english_text": "Clutter",
        "pronunciation": "/ˈklʌt.ər/",
        "part_of_speech": "Noun & Verb",
        "english_definition": "A collection of things lying around in an untidy, disorganized state.",
        "when_to_use": "Use when cleaning rooms, organizing your work desk, or removing mess.",
        "examples_json": [
            {"english": "Please clear the clutter from your study desk.", "telugu": "దయచేసి నీ స్టడీ డెస్క్ మీద ఉన్న చిందరవందర వస్తువులను సర్దు."},
            {"english": "A clean room without clutter helps me focus better.", "telugu": "చిందరవందర వస్తువులు లేని శుభ్రమైన గది నాకు బాగా దృష్టి పెట్టడానికి సహాయపడుతుంది."}
        ],
        "common_mistakes_json": [
            {"incorrect": "There are many clutters.", "correct": "There is a lot of clutter.", "reason": "'Clutter' is uncountable when used as a noun."}
        ],
        "synonyms_json": ["Mess", "Disorder", "Jumble"]
    })

    # 3. Food and Cooking Words
    items_to_add.append({
        "section": "words",
        "category": "Food and Cooking Words",
        "level": "BEGINNER",
        "telugu_text": "నూనెలో వేయించడం / పోపు పెట్టడం",
        "telugu_transliteration": "Sauté",
        "english_text": "Sauté",
        "pronunciation": "/ˈsoʊ.teɪ/",
        "part_of_speech": "Verb",
        "english_definition": "To fry quickly in a little hot fat or oil.",
        "when_to_use": "Used in cooking instructions when frying onions, garlic, or vegetables in a small amount of oil.",
        "examples_json": [
            {"english": "Sauté the chopped onions until they turn golden brown.", "telugu": "తరిగిన ఉల్లిపాయలను బంగారు రంగు వచ్చేవరకు వేయించండి."},
            {"english": "Add garlic and sauté for two minutes.", "telugu": "వెల్లుల్లి వేసి రెండు నిమిషాలు వేయించండి."}
        ],
        "common_mistakes_json": [
            {"incorrect": "Deep fry the onions (when you only need a little oil).", "correct": "Sauté the onions.", "reason": "'Deep fry' uses a lot of oil; 'sauté' uses very little."}
        ],
        "synonyms_json": ["Pan-fry", "Stir-fry"]
    })

    # 4. Shopping Vocabulary
    items_to_add.append({
        "section": "words",
        "category": "Shopping Vocabulary",
        "level": "BEGINNER",
        "telugu_text": "ధర తగ్గించమని బేరమాడటం",
        "telugu_transliteration": "Bargain",
        "english_text": "Bargain",
        "pronunciation": "/ˈbɑːr.ɡɪn/",
        "part_of_speech": "Verb & Noun",
        "english_definition": "To negotiate the terms and price of a purchase, or a thing bought for less than the usual price.",
        "when_to_use": "Use in markets, shopping, or when describing great deals.",
        "examples_json": [
            {"english": "You can bargain at local street markets for a better price.", "telugu": "మంచి ధర కోసం మీరు లోకల్ స్ట్రీట్ మార్కెట్లలో బేరమాడవచ్చు."},
            {"english": "This shirt was a real bargain at half price!", "telugu": "సగం ధరకే వచ్చిన ఈ షర్ట్ నిజంగా గొప్ప బేరం!"}
        ],
        "common_mistakes_json": [
            {"incorrect": "I made a bargain with him for reducing price.", "correct": "I bargained with him to reduce the price.", "reason": "Use 'bargain with someone to do something'."}
        ],
        "synonyms_json": ["Negotiate", "Haggle", "Deal"]
    })

    # 5. Travel Vocabulary
    items_to_add.append({
        "section": "words",
        "category": "Travel Vocabulary",
        "level": "BEGINNER",
        "telugu_text": "రోజూ ప్రయాణం చేయడం (ఆఫీస్ లేదా కాలేజీకి)",
        "telugu_transliteration": "Commute",
        "english_text": "Commute",
        "pronunciation": "/kəˈmjuːt/",
        "part_of_speech": "Verb & Noun",
        "english_definition": "To travel regularly over some distance between one's home and place of work or study.",
        "when_to_use": "Use when discussing daily office or college travel via bus, metro, or bike.",
        "examples_json": [
            {"english": "I commute to my office by metro every morning.", "telugu": "నేను ప్రతిరోజూ ఉదయం మెట్రో ద్వారా నా ఆఫీస్‌కు ప్రయాణిస్తాను."},
            {"english": "Her daily commute takes about forty-five minutes.", "telugu": "ఆమె రోజువారీ ఆఫీస్ ప్రయాణానికి దాదాపు 45 నిమిషాలు పడుతుంది."}
        ],
        "common_mistakes_json": [
            {"incorrect": "I am traveling to office every day.", "correct": "I commute to office every day.", "reason": "'Commute' specifically denotes regular home-to-work travel."}
        ],
        "synonyms_json": ["Travel", "Journey", "Transit"]
    })

    # 6. Family and Relationships
    items_to_add.append({
        "section": "words",
        "category": "Family and Relationships",
        "level": "BEGINNER",
        "telugu_text": "సొంత సోదరుడు లేదా సోదరి",
        "telugu_transliteration": "Sibling",
        "english_text": "Sibling",
        "pronunciation": "/ˈsɪb.lɪŋ/",
        "part_of_speech": "Noun",
        "english_definition": "A brother or sister.",
        "when_to_use": "Use in introductions, interviews, and family discussions instead of saying 'real brother' or 'co-brother'.",
        "examples_json": [
            {"english": "Do you have any siblings?", "telugu": "మీకు తోబుట్టువులు (అన్నదమ్ములు లేదా అక్కాచెల్లెళ్ళు) ఉన్నారా?"},
            {"english": "I have two siblings: an elder brother and a younger sister.", "telugu": "నాకు ఇద్దరు తోబుట్టువులు ఉన్నారు: ఒక అన్నయ్య మరియు ఒక చెల్లెలు."}
        ],
        "common_mistakes_json": [
            {"incorrect": "He is my cousin brother.", "correct": "He is my cousin.", "reason": "Never say 'cousin brother' or 'cousin sister'. Simply say 'cousin'."}
        ],
        "synonyms_json": ["Brother", "Sister", "Kin"]
    })

    # 7. Feelings and Emotions
    items_to_add.append({
        "section": "words",
        "category": "Feelings and Emotions",
        "level": "INTERMEDIATE",
        "telugu_text": "కంగారుగా / ఆందోళనగా ఉండటం",
        "telugu_transliteration": "Anxious",
        "english_text": "Anxious",
        "pronunciation": "/ˈæŋk.ʃəs/",
        "part_of_speech": "Adjective",
        "english_definition": "Experiencing worry, nervousness, or unease, typically about an imminent event or uncertain outcome.",
        "when_to_use": "Use when describing nervousness before an exam, job interview, or medical report.",
        "examples_json": [
            {"english": "I felt anxious before my first job interview.", "telugu": "నా మొదటి జాబ్ ఇంటర్వ్యూకు ముందు నాకు కొంచెం కంగారుగా అనిపించింది."},
            {"english": "Take a deep breath if you feel anxious while speaking.", "telugu": "మాట్లాడేటప్పుడు మీకు కంగారు అనిపిస్తే దీర్ఘంగా శ్వాస తీసుకోండి."}
        ],
        "common_mistakes_json": [
            {"incorrect": "I am having anxious.", "correct": "I am feeling anxious / I am anxious.", "reason": "'Anxious' is an adjective, not a noun."}
        ],
        "synonyms_json": ["Nervous", "Apprehensive", "Worried", "Uneasy"]
    })

    # 8. Workplace Vocabulary
    items_to_add.append({
        "section": "words",
        "category": "Workplace Vocabulary",
        "level": "INTERMEDIATE",
        "telugu_text": "కలిసి పనిచేయడం / సమన్వయం",
        "telugu_transliteration": "Collaboration",
        "english_text": "Collaboration",
        "pronunciation": "/kəˌlæb.əˈreɪ.ʃən/",
        "part_of_speech": "Noun",
        "english_definition": "The action of working with someone to produce or create something.",
        "when_to_use": "Use in corporate updates, resumes, and interview explanations of teamwork.",
        "examples_json": [
            {"english": "Effective collaboration between designers and developers ensures high quality.", "telugu": "డిజైనర్లు మరియు డెవలపర్ల మధ్య ప్రభావవంతమైన సహకారం నాణ్యతను నిర్ధారిస్తుంది."},
            {"english": "We solved the server issue in close collaboration with the DevOps team.", "telugu": "మేము డెవ్ఆప్స్ టీమ్‌తో సన్నిహిత సమన్వయంతో సర్వర్ సమస్యను పరిష్కరించాము."}
        ],
        "common_mistakes_json": [
            {"incorrect": "We collaborated to each other.", "correct": "We collaborated with each other.", "reason": "Use 'collaborate WITH someone'."}
        ],
        "synonyms_json": ["Teamwork", "Partnership", "Cooperation"]
    })

    # 9. Office Vocabulary
    items_to_add.append({
        "section": "words",
        "category": "Office Vocabulary",
        "level": "INTERMEDIATE",
        "telugu_text": "సమావేశంలో చర్చించాల్సిన అంశాల పట్టిక",
        "telugu_transliteration": "Agenda",
        "english_text": "Agenda",
        "pronunciation": "/əˈdʒen.də/",
        "part_of_speech": "Noun",
        "english_definition": "A list of items to be discussed or acted upon at a formal meeting.",
        "when_to_use": "Use before starting team meetings, client calls, or project standups.",
        "examples_json": [
            {"english": "What is the agenda for today's team standup meeting?", "telugu": "ఈరోజు టీమ్ స్టాండప్ మీటింగ్‌లో చర్చించాల్సిన అంశాలు ఏమిటి?"},
            {"english": "Let's stick to the agenda so we finish on time.", "telugu": "మనం సమయానికి పూర్తి చేయడానికి అజెండా ప్రకారమే చర్చిద్దాం."}
        ],
        "common_mistakes_json": [
            {"incorrect": "The agendums are ready.", "correct": "The agenda is ready.", "reason": "'Agenda' is used as a singular collective noun in modern English."}
        ],
        "synonyms_json": ["Schedule", "Plan", "Timetable", "List of topics"]
    })

    # 10. Interview Vocabulary
    items_to_add.append({
        "section": "words",
        "category": "Interview Vocabulary",
        "level": "ADVANCED",
        "telugu_text": "విజయవంతంగా సాధించడం",
        "telugu_transliteration": "Accomplish",
        "english_text": "Accomplish",
        "pronunciation": "/əˈkɑːm.plɪʃ/",
        "part_of_speech": "Verb",
        "english_definition": "To achieve or complete something successfully.",
        "when_to_use": "Use in resume bullet points and interview responses when describing achievements and milestones.",
        "examples_json": [
            {"english": "We accomplished the project deployment two days ahead of schedule.", "telugu": "మేము షెడ్యూల్ కంటే రెండు రోజుల ముందే ప్రాజెక్ట్ డెప్లాయ్‌మెంట్‌ను విజయవంతంగా సాధించాము."},
            {"english": "Tell me about a major goal you accomplished recently.", "telugu": "ఇటీవల మీరు విజయవంతంగా పూర్తి చేసిన ముఖ్యమైన లక్ష్యం గురించి చెప్పండి."}
        ],
        "common_mistakes_json": [
            {"incorrect": "I accomplished to build the app.", "correct": "I accomplished building the app / I succeeded in building the app.", "reason": "'Accomplish' takes a direct noun object."}
        ],
        "synonyms_json": ["Achieve", "Fulfill", "Execute", "Attain"]
    })

    # 11. Technology Vocabulary
    items_to_add.append({
        "section": "words",
        "category": "Technology Vocabulary",
        "level": "INTERMEDIATE",
        "telugu_text": "సర్వర్‌లోకి లేదా క్లౌడ్‌లోకి కోడ్ పంపించడం",
        "telugu_transliteration": "Deployment",
        "english_text": "Deployment",
        "pronunciation": "/dɪˈplɔɪ.mənt/",
        "part_of_speech": "Noun",
        "english_definition": "The process of moving software or an application to a production server so users can access it.",
        "when_to_use": "Use when explaining DevOps, backend updates, release pipelines, and cloud hosting.",
        "examples_json": [
            {"english": "Our automated deployment pipeline triggers upon every Git push.", "telugu": "ప్రతి గిట్ పుష్ జరిగినప్పుడు మా ఆటోమేటెడ్ డెప్లాయ్‌మెంట్ పైప్‌లైన్ ప్రారంభమవుతుంది."},
            {"english": "The deployment went smoothly without any server downtime.", "telugu": "ఎలాంటి సర్వర్ డౌన్‌టైమ్ లేకుండా డెప్లాయ్‌మెంట్ సాఫీగా జరిగింది."}
        ],
        "common_mistakes_json": [
            {"incorrect": "We deployed the code to local (local is not a deployment).", "correct": "We ran the code locally and deployed it to production.", "reason": "'Deployment' refers to delivery to a live or staging host environment."}
        ],
        "synonyms_json": ["Release", "Rollout", "Launch"]
    })

    # 12. Commonly Confused Words
    items_to_add.append({
        "section": "words",
        "category": "Commonly Confused Words",
        "level": "BEGINNER",
        "telugu_text": "సలహా (నామవాచకం) vs సలహా ఇవ్వడం (క్రియ)",
        "telugu_transliteration": "Advice vs Advise",
        "english_text": "Advice vs Advise",
        "pronunciation": "/ədˈvaɪs/ (Noun) vs /ədˈvaɪz/ (Verb)",
        "part_of_speech": "Noun vs Verb",
        "english_definition": "'Advice' with a 'c' is the recommendation (noun). 'Advise' with an 's' is the action of recommending (verb).",
        "when_to_use": "Use 'advice' when you receive guidance; use 'advise' when someone tells or guides you to do something.",
        "examples_json": [
            {"english": "Thank you for your valuable advice. (Noun)", "telugu": "మీ విలువైన సలహాకు ధన్యవాదాలు."},
            {"english": "My mentor advised me to practice daily. (Verb)", "telugu": "రోజూ ప్రాక్టీస్ చేయాలని నా మెంటార్ నాకు సలహా ఇచ్చారు."}
        ],
        "common_mistakes_json": [
            {"incorrect": "He gave me a good advise.", "correct": "He gave me good advice.", "reason": "Use 'advice' with a 'c' as a noun. Also, 'advice' is uncountable—say 'a piece of advice' or just 'advice'."}
        ],
        "synonyms_json": ["Recommendation", "Guidance", "Counsel"]
    })

    # 13. Verbs Used in Daily Life
    items_to_add.append({
        "section": "words",
        "category": "Verbs Used in Daily Life",
        "level": "BEGINNER",
        "telugu_text": "గమనించడం / చూడటం",
        "telugu_transliteration": "Notice",
        "english_text": "Notice",
        "pronunciation": "/ˈnoʊ.tɪs/",
        "part_of_speech": "Verb",
        "english_definition": "To become aware of something by seeing, hearing, or sensing it.",
        "when_to_use": "Use when identifying a change, an error in code, or a colleague's mood.",
        "examples_json": [
            {"english": "Did you notice the typo in the email subject?", "telugu": "ఈమెయిల్ సబ్జెక్ట్‌లో ఉన్న చిన్న తప్పును మీరు గమనించారా?"},
            {"english": "I noticed that the API is responding much faster now.", "telugu": "ఏపీఐ ఇప్పుడు చాలా వేగంగా రెస్పాన్స్ ఇస్తోందని నేను గమనించాను."}
        ],
        "common_mistakes_json": [
            {"incorrect": "I saw that he was absent (neutral).", "correct": "I noticed that he was absent (more observant).", "reason": "'Notice' conveys active perception compared to casual seeing."}
        ],
        "synonyms_json": ["Observe", "Spot", "Detect", "Perceive"]
    })

    # 14. Adjectives Used in Conversations
    items_to_add.append({
        "section": "words",
        "category": "Adjectives Used in Conversations",
        "level": "INTERMEDIATE",
        "telugu_text": "స్పష్టంగా కనిపించే / సహజంగా తెలిసే",
        "telugu_transliteration": "Obvious",
        "english_text": "Obvious",
        "pronunciation": "/ˈɑːb.vi.əs/",
        "part_of_speech": "Adjective",
        "english_definition": "Easily perceived or understood; clear, self-evident, or apparent.",
        "when_to_use": "Use when a fact or conclusion is very clear and needs no explanation.",
        "examples_json": [
            {"english": "It is obvious that daily speaking practice improves fluency.", "telugu": "రోజూ మాట్లాడటం ప్రాక్టీస్ చేస్తే ఫ్లూయెన్సీ మెరుగవుతుందని స్పష్టంగా తెలుస్తుంది."},
            {"english": "The solution was so obvious once we read the logs.", "telugu": "లాగ్స్ చదివిన వెంటనే పరిష్కారం చాలా స్పష్టంగా కనిపించింది."}
        ],
        "common_mistakes_json": [
            {"incorrect": "It is clearly obvious.", "correct": "It is obvious.", "reason": "Avoid redundancy; 'obvious' already means clearly evident."}
        ],
        "synonyms_json": ["Clear", "Evident", "Apparent", "Manifest"]
    })

    # 15. Advanced Vocabulary
    items_to_add.append({
        "section": "words",
        "category": "Advanced Vocabulary",
        "level": "ADVANCED",
        "telugu_text": "చాలా సూక్ష్మంగా మరియు శ్రద్ధగా పనిచేసే",
        "telugu_transliteration": "Meticulous",
        "english_text": "Meticulous",
        "pronunciation": "/məˈtɪk.jə.ləs/",
        "part_of_speech": "Adjective",
        "english_definition": "Showing great attention to detail; very careful and precise.",
        "when_to_use": "Use to describe thorough work, careful code review, or high-standard execution.",
        "examples_json": [
            {"english": "She is meticulous about code quality and automated testing.", "telugu": "ఆమె కోడ్ క్వాలిటీ మరియు టెస్టింగ్ విషయంలో చాలా శ్రద్ధగా ఉంటుంది."},
            {"english": "His meticulous planning ensured the launch was a total success.", "telugu": "అతని సూక్ష్మమైన ప్రణాళిక విడుదల గొప్ప విజయం సాధించేలా చేసింది."}
        ],
        "common_mistakes_json": [
            {"incorrect": "He works meticulously clean.", "correct": "He works meticulously / His work is meticulous.", "reason": "Use adverb 'meticulously' to modify verbs, adjective 'meticulous' for nouns."}
        ],
        "synonyms_json": ["Diligent", "Thorough", "Scrupulous", "Precise"]
    })

    # =========================================================================
    # SECTION 2: DAILY USE PHRASES AND EXPRESSIONS (14 Categories)
    # =========================================================================

    # Contextual equivalents for key expressions highlighted in prompt:
    items_to_add.append({
        "section": "phrases",
        "category": "Daily Conversations",
        "level": "BEGINNER",
        "telugu_text": "పోనీ లే",
        "telugu_transliteration": "Poni le",
        "english_text": "Never mind / It's okay",
        "pronunciation": "/ˈnev.ər maɪnd/",
        "part_of_speech": "Conversational Expression",
        "english_definition": "Used to tell someone not to worry about something or to drop a topic that is no longer important.",
        "when_to_use": "Use when something small went wrong and you want to reassure the other person, or when you decide not to repeat what you were saying.",
        "contextual_alternatives_json": [
            {"english": "Never mind", "context": "When you decide what you were saying is not important: 'I was going to ask, but never mind.'"},
            {"english": "It's okay / Don't worry about it", "context": "When consoling someone who made a small mistake: 'You spilled a little water? Poni le, it's okay!'"},
            {"english": "Let it be", "context": "When you want to stop arguing or leave a situation as it is."}
        ],
        "examples_json": [
            {"english": "Don't worry about the delay, it's okay!", "telugu": "ఆలస్యమైనందుకు చింతించకండి, పోనీ లే పర్లేదు!"},
            {"english": "I was looking for my pen, but never mind, I found another one.", "telugu": "నా పెన్ కోసం చూస్తున్నాను, కానీ పోనీ లే, నాకు ఇంకొకటి దొరికింది."}
        ],
        "common_mistakes_json": [
            {"incorrect": "Leave it on (literal Telugu translation).", "correct": "Let it go / Never mind.", "reason": "Do not translate Telugu 'vadhiley / poni le' literally as 'leave it on'."}
        ],
        "synonyms_json": ["Forget about it", "Don't fret", "No worries"]
    })

    items_to_add.append({
        "section": "phrases",
        "category": "Agreeing and Disagreeing",
        "level": "BEGINNER",
        "telugu_text": "పర్లేదు",
        "telugu_transliteration": "Parledu",
        "english_text": "It's okay / No problem",
        "pronunciation": "/ɪts oʊˈkeɪ/",
        "part_of_speech": "Conversational Expression",
        "english_definition": "Used to express that everything is fine, an apology is accepted, or a situation is manageable.",
        "when_to_use": "Use in response to 'Thank you', 'Sorry', or when evaluating whether something is acceptable.",
        "contextual_alternatives_json": [
            {"english": "No problem / Not at all", "context": "When responding politely to 'Thank you' or an apology."},
            {"english": "It's alright / That's fine", "context": "When someone arrives slightly late or makes a minor error."},
            {"english": "Not bad", "context": "When expressing that something is decent: 'How is the food? - Parledu, not bad.'"}
        ],
        "examples_json": [
            {"english": "A: 'Thank you for helping me!' B: 'Parledu! No problem at all.'", "telugu": "A: 'నాకు సహాయం చేసినందుకు ధన్యవాదాలు!' B: 'పర్లేదండి, పర్వాలేదు!'"},
            {"english": "A: 'I'm so sorry I'm 5 minutes late.' B: 'It's alright, don't worry.'", "telugu": "A: '5 నిమిషాలు ఆలస్యమైనందుకు క్షమించండి.' B: 'పర్లేదు, పరవాలేదు.'"}
        ],
        "common_mistakes_json": [
            {"incorrect": "No mention (broken Indian English).", "correct": "Don't mention it / No problem / You're welcome.", "reason": "Say 'Don't mention it' or 'No problem', never just 'No mention'."}
        ],
        "synonyms_json": ["You're welcome", "No worries", "Anytime"]
    })

    items_to_add.append({
        "section": "phrases",
        "category": "Giving Suggestions",
        "level": "BEGINNER",
        "telugu_text": "చూద్దాం",
        "telugu_transliteration": "Chuddam",
        "english_text": "Let's see",
        "pronunciation": "/lets siː/",
        "part_of_speech": "Conversational Expression",
        "english_definition": "Used when waiting to find out what happens before making a final decision.",
        "when_to_use": "Use when you want to evaluate future conditions, weather, or plans before committing.",
        "contextual_alternatives_json": [
            {"english": "Let's see", "context": "Casual everyday usage: 'Will it rain today? - Let's see.'"},
            {"english": "We'll see how it goes", "context": "Professional or deliberate pause: 'Let's monitor the server metrics and see how it goes.'"},
            {"english": "Time will tell", "context": "Philosophical or long-term evaluation."}
        ],
        "examples_json": [
            {"english": "A: 'Are we going to the movie this Sunday?' B: 'Chuddam, let's see how busy we are.'", "telugu": "A: 'మనం ఈ ఆదివారం సినిమాకి వెళ్తున్నామా?' B: 'చూద్దాం, పనులను బట్టి నిర్ణయిద్దాం.'"},
            {"english": "Let's see what the manager suggests in tomorrow's meeting.", "telugu": "రేపటి మీటింగ్‌లో మేనేజర్ ఏమి సలహా ఇస్తారో చూద్దాం."}
        ],
        "common_mistakes_json": [
            {"incorrect": "We will watch (literal translation of chuddam).", "correct": "Let's see.", "reason": "'Watch' means looking at video/TV. To express 'we will find out', use 'let's see'."}
        ],
        "synonyms_json": ["We'll find out", "Let's wait and watch"]
    })

    items_to_add.append({
        "section": "phrases",
        "category": "Giving Answers",
        "level": "BEGINNER",
        "telugu_text": "నాకు అర్థమైంది",
        "telugu_transliteration": "Naaku arthamaindi",
        "english_text": "I got it / I understand",
        "pronunciation": "/aɪ ɡɑːt ɪt/",
        "part_of_speech": "Conversational Expression",
        "english_definition": "Used to acknowledge comprehension of an instruction, concept, or explanation.",
        "when_to_use": "Use in discussions, training sessions, or coding meetings when a concept becomes clear.",
        "contextual_alternatives_json": [
            {"english": "I got it / Got it!", "context": "Casual, fast conversational confirmation with colleagues or friends."},
            {"english": "I understand completely", "context": "Formal or empathetic communication with managers or clients."},
            {"english": "That makes sense", "context": "When someone explains their logic and you agree with it."}
        ],
        "examples_json": [
            {"english": "A: 'Click here to submit the form.' B: 'Got it, thanks!'", "telugu": "A: 'ఫారమ్ సబ్మిట్ చేయడానికి ఇక్కడ క్లిక్ చేయండి.' B: 'అర్థమైంది, థాంక్స్!'"},
            {"english": "I understand the requirement clearly now.", "telugu": "రిక్వైర్‌మెంట్ ఇప్పుడు నాకు స్పష్టంగా అర్థమైంది."}
        ],
        "common_mistakes_json": [
            {"incorrect": "I understooded.", "correct": "I understood / I got it.", "reason": "'Understood' is already the past tense of 'understand'."}
        ],
        "synonyms_json": ["Understood", "Clear", "Makes sense"]
    })

    items_to_add.append({
        "section": "phrases",
        "category": "Agreeing and Disagreeing",
        "level": "INTERMEDIATE",
        "telugu_text": "అలా కాదు",
        "telugu_transliteration": "Alaa kaadhu",
        "english_text": "That's not how it works / That's not what I meant",
        "pronunciation": "/ðæts nɑːt haʊ ɪt wɜːrks/",
        "part_of_speech": "Conversational Expression",
        "english_definition": "Used to correct a misunderstanding or clarify that a procedure or statement is incorrect.",
        "when_to_use": "Use gently when clarifying your intention or correcting a technical process.",
        "contextual_alternatives_json": [
            {"english": "That's not what I meant", "context": "When someone misinterprets your words: 'Ala kaadhu, that's not what I meant to say.'"},
            {"english": "That's not how it works", "context": "When correcting someone on how a tool, system, or process operates."},
            {"english": "Not quite", "context": "Polite way of saying someone is partially wrong."}
        ],
        "examples_json": [
            {"english": "That's not quite what I meant; let me clarify.", "telugu": "నా ఉద్దేశ్యం అది కాదు; నేను స్పష్టంగా వివరిస్తాను."},
            {"english": "That's not how this algorithm works.", "telugu": "ఈ అల్గోరిథం పనిచేసే విధానం అలా కాదు."}
        ],
        "common_mistakes_json": [
            {"incorrect": "Not like that (too abrupt in professional settings).", "correct": "That's not quite what I meant / Not exactly.", "reason": "'Not like that' sounds harsh; 'That's not what I meant' is courteous."}
        ],
        "synonyms_json": ["Not exactly", "Not quite", "Let me rephrase"]
    })

    items_to_add.append({
        "section": "phrases",
        "category": "Friends and Family",
        "level": "BEGINNER",
        "telugu_text": "వదిలేయ్",
        "telugu_transliteration": "Vadhiley",
        "english_text": "Let it go / Drop it",
        "pronunciation": "/let ɪt ɡoʊ/",
        "part_of_speech": "Conversational Expression",
        "english_definition": "Used to tell someone to stop thinking about a frustrating issue or past argument.",
        "when_to_use": "Use when comforting a friend or asking someone to move on from a past problem.",
        "contextual_alternatives_json": [
            {"english": "Let it go", "context": "Encouraging emotional release: 'Don't hold onto anger, let it go.'"},
            {"english": "Drop it", "context": "Firm request to stop discussing an annoying topic right now."},
            {"english": "Forget about it", "context": "Casual reassurance that an issue is resolved."}
        ],
        "examples_json": [
            {"english": "You can't change what happened yesterday, so let it go.", "telugu": "నిన్న జరిగినదాన్ని నువ్వు మార్చలేవు, కాబట్టి దాన్ని వదిలేయ్."},
            {"english": "Let's drop this topic and focus on the future.", "telugu": "ఈ విషయాన్ని ఇక్కడితో వదిలేసి భవిష్యత్తుపై దృష్టి పెడదాం."}
        ],
        "common_mistakes_json": [
            {"incorrect": "Leave it away.", "correct": "Let it go / Drop it.", "reason": "'Leave it away' is incorrect English; use the idiom 'let it go'."}
        ],
        "synonyms_json": ["Move on", "Put it behind you"]
    })

    items_to_add.append({
        "section": "phrases",
        "category": "Daily Conversations",
        "level": "BEGINNER",
        "telugu_text": "నాకు గుర్తుంది",
        "telugu_transliteration": "Naaku gurthundi",
        "english_text": "I remember",
        "pronunciation": "/aɪ rɪˈmem.bər/",
        "part_of_speech": "Conversational Expression",
        "english_definition": "Used to state that a fact or memory has been retained in your mind.",
        "when_to_use": "Use when confirming a task, appointment, or past story.",
        "contextual_alternatives_json": [
            {"english": "I remember", "context": "Standard confirmation: 'Yes, I remember our conversation.'"},
            {"english": "It's on my mind", "context": "When assuring a manager an action item is being prioritized."},
            {"english": "I recall", "context": "Slightly formal: 'As far as I recall, the deadline was Friday.'"}
        ],
        "examples_json": [
            {"english": "I remember what you told me yesterday.", "telugu": "నిన్న నువ్వు నాకు చెప్పిన మాట నాకు గుర్తుంది."},
            {"english": "Don't worry, I remember to submit the report before 5 PM.", "telugu": "కంగారు పడకండి, సాయంత్రం 5 గంటలలోపు రిపోర్ట్ ఇవ్వాలని నాకు గుర్తుంది."}
        ],
        "common_mistakes_json": [
            {"incorrect": "I am remembering.", "correct": "I remember.", "reason": "'Remember' is a stative verb; do not use in continuous tense for general memory."}
        ],
        "synonyms_json": ["I recall", "I recollect"]
    })

    items_to_add.append({
        "section": "phrases",
        "category": "Daily Conversations",
        "level": "BEGINNER",
        "telugu_text": "నాకు గుర్తులేదు",
        "telugu_transliteration": "Naaku gurthuledu",
        "english_text": "I don't remember / It slipped my mind",
        "pronunciation": "/aɪ doʊnt rɪˈmem.bər/",
        "part_of_speech": "Conversational Expression",
        "english_definition": "Used to state that you have forgotten a detail, password, or event.",
        "when_to_use": "Use when you cannot recall a name, number, or scheduled task.",
        "contextual_alternatives_json": [
            {"english": "I don't remember", "context": "Direct and plain: 'I don't remember his exact phone number.'"},
            {"english": "It slipped my mind", "context": "Polite apology for momentarily forgetting a task: 'Sorry, it completely slipped my mind.'"},
            {"english": "I can't recall right now", "context": "Professional reply in interviews or meetings."}
        ],
        "examples_json": [
            {"english": "I apologize, it completely slipped my mind to send the email.", "telugu": "క్షమించండి, ఈమెయిల్ పంపించాలనే విషయం నాకు పూర్తిగా గుర్తులేదు."},
            {"english": "I don't remember where I kept my car keys.", "telugu": "నా కార్ కీస్ ఎక్కడ పెట్టానో నాకు గుర్తులేదు."}
        ],
        "common_mistakes_json": [
            {"incorrect": "I not remember.", "correct": "I don't remember.", "reason": "Use auxiliary 'do not / don't' to negate present tense verbs."}
        ],
        "synonyms_json": ["I've forgotten", "It escapes me"]
    })

    # =========================================================================
    # SECTION 3: COMPLETE TELUGU-TO-ENGLISH SENTENCES
    # =========================================================================

    items_to_add.append({
        "section": "sentences",
        "category": "Daily Conversations",
        "level": "BEGINNER",
        "telugu_text": "నేను మీకు కాల్ చేయవచ్చా?",
        "telugu_transliteration": "Nenu meeku call cheyavachaa?",
        "english_text": "Can I give you a call?",
        "pronunciation": "/kæn aɪ ɡɪv juː ə kɔːl/",
        "part_of_speech": "Polite Question",
        "english_definition": "A friendly and natural way to ask someone permission to speak on the phone.",
        "when_to_use": "Use over WhatsApp, Slack, Teams, or SMS before calling a colleague, friend, or client.",
        "sentence_structure": "Modal verb (Can/Could) + Subject (I) + Verb Phrase (give you a call)",
        "word_by_word_json": [
            {"telugu": "నేను", "english": "I"},
            {"telugu": "మీకు", "english": "you / to you"},
            {"telugu": "కాల్ చేయవచ్చా?", "english": "can give a call / may I call?"}
        ],
        "contextual_alternatives_json": [
            {"english": "Could I call you now?", "context": "More formal / polite request."},
            {"english": "Are you free for a quick call?", "context": "Workplace etiquette on Slack or Teams."}
        ],
        "examples_json": [
            {"english": "Are you at your desk? Can I give you a quick call?", "telugu": "మీరు డెస్క్ దగ్గరే ఉన్నారా? నేను మీకు ఒకసారి కాల్ చేయవచ్చా?"},
            {"english": "Could I give you a call around 3 PM to discuss the project?", "telugu": "ప్రాజెక్ట్ గురించి మాట్లాడటానికి నేను మధ్యాహ్నం 3 గంటలకు మీకు కాల్ చేయవచ్చా?"}
        ],
        "common_mistakes_json": [
            {"incorrect": "Shall I do call to you? (literal Telugu translation)", "correct": "Can I give you a call?", "reason": "Never say 'do call to you'. In English, say 'give you a call' or 'call you'."}
        ],
        "synonyms_json": ["May I call you?", "Can we talk on the phone?"]
    })

    items_to_add.append({
        "section": "sentences",
        "category": "Workplace and Office",
        "level": "INTERMEDIATE",
        "telugu_text": "నేను మీకు సోమవారం అప్డేట్ ఇస్తాను.",
        "telugu_transliteration": "Nenu meeku somavaaram update isthaanu.",
        "english_text": "I'll give you an update by Monday.",
        "pronunciation": "/aɪl ɡɪv juː ən ˈʌp.deɪt baɪ ˈmʌn.deɪ/",
        "part_of_speech": "Professional Statement",
        "english_definition": "A commitment to provide progress information before or on Monday.",
        "when_to_use": "Use in status emails, sprint planning, and client communications.",
        "sentence_structure": "Future Simple (I will + V1) with preposition of deadline (by Monday).",
        "word_by_word_json": [
            {"telugu": "నేను", "english": "I"},
            {"telugu": "మీకు", "english": "you"},
            {"telugu": "సోమవారం", "english": "by Monday"},
            {"telugu": "అప్డేట్ ఇస్తాను", "english": "will give an update"}
        ],
        "contextual_alternatives_json": [
            {"english": "I'll keep you posted by Monday.", "context": "Idiomatic professional alternative."},
            {"english": "I will get back to you with an update on Monday.", "context": "Formal client communication."}
        ],
        "examples_json": [
            {"english": "We are still running the tests; I'll give you an update by Monday morning.", "telugu": "మేము ఇంకా టెస్టులు రన్ చేస్తున్నాము; నేను మీకు సోమవారం ఉదయానికల్లా అప్డేట్ ఇస్తాను."},
            {"english": "I will keep you posted once the review is completed.", "telugu": "రివ్యూ పూర్తి కాగానే నేను మీకు సమాచారం అందిస్తాను."}
        ],
        "common_mistakes_json": [
            {"incorrect": "I will give update in Monday.", "correct": "I'll give you an update BY Monday.", "reason": "Use 'by' to mean deadline, and don't omit the article 'an update'."}
        ],
        "synonyms_json": ["I will update you by Monday", "I'll keep you informed"]
    })

    items_to_add.append({
        "section": "sentences",
        "category": "Workplace and Office",
        "level": "BEGINNER",
        "telugu_text": "మా మేనేజర్ సెలవులో ఉన్నారు.",
        "telugu_transliteration": "Maa manager selavulo unnaaru.",
        "english_text": "My manager is on leave.",
        "pronunciation": "/maɪ ˈmæn.ə.dʒər ɪz ɑːn liːv/",
        "part_of_speech": "Workplace Statement",
        "english_definition": "States that your manager is away from work due to vacation or sick time.",
        "when_to_use": "Use when someone asks to speak with your manager or asks for manager approval.",
        "sentence_structure": "Subject (My manager) + linking verb (is) + prepositional phrase (on leave).",
        "word_by_word_json": [
            {"telugu": "మా మేనేజర్", "english": "My manager"},
            {"telugu": "సెలవులో", "english": "on leave"},
            {"telugu": "ఉన్నారు", "english": "is"}
        ],
        "contextual_alternatives_json": [
            {"english": "My manager is out of office today.", "context": "Very common corporate expression (OOO)."},
            {"english": "She is taking the day off.", "context": "Informal peer conversation."}
        ],
        "examples_json": [
            {"english": "My manager is on leave today, but I can help you with this issue.", "telugu": "మా మేనేజర్ ఈరోజు సెలవులో ఉన్నారు, కానీ ఈ సమస్య విషయంలో నేను మీకు సహాయం చేయగలను."},
            {"english": "Our team lead is out of the office until Thursday.", "telugu": "మా టీమ్ లీడ్ గురువారం వరకు సెలవులో ఉన్నారు."}
        ],
        "common_mistakes_json": [
            {"incorrect": "My manager is in leave.", "correct": "My manager is ON leave.", "reason": "The correct preposition is 'on leave', never 'in leave'."}
        ],
        "synonyms_json": ["Out of office", "On vacation", "Off duty"]
    })

    items_to_add.append({
        "section": "sentences",
        "category": "Meetings and Calls",
        "level": "BEGINNER",
        "telugu_text": "నా మాట వినిపిస్తోందా?",
        "telugu_transliteration": "Naa maata vinipisthondaa?",
        "english_text": "Am I audible? / Can you hear me?",
        "pronunciation": "/æm aɪ ˈɔː.də.bəl/",
        "part_of_speech": "Meeting Question",
        "english_definition": "Used to verify that your microphone and voice are reaching participants in an online meeting.",
        "when_to_use": "Use at the start of Zoom, Google Meet, or Teams video calls.",
        "sentence_structure": "Inverted question: Helping Verb (Am/Can) + Subject (I/you) + Adjective/Verb.",
        "word_by_word_json": [
            {"telugu": "నా మాట", "english": "my voice / me"},
            {"telugu": "వినిపిస్తోందా?", "english": "is it audible? / can you hear?"}
        ],
        "contextual_alternatives_json": [
            {"english": "Can you hear me clearly?", "context": "Most natural everyday English across global teams."},
            {"english": "Am I audible?", "context": "Common in Indian corporate settings, though 'Can you hear me' is preferred globally."}
        ],
        "examples_json": [
            {"english": "Hi everyone, can you hear me clearly?", "telugu": "అందరికీ నమస్కారం, నా మాట స్పష్టంగా వినిపిస్తోందా?"},
            {"english": "Sorry, you were on mute. Am I audible now?", "telugu": "క్షమించండి, మీరు మ్యూట్‌లో ఉన్నారు. ఇప్పుడు నా మాట వినిపిస్తోందా?"}
        ],
        "common_mistakes_json": [
            {"incorrect": "My voice is coming? (literal Telugu translation)", "correct": "Can you hear me? / Am I audible?", "reason": "Never say 'My voice is coming'. Say 'Can you hear me?'."}
        ],
        "synonyms_json": ["Can you hear me?", "Is my audio clear?"]
    })

    items_to_add.append({
        "section": "sentences",
        "category": "Workplace and Office",
        "level": "BEGINNER",
        "telugu_text": "నేను నా పని పూర్తి చేశాను.",
        "telugu_transliteration": "Nenu naa pani poorthi chesaanu.",
        "english_text": "I have completed my work.",
        "pronunciation": "/aɪ hæv kəmˈpliː.tɪd maɪ wɜːrk/",
        "part_of_speech": "Status Statement",
        "english_definition": "States that your allocated task has just been finished.",
        "when_to_use": "Use when reporting completion of a task, sprint ticket, or assignment.",
        "sentence_structure": "Present Perfect: Subject (I) + have + Past Participle (completed) + Object.",
        "word_by_word_json": [
            {"telugu": "నేను", "english": "I"},
            {"telugu": "నా పని", "english": "my work / task"},
            {"telugu": "పూర్తి చేశాను", "english": "have completed"}
        ],
        "contextual_alternatives_json": [
            {"english": "I'm all done with my task.", "context": "Casual workplace phrasing."},
            {"english": "I've wrapped up my assignments.", "context": "Idiomatic native phrasing."}
        ],
        "examples_json": [
            {"english": "I have completed my work and pushed the code to Git.", "telugu": "నేను నా పని పూర్తి చేశాను మరియు కోడ్‌ను గిట్‌కు పుష్ చేశాను."},
            {"english": "I'm done with today's tasks; let me know if you need any assistance.", "telugu": "ఈరోజు నా పనులు పూర్తయ్యాయి; మీకు ఏమైనా సహాయం కావాలంటే చెప్పండి."}
        ],
        "common_mistakes_json": [
            {"incorrect": "My work is overed.", "correct": "I have completed my work / My work is done.", "reason": "'Overed' is not a word in English. Say 'My work is done' or 'I have finished'."}
        ],
        "synonyms_json": ["I'm done", "I've finished my task"]
    })

    items_to_add.append({
        "section": "sentences",
        "category": "Meetings and Calls",
        "level": "BEGINNER",
        "telugu_text": "మీరు మళ్ళీ చెప్పగలరా?",
        "telugu_transliteration": "Meeru malli cheppagalaraa?",
        "english_text": "Could you say that again?",
        "pronunciation": "/kʊd juː seɪ ðæt əˈɡen/",
        "part_of_speech": "Polite Request",
        "english_definition": "A courteous request asking someone to repeat what they just said because you did not hear or understand.",
        "when_to_use": "Use when internet glitches occur, background noise interferes, or someone speaks too fast.",
        "sentence_structure": "Polite Modal (Could) + Subject (you) + Verb (say) + Object (that again).",
        "word_by_word_json": [
            {"telugu": "మీరు", "english": "you"},
            {"telugu": "మళ్ళీ", "english": "again"},
            {"telugu": "చెప్పగలరా?", "english": "could you say?"}
        ],
        "contextual_alternatives_json": [
            {"english": "Pardon me? / Come again?", "context": "Quick polite conversational check."},
            {"english": "Could you please repeat that? I missed the last part.", "context": "Professional meeting clarity."}
        ],
        "examples_json": [
            {"english": "There was a brief lag on the line. Could you say that again?", "telugu": "కాల్‌లో చిన్న అంతరాయం వచ్చింది. మీరు మళ్ళీ చెప్పగలరా?"},
            {"english": "Pardon me, could you repeat the last question?", "telugu": "క్షమించండి, చివరి ప్రశ్నను మళ్ళీ పునరావృతం చేయగలరా?"}
        ],
        "common_mistakes_json": [
            {"incorrect": "Repeat again please (redundant).", "correct": "Could you repeat that? / Could you say that again?", "reason": "'Repeat' already means say again. Never say 'repeat again'."}
        ],
        "synonyms_json": ["Pardon?", "Could you repeat that?"]
    })

    # =========================================================================
    # SECTION 4: SITUATION-BASED EXPRESSIONS (6 Categories with Dialogues)
    # =========================================================================

    items_to_add.append({
        "section": "situations",
        "category": "Workplace and Office English",
        "level": "INTERMEDIATE",
        "telugu_text": "ప్రాజెక్ట్ డెడ్‌లైన్ పొడిగించమని మేనేజర్‌ను అడగడం",
        "telugu_transliteration": "Project deadline podiginchamani adagadam",
        "english_text": "Could we extend the deadline by two days?",
        "pronunciation": "/kʊd wiː ɪkˈstend ðə ˈded.laɪn/",
        "part_of_speech": "Professional Request",
        "english_definition": "A professional way to request additional time on a project without sounding careless.",
        "when_to_use": "Use in 1-on-1 manager check-ins when unexpected technical hurdles require more time for quality testing.",
        "dialogue_json": [
            {"speaker": "Learner", "text": "Hi Rahul, we encountered an unexpected database bug during staging tests. Could we extend the deadline by two days so we can test thoroughly?"},
            {"speaker": "Manager", "text": "Thanks for flagging this early. Yes, quality is the priority. Let's push the release to Thursday."}
        ],
        "examples_json": [
            {"english": "Due to unexpected API changes, we request a brief deadline extension.", "telugu": "ఊహించని ఏపీఐ మార్పుల వల్ల, మేము గడువును కొద్దిగా పొడిగించాలని కోరుతున్నాము."},
            {"english": "Would it be possible to submit the report on Wednesday instead?", "telugu": "నివేదికను బుధవారం సమర్పించడం సాధ్యమేనా?"}
        ],
        "common_mistakes_json": [
            {"incorrect": "I want more time for finish project.", "correct": "Could we extend the deadline by two days?", "reason": "Saying 'I want more time' sounds blunt; use polite conditional modal phrasing."}
        ]
    })

    items_to_add.append({
        "section": "situations",
        "category": "Meetings and Professional Communication",
        "level": "INTERMEDIATE",
        "telugu_text": "మీటింగ్ మధ్యలో మర్యాదగా జోక్యం చేసుకుని మాట్లాడటం",
        "telugu_transliteration": "Meeting lo maryadaga madhyalo matladadam",
        "english_text": "Sorry to interrupt, but may I add a quick point here?",
        "pronunciation": "/ˈsɑːr.i tuː ˌɪn.təˈrʌpt bʌt meɪ aɪ æd ə kwɪk pɔɪnt/",
        "part_of_speech": "Polite Interruption",
        "english_definition": "A respectful way to join an ongoing discussion to add valuable information without offending the speaker.",
        "when_to_use": "Use during group calls, architecture debates, or strategy meetings.",
        "dialogue_json": [
            {"speaker": "Colleague", "text": "...and that is why we should consider using the third-party authentication library."},
            {"speaker": "Learner", "text": "Sorry to interrupt, Priya, but may I add a quick point? That library has a known memory leak issue in the latest version."},
            {"speaker": "Colleague", "text": "Good catch! Thanks for pointing that out."}
        ],
        "examples_json": [
            {"english": "May I jump in here with a quick suggestion?", "telugu": "నేను ఇక్కడ ఒక చిన్న సలహా ఇవ్వవచ్చా?"},
            {"english": "Excuse me for interrupting, but I have a quick update on that.", "telugu": "మధ్యలో మాట్లాడినందుకు క్షమించండి, కానీ దానిపై నా దగ్గర చిన్న అప్డేట్ ఉంది."}
        ],
        "common_mistakes_json": [
            {"incorrect": "Stop, I want to tell something (rude).", "correct": "Sorry to interrupt, may I add a quick point?", "reason": "Never interrupt abruptly without courtesy words."}
        ]
    })

    items_to_add.append({
        "section": "situations",
        "category": "Shopping and Travel",
        "level": "BEGINNER",
        "telugu_text": "సూపర్ మార్కెట్‌లో ఒక వస్తువు ఎక్కడ ఉందో అడగడం",
        "telugu_transliteration": "Supermarket lo vasthuvu ekkada undo adagadam",
        "english_text": "Excuse me, which aisle can I find olive oil in?",
        "pronunciation": "/ɪkˈskjuːz miː wɪtʃ aɪl kæn aɪ faɪnd/",
        "part_of_speech": "Inquiry",
        "english_definition": "How to ask store staff for product locations politely.",
        "when_to_use": "Use in supermarkets, department stores, or retail outlets.",
        "dialogue_json": [
            {"speaker": "Customer", "text": "Excuse me, which aisle can I find organic olive oil in?"},
            {"speaker": "Store Assistant", "text": "That's in Aisle 4, right next to the cooking sauces on the middle shelf."},
            {"speaker": "Customer", "text": "Wonderful, thank you so much for your help!"}
        ],
        "examples_json": [
            {"english": "Excuse me, where can I find fresh bread?", "telugu": "క్షమించండి, తాజా బ్రెడ్ ఎక్కడ దొరుకుతుంది?"},
            {"english": "Could you tell me where the dairy section is located?", "telugu": "డైరీ సెక్షన్ ఎక్కడ ఉందో చెప్పగలరా?"}
        ],
        "common_mistakes_json": [
            {"incorrect": "Where is oil? (too blunt).", "correct": "Excuse me, where can I find the oil?", "reason": "Always begin inquiries with 'Excuse me'."}
        ]
    })

    items_to_add.append({
        "section": "situations",
        "category": "Interview and Career Communication",
        "level": "ADVANCED",
        "telugu_text": "ఇంటర్వ్యూలో ఒక క్లిష్టమైన ప్రాజెక్ట్ సమస్యను ఎలా పరిష్కరించారో వివరించడం",
        "telugu_transliteration": "Interview lo problem solving explain cheyyadam",
        "english_text": "We diagnosed the bottleneck by analyzing database query execution plans.",
        "pronunciation": "/wiː ˌdaɪ.əɡˈnoʊzd ðə ˈbɑː.t̬əl.nek/",
        "part_of_speech": "STAR Storytelling",
        "english_definition": "Explaining the technical action step taken to solve a performance problem.",
        "when_to_use": "Use in technical interviews when asked: 'Tell me about a difficult bug you solved.'",
        "dialogue_json": [
            {"speaker": "Interviewer", "text": "Tell me about a time your API slowed down and how you resolved it."},
            {"speaker": "Candidate", "text": "During peak hours, our login endpoint latency spiked. We diagnosed the bottleneck by analyzing query execution plans and added a composite index, reducing latency by 70%."},
            {"speaker": "Interviewer", "text": "Excellent approach. That shows strong backend optimization skills."}
        ],
        "examples_json": [
            {"english": "We identified the root cause through detailed log aggregation.", "telugu": "వివరణాత్మక లాగ్స్ విశ్లేషణ ద్వారా మేము ప్రధాన కారణాన్ని గుర్తించాము."},
            {"english": "I refactored the legacy function to improve code maintainability.", "telugu": "కోడ్ నిర్వహణను మెరుగుపరచడానికి నేను పాత ఫంక్షన్‌ను రీఫ్యాక్టర్ చేశాను."}
        ],
        "common_mistakes_json": [
            {"incorrect": "We done something and it worked.", "correct": "We diagnosed the issue systematically and applied an indexed query.", "reason": "Use precise technical vocabulary in interviews."}
        ]
    })

    # Save all items
    for data in items_to_add:
        item = WordItem(**data)
        db.add(item)
    db.commit()

    # Seed interactive quiz exercises
    exercises_to_add = [
        {
            "section": "words",
            "exercise_type": "translation",
            "question": "What is the English word for 'సౌకర్యవంతమైన' (fitting someone's plans and needs)?",
            "telugu_prompt": "సరైన ఇంగ్లీష్ పదాన్ని ఎంచుకోండి:",
            "options_json": ["Convenient", "Hesitate", "Utensil", "Clutter"],
            "correct_answer": "Convenient",
            "explanation": "'Convenient' means fitting in well with a person's needs or schedule (e.g. 'Is 4 PM convenient for you?')."
        },
        {
            "section": "phrases",
            "exercise_type": "mcq",
            "question": "A friend apologizes for being 5 minutes late. What is the most natural native response for 'పర్లేదు / ఏమీ అనుకోకు'?",
            "telugu_prompt": "సహజమైన ఇంగ్లీష్ సమాధానం:",
            "options_json": ["Never mind, it's totally fine!", "You are late.", "Leave it away.", "No mention."],
            "correct_answer": "Never mind, it's totally fine!",
            "explanation": "'Never mind, it's totally fine!' or 'No problem at all' is polite, reassuring, and native."
        },
        {
            "section": "sentences",
            "exercise_type": "sentence_formation",
            "question": "How do you politely ask 'నేను మీకు కాల్ చేయవచ్చా?' in English?",
            "telugu_prompt": "మర్యాదపూర్వకమైన వాక్యాన్ని ఎంచుకోండి:",
            "options_json": ["Can I give you a call?", "Shall I do call to you?", "I call you now?", "Give me call."],
            "correct_answer": "Can I give you a call?",
            "explanation": "'Can I give you a call?' or 'Could I give you a quick call?' is the idiomatic standard expression."
        },
        {
            "section": "sentences",
            "exercise_type": "mcq",
            "question": "In a virtual meeting, how do you correctly check 'నా మాట వినిపిస్తోందా?'?",
            "telugu_prompt": "ఆన్‌లైన్ మీటింగ్‌లో సరిగ్గా ఎలా అడగాలి?",
            "options_json": ["Can you hear me clearly?", "My voice is coming?", "Is my speaking hearing?", "Hear my talk?"],
            "correct_answer": "Can you hear me clearly?",
            "explanation": "Never translate literally as 'My voice is coming'. Always say 'Can you hear me clearly?' or 'Am I audible?'."
        },
        {
            "section": "situations",
            "exercise_type": "usage_choice",
            "question": "In an office meeting, what is the most professional way to interrupt politely to add a point?",
            "telugu_prompt": "మీటింగ్‌లో మర్యాదగా మాట్లాడేందుకు ఏది సరైనది?",
            "options_json": [
                "Sorry to interrupt, but may I add a quick point here?",
                "Stop talking, I want to tell something.",
                "Wait please, listen to me now.",
                "Cut the call."
            ],
            "correct_answer": "Sorry to interrupt, but may I add a quick point here?",
            "explanation": "'Sorry to interrupt, but may I add a quick point here?' is courteous, respectful, and standard in global offices."
        }
    ]

    for ex_data in exercises_to_add:
        exercise = WordExercise(**ex_data)
        db.add(exercise)
    db.commit()
