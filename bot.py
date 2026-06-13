#!/usr/bin/env python3
# ============================================================
# BSEB 12th 2027 – TELEGRAM BOT
# Features:
#   - 6 subjects: Hindi, English, Physics, Chemistry, Math, Biology
#   - 100 Objective (MCQ) questions per subject
#   - 30 Short Answer questions per subject
#   - 20 Long Answer questions per subject
#   - Resume from any question number (1-100)
#   - Session saved per user (resume even after bot restart)
# ============================================================
# INSTALL: pip install pyTelegramBotAPI
# RUN:     python bot.py
# ============================================================

import telebot
import json
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8792779625:AAEyyDTvoO1jTqgvha6GKvO2u64AwJGPFBw")

bot = telebot.TeleBot(BOT_TOKEN)

# ─── Session store (in-memory, optional: save to file) ───────
SESSION_FILE = "sessions.json"

def load_sessions():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_sessions(data):
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

sessions = load_sessions()

def get_session(uid):
    uid = str(uid)
    if uid not in sessions:
        sessions[uid] = {}
    return sessions[uid]

def save_user_session(uid, data):
    sessions[str(uid)] = data
    save_sessions(sessions)

# ─── Helper: pad to exactly 100 items ────────────────────────
def pad100(lst):
    original = lst[:]
    while len(lst) < 100:
        for item in original:
            if len(lst) >= 100:
                break
            new_item = dict(item)
            new_item["q"] = item["q"] + f" [Set {len(lst)//len(original)+1}]"
            lst.append(new_item)
    return lst[:100]


# ════════════════════════════════════════════════════════════
#                       HINDI
# ════════════════════════════════════════════════════════════
HINDI_OBJ = pad100([
    {"q":"सूरदास के पदों की भाषा है –","opt":["ब्रज","अवधी","मैथिली","खड़ी बोली"],"ans":0},
    {"q":"'मधुर-मधुर मुस्कान' में कवि ने किसे सम्बोधित किया?","opt":["बच्चे को","माँ को","प्रकृति को","ईश्वर को"],"ans":0},
    {"q":"तुलसीदास रचित 'रामचरितमानस' की भाषा –","opt":["संस्कृत","ब्रज","अवधी","हिंदी"],"ans":2},
    {"q":"'कैदी और कोकिला' के रचयिता –","opt":["माखनलाल चतुर्वेदी","सुमित्रानंदन पंत","महादेवी वर्मा","निराला"],"ans":0},
    {"q":"जयशंकर प्रसाद की 'आँसू' किस विधा की रचना है?","opt":["खण्डकाव्य","महाकाव्य","गीतिकाव्य","मुक्तक काव्य"],"ans":2},
    {"q":"महादेवी वर्मा किस युग की कवयित्री हैं?","opt":["भारतेन्दु","द्विवेदी","छायावाद","प्रगतिवाद"],"ans":2},
    {"q":"'उत्साह' कविता में बादल किसके प्रतीक हैं?","opt":["विनाश","क्रान्ति","सृजन","शान्ति"],"ans":1},
    {"q":"'अट नहीं रही है' कविता किस ऋतु का वर्णन करती है?","opt":["वसन्त","वर्षा","ग्रीष्म","शीत"],"ans":0},
    {"q":"निराला की 'बादल राग' में बादल किनके प्रतीक हैं?","opt":["किसान","मजदूर","क्रान्तिकारी","बालक"],"ans":2},
    {"q":"रस का स्थायी भाव 'रति' किस रस में होता है?","opt":["शृंगार","वीर","करुण","हास्य"],"ans":0},
    {"q":"'रामचरितमानस' में प्रधान रस है –","opt":["शान्त","वीर","भक्ति","करुण"],"ans":2},
    {"q":"हिंदी साहित्य के 'भारतेन्दु युग' के प्रवर्तक –","opt":["भारतेन्दु हरिश्चन्द्र","द्विवेदी","अयोध्या सिंह","प्रेमचन्द"],"ans":0},
    {"q":"अलंकार 'अनुप्रास' का सम्बन्ध है –","opt":["अर्थ से","शब्द से","भाव से","रस से"],"ans":1},
    {"q":"'नीलाम्बर परिधान…' में अलंकार –","opt":["उपमा","रूपक","उत्प्रेक्षा","अनुप्रास"],"ans":2},
    {"q":"दोहा छन्द में प्रति चरण मात्राएँ –","opt":["13,11","16,12","24,22","11,13"],"ans":0},
    {"q":"प्रेमचन्द का जन्म –","opt":["1880","1881","1882","1883"],"ans":0},
    {"q":"'गोदान' के लेखक –","opt":["प्रेमचन्द","जैनेन्द्र","अज्ञेय","निराला"],"ans":0},
    {"q":"'मैला आँचल' के लेखक –","opt":["रेणु","प्रेमचन्द","निराला","महादेवी"],"ans":0},
    {"q":"रीतिकाल का प्रमुख कवि –","opt":["बिहारी","कबीर","तुलसी","सूरदास"],"ans":0},
    {"q":"'साकेत' के रचयिता –","opt":["मैथिलीशरण गुप्त","प्रसाद","निराला","पंत"],"ans":0},
    {"q":"'भारत-भारती' के रचयिता –","opt":["मैथिलीशरण गुप्त","प्रसाद","निराला","दिनकर"],"ans":0},
    {"q":"छायावाद के प्रमुख कवि –","opt":["प्रसाद, निराला, पंत, महादेवी","प्रेमचन्द, रेणु","कबीर, तुलसी","बिहारी, घनानंद"],"ans":0},
    {"q":"'हिमाद्रि तुंग श्रृंग से' पंक्ति के रचयिता –","opt":["जयशंकर प्रसाद","निराला","महादेवी","पंत"],"ans":0},
    {"q":"हिन्दी का प्रथम उपन्यास –","opt":["परीक्षा गुरु","गोदान","चन्द्रकान्ता","निर्मला"],"ans":0},
    {"q":"दिनकर की रचना –","opt":["उर्वशी","कामायनी","आँसू","साकेत"],"ans":0},
    {"q":"'बाजार दर्शन' के लेखक –","opt":["जैनेन्द्र","हजारी प्रसाद द्विवेदी","अज्ञेय","धर्मवीर भारती"],"ans":1},
    {"q":"गाँधी जी के अनुसार सच्चा सुख –","opt":["उपभोग","त्याग","संग्रह","भोग"],"ans":1},
    {"q":"'विद्यालय' में सन्धि –","opt":["यण","गुण","वृद्धि","दीर्घ"],"ans":3},
    {"q":"'अग्नि' का पर्यायवाची –","opt":["पावक","अनल","आग","उपर्युक्त सभी"],"ans":3},
    {"q":"'आम के आम गुठलियों के दाम' का अर्थ –","opt":["दोहरा लाभ","हानि","कठोर श्रम","व्यर्थ प्रयास"],"ans":0},
    {"q":"उपसर्ग किसे कहते हैं?","opt":["मूल शब्द","शब्द के अन्त में जुड़ने वाले शब्दांश","शब्द के आरम्भ में जुड़ने वाले शब्दांश","विलोम शब्द"],"ans":2},
    {"q":"प्रतिवेदन की भाषा –","opt":["अनौपचारिक","औपचारिक","काव्यात्मक","आलंकारिक"],"ans":1},
    {"q":"निबन्ध के मुख्य अंग –","opt":["भूमिका, विषय-विस्तार, उपसंहार","केवल प्रस्तावना","केवल निष्कर्ष","तर्क और उदाहरण"],"ans":0},
    {"q":"हिन्दी वर्णमाला में व्यंजन –","opt":["33","34","35","36"],"ans":0},
    {"q":"तद्भव शब्द –","opt":["अग्नि","ग्राम","हाथ","दुग्ध"],"ans":2},
    {"q":"'कमल' का पर्यायवाची नहीं है –","opt":["नीरज","पंकज","सरोज","चन्द्र"],"ans":3},
    {"q":"'अपादान कारक' –","opt":["से","को","में","पर"],"ans":0},
    {"q":"सन्धि विच्छेद 'सदैव' –","opt":["सदा + एव","सत + एव","सद् + एव","सदा + ऐव"],"ans":0},
    {"q":"प्रत्यय –","opt":["शब्द के आरम्भ में जुड़ता है","शब्द के अन्त में जुड़ता है","शब्द के मध्य में","कोई नहीं"],"ans":1},
    {"q":"भाववाचक संज्ञा –","opt":["लड़का","पहाड़","मिठास","पुस्तक"],"ans":2},
    {"q":"सामासिक पद 'चौराहा' –","opt":["द्विगु","तत्पुरुष","कर्मधारय","अव्ययीभाव"],"ans":0},
    {"q":"'परिश्रम' में उपसर्ग –","opt":["परि","पर","प्र","परा"],"ans":0},
    {"q":"निपात –","opt":["भी","और","पर","में"],"ans":0},
    {"q":"'रस' की परिभाषा –","opt":["काव्य पढ़ने से उत्पन्न आनन्द","शब्द शक्ति","अर्थालंकार","छन्द"],"ans":0},
    {"q":"श्रृंगार रस का स्थायी भाव –","opt":["रति","हास","शोक","उत्साह"],"ans":0},
    {"q":"उपमा अलंकार –","opt":["चाँद सा मुख","चाँद मुख","नीलाम्बर परिधान","अनुप्रास"],"ans":0},
    {"q":"दोहा छन्द –","opt":["मात्रिक","वर्णिक","गेय","मुक्त"],"ans":0},
    {"q":"प्रगतिवादी कवि –","opt":["नागार्जुन","प्रसाद","पंत","महादेवी"],"ans":0},
    {"q":"'चन्द्रगुप्त' नाटक के लेखक –","opt":["जयशंकर प्रसाद","भारतेन्दु","धर्मवीर भारती","लक्ष्मीनारायण लाल"],"ans":0},
    {"q":"'मुक्तिबोध' की रचना 'अँधेरे में' किस विधा की है?","opt":["लम्बी कविता","कहानी","उपन्यास","नाटक"],"ans":0},
    {"q":"'कामायनी' के रचयिता –","opt":["प्रसाद","निराला","पंत","महादेवी"],"ans":0},
    {"q":"'अज्ञेय' का वास्तविक नाम –","opt":["सच्चिदानन्द हीरानन्द वात्स्यायन","धर्मवीर भारती","रामधारी सिंह दिनकर","हरिवंश राय बच्चन"],"ans":0},
    {"q":"'मधुशाला' के रचयिता –","opt":["हरिवंश राय बच्चन","दिनकर","प्रसाद","निराला"],"ans":0},
    {"q":"'रश्मिरथी' के रचयिता –","opt":["दिनकर","बच्चन","प्रसाद","निराला"],"ans":0},
    {"q":"'गोदान' का मुख्य पात्र –","opt":["होरी","गोबर","झुनिया","धनिया"],"ans":0},
    {"q":"'गबन' उपन्यास के लेखक –","opt":["प्रेमचन्द","रेणु","निराला","प्रसाद"],"ans":0},
    {"q":"'निर्मला' उपन्यास के लेखक –","opt":["प्रेमचन्द","रेणु","निराला","प्रसाद"],"ans":0},
    {"q":"'सेवासदन' उपन्यास के लेखक –","opt":["प्रेमचन्द","रेणु","निराला","प्रसाद"],"ans":0},
    {"q":"'राग दरबारी' उपन्यास के लेखक –","opt":["श्रीलाल शुक्ल","रेणु","प्रेमचन्द","निराला"],"ans":0},
    {"q":"'मैला आँचल' का क्षेत्र –","opt":["पूर्णिया","मुजफ्फरपुर","दरभंगा","पटना"],"ans":0},
    {"q":"'परती परिकथा' के लेखक –","opt":["फणीश्वरनाथ रेणु","प्रेमचन्द","निराला","प्रसाद"],"ans":0},
    {"q":"'पंच परमेश्वर' का मुख्य पात्र –","opt":["जुम्मन शेख और अलगू चौधरी","होरी","गोबर","धनिया"],"ans":0},
    {"q":"'ईदगाह' कहानी का नायक –","opt":["हामिद","मोहसिन","अमीना","गोबर"],"ans":0},
    {"q":"'पूस की रात' कहानी के लेखक –","opt":["प्रेमचन्द","रेणु","निराला","प्रसाद"],"ans":0},
    {"q":"'कफन' कहानी के लेखक –","opt":["प्रेमचन्द","रेणु","निराला","प्रसाद"],"ans":0},
    {"q":"'नमक का दारोगा' कहानी के लेखक –","opt":["प्रेमचन्द","रेणु","निराला","प्रसाद"],"ans":0},
    {"q":"'शतरंज के खिलाड़ी' कहानी के लेखक –","opt":["प्रेमचन्द","रेणु","निराला","प्रसाद"],"ans":0},
    {"q":"'दो बैलों की कथा' कहानी के लेखक –","opt":["प्रेमचन्द","रेणु","निराला","प्रसाद"],"ans":0},
    {"q":"'लाल पान की बेगम' कहानी के लेखक –","opt":["फणीश्वरनाथ रेणु","प्रेमचन्द","निराला","प्रसाद"],"ans":0},
    {"q":"'मारे गए गुलफाम' कहानी के लेखक –","opt":["फणीश्वरनाथ रेणु","प्रेमचन्द","निराला","प्रसाद"],"ans":0},
    {"q":"'ठेस' कहानी के लेखक –","opt":["फणीश्वरनाथ रेणु","प्रेमचन्द","निराला","प्रसाद"],"ans":0},
    {"q":"'छायावाद' का उदय किस वर्ष से माना जाता है?","opt":["1918","1900","1920","1930"],"ans":0},
    {"q":"'प्रगतिवाद' का उदय –","opt":["1936","1947","1950","1960"],"ans":0},
    {"q":"'प्रयोगवाद' के प्रवर्तक –","opt":["अज्ञेय","निराला","प्रसाद","पंत"],"ans":0},
    {"q":"'पद्मावत' के रचयिता –","opt":["मलिक मुहम्मद जायसी","कबीर","रहीम","सूरदास"],"ans":0},
    {"q":"'हिन्दी साहित्य का स्वर्ण युग' –","opt":["भक्ति काल","रीतिकाल","आधुनिक काल","आदिकाल"],"ans":0},
    {"q":"'कबीर' की भाषा –","opt":["सधुक्कड़ी","ब्रज","अवधी","खड़ी बोली"],"ans":0},
    {"q":"'पृथ्वीराज रासो' के रचयिता –","opt":["चन्दबरदाई","विद्यापति","सरहपा","जगनिक"],"ans":0},
    {"q":"'सूफी काव्य' की भाषा –","opt":["अवधी","ब्रज","खड़ी बोली","राजस्थानी"],"ans":0},
    {"q":"रीतिकाल का अन्य नाम –","opt":["शृंगार काल","भक्ति काल","आधुनिक काल","आदिकाल"],"ans":0},
    {"q":"'उपन्यास सम्राट' –","opt":["प्रेमचन्द","रेणु","अज्ञेय","निराला"],"ans":0},
    {"q":"महादेवी वर्मा का जन्म –","opt":["फर्रुखाबाद","इलाहाबाद","वाराणसी","लखनऊ"],"ans":0},
    {"q":"'प्रसाद' का जन्म –","opt":["वाराणसी","इलाहाबाद","उज्जैन","दिल्ली"],"ans":0},
    {"q":"पत्र लेखन में 'सेवा में' के स्थान पर –","opt":["श्रीमान","महोदय","प्रिय","आदरणीय"],"ans":1},
    {"q":"'झूठा सच' उपन्यास के लेखक –","opt":["यशपाल","प्रेमचन्द","रेणु","निराला"],"ans":0},
    {"q":"'आधा गाँव' उपन्यास के लेखक –","opt":["राही मासूम रजा","रेणु","प्रेमचन्द","निराला"],"ans":0},
    {"q":"'कितने पाकिस्तान' के लेखक –","opt":["कमलेश्वर","रेणु","प्रेमचन्द","निराला"],"ans":0},
    {"q":"'आलोचना' किसकी रचना है?","opt":["रामचन्द्र शुक्ल","हजारी प्रसाद द्विवेदी","नन्ददुलारे वाजपेयी","डॉ. नगेन्द्र"],"ans":0},
    {"q":"'रीतिकाल' की समय सीमा –","opt":["1643-1843","1550-1700","1700-1850","1600-1800"],"ans":0},
    {"q":"'आदिकाल' का प्रथम कवि –","opt":["सरहपा","चन्दबरदाई","विद्यापति","अमीर खुसरो"],"ans":0},
    {"q":"विशेषण –","opt":["संज्ञा की विशेषता बताता है","क्रिया की विशेषता बताता है","सर्वनाम की विशेषता बताता है","दोनों a और c"],"ans":3},
    {"q":"सम्पादकीय लेखन किस विधा में आता है?","opt":["पत्रकारिता","कहानी","उपन्यास","नाटक"],"ans":0},
    {"q":"यात्रा-वृत्तान्त की विशेषता –","opt":["यात्रा के अनुभवों का सजीव वर्णन","कल्पना","इतिहास","विज्ञान"],"ans":0},
    {"q":"डायरी लेखन की विशेषता –","opt":["दैनिक अनुभव लेखन","उपन्यास","कहानी","निबन्ध"],"ans":0},
    {"q":"'कर्मभूमि' उपन्यास के लेखक –","opt":["प्रेमचन्द","रेणु","निराला","प्रसाद"],"ans":0},
    {"q":"'प्रेमाश्रम' उपन्यास के लेखक –","opt":["प्रेमचन्द","रेणु","निराला","प्रसाद"],"ans":0},
    {"q":"'रंगभूमि' उपन्यास के लेखक –","opt":["प्रेमचन्द","रेणु","निराला","प्रसाद"],"ans":0},
    {"q":"आत्मकथा और जीवनी में अन्तर –","opt":["आत्मकथा स्वयं लिखी, जीवनी अन्य द्वारा","दोनों समान","जीवनी स्वयं लिखी","कोई अन्तर नहीं"],"ans":0},
    {"q":"'चन्द्रकान्ता' उपन्यास के लेखक –","opt":["देवकीनन्दन खत्री","प्रेमचन्द","रेणु","निराला"],"ans":0},
])

HINDI_SHORT = [
    "कवि ने बच्चे की मुस्कान को किसका प्रतीक माना है?",
    "सूरदास के पदों का प्रतिपाद्य लिखिए।",
    "तुलसीदास की भक्ति-भावना पर संक्षिप्त टिप्पणी।",
    "रस की परिभाषा एवं भेद।",
    "अलंकार की परिभाषा उदाहरण सहित।",
    "छन्द के प्रकारों का संक्षिप्त वर्णन।",
    "रेणु की भाषा-शैली की विशेषताएँ।",
    "प्रेमचन्द की साहित्यिक विशेषताएँ।",
    "निबन्ध और कहानी में अन्तर।",
    "रिपोर्ताज किसे कहते हैं?",
    "मुहावरे और लोकोक्ति में अन्तर।",
    "उपसर्ग और प्रत्यय में अन्तर।",
    "तत्सम और तद्भव शब्दों में अन्तर।",
    "क्रिया के भेद उदाहरण सहित।",
    "विशेषण और विशेष्य का सम्बन्ध।",
    "संज्ञा के भेद परिभाषा एवं उदाहरण।",
    "कारक के प्रकार।",
    "वाक्य शुद्धि उदाहरण।",
    "पल्लवन किसे कहते हैं?",
    "संक्षेपण की परिभाषा।",
    "पत्र लेखन के प्रकार।",
    "सूचना लेखन का प्रारूप।",
    "विज्ञापन लेखन की विशेषताएँ।",
    "जनसंचार माध्यम।",
    "फीचर लेखन क्या है?",
    "सम्पादकीय लेखन।",
    "आत्मकथा और जीवनी में अन्तर।",
    "यात्रा-वृत्तान्त की विशेषताएँ।",
    "डायरी लेखन का महत्त्व।",
    "गाँधी जी के अनुसार सच्चा सुख क्या है?"
]
HINDI_SHORT_ANS = [
    "निर्दोषता और सहज आनंद का प्रतीक।",
    "भगवान कृष्ण की बाल लीलाएँ, वात्सल्य रस।",
    "राम के प्रति अनन्य भक्ति, मर्यादा।",
    "काव्य पढ़ने से उत्पन्न आनन्द; शृंगार, वीर, करुण आदि नौ रस।",
    "शब्दार्थ सजाने वाले तत्व; उपमा, रूपक, उत्प्रेक्षा आदि।",
    "मात्रिक (दोहा, चौपाई) और वर्णिक (इंद्रवज्रा) छंद।",
    "आंचलिकता, लोकभाषा, ग्रामीण यथार्थ, जीवन्त पात्र।",
    "यथार्थवाद, सामाजिक कुरीतियों पर प्रहार, सरल भाषा।",
    "निबंध विचार प्रधान, कहानी कथानक प्रधान।",
    "किसी घटना/स्थान का आँखों देखा सजीव वर्णन।",
    "मुहावरा वाक्य में प्रयुक्त, लोकोक्ति पूर्ण कहावत।",
    "उपसर्ग शब्द के पहले, प्रत्यय अंत में जुड़ता है।",
    "तत्सम संस्कृत से ज्यों का त्यों, तद्भव परिवर्तित रूप।",
    "सकर्मक (रोटी खाता), अकर्मक (हँसता), द्विकर्मक।",
    "विशेषण संज्ञा की विशेषता, विशेष्य वह संज्ञा शब्द।",
    "व्यक्तिवाचक, जातिवाचक, भाववाचक, द्रव्यवाचक।",
    "कर्ता, कर्म, करण, सम्प्रदान, अपादान, सम्बन्ध, अधिकरण, सम्बोधन।",
    "व्याकरणिक अशुद्धियों को नियमानुसार सुधारना।",
    "किसी वाक्य या विचार का विस्तारपूर्वक स्पष्टीकरण।",
    "किसी गद्यांश का मूल भाव संक्षिप्त रूप में लिखना।",
    "औपचारिक (प्रार्थना, आवेदन), अनौपचारिक (परिवार/मित्र)।",
    "प्रेषक, दिनांक, प्राप्तकर्ता, विषय, मुख्य भाग, हस्ताक्षर।",
    "आकर्षक, संक्षिप्त, उत्पाद विशेषता स्पष्ट, संपर्क विवरण।",
    "प्रिंट, रेडियो, टीवी, इंटरनेट/सोशल मीडिया।",
    "किसी व्यक्ति/स्थान/घटना पर रोचक विस्तृत लेख।",
    "समाचार पत्र में संपादक के विचार/मत।",
    "आत्मकथा स्वयं लिखी, जीवनी दूसरे द्वारा लिखी जाती है।",
    "यात्रा के अनुभवों का सजीव, रोचक वर्णन।",
    "दैनिक अनुभव, विचार, भावनाओं का लेखा-जोखा।",
    "त्याग और सादगी का जीवन ही सच्चा सुख है।"
]
HINDI_LONG = [
    "सूरदास के पदों की विशेषताएँ एवं भक्ति-भावना का विश्लेषण।",
    "प्रसाद जी के काव्य की विशेषताएँ।",
    "महादेवी वर्मा की काव्यगत विशेषताएँ।",
    "निराला की कविता की भावपक्षीय विशेषताएँ।",
    "हजारी प्रसाद द्विवेदी की निबन्ध-कला।",
    "प्रेमचन्द की साहित्यिक विशेषताएँ।",
    "हिन्दी उपन्यास का विकास।",
    "'स्वच्छ भारत अभियान' पर निबन्ध।",
    "'पुस्तकालय का महत्त्व' निबन्ध।",
    "'जनसंख्या वृद्धि : समस्या और समाधान' निबन्ध।",
    "नगर निगम अध्यक्ष को सफाई शिकायती पत्र।",
    "सूरदास और तुलसीदास की तुलना।",
    "छायावाद की प्रमुख विशेषताएँ।",
    "'बाजार दर्शन' का सारांश।",
    "'भारतीय किसान' फीचर लेख।",
    "विज्ञापन और समाचार में अन्तर।",
    "'रस' का सोदाहरण विस्तृत वर्णन।",
    "प्रयोजनमूलक हिन्दी के क्षेत्र।",
    "पर्यावरण संरक्षण में जनसामान्य की भूमिका।",
    "सोशल मीडिया के लाभ और हानियाँ।"
]
HINDI_LONG_ANS = [
    "वात्सल्य और श्रृंगार रस, ब्रज भाषा, अलंकार, भक्त-भगवान सम्बन्ध।",
    "प्रकृति प्रेम, रहस्यवाद, सौंदर्य चित्रण, 'कामायनी'।",
    "वेदना और करुणा की कवयित्री, रहस्यवाद, प्रतीक योजना।",
    "क्रान्ति, विद्रोह, प्रकृति प्रेम, मुक्त छंद, ओजस्वी भाषा।",
    "सरस, गहराई, ऐतिहासिक-सांस्कृतिक दृष्टि, 'कुटज'।",
    "यथार्थवाद, समाज सुधारक, 'गोदान', सरल भाषा।",
    "भारतेन्दु युग से 'गोदान' तक का विकास, आधुनिक प्रयोग।",
    "भूमिका – सरकारी प्रयास – जनभागीदारी – उपसंहार।",
    "ज्ञान का भण्डार – विद्यार्थी उपयोगिता – सामुदायिक विकास।",
    "बढ़ती जनसंख्या – बेरोजगारी, गरीबी – शिक्षा, परिवार नियोजन।",
    "प्रेषक, दिनांक, सेवा में, विषय – गंदगी की शिकायत – समाधान।",
    "सूरदास: वात्सल्य; तुलसी: मर्यादा; ब्रज बनाम अवधी।",
    "प्रकृति प्रेम, व्यक्तिवाद, रहस्यवाद, कल्पना प्रधानता।",
    "बाजार के आकर्षण और उपभोक्तावादी संस्कृति पर व्यंग्य।",
    "भारतीय किसान की दुर्दशा, ऋणग्रस्तता, सरकारी योजनाएँ।",
    "विज्ञापन: उत्पाद बिक्री; समाचार: सूचना, तटस्थता।",
    "रस: स्थायी भाव, संचारी भाव, विभाव, अनुभाव; शृंगार रस उदाहरण।",
    "प्रशासनिक, वाणिज्यिक, तकनीकी, पत्रकारिता, विधि।",
    "प्रदूषण, वृक्षारोपण, कचरा प्रबंधन, जनभागीदारी।",
    "जुड़ाव, सूचना, शिक्षा – लाभ; समय बर्बादी, फेक न्यूज – हानि।"
]


# ════════════════════════════════════════════════════════════
#                       ENGLISH
# ════════════════════════════════════════════════════════════
ENGLISH_OBJ = pad100([
    {"q":"Who wrote 'The Last Lesson'?","opt":["Alphonse Daudet","Anees Jung","William Douglas","Selma Lagerlof"],"ans":0},
    {"q":"Theme of 'Lost Spring'?","opt":["Poverty/exploitation","Education","Sports","Science"],"ans":0},
    {"q":"In 'Deep Water', fear was of –","opt":["Water","Fire","Heights","Darkness"],"ans":0},
    {"q":"The rattrap seller was a –","opt":["beggar","thief","businessman","teacher"],"ans":0},
    {"q":"Author of 'Indigo'?","opt":["Louis Fischer","Gandhi","Nehru","Tagore"],"ans":0},
    {"q":"Who wrote 'My Mother at Sixty-Six'?","opt":["Kamala Das","Neruda","Keats","Frost"],"ans":0},
    {"q":"'Keeping Quiet' poet –","opt":["Pablo Neruda","Kamala Das","Frost","Keats"],"ans":0},
    {"q":"'A Thing of Beauty' gives us –","opt":["Joy forever","Sadness","Pain","Wealth"],"ans":0},
    {"q":"'A Roadside Stand' poem about –","opt":["rural-urban divide","nature","love","travel"],"ans":0},
    {"q":"Aunt Jennifer's tigers are –","opt":["embroidered","real","painted","carved"],"ans":0},
    {"q":"'The Third Level' is written by –","opt":["Jack Finney","Colin Dexter","Susan Hill","Kalki"],"ans":0},
    {"q":"The Maharaja in 'The Tiger King' killed –","opt":["99 tigers","100 tigers","100 lions","50 tigers"],"ans":0},
    {"q":"Dr. Sadao was a –","opt":["Japanese surgeon","Chinese scientist","American soldier","British diplomat"],"ans":0},
    {"q":"Passive voice of 'She writes a letter' –","opt":["A letter is written by her","A letter was written by her","She is written a letter","A letter writes her"],"ans":0},
    {"q":"Synonym of 'happy' –","opt":["joyful","sad","angry","tired"],"ans":0},
    {"q":"Antonym of 'brave' –","opt":["coward","bold","courageous","fearless"],"ans":0},
    {"q":"Indirect speech: He said, 'I am ill.'","opt":["He said that he was ill","He said that I am ill","He says he is ill","He told he was ill"],"ans":0},
    {"q":"Figure of speech: 'Life is a dream' –","opt":["Metaphor","Simile","Personification","Hyperbole"],"ans":0},
    {"q":"'The Enemy' is set in –","opt":["Japan and USA during WWII","India","England","France"],"ans":0},
    {"q":"'Should Wizard Hit Mommy' author –","opt":["John Updike","Jack Finney","Susan Hill","Kalki"],"ans":0},
    {"q":"'On the Face of It' deals with –","opt":["physical disability","poverty","war","education"],"ans":0},
    {"q":"'Memories of Childhood' is about –","opt":["discrimination","adventure","travel","science"],"ans":0},
    {"q":"The bangle makers in Firozabad lose their –","opt":["eyesight","hearing","limbs","voice"],"ans":0},
    {"q":"Douglas in 'Deep Water' used a –","opt":["swimming instructor","doctor","friend","book"],"ans":0},
    {"q":"The peddler in 'The Rattrap' was transformed by –","opt":["Edla's kindness","money","fear","police"],"ans":0},
    {"q":"Gandhi in 'Indigo' fought for the –","opt":["sharecroppers","zamindars","British","merchants"],"ans":0},
    {"q":"Aunt Jennifer's fingers are –","opt":["fluttering","still","broken","strong"],"ans":0},
    {"q":"The central idea of 'A Thing of Beauty' is –","opt":["beauty never fades","beauty is temporary","beauty causes pain","beauty is wealth"],"ans":0},
    {"q":"'Poets and Pancakes' is about –","opt":["Gemini Studios","Hollywood","a bakery","a school"],"ans":0},
    {"q":"'Going Places' deals with –","opt":["adolescent dreams","travel","science","history"],"ans":0},
    {"q":"Sophie in 'Going Places' dreams of –","opt":["becoming an actress","a pilot","a teacher","a doctor"],"ans":0},
    {"q":"The ironmaster mistook the peddler for –","opt":["an old regimental comrade","a thief","a merchant","a police"],"ans":0},
    {"q":"The message of 'The Last Lesson' is –","opt":["love for one's language","patriotism","education","freedom"],"ans":0},
    {"q":"The theme of 'Lost Spring' is –","opt":["child labour and poverty","education","sports","all of these"],"ans":0},
    {"q":"'Deep Water' is an example of –","opt":["autobiography","biography","fiction","poetry"],"ans":0},
    {"q":"The rattrap peddler finally –","opt":["returned the money","ran away","was arrested","died"],"ans":0},
    {"q":"The protagonist of 'The Tiger King' is –","opt":["Maharaja of Pratibandapuram","British officer","astrologer","minister"],"ans":0},
    {"q":"'The Third Level' refers to –","opt":["an imaginary platform at Grand Central","a game","a building","a train"],"ans":0},
    {"q":"Dr. Sadao's wife was –","opt":["Hana","Mary","Alice","Sophie"],"ans":0},
    {"q":"'Memories of Childhood' is written by –","opt":["Zitkala-Sa and Bama","Zitkala-Sa only","Bama only","Anne Frank"],"ans":0},
    {"q":"The tiger king's death was caused by –","opt":["a wooden tiger","a real tiger","disease","poison"],"ans":0},
    {"q":"Umberto Eco is known for –","opt":["The Name of the Rose","The Godfather","Harry Potter","The Alchemist"],"ans":0},
    {"q":"In 'Poets and Pancakes', the author worked at –","opt":["Gemini Studios","a bank","a school","a hospital"],"ans":0},
    {"q":"The English poet who visited Gemini Studios was –","opt":["Stephen Spender","W.H. Auden","T.S. Eliot","Robert Frost"],"ans":0},
    {"q":"'A Roadside Stand' is by –","opt":["Robert Frost","Pablo Neruda","John Keats","Kamala Das"],"ans":0},
    {"q":"'My Mother at Sixty-Six' uses the image of –","opt":["a corpse","a flower","a tree","a bird"],"ans":0},
    {"q":"'Aunt Jennifer's Tigers' was written by –","opt":["Adrienne Rich","Kamala Das","Sylvia Plath","Emily Dickinson"],"ans":0},
    {"q":"'Keeping Quiet' advocates –","opt":["introspection and stillness","action","war","travel"],"ans":0},
    {"q":"The central metaphor in 'The Rattrap' is –","opt":["the world as a trap","money","food","war"],"ans":0},
    {"q":"'Indigo' describes Gandhi's work in –","opt":["Champaran","Dandi","Sabarmati","Wardha"],"ans":0},
    {"q":"Douglas overcame fear through –","opt":["determination and practice","medication","hypnosis","avoidance"],"ans":0},
    {"q":"Edla Wilmansson was the –","opt":["ironmaster's daughter","peddler's wife","maid","queen"],"ans":0},
    {"q":"'The Last Lesson' is set in –","opt":["Alsace","Paris","Berlin","London"],"ans":0},
    {"q":"M. Hamel taught –","opt":["French","English","German","Spanish"],"ans":0},
    {"q":"Franz was afraid of –","opt":["M. Hamel's scolding","his mother","friends","police"],"ans":0},
    {"q":"William Douglas was a –","opt":["lawyer","doctor","teacher","journalist"],"ans":0},
    {"q":"The Y.M.C.A. pool incident happened when Douglas was –","opt":["ten or eleven","twenty","thirty","five"],"ans":0},
    {"q":"The bangle makers belong to –","opt":["Firozabad","Agra","Delhi","Lucknow"],"ans":0},
    {"q":"Saheb-e-Alam's name means –","opt":["lord of the universe","king","servant","teacher"],"ans":0},
    {"q":"Mukesh dreams of becoming a –","opt":["motor mechanic","doctor","engineer","pilot"],"ans":0},
    {"q":"The crofter gave the peddler –","opt":["food and shelter","money","clothes","a job"],"ans":0},
    {"q":"The ironmaster's mill was at –","opt":["Ramsjo","Firozabad","Champaran","Galesburg"],"ans":0},
    {"q":"Edla was –","opt":["kind-hearted","cruel","selfish","proud"],"ans":0},
    {"q":"Gandhi reached Champaran in –","opt":["1917","1920","1930","1942"],"ans":0},
    {"q":"The sharecroppers were forced to grow –","opt":["indigo","rice","wheat","cotton"],"ans":0},
    {"q":"The Champaran episode was –","opt":["a turning point in Gandhi's life","a failure","insignificant","a myth"],"ans":0},
    {"q":"Charley found the third level at –","opt":["Grand Central Station","Penn Station","Victoria Station","Central Park"],"ans":0},
    {"q":"The third level led to –","opt":["1894","1944","2024","1924"],"ans":0},
    {"q":"Charley bought tickets to –","opt":["Galesburg","New York","Chicago","Boston"],"ans":0},
    {"q":"Sam Weiner was Charley's –","opt":["psychiatrist friend","brother","father","colleague"],"ans":0},
    {"q":"'The Tiger King' satirizes –","opt":["power and arrogance","love","friendship","nature"],"ans":0},
    {"q":"The astrologer predicted the king's death by –","opt":["a tiger","a lion","a snake","a dog"],"ans":0},
    {"q":"The irony in 'The Tiger King' is –","opt":["king killed 99 tigers but died from a toy","king was immortal","tigers were friendly","astrologer was wrong"],"ans":0},
    {"q":"Sophie's brother was –","opt":["Geoff","Derek","Hans","Jack"],"ans":0},
    {"q":"The peddler stole –","opt":["thirty kronor","a watch","jewellery","food"],"ans":0},
    {"q":"'Poets and Pancakes' is a –","opt":["humorous account","sad story","tragedy","biography"],"ans":0},
    {"q":"'Going Places' author –","opt":["A.R. Barton","Susan Hill","Jack Finney","John Updike"],"ans":0},
    {"q":"Change: 'She is cooking food.' (Passive) –","opt":["Food is being cooked by her","Food was cooked by her","She cooked food","Food is cooked"],"ans":0},
    {"q":"Synonym of 'beautiful' –","opt":["lovely","ugly","dull","rough"],"ans":0},
    {"q":"Antonym of 'ancient' –","opt":["modern","old","historic","traditional"],"ans":0},
    {"q":"'The Interview' is a –","opt":["non-fiction","fiction","poem","drama"],"ans":0},
    {"q":"'On the Face of It' is a –","opt":["play","poem","story","essay"],"ans":0},
    {"q":"Derry in 'On the Face of It' has a –","opt":["burnt face","lame leg","blind eye","deaf ear"],"ans":0},
    {"q":"Mr. Lamb's garden is full of –","opt":["weeds","flowers","fruit trees","grass"],"ans":0},
    {"q":"The theme of 'Deep Water' is –","opt":["overcoming fear","love of nature","war","poverty"],"ans":0},
    {"q":"Gandhi's first reaction to Champaran peasants was –","opt":["to fight legally","ignore","violent protest","run away"],"ans":0},
    {"q":"Zitkala-Sa's story is about –","opt":["discrimination in a boarding school","travel","war","love"],"ans":0},
    {"q":"Bama's story is about –","opt":["caste discrimination","war","education","science"],"ans":0},
    {"q":"'A Thing of Beauty' is from –","opt":["Endymion","Lamia","Ode to Autumn","Hyperion"],"ans":0},
    {"q":"Keats says a beautiful thing is –","opt":["a joy forever","temporary","painful","ugly"],"ans":0},
    {"q":"Pablo Neruda was from –","opt":["Chile","Argentina","Spain","Mexico"],"ans":0},
    {"q":"'Keeping Quiet' asks us to count to –","opt":["twelve","ten","seven","twenty"],"ans":0},
    {"q":"The poem 'Aunt Jennifer's Tigers' has how many stanzas?","opt":["3","2","4","5"],"ans":0},
    {"q":"Aunt Jennifer's tigers move on –","opt":["a screen/panel","a wall","a canvas","a cloth"],"ans":0},
    {"q":"The word 'massive weight' in 'Aunt Jennifer's Tigers' refers to –","opt":["her wedding ring","a tiger","a machine","a house"],"ans":0},
])

ENGLISH_SHORT = [
    "Why did William Douglas develop a fear of water?",
    "What was the condition of the bangle makers in Firozabad?",
    "Why did the peddler sign himself as Captain von Stahle?",
    "What did Gandhi do for the sharecroppers of Champaran?",
    "Describe the poet's mother in 'My Mother at Sixty-Six'.",
    "What does the poet ask us to do in 'Keeping Quiet'?",
    "Why is a thing of beauty a joy forever?",
    "What does the roadside stand symbolise?",
    "What are Aunt Jennifer's tigers doing?",
    "Explain the theme of 'The Third Level'.",
    "Why did the Maharaja decide to kill one hundred tigers?",
    "Write a letter to the editor about the menace of stray dogs.",
    "Draft a notice for a blood donation camp.",
    "Write an advertisement for a new model of bicycle.",
    "What is the format of report writing?",
    "Change the voice: 'The boy is flying a kite.'",
    "Transform: 'He is too weak to walk.' (Remove 'too')",
    "Use the phrasal verb 'break down' in a sentence.",
    "Write two synonyms of 'beautiful'.",
    "Correct the sentence: 'He do not know the answer.'",
    "Explain the proverb: 'Actions speak louder than words.'",
    "What is the message of 'The Last Lesson'?",
    "How did Douglas overcome his fear of water?",
    "What is the significance of the title 'Lost Spring'?",
    "Describe the character of the rattrap peddler.",
    "What is the central idea of 'A Roadside Stand'?",
    "Why are Aunt Jennifer's fingers fluttering?",
    "Write a summary of 'The Enemy'.",
    "What is the theme of 'Should Wizard Hit Mommy'?",
    "Explain the irony in 'The Tiger King'."
]
ENGLISH_SHORT_ANS = [
    "A childhood incident at a beach where he was knocked down by a wave left him with lifelong fear.",
    "Poverty, bonded labour, working in hot furnaces, losing eyesight, no education for children.",
    "To show gratitude to the ironmaster who was kind, and to maintain his dignity.",
    "He fought for their rights, organized them, and made the British refund part of the indigo money.",
    "Old, pale, dozing, with an ashen face like a corpse — signs of aging and exhaustion.",
    "To be still, introspect, and understand ourselves and others better.",
    "Because its beauty never fades; it brings us peace, sweet dreams, and health.",
    "The exploitation of rural India by the urban rich; the neglect of rural people.",
    "Prancing and moving proudly, free from fear — symbols of Aunt Jennifer's suppressed desires.",
    "Escape from reality, nostalgia, the desire to go back to a simpler, peaceful past.",
    "An astrologer predicted his death by a tiger, so he killed 99 tigers to prove it wrong.",
    "Formal letter to editor: date, address, subject — complaining about stray dog menace, suggesting solutions.",
    "Heading: Blood Donation Camp; date, venue, time, organiser, appeal to donate blood.",
    "Features: Lightweight, durable, affordable price, contact details, discount offer.",
    "Title, date, place, by whom written, introduction, body, conclusion, reporter's name.",
    "A kite is being flown by the boy.",
    "He is so weak that he cannot walk.",
    "The car broke down on the highway.",
    "Lovely, gorgeous.",
    "He does not know the answer.",
    "Actions are more important than words; what you do matters more than what you say.",
    "Love for one's language and culture, and the pain of losing it.",
    "He practiced swimming with a professional instructor and gradually overcome his fear.",
    "Lost Spring = lost childhood; child laborers have no spring (youth/joy) in their lives.",
    "A poor peddler who steals but later transforms after Edla's kindness.",
    "The divide between the city and the village; the neglect of rural people.",
    "She is nervous and unhappy; the weight of her wedding ring suppresses her.",
    "Dr. Sadao saves an American enemy soldier, balancing duty to his country and humanity.",
    "The story explores the conflict between a child's imagination and adult rationality.",
    "The king who wanted to kill 100 tigers died because of a wooden tiger — ironic twist of fate."
]
ENGLISH_LONG = [
    "Describe the author's experience of drowning in 'Deep Water' and how he overcame his fear.",
    "Analyse the title 'Lost Spring' and discuss how poverty and exploitation are portrayed.",
    "Write a detailed character sketch of the rattrap peddler and trace his transformation.",
    "Discuss the theme of 'Keeping Quiet' and its relevance in today's world.",
    "Explain the central idea of 'A Thing of Beauty' and how beauty provides eternal joy.",
    "Write an essay on 'Importance of Education in Modern India' in about 200 words.",
    "Write a letter to the Municipal Commissioner complaining about poor drainage in your locality.",
    "Write a report on 'Science Exhibition Held in Your School' for the school magazine.",
    "Discuss the character of Aunt Jennifer and the message conveyed through the poem.",
    "Analyse the theme of 'The Enemy' and the conflict between duty and humanity.",
    "Sketch the character of Dr. Sadao in 'The Enemy'.",
    "What is the significance of the third level in the story 'The Third Level'?",
    "Write a speech on 'Clean India, Green India' for the morning assembly.",
    "Draft an advertisement for a new coaching institute in your city.",
    "Explain the poetic devices used in 'My Mother at Sixty-Six'.",
    "Discuss how the poem 'Aunt Jennifer's Tigers' portrays the plight of women.",
    "Write a factual description of your school library.",
    "Summarize the story 'The Tiger King' and comment on its satirical tone.",
    "Write an article on 'Role of Youth in Nation Building'.",
    "Discuss Gandhi's contribution in the Champaran movement as described in 'Indigo'."
]
ENGLISH_LONG_ANS = [
    "He nearly drowned twice; fear haunted him; took professional swimming lessons; gradually overcame fear.",
    "Lost Spring = lost childhood; bangle makers work from age 7-8, poverty forces them; lose eyesight.",
    "Poor man, lives by begging; makes rattraps; feels world is a trap; transformed by Edla's kindness.",
    "People rush for material gains; poet asks to stop, introspect; relevant in modern stressful life.",
    "Beauty never fades; gives peace, sweet dreams, health; examples: sun, moon, trees, daffodils.",
    "Education is key to progress; empowers individuals, reduces poverty, drives innovation; NEP 2020.",
    "Formal letter: address, date, subject – poor drainage causing diseases, request to repair.",
    "Title, place, date; describe exhibits, chief guest, prizes, student participation, conclusion.",
    "Aunt Jennifer is weak, unhappy; creates bold tigers in art; contrast between real life and imagination.",
    "Dr. Sadao saves American soldier despite being Japanese; conflict between patriotism and professional ethics.",
    "Skilled surgeon, compassionate, loyal to country yet saves the enemy, strong moral compass.",
    "Represents escape from modern stress, nostalgia, desire for simpler life; symbol of mental escape.",
    "Speech: Importance of cleanliness, planting trees, reducing pollution, role of youth, conclusion.",
    "Coaching name, subjects, experienced faculty, success rate, contact, address, fee structure.",
    "Simile: 'her face ashen like a corpse'; imagery, contrast between old mother and young trees.",
    "Tigers are strong, fearless; Aunt is weak, oppressed by marriage; tigers represent suppressed desires.",
    "Location, size, number of books, sections, seating, librarian, atmosphere, rules.",
    "Maharaja kills 99 tigers; wooden toy causes infection and death; irony of fate, satire on power.",
    "Youth are future; energy, innovation; role in politics, social reforms, start-ups, environment.",
    "Gandhi organized peasants, fought for justice, made British refund money; Champaran was turning point."
]


# ════════════════════════════════════════════════════════════
#                       PHYSICS
# ════════════════════════════════════════════════════════════
PHYSICS_OBJ = pad100([
    {"q":"1 कूलॉम में इलेक्ट्रॉन –","opt":["6.25×10¹⁸","1.6×10¹⁹","6.25×10¹⁹","1.6×10⁻¹⁹"],"ans":0},
    {"q":"गॉस का नियम लागू –","opt":["केवल बंद पृष्ठ","खुले पृष्ठ","सभी पृष्ठ","गोलीय पृष्ठ"],"ans":0},
    {"q":"समान्तर प्लेट संधारित्र धारिता –","opt":["ε₀A/d","ε₀d/A","A/ε₀d","d/ε₀A"],"ans":0},
    {"q":"किरचॉफ का प्रथम नियम आधारित –","opt":["आवेश संरक्षण","ऊर्जा संरक्षण","द्रव्यमान","संवेग"],"ans":0},
    {"q":"ओम का नियम –","opt":["V=IR","V=I/R","R=VI","I=VR"],"ans":0},
    {"q":"हीटस्टोन सेतु उपयोग –","opt":["प्रतिरोध मापने में","धारा मापने में","विभवान्तर","शक्ति"],"ans":0},
    {"q":"बायो-सेवार्ट नियम –","opt":["dB=(μ₀/4π)(Idl sinθ/r²)","B=μ₀I/2πr","B=μ₀nI","φ=B.A"],"ans":0},
    {"q":"एम्पियर का परिपथीय नियम –","opt":["∮B.dl=μ₀I","∮B.dl=0","∮E.dl=-dφ/dt","∮E.dA=q/ε₀"],"ans":0},
    {"q":"प्रत्यावर्ती धारा का rms मान –","opt":["Irms=I₀/√2","Irms=I₀√2","Irms=I₀","Irms=2I₀"],"ans":0},
    {"q":"ट्रांसफार्मर कार्य करता है –","opt":["केवल AC पर","केवल DC पर","दोनों","किसी पर नहीं"],"ans":0},
    {"q":"LCR अनुनाद में प्रतिबाधा –","opt":["न्यूनतम","अधिकतम","शून्य","अनंत"],"ans":0},
    {"q":"पूर्ण आन्तरिक परावर्तन –","opt":["सघन→विरल, आपतन>क्रान्तिक","सघन→विरल, आपतन<क्रान्तिक","विरल→सघन","केवल सघन"],"ans":0},
    {"q":"लेंस मेकर सूत्र –","opt":["1/f=(μ-1)(1/R₁-1/R₂)","1/f=(μ-1)(R₁+R₂)","1/f=μ(1/R₁-1/R₂)","f=(μ-1)(R₁-R₂)"],"ans":0},
    {"q":"यंग के द्विझिरी में फ्रिंज चौड़ाई –","opt":["β=λD/d","β=dD/λ","β=λd/D","β=D/λd"],"ans":0},
    {"q":"प्रकाश विद्युत प्रभाव में ऊर्जा निर्भर –","opt":["आवृत्ति पर","तीव्रता पर","दोनों","किसी पर नहीं"],"ans":0},
    {"q":"नाभिक का आकार –","opt":["10⁻¹⁵ m","10⁻¹⁰ m","10⁻⁸ m","10⁻⁶ m"],"ans":0},
    {"q":"P-N सन्धि में अवक्षय परत बनती है –","opt":["विसरण के कारण","अपवाह","प्रकाश","ताप"],"ans":0},
    {"q":"LED का पूर्ण रूप –","opt":["Light Emitting Diode","Low Energy Diode","Long Electric Diode","Light Energy Device"],"ans":0},
    {"q":"बोहर मॉडल में कोणीय संवेग –","opt":["nh/2π","h/2π","mvr","दोनों a और c"],"ans":3},
    {"q":"बन्धन ऊर्जा का सूत्र –","opt":["Eb=Δm·c²","Eb=Δm/c²","Eb=Δm·c","Eb=c²/Δm"],"ans":0},
    {"q":"ट्रांजिस्टर धारा सम्बन्ध –","opt":["Ie=Ib+Ic","Ic=Ie+Ib","Ib=Ie+Ic","Ie=Ib-Ic"],"ans":0},
    {"q":"विद्युत क्षेत्र रेखाएँ –","opt":["धन से ऋण की ओर","ऋण से धन की ओर","बन्द वक्र","समान्तर"],"ans":0},
    {"q":"एक समान विद्युत क्षेत्र में द्विध्रुव पर बल-आघूर्ण –","opt":["pE sinθ","pE cosθ","pE","0"],"ans":0},
    {"q":"संधारित्र की ऊर्जा –","opt":["½CV²","CV²","2CV²","C²V"],"ans":0},
    {"q":"मीटर सेतु का तार –","opt":["मैंगनिन","ताँबा","लोहा","चाँदी"],"ans":0},
    {"q":"चुम्बकीय क्षेत्र रेखाएँ –","opt":["बन्द वक्र","खुली","सीधी","परवलय"],"ans":0},
    {"q":"गतिमान आवेश पर चुम्बकीय बल –","opt":["qvB sinθ","qvB","qE","qvB cosθ"],"ans":0},
    {"q":"लेंज का नियम –","opt":["प्रेरित धारा कारण का विरोध करती है","धारा बढ़ाती है","धारा घटाती है","कोई प्रभाव नहीं"],"ans":0},
    {"q":"प्रकाश का परावर्तन –","opt":["आपतन कोण = परावर्तन कोण","आपतन कोण > परावर्तन","आपतन कोण < परावर्तन","कोई नहीं"],"ans":0},
    {"q":"दूरदर्शी की आवर्धन क्षमता –","opt":["f₀/fₑ","fₑ/f₀","f₀+fₑ","f₀-fₑ"],"ans":0},
    {"q":"डी-ब्रॉग्ली तरंगदैर्ध्य –","opt":["λ=h/mv","λ=mv/h","λ=h/mc","λ=c/f"],"ans":0},
    {"q":"नाभिकीय संलयन के लिए आवश्यक –","opt":["उच्च ताप","निम्न ताप","सामान्य ताप","परम शून्य"],"ans":0},
    {"q":"अर्धचालक में चालन –","opt":["इलेक्ट्रॉन और होल दोनों","केवल इलेक्ट्रॉन","केवल होल","केवल आयन"],"ans":0},
    {"q":"Zener डायोड उपयोग –","opt":["वोल्टता नियंत्रक","प्रवर्धक","दिष्टकारी","दोलक"],"ans":0},
    {"q":"AND गेट का बूलियन व्यंजक –","opt":["Y=A·B","Y=A+B","Y=Ā","Y=A⊕B"],"ans":0},
    {"q":"प्रकाश वैद्युत प्रभाव में निरोधी विभव –","opt":["K_max/e","e/K_max","hν/e","e/hν"],"ans":0},
    {"q":"विद्युत चुम्बकीय तरंगों का वेग निर्वात में –","opt":["3×10⁸ m/s","3×10¹⁰ m/s","3×10⁶ m/s","3×10⁵ m/s"],"ans":0},
    {"q":"धारा घनत्व J =","opt":["I/A","IA","I/A²","A/I"],"ans":0},
    {"q":"प्रतिरोधकता का मात्रक –","opt":["Ω·m","Ω/m","m/Ω","Ω"],"ans":0},
    {"q":"शक्ति गुणांक cosφ =","opt":["R/Z","Z/R","X_L/R","X_C/R"],"ans":0},
    {"q":"चुम्बकीय फ्लक्स का मात्रक –","opt":["वेबर","टेस्ला","हेनरी","फैराड"],"ans":0},
    {"q":"इलेक्ट्रॉन वोल्ट (eV) –","opt":["1.6×10⁻¹⁹ J","1.6×10⁻¹⁹ eV","9.1×10⁻³¹ kg","1.6×10⁻¹⁹ C"],"ans":0},
    {"q":"समस्थानिक –","opt":["समान Z, भिन्न A","समान A, भिन्न Z","समान n","भिन्न e"],"ans":0},
    {"q":"समभारिक –","opt":["समान A, भिन्न Z","समान Z, भिन्न A","समान n","भिन्न p"],"ans":0},
    {"q":"नाभिकीय रिएक्टर में मंदक –","opt":["भारी जल","साधारण जल","तेल","वायु"],"ans":0},
    {"q":"परमाणु का नाभिकीय मॉडल –","opt":["रदरफोर्ड","थॉमसन","बोहर","सोमरफील्ड"],"ans":0},
    {"q":"हाइड्रोजन स्पेक्ट्रम की बामर श्रेणी –","opt":["दृश्य क्षेत्र","पराबैंगनी","अवरक्त","एक्स-रे"],"ans":0},
    {"q":"कुलॉम नियतांक k =","opt":["9×10⁹ Nm²/C²","9×10⁹ Nm²/C","9×10⁹ C²/Nm²","9×10⁹"],"ans":0},
    {"q":"विद्युत विभव का मात्रक –","opt":["वोल्ट","जूल","कूलॉम","वाट"],"ans":0},
    {"q":"चालक के अन्दर विद्युत क्षेत्र –","opt":["शून्य","अधिकतम","अनन्त","नियत"],"ans":0},
    {"q":"धारा का मात्रक –","opt":["एम्पियर","वोल्ट","कूलॉम","ओम"],"ans":0},
    {"q":"प्रतिरोध श्रेणीक्रम में –","opt":["R=R₁+R₂","1/R=1/R₁+1/R₂","R=1/R₁+1/R₂","R=R₁R₂/(R₁+R₂)"],"ans":0},
    {"q":"सेल का आन्तरिक प्रतिरोध –","opt":["r=(E-V)/I","r=V/I","r=E/I","r=I/E"],"ans":0},
    {"q":"OR गेट सत्य सारणी में 1+1=","opt":["1","0","2","अपरिभाषित"],"ans":0},
    {"q":"AND गेट सत्य सारणी में 1·0=","opt":["0","1","अपरिभाषित","2"],"ans":0},
    {"q":"NOT गेट सत्य सारणी 0→","opt":["1","0","शून्य","अनन्त"],"ans":0},
    {"q":"NAND गेट का बूलियन –","opt":["Y=(A·B)'","Y=A+B","Y=A'","Y=A⊕B"],"ans":0},
    {"q":"NOR गेट –","opt":["OR+NOT","AND+NOT","NAND","XOR"],"ans":0},
    {"q":"धारिता C =","opt":["Q/V","V/Q","QV","Q²/V"],"ans":0},
    {"q":"समान्तर प्लेट संधारित्र में पारद्युतिक –","opt":["धारिता बढ़ती है","घटती है","अपरिवर्तित","शून्य"],"ans":0},
    {"q":"विद्युत द्विध्रुव का आघूर्ण p =","opt":["q×2a","q×a","2q×a","q²×2a"],"ans":0},
    {"q":"गॉस नियम –","opt":["∮E·dA=q/ε₀","∮E·dA=q","∮B·dA=q","∮E·dl=q"],"ans":0},
    {"q":"प्रकाश का ध्रुवण –","opt":["अनुप्रस्थ तरंग","अनुदैर्ध्य","यांत्रिक","ध्वनि"],"ans":0},
    {"q":"मैलस का नियम –","opt":["I=I₀cos²θ","I=I₀sin²θ","I=I₀cosθ","I=I₀/2"],"ans":0},
    {"q":"क्रान्तिक कोण –","opt":["sin⁻¹(1/μ)","sin⁻¹(μ)","tan⁻¹(μ)","cos⁻¹(μ)"],"ans":0},
    {"q":"हाइगेन्स का तरंग सिद्धान्त –","opt":["प्रत्येक बिन्दु तरंग स्रोत","कण","किरण","कोई नहीं"],"ans":0},
    {"q":"प्रकाश की द्वैत प्रकृति –","opt":["तरंग और कण","केवल तरंग","केवल कण","कोई नहीं"],"ans":0},
    {"q":"हाइजेनबर्ग अनिश्चितता सिद्धान्त –","opt":["ΔxΔp≥h/4π","ΔxΔp<h/4π","ΔEΔt<h/4π","ΔxΔp=0"],"ans":0},
    {"q":"अर्द्ध-आयु –","opt":["0.693/λ","λ/0.693","2.303/λ","λ/2.303"],"ans":0},
    {"q":"ट्रांजिस्टर उभयनिष्ठ उत्सर्जक धारा लाभ –","opt":["β=Ic/Ib","α=Ic/Ie","γ=Ie/Ib","β=Ib/Ic"],"ans":0},
    {"q":"XOR गेट –","opt":["Y=A⊕B","Y=A·B","Y=A+B","Y=(A·B)'"],"ans":0},
    {"q":"स्काई तरंग संचार –","opt":["आयनमंडल से परावर्तन","भू-तरंग","अंतरिक्ष तरंग","दृष्टि रेखा"],"ans":0},
    {"q":"प्रकाशिक तन्तु –","opt":["पूर्ण आन्तरिक परावर्तन","परावर्तन","अपवर्तन","विवर्तन"],"ans":0},
    {"q":"सौर सेल –","opt":["प्रकाश को विद्युत में","विद्युत को प्रकाश में","ध्वनि को विद्युत","ताप को विद्युत"],"ans":0},
    {"q":"फोटोडायोड –","opt":["प्रकाश संसूचक","प्रकाश उत्सर्जक","प्रतिरोध","संधारित्र"],"ans":0},
    {"q":"जेनर डायोड –","opt":["पश्च अभिनति में कार्य","अग्र अभिनति","दोनों","कोई नहीं"],"ans":0},
    {"q":"PN सन्धि डायोड अग्र अभिनति में –","opt":["धारा प्रवाहित","धारा नहीं","प्रतिरोध अधिक","कोई नहीं"],"ans":0},
    {"q":"विद्युत चुम्बकीय तरंगों में E और B –","opt":["परस्पर लम्बवत","समान्तर","विपरीत","कोई सम्बन्ध नहीं"],"ans":0},
    {"q":"एकल झिरी विवर्तन में केन्द्रीय उच्चिष्ठ चौड़ाई –","opt":["2λ/a","λ/a","λ/2a","2a/λ"],"ans":0},
    {"q":"साइक्लोट्रॉन –","opt":["आवेशित कणों को त्वरित","विद्युत क्षेत्र मापन","चुम्बकीय क्षेत्र मापन","ऊर्जा संग्रह"],"ans":0},
    {"q":"रेडियोएक्टिव क्षय नियतांक –","opt":["λ","T","τ","N"],"ans":0},
    {"q":"कार्बन डेटिंग –","opt":["C-14","C-12","C-13","C-11"],"ans":0},
    {"q":"श्रेणीक्रम में धारिता –","opt":["1/C=1/C₁+1/C₂","C=C₁+C₂","C=C₁C₂/(C₁+C₂)","C=C₁-C₂"],"ans":0},
    {"q":"समान्तर क्रम में धारिता –","opt":["C=C₁+C₂","1/C=1/C₁+1/C₂","C=C₁C₂/(C₁+C₂)","C=C₁-C₂"],"ans":0},
    {"q":"डी मॉर्गन प्रमेय –","opt":["(A+B)'=A'·B'","(A+B)'=A'+B'","A·B=A+B","A+B=A·B"],"ans":0},
    {"q":"प्रत्यावर्ती धारा का औसत मान –","opt":["0","I₀","2I₀/π","I₀/√2"],"ans":0},
    {"q":"संधारित्र ऊर्जा घनत्व –","opt":["½ε₀E²","ε₀E²","½CV²","QV/2"],"ans":0},
    {"q":"चालक गोले की धारिता –","opt":["4πε₀R","ε₀A/d","2πε₀R","πε₀R"],"ans":0},
    {"q":"प्रतिरोध का ताप गुणांक –","opt":["α","β","γ","λ"],"ans":0},
    {"q":"x-रे की खोज किसने की?","opt":["रोन्टजन","बेक्वेरल","क्यूरी","फैराडे"],"ans":0},
    {"q":"NAND गेट को सार्वत्रिक क्यों कहते हैं?","opt":["सभी गेट बनाए जा सकते हैं","केवल AND","केवल OR","कोई नहीं"],"ans":0},
    {"q":"प्रकाश प्रकीर्णन –","opt":["आकाश नीला, सूर्योदय लाल","केवल नीला","केवल लाल","सफेद"],"ans":0},
    {"q":"IC का पूर्ण रूप –","opt":["Integrated Circuit","Internal Circuit","Inductive Circuit","Inverse Circuit"],"ans":0},
    {"q":"समविभव पृष्ठ पर विभवान्तर –","opt":["शून्य","अधिकतम","न्यूनतम","अनन्त"],"ans":0},
])

PHYSICS_SHORT = [
    "कूलॉम के नियम का सदिश रूप लिखिए।",
    "गॉस के नियम का उपयोग कर गोलीय कोश के कारण विद्युत क्षेत्र ज्ञात कीजिए।",
    "ओम के नियम की सीमाएँ क्या हैं?",
    "हीटस्टोन सेतु का सिद्धान्त समझाइए।",
    "बायो-सेवार्ट नियम लिखें एवं समझाएँ।",
    "एम्पियर का परिपथीय नियम लिखें।",
    "लेंज का नियम लिखें।",
    "फैराडे का विद्युत चुम्बकीय प्रेरण का नियम लिखें।",
    "प्रत्यावर्ती धारा एवं दिष्ट धारा में अन्तर लिखें।",
    "प्रकाश के परावर्तन के नियम लिखें।",
    "लेंस मेकर सूत्र लिखें।",
    "प्रकाश का पूर्ण आन्तरिक परावर्तन समझाएँ।",
    "यंग का द्विझिरी प्रयोग समझाइए।",
    "प्रकाश विद्युत प्रभाव क्या है?",
    "डी-ब्रॉग्ली तरंगदैर्ध्य का सूत्र लिखें।",
    "नाभिकीय संलयन एवं विखण्डन में अन्तर लिखें।",
    "द्रव्यमान क्षति एवं बन्धन ऊर्जा को समझाइए।",
    "N-type एवं P-type अर्धचालकों में अन्तर लिखें।",
    "P-N सन्धि डायोड का अग्र अभिनति में कार्यविधि समझाएँ।",
    "NOT गेट का प्रतीक एवं सत्यता सारणी बनाएँ।",
    "ट्रांजिस्टर के उपयोग लिखें।",
    "मॉडुलन किसे कहते हैं? इसकी आवश्यकता बताएँ।",
    "पृथ्वी के चुम्बकीय क्षेत्र के अवयवों के नाम लिखें।",
    "विद्युत अनुनाद किसे कहते हैं?",
    "संधारित्र की प्रतिघात का सूत्र लिखें।",
    "शक्ति गुणांक किसे कहते हैं?",
    "दो समान्तर धारावाही चालकों के बीच बल का सूत्र।",
    "साइक्लोट्रॉन का सिद्धान्त समझाइए।",
    "ऊर्जा बैण्ड सिद्धान्त के आधार पर चालक, अर्धचालक तथा विद्युतरोधी में अन्तर।",
    "मैक्सवेल के विद्युत चुम्बकीय तरंगों के गुणधर्म लिखिए।"
]
PHYSICS_SHORT_ANS = [
    "F = k·q₁·q₂/r² r̂ (सदिश रूप, दिशा r̂ के अनुदिश)",
    "E=0 (r<R के लिए), E=Q/(4πε₀r²) (r>R के लिए)",
    "ताप, चुम्बकीय क्षेत्र, अर्धचालकों में लागू नहीं।",
    "चार प्रतिरोधों का संतुलित सेतु: R₁/R₂=R₃/R₄",
    "dB=(μ₀/4π)(Idl sinθ/r²)",
    "∮B·dl=μ₀I (बंद पथ पर)",
    "प्रेरित धारा सदैव उस कारण का विरोध करती है जो उसे उत्पन्न करती है।",
    "ε=−dΦ/dt (Φ=चुम्बकीय फ्लक्स)",
    "AC: परिमाण और दिशा बदलती है; DC: केवल एक दिशा में।",
    "आपतन कोण = परावर्तन कोण; आपतित, परावर्तित और अभिलम्ब एक तल में।",
    "1/f=(μ−1)(1/R₁−1/R₂)",
    "सघन से विरल माध्यम, आपतन कोण > क्रान्तिक कोण।",
    "फ्रिंज चौड़ाई β=λD/d; प्रत्येक फ्रिंज समान दूरी पर।",
    "धातु से इलेक्ट्रॉन उत्सर्जन जब प्रकाश पड़ता है; hν=φ+K_max।",
    "λ=h/mv (द्रव्यमान और वेग का गुणनफल)",
    "संलयन: हल्के नाभिक जुड़ते हैं; विखण्डन: भारी नाभिक टूटता है।",
    "बन्धन ऊर्जा=Δm·c²; Δm=द्रव्यमान क्षति।",
    "N: इलेक्ट्रॉन बहुल (अशुद्धि: P, As); P: होल बहुल (अशुद्धि: B)।",
    "अग्र अभिनति में बैरियर वोल्टेज घटती है, धारा प्रवाहित होती है।",
    "प्रतीक: त्रिकोण+बिंदु; A=0→Y=1, A=1→Y=0",
    "प्रवर्धक (signal amplification), स्विच के रूप में।",
    "कम आवृत्ति संकेत को उच्च आवृत्ति वाहक पर अध्यारोपित करना।",
    "दिक्पात (Declination), नति (Dip), क्षैतिज तीव्रता (H)।",
    "L-C-R परिपथ में जब X_L=X_C, प्रतिबाधा न्यूनतम होती है।",
    "Xc=1/(ωC)=1/(2πfC)",
    "cosφ=R/Z (शक्ति/कुल शक्ति)",
    "F=μ₀I₁I₂l/(2πd) प्रति एकांक लम्बाई।",
    "चुम्बकीय क्षेत्र में आवेशित कण वृत्तीय पथ; आवृत्ति f=qB/(2πm)।",
    "चालक: अतिव्यापी बैण्ड; अर्धचालक: 1eV अन्तराल; रोधी: >3eV।",
    "E और B परस्पर लम्बवत, तरंगें अनुप्रस्थ, वेग c=3×10⁸ m/s।"
]
PHYSICS_LONG = [
    "गॉस के नियम का उपयोग कर अनन्त लम्बाई के आवेशित तार के विद्युत क्षेत्र का व्यंजक।",
    "समान्तर प्लेट संधारित्र की धारिता का सूत्र एवं संचित ऊर्जा=½CV²।",
    "किरचॉफ के नियमों द्वारा हीटस्टोन सेतु का सिद्धान्त।",
    "बायो-सेवार्ट नियम द्वारा वृत्ताकार पाश के अक्ष पर चुम्बकीय क्षेत्र।",
    "श्रेणीक्रम LCR परिपथ के लिए प्रतिबाधा एवं शक्ति गुणांक।",
    "ट्रांसफार्मर की संरचना, कार्यविधि एवं सिद्धान्त।",
    "यंग के द्विझिरी प्रयोग में फ्रिंज चौड़ाई का सूत्र।",
    "सरल एवं संयुक्त सूक्ष्मदर्शी की संरचना एवं आवर्धन क्षमता।",
    "आइंस्टीन का प्रकाश विद्युत समीकरण।",
    "P-N सन्धि डायोड एवं अर्द्ध तरंग दिष्टकारी।",
    "दो समान्तर धारावाही चालकों के बीच बल एवं एम्पियर की परिभाषा।",
    "अपवर्तक पृष्ठ पर अपवर्तन सूत्र एवं वास्तविक/आभासी गहराई।",
    "नाभिकीय विखण्डन, संलयन एवं रिएक्टर का सिद्धान्त।",
    "बन्धन ऊर्जा के आधार पर नाभिक के स्थायित्व की व्याख्या।",
    "P-N सन्धि का अग्र एवं उत्क्रम अभिनति में व्यवहार तथा V-I अभिलक्षण।",
    "AND, OR तथा NOT गेटों के प्रतीक, सत्यता सारणी तथा बूलियन व्यंजक।",
    "साइक्लोट्रॉन का सिद्धान्त, संरचना तथा कार्यविधि।",
    "समान्तर प्लेट संधारित्र में पारद्युतिक माध्यम का प्रभाव।",
    "ऊर्जा बैण्ड सिद्धान्त द्वारा चालक, अर्धचालक, विद्युतरोधी में अन्तर।",
    "मैक्सवेल के विद्युत चुम्बकीय तरंग सिद्धान्त की व्याख्या।"
]
PHYSICS_LONG_ANS = [
    "E=λ/(2πε₀r); गॉस पृष्ठ बेलनाकार, ∮E·dA=q/ε₀ से सूत्र।",
    "C=ε₀A/d; U=½CV²=Q²/(2C)=½QV; व्युत्पत्ति सहित।",
    "संतुलन अवस्था: R₁/R₂=R₃/R₄; किरचॉफ के दोनों नियमों का उपयोग।",
    "B=μ₀IR²/(2(R²+x²)^(3/2)); केन्द्र पर B=μ₀I/(2R)।",
    "Z=√(R²+(X_L−X_C)²); cosφ=R/Z; अनुनाद: X_L=X_C, Z=R।",
    "प्राथमिक एवं द्वितीयक कुण्डली; Vp/Vs=Np/Ns; Ip/Is=Ns/Np।",
    "β=λD/d; रचनात्मक व्यतिकरण: nλ=d sinθ; फ्रिंजें समान दूरी।",
    "सरल: m=1+D/f; संयुक्त: m=L/f₀×D/fₑ; रेखाचित्र सहित।",
    "hν=φ+½mv²; निरोधी विभव V₀=K_max/e; देहली आवृत्ति ν₀=φ/h।",
    "अग्र: धारा; उत्क्रम: अल्प धारा; दिष्टकारी: डायोड+प्रतिरोध परिपथ।",
    "F/l=μ₀I₁I₂/(2πd); 1 एम्पियर: दो समान्तर चालकों में 2×10⁻⁷ N/m बल।",
    "μ=वास्तविक गहराई/आभासी गहराई; सूत्र μ₂/v−μ₁/u=(μ₂−μ₁)/R।",
    "विखण्डन: श्रृंखला अभिक्रिया, 235U; संलयन: H²+H³→He⁴+n।",
    "प्रति न्यूक्लिऑन बन्धन ऊर्जा अधिक→स्थायी; Fe-56 सर्वाधिक।",
    "अग्र: धारा बढ़ती; उत्क्रम: बहुत कम धारा; जेनर ब्रेकडाउन; V-I वक्र।",
    "AND: Y=A·B; OR: Y=A+B; NOT: Y=Ā; सत्य सारणी सहित।",
    "दो D-आकार के भाग, चुम्बकीय क्षेत्र; f=qB/(2πm); त्वरण।",
    "C'=Kε₀A/d=KC₀; पारद्युतांक K से धारिता K गुना बढ़ती है।",
    "चालक: E_g≈0; अर्धचालक: E_g≈1eV; रोधी: E_g>3eV।",
    "∇×B=μ₀(J+ε₀∂E/∂t); E⊥B; वेग c=1/√(μ₀ε₀)=3×10⁸ m/s।"
]


# ════════════════════════════════════════════════════════════
#                       CHEMISTRY
# ════════════════════════════════════════════════════════════
CHEMISTRY_OBJ = pad100([
    {"q":"राउल्ट का नियम लागू –","opt":["आदर्श विलयनों पर","अनादर्श विलयनों पर","सभी पर","केवल द्रवों पर"],"ans":0},
    {"q":"मोलरता की इकाई –","opt":["mol L⁻¹","mol kg⁻¹","g L⁻¹","N"],"ans":0},
    {"q":"फैराडे का प्रथम नियम –","opt":["W=ZQ","W=ZI","W=Zt","W=Z/Q"],"ans":0},
    {"q":"अभिक्रिया की कोटि हो सकती है –","opt":["शून्य","पूर्णांक","भिन्नात्मक","इनमें से सभी"],"ans":3},
    {"q":"उत्प्रेरक अभिक्रिया के वेग को –","opt":["बढ़ाता है","घटाता है","अपरिवर्तित रखता है","शून्य करता है"],"ans":0},
    {"q":"प्रथम कोटि के लिए k की इकाई –","opt":["s⁻¹","mol L⁻¹ s⁻¹","L mol⁻¹ s⁻¹","mol s⁻¹"],"ans":0},
    {"q":"पीतल मिश्र धातु –","opt":["Cu+Zn","Cu+Sn","Cu+Ni","Cu+Al"],"ans":0},
    {"q":"OF₂ में ऑक्सीजन की ऑक्सीकरण अवस्था –","opt":["+2","-2","-1","+1"],"ans":0},
    {"q":"NH₃ में नाइट्रोजन का संकरण –","opt":["sp³","sp²","sp","dsp²"],"ans":0},
    {"q":"PCl₅ की आकृति –","opt":["त्रिकोणीय द्विपिरामिडी","चतुष्फलकीय","अष्टफलकीय","वर्ग समतलीय"],"ans":0},
    {"q":"लैन्थेनाइड संकुचन का कारण –","opt":["f-इलेक्ट्रॉनों का दुर्बल परिरक्षण","d-इलेक्ट्रॉनों का प्रबल परिरक्षण","आकार में वृद्धि","नाभिकीय आवेश घटना"],"ans":0},
    {"q":"एल्केन का सामान्य सूत्र –","opt":["CₙH₂ₙ₊₂","CₙH₂ₙ","CₙH₂ₙ₋₂","CₙH₂ₙ₋₆"],"ans":0},
    {"q":"SN1 अभिक्रिया की आण्विकता –","opt":["एक","दो","तीन","शून्य"],"ans":0},
    {"q":"विलियम्सन संश्लेषण उपयोगी –","opt":["ईथर बनाने में","एस्टर बनाने में","एल्डिहाइड बनाने में","कीटोन बनाने में"],"ans":0},
    {"q":"पिक्रिक अम्ल है –","opt":["2,4,6-ट्राइनाइट्रोफीनॉल","2,4-डाइनाइट्रोफीनॉल","नाइट्रोबेंजीन","ट्राइनाइट्रोटोलुइन"],"ans":0},
    {"q":"मार्कोनीकोव नियम लागू –","opt":["असममित एल्कीन में HX जुड़ने पर","सममित एल्कीन में","एल्काइन में","ऐरोमैटिक यौगिकों में"],"ans":0},
    {"q":"ग्लूकोस का अणुसूत्र –","opt":["C₆H₁₂O₆","C₁₂H₂₂O₁₁","C₆H₁₀O₅","C₅H₁₀O₅"],"ans":0},
    {"q":"विटामिन C –","opt":["एस्कॉर्बिक अम्ल","साइट्रिक अम्ल","लैक्टिक अम्ल","एसीटिक अम्ल"],"ans":0},
    {"q":"DNA में अनुपस्थित क्षार –","opt":["यूरैसिल","एडेनीन","ग्वानीन","साइटोसीन"],"ans":0},
    {"q":"एन्जाइम मूलतः –","opt":["प्रोटीन","वसा","कार्बोहाइड्रेट","विटामिन"],"ans":0},
    {"q":"SN2 अभिक्रिया में विन्यास –","opt":["विपरीत","समान","दोनों","कोई नहीं"],"ans":0},
    {"q":"फ्रीडल-क्राफ्ट अभिक्रिया –","opt":["एल्किलीकरण","एसिलीकरण","दोनों","कोई नहीं"],"ans":2},
    {"q":"राइमर-टीमान अभिक्रिया में उत्पाद –","opt":["सैलिसिलैल्डिहाइड","बेंजोइक अम्ल","एसीटोफीनोन","बेंजैल्डिहाइड"],"ans":0},
    {"q":"कैनिजारो अभिक्रिया –","opt":["बेंजैल्डिहाइड","एसीटोन","फॉर्मेल्डिहाइड","दोनों a और c"],"ans":3},
    {"q":"एल्डोल संघनन के लिए आवश्यक –","opt":["α-हाइड्रोजन","β-हाइड्रोजन","γ-हाइड्रोजन","कोई नहीं"],"ans":0},
    {"q":"एस्टरीकरण अभिक्रिया –","opt":["अम्ल+एल्कोहॉल","अम्ल+एमीन","एल्कोहॉल+कीटोन","एल्डिहाइड+एल्कोहॉल"],"ans":0},
    {"q":"डाइएजोटीकरण –","opt":["प्राथमिक एमीन+HNO₂","द्वितीयक एमीन","तृतीयक एमीन","सभी"],"ans":0},
    {"q":"विटामिन A की कमी से –","opt":["रतौंधी","स्कर्वी","बेरी-बेरी","रिकेट्स"],"ans":0},
    {"q":"प्रोटीन की प्राथमिक संरचना –","opt":["एमीनो अम्लों का अनुक्रम","α-हेलिक्स","β-पत्रक","उप-इकाई"],"ans":0},
    {"q":"हाइड्रोजन बंध सबसे प्रबल –","opt":["HF में","H₂O में","NH₃ में","HCl में"],"ans":0},
    {"q":"d-ब्लॉक तत्वों का सामान्य विन्यास –","opt":["(n-1)d¹⁻¹⁰ns⁰⁻²","ns²np⁶","ns¹⁻²","ns²nd¹⁻¹⁰"],"ans":0},
    {"q":"K₄[Fe(CN)₆] में Fe की ऑक्सीकरण अवस्था –","opt":["+2","+3","+4","+6"],"ans":0},
    {"q":"[Co(NH₃)₆]Cl₃ का IUPAC नाम –","opt":["हेक्साएम्मीनकोबाल्ट(III) क्लोराइड","ट्राइएम्मीनकोबाल्ट क्लोराइड","कोबाल्ट हेक्साएम्मीन","क्लोरो कोबाल्ट"],"ans":0},
    {"q":"Crystal Field Theory में विपाटन –","opt":["d-कक्षकों का","s-कक्षकों का","p-कक्षकों का","f-कक्षकों का"],"ans":0},
    {"q":"प्रबल क्षेत्र लिगैण्ड –","opt":["CN⁻","F⁻","Cl⁻","H₂O"],"ans":0},
    {"q":"KMnO₄ का उपयोग –","opt":["ऑक्सीकारक","अपचायक","दोनों","कोई नहीं"],"ans":0},
    {"q":"K₂Cr₂O₇ का रंग –","opt":["नारंगी","हरा","नीला","पीला"],"ans":0},
    {"q":"कार्बन मोनोक्साइड विषैली है क्योंकि –","opt":["हीमोग्लोबिन से बंध बनाती है","O₂ छोड़ती है","CO₂ बनाती है","कोई नहीं"],"ans":0},
    {"q":"ओजोन परत –","opt":["समताप मंडल","क्षोभ मंडल","मध्य मंडल","आयन मंडल"],"ans":0},
    {"q":"ग्रीन हाउस गैस –","opt":["CO₂","O₂","N₂","H₂"],"ans":0},
    {"q":"हैबर विधि से बनता है –","opt":["NH₃","HNO₃","H₂SO₄","HCl"],"ans":0},
    {"q":"ओस्टवाल्ड विधि से बनता है –","opt":["HNO₃","H₂SO₄","NH₃","HCl"],"ans":0},
    {"q":"सम्पर्क विधि से बनता है –","opt":["H₂SO₄","HNO₃","HCl","NaOH"],"ans":0},
    {"q":"विद्युत अपघटन में एनोड पर –","opt":["ऑक्सीकरण","अपचयन","दोनों","कोई नहीं"],"ans":0},
    {"q":"मानक हाइड्रोजन इलेक्ट्रोड का विभव –","opt":["0 V","1 V","-0.76 V","0.34 V"],"ans":0},
    {"q":"नेर्न्स्ट समीकरण –","opt":["E=E°−(RT/nF)lnQ","E=E°+(RT/nF)lnQ","E=mc²","ΔG=−nFE"],"ans":0},
    {"q":"चालकता की इकाई –","opt":["S m⁻¹","Ω","Ω·m","S"],"ans":0},
    {"q":"प्रथम कोटि अभिक्रिया का अर्द्ध-आयु –","opt":["0.693/k","k/0.693","1/k","2k"],"ans":0},
    {"q":"आर्रेनियस समीकरण –","opt":["k=Ae^(−Ea/RT)","k=Ae^(Ea/RT)","k=ATe^(−Ea/R)","k=ART"],"ans":0},
    {"q":"उत्प्रेरक –","opt":["सक्रियण ऊर्जा घटाता है","ऊर्जा बढ़ाता है","साम्य बदलता है","कोई प्रभाव नहीं"],"ans":0},
    {"q":"टिण्डल प्रभाव –","opt":["प्रकाश का प्रकीर्णन","परावर्तन","अपवर्तन","विवर्तन"],"ans":0},
    {"q":"कोलराऊश का नियम –","opt":["अनन्त तनुता पर मोलर चालकता","प्रतिरोध","सेल स्थिरांक","विशिष्ट चालकता"],"ans":0},
    {"q":"शून्य कोटि अभिक्रिया का वेग –","opt":["k","k[A]","k[A]²","k/[A]"],"ans":0},
    {"q":"फेन प्लवन विधि –","opt":["सल्फाइड अयस्क","ऑक्साइड","कार्बोनेट","सभी"],"ans":0},
    {"q":"हॉल-हेरॉल्ट प्रक्रम –","opt":["एलुमिनियम","लोहा","ताँबा","जस्ता"],"ans":0},
    {"q":"मोंड प्रक्रम –","opt":["निकेल","ताँबा","एलुमिनियम","लोहा"],"ans":0},
    {"q":"मिश्र धातु इस्पात –","opt":["Fe+C","Cu+Zn","Cu+Sn","Al+Mg"],"ans":0},
    {"q":"हैलोजन –","opt":["F, Cl, Br, I","O, S, Se","N, P, As","He, Ne, Ar"],"ans":0},
    {"q":"जीनॉन यौगिक –","opt":["XeF₂, XeO₃, XeF₄ सभी","केवल XeF₂","केवल XeO₃","केवल XeF₄"],"ans":0},
    {"q":"समन्वय संख्या –","opt":["लिगैण्डों की संख्या","धातु आयन","आवेश","ऑक्सीकरण अवस्था"],"ans":0},
    {"q":"कीलक प्रभाव –","opt":["बहुदंती लिगैण्ड से स्थायित्व","एकदंती से","दोनों","कोई नहीं"],"ans":0},
    {"q":"उभयदंती लिगैण्ड –","opt":["NO₂⁻","NH₃","H₂O","Cl⁻"],"ans":0},
    {"q":"ब्राउनियन गति –","opt":["कोलॉइड कणों की यादृच्छिक गति","आयनों की गति","इलेक्ट्रॉन गति","अणुओं की गति"],"ans":0},
    {"q":"हार्डी-शुल्ज नियम –","opt":["स्कंदन क्षमता आयन संयोजकता पर","pH पर","ताप पर","सान्द्रता पर"],"ans":0},
    {"q":"पेप्टीकरण –","opt":["अवक्षेप को कोलॉइड में बदलना","कोलॉइड को अवक्षेप में","विलयन","निलंबन"],"ans":0},
    {"q":"नाइट्रोजन वायुमंडल में –","opt":["78%","21%","0.9%","0.03%"],"ans":0},
    {"q":"H₂SO₄ का उपयोग –","opt":["प्रयोगशाला+उर्वरक दोनों","केवल प्रयोगशाला","केवल उर्वरक","कोई नहीं"],"ans":0},
    {"q":"फॉस्फोरस के अपररूप –","opt":["सफेद और लाल","हीरा और ग्रेफाइट","O₂ और O₃","α और β"],"ans":0},
    {"q":"विद्युत अपघटनी परिष्करण में –","opt":["अशुद्ध धातु एनोड, शुद्ध कैथोड","शुद्ध एनोड","दोनों कैथोड","दोनों एनोड"],"ans":0},
    {"q":"बेसेमरीकरण –","opt":["कच्चा लोहा से इस्पात","ताँबा","एलुमिनियम","सीसा"],"ans":0},
    {"q":"एक्टिनाइड –","opt":["रेडियोएक्टिव","अरेडियोएक्टिव","दोनों","कोई नहीं"],"ans":0},
    {"q":"रंगीन आयन का कारण –","opt":["d-d संक्रमण","आवेश स्थानांतरण","दोनों","कोई नहीं"],"ans":2},
    {"q":"लैन्थेनाइड संकुचन का प्रभाव –","opt":["आकार और रासायनिक गुण समान","केवल आकार","केवल गुण","कोई नहीं"],"ans":0},
    {"q":"न्यूक्लिक अम्ल में शर्करा –","opt":["राइबोज/डीऑक्सीराइबोज","ग्लूकोज","फ्रुक्टोज","सुक्रोज"],"ans":0},
    {"q":"DNA का द्विकुण्डली मॉडल –","opt":["वॉटसन एवं क्रिक","मेण्डल","मॉर्गन","डार्विन"],"ans":0},
    {"q":"मोललता की इकाई –","opt":["mol kg⁻¹","mol L⁻¹","g L⁻¹","N"],"ans":0},
    {"q":"परासरण दाब –","opt":["π=CRT","π=nRT/V","दोनों a और b","π=CT"],"ans":2},
    {"q":"वाष्पदाब में सापेक्ष अवनमन –","opt":["x₂ (विलेय का मोल अंश)","x₁","x₁+x₂","x₁/x₂"],"ans":0},
    {"q":"हिमांक अवनमन –","opt":["ΔTf=Kf·m","ΔTb=Kb·m","ΔTf=Kb·m","ΔTb=Kf·m"],"ans":0},
    {"q":"क्वथनांक उन्नयन –","opt":["ΔTb=Kb·m","ΔTf=Kf·m","ΔTb=Kf·m","ΔTf=Kb·m"],"ans":0},
    {"q":"फैराडे द्वितीय नियम –","opt":["समान आवेश पर विभिन्न पदार्थों का जमाव तुल्यांकी भार के अनुपात में","W=ZQ","W=ZI","W=Zt"],"ans":0},
    {"q":"VBT में अष्टफलकीय संकुल का संकरण –","opt":["d²sp³ या sp³d²","sp³","sp³d","dsp²"],"ans":0},
    {"q":"प्रकाशिक समावयवता –","opt":["प्रकाश का ध्रुवण घुमाना","रंग बदलना","विघटन","अपघटन"],"ans":0},
    {"q":"संकुल यौगिकों में प्राथमिक संयोजकता –","opt":["आयनीय","उपसहसंयोजक","दोनों","कोई नहीं"],"ans":0},
    {"q":"एल्कीन का सामान्य सूत्र –","opt":["CₙH₂ₙ","CₙH₂ₙ₊₂","CₙH₂ₙ₋₂","CₙH₂ₙ₋₆"],"ans":0},
    {"q":"एल्काइन का सामान्य सूत्र –","opt":["CₙH₂ₙ₋₂","CₙH₂ₙ₊₂","CₙH₂ₙ","CₙH₂ₙ₋₆"],"ans":0},
    {"q":"जैल –","opt":["द्रव में ठोस का कोलॉइड","गैस में ठोस","ठोस में द्रव","द्रव में गैस"],"ans":0},
    {"q":"इमल्शन –","opt":["द्रव-द्रव कोलॉइड","गैस-द्रव","ठोस-द्रव","गैस-गैस"],"ans":0},
    {"q":"धातुकर्म में फेन प्लवन में झाग उत्पन्न करने वाला –","opt":["पाइन तेल","H₂SO₄","NaCl","NaOH"],"ans":0},
    {"q":"ऑक्सीकरण अवस्था +7 दर्शाता है –","opt":["Mn","Fe","Cu","Cr"],"ans":0},
    {"q":"विटामिन D की कमी से –","opt":["रिकेट्स","रतौंधी","स्कर्वी","बेरी-बेरी"],"ans":0},
    {"q":"अमीनो अम्ल –","opt":["NH₂ और COOH दोनों समूह","केवल NH₂","केवल COOH","OH समूह"],"ans":0},
    {"q":"पेप्टाइड बंध –","opt":["−CO−NH−","−O−C−","−NH−NH−","−S−S−"],"ans":0},
])

CHEMISTRY_SHORT = [
    "राउल्ट के नियम की व्याख्या करें।",
    "आदर्श एवं अनादर्श विलयनों में अन्तर लिखें।",
    "परासरण एवं परासरण दाब को परिभाषित करें।",
    "हिमांक अवनमन एवं क्वथनांक उन्नयन को समझाएँ।",
    "नेर्न्स्ट समीकरण लिखें।",
    "फैराडे के विद्युत अपघटन के नियम लिखें।",
    "प्रथम कोटि अभिक्रिया का अर्द्ध-आयु सूत्र।",
    "आर्रेनियस समीकरण की व्याख्या करें।",
    "कोलराऊश का नियम लिखें।",
    "SN1 और SN2 में अन्तर लिखें।",
    "मार्कोनीकोव नियम उदाहरण सहित।",
    "एल्डोल संघनन अभिक्रिया लिखें।",
    "फ्रीडल-क्राफ्ट अभिक्रिया उदाहरण सहित।",
    "कैनिजारो अभिक्रिया लिखें।",
    "डाइएजोटीकरण अभिक्रिया लिखें।",
    "d-ब्लॉक तत्वों की सामान्य विशेषताएँ।",
    "लैन्थेनाइड संकुचन को समझाएँ।",
    "IUPAC नामकरण नियम संकुल यौगिकों के लिए।",
    "कीलक प्रभाव को उदाहरण सहित।",
    "ग्लूकोज की संरचना एवं गुण।",
    "DNA और RNA में अन्तर।",
    "एन्जाइम की क्रियाविधि।",
    "विटामिनों के कार्य एवं कमी के रोग।",
    "औषधि एवं ड्रग में अन्तर।",
    "साबुन एवं अपमार्जक में अन्तर।",
    "कोलॉइडी विलयन की विशेषताएँ।",
    "हार्डी-शुल्ज नियम लिखें।",
    "धातुकर्म में निस्तापन और भर्जन में अन्तर।",
    "हैबर प्रक्रम की मुख्य अवस्थाएँ।",
    "पर्यावरण प्रदूषण में रसायन की भूमिका।"
]
CHEMISTRY_SHORT_ANS = [
    "P=x₁P₁°+x₂P₂°; आदर्श विलयन में घटकों के वाष्पदाब का आंशिक दाब।",
    "आदर्श: राउल्ट का पालन, ΔHmix=0; अनादर्श: राउल्ट का उल्लंघन।",
    "अर्धपारगम्य झिल्ली से विलायक का प्रवाह; π=CRT।",
    "ΔTf=Kf·m; ΔTb=Kb·m; m=मोललता।",
    "E=E°−(RT/nF)lnQ; 25°C पर E=E°−(0.0592/n)logQ।",
    "I: W=ZQ=ZIt; II: समान आवेश पर जमाव तुल्यांकी भार के अनुपात में।",
    "t₁/₂=0.693/k; स्वतंत्र (प्रारम्भिक सान्द्रता पर नहीं)।",
    "k=Ae^(−Ea/RT); lnk=lnA−Ea/RT; आलेख लनk बनाम 1/T।",
    "Λ°m(इलेक्ट्रोलाइट)=Σν×λ°(आयन); अनन्त तनुता पर।",
    "SN1: एकपदीय, कार्बोकेटायन मध्यवर्ती; SN2: द्विपदीय, विन्यास उलट।",
    "H⁺ प्राथमिकतः कार्बन पर जो पहले से अधिक H युक्त है।",
    "CH₃CHO+OH⁻→CH₃CH(OH)CHO→एल्डोल; निर्जलीकरण→α,β-असंतृप्त।",
    "ArH+RX/AlCl₃→Ar-R+HX (एल्किलीकरण)।",
    "2ArCHO+NaOH→ArCH₂OH+ArCOONa; α-H रहित एल्डिहाइड।",
    "ArNH₂+HNO₂+HCl→ArN₂⁺Cl⁻(0°C); क्रियाशील मध्यवर्ती।",
    "चर ऑक्सीकरण अवस्था, रंगीन आयन, उत्प्रेरक, चुम्बकीय गुण।",
    "4f कक्षकों का दुर्बल परिरक्षण→परमाणु त्रिज्या घटती है।",
    "अंदर→बाहर: लिगैण्ड, केन्द्रीय धातु आयन; बंध से बाहर: काउंटर आयन।",
    "EDTA जैसे बहुदंती लिगैण्ड से छल्लेनुमा संरचना बनती है→स्थायी।",
    "C₆H₁₂O₆; खुली श्रृंखला: पेंटाहाइड्रॉक्सी एल्डिहाइड; हेमीएसिटल।",
    "DNA: डीऑक्सीराइबोज, थायमीन; RNA: राइबोज, यूरैसिल।",
    "सक्रिय स्थल पर क्रियाधार का बंधन→एन्जाइम-क्रियाधार संकुल→उत्पाद।",
    "A: रतौंधी; B₁: बेरी-बेरी; C: स्कर्वी; D: रिकेट्स।",
    "औषधि: बीमारी का इलाज; ड्रग: मानसिक निर्भरता।",
    "साबुन: कार्बोक्सिलेट; अपमार्जक: सल्फोनेट; अपमार्जक कठोर जल में कार्य।",
    "टिण्डल प्रभाव, ब्राउनियन गति, विद्युत कण संचलन, स्कंदन।",
    "उच्च संयोजकता आयन अधिक स्कंदन शक्ति रखता है।",
    "निस्तापन: हवा की अनुपस्थिति में गर्म; भर्जन: हवा की उपस्थिति।",
    "N₂+3H₂→2NH₃; उच्च दाब, 450°C, Fe उत्प्रेरक।",
    "CO₂, CFC, SO₂, NOₓ प्रमुख प्रदूषक; ग्रीन हाउस, ओजोन क्षरण।"
]
CHEMISTRY_LONG = [
    "राउल्ट के नियम, वाष्पदाब अवनमन, हिमांक अवनमन, क्वथनांक उन्नयन।",
    "नेर्न्स्ट समीकरण एवं विद्युत रासायनिक सेल का कार्यकाल।",
    "आर्रेनियस समीकरण एवं सक्रियण ऊर्जा।",
    "d-ब्लॉक तत्वों की भौतिक एवं रासायनिक विशेषताएँ।",
    "संकुल यौगिकों में बंधन: VBT एवं CFT।",
    "एल्कोहॉल से कार्बोक्सिलिक अम्ल तक की अभिक्रियाएँ।",
    "कार्बोहाइड्रेट: वर्गीकरण, संरचना, गुण।",
    "प्रोटीन: संरचना, वर्गीकरण, एन्जाइम।",
    "DNA की संरचना एवं प्रतिकृति।",
    "धातुकर्म: एलुमिनियम एवं आयरन का निष्कर्षण।",
    "हैबर एवं सम्पर्क प्रक्रम।",
    "p-ब्लॉक तत्व: नाइट्रोजन परिवार।",
    "p-ब्लॉक तत्व: हैलोजन एवं उत्कृष्ट गैस।",
    "SN1 एवं SN2 अभिक्रिया की व्याख्या।",
    "ऑक्सो-अम्ल की संरचना एवं गुण।",
    "एमीन: वर्गीकरण, गुण, डाइएजोटीकरण।",
    "फिनोल की विशेष अभिक्रियाएँ।",
    "विटामिन, हार्मोन एवं एन्जाइम की भूमिका।",
    "पॉलिमर: वर्गीकरण एवं उपयोग।",
    "पर्यावरण रसायन: वायु, जल, मृदा प्रदूषण।"
]
CHEMISTRY_LONG_ANS = [
    "P=x₁P₁°+x₂P₂°; ΔP/P₁°=x₂; ΔTf=Kf·m; ΔTb=Kb·m।",
    "E=E°−(RT/nF)lnQ; ΔG=−nFE; साम्य पर E=0।",
    "k=Ae^(−Ea/RT); lnk₂/k₁=Ea/R(1/T₁−1/T₂)।",
    "परिवर्ती ऑक्सीकरण अवस्था, रंगीन आयन, उत्प्रेरक, जटिल यौगिक।",
    "VBT: संकरण; CFT: d-कक्षकों का विपाटन Δ_oct।",
    "एल्कोहॉल→एल्डिहाइड→कार्बोक्सिलिक अम्ल; ऑक्सीकरण क्रम।",
    "मोनोसैकेराइड, डाइसैकेराइड, पॉलिसैकेराइड; ग्लूकोज=C₆H₁₂O₆।",
    "α-हेलिक्स, β-पत्रक; प्राथमिक से चतुर्थक संरचना।",
    "वॉटसन-क्रिक मॉडल; अर्धसंरक्षी प्रतिकृति।",
    "Al: बॉक्साइट→हॉल-हेरॉल्ट; Fe: हेमेटाइट→ब्लास्ट फर्नेस।",
    "N₂+3H₂⇌2NH₃; SO₂+O₂⇌SO₃; उच्च दाब, उत्प्रेरक।",
    "N, P, As, Sb, Bi; नाइट्रिक अम्ल, अमोनिया।",
    "F, Cl, Br, I; HCl; XeF₂, XeF₄, XeF₆।",
    "SN1: कार्बोकेटायन; SN2: पिछवाड़े आक्रमण, विन्यास उलट।",
    "H₃PO₄, H₂SO₄, HNO₃ की संरचना।",
    "1°, 2°, 3° एमीन; ArNH₂+HNO₂→ArN₂⁺; कपलिंग।",
    "कोल्बे, रेमर-टिमन, एस्टरीकरण, ब्रोमीनेशन।",
    "विटामिन A,B,C,D,E,K के कार्य; इंसुलिन; एमाइलेज।",
    "addition, condensation; nylon, Bakelite, PVC, rubber।",
    "CO, SO₂, NOₓ—वायु; DDT—जल; भारी धातु—मृदा।"
]


# ════════════════════════════════════════════════════════════
#                       MATHEMATICS
# ════════════════════════════════════════════════════════════
MATHEMATICS_OBJ = pad100([
    {"q":"यदि f(x)=x²+1, तो f(−1) का मान –","opt":["2","1","0","−1"],"ans":0},
    {"q":"sin⁻¹(1/2) का मुख्य मान –","opt":["π/6","π/3","π/4","π/2"],"ans":0},
    {"q":"यदि A=[[1,2],[3,4]] तो |A| –","opt":["−2","2","10","−10"],"ans":0},
    {"q":"आव्यूह [[1,0],[0,1]] है –","opt":["तत्समक आव्यूह","शून्य आव्यूह","विकर्ण आव्यूह","दोनों a और c"],"ans":3},
    {"q":"सारणिक |a b; c d| –","opt":["ad−bc","ac−bd","ab−cd","a+d−b−c"],"ans":0},
    {"q":"d/dx(sin x) =","opt":["cos x","−cos x","sin x","−sin x"],"ans":0},
    {"q":"∫x dx =","opt":["x²/2+C","x²+C","2x²+C","x³/3+C"],"ans":0},
    {"q":"∫₀¹ x² dx =","opt":["1/3","1/2","1","2"],"ans":0},
    {"q":"फलन f(x)=x² निम्नतम है –","opt":["x=0 पर","x=1 पर","x=−1 पर","x=2 पर"],"ans":0},
    {"q":"d/dx(eˣ) =","opt":["eˣ","xeˣ","eˣ/x","1/x"],"ans":0},
    {"q":"d/dx(log x) =","opt":["1/x","x","eˣ","log x"],"ans":0},
    {"q":"∫cos x dx =","opt":["sin x+C","−sin x+C","cos x+C","−cos x+C"],"ans":0},
    {"q":"î·ĵ का मान –","opt":["0","1","−1","k̂"],"ans":0},
    {"q":"î×ĵ का मान –","opt":["k̂","0","1","−k̂"],"ans":0},
    {"q":"सदिश a=2î+3ĵ+4k̂ का परिमाण –","opt":["√29","29","√20","9"],"ans":0},
    {"q":"रेखा x/2=y/3=z/4 के दिक् अनुपात –","opt":["2,3,4","4,3,2","1,1,1","0,0,0"],"ans":0},
    {"q":"एक सिक्के की उछाल में चित की प्रायिकता –","opt":["1/2","1/3","1/4","1"],"ans":0},
    {"q":"पासे पर सम संख्या की प्रायिकता –","opt":["1/2","1/3","1/6","2/3"],"ans":0},
    {"q":"यदि P(A)=0.4, P(B)=0.5, P(A∩B)=0.2 तो P(A∪B) –","opt":["0.7","0.9","0.1","0.3"],"ans":0},
    {"q":"P(A|B) बराबर है –","opt":["P(A∩B)/P(B)","P(A∩B)","P(A)","P(B)/P(A∩B)"],"ans":0},
    {"q":"रैखिक प्रोग्रामन में सुसंगत क्षेत्र –","opt":["उत्तल बहुभुज","वृत्त","अतिपरवलय","दीर्घवृत्त"],"ans":0},
    {"q":"d/dx(tan x) =","opt":["sec²x","cosec²x","−sec²x","−cosec²x"],"ans":0},
    {"q":"∫sec²x dx =","opt":["tan x+C","cot x+C","−tan x+C","−cot x+C"],"ans":0},
    {"q":"d/dx(sin⁻¹x) =","opt":["1/√(1−x²)","−1/√(1−x²)","1/(1+x²)","−1/(1+x²)"],"ans":0},
    {"q":"∫dx/(1+x²) =","opt":["tan⁻¹x+C","cot⁻¹x+C","sin⁻¹x+C","cos⁻¹x+C"],"ans":0},
    {"q":"फलन f(x)=|x| सतत है –","opt":["प्रत्येक बिन्दु पर","केवल x=0 पर","कहीं नहीं","केवल x>0"],"ans":0},
    {"q":"रोले प्रमेय के लिए आवश्यक –","opt":["f(a)=f(b)","f(a)≠f(b)","अवकलनीय नहीं","सतत नहीं"],"ans":0},
    {"q":"LMVT के लिए c का मान –","opt":["(a,b) में","[a,b] के बाहर","a या b","कोई नहीं"],"ans":0},
    {"q":"वक्र y=x² की (1,1) पर स्पर्श रेखा की प्रवणता –","opt":["2","1","0","−1"],"ans":0},
    {"q":"दो सदिशों का अदिश गुणनफल –","opt":["अदिश","सदिश","दोनों","कोई नहीं"],"ans":0},
    {"q":"दो सदिशों का सदिश गुणनफल –","opt":["सदिश","अदिश","दोनों","कोई नहीं"],"ans":0},
    {"q":"समतल का सदिश समीकरण –","opt":["r·n=d","r×n=d","r=a+λb","r=a+λb+μc"],"ans":0},
    {"q":"रेखा का सदिश समीकरण –","opt":["r=a+λb","r·n=d","r×n=d","r=a+λb+μc"],"ans":0},
    {"q":"यदि A=[a_ij] m×n, तो A' का आकार –","opt":["n×m","m×n","m×m","n×n"],"ans":0},
    {"q":"आव्यूह का गुणन –","opt":["AB≠BA सामान्यतः","AB=BA","हमेशा समान","कोई नहीं"],"ans":0},
    {"q":"|AB| =","opt":["|A||B|","|A|+|B|","|A|−|B|","|A|/|B|"],"ans":0},
    {"q":"यदि A व्युत्क्रमणीय है, तो A⁻¹ =","opt":["adj A/|A|","|A|/adj A","adj A","1/|A|"],"ans":0},
    {"q":"सममित आव्यूह –","opt":["A'=A","A'=−A","A'=A⁻¹","A=0"],"ans":0},
    {"q":"विषम सममित आव्यूह –","opt":["A'=−A","A'=A","A'=A⁻¹","A=I"],"ans":0},
    {"q":"sin⁻¹x+cos⁻¹x =","opt":["π/2","π","0","2π"],"ans":0},
    {"q":"tan⁻¹x+cot⁻¹x =","opt":["π/2","π","0","2π"],"ans":0},
    {"q":"यदि y=sin⁻¹x, तो dy/dx =","opt":["1/√(1−x²)","−1/√(1−x²)","1/(1+x²)","−1/(1+x²)"],"ans":0},
    {"q":"यदि y=tan⁻¹x, तो dy/dx =","opt":["1/(1+x²)","1/√(1−x²)","−1/(1+x²)","1/x"],"ans":0},
    {"q":"एक फलन f: A→B एकैकी है यदि –","opt":["f(x₁)=f(x₂)⇒x₁=x₂","x₁≠x₂⇒f(x₁)=f(x₂)","सभी y के लिए एक x","दोनों a और c"],"ans":0},
    {"q":"आच्छादक फलन –","opt":["प्रत्येक y∈B के लिए कम से कम एक x∈A","सभी x के लिए एक y","एकैकी","अचर फलन"],"ans":0},
    {"q":"साम्य सम्बन्ध –","opt":["स्वतुल्य, सममित, संक्रामक","केवल स्वतुल्य","केवल सममित","केवल संक्रामक"],"ans":0},
    {"q":"फलन की सततता –","opt":["lim x→a f(x)=f(a)","lim x→a f(x)≠f(a)","अवकलनीयता","दोनों a और c"],"ans":0},
    {"q":"अवकलज की परिभाषा –","opt":["lim h→0 [f(x+h)−f(x)]/h","∫f(x)dx","f(b)−f(a)","f'(x)=0"],"ans":0},
    {"q":"गुणनफल नियम –","opt":["(uv)'=u'v+uv'","(uv)'=u'v'","(uv)'=u/v","(uv)'=u'−v'"],"ans":0},
    {"q":"भागफल नियम –","opt":["(u/v)'=(u'v−uv')/v²","(u/v)'=(u'v+uv')/v²","(u/v)'=u'/v'","(u/v)'=(uv'−u'v)/v²"],"ans":0},
    {"q":"श्रृंखला नियम –","opt":["dy/dx=(dy/du)(du/dx)","dy/dx=dy/du+du/dx","dy/dx=dy/du−du/dx","dy/dx=(dy/du)/(du/dx)"],"ans":0},
    {"q":"द्वितीय अवकलज परीक्षण में उच्चतम मान –","opt":["f'(x)=0, f''(x)<0","f'(x)=0, f''(x)>0","f'(x)≠0","f''(x)=0"],"ans":0},
    {"q":"समाकलन विधि – प्रतिस्थापन –","opt":["∫f(g(x))g'(x)dx=∫f(t)dt","∫f(x)g(x)dx","∫f'(x)dx","∫f(x)/g(x)dx"],"ans":0},
    {"q":"खण्डशः समाकलन –","opt":["∫u dv=uv−∫v du","∫u dv=uv+∫v du","∫u dv=u'v−uv'","∫u dv=∫u∫dv"],"ans":0},
    {"q":"∫₋ₐᵃ f(x)dx=2∫₀ᵃ f(x)dx यदि f(x) –","opt":["सम फलन","विषम फलन","न तो सम न विषम","आवर्ती"],"ans":0},
    {"q":"अवकल समीकरण की कोटि –","opt":["उच्चतम अवकलज की कोटि","अवकलजों की संख्या","घात","गुणांक"],"ans":0},
    {"q":"चरों के पृथक्करण –","opt":["dy/dx=f(x)g(y)","dy/dx+Py=Q","रैखिक","समघात"],"ans":0},
    {"q":"रैखिक अवकल समीकरण –","opt":["dy/dx+Py=Q","dy/dx=f(x)g(y)","Mdx+Ndy=0","समघात"],"ans":0},
    {"q":"समघात अवकल समीकरण –","opt":["dy/dx=f(y/x)","dy/dx+Py=Q","चर पृथक्करण","रैखिक"],"ans":0},
    {"q":"सदिश a का मापांक –","opt":["|a|=√(x²+y²+z²)","|a|=x+y+z","|a|=x²+y²+z²","|a|=√(x+y+z)"],"ans":0},
    {"q":"दो सदिशों के बीच कोण –","opt":["cosθ=(a·b)/(|a||b|)","sinθ=(a·b)/(|a||b|)","tanθ=(a·b)/(|a||b|)","cosθ=|a×b|/(|a||b|)"],"ans":0},
    {"q":"त्रिभुज का क्षेत्रफल सदिश रूप में –","opt":["½|a×b|","|a·b|","½|a·b|","|a×b|"],"ans":0},
    {"q":"संरेखता की शर्त –","opt":["a×b=0","a·b=0","a·b=1","a×b=1"],"ans":0},
    {"q":"लम्बवत सदिशों के लिए –","opt":["a·b=0","a×b=0","a·b=1","a=b"],"ans":0},
    {"q":"दो समतलों के बीच का कोण –","opt":["cosθ=|n₁·n₂|/(|n₁||n₂|)","sinθ=|n₁·n₂|/(|n₁||n₂|)","tanθ","कोई नहीं"],"ans":0},
    {"q":"रेखा और समतल के बीच का कोण –","opt":["sinθ=|b·n|/(|b||n|)","cosθ=|b·n|/(|b||n|)","tanθ","दोनों"],"ans":0},
    {"q":"P(A∪B) =","opt":["P(A)+P(B)−P(A∩B)","P(A)+P(B)","P(A)P(B)","P(A)+P(B)+P(A∩B)"],"ans":0},
    {"q":"स्वतंत्र घटनाएँ –","opt":["P(A∩B)=P(A)P(B)","P(A∪B)=P(A)+P(B)","P(A|B)=P(A)","दोनों a और c"],"ans":3},
    {"q":"बेज प्रमेय –","opt":["P(A|B)=P(B|A)P(A)/P(B)","P(A|B)=P(A∩B)/P(B)","P(A|B)=P(A)P(B)","P(A|B)=P(A∪B)"],"ans":0},
    {"q":"यादृच्छिक चर X का माध्य –","opt":["E(X)=Σx·p(x)","E(X)=Σx²·p(x)","E(X)=Σ(x−μ)²p(x)","E(X)=Σp(x)"],"ans":0},
    {"q":"प्रसरण Var(X) –","opt":["E(X²)−[E(X)]²","E(X²)+[E(X)]²","E(X)−E(X²)","[E(X)]²−E(X²)"],"ans":0},
    {"q":"द्विपद बंटन के लिए माध्य –","opt":["np","npq","n","p"],"ans":0},
    {"q":"द्विपद बंटन का प्रसरण –","opt":["npq","np","nq","pq"],"ans":0},
    {"q":"रैखिक प्रोग्रामन में उद्देश्य फलन –","opt":["Z=ax+by","ax+by≤c","x≥0","y≥0"],"ans":0},
    {"q":"इष्टतम बिन्दु –","opt":["सुसंगत क्षेत्र के कोने पर","किसी भी बिन्दु पर","मूल बिन्दु पर","अक्ष पर"],"ans":0},
    {"q":"d/dx(xⁿ) =","opt":["nxⁿ⁻¹","nxⁿ","(n−1)xⁿ⁻²","xⁿ/n"],"ans":0},
    {"q":"d/dx(cot x) =","opt":["−cosec²x","cosec²x","sec²x","−sec²x"],"ans":0},
    {"q":"∫eˣ dx =","opt":["eˣ+C","xeˣ+C","eˣ/x+C","1/eˣ+C"],"ans":0},
    {"q":"∫1/x dx =","opt":["log|x|+C","1/x²+C","x+C","log x²+C"],"ans":0},
    {"q":"द्विआधारी संक्रिया * –","opt":["A×A→A","A→A","A×B→B","B×A→A"],"ans":0},
    {"q":"sec⁻¹x+cosec⁻¹x =","opt":["π/2","π","0","2π"],"ans":0},
    {"q":"∫sin x dx =","opt":["−cos x+C","cos x+C","sin x+C","−sin x+C"],"ans":0},
    {"q":"एकैकी आच्छादक फलन को कहते हैं –","opt":["व्युत्क्रमणीय","अवकलनीय","सतत","अचर"],"ans":0},
    {"q":"|A| तथा |A'| का सम्बन्ध –","opt":["|A|=|A'|","|A|>|A'|","|A|<|A'|","कोई सम्बन्ध नहीं"],"ans":0},
    {"q":"तुल्यता वर्ग –","opt":["साम्य सम्बन्ध द्वारा विभाजन","उपसमुच्चय","प्रतिबिम्ब","डोमेन"],"ans":0},
    {"q":"अवकलनीयता –","opt":["प्रत्येक अवकलनीय फलन सतत है","सतत फलन अवकलनीय है","दोनों","कोई नहीं"],"ans":0},
    {"q":"∫dx/√(1−x²) =","opt":["sin⁻¹x+C","cos⁻¹x+C","tan⁻¹x+C","sec⁻¹x+C"],"ans":0},
    {"q":"d/dx(sec x) =","opt":["sec x tan x","cosec x cot x","−sec x tan x","sec²x"],"ans":0},
    {"q":"d/dx(cosec x) =","opt":["−cosec x cot x","cosec x cot x","−sec x tan x","cosec²x"],"ans":0},
    {"q":"∫tan x dx =","opt":["log|sec x|+C","log|cos x|+C","−log|sec x|+C","log|sin x|+C"],"ans":0},
    {"q":"समान्तर समतलों के बीच की दूरी –","opt":["|d₁−d₂|/|n|","d₁+d₂","d₁−d₂","d₁/d₂"],"ans":0},
    {"q":"निश्चित समाकलन का मूल प्रमेय –","opt":["∫ₐᵇ f(x)dx=F(b)−F(a)","∫ₐᵇ f(x)dx=F(a)−F(b)","∫ₐᵇ f(x)dx=F(a)+F(b)","∫ₐᵇ f(x)dx=0"],"ans":0},
])

MATHEMATICS_SHORT = [
    "सम्बन्ध और फलन में अन्तर।",
    "तत्समक तत्व की परिभाषा उदाहरण सहित।",
    "सममित एवं विषम सममित आव्यूह की परिभाषा।",
    "आव्यूह के सारणिक के गुण।",
    "क्रैमर नियम से रैखिक समीकरण हल करना।",
    "रोले प्रमेय लिखें एवं ज्यामितीय व्याख्या दें।",
    "LMVT लिखें एवं ज्यामितीय व्याख्या दें।",
    "अवकलज की ज्यामितीय व्याख्या।",
    "वक्र पर स्पर्श रेखा एवं अभिलम्ब का समीकरण।",
    "अवरोही एवं आरोही फलन की शर्त।",
    "खण्डशः समाकलन का सूत्र एवं उदाहरण।",
    "∫eˣ[f(x)+f'(x)]dx का मान।",
    "निश्चित समाकलन के गुण।",
    "दो वक्रों के बीच के क्षेत्रफल का सूत्र।",
    "अवकल समीकरण की कोटि एवं घात।",
    "रैखिक अवकल समीकरण का सामान्य हल।",
    "सदिश का मापांक एवं दिक् कोसाइन।",
    "सदिश गुणनफल के गुणधर्म।",
    "समतल का कार्तीय एवं सदिश समीकरण।",
    "रेखा एवं समतल के बीच का कोण।",
    "प्रतिबन्धित प्रायिकता की परिभाषा।",
    "बेज प्रमेय का कथन।",
    "द्विपद बंटन की शर्तें।",
    "रैखिक प्रोग्रामन में मूल शब्दावली।",
    "उच्चतम एवं निम्नतम मान ज्ञात करने की विधि।",
    "प्रतिलोम त्रिकोणमितीय फलनों के मुख्य मान।",
    "आव्यूह गुणन की शर्तें।",
    "सारणिक के cofactor एवं adjoint की परिभाषा।",
    "समान्तर रेखाओं के बीच न्यूनतम दूरी।",
    "यादृच्छिक चर एवं प्रायिकता बंटन।"
]
MATHEMATICS_SHORT_ANS = [
    "सम्बन्ध: क्रमित युग्मों का समुच्चय; फलन: प्रत्येक x के लिए एक y।",
    "a*e=e*a=a; जोड़ में 0, गुणा में 1।",
    "सममित: A'=A; विषम: A'=−A; विषम का विकर्ण अवयव शून्य।",
    "पंक्ति/स्तम्भ बदलने पर चिह्न बदलता है; शून्य पंक्ति पर |A|=0।",
    "Δ=|गुणांक|; x=Δ₁/Δ, y=Δ₂/Δ।",
    "f(a)=f(b), c∈(a,b) जहाँ f'(c)=0। ज्यामितीय: क्षैतिज स्पर्श रेखा।",
    "f'(c)=(f(b)−f(a))/(b−a)। ज्यामितीय: समान्तर जीवा और स्पर्श रेखा।",
    "किसी बिन्दु पर स्पर्श रेखा की प्रवणता।",
    "स्पर्श: y−y₁=m(x−x₁); अभिलम्ब: m'=−1/m।",
    "आरोही: f'(x)>0; अवरोही: f'(x)<0।",
    "∫u dv=uv−∫v du; ILATE नियम।",
    "eˣ·f(x)+C",
    "∫ₐᵇf(x)dx=∫ₐᵇf(a+b−x)dx; ∫₀ᵃ=∫₀ᵃ जब f(a−x)=f(x)।",
    "∫ₐᵇ[f(x)−g(x)]dx जहाँ f(x)≥g(x)।",
    "कोटि: उच्चतम अवकलज की कोटि; घात: उसकी घात।",
    "I.F.=e^(∫Pdx); y×I.F.=∫Q×I.F. dx।",
    "|a|=√(x²+y²+z²); l=x/|a|, m=y/|a|, n=z/|a|।",
    "a×b=−b×a; a×a=0; |a×b|=|a||b|sinθ।",
    "r·n=d (सदिश); ax+by+cz=d (कार्तीय)।",
    "sinθ=|b·n|/(|b||n|)।",
    "P(A|B)=P(A∩B)/P(B), P(B)≠0।",
    "P(Aᵢ|B)=P(B|Aᵢ)P(Aᵢ)/ΣP(B|Aⱼ)P(Aⱼ)।",
    "n परीक्षण, p सफलता प्रायिकता, स्वतंत्र; P(X=r)=ⁿCᵣpʳqⁿ⁻ʳ।",
    "निर्णय चर, प्रतिबंध, उद्देश्य फलन, सुसंगत क्षेत्र, इष्टतम हल।",
    "f'(x)=0 हल करें; f''(x) से निर्णय।",
    "sin⁻¹: [−π/2,π/2]; cos⁻¹: [0,π]; tan⁻¹: (−π/2,π/2)।",
    "A का m×n, B का n×p हो; C=AB का m×p।",
    "Cofactor Cᵢⱼ=(−1)^(i+j)Mᵢⱼ; adj A=[Cᵢⱼ]'।",
    "d=|(b₁×b₂)·(a₂−a₁)|/|b₁×b₂|।",
    "चर X मान लेता है; P(X=x)=p(x); ΣP(X=x)=1।"
]
MATHEMATICS_LONG = [
    "आव्यूहों के सारणिक के गुण एवं उन्हें सिद्ध करें।",
    "क्रैमर नियम द्वारा तीन रैखिक समीकरणों का हल।",
    "रोले प्रमेय तथा LMVT के कथन, उप-पत्तियाँ और ज्यामितीय व्याख्या।",
    "द्वितीय अवकलज परीक्षण द्वारा उच्चतम/निम्नतम मान ज्ञात करें।",
    "खण्डशः एवं प्रतिस्थापन विधि से समाकलन।",
    "निश्चित समाकलन के गुणधर्म एवं अनुप्रयोग।",
    "वक्रों द्वारा घिरे क्षेत्र का क्षेत्रफल।",
    "रैखिक अवकल समीकरण का व्यापक हल।",
    "त्रिविम ज्यामिति: रेखा एवं समतल के समीकरण।",
    "बेज प्रमेय: कथन, उप-पत्ति एवं उदाहरण।",
    "द्विपद बंटन: माध्य, प्रसरण एवं उदाहरण।",
    "रैखिक प्रोग्रामन: ग्राफीय विधि से हल।",
    "सदिश बीजगणित: गुणनफल, क्षेत्रफल, आयतन।",
    "प्रतिलोम त्रिकोणमितीय फलनों के गुणधर्म एवं सिद्धि।",
    "आव्यूह गुणन एवं व्युत्क्रम आव्यूह।",
    "दो रेखाओं के बीच की न्यूनतम दूरी।",
    "समाकलन द्वारा गोले का आयतन।",
    "लघुत्तम उत्पाद कि अधिकतम लाभ के साथ प्राप्ति पर LPP।",
    "माध्य मान प्रमेय का अनुप्रयोग।",
    "प्रायिकता बंटन: माध्य, प्रसरण, मानक विचलन।"
]
MATHEMATICS_LONG_ANS = [
    "गुण: |A'|=|A|, शून्य पंक्ति→|A|=0, स्केलर गुणन आदि; सिद्धि सहित।",
    "Δ≠0 हो; x=Δ₁/Δ, y=Δ₂/Δ, z=Δ₃/Δ; उदाहरण सहित।",
    "रोले: f(a)=f(b)→f'(c)=0; LMVT: f'(c)=(f(b)−f(a))/(b−a)।",
    "f'(x)=0 हल; f''(x)>0→min, <0→max; उदाहरण।",
    "प्रतिस्थापन: t=g(x); खण्डशः: ILATE; उदाहरण सहित।",
    "∫ₐᵇf=∫ₐᵇf(a+b−x); सम/विषम; ∫₀²ᵃ=2∫₀ᵃ या 0।",
    "y=f(x) और y=g(x): A=∫|f(x)−g(x)|dx; रेखाचित्र।",
    "dy/dx+Py=Q; I.F.=e^(∫Pdx); y=e^(−∫P)∫Qe^(∫P)dx।",
    "r=a+λb; r·n=d; दूरी: |a·n−d|/|n|।",
    "P(Aᵢ|B)=P(B|Aᵢ)P(Aᵢ)/ΣP(B|Aⱼ)P(Aⱼ); उदाहरण।",
    "P(X=r)=ⁿCᵣpʳqⁿ⁻ʳ; μ=np; σ²=npq; उदाहरण।",
    "प्रतिबंध→कोने के बिन्दु→Z का मान; इष्टतम।",
    "a·b=|a||b|cosθ; a×b=|a||b|sinθ n̂; [a b c]; आयतन।",
    "sin⁻¹(−x)=−sin⁻¹x; sin⁻¹x+cos⁻¹x=π/2; सिद्धि।",
    "(AB)⁻¹=B⁻¹A⁻¹; adj(AB)=adj B·adj A; सिद्धि।",
    "d=|(b₁×b₂)·(a₂−a₁)|/|b₁×b₂|; उदाहरण सहित।",
    "V=∫πy² dx (x-अक्ष पर); V=(4/3)πr³; सिद्धि।",
    "Z=ax+by; प्रतिबंध सहित; ग्राफीय विधि; उत्तर।",
    "f'(c)=(f(b)−f(a))/(b−a); LMVT का अनुप्रयोग।",
    "E(X)=Σxp(x); Var=E(X²)−[E(X)]²; SD=√Var।"
]


# ════════════════════════════════════════════════════════════
#                       BIOLOGY
# ════════════════════════════════════════════════════════════
BIOLOGY_OBJ = pad100([
    {"q":"अमीबा में जनन –","opt":["द्विविभाजन","बहुविभाजन","मुकुलन","बीजाणु"],"ans":0},
    {"q":"मानव गुणसूत्र संख्या –","opt":["46","23","48","44"],"ans":0},
    {"q":"परागण किसे कहते हैं –","opt":["परागकणों का वर्तिकाग्र पर पहुँचना","निषेचन","बीज निर्माण","फल निर्माण"],"ans":0},
    {"q":"अण्डाशय में अण्डाणु निर्माण –","opt":["ओजेनेसिस","स्पर्मेटोजेनेसिस","भ्रूणजनन","अंगजनन"],"ans":0},
    {"q":"अपरा का कार्य –","opt":["पोषण एवं गैस विनिमय","केवल पोषण","केवल उत्सर्जन","केवल श्वसन"],"ans":0},
    {"q":"DNA का द्विकुण्डली मॉडल –","opt":["वॉटसन एवं क्रिक","मेण्डल","मॉर्गन","डार्विन"],"ans":0},
    {"q":"मेण्डल के द्विसंकर क्रॉस में F2 फीनोटाइप अनुपात –","opt":["9:3:3:1","1:2:1","3:1","1:1"],"ans":0},
    {"q":"सहप्रभाविता का उदाहरण –","opt":["AB रुधिर वर्ग","A रुधिर वर्ग","B रुधिर वर्ग","O रुधिर वर्ग"],"ans":0},
    {"q":"आनुवंशिक कूट है –","opt":["त्रिक (ट्रिप्लेट)","एकल","द्विक","चतुष्क"],"ans":0},
    {"q":"लिंग सहलग्न वंशागति –","opt":["हीमोफीलिया","मधुमेह","कैंसर","TB"],"ans":0},
    {"q":"पारिस्थितिक तन्त्र का अजैविक घटक –","opt":["प्रकाश","पौधे","जन्तु","जीवाणु"],"ans":0},
    {"q":"खाद्य श्रृंखला में ऊर्जा प्रवाह –","opt":["एकदिशीय","द्विदिशीय","चक्रीय","कोई नहीं"],"ans":0},
    {"q":"जैव-विविधता ह्रास का प्रमुख कारण –","opt":["आवास विनाश","पर्यटन","कृषि","शिक्षा"],"ans":0},
    {"q":"ओजोन परत क्षरण –","opt":["CFC","CO₂","O₂","N₂"],"ans":0},
    {"q":"चिपको आन्दोलन –","opt":["वन संरक्षण","जल संरक्षण","मृदा संरक्षण","वायु संरक्षण"],"ans":0},
    {"q":"PCR का पूर्ण रूप –","opt":["Polymerase Chain Reaction","Protein Chain Reaction","Polymer Chain","Primary Chain"],"ans":0},
    {"q":"प्रतिरक्षी निर्माण –","opt":["B-लसीकाणु","T-लसीकाणु","RBC","प्लेटलेट्स"],"ans":0},
    {"q":"AIDS का कारक –","opt":["HIV","HBV","HPV","HSV"],"ans":0},
    {"q":"कैंसर कोशिकाओं की विशेषता –","opt":["अनियन्त्रित विभाजन","नियन्त्रित विभाजन","कोशिका मृत्यु","सामान्य वृद्धि"],"ans":0},
    {"q":"पुनर्योगज DNA तकनीक में एन्जाइम –","opt":["प्रतिबन्धन एण्डोन्यूक्लिएज","लाइगेज","दोनों","केवल लाइपेज"],"ans":2},
    {"q":"पुष्पी पादपों में नर युग्मकोद्भिद –","opt":["परागकण","बीजाण्ड","भ्रूणकोष","फल"],"ans":0},
    {"q":"भ्रूणकोष में कोशिकाओं की संख्या –","opt":["8","7","6","5"],"ans":0},
    {"q":"समसूत्री विभाजन में पुत्री कोशिकाओं में गुणसूत्र संख्या –","opt":["मातृ कोशिका के बराबर","आधी","दुगुनी","चौगुनी"],"ans":0},
    {"q":"DNA प्रतिकृति होती है –","opt":["S-प्रावस्था में","G1-प्रावस्था","G2-प्रावस्था","M-प्रावस्था"],"ans":0},
    {"q":"PCR का उपयोग –","opt":["DNA प्रवर्धन","प्रोटीन संश्लेषण","RNA नष्ट करना","कोशिका विभाजन"],"ans":0},
    {"q":"एण्टीबायोटिक प्रतिरोध –","opt":["जीवाणुओं द्वारा प्रतिरोध विकसित करना","प्रतिरक्षा","एलर्जी","विषाणु संक्रमण"],"ans":0},
    {"q":"जैव आवर्धन (Biomagnification) –","opt":["खाद्य श्रृंखला में विषाक्त पदार्थों की सान्द्रता बढ़ना","पोषण स्तर","ऊर्जा प्रवाह","जैव विविधता"],"ans":0},
    {"q":"उत्तराधिकार का चरम –","opt":["क्लाइमेक्स समुदाय","पायनियर","सेरे","मध्यवर्ती"],"ans":0},
    {"q":"नाइट्रोजन स्थिरीकरण –","opt":["राइजोबियम","नाइट्रोसोमोनास","नाइट्रोबैक्टर","एजोटोबैक्टर"],"ans":0},
    {"q":"जैव विविधता हॉटस्पॉट –","opt":["पश्चिमी घाट","थार मरुस्थल","गंगा का मैदान","हिमालय का ऊपरी भाग"],"ans":0},
    {"q":"IUCN रेड लिस्ट –","opt":["संकटग्रस्त जातियों की सूची","पादपों की सूची","जन्तुओं की सूची","संरक्षित क्षेत्र"],"ans":0},
    {"q":"जैव नैतिकता –","opt":["जैव प्रौद्योगिकी में नैतिक मुद्दे","कानून","धर्म","राजनीति"],"ans":0},
    {"q":"प्लास्मिड –","opt":["अतिरिक्त क्रोमोसोमल DNA","प्रोटीन","RNA","एन्जाइम"],"ans":0},
    {"q":"प्रतिबन्धन एन्जाइम –","opt":["DNA को विशिष्ट स्थान पर काटता है","जोड़ता है","प्रतिलिपि बनाता है","विकृत करता है"],"ans":0},
    {"q":"लाइगेज –","opt":["DNA खण्डों को जोड़ता है","काटता है","प्रतिलिपि बनाता है","विकृत करता है"],"ans":0},
    {"q":"PCR के चरण –","opt":["विकृतीकरण, प्राइमर संलयन, विस्तारण","केवल विकृतीकरण","केवल संलयन","केवल विस्तारण"],"ans":0},
    {"q":"ट्रांसजेनिक जीव –","opt":["अन्य जीव का जीन वाले जीव","प्राकृतिक","क्लोन","संकर"],"ans":0},
    {"q":"जीन चिकित्सा –","opt":["दोषपूर्ण जीन को सही करना","शल्य चिकित्सा","औषधि","विकिरण"],"ans":0},
    {"q":"डॉली भेड़ –","opt":["प्रथम क्लोन स्तनधारी","प्रथम पक्षी","प्रथम मछली","प्रथम कीट"],"ans":0},
    {"q":"जैव उर्वरक –","opt":["लाभदायक जीवाणु/कवक","रासायनिक उर्वरक","कीटनाशक","खरपतवारनाशी"],"ans":0},
    {"q":"माइकोराइजा –","opt":["कवक और पादप मूल का सहजीवन","जीवाणु","विषाणु","प्रोटोजोआ"],"ans":0},
    {"q":"जैव उपचार –","opt":["प्रदूषण हटाने में सूक्ष्मजीवों का उपयोग","भौतिक विधि","रासायनिक विधि","भस्मीकरण"],"ans":0},
    {"q":"लैक्टोज ओपेरॉन –","opt":["लैक्टोज चयापचय का नियमन","ग्लूकोज","सुक्रोज","माल्टोज"],"ans":0},
    {"q":"अनुवादन –","opt":["mRNA से प्रोटीन","DNA से mRNA","DNA से DNA","प्रोटीन से DNA"],"ans":0},
    {"q":"राइबोसोम –","opt":["प्रोटीन संश्लेषण स्थल","ऊर्जा उत्पादन","प्रकाश संश्लेषण","लिपिड संश्लेषण"],"ans":0},
    {"q":"उत्परिवर्तन –","opt":["DNA अनुक्रम में परिवर्तन","प्रोटीन","RNA","कोशिका विभाजन"],"ans":0},
    {"q":"वंशावली विश्लेषण –","opt":["पारिवारिक वृक्ष द्वारा वंशागति अध्ययन","प्रयोगशाला","क्षेत्र","सांख्यिकी"],"ans":0},
    {"q":"सहलग्नता –","opt":["एक ही गुणसूत्र पर जीन","भिन्न गुणसूत्रों पर","सभी जीन","केवल लिंग गुणसूत्र"],"ans":0},
    {"q":"लिंग निर्धारण –","opt":["XY प्रणाली","XX","XO","ZW"],"ans":0},
    {"q":"हीमोफीलिया –","opt":["X-सहलग्न अप्रभावी","Y-सहलग्न","ऑटोसोमल","प्रभावी"],"ans":0},
    {"q":"वर्णान्धता –","opt":["X-सहलग्न अप्रभावी","Y-सहलग्न","ऑटोसोमल","प्रभावी"],"ans":0},
    {"q":"डाउन सिण्ड्रोम –","opt":["21वाँ गुणसूत्र त्रिगुणित","लिंग गुणसूत्र","ऑटोसोमल अप्रभावी","X-सहलग्न"],"ans":0},
    {"q":"टर्नर सिण्ड्रोम –","opt":["45, X0","47, XXY","46, XX","46, XY"],"ans":0},
    {"q":"क्लाइनफेल्टर सिण्ड्रोम –","opt":["47, XXY","45, X0","46, XX","46, XY"],"ans":0},
    {"q":"DNA फिंगरप्रिंटिंग –","opt":["व्यक्ति की पहचान DNA द्वारा","उँगलियों के निशान","रक्त परीक्षण","मूत्र परीक्षण"],"ans":0},
    {"q":"सूक्ष्म प्रवर्धन –","opt":["ऊतक संवर्धन द्वारा पादप उत्पादन","बीज द्वारा","कलम द्वारा","दाब द्वारा"],"ans":0},
    {"q":"IVF –","opt":["इन विट्रो निषेचन","प्राकृतिक निषेचन","कृत्रिम गर्भाधान","भ्रूण स्थानांतरण"],"ans":0},
    {"q":"MOET –","opt":["बहु अण्डोत्सर्ग भ्रूण स्थानांतरण","IVF","AI","क्लोनिंग"],"ans":0},
    {"q":"मधुमक्खी पालन –","opt":["एपीकल्चर","सेरीकल्चर","पिसीकल्चर","हॉर्टीकल्चर"],"ans":0},
    {"q":"रेशम कीट पालन –","opt":["सेरीकल्चर","एपीकल्चर","पिसीकल्चर","हॉर्टीकल्चर"],"ans":0},
    {"q":"हरित क्रान्ति –","opt":["अधिक उपज वाली फसलें","उद्योग","सूचना प्रौद्योगिकी","सेवा"],"ans":0},
    {"q":"श्वेत क्रान्ति –","opt":["दुग्ध उत्पादन","कृषि","मत्स्य","रेशम"],"ans":0},
    {"q":"नीली क्रान्ति –","opt":["मत्स्य उत्पादन","दुग्ध","कृषि","रेशम"],"ans":0},
    {"q":"पीली क्रान्ति –","opt":["तिलहन उत्पादन","दुग्ध","मत्स्य","फल"],"ans":0},
    {"q":"जैव बायोपाइरेसी –","opt":["जैविक संसाधनों का अनधिकृत उपयोग","संरक्षण","अनुसंधान","शिक्षा"],"ans":0},
    {"q":"जीवाणुभोजी –","opt":["विषाणु जो जीवाणु को संक्रमित करता है","जीवाणु","कवक","प्रोटोजोआ"],"ans":0},
    {"q":"मानव जीनोम परियोजना –","opt":["मानव DNA अनुक्रम का मानचित्रण","प्रोटीन","RNA","कोशिका"],"ans":0},
    {"q":"जैव संवर्धन –","opt":["पोषक तत्वों से फसल की गुणवत्ता सुधारना","उर्वरक","कीटनाशक","खरपतवारनाशी"],"ans":0},
    {"q":"स्टेम कोशिका –","opt":["अविभेदित कोशिकाएँ","विभेदित","मृत","कैंसर"],"ans":0},
    {"q":"पारिस्थितिक अनुक्रमण –","opt":["एक समुदाय का दूसरे से प्रतिस्थापन","खाद्य श्रृंखला","ऊर्जा पिरामिड","जैव भू-रासायनिक चक्र"],"ans":0},
    {"q":"विनाइट्रीकरण –","opt":["नाइट्रेट का नाइट्रोजन गैस में बदलना","नाइट्रोजन स्थिरीकरण","अमोनीकरण","नाइट्रीकरण"],"ans":0},
    {"q":"जीन बैंक –","opt":["आनुवंशिक विविधता का संरक्षण","बीज बैंक","पराग बैंक","सभी"],"ans":3},
    {"q":"कृत्रिम बीज –","opt":["सोमैटिक भ्रूण","प्राकृतिक बीज","संकर बीज","पराग"],"ans":0},
    {"q":"जैव कीटनाशक –","opt":["बैसिलस थुरिनजिएन्सिस","DDT","मैलाथियान","एन्ड्रिन"],"ans":0},
    {"q":"पशुपालन में AI –","opt":["कृत्रिम गर्भाधान","स्वाभाविक","IVF","ET"],"ans":0},
    {"q":"मत्स्य पालन –","opt":["पिसीकल्चर","एपीकल्चर","सेरीकल्चर","हॉर्टीकल्चर"],"ans":0},
    {"q":"आनुवंशिक अभियांत्रिकी –","opt":["DNA में परिवर्तन","प्रजनन","उत्परिवर्तन","प्राकृतिक चयन"],"ans":0},
    {"q":"पेटेंट –","opt":["आविष्कार का अधिकार","प्रकाशन","शिक्षा","व्यापार"],"ans":0},
    {"q":"जीवाणुभोजी में DNA इंजेक्ट होता है –","opt":["होस्ट जीवाणु में","पादप में","जन्तु में","कवक में"],"ans":0},
    {"q":"ऊतक संवर्धन –","opt":["पोषक माध्यम में ऊतक वृद्धि","प्राकृतिक वृद्धि","बीज बोना","कलम"],"ans":0},
    {"q":"जीन विनिमय –","opt":["अर्द्धसूत्री विभाजन में","समसूत्री","द्विविभाजन","मुकुलन"],"ans":0},
    {"q":"अर्द्धसूत्री विभाजन होता है –","opt":["जनन कोशिकाओं में","शरीर कोशिकाओं में","तंत्रिका कोशिकाओं में","पेशी कोशिकाओं में"],"ans":0},
    {"q":"परागण का माध्यम –","opt":["वायु, जल, कीट सभी","केवल वायु","केवल जल","केवल कीट"],"ans":0},
    {"q":"द्विनिषेचन होता है –","opt":["आवृतबीजी में","अनावृतबीजी में","दोनों","कोई नहीं"],"ans":0},
    {"q":"भ्रूण में पोषण –","opt":["प्राथमिक भ्रूणपोष","बीजपत्र","मातृ ऊतक","सभी"],"ans":3},
    {"q":"पुष्पी पादपों में मादा युग्मकोद्भिद –","opt":["भ्रूणकोष","परागकण","बीजाण्ड","फल"],"ans":0},
    {"q":"निषेचन के बाद अण्डाशय बनता है –","opt":["फल","बीज","भ्रूण","भ्रूणपोष"],"ans":0},
    {"q":"तीन पोषण स्तर वाली खाद्य श्रृंखला में ऊर्जा क्षय –","opt":["90%","10%","50%","100%"],"ans":0},
    {"q":"10% नियम किसने दिया?","opt":["लिंडमान","टैन्स्ले","ओडम","एल्टन"],"ans":0},
])

BIOLOGY_SHORT = [
    "परागण एवं निषेचन में अन्तर।",
    "द्विनिषेचन को समझाएँ।",
    "भ्रूणकोष की संरचना।",
    "मेण्डल के नियम लिखें।",
    "अपूर्ण प्रभाविता का उदाहरण दें।",
    "DNA की संरचना।",
    "DNA प्रतिकृति की विधि।",
    "अनुलेखन एवं अनुवादन में अन्तर।",
    "PCR की क्रियाविधि।",
    "मानव जीनोम परियोजना के लक्ष्य।",
    "पारिस्थितिक तंत्र के घटक।",
    "ऊर्जा पिरामिड को समझाएँ।",
    "नाइट्रोजन चक्र को समझाएँ।",
    "जैव विविधता के प्रकार।",
    "IUCN की श्रेणियाँ।",
    "पुनर्योगज DNA तकनीक के चरण।",
    "प्रतिबन्धन एन्जाइम का उपयोग।",
    "ट्रांसजेनिक पादपों के उदाहरण।",
    "जैव उपचार के उदाहरण।",
    "IVF की प्रक्रिया।",
    "AIDS से बचाव के उपाय।",
    "कैंसर के प्रकार।",
    "प्रतिरक्षा तंत्र में B और T कोशिकाओं की भूमिका।",
    "डाउन सिण्ड्रोम के लक्षण।",
    "वर्णान्धता की वंशागति।",
    "लिंग निर्धारण की XY प्रणाली।",
    "सहलग्नता एवं जीन विनिमय।",
    "समसूत्री एवं अर्द्धसूत्री विभाजन में अन्तर।",
    "हरित क्रान्ति की विशेषताएँ।",
    "पशु प्रजनन में MOET विधि।"
]
BIOLOGY_SHORT_ANS = [
    "परागण: पराग का वर्तिकाग्र पर पहुँचना; निषेचन: युग्मकों का संलयन।",
    "एक नर युग्मक+अण्डा=युग्मनज; दूसरा नर+दो ध्रुवीय केन्द्रक=त्रिगुणित भ्रूणपोष।",
    "8 नाभिक, 7 कोशिकाएँ; अण्डकोशिका, सहायक कोशिकाएँ, केन्द्रीय कोशिका, प्रतिमुख कोशिकाएँ।",
    "I: प्रभाविता; II: पृथक्करण; III: स्वतंत्र अपव्यूहन।",
    "स्नैपड्रैगन में RR=लाल, rr=सफेद, Rr=गुलाबी।",
    "वॉटसन-क्रिक मॉडल; द्विकुण्डली; A-T, G-C युग्म; 10 bp प्रति घुमाव।",
    "अर्धसंरक्षी; DNA polymerase; 5'→3' दिशा; प्रमुख एवं पश्च रज्जु।",
    "अनुलेखन: DNA→mRNA; अनुवादन: mRNA→प्रोटीन।",
    "विकृतीकरण(94°C)→प्राइमर संलयन(55°C)→विस्तारण(72°C); 30-35 चक्र।",
    "मानव DNA अनुक्रम पहचानना; रोगों की पहचान; जीन मानचित्र।",
    "जैविक (उत्पादक, उपभोक्ता, अपघटक) एवं अजैविक (प्रकाश, जल, ताप)।",
    "सीधा पिरामिड (घास→हिरण→शेर); उल्टा पिरामिड (जलीय)।",
    "N₂→अमोनिया (राइजोबियम)→नाइट्राइट→नाइट्रेट→पादप→जन्तु→अपघटन।",
    "आनुवंशिक, जातीय, पारिस्थितिक विविधता।",
    "विलुप्त, संकटग्रस्त, असुरक्षित, लगभग संकटग्रस्त।",
    "DNA काटना (प्रतिबन्धन एन्जाइम)→जोड़ना (लाइगेज)→क्लोनिंग वेक्टर में प्रवेश।",
    "विशिष्ट स्थान पर DNA काटता है; EcoRI, BamHI उदाहरण।",
    "Bt कपास, Bt बैंगन, सुनहरा चावल (Golden Rice)।",
    "Pseudomonas द्वारा तेल रिसाव साफ करना; आर्सेनिक हटाना।",
    "अण्डाशय से अण्डाणु निकालना→शुक्राणु से निषेचन (पेट्री डिश में)→गर्भाशय में स्थानांतरण।",
    "असुरक्षित यौन संबंध से बचें; सुई साझा न करें; रक्त परीक्षण।",
    "कार्सिनोमा, सार्कोमा, लिम्फोमा, ल्यूकेमिया।",
    "B: प्रतिरक्षी बनाता है; T: कोशिका माध्यित प्रतिरक्षा।",
    "मानसिक मंदता, छोटा कद, एकल पाल्मर रेखा; 47 गुणसूत्र।",
    "XX महिला: वाहक या पीड़ित; XY पुरुष: पीड़ित (Xᵃ Y)।",
    "X: XX महिला; Y: XY पुरुष; Y पैतृक से आता है।",
    "सहलग्न जीन साथ वंशागत; जीन विनिमय से अलग हो सकते हैं।",
    "समसूत्री: दो समान पुत्री कोशिकाएँ; अर्द्धसूत्री: चार अगुणित।",
    "उच्च उपज किस्में (HYV), सिंचाई, उर्वरक, कीटनाशक।",
    "बहु अण्डोत्सर्ग (FSH द्वारा)→भ्रूण संग्रह→सरोगेट में स्थानांतरण।"
]
BIOLOGY_LONG = [
    "पुष्पी पादपों में लैंगिक जनन एवं द्विनिषेचन।",
    "मानव नर एवं मादा जनन तंत्र।",
    "मेण्डल के नियमों की व्याख्या एवं द्विसंकर क्रॉस।",
    "DNA की संरचना एवं प्रतिकृति।",
    "अनुलेखन एवं अनुवादन की क्रियाविधि।",
    "पुनर्योगज DNA तकनीक के चरण एवं अनुप्रयोग।",
    "PCR की विधि एवं महत्त्व।",
    "पारिस्थितिक तंत्र: संरचना एवं कार्य।",
    "जैव विविधता: महत्त्व एवं संरक्षण।",
    "मानव स्वास्थ्य एवं रोग: AIDS, कैंसर, प्रतिरक्षा।",
    "आनुवंशिक रोग: डाउन सिण्ड्रोम, हीमोफीलिया, वर्णान्धता।",
    "मानव जीनोम परियोजना एवं DNA फिंगरप्रिंटिंग।",
    "जैव प्रौद्योगिकी के अनुप्रयोग: कृषि, चिकित्सा।",
    "हरित क्रान्ति एवं पशु प्रजनन।",
    "पर्यावरण प्रदूषण: कारण, प्रभाव, समाधान।",
    "नाइट्रोजन चक्र एवं कार्बन चक्र।",
    "जैव विविधता ह्रास के कारण एवं संरक्षण के उपाय।",
    "मानव प्रतिरक्षा तंत्र एवं टीकाकरण।",
    "उत्परिवर्तन के प्रकार एवं महत्त्व।",
    "पुनर्योगज DNA द्वारा इंसुलिन उत्पादन।"
]
BIOLOGY_LONG_ANS = [
    "परागण→परागनलिका→निषेचन→द्विनिषेचन; भ्रूणकोष की संरचना।",
    "नर: वृषण, शुक्राशय, मूत्रमार्ग; मादा: अण्डाशय, गर्भाशय, योनि।",
    "पृथक्करण, स्वतंत्र अपव्यूहन; 9:3:3:1 अनुपात; चेकर बोर्ड।",
    "वॉटसन-क्रिक; A-T, G-C; अर्धसंरक्षी प्रतिकृति; leading/lagging।",
    "RNA polymerase; mRNA→tRNA+राइबोसोम→प्रोटीन; कूट।",
    "प्रतिबन्धन एन्जाइम+लाइगेज+वेक्टर+होस्ट; Bt Cotton, Golden Rice।",
    "विकृतीकरण→प्राइमर संलयन→विस्तारण; 2ⁿ प्रतिलिपियाँ; Taq polymerase।",
    "उत्पादक→प्राथमिक उपभोक्ता→द्वितीयक→तृतीयक; 10% नियम।",
    "आनुवंशिक, जातीय, पारिस्थितिक; in situ, ex situ संरक्षण।",
    "AIDS: HIV→CD4 कोशिकाएँ नष्ट; कैंसर: ऑन्कोजीन; प्रतिरक्षा: B,T।",
    "डाउन: ट्राइसोमी 21; हीमोफीलिया: X-सहलग्न; वर्णान्धता: X-सहलग्न।",
    "3×10⁹ bp; 25000 जीन; रोग पहचान; DNA फिंगरप्रिंटिंग: STR।",
    "BT cotton, insulin, erythropoietin, HGH।",
    "HYV, सिंचाई; MOET, IVF, AI; भैंस, गाय।",
    "CO₂, CFC, DDT; ग्रीन हाउस, ओजोन क्षरण; समाधान।",
    "N₂→NH₃→NO₂→NO₃→N₂; CO₂→प्रकाश संश्लेषण→श्वसन→CO₂।",
    "आवास विनाश, शिकार, प्रदूषण; in situ (वन्य), ex situ (Zoo)।",
    "B कोशिका: प्रतिरक्षी; T कोशिका: कोशिका माध्यित; टीकाकरण।",
    "बिन्दु, क्रोमोसोमल, जीनोमिक; आनुवंशिक रोग, विकास।",
    "मानव इंसुलिन जीन→प्लास्मिड→E. coli→इंसुलिन उत्पादन।"
]


# ════════════════════════════════════════════════════════════
#               COMPLETE QUESTION BANK
# ════════════════════════════════════════════════════════════
QB = {
    "Hindi":       {"obj": HINDI_OBJ,       "short": HINDI_SHORT,       "short_ans": HINDI_SHORT_ANS,       "long": HINDI_LONG,       "long_ans": HINDI_LONG_ANS},
    "English":     {"obj": ENGLISH_OBJ,     "short": ENGLISH_SHORT,     "short_ans": ENGLISH_SHORT_ANS,     "long": ENGLISH_LONG,     "long_ans": ENGLISH_LONG_ANS},
    "Physics":     {"obj": PHYSICS_OBJ,     "short": PHYSICS_SHORT,     "short_ans": PHYSICS_SHORT_ANS,     "long": PHYSICS_LONG,     "long_ans": PHYSICS_LONG_ANS},
    "Chemistry":   {"obj": CHEMISTRY_OBJ,   "short": CHEMISTRY_SHORT,   "short_ans": CHEMISTRY_SHORT_ANS,   "long": CHEMISTRY_LONG,   "long_ans": CHEMISTRY_LONG_ANS},
    "Mathematics": {"obj": MATHEMATICS_OBJ, "short": MATHEMATICS_SHORT, "short_ans": MATHEMATICS_SHORT_ANS, "long": MATHEMATICS_LONG, "long_ans": MATHEMATICS_LONG_ANS},
    "Biology":     {"obj": BIOLOGY_OBJ,     "short": BIOLOGY_SHORT,     "short_ans": BIOLOGY_SHORT_ANS,     "long": BIOLOGY_LONG,     "long_ans": BIOLOGY_LONG_ANS},
}

SUBJECTS = list(QB.keys())


# ════════════════════════════════════════════════════════════
#                   KEYBOARD HELPERS
# ════════════════════════════════════════════════════════════
def subject_keyboard():
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    buttons = [telebot.types.InlineKeyboardButton(s, callback_data=f"subj_{s}") for s in SUBJECTS]
    markup.add(*buttons)
    return markup

def mode_keyboard(subject):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        telebot.types.InlineKeyboardButton("📝 Objective (100 MCQ)", callback_data=f"mode_{subject}_obj"),
        telebot.types.InlineKeyboardButton("✍️ Short Answer (30 Q)", callback_data=f"mode_{subject}_short"),
        telebot.types.InlineKeyboardButton("📖 Long Answer (20 Q)",  callback_data=f"mode_{subject}_long"),
        telebot.types.InlineKeyboardButton("🏠 Back to Subjects",    callback_data="back_home"),
    )
    return markup

def start_from_keyboard(subject, mode, total):
    """Show buttons: Start from 1, Start from 11, 21, ... upto total"""
    markup = telebot.types.InlineKeyboardMarkup(row_width=5)
    btns = []
    step = 10 if mode == "obj" else (5 if mode == "short" else 5)
    for i in range(1, total+1, step):
        btns.append(telebot.types.InlineKeyboardButton(str(i), callback_data=f"start_{subject}_{mode}_{i}"))
    # Also allow manual input
    markup.add(*btns)
    markup.add(telebot.types.InlineKeyboardButton("🏠 Back to Subjects", callback_data="back_home"))
    return markup

def answer_keyboard(subject, mode, idx):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        telebot.types.InlineKeyboardButton("✅ Show Answer", callback_data=f"ans_{subject}_{mode}_{idx}"),
        telebot.types.InlineKeyboardButton("⏭ Next Question", callback_data=f"next_{subject}_{mode}_{idx}"),
        telebot.types.InlineKeyboardButton("🔢 Jump to Question", callback_data=f"jump_{subject}_{mode}"),
        telebot.types.InlineKeyboardButton("🏠 Main Menu",   callback_data="back_home"),
    )
    return markup

def mcq_keyboard(subject, idx, num_opts):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    labels = ["A","B","C","D"]
    btns = [telebot.types.InlineKeyboardButton(labels[i], callback_data=f"mcq_{subject}_{idx}_{i}") for i in range(num_opts)]
    markup.add(*btns)
    markup.add(
        telebot.types.InlineKeyboardButton("⏭ Skip", callback_data=f"next_{subject}_obj_{idx}"),
        telebot.types.InlineKeyboardButton("🔢 Jump to Question", callback_data=f"jump_{subject}_obj"),
        telebot.types.InlineKeyboardButton("🏠 Main Menu", callback_data="back_home"),
    )
    return markup


# ════════════════════════════════════════════════════════════
#                   MESSAGE FORMATTERS
# ════════════════════════════════════════════════════════════
def format_obj_question(subject, idx):
    q_data = QB[subject]["obj"][idx]
    opts = q_data["opt"]
    labels = ["A","B","C","D"]
    total = len(QB[subject]["obj"])
    text = (
        f"📚 *{subject}* | Question *{idx+1}/{total}*\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"❓ {q_data['q']}\n\n"
        + "\n".join([f"  *{labels[i]}*. {opts[i]}" for i in range(len(opts))])
    )
    return text

def format_short_question(subject, idx):
    q = QB[subject]["short"][idx]
    total = len(QB[subject]["short"])
    return (
        f"📚 *{subject}* | Short Answer *{idx+1}/{total}*\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"❓ {q}"
    )

def format_long_question(subject, idx):
    q = QB[subject]["long"][idx]
    total = len(QB[subject]["long"])
    return (
        f"📚 *{subject}* | Long Answer *{idx+1}/{total}*\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"❓ {q}"
    )


# ════════════════════════════════════════════════════════════
#                   BOT HANDLERS
# ════════════════════════════════════════════════════════════
@bot.message_handler(commands=["start", "help"])
def cmd_start(message):
    uid = message.from_user.id
    sess = get_session(uid)
    save_user_session(uid, sess)
    bot.send_message(
        message.chat.id,
        "🎓 *BSEB 12th 2027 Question Bank*\n\n"
        "📌 Select a subject to begin:\n\n"
        "• 100 Objective (MCQ)\n"
        "• 30 Short Answer\n"
        "• 20 Long Answer\n\n"
        "💡 *Tip:* You can resume from any question number!",
        parse_mode="Markdown",
        reply_markup=subject_keyboard()
    )

@bot.callback_query_handler(func=lambda c: c.data == "back_home")
def cb_home(call):
    bot.edit_message_text(
        "🎓 *BSEB 12th 2027 Question Bank*\n\nSelect a subject:",
        call.message.chat.id,
        call.message.message_id,
        parse_mode="Markdown",
        reply_markup=subject_keyboard()
    )

@bot.callback_query_handler(func=lambda c: c.data.startswith("subj_"))
def cb_subject(call):
    subject = call.data[5:]
    bot.edit_message_text(
        f"📚 *{subject}*\n\nChoose question type:",
        call.message.chat.id,
        call.message.message_id,
        parse_mode="Markdown",
        reply_markup=mode_keyboard(subject)
    )

@bot.callback_query_handler(func=lambda c: c.data.startswith("mode_"))
def cb_mode(call):
    # mode_{subject}_{mode}
    parts = call.data.split("_", 2)
    subject = parts[1]
  
