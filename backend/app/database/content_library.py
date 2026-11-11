"""
Built-in structured Words & Expressions Library for SpeakMate AI.
Organized cleanly into the three official learning modes:
1. words: Everyday individual vocabulary across categories & levels.
2. expressions: Daily-use expressions, complete Telugu-to-English sentences, office & interview expressions.
3. situation_expressions: Contextual expressions organized by 9 real-life situation categories.
"""

WORDS_LIBRARY = [
    # Daily Use Words & Core Verbs
    {
        "uid": "word_postpone",
        "section": "words",
        "mode": "words",
        "category": "Daily Use Words",
        "level": "BEGINNER",
        "telugu_text": "వాయిదా వేయడం",
        "telugu_transliteration": "Vaayida veyadam",
        "english_text": "Postpone",
        "valid_alternatives": ["put off", "delay", "defer", "reschedule"],
        "pronunciation": "/pəʊstˈpəʊn/",
        "part_of_speech": "Verb",
        "english_definition": "To arrange for an event or activity to happen at a later time or date.",
        "when_to_use": "Use when plans, meetings, exams, or trips are moved to a future date.",
        "examples": [
            {"english": "We had to postpone the meeting until tomorrow morning.", "telugu": "మనం మీటింగ్‌ను రేపు ఉదయానికి వాయిదా వేయాల్సి వచ్చింది."},
            {"english": "Don't postpone important tasks for later.", "telugu": "ముఖ్యమైన పనులను తర్వాతకు వాయిదా వేయకండి."}
        ],
        "mistakes": [
            {"incorrect": "We postponed the meeting to back.", "correct": "We postponed the meeting until tomorrow.", "reason": "Use 'until' or 'to a later date', not 'to back'."}
        ],
        "synonyms": ["Put off", "Delay", "Defer", "Reschedule"]
    },
    {
        "uid": "word_convenient",
        "section": "words",
        "mode": "words",
        "category": "Daily Use Words",
        "level": "BEGINNER",
        "telugu_text": "సౌకర్యవంతమైన / అనుకూలమైన",
        "telugu_transliteration": "Saukarryavanthamaina",
        "english_text": "Convenient",
        "valid_alternatives": ["suitable", "handy", "favorable", "easy"],
        "pronunciation": "/kənˈviː.ni.ənt/",
        "part_of_speech": "Adjective",
        "english_definition": "Fitting in well with someone's needs, time, or plans.",
        "when_to_use": "Use when choosing a suitable meeting time or location.",
        "examples": [
            {"english": "Is 4 PM convenient for a quick call?", "telugu": "సాయంత్రం 4 గంటలకు కాల్ చేయడానికి మీకు అనుకూలమేనా?"}
        ],
        "mistakes": [
            {"incorrect": "Are you convenient tomorrow?", "correct": "Is tomorrow convenient for you?", "reason": "'Convenient' describes the time or thing, not the person directly."}
        ],
        "synonyms": ["Suitable", "Handy", "Accessible"]
    },
    {
        "uid": "word_hesitate",
        "section": "words",
        "mode": "words",
        "category": "Daily Use Words",
        "level": "BEGINNER",
        "telugu_text": "సంకోచించడం / తటపటాయించడం",
        "telugu_transliteration": "Sankochinchadam",
        "english_text": "Hesitate",
        "valid_alternatives": ["hold back", "pause", "waver", "feel shy"],
        "pronunciation": "/ˈhez.ɪ.teɪt/",
        "part_of_speech": "Verb",
        "english_definition": "To pause before saying or doing something because you feel unsure.",
        "when_to_use": "Use when encouraging someone to ask questions freely.",
        "examples": [
            {"english": "Please do not hesitate to ask questions.", "telugu": "దయచేసి ప్రశ్నలు అడగడానికి సంకోచించకండి."}
        ],
        "mistakes": [
            {"incorrect": "Don't hesitate for ask.", "correct": "Don't hesitate to ask.", "reason": "Follow 'hesitate' with 'to + verb'."}
        ],
        "synonyms": ["Pause", "Hold back", "Waver"]
    },
    {
        "uid": "word_mention",
        "section": "words",
        "mode": "words",
        "category": "Verbs Used in Daily Life",
        "level": "BEGINNER",
        "telugu_text": "ప్రస్తావించడం / చెప్పడం",
        "telugu_transliteration": "Prasthaavinchadam",
        "english_text": "Mention",
        "valid_alternatives": ["bring up", "note", "state", "refer to"],
        "pronunciation": "/ˈmen.ʃən/",
        "part_of_speech": "Verb",
        "english_definition": "To briefly talk or write about someone or something.",
        "when_to_use": "Use when noting a detail in a conversation, resume, or email.",
        "examples": [
            {"english": "Did he mention what time he will arrive?", "telugu": "అతను ఎప్పుడు వస్తాడో చెప్పాడా?"}
        ],
        "mistakes": [
            {"incorrect": "He mentioned about the plan.", "correct": "He mentioned the plan.", "reason": "Do not put 'about' directly after 'mention'."}
        ],
        "synonyms": ["Bring up", "Note", "State"]
    },
    {
        "uid": "word_borrow",
        "section": "words",
        "mode": "words",
        "category": "Commonly Confused Words",
        "level": "BEGINNER",
        "telugu_text": "అప్పుగా తీసుకోవడం",
        "telugu_transliteration": "Appugaa teesukovadam",
        "english_text": "Borrow",
        "valid_alternatives": ["take on loan", "use temporarily"],
        "pronunciation": "/ˈbɒr.əʊ/",
        "part_of_speech": "Verb",
        "english_definition": "To take and use something belonging to someone else with the plan to return it.",
        "when_to_use": "Use when taking a pen, book, or money temporarily FROM someone.",
        "examples": [
            {"english": "May I borrow your pen for a minute?", "telugu": "నేను ఒక నిమిషం నీ పెన్ తీసుకోవచ్చా?"}
        ],
        "mistakes": [
            {"incorrect": "Can you borrow me your pen?", "correct": "Can you lend me your pen? / Can I borrow your pen?", "reason": "You borrow FROM someone; someone lends TO you."}
        ],
        "synonyms": ["Loan", "Take temporarily"]
    },
    {
        "uid": "word_lend",
        "section": "words",
        "mode": "words",
        "category": "Commonly Confused Words",
        "level": "BEGINNER",
        "telugu_text": "అప్పుగా ఇవ్వడం",
        "telugu_transliteration": "Appugaa ivvadam",
        "english_text": "Lend",
        "valid_alternatives": ["loan", "give temporarily"],
        "pronunciation": "/lend/",
        "part_of_speech": "Verb",
        "english_definition": "To give something to someone for a short time expecting them to return it.",
        "when_to_use": "Use when you give your item temporarily TO another person.",
        "examples": [
            {"english": "Could you lend me your charger?", "telugu": "నీ ఛార్జర్ కాసేపు ఇస్తావా?"}
        ],
        "mistakes": [
            {"incorrect": "Please borrow me 500 rupees.", "correct": "Please lend me 500 rupees.", "reason": "Say 'lend me' when asking someone to give temporarily."}
        ],
        "synonyms": ["Loan", "Provide temporarily"]
    },
    {
        "uid": "word_remind",
        "section": "words",
        "mode": "words",
        "category": "Commonly Confused Words",
        "level": "BEGINNER",
        "telugu_text": "గుర్తు చేయడం",
        "telugu_transliteration": "Gurthu cheyadam",
        "english_text": "Remind",
        "valid_alternatives": ["jog someone's memory", "prompt"],
        "pronunciation": "/rɪˈmaɪnd/",
        "part_of_speech": "Verb",
        "english_definition": "To help someone remember something they might forget.",
        "when_to_use": "Use when asking another person or an alarm to make you remember a task.",
        "examples": [
            {"english": "Please remind me to send that email before 5 PM.", "telugu": "సాయంత్రం 5 గంటలలోపు ఆ ఈమెయిల్ పంపమని నాకు గుర్తు చేయండి."}
        ],
        "mistakes": [
            {"incorrect": "Remind me the meeting.", "correct": "Remind me about the meeting.", "reason": "Always use 'remind [person] about [thing]' or 'to [verb]'."}
        ],
        "synonyms": ["Prompt", "Alert"]
    },
    {
        "uid": "word_remember",
        "section": "words",
        "mode": "words",
        "category": "Verbs Used in Daily Life",
        "level": "BEGINNER",
        "telugu_text": "గుర్తుంచుకోవడం / జ్ఞాపకం ఉండటం",
        "telugu_transliteration": "Gurthunchukovadam",
        "english_text": "Remember",
        "valid_alternatives": ["recall", "keep in mind"],
        "pronunciation": "/rɪˈmem.bər/",
        "part_of_speech": "Verb",
        "english_definition": "To have an image or fact in your mind from the past.",
        "when_to_use": "Use when recalling facts, names, or past events yourself.",
        "examples": [
            {"english": "I remember meeting you at the workshop last year.", "telugu": "గత ఏడాది వర్క్‌షాప్‌లో నిన్ను కలిసినట్లు నాకు గుర్తుంది."}
        ],
        "synonyms": ["Recall", "Keep in mind"]
    },
    {
        "uid": "word_afford",
        "section": "words",
        "mode": "words",
        "category": "Shopping Vocabulary",
        "level": "INTERMEDIATE",
        "telugu_text": "ఖర్చు భరించగలగడం / కొనగలిగే స్థోమత",
        "telugu_transliteration": "Bharinchagalagadam",
        "english_text": "Afford",
        "valid_alternatives": ["pay for", "spare money for", "manage the cost"],
        "pronunciation": "/əˈfɔːd/",
        "part_of_speech": "Verb",
        "english_definition": "To have enough money or time to buy or do something.",
        "when_to_use": "Commonly used after 'can' or 'can't' when discussing prices or budgets.",
        "examples": [
            {"english": "I can't afford such an expensive phone right now.", "telugu": "ప్రస్తుతం అంత ఖరీదైన ఫోన్ కొనే స్థోమత నాకు లేదు."}
        ],
        "synonyms": ["Bear the cost", "Manage"]
    },
    {
        "uid": "word_bargain",
        "section": "words",
        "mode": "words",
        "category": "Shopping Vocabulary",
        "level": "BEGINNER",
        "telugu_text": "బేరం ఆడటం / తక్కువ ధర డీల్",
        "telugu_transliteration": "Beram aadadam",
        "english_text": "Bargain",
        "valid_alternatives": ["negotiate", "haggle", "good deal"],
        "pronunciation": "/ˈbɑː.ɡɪn/",
        "part_of_speech": "Verb / Noun",
        "english_definition": "To discuss prices to agree on a lower amount, or something bought cheaply.",
        "when_to_use": "Use in local markets or while discussing discounts.",
        "examples": [
            {"english": "My mother knows how to bargain well in local markets.", "telugu": "మా అమ్మకు లోకల్ మార్కెట్లలో బాగా బేరం ఆడటం వచ్చు."}
        ],
        "synonyms": ["Negotiate", "Good deal"]
    },
    {
        "uid": "word_utensils",
        "section": "words",
        "mode": "words",
        "category": "Home and Household Words",
        "level": "BEGINNER",
        "telugu_text": "వంట పాత్రలు",
        "telugu_transliteration": "Vanta paathralu",
        "english_text": "Utensils",
        "valid_alternatives": ["kitchenware", "cookware", "dishes", "pots and pans"],
        "pronunciation": "/juːˈten.sɪlz/",
        "part_of_speech": "Noun",
        "english_definition": "Tools and containers used in the kitchen for cooking or eating.",
        "when_to_use": "Use when talking about washing dishes or buying kitchen tools.",
        "examples": [
            {"english": "Please wash the kitchen utensils after dinner.", "telugu": "దయచేసి డిన్నర్ తర్వాత వంట పాత్రలు కడగండి."}
        ],
        "synonyms": ["Kitchenware", "Cookware"]
    },
    {
        "uid": "word_clutter",
        "section": "words",
        "mode": "words",
        "category": "Home and Household Words",
        "level": "INTERMEDIATE",
        "telugu_text": "చెల్లాచెదురుగా ఉన్న వస్తువులు / అస్తవ్యస్తం",
        "telugu_transliteration": "Asthavyastham",
        "english_text": "Clutter",
        "valid_alternatives": ["mess", "disorder", "untidiness", "jumble"],
        "pronunciation": "/ˈklʌt.ər/",
        "part_of_speech": "Noun",
        "english_definition": "Many things lying around in an untidy way.",
        "when_to_use": "Use when cleaning rooms or organizing your workspace.",
        "examples": [
            {"english": "Let's clear the clutter on the study table.", "telugu": "స్టడీ టేబుల్ మీద చెల్లాచెదురుగా ఉన్న వస్తువులను సర్దుదాం."}
        ],
        "synonyms": ["Mess", "Disorder"]
    },
    {
        "uid": "word_delicious",
        "section": "words",
        "mode": "words",
        "category": "Food and Cooking Words",
        "level": "BEGINNER",
        "telugu_text": "రుచికరమైన",
        "telugu_transliteration": "Ruchikaramaina",
        "english_text": "Delicious",
        "valid_alternatives": ["tasty", "yummy", "mouthwatering", "flavorful"],
        "pronunciation": "/dɪˈlɪʃ.əs/",
        "part_of_speech": "Adjective",
        "english_definition": "Having a very pleasant taste or smell.",
        "when_to_use": "Compliment home-cooked food or restaurant meals politely.",
        "examples": [
            {"english": "The homemade biryani was absolutely delicious!", "telugu": "ఇంట్లో చేసిన బిర్యానీ చాలా రుచికరంగా ఉంది!"}
        ],
        "synonyms": ["Tasty", "Flavorful"]
    },
    {
        "uid": "word_spoil",
        "section": "words",
        "mode": "words",
        "category": "Food and Cooking Words",
        "level": "BEGINNER",
        "telugu_text": "పాడైపోవడం / చెడిపోవడం",
        "telugu_transliteration": "Paadaipovadam",
        "english_text": "Spoil",
        "valid_alternatives": ["go bad", "rot", "ruin", "get spoiled"],
        "pronunciation": "/spɔɪl/",
        "part_of_speech": "Verb",
        "english_definition": "To become no longer fresh or good enough to eat or use.",
        "when_to_use": "Use when talking about food kept outside the fridge or ruined plans.",
        "examples": [
            {"english": "Keep the milk in the fridge so it doesn't spoil.", "telugu": "పాలు పాడైపోకుండా ఫ్రిజ్‌లో పెట్టండి."}
        ],
        "synonyms": ["Go bad", "Ruin"]
    },
    {
        "uid": "word_depart",
        "section": "words",
        "mode": "words",
        "category": "Travel Vocabulary",
        "level": "BEGINNER",
        "telugu_text": "బయలుదేరడం",
        "telugu_transliteration": "Bayaluderadam",
        "english_text": "Depart",
        "valid_alternatives": ["leave", "start the journey", "set off", "head out"],
        "pronunciation": "/dɪˈpɑːt/",
        "part_of_speech": "Verb",
        "english_definition": "To leave a place to begin a journey, especially for trains or flights.",
        "when_to_use": "Commonly seen at airports, train stations, and bus stops.",
        "examples": [
            {"english": "Our train will depart from platform three at 6 PM.", "telugu": "మన రైలు సాయంత్రం 6 గంటలకు ప్లాట్‌ఫాం 3 నుండి బయలుదేరుతుంది."}
        ],
        "synonyms": ["Leave", "Set off"]
    },
    {
        "uid": "word_luggage",
        "section": "words",
        "mode": "words",
        "category": "Travel Vocabulary",
        "level": "BEGINNER",
        "telugu_text": "ప్రయాణ సామాను",
        "telugu_transliteration": "Prayana saamaanu",
        "english_text": "Luggage",
        "valid_alternatives": ["baggage", "bags", "suitcases"],
        "pronunciation": "/ˈlʌɡ.ɪdʒ/",
        "part_of_speech": "Noun (Uncountable)",
        "english_definition": "Suitcases and bags used to carry belongings when travelling.",
        "when_to_use": "Note: Never say 'luggages' — 'luggage' is always uncountable.",
        "examples": [
            {"english": "Please keep your luggage in the overhead bin.", "telugu": "దయచేసి మీ సామానును పై రాక్‌లో పెట్టండి."}
        ],
        "mistakes": [
            {"incorrect": "I have heavy luggages.", "correct": "I have heavy luggage.", "reason": "'Luggage' is uncountable; never add 's'."}
        ],
        "synonyms": ["Baggage", "Suitcases"]
    },
    {
        "uid": "word_affection",
        "section": "words",
        "mode": "words",
        "category": "Family and Relationships",
        "level": "INTERMEDIATE",
        "telugu_text": "ఆప్యాయత / ప్రేమ",
        "telugu_transliteration": "Aapyaayatha",
        "english_text": "Affection",
        "valid_alternatives": ["fondness", "warmth", "care", "love"],
        "pronunciation": "/əˈfek.ʃən/",
        "part_of_speech": "Noun",
        "english_definition": "A gentle feeling of fondness, caring, or love toward family or friends.",
        "when_to_use": "Use to describe warm family bonds and kindness.",
        "examples": [
            {"english": "Grandparents always show deep affection for their grandchildren.", "telugu": "తాతయ్య అమ్మమ్మలు మనవలపై ఎప్పుడూ ఎంతో ఆప్యాయత చూపిస్తారు."}
        ],
        "synonyms": ["Fondness", "Care", "Warmth"]
    },
    {
        "uid": "word_encourage",
        "section": "words",
        "mode": "words",
        "category": "Family and Relationships",
        "level": "BEGINNER",
        "telugu_text": "ప్రోత్సహించడం",
        "telugu_transliteration": "Prothsahinchadam",
        "english_text": "Encourage",
        "valid_alternatives": ["motivate", "support", "inspire", "boost"],
        "pronunciation": "/ɪnˈkʌr.ɪdʒ/",
        "part_of_speech": "Verb",
        "english_definition": "To give someone confidence, support, or hope to do something.",
        "when_to_use": "Use when supporting friends, team members, or children.",
        "examples": [
            {"english": "My mentor encouraged me to apply for the senior role.", "telugu": "నా మెంటర్ నన్ను సీనియర్ రోల్‌కి అప్లై చేయమని ప్రోత్సహించారు."}
        ],
        "synonyms": ["Motivate", "Support"]
    },
    {
        "uid": "word_anxious",
        "section": "words",
        "mode": "words",
        "category": "Feelings and Emotions",
        "level": "INTERMEDIATE",
        "telugu_text": "ఆందోళనగా / కంగారుగా ఉన్న",
        "telugu_transliteration": "Aandolanagaa unna",
        "english_text": "Anxious",
        "valid_alternatives": ["nervous", "worried", "tense", "uneasy"],
        "pronunciation": "/ˈæŋk.ʃəs/",
        "part_of_speech": "Adjective",
        "english_definition": "Feeling worried or nervous about something uncertain.",
        "when_to_use": "Express nervousness before an interview, exam, or test results.",
        "examples": [
            {"english": "I felt a bit anxious before my first job interview.", "telugu": "నా మొదటి జాబ్ ఇంటర్వ్యూకి ముందు నాకు కొంచెం ఆందోళనగా అనిపించింది."}
        ],
        "synonyms": ["Worried", "Nervous", "Uneasy"]
    },
    {
        "uid": "word_relieved",
        "section": "words",
        "mode": "words",
        "category": "Feelings and Emotions",
        "level": "INTERMEDIATE",
        "telugu_text": "ఊపిరి పీల్చుకున్న / ఉపశమనం పొందిన",
        "telugu_transliteration": "Upashamanam pondina",
        "english_text": "Relieved",
        "valid_alternatives": ["comforted", "relaxed", "reassured", "at ease"],
        "pronunciation": "/rɪˈliːvd/",
        "part_of_speech": "Adjective",
        "english_definition": "Happy and relaxed because a worry or problem has ended.",
        "when_to_use": "Use right after a tough exam ends or good news arrives.",
        "examples": [
            {"english": "I felt so relieved after finishing my presentation.", "telugu": "నా ప్రెజెంటేషన్ ముగిశాక నాకు చాలా ఊరటగా అనిపించింది."}
        ],
        "synonyms": ["Relaxed", "Reassured"]
    },
    {
        "uid": "word_collaborate",
        "section": "words",
        "mode": "words",
        "category": "Workplace Vocabulary",
        "level": "INTERMEDIATE",
        "telugu_text": "కలిసి పనిచేయడం / సహకరించుకోవడం",
        "telugu_transliteration": "Kalisi panicheyadam",
        "english_text": "Collaborate",
        "valid_alternatives": ["work together", "team up", "cooperate", "partner"],
        "pronunciation": "/kəˈlæb.ə.reɪt/",
        "part_of_speech": "Verb",
        "english_definition": "To work together with other people on a shared task or project.",
        "when_to_use": "Use in office emails, team meetings, and interviews.",
        "examples": [
            {"english": "Our frontend and backend teams collaborate closely.", "telugu": "మా ఫ్రంట్‌ఎండ్ మరియు బ్యాక్‌ఎండ్ టీమ్స్ కలిసి పనిచేస్తాయి."}
        ],
        "synonyms": ["Work together", "Team up", "Cooperate"]
    },
    {
        "uid": "word_deadline",
        "section": "words",
        "mode": "words",
        "category": "Office Vocabulary",
        "level": "BEGINNER",
        "telugu_text": "గడువు తేదీ / చివరి సమయం",
        "telugu_transliteration": "Gaduvu thedi",
        "english_text": "Deadline",
        "valid_alternatives": ["due date", "time limit", "cutoff time"],
        "pronunciation": "/ˈded.laɪn/",
        "part_of_speech": "Noun",
        "english_definition": "The latest time or date by which a task must be finished.",
        "when_to_use": "Use in workplace updates, schedules, and assignments.",
        "examples": [
            {"english": "We must submit the report before Friday's deadline.", "telugu": "మనం శుక్రవారం గడువులోపు రిపోర్ట్ సమర్పించాలి."}
        ],
        "synonyms": ["Due date", "Time limit"]
    },
    {
        "uid": "word_reschedule",
        "section": "words",
        "mode": "words",
        "category": "Office Vocabulary",
        "level": "BEGINNER",
        "telugu_text": "సమయం మార్చడం / మళ్ళీ ప్లాన్ చేయడం",
        "telugu_transliteration": "Samayam maarchadam",
        "english_text": "Reschedule",
        "valid_alternatives": ["move the meeting", "postpone", "change the time"],
        "pronunciation": "/ˌriːˈʃedʒ.uːl/",
        "part_of_speech": "Verb",
        "english_definition": "To change the date or time of a planned event.",
        "when_to_use": "Polite workplace word when you cannot attend an existing meeting slot.",
        "examples": [
            {"english": "Could we reschedule our call to tomorrow afternoon?", "telugu": "మనం కాల్‌ను రేపు మధ్యాహ్నానికి మార్చుకోవచ్చా?"}
        ],
        "synonyms": ["Postpone", "Move", "Rearrange"]
    },
    {
        "uid": "word_accomplish",
        "section": "words",
        "mode": "words",
        "category": "Interview Vocabulary",
        "level": "ADVANCED",
        "telugu_text": "సాధించడం / విజయవంతంగా పూర్తి చేయడం",
        "telugu_transliteration": "Saadhinchadam",
        "english_text": "Accomplish",
        "valid_alternatives": ["achieve", "complete", "attain", "fulfill"],
        "pronunciation": "/əˈkʌm.plɪʃ/",
        "part_of_speech": "Verb",
        "english_definition": "To succeed in finishing or achieving something difficult.",
        "when_to_use": "Great strong verb for job interviews and resumes.",
        "examples": [
            {"english": "We accomplished all quarterly targets ahead of time.", "telugu": "మనం క్వార్టర్లీ టార్గెట్స్ అన్నింటినీ ముందే సాధించాము."}
        ],
        "synonyms": ["Achieve", "Attain", "Fulfill"]
    },
    {
        "uid": "word_proficient",
        "section": "words",
        "mode": "words",
        "category": "Interview Vocabulary",
        "level": "ADVANCED",
        "telugu_text": "నైపుణ్యం కలిగిన / సమర్థుడైన",
        "telugu_transliteration": "Naipunyam kaligina",
        "english_text": "Proficient",
        "valid_alternatives": ["skilled", "expert", "fluent", "experienced"],
        "pronunciation": "/prəˈfɪʃ.ənt/",
        "part_of_speech": "Adjective",
        "english_definition": "Very skilled and capable at doing a particular job or activity.",
        "when_to_use": "Use on resumes and interviews instead of repeatedly saying 'I know'.",
        "examples": [
            {"english": "I am proficient in Python, SQL, and REST API design.", "telugu": "నాకు పైథాన్, SQL మరియు REST API లో మంచి నైపుణ్యం ఉంది."}
        ],
        "synonyms": ["Skilled", "Competent", "Expert"]
    },
    {
        "uid": "word_troubleshoot",
        "section": "words",
        "mode": "words",
        "category": "Technology Vocabulary",
        "level": "INTERMEDIATE",
        "telugu_text": "సాంకేతిక సమస్యను గుర్తించి పరిష్కరించడం",
        "telugu_transliteration": "Samasyanu parishkarinchadam",
        "english_text": "Troubleshoot",
        "valid_alternatives": ["debug", "fix the issue", "diagnose", "resolve"],
        "pronunciation": "/ˈtrʌb.əl.ʃuːt/",
        "part_of_speech": "Verb",
        "english_definition": "To trace and solve problems in a computer, software, or system.",
        "when_to_use": "Essential word for IT support and engineering teams.",
        "examples": [
            {"english": "Can you help me troubleshoot this login timeout error?", "telugu": "ఈ లాగిన్ టైమౌట్ ఎర్రర్‌ను సరిచేయడానికి సహాయం చేయగలరా?"}
        ],
        "synonyms": ["Debug", "Diagnose", "Resolve"]
    },
    {
        "uid": "word_deploy",
        "section": "words",
        "mode": "words",
        "category": "Technology Vocabulary",
        "level": "INTERMEDIATE",
        "telugu_text": "సాఫ్ట్‌వేర్‌ను లైవ్ లోకి విడుదల చేయడం",
        "telugu_transliteration": "Live loki vidudala cheyadam",
        "english_text": "Deploy",
        "valid_alternatives": ["release", "launch", "publish", "push live"],
        "pronunciation": "/dɪˈplɔɪ/",
        "part_of_speech": "Verb",
        "english_definition": "To release software or a website onto live servers for users.",
        "when_to_use": "Daily software development vocabulary.",
        "examples": [
            {"english": "We will deploy the updated build after testing passes.", "telugu": "టెస్టింగ్ పూర్తయ్యాక మనం కొత్త బిల్డ్‌ను డిప్లాయ్ చేస్తాము."}
        ],
        "synonyms": ["Release", "Launch", "Publish"]
    },
    {
        "uid": "word_consistent",
        "section": "words",
        "mode": "words",
        "category": "Adjectives Used in Conversations",
        "level": "INTERMEDIATE",
        "telugu_text": "స్థిరంగా / క్రమం తప్పకుండా చేసే",
        "telugu_transliteration": "Sthiranga chese",
        "english_text": "Consistent",
        "valid_alternatives": ["regular", "steady", "reliable", "constant"],
        "pronunciation": "/kənˈsɪs.tənt/",
        "part_of_speech": "Adjective",
        "english_definition": "Happening in the same steady way or showing steady effort.",
        "when_to_use": "Describe study habits, daily practice, or reliable work.",
        "examples": [
            {"english": "Being consistent with daily practice improves fluency fast.", "telugu": "రోజూ స్థిరంగా ప్రాక్టీస్ చేయడం వల్ల ఇంగ్లీష్ త్వరగా వస్తుంది."}
        ],
        "synonyms": ["Steady", "Regular", "Reliable"]
    },
    {
        "uid": "word_polite",
        "section": "words",
        "mode": "words",
        "category": "Adjectives Used in Conversations",
        "level": "BEGINNER",
        "telugu_text": "మర్యాదగల / వినయపూర్వకమైన",
        "telugu_transliteration": "Maryadagala",
        "english_text": "Polite",
        "valid_alternatives": ["courteous", "respectful", "kind", "well-mannered"],
        "pronunciation": "/pəˈlaɪt/",
        "part_of_speech": "Adjective",
        "english_definition": "Having good manners and showing respect for other people.",
        "when_to_use": "Describe respectful tone and behavior.",
        "examples": [
            {"english": "The hotel staff was extremely polite and helpful.", "telugu": "హోటల్ సిబ్బంది చాలా మర్యాదగా మరియు సహాయకారిగా ఉన్నారు."}
        ],
        "synonyms": ["Courteous", "Respectful"]
    },
    {
        "uid": "word_negotiate",
        "section": "words",
        "mode": "words",
        "category": "Advanced Vocabulary",
        "level": "ADVANCED",
        "telugu_text": "చర్చించి ఒక ఒప్పందానికి రావడం",
        "telugu_transliteration": "Charchinchi oppandaniki raavadam",
        "english_text": "Negotiate",
        "valid_alternatives": ["bargain", "discuss terms", "compromise"],
        "pronunciation": "/nɪˈɡəʊ.ʃi.eɪt/",
        "part_of_speech": "Verb",
        "english_definition": "To have formal discussions to reach an agreement on salary, terms, or prices.",
        "when_to_use": "Use when discussing job offers, contracts, or pricing.",
        "examples": [
            {"english": "She negotiated a higher salary offer politely.", "telugu": "ఆమె మర్యాదగా మాట్లాడి మంచి జీతం కోసం ఒప్పించింది."}
        ],
        "synonyms": ["Bargain", "Discuss terms"]
    },
    {
        "uid": "word_prioritize",
        "section": "words",
        "mode": "words",
        "category": "Workplace Vocabulary",
        "level": "INTERMEDIATE",
        "telugu_text": "ప్రాధాన్యత ఇవ్వడం",
        "telugu_transliteration": "Praadhaanyatha ivvadam",
        "english_text": "Prioritize",
        "valid_alternatives": ["put first", "focus on first", "rank by importance"],
        "pronunciation": "/praɪˈɒr.ɪ.taɪz/",
        "part_of_speech": "Verb",
        "english_definition": "To decide which tasks are most urgent and do them first.",
        "when_to_use": "Explain time management at work or in interviews.",
        "examples": [
            {"english": "Let's prioritize the client issue before adding new features.", "telugu": "కొత్త ఫీచర్ల కంటే ముందు క్లయింట్ సమస్యకు ప్రాధాన్యత ఇద్దాం."}
        ],
        "synonyms": ["Put first", "Focus on first"]
    },
    {
        "uid": "word_clarify",
        "section": "words",
        "mode": "words",
        "category": "Verbs Used in Daily Life",
        "level": "INTERMEDIATE",
        "telugu_text": "స్పష్టం చేయడం / సందేహం నివృత్తి చేయడం",
        "telugu_transliteration": "Spashtam cheyadam",
        "english_text": "Clarify",
        "valid_alternatives": ["explain clearly", "clear up", "make clear", "confirm"],
        "pronunciation": "/ˈklær.ɪ.faɪ/",
        "part_of_speech": "Verb",
        "english_definition": "To make a point or instruction clear and easy to understand.",
        "when_to_use": "Use when politely double-checking requirements.",
        "examples": [
            {"english": "Could you please clarify this requirement once more?", "telugu": "దయచేసి ఈ అవసరాన్ని మరోసారి స్పష్టం చేయగలరా?"}
        ],
        "synonyms": ["Explain clearly", "Clear up"]
    },
    {
        "uid": "word_urgent",
        "section": "words",
        "mode": "words",
        "category": "Daily Use Words",
        "level": "BEGINNER",
        "telugu_text": "అత్యవసరమైన",
        "telugu_transliteration": "Athyavasaramaina",
        "english_text": "Urgent",
        "valid_alternatives": ["emergency", "critical", "high priority", "pressing", "immediate"],
        "pronunciation": "/ˈɜː.dʒənt/",
        "part_of_speech": "Adjective",
        "english_definition": "Very important and needing immediate attention.",
        "when_to_use": "Use when something cannot wait until later.",
        "examples": [
            {"english": "I have some urgent work at the bank today.", "telugu": "ఈరోజు బ్యాంక్‌లో నాకు ఒక అత్యవసరమైన పని ఉంది."}
        ],
        "synonyms": ["Critical", "Immediate", "Pressing"]
    },
    {
        "uid": "word_grateful",
        "section": "words",
        "mode": "words",
        "category": "Feelings and Emotions",
        "level": "BEGINNER",
        "telugu_text": "కృతజ్ఞతగా ఉన్న",
        "telugu_transliteration": "Krutajnyathagaa unna",
        "english_text": "Grateful",
        "valid_alternatives": ["thankful", "appreciative", "indebted"],
        "pronunciation": "/ˈɡreɪt.fəl/",
        "part_of_speech": "Adjective",
        "english_definition": "Showing or feeling thanks for someone's kindness or help.",
        "when_to_use": "Use in heartfelt thank-you notes or conversations.",
        "examples": [
            {"english": "I am really grateful for your guidance and support.", "telugu": "మీ మార్గదర్శకత్వం మరియు సహాయానికి నేను నిజంగా కృతజ్ఞుడిని."}
        ],
        "synonyms": ["Thankful", "Appreciative"]
    },
    {
        "uid": "word_apologize",
        "section": "words",
 "mode": "words",
        "category": "Verbs Used in Daily Life",
        "level": "BEGINNER",
        "telugu_text": "క్షమాపణ చెప్పడం",
        "telugu_transliteration": "Kshamaapana cheppadam",
        "english_text": "Apologize",
        "valid_alternatives": ["say sorry", "be sorry", "regret"],
        "pronunciation": "/əˈpɒl.ə.dʒaɪz/",
        "part_of_speech": "Verb",
        "english_definition": "To say you are sorry for a mistake or causing trouble.",
        "when_to_use": "Polite workplace or formal alternative to 'say sorry'.",
        "examples": [
            {"english": "I sincerely apologize for the delay in replying.", "telugu": "జవాబు ఇవ్వడంలో ఆలస్యమైనందుకు నేను హృదయపూర్వకంగా క్షమాపణ కోరుతున్నాను."}
        ],
        "synonyms": ["Say sorry", "Express regret"]
    },
    {
        "uid": "word_confident",
        "section": "words",
        "mode": "words",
        "category": "Adjectives Used in Conversations",
        "level": "BEGINNER",
        "telugu_text": "ఆత్మవిశ్వాసంతో ఉన్న",
        "telugu_transliteration": "Aathmavishwasamtho unna",
        "english_text": "Confident",
        "valid_alternatives": ["self-assured", "sure", "certain", "bold"],
        "pronunciation": "/ˈkɒn.fɪ.dənt/",
        "part_of_speech": "Adjective",
        "english_definition": "Feeling sure about your own abilities and qualities.",
        "when_to_use": "Describe speaking clearly without fear.",
        "examples": [
            {"english": "Daily speaking practice makes you feel much more confident.", "telugu": "రోజూ మాట్లాడటం సాధన చేస్తే మీకు ఆత్మవిశ్వాసం పెరుగుతుంది."}
        ],
        "synonyms": ["Self-assured", "Certain"]
    },
    {
        "uid": "word_overwhelmed",
        "section": "words",
        "mode": "words",
        "category": "Feelings and Emotions",
        "level": "ADVANCED",
        "telugu_text": "పని భారంతో లేదా భావోద్వేగంతో ఉక్కిరిబిక్కిరి అవ్వడం",
        "telugu_transliteration": "Ukkiribikkiri avvadam",
        "english_text": "Overwhelmed",
        "valid_alternatives": ["stressed out", "overloaded", "swamped", "flooded"],
        "pronunciation": "/ˌəʊ.vəˈwelmd/",
        "part_of_speech": "Adjective",
        "english_definition": "Feeling like there is too much work, stress, or emotion to handle at once.",
        "when_to_use": "Express heavy workload politely to teammates or friends.",
        "examples": [
            {"english": "I felt overwhelmed with three deadlines on the same day.", "telugu": "ఒకే రోజు మూడు డెడ్‌లైన్స్ ఉండటంతో నేను చాలా ఒత్తిడిగా ఫీల్ అయ్యాను."}
        ],
        "synonyms": ["Swamped", "Overloaded", "Stressed"]
    },
    {
        "uid": "word_reliable",
        "section": "words",
        "mode": "words",
        "category": "Adjectives Used in Conversations",
        "level": "INTERMEDIATE",
        "telugu_text": "నమ్మదగిన / విశ్వసనీయమైన",
        "telugu_transliteration": "Nammadagina",
        "english_text": "Reliable",
        "valid_alternatives": ["dependable", "trustworthy", "consistent", "steady"],
        "pronunciation": "/rɪˈlaɪ.ə.bəl/",
        "part_of_speech": "Adjective",
        "english_definition": "Able to be trusted to work well or behave properly.",
        "when_to_use": "Describe teammates, internet connections, or services.",
        "examples": [
            {"english": "Ravi is a very reliable developer on our team.", "telugu": "రవి మా టీమ్‌లో చాలా నమ్మదగిన డెవలపర్."}
        ],
        "synonyms": ["Dependable", "Trustworthy"]
    },
    {
        "uid": "word_receipt",
        "section": "words",
        "mode": "words",
        "category": "Shopping Vocabulary",
        "level": "BEGINNER",
        "telugu_text": "రసీదు / కొనుగోలు బిల్లు",
        "telugu_transliteration": "Raseedu",
        "english_text": "Receipt",
        "valid_alternatives": ["bill", "invoice", "proof of purchase"],
        "pronunciation": "/rɪˈsiːt/",
        "part_of_speech": "Noun",
        "english_definition": "A paper or digital record proving you paid for something.",
        "when_to_use": "Note silent 'p' in pronunciation! Always ask for it at counters.",
        "examples": [
            {"english": "Could you please give me the receipt for this item?", "telugu": "దయచేసి ఈ వస్తువుకు రసీదు ఇస్తారా?"}
        ],
        "synonyms": ["Bill", "Invoice"]
    },
    {
        "uid": "word_commute",
        "section": "words",
        "mode": "words",
        "category": "Travel Vocabulary",
        "level": "INTERMEDIATE",
        "telugu_text": "రోజూ ఆఫీసు లేదా కాలేజీకి రాకపోకలు సాగించడం",
        "telugu_transliteration": "Raakapokalu saaginchadam",
        "english_text": "Commute",
        "valid_alternatives": ["daily travel", "travel to work", "ride to office"],
        "pronunciation": "/kəˈmjuːt/",
        "part_of_speech": "Verb / Noun",
        "english_definition": "Regular daily travel between home and workplace or college.",
        "when_to_use": "Use instead of saying 'up and down daily'.",
        "examples": [
            {"english": "My daily commute to the office takes forty minutes.", "telugu": "ఆఫీసుకు నా రోజువారీ ప్రయాణానికి నలభై నిమిషాలు పడుతుంది."}
        ],
        "mistakes": [
            {"incorrect": "I do daily up and down to office.", "correct": "I commute to the office daily.", "reason": "'Up and down' is an Indian English translation; native speakers say 'commute'."}
        ],
        "synonyms": ["Travel regularly", "Daily trip"]
    },
    {
        "uid": "word_implement",
        "section": "words",
        "mode": "words",
        "category": "Technology Vocabulary",
        "level": "INTERMEDIATE",
        "telugu_text": "అమలు చేయడం / కోడ్ లోకి మార్చడం",
        "telugu_transliteration": "Amalu cheyadam",
        "english_text": "Implement",
        "valid_alternatives": ["put into action", "build", "carry out", "execute"],
        "pronunciation": "/ˈɪm.plɪ.ment/",
        "part_of_speech": "Verb",
        "english_definition": "To put a plan, rule, or software feature into working action.",
        "when_to_use": "Very common in workplace and engineering updates.",
        "examples": [
            {"english": "We need to implement search filters on this page.", "telugu": "ఈ పేజీలో మనం సెర్చ్ ఫిల్టర్స్‌ను అమలు చేయాలి."}
        ],
        "synonyms": ["Execute", "Apply", "Carry out"]
    },
    {
        "uid": "word_empathy",
        "section": "words",
        "mode": "words",
        "category": "Advanced Vocabulary",
        "level": "ADVANCED",
        "telugu_text": "ఇతరుల బాధను లేదా పరిస్థితిని మనదిగా అర్థం చేసుకోవడం",
        "telugu_transliteration": "Saahanubhoothi",
        "english_text": "Empathy",
        "valid_alternatives": ["understanding", "compassion", "sensitivity"],
        "pronunciation": "/ˈem.pə.θi/",
        "part_of_speech": "Noun",
        "english_definition": "The ability to understand and share someone else's feelings.",
        "when_to_use": "Leadership and HR interview quality.",
        "examples": [
            {"english": "Good customer support starts with genuine empathy.", "telugu": "మంచి కస్టమర్ సపోర్ట్ అనేది అవతలి వారి పరిస్థితిని అర్థం చేసుకోవడంతో మొదలవుతుంది."}
        ],
        "synonyms": ["Compassion", "Understanding"]
    },
    {
        "uid": "word_chore",
        "section": "words",
        "mode": "words",
        "category": "Home and Household Words",
        "level": "INTERMEDIATE",
        "telugu_text": "ఇంటి రోజువారీ చిన్న పనులు",
        "telugu_transliteration": "Inti panulu",
        "english_text": "Chore",
        "valid_alternatives": ["household task", "errand", "housework", "daily duty"],
        "pronunciation": "/tʃɔːr/",
        "part_of_speech": "Noun",
        "english_definition": "A routine everyday task, especially around the house.",
        "when_to_use": "Describe cleaning, sweeping, washing clothes, or buying groceries.",
        "examples": [
            {"english": "I finish all my household chores on Sunday morning.", "telugu": "నేను ఆదివారం ఉదయమే ఇంటి పనులన్నీ పూర్తి చేస్తాను."}
        ],
        "synonyms": ["Housework", "Household task"]
    },
    {
        "uid": "word_appreciate",
        "section": "words",
        "mode": "words",
        "category": "Workplace Vocabulary",
        "level": "INTERMEDIATE",
        "telugu_text": "అభినందించడం / కృతజ్ఞత చూపడం",
        "telugu_transliteration": "Abhinandinchadam",
        "english_text": "Appreciate",
        "valid_alternatives": ["value", "thank for", "be grateful for", "admire"],
        "pronunciation": "/əˈpriː.ʃi.eɪt/",
        "part_of_speech": "Verb",
        "english_definition": "To recognize the value of someone's help or effort and feel thankful.",
        "when_to_use": "Polite workplace thank-you phrase.",
        "examples": [
            {"english": "I truly appreciate your help with the client presentation.", "telugu": "క్లయింట్ ప్రెజెంటేషన్‌లో మీ సహాయాన్ని నేను నిజంగా అభినందిస్తున్నాను."}
        ],
        "synonyms": ["Value", "Admire", "Thank"]
    },
    {
        "uid": "word_punctual",
        "section": "words",
        "mode": "words",
        "category": "Adjectives Used in Conversations",
        "level": "BEGINNER",
        "telugu_text": "సమయపాలన గల / సమయానికి వచ్చే",
        "telugu_transliteration": "Samayapaalana gala",
        "english_text": "Punctual",
        "valid_alternatives": ["on time", "prompt", "timely"],
        "pronunciation": "/ˈpʌŋk.tʃu.əl/",
        "part_of_speech": "Adjective",
        "english_definition": "Always arriving or doing things at the expected time.",
        "when_to_use": "Useful for interviews and describing disciplined habits.",
        "examples": [{"english": "She is always punctual for morning meetings.", "telugu": "ఆమె ఉదయం మీటింగ్‌లకు ఎప్పుడూ సమయానికి వస్తుంది."}],
        "synonyms": ["On time", "Prompt"]
    },
    {
        "uid": "word_exhausted",
        "section": "words",
        "mode": "words",
        "category": "Feelings and Emotions",
        "level": "INTERMEDIATE",
        "telugu_text": "తీవ్రంగా అలసిపోయిన",
        "telugu_transliteration": "Thivranga alasipoyina",
        "english_text": "Exhausted",
        "valid_alternatives": ["very tired", "drained", "worn out", "fatigued"],
        "pronunciation": "/ɪɡˈzɔː.stɪd/",
        "part_of_speech": "Adjective",
        "english_definition": "Extremely tired and lacking energy.",
        "when_to_use": "Stronger natural alternative to 'very tired'.",
        "examples": [{"english": "After the twelve-hour journey, I felt completely exhausted.", "telugu": "పన్నెండు గంటల ప్రయాణం తర్వాత నేను పూర్తిగా అలసిపోయాను."}],
        "synonyms": ["Worn out", "Drained"]
    },
    {
        "uid": "word_recipe",
        "section": "words",
        "mode": "words",
        "category": "Food and Cooking Words",
        "level": "BEGINNER",
        "telugu_text": "వంట తయారీ విధానం",
        "telugu_transliteration": "Vanta vidhaanam",
        "english_text": "Recipe",
        "valid_alternatives": ["cooking instructions", "ingredients and steps", "formula"],
        "pronunciation": "/ˈres.ɪ.pi/",
        "part_of_speech": "Noun",
        "english_definition": "A set of instructions for preparing a dish.",
        "when_to_use": "Note ending sound '-pee'! Common word when sharing cooking tips.",
        "examples": [{"english": "Can you share your grandmother's dosa batter recipe?", "telugu": "నీ అమ్మమ్మ చేసిన దోసె పిండి రెసిపీ చెబుతావా?"}],
        "synonyms": ["Cooking method", "Formula"]
    },
    {
        "uid": "word_simmer",
        "section": "words",
        "mode": "words",
        "category": "Food and Cooking Words",
        "level": "INTERMEDIATE",
        "telugu_text": "చిన్న మంటపై నెమ్మదిగా ఉడికించడం",
        "telugu_transliteration": "Chinna mantapai udikinchadam",
        "english_text": "Simmer",
        "valid_alternatives": ["cook slowly", "boil gently", "slow cook"],
        "pronunciation": "/ˈsɪm.ər/",
        "part_of_speech": "Verb",
        "english_definition": "To cook food gently just below boiling temperature.",
        "when_to_use": "Everyday kitchen cooking vocabulary.",
        "examples": [{"english": "Let the sambar simmer for ten minutes on low flame.", "telugu": "సాంబార్‌ను తక్కువ మంటపై పది నిమిషాలు ఉడకనివ్వండి."}],
        "synonyms": ["Slow cook", "Boil gently"]
    },
    {
        "uid": "word_sibling",
        "section": "words",
        "mode": "words",
        "category": "Family and Relationships",
        "level": "BEGINNER",
        "telugu_text": "తోబుట్టువు (సోదరుడు లేదా సోదరి)",
        "telugu_transliteration": "Thobuttuvu",
        "english_text": "Sibling",
        "valid_alternatives": ["brother or sister", "brother", "sister"],
        "pronunciation": "/ˈsɪb.lɪŋ/",
        "part_of_speech": "Noun",
        "english_definition": "A brother or sister.",
        "when_to_use": "Use instead of saying 'cousin brother' or 'own brother' when asking about family.",
        "examples": [{"english": "How many siblings do you have?", "telugu": "మీకు ఎంతమంది తోబుట్టువులు ఉన్నారు?"}],
        "mistakes": [{"incorrect": "He is my cousin brother.", "correct": "He is my cousin.", "reason": "In natural English, say 'cousin' without adding 'brother' or 'sister'."}],
        "synonyms": ["Brother or sister"]
    },
    {
        "uid": "word_feedback",
        "section": "words",
        "mode": "words",
        "category": "Office Vocabulary",
        "level": "BEGINNER",
        "telugu_text": "అభిప్రాయం / సూచనలు",
        "telugu_transliteration": "Abhipraayam / Soochanalu",
        "english_text": "Feedback",
        "valid_alternatives": ["review", "comments", "suggestions", "input"],
        "pronunciation": "/ˈfiːd.bæk/",
        "part_of_speech": "Noun (Uncountable)",
        "english_definition": "Helpful information or criticism given to improve work or performance.",
        "when_to_use": "Remember: 'feedback' is uncountable—never say 'feedbacks'!",
        "examples": [{"english": "Thank you for the constructive feedback on my report.", "telugu": "నా రిపోర్ట్‌పై ఇచ్చిన విలువైన సూచనలకు ధన్యవాదాలు."}],
        "mistakes": [{"incorrect": "Please give me your feedbacks.", "correct": "Please give me your feedback.", "reason": "'Feedback' has no plural form."}],
        "synonyms": ["Input", "Comments", "Review"]
    },
    {
        "uid": "word_coordinate",
        "section": "words",
        "mode": "words",
        "category": "Workplace Vocabulary",
        "level": "INTERMEDIATE",
        "telugu_text": "సమన్వయం చేయడం",
        "telugu_transliteration": "Samanvayam cheyadam",
        "english_text": "Coordinate",
        "valid_alternatives": ["organize", "align", "arrange together", "manage"],
        "pronunciation": "/kəʊˈɔː.dɪ.neɪt/",
        "part_of_speech": "Verb",
        "english_definition": "To organize different people or activities so they work effectively together.",
        "when_to_use": "Common verb for event planning and project management.",
        "examples": [{"english": "I will coordinate with the design team to finalize the layout.", "telugu": "లేఅవుట్ ఖరారు చేయడానికి నేను డిజైన్ టీమ్‌తో సమన్వయం చేస్తాను."}],
        "synonyms": ["Organize", "Align"]
    },
    {
        "uid": "word_itinerary",
        "section": "words",
        "mode": "words",
        "category": "Travel Vocabulary",
        "level": "ADVANCED",
        "telugu_text": "ప్రయాణ ప్రణాళిక / రూట్ ప్లాన్",
        "telugu_transliteration": "Prayana pranalika",
        "english_text": "Itinerary",
        "valid_alternatives": ["travel plan", "trip schedule", "route plan"],
        "pronunciation": "/aɪˈtɪn.ər.ər.i/",
        "part_of_speech": "Noun",
        "english_definition": "A detailed plan of a journey, including places to visit and dates.",
        "when_to_use": "Use when organizing trips, vacations, or business travel.",
        "examples": [{"english": "Let's finalize our travel itinerary before booking hotels.", "telugu": "హోటల్స్ బుక్ చేసే ముందు మన ప్రయాణ ప్రణాళికను ఖరారు చేద్దాం."}],
        "synonyms": ["Travel plan", "Schedule"]
    },
    {
        "uid": "word_advice",
        "section": "words",
        "mode": "words",
        "category": "Commonly Confused Words",
        "level": "BEGINNER",
        "telugu_text": "సలహా",
        "telugu_transliteration": "Salaha",
        "english_text": "Advice",
        "valid_alternatives": ["suggestion", "guidance", "tip", "counsel"],
        "pronunciation": "/ədˈvaɪs/",
        "part_of_speech": "Noun (Uncountable)",
        "english_definition": "Guidance or recommendations offered to help someone decide what to do.",
        "when_to_use": "'Advice' (with C) is the noun; 'Advise' (with S) is the verb. Never say 'advices'!",
        "examples": [{"english": "Thank you for that helpful piece of advice.", "telugu": "ఆ ఉపయోగకరమైన సలహా ఇచ్చినందుకు ధన్యవాదాలు."}],
        "mistakes": [{"incorrect": "He gave me good advices.", "correct": "He gave me good advice.", "reason": "'Advice' is uncountable."}],
        "synonyms": ["Guidance", "Suggestion"]
    },
    {
        "uid": "word_refund",
        "section": "words",
        "mode": "words",
        "category": "Shopping Vocabulary",
        "level": "BEGINNER",
        "telugu_text": "డబ్బు వాపసు / తిరిగి చెల్లింపు",
        "telugu_transliteration": "Dabbu vaapasu",
        "english_text": "Refund",
        "valid_alternatives": ["money back", "repayment", "return the money"],
        "pronunciation": "/ˈriː.fʌnd/",
        "part_of_speech": "Noun / Verb",
        "english_definition": "Money paid back to you because an item was returned or an order was cancelled.",
        "examples": [{"english": "Since the product was damaged, they issued a full refund.", "telugu": "వస్తువు దెబ్బతిన్నందున వారు పూర్తి డబ్బును వాపసు ఇచ్చారు."}],
        "synonyms": ["Money back", "Reimbursement"]
    },
    {
        "uid": "word_deadline_missed",
        "section": "words",
        "mode": "words",
        "category": "Verbs Used in Daily Life",
        "level": "INTERMEDIATE",
        "telugu_text": "ఆలస్యం చేయడం / సాగదీయడం",
        "telugu_transliteration": "Aalasyam cheyadam / Saagadeeyadam",
        "english_text": "Procrastinate",
        "valid_alternatives": ["delay unnecessarily", "put off", "waste time delaying"],
        "pronunciation": "/prəˈkræs.tɪ.neɪt/",
        "part_of_speech": "Verb",
        "english_definition": "To keep delaying tasks that you know you should do soon.",
        "examples": [{"english": "Try not to procrastinate when studying for interviews.", "telugu": "ఇంటర్వ్యూలకు చదివేటప్పుడు పనులను వాయిదా వేస్తూ సాగదీయకండి."}],
        "synonyms": ["Put off", "Stall", "Delay"]
    },
    {
        "uid": "word_curious",
        "section": "words",
        "mode": "words",
        "category": "Adjectives Used in Conversations",
        "level": "BEGINNER",
        "telugu_text": "తెలుసుకోవాలనే ఆసక్తి గల",
        "telugu_transliteration": "Thelusukovalane aasakthi",
        "english_text": "Curious",
        "valid_alternatives": ["eager to know", "interested", "inquisitive"],
        "pronunciation": "/ˈkjʊə.ri.əs/",
        "part_of_speech": "Adjective",
        "english_definition": "Wanting to learn or know more about something.",
        "examples": [{"english": "I'm curious to learn how voice recognition works.", "telugu": "వాయిస్ రికగ్నిషన్ ఎలా పనిచేస్తుందో తెలుసుకోవాలని నాకు ఆసక్తిగా ఉంది."}],
        "synonyms": ["Interested", "Eager to know"]
    },
    {
        "uid": "word_flexible",
        "section": "words",
        "mode": "words",
        "category": "Workplace Vocabulary",
        "level": "INTERMEDIATE",
        "telugu_text": "సమయానికి లేదా పరిస్థితికి అనుగుణంగా మారగలిగే",
        "telugu_transliteration": "Anugunanga maaragalige",
        "english_text": "Flexible",
        "valid_alternatives": ["adaptable", "adjustable", "open to change"],
        "pronunciation": "/ˈflek.sə.bəl/",
        "part_of_speech": "Adjective",
        "english_definition": "Able to change easily to suit new conditions or schedules.",
        "examples": [{"english": "I am flexible with the meeting timing tomorrow.", "telugu": "రేపు మీటింగ్ సమయం విషయంలో నాకు ఏ సమయమైనా అనుకూలమే."}],
        "synonyms": ["Adaptable", "Adjustable"]
    },
    {
        "uid": "word_efficient",
        "section": "words",
        "mode": "words",
        "category": "Advanced Vocabulary",
        "level": "ADVANCED",
        "telugu_text": "తక్కువ సమయంలో సమర్థవంతంగా పని చేసే",
        "telugu_transliteration": "Samarthavanthanga pani chese",
        "english_text": "Efficient",
        "valid_alternatives": ["productive", "effective", "well-organized", "streamlined"],
        "pronunciation": "/ɪˈfɪʃ.ənt/",
        "part_of_speech": "Adjective",
        "english_definition": "Working quickly and cleanly without wasting time, effort, or money.",
        "examples": [{"english": "Using keyboard shortcuts is a very efficient way to work.", "telugu": "కీబోర్డ్ షార్ట్‌కట్స్ వాడటం పనిని త్వరగా, సమర్థవంతంగా చేసే మార్గం."}],
        "synonyms": ["Productive", "Well-organized"]
    },
]

EXPRESSIONS_LIBRARY = [
    {
        "uid": "expr_never_mind",
        "section": "phrases",
        "mode": "expressions",
        "category": "Daily Conversations",
        "level": "BEGINNER",
        "telugu_text": "పోనీ లే / ఏం పర్లేదు",
        "telugu_transliteration": "Poni le / Em parledhu",
        "english_text": "Never mind",
        "valid_alternatives": ["it's okay", "no problem", "forget it", "don't worry about it", "that's alright", "leave it"],
        "pronunciation": "/ˈnev.ər maɪnd/",
        "part_of_speech": "Expression",
        "english_definition": "Used to tell someone politely not to worry about a small mistake or change.",
        "when_to_use": "When someone apologizes for something minor or you decide to drop a small matter.",
        "contextual_alternatives": [
            {"english": "Never mind, it happens.", "context": "Casual dismissal when someone makes a small error."},
            {"english": "No worries at all.", "context": "Warm, friendly reassurance among friends or colleagues."},
            {"english": "Leave it, it's fine.", "context": "Moving past a topic comfortably."}
        ],
        "examples": [
            {"english": "Oh, you forgot the pen? Never mind, I have an extra one.", "telugu": "అయ్యో, పెన్ మర్చిపోయావా? పోనీ లే, నా దగ్గర ఇంకోటి ఉంది."}
        ],
        "mistakes": [
            {"incorrect": "Leave it, don't do tension.", "correct": "Never mind, don't worry about it.", "reason": "'Don't do tension' is a direct Telugu-to-English phrase; use 'don't worry about it'."}
        ],
        "synonyms": ["No worries", "Forget it", "It's fine"]
    },
    {
        "uid": "expr_let_us_see",
        "section": "phrases",
        "mode": "expressions",
        "category": "Daily Conversations",
        "level": "BEGINNER",
        "telugu_text": "చూద్దాం / తర్వాత చూద్దాం",
        "telugu_transliteration": "Chooddam",
        "english_text": "Let's see",
        "valid_alternatives": ["we'll see", "let us check", "we will check later", "let's figure it out"],
        "part_of_speech": "Expression",
        "english_definition": "Used when thinking about a decision or checking what happens next.",
        "when_to_use": "Depending on context: 'Let's check' (inspecting now) vs 'We'll see' (deciding in the future).",
        "contextual_alternatives": [
            {"english": "Let's see what happens.", "context": "Waiting for future results."},
            {"english": "We'll see about the weekend plan.", "context": "Not committing to a future plan yet."}
        ],
        "examples": [
            {"english": "Let's see how the new schedule works this week.", "telugu": "ఈ వారం కొత్త షెడ్యూల్ ఎలా పనిచేస్తుందో చూద్దాం."}
        ],
        "synonyms": ["We'll see", "Let's check"]
    },
    {
        "uid": "expr_i_got_it",
        "section": "phrases",
        "mode": "expressions",
        "category": "Daily Conversations",
        "level": "BEGINNER",
        "telugu_text": "నాకు అర్థమైంది",
        "telugu_transliteration": "Naaku arthamaindi",
        "english_text": "I got it",
        "valid_alternatives": ["i understand", "got it", "that makes sense", "i understood", "clear"],
        "part_of_speech": "Expression",
        "english_definition": "Signals clearly that you understood an explanation or instruction.",
        "when_to_use": "Natural conversational way to confirm understanding.",
        "contextual_alternatives": [
            {"english": "Got it, thanks for explaining!", "context": "Casual conversations with teammates and friends."},
            {"english": "That makes complete sense.", "context": "Polite workplace confirmation."}
        ],
        "examples": [
            {"english": "Ah, I got it! You click save before closing the tab.", "telugu": "ఆ, నాకు అర్థమైంది! ట్యాబ్ క్లోజ్ చేసే ముందు సేవ్ క్లిక్ చేయాలి కదా."}
        ],
        "mistakes": [
            {"incorrect": "I am understood.", "correct": "I understand / I got it.", "reason": "Saying 'I am understood' means other people understand you! Say 'I understand'."}
        ],
        "synonyms": ["I understand", "Makes sense"]
    },
    {
        "uid": "expr_not_like_that",
        "section": "phrases",
        "mode": "expressions",
        "category": "Agreeing and Disagreeing",
        "level": "BEGINNER",
        "telugu_text": "అలా కాదు",
        "telugu_transliteration": "Ala kaadhu",
        "english_text": "That's not what I meant",
        "valid_alternatives": ["not like that", "it's not like that", "actually, not that way", "that's not right"],
        "part_of_speech": "Expression",
        "english_definition": "Gently corrects a misunderstanding without sounding rude.",
        "when_to_use": "Use 'Not like that' casually or 'That's not what I meant' politely.",
        "examples": [
            {"english": "Not like that—you need to stir it slowly on low heat.", "telugu": "అలా కాదు—తక్కువ మంట మీద నెమ్మదిగా కలపాలి."}
        ],
        "synonyms": ["Not like that", "Let me clarify"]
    },
    {
        "uid": "expr_drop_it",
        "section": "phrases",
        "mode": "expressions",
        "category": "Daily Conversations",
        "level": "BEGINNER",
        "telugu_text": "వదిలేయ్ / దాని గురించి మాట్లాడకు",
        "telugu_transliteration": "Vadhiley",
        "english_text": "Let it go",
        "valid_alternatives": ["drop it", "leave it", "forget about it", "don't worry about it"],
        "part_of_speech": "Expression",
        "english_definition": "Used to tell someone to stop worrying or arguing about an unpleasant thing.",
        "examples": [
            {"english": "It's over now—just let it go and move on.", "telugu": "అది అయిపోయింది కదా—వదిలేయ్, ముందుకు వెళ్దాం."}
        ],
        "synonyms": ["Drop it", "Forget it"]
    },
    {
        "uid": "expr_i_remember",
        "section": "phrases",
        "mode": "expressions",
        "category": "Daily Conversations",
        "level": "BEGINNER",
        "telugu_text": "నాకు గుర్తుంది",
        "telugu_transliteration": "Naaku gurthundi",
        "english_text": "I remember",
        "valid_alternatives": ["i recall", "i still remember", "it rings a bell", "yes, i remember"],
        "part_of_speech": "Expression",
        "english_definition": "Confirms that you have a memory of a person, promise, or fact.",
        "examples": [
            {"english": "Yes, I clearly remember your advice from last month.", "telugu": "అవును, గత నెలలో నువ్వు ఇచ్చిన సలహా నాకు బాగా గుర్తుంది."}
        ],
        "mistakes": [
            {"incorrect": "For me it is remembering.", "correct": "I remember it.", "reason": "Keep 'remember' active: 'I remember', not 'is remembering for me'."}
        ],
        "synonyms": ["I recall", "It comes to mind"]
    },
    {
        "uid": "expr_slipped_my_mind",
        "section": "phrases",
        "mode": "expressions",
        "category": "Natural Alternatives",
        "level": "INTERMEDIATE",
        "telugu_text": "నాకు గుర్తులేదు / పూర్తిగా మర్చిపోయాను",
        "telugu_transliteration": "Naaku gurthu ledhu",
        "english_text": "It slipped my mind",
        "valid_alternatives": ["i don't remember", "i forgot", "i can't remember", "i can't recall"],
        "part_of_speech": "Expression",
        "english_definition": "A very natural English idiom meaning 'I accidentally forgot'.",
        "examples": [
            {"english": "I'm sorry I didn't call back—it completely slipped my mind.", "telugu": "మళ్ళీ కాల్ చేయలేకపోయాను క్షమించండి—పూర్తిగా మర్చిపోయాను."}
        ],
        "synonyms": ["I forgot", "I don't recall"]
    },
    {
        "uid": "expr_no_problem",
        "section": "phrases",
        "mode": "expressions",
        "category": "Apologies and Thanking",
        "level": "BEGINNER",
        "telugu_text": "ఏం పర్లేదు / ఇబ్బంది ఏమీ లేదు",
        "telugu_transliteration": "Em parledhu",
        "english_text": "No problem at all",
        "valid_alternatives": ["no problem", "that's fine", "don't mention it", "you're welcome", "not an issue", "no worries"],
        "part_of_speech": "Expression",
        "english_definition": "Polite reassurance in response to 'Thank you' or 'Sorry'.",
        "examples": [
            {"english": "No problem at all! I'm always happy to help.", "telugu": "ఏం పర్లేదు! సహాయం చేయడానికి నేను ఎప్పుడూ సిద్ధంగా ఉంటాను."}
        ],
        "synonyms": ["You're welcome", "Don't mention it"]
    },
    {
        "uid": "expr_on_my_way",
        "section": "phrases",
        "mode": "expressions",
        "category": "Daily Conversations",
        "level": "BEGINNER",
        "telugu_text": "నేను దారిలోనే ఉన్నాను / వస్తున్నాను",
        "telugu_transliteration": "Nenu daarilone unnanu",
        "english_text": "I'm on my way",
        "valid_alternatives": ["i am on the way", "coming right now", "heading there now"],
        "part_of_speech": "Expression",
        "english_definition": "Lets someone know you have already started traveling to meet them.",
        "examples": [
            {"english": "Wait five minutes—I'm on my way to the office!", "telugu": "ఐదు నిమిషాలు ఆగు—నేను ఆఫీసు దారిలోనే ఉన్నాను!"}
        ],
        "synonyms": ["Heading over now", "Nearly there"]
    },
    {
        "uid": "expr_reach_home_call",
        "section": "sentences",
        "mode": "expressions",
        "category": "Complete Telugu-to-English Sentences",
        "level": "INTERMEDIATE",
        "telugu_text": "నేను ఇంటికి చేరుకోగానే నీకు ఫోన్ చేస్తాను",
        "telugu_transliteration": "Nenu intiki cherukogane neeku phone chesthanu",
        "english_text": "I will call you as soon as I get home",
        "valid_alternatives": [
            "i will call you once i reach home",
            "i'll call you when i reach home",
            "i will phone you after reaching home",
            "i'll call you once i get home"
        ],
        "part_of_speech": "Complete Sentence",
        "sentence_structure": "Subject + will + Verb1 + as soon as + Subject + present simple verb",
        "word_by_word": [
            {"telugu": "నేను", "english": "I"},
            {"telugu": "ఇంటికి చేరుకోగానే", "english": "as soon as I get home"},
            {"telugu": "నీకు ఫోన్ చేస్తాను", "english": "will call you"}
        ],
        "english_definition": "In time clauses with 'as soon as' or 'when', use Present Simple instead of 'will'.",
        "examples": [
            {"english": "I'll message you as soon as I reach the station.", "telugu": "స్టేషన్‌కు చేరుకోగానే నీకు మెసేజ్ చేస్తాను."}
        ],
        "mistakes": [
            {"incorrect": "I will call you as soon as I will reach home.", "correct": "I will call you as soon as I get home.", "reason": "Never use 'will' inside the 'as soon as / when' part of the sentence."}
        ],
        "synonyms": ["I'll ring you once I'm home"]
    },
    {
        "uid": "expr_looking_forward",
        "section": "phrases",
        "mode": "expressions",
        "category": "Office Communication",
        "level": "INTERMEDIATE",
        "telugu_text": "మీ స్పందన కోసం ఆసక్తిగా ఎదురుచూస్తున్నాను",
        "telugu_transliteration": "Mee spandana kosam eduruchusthunnanu",
        "english_text": "I look forward to hearing from you",
        "valid_alternatives": ["looking forward to your reply", "i am looking forward to hearing from you", "waiting for your response"],
        "part_of_speech": "Workplace Expression",
        "english_definition": "Polite, professional email closing showing positive anticipation.",
        "examples": [
            {"english": "Thank you for the interview. I look forward to hearing from you.", "telugu": "ఇంటర్వ్యూకు ధన్యవాదాలు. మీ స్పందన కోసం ఎదురుచూస్తున్నాను."}
        ],
        "mistakes": [
            {"incorrect": "I look forward to hear from you.", "correct": "I look forward to hearing from you.", "reason": "Always use verb + '-ing' after 'look forward to'."}
        ],
        "synonyms": ["Waiting for your response"]
    },
    {
        "uid": "expr_let_me_check",
        "section": "phrases",
        "mode": "expressions",
        "category": "Office Communication",
        "level": "BEGINNER",
        "telugu_text": "నేను ఒకసారి చెక్ చేసి చెబుతాను",
        "telugu_transliteration": "Nenu okasari check chesi chepthanu",
        "english_text": "Let me check and get back to you",
        "valid_alternatives": ["i will check and tell you", "let me verify and inform you", "i'll check and let you know"],
        "part_of_speech": "Workplace Expression",
        "english_definition": "Professional phrase used when you don't know an answer immediately and need to verify it.",
        "examples": [
            {"english": "Good question—let me check with the manager and get back to you.", "telugu": "మంచి ప్రశ్న—మేనేజర్‌తో చెక్ చేసి మీకు మళ్ళీ చెబుతాను."}
        ],
        "synonyms": ["I'll verify and update you"]
    },
    {
        "uid": "expr_could_you_repeat",
        "section": "phrases",
        "mode": "expressions",
        "category": "Asking Questions",
        "level": "BEGINNER",
        "telugu_text": "దయచేసి మరొక్కసారి చెబుతారా?",
        "telugu_transliteration": "Dayachesi marokkasari chepthara?",
        "english_text": "Could you please repeat that?",
        "valid_alternatives": ["could you say that again", "pardon me", "sorry, could you repeat", "can you please repeat"],
        "part_of_speech": "Polite Request",
        "english_definition": "Courteous way to ask someone to repeat what they just said.",
        "examples": [
            {"english": "Sorry, the line broke up. Could you please repeat that?", "telugu": "క్షమించండి, కాల్ కట్ అయింది. దయచేసి మళ్ళీ చెబుతారా?"}
        ],
        "mistakes": [
            {"incorrect": "Tell again!", "correct": "Could you please repeat that?", "reason": "'Tell again' sounds abrupt; 'Could you please repeat that?' is polite."}
        ],
        "synonyms": ["Excuse me?", "Could you say that again?"]
    },
    {
        "uid": "expr_keep_in_touch",
        "section": "phrases",
        "mode": "expressions",
        "category": "Friends and Family",
        "level": "BEGINNER",
        "telugu_text": "టచ్‌లో ఉండండి / అప్పుడప్పుడూ మాట్లాడుకుంటూ ఉందాం",
        "telugu_transliteration": "Touch lo undandi",
        "english_text": "Keep in touch",
        "valid_alternatives": ["stay in touch", "stay connected", "let's stay in touch"],
        "part_of_speech": "Expression",
        "english_definition": "Stay connected through calls or messages even when busy or far away.",
        "examples": [
            {"english": "It was lovely meeting you! Let's keep in touch.", "telugu": "నిన్ను కలవడం చాలా సంతోషంగా ఉంది! టచ్‌లో ఉందాం."}
        ],
        "synonyms": ["Stay connected", "Stay in touch"]
    },
    {
        "uid": "expr_not_feeling_well",
        "section": "sentences",
        "mode": "expressions",
        "category": "Complete Telugu-to-English Sentences",
        "level": "BEGINNER",
        "telugu_text": "ఈరోజు నాకు ఆరోగ్యం బాగాలేదు",
        "telugu_transliteration": "Eeroju naaku arogyam baagaledhu",
        "english_text": "I'm not feeling well today",
        "valid_alternatives": ["i am feeling unwell today", "i am sick today", "i'm under the weather today", "my health is not good today"],
        "part_of_speech": "Complete Sentence",
        "sentence_structure": "Subject + am not + feeling well + time",
        "word_by_word": [
            {"telugu": "నాకు", "english": "I"},
            {"telugu": "ఆరోగ్యం బాగాలేదు", "english": "am not feeling well"},
            {"telugu": "ఈరోజు", "english": "today"}
        ],
        "english_definition": "Natural way to inform family, friends, or managers that you are unwell.",
        "examples": [
            {"english": "I'm not feeling well today, so I need to take rest.", "telugu": "ఈరోజు నాకు ఒంట్లో బాగోలేదు, కాబట్టి రెస్ట్ తీసుకోవాలి."}
        ],
        "synonyms": ["I feel under the weather"]
    },
    {
        "uid": "expr_how_is_it_going",
        "section": "phrases",
        "mode": "expressions",
        "category": "Greetings",
        "level": "BEGINNER",
        "telugu_text": "అంతా ఎలా నడుస్తోంది? / పనులు ఎలా ఉన్నాయి?",
        "telugu_transliteration": "Antha ela nadusthondi?",
        "english_text": "How is it going?",
        "valid_alternatives": ["how's it going", "how are things", "how have you been", "how are you doing"],
        "part_of_speech": "Greeting",
        "english_definition": "Natural warm greeting to ask someone about their day or work.",
        "examples": [
            {"english": "Hey Kiran! Long time no see. How is it going?", "telugu": "హాయ్ కిరణ్! చాలా రోజులైంది చూసి. పనులు ఎలా నడుస్తున్నాయి?"}
        ],
        "synonyms": ["How are things?", "How's everything?"]
    },
    {
        "uid": "expr_in_my_opinion",
        "section": "phrases",
        "mode": "expressions",
        "category": "Agreeing and Disagreeing",
        "level": "INTERMEDIATE",
        "telugu_text": "నా అభిప్రాయం ప్రకారం / నాకు అనిపించేది ఏమిటంటే",
        "telugu_transliteration": "Naa abhiprayam prakaaram",
        "english_text": "In my opinion",
        "valid_alternatives": ["from my perspective", "i think", "in my view", "to be honest"],
        "part_of_speech": "Conversational Connector",
        "english_definition": "Polite opener when sharing your personal viewpoint in meetings or interviews.",
        "examples": [
            {"english": "In my opinion, starting early saves a lot of stress.", "telugu": "నా అభిప్రాయం ప్రకారం, ముందే మొదలుపెడితే ఒత్తిడి తగ్గుతుంది."}
        ],
        "mistakes": [
            {"incorrect": "According to me, this is better.", "correct": "In my opinion, this is better.", "reason": "Say 'According to [someone else]', and 'In my opinion' for yourself."}
        ],
        "synonyms": ["From my point of view", "I believe"]
    },
    {
        "uid": "expr_pass_interview_strengths",
        "section": "phrases",
        "mode": "expressions",
        "category": "Interview Expressions",
        "level": "ADVANCED",
        "telugu_text": "నేను త్వరగా కొత్త విషయాలు నేర్చుకోగలను",
        "telugu_transliteration": "Nenu thvaraga kottha vishayalu nerchukogalanu",
        "english_text": "I am a quick learner",
        "valid_alternatives": ["i pick up new things quickly", "i learn quickly", "i adapt fast to new tools"],
        "part_of_speech": "Interview Expression",
        "english_definition": "Confident expression to showcase adaptability during job interviews.",
        "examples": [
            {"english": "One of my biggest strengths is that I am a quick learner.", "telugu": "నా బలాల్లో ముఖ్యమైనది నేను కొత్త విషయాలు త్వరగా నేర్చుకోవడం."}
        ],
        "synonyms": ["I adapt fast", "I pick up skills rapidly"]
    },
    {
        "uid": "expr_running_late",
        "section": "phrases",
        "mode": "expressions",
        "category": "Workplace Communication",
        "level": "BEGINNER",
        "telugu_text": "ట్రాఫిక్ వల్ల నాకు కాస్త ఆలస్యం అవుతోంది",
        "telugu_transliteration": "Naaku aalasyam avuthondi",
        "english_text": "I'm running a little late",
        "valid_alternatives": ["i am running late", "i will be slightly late", "stuck in traffic, i'll be late"],
        "part_of_speech": "Expression",
        "english_definition": "Polite phrase to warn colleagues or friends if you won't arrive exactly on time.",
        "examples": [
            {"english": "Sorry team, I'm running ten minutes late due to heavy traffic.", "telugu": "క్షమించండి టీమ్, ట్రాఫిక్ వల్ల పది నిమిషాలు ఆలస్యంగా వస్తాను."}
        ],
        "synonyms": ["I'll be delayed slightly"]
    },
    {
        "uid": "expr_stuck_in_work",
        "section": "phrases",
        "mode": "expressions",
        "category": "Daily Conversations",
        "level": "INTERMEDIATE",
        "telugu_text": "నేను ఒక పనిలో బిజీగా ఇరుక్కుపోయాను",
        "telugu_transliteration": "Nenu panilo busy ga irukkupoyanu",
        "english_text": "I got caught up with some work",
        "valid_alternatives": ["i was tied up with work", "i am busy with work", "i got stuck in work"],
        "part_of_speech": "Expression",
        "english_definition": "Explains politely why you couldn't reply or join earlier.",
        "examples": [
            {"english": "Sorry I missed your message—I got caught up with an urgent client call.", "telugu": "మీ మెసేజ్ చూడలేకపోయాను—ఒక అర్జెంట్ క్లయింట్ కాల్‌లో బిజీగా ఉండిపోయాను."}
        ],
        "synonyms": ["I was tied up"]
    },
    {
        "uid": "expr_what_do_you_mean",
        "section": "phrases",
        "mode": "expressions",
        "category": "Asking Questions",
        "level": "BEGINNER",
        "telugu_text": "మీ ఉద్దేశం ఏమిటి? / మీరు చెప్పేదానికి అర్థం ఏంటి?",
        "telugu_transliteration": "Mee uddesham emiti?",
        "english_text": "What do you mean by that?",
        "valid_alternatives": ["what do you mean", "could you clarify what you mean", "what are you trying to say"],
        "part_of_speech": "Question",
        "english_definition": "Asks someone politely to clarify a confusing statement.",
        "examples": [
            {"english": "What do you mean by 'urgent upgrade'? Is the server down?", "telugu": "'అర్జెంట్ అప్‌గ్రేడ్' అంటే మీ ఉద్దేశం ఏమిటి? సర్వర్ డౌన్ అయిందా?"}
        ],
        "synonyms": ["Could you clarify that?"]
    },
    {
        "uid": "expr_makes_sense",
        "section": "phrases",
        "mode": "expressions",
        "category": "Natural Alternatives",
        "level": "INTERMEDIATE",
        "telugu_text": "ఆ మాట సహేతుకంగానే ఉంది / కరెక్ట్ అనిపిస్తోంది",
        "telugu_transliteration": "Correct anipisthondi",
        "english_text": "That makes a lot of sense",
        "valid_alternatives": ["that makes sense", "fair enough", "sounds logical", "you have a good point"],
        "part_of_speech": "Expression",
        "english_definition": "Shows intelligent agreement with someone's logic or reasoning.",
        "examples": [
            {"english": "Fixing the database timeout first makes a lot of sense.", "telugu": "ముందుగా డేటాబేస్ టైమౌట్ సరిచేయడం కరెక్ట్ అనిపిస్తోంది."}
        ],
        "synonyms": ["Sounds reasonable", "Fair point"]
    },
    {
        "uid": "expr_take_it_easy",
        "section": "phrases",
        "mode": "expressions",
        "category": "Natural Alternatives",
        "level": "BEGINNER",
        "telugu_text": "టెన్షన్ పడకు / ప్రశాంతంగా ఉండు",
        "telugu_transliteration": "Tension padaku",
        "english_text": "Take it easy",
        "valid_alternatives": ["calm down", "relax", "don't stress", "don't panic"],
        "part_of_speech": "Expression",
        "english_definition": "Kind expression to help someone relax instead of saying 'Don't take tension'.",
        "examples": [
            {"english": "Take it easy! Everyone makes mistakes while learning.", "telugu": "టెన్షన్ పడకు! నేర్చుకునేటప్పుడు అందరూ తప్పులు చేస్తారు."}
        ],
        "synonyms": ["Relax", "Don't stress out"]
    },
    {
        "uid": "expr_used_to_living",
        "section": "sentences",
        "mode": "expressions",
        "category": "Complete Telugu-to-English Sentences",
        "level": "INTERMEDIATE",
        "telugu_text": "నాకు ఈ నగరంలో ఉండటం అలవాటు అయింది",
        "telugu_transliteration": "Naaku ee nagaram lo undadam alavaatu ayindi",
        "english_text": "I have gotten used to living in this city",
        "valid_alternatives": ["i am used to living in this city", "i got used to living here", "i'm accustomed to living in this city"],
        "part_of_speech": "Complete Sentence",
        "sentence_structure": "Subject + be/get + used to + Verb-ing",
        "word_by_word": [
            {"telugu": "నాకు", "english": "I"},
            {"telugu": "అలవాటు అయింది", "english": "am used to / got used to"},
            {"telugu": "ఇక్కడ ఉండటం", "english": "living here"}
        ],
        "english_definition": "Describes something that felt new at first but now feels normal.",
        "examples": [
            {"english": "After six months, I am used to waking up at 6 AM.", "telugu": "ఆరు నెలల తర్వాత నాకు ఉదయం 6 గంటలకు లేవడం అలవాటైంది."}
        ],
        "mistakes": [
            {"incorrect": "I am used to live in this city.", "correct": "I am used to living in this city.", "reason": "After 'be/get used to', always use the '-ing' form (living)."}
        ],
        "synonyms": ["I'm comfortable living here now"]
    },
]

SITUATION_EXPRESSIONS_LIBRARY = [
    # 1. Daily Life
    {
        "uid": "sit_daily_water",
        "section": "situations",
        "mode": "situation_expressions",
        "category": "Daily Life",
        "level": "BEGINNER",
        "telugu_text": "దయచేసి నాకు ఒక గ్లాసు మంచినీళ్ళు ఇస్తారా?",
        "telugu_transliteration": "Dayachesi oka glass water isthara?",
        "english_text": "Could I please have a glass of water?",
        "valid_alternatives": ["can i have a glass of water please", "please give me a glass of water", "may i have some water"],
        "english_definition": "Polite everyday request for drinking water at a home or cafe.",
        "examples": [{"english": "Excuse me, could I have a glass of water, please?", "telugu": "ఎక్స్‌క్యూజ్ మీ, ఒక గ్లాసు మంచినీళ్ళు ఇస్తారా?"}],
        "dialogue": [{"speaker": "Guest", "text": "Could I please have a glass of water?"}, {"speaker": "Host", "text": "Sure! Here you go."}]
    },
    {
        "uid": "sit_daily_electricity",
        "section": "situations",
        "mode": "situation_expressions",
        "category": "Daily Life",
        "level": "BEGINNER",
        "telugu_text": "మా వీధిలో కరెంట్ పోయింది, ఎప్పుడు వస్తుందో తెలుసా?",
        "telugu_transliteration": "Current poyindi, eppudu vasthundo telusa?",
        "english_text": "There's a power outage in our street—do you know when it'll be back?",
        "valid_alternatives": ["the power went out in our area, when will it come back", "power is gone in our street, any idea when it restores"],
        "english_definition": "Natural phrase using 'power outage' or 'power went out' instead of 'current gone'.",
        "examples": [{"english": "Power went out around noon due to maintenance.", "telugu": "మెయింటెనెన్స్ వల్ల మధ్యాహ్నం కరెంట్ పోయింది."}]
    },
    {
        "uid": "sit_daily_wake_early",
        "section": "situations",
        "mode": "situation_expressions",
        "category": "Daily Life",
        "level": "BEGINNER",
        "telugu_text": "రేపు ఉదయం నన్ను ఆరు గంటలకు నిద్రలేపు",
        "telugu_transliteration": "Repu nannu 6 ki nidra lepu",
        "english_text": "Please wake me up at 6 AM tomorrow",
        "valid_alternatives": ["wake me up at 6 tomorrow morning", "can you wake me up at six tomorrow"],
        "english_definition": "Asking family members politely to wake you up.",
        "examples": [{"english": "Can you wake me up at 6 AM so I don't miss my train?", "telugu": "ట్రైన్ మిస్ కాకుండా నన్ను ఉదయం 6 గంటలకు లేపుతావా?"}]
    },
    # 2. Office
    {
        "uid": "sit_office_early_leave",
        "section": "situations",
        "mode": "situation_expressions",
        "category": "Office",
        "level": "INTERMEDIATE",
        "telugu_text": "ఈరోజు వ్యక్తిగత పని వల్ల కొంచెం త్వరగా వెళ్ళవచ్చా అని మేనేజర్‌ని అడగడం",
        "telugu_transliteration": "Eeroju konchem thvaraga vellavacha ani manager ni adagadam",
        "english_text": "Would it be alright if I left a little early today?",
        "valid_alternatives": ["may i leave early today", "could i leave a bit early today", "can i take half day today", "i need to leave early today if that's okay"],
        "english_definition": "Polite workplace phrasing for requesting early departure.",
        "examples": [{"english": "I've finished all my tasks; would it be okay if I left an hour early today?", "telugu": "నా పనులన్నీ పూర్తి చేశాను; ఈరోజు ఒక గంట ముందు వెళ్ళవచ్చా?"}]
    },
    {
        "uid": "sit_office_join_call",
        "section": "situations",
        "mode": "situation_expressions",
        "category": "Office",
        "level": "BEGINNER",
        "telugu_text": "నేను ఐదు నిమిషాల్లో మీటింగ్‌కి జాయిన్ అవుతాను",
        "telugu_transliteration": "Nenu 5 minutes lo join avuthanu",
        "english_text": "I'll join the meeting in five minutes",
        "valid_alternatives": ["i will join the call in five minutes", "joining in 5 mins", "be right there in 5 minutes"],
        "english_definition": "Standard Slack/Teams update when slightly delayed.",
        "examples": [{"english": "Restarting my laptop—I'll join the meeting in five minutes.", "telugu": "లాప్‌టాప్ రీస్టార్ట్ చేస్తున్నాను—ఐదు నిమిషాల్లో జాయిన్ అవుతాను."}]
    },
    {
        "uid": "sit_office_send_file",
        "section": "situations",
        "mode": "situation_expressions",
        "category": "Office",
        "level": "BEGINNER",
        "telugu_text": "దయచేసి ఆ డాక్యుమెంట్‌ను నాకు ఈమెయిల్ చేయగలరా?",
        "telugu_transliteration": "Aa document email cheyagalara?",
        "english_text": "Could you please email that document to me?",
        "valid_alternatives": ["please send me that file over email", "can you share that document with me", "kindly mail me that file"],
        "english_definition": "Polite office request for files or reports.",
        "examples": [{"english": "Could you please share the updated budget spreadsheet with me?", "telugu": "దయచేసి అప్‌డేటెడ్ బడ్జెట్ ఫైల్‌ను నాతో షేర్ చేయగలరా?"}]
    },
    # 3. Friends and Family
    {
        "uid": "sit_friends_catchup",
        "section": "situations",
        "mode": "situation_expressions",
        "category": "Friends and Family",
        "level": "BEGINNER",
        "telugu_text": "ఈ వీకెండ్‌లో మనం కాఫీకి కలుద్దామా?",
        "telugu_transliteration": "Ee weekend lo coffee ki kaluddama?",
        "english_text": "Shall we catch up over coffee this weekend?",
        "valid_alternatives": ["let's meet for coffee this weekend", "want to grab coffee this weekend", "should we meet this weekend"],
        "english_definition": "Natural friendly invitation using 'catch up'.",
        "examples": [{"english": "It's been ages! Let's catch up over coffee this Saturday.", "telugu": "చాలా కాలమైంది కలిసి! ఈ శనివారం కాఫీ తాగుతూ మాట్లాడుకుందాం."}]
    },
    {
        "uid": "sit_friends_congratulate",
        "section": "situations",
        "mode": "situation_expressions",
        "category": "Friends and Family",
        "level": "BEGINNER",
        "telugu_text": "నీ కొత్త ఉద్యోగానికి హృదయపూర్వక శుభాకాంక్షలు",
        "telugu_transliteration": "Kottha udyoganiki shubhakankshalu",
        "english_text": "Congratulations on your new job!",
        "valid_alternatives": ["congrats on getting the new job", "happy for your new job", "many congratulations on your new role"],
        "english_definition": "Warm way to congratulate loved ones (use 'on', not 'for' after congratulations).",
        "examples": [{"english": "Congratulations on your promotion! You truly deserve it.", "telugu": "నీ ప్రమోషన్‌కు శుభాకాంక్షలు! నువ్వు దీనికి పూర్తిగా అర్హుడివి."}]
    },
    {
        "uid": "sit_family_dinner_ready",
        "section": "situations",
        "mode": "situation_expressions",
        "category": "Friends and Family",
        "level": "BEGINNER",
        "telugu_text": "భోజనం సిద్ధంగా ఉంది, అందరూ రండి",
        "telugu_transliteration": "Bhojanam siddhamga undi",
        "english_text": "Dinner is ready, please come to the table",
        "valid_alternatives": ["dinner is served", "food is ready, let's eat", "come eat, dinner is ready"],
        "english_definition": "Everyday home phrase calling family members to eat.",
        "examples": [{"english": "Everyone, wash your hands—dinner is ready!", "telugu": "అందరూ చేతులు కడుక్కోండి—భోజనం సిద్ధంగా ఉంది!"}]
    },
    # 4. Shopping
    {
        "uid": "sit_shopping_discount",
        "section": "situations",
        "mode": "situation_expressions",
        "category": "Shopping",
        "level": "BEGINNER",
        "telugu_text": "దీని మీద ఏమైనా డిస్కౌంట్ ఉందా?",
        "telugu_transliteration": "Deeni meeda emaina discount unda?",
        "english_text": "Is there any discount on this item?",
        "valid_alternatives": ["do you offer any discount on this", "can you lower the price a bit", "any offers on this"],
        "english_definition": "Polite inquiry at retail counters.",
        "examples": [{"english": "I really like this jacket—is there any festival discount on it?", "telugu": "నాకు ఈ జాకెట్ బాగా నచ్చింది—దీనిపై ఏమైనా పండుగ డిస్కౌంట్ ఉందా?"}]
    },
    {
        "uid": "sit_shopping_try_on",
        "section": "situations",
        "mode": "situation_expressions",
        "category": "Shopping",
        "level": "BEGINNER",
        "telugu_text": "ట్రయల్ రూమ్ ఎక్కడుంది? ఇది నాకు సరిపోతుందో లేదో చూసుకోవాలి",
        "telugu_transliteration": "Trial room ekkadundi?",
        "english_text": "Where is the fitting room? I'd like to try this on.",
        "valid_alternatives": ["where is the changing room, can i try this", "can i try this on in the trial room"],
        "english_definition": "Useful shopping question when buying clothes.",
        "examples": [{"english": "Could I try this shirt on in medium size?", "telugu": "ఈ షర్ట్ మీడియం సైజులో వేసి చూసుకోవచ్చా?"}]
    },
    {
        "uid": "sit_shopping_exchange",
        "section": "situations",
        "mode": "situation_expressions",
        "category": "Shopping",
        "level": "INTERMEDIATE",
        "telugu_text": "ఇది సైజ్ సరిపోకపోతే మార్చుకోవచ్చా?",
        "telugu_transliteration": "Size saripokapothe marchukovacha?",
        "english_text": "Can I exchange this if the size doesn't fit?",
        "valid_alternatives": ["is it possible to exchange if it doesn't fit", "what is your exchange policy for size issues"],
        "english_definition": "Smart question before buying gifts or apparel.",
        "examples": [{"english": "Could I exchange this within seven days if needed?", "telugu": "అవసరమైతే ఏడు రోజుల్లో దీన్ని మార్చుకోవచ్చా?"}]
    },
    # 5. Travel
    {
        "uid": "sit_travel_bus_stop",
        "section": "situations",
        "mode": "situation_expressions",
        "category": "Travel",
        "level": "BEGINNER",
        "telugu_text": "ఈ బస్సు రైల్వే స్టేషన్‌కు వెళ్తుందా?",
        "telugu_transliteration": "Ee bus railway station ki velthunda?",
        "english_text": "Does this bus go to the railway station?",
        "valid_alternatives": ["will this bus stop at the railway station", "is this bus going towards the station"],
        "english_definition": "Confirm route before boarding public transport.",
        "examples": [{"english": "Excuse me, does this metro train stop at Ameerpet?", "telugu": "ఎక్స్‌క్యూజ్ మీ, ఈ మెట్రో అమీర్‌పేట్‌లో ఆగుతుందా?"}]
    },
    {
        "uid": "sit_travel_window_seat",
        "section": "situations",
        "mode": "situation_expressions",
        "category": "Travel",
        "level": "BEGINNER",
        "telugu_text": "నాకు విండో సీటు కావాలి",
        "telugu_transliteration": "Naaku window seat kaavali",
        "english_text": "I would prefer a window seat, please",
        "valid_alternatives": ["i want a window seat", "could i get a window seat", "can i have a window seat"],
        "english_definition": "Polite seat preference at flight/train check-in counters.",
        "examples": [{"english": "If available, could you assign me a window seat?", "telugu": "ఖాళీ ఉంటే దయచేసి నాకు విండో సీటు ఇవ్వగలరా?"}]
    },
    {
        "uid": "sit_travel_lost_bag",
        "section": "situations",
        "mode": "situation_expressions",
        "category": "Travel",
        "level": "INTERMEDIATE",
        "telugu_text": "నా బ్యాగ్ ఇంకా రాలేదు, దయచేసి సహాయం చేయండి",
        "telugu_transliteration": "Naa bag inka raledhu, sahayam cheyandi",
        "english_text": "My luggage hasn't arrived yet—could you please help me check?",
        "valid_alternatives": ["my bag is missing, please help", "i haven't received my baggage yet"],
        "english_definition": "Calmly reporting delayed baggage at transport desks.",
        "examples": [{"english": "Excuse me, my suitcase isn't on the belt yet.", "telugu": "క్షమించండి, నా సూట్‌కేస్ ఇంకా బెల్ట్ మీద రాలేదు."}]
    },
    # 6. Restaurant
    {
        "uid": "sit_restaurant_table",
        "section": "situations",
        "mode": "situation_expressions",
        "category": "Restaurant",
        "level": "BEGINNER",
        "telugu_text": "నలుగురికి టేబుల్ ఖాళీగా ఉందా?",
        "telugu_transliteration": "Naluguriki table khaaliga unda?",
        "english_text": "Do you have a table for four?",
        "valid_alternatives": ["table for four please", "is there a table available for four people"],
        "english_definition": "Standard polite question when entering a busy restaurant.",
        "examples": [{"english": "Good evening! Do you have a quiet table for four?", "telugu": "శుభ సాయంత్రం! నలుగురికి ప్రశాంతమైన టేబుల్ ఉందా?"}]
    },
    {
        "uid": "sit_restaurant_less_spicy",
        "section": "situations",
        "mode": "situation_expressions",
        "category": "Restaurant",
        "level": "BEGINNER",
        "telugu_text": "దయచేసి కూరలో కారం తక్కువ వేయండి",
        "telugu_transliteration": "Kaaram thakkuva veyandi",
        "english_text": "Please make it mild, not too spicy",
        "valid_alternatives": ["could you make it less spicy", "keep the spice level mild please", "not too spicy please"],
        "english_definition": "Customizing food spice level naturally.",
        "examples": [{"english": "I'll order paneer butter masala—please make it mild.", "telugu": "పన్నీర్ బటర్ మసాలా ఆర్డర్ చేస్తాను—దయచేసి కారం తక్కువ చేయండి."}]
    },
    {
        "uid": "sit_restaurant_bill",
        "section": "situations",
        "mode": "situation_expressions",
        "category": "Restaurant",
        "level": "BEGINNER",
        "telugu_text": "దయచేసి బిల్లు తీసుకురండి",
        "telugu_transliteration": "Dayachesi bill theesukurandi",
        "english_text": "Could we have the bill, please?",
        "valid_alternatives": ["can we get the check please", "please bring the bill", "bill please"],
        "english_definition": "Polite phrase when ready to pay after dining.",
        "examples": [{"english": "Everything was great! Could we have the bill, please?", "telugu": "భోజనం చాలా బాగుంది! దయచేసి బిల్లు ఇస్తారా?"}]
    },
    # 7. Social Conversations
    {
        "uid": "sit_social_nice_to_meet",
        "section": "situations",
        "mode": "situation_expressions",
        "category": "Social Conversations",
        "level": "BEGINNER",
        "telugu_text": "మిమ్మల్ని కలవడం చాలా సంతోషంగా ఉంది",
        "telugu_transliteration": "Mimmali kalavadam chala santhosham",
        "english_text": "It was a pleasure meeting you",
        "valid_alternatives": ["nice to meet you", "glad to meet you", "pleased to meet you"],
        "english_definition": "Polite parting or greeting remark in social gatherings.",
        "examples": [{"english": "Thank you for your time—it was a real pleasure meeting you!", "telugu": "మీ సమయానికి ధన్యవాదాలు—మిమ్మల్ని కలవడం నాకు ఎంతో ఆనందంగా ఉంది!"}]
    },
    {
        "uid": "sit_social_hobby",
        "section": "situations",
        "mode": "situation_expressions",
        "category": "Social Conversations",
        "level": "INTERMEDIATE",
        "telugu_text": "ఖాళీ సమయంలో మీకు ఏం చేయడం ఇష్టం?",
        "telugu_transliteration": "Khaali samayam lo em cheyadam ishtam?",
        "english_text": "What do you enjoy doing in your free time?",
        "valid_alternatives": ["what are your hobbies", "what do you do in your spare time", "how do you spend weekends"],
        "english_definition": "Engaging small-talk starter at events or parties.",
        "examples": [{"english": "Besides work, what do you enjoy doing in your free time?", "telugu": "పని కాకుండా, ఖాళీ సమయంలో మీకు ఏం చేయడం ఇష్టం?"}]
    },
    {
        "uid": "sit_social_compliment",
        "section": "situations",
        "mode": "situation_expressions",
        "category": "Social Conversations",
        "level": "INTERMEDIATE",
        "telugu_text": "నీ డ్రెస్ చాలా బాగుంది / నీ ఇంగ్లీష్ చాలా బాగుంది",
        "telugu_transliteration": "Chala baagundi",
        "english_text": "You've improved so much—that sounds great!",
        "valid_alternatives": ["that looks great on you", "you sound very confident", "well done"],
        "english_definition": "Friendly encouragement during social chats.",
        "examples": [{"english": "You've improved your speaking skills so much in just a few weeks!", "telugu": "కొన్ని వారాల్లోనే నీ మాట్లాడే విధానం చాలా మెరుగుపడింది!"}]
    },
    # 8. Job Interviews
    {
        "uid": "sit_interview_strength",
        "section": "situations",
        "mode": "situation_expressions",
        "category": "Job Interviews",
        "level": "INTERMEDIATE",
        "telugu_text": "నా ప్రధాన బలం సమస్యలను ప్రశాంతంగా పరిష్కరించడం",
        "telugu_transliteration": "Naa pradhana balam problem solving",
        "english_text": "My biggest strength is calm problem-solving under pressure",
        "valid_alternatives": ["my strength is solving problems calmly", "i stay calm and solve problems well"],
        "english_definition": "Clear, impactful answer to 'What are your strengths?'.",
        "examples": [{"english": "I would say my core strength is staying calm and breaking down complex issues.", "telugu": "క్లిష్ట సమస్యలను ప్రశాంతంగా విభజించి పరిష్కరించడం నా బలం."}]
    },
    {
        "uid": "sit_interview_ask_role",
        "section": "situations",
        "mode": "situation_expressions",
        "category": "Job Interviews",
        "level": "ADVANCED",
        "telugu_text": "ఈ రోల్ లో మీరు మొదటి 90 రోజుల్లో నా నుండి ఏమి ఆశిస్తున్నారు?",
        "telugu_transliteration": "Modati 90 rojullo em expect chesthunnaru?",
        "english_text": "What would you expect from me in the first 90 days?",
        "valid_alternatives": ["what are the expectations for the first 3 months", "what goals do you have for this role initially"],
        "english_definition": "Smart closing question to ask the interviewer at the end.",
        "examples": [{"english": "Thank you—what does success in the first 90 days look like for this role?", "telugu": "ధన్యవాదాలు—ఈ రోల్‌లో మొదటి 90 రోజుల విజయాన్ని మీరు ఎలా చూస్తారు?"}]
    },
    {
        "uid": "sit_interview_salary",
        "section": "situations",
        "mode": "situation_expressions",
        "category": "Job Interviews",
        "level": "ADVANCED",
        "telugu_text": "కంపెనీ ప్రమాణాలు మరియు నా అనుభవానికి తగ్గట్టు జీతం ఆశిస్తున్నాను",
        "telugu_transliteration": "Company standards prakaram salary expect chesthunnanu",
        "english_text": "I'm open to a package aligned with my skills and industry standards",
        "valid_alternatives": ["i am flexible based on company standards", "i expect compensation matching market standards"],
        "english_definition": "Diplomatic salary discussion line for HR rounds.",
        "examples": [{"english": "I'm open to discussing a fair package based on my skills and market standards.", "telugu": "నా నైపుణ్యాలు మరియు మార్కెట్ ప్రమాణాలకు తగిన ప్యాకేజీ చర్చించడానికి సిద్ధంగా ఉన్నాను."}]
    },
    # 9. Workplace Communication
    {
        "uid": "sit_workplace_standup",
        "section": "situations",
        "mode": "situation_expressions",
        "category": "Workplace Communication",
        "level": "INTERMEDIATE",
        "telugu_text": "నిన్న నేను లాగిన్ బగ్ ఫిక్స్ చేశాను, ఈరోజు టెస్టింగ్ చేస్తాను",
        "telugu_transliteration": "Ninna bug fix chesanu, eeroju testing chesthanu",
        "english_text": "Yesterday I resolved the login bug, and today I'll focus on testing",
        "valid_alternatives": ["yesterday i fixed the login bug and today i am testing", "i fixed the login issue yesterday; today is testing"],
        "english_definition": "Crisp daily standup status update.",
        "examples": [{"english": "Quick update: yesterday I fixed the login bug, and today I'm writing unit tests.", "telugu": "త్వరిత అప్‌డేట్: నిన్న లాగిన్ బగ్ ఫిక్స్ చేశాను, ఈరోజు యూనిట్ టెస్టులు రాస్తున్నాను."}]
    },
    {
        "uid": "sit_workplace_clarify_deadline",
        "section": "situations",
        "mode": "situation_expressions",
        "category": "Workplace Communication",
        "level": "INTERMEDIATE",
        "telugu_text": "మరికొంత స్పష్టత ఉంటే నేను పని త్వరగా పూర్తి చేయగలను",
        "telugu_transliteration": "Konchem clarity unte tondaraga complete chesthanu",
        "english_text": "Could you clarify the requirements so I can proceed smoothly?",
        "valid_alternatives": ["please share more clarity on this task", "could we confirm the scope before i start"],
        "english_definition": "Proactive communication that avoids wasted effort.",
        "examples": [{"english": "Before I begin coding, could you clarify the expected output format?", "telugu": "కోడింగ్ ప్రారంభించే ముందు, ఆశించిన అవుట్‌పుట్ ఫార్మాట్‌ను స్పష్టం చేయగలరా?"}]
    },
    {
        "uid": "sit_workplace_share_screen",
        "section": "situations",
        "mode": "situation_expressions",
        "category": "Workplace Communication",
        "level": "BEGINNER",
        "telugu_text": "నా స్క్రీన్ మీకు కనిపిస్తోందా?",
        "telugu_transliteration": "Naa screen kanipisthonda?",
        "english_text": "Is my screen visible to everyone?",
        "valid_alternatives": ["can you see my screen", "is my screen shared clearly", "can everyone see my screen"],
        "english_definition": "Everyday remote meeting phrase.",
        "examples": [{"english": "Let me share my screen—can everyone see the dashboard clearly?", "telugu": "నా స్క్రీన్ షేర్ చేస్తాను—డ్యాష్‌బోర్డ్ అందరికీ స్పష్టంగా కనిపిస్తోందా?"}]
    },
]

FULL_CONTENT_LIBRARY = WORDS_LIBRARY + EXPRESSIONS_LIBRARY + SITUATION_EXPRESSIONS_LIBRARY
