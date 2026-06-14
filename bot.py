import os, json, random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import google.generativeai as genai

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8792779625:AAEyyDTvoO1jTqgvha6GKvO2u64AwJGPFBw")
DATA_FILE = "bseb_data.json"

# ─── AI CHAT (Google Gemini) ─────────────────────────────────
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
genai.configure(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None
gemini_model = genai.GenerativeModel('gemini-1.5-flash') if GEMINI_API_KEY else None

PHY_OBJ = [
{"q":"विद्युत क्षेत्र की SI इकाई:","opts":["N/C","C/N","V·m","J/C"],"ans":0},
{"q":"कूलॉम बल किसके व्युत्क्रमानुपाती?","opts":["r","r²","r³","√r"],"ans":1},
{"q":"ΦE = ?","opts":["q/ε₀","ε₀/q","q·ε₀","q²/ε₀"],"ans":0},
{"q":"विद्युत विभव V = ?","opts":["kq/r²","kq/r","kq·r","k/qr"],"ans":1},
{"q":"समविभव पृष्ठ पर कार्य:","opts":["अधिकतम","न्यूनतम","शून्य","अनंत"],"ans":2},
{"q":"संधारित्र ऊर्जा U = ?","opts":["CV","CV²","½CV²","2CV"],"ans":2},
{"q":"ε₀ = ?","opts":["8.85×10⁻¹²","9×10⁹","6.67×10⁻¹¹","1.6×10⁻¹⁹"],"ans":0},
{"q":"ओम नियम में R किस पर निर्भर नहीं?","opts":["तापमान","V और I दोनों","लंबाई","क्षेत्रफल"],"ans":1},
{"q":"विद्युत शक्ति P = ?","opts":["VI","V/I","I/V","V+I"],"ans":0},
{"q":"किर्चहॉफ I नियम का आधार:","opts":["ऊर्जा","आवेश संरक्षण","संवेग","द्रव्यमान"],"ans":1},
{"q":"व्हीटस्टोन ब्रिज: P/Q = ?","opts":["R/S","S/R","P·Q","P+Q"],"ans":0},
{"q":"लॉरेन्ज बल F = ?","opts":["qE","q(v×B)","qvB","q(E+v×B)"],"ans":3},
{"q":"साइक्लोट्रॉन आवृत्ति किस पर निर्भर नहीं?","opts":["q","m","v","B"],"ans":2},
{"q":"∮B·dl = ?","opts":["μ₀I","μ₀/I","I/μ₀","μ₀I²"],"ans":0},
{"q":"वृत्ताकार लूप केंद्र पर B = ?","opts":["μ₀I/2R","μ₀I/R","μ₀I/4πR","2μ₀I/R"],"ans":0},
{"q":"चुंबकीय फ्लक्स SI मात्रक:","opts":["टेस्ला","हेनरी","वेबर","एम्पियर"],"ans":2},
{"q":"फैराडे नियम: ε = ?","opts":["dΦ/dt","-dΦ/dt","Φ/t","-Φ·t"],"ans":1},
{"q":"स्व-प्रेरकत्व SI मात्रक:","opts":["वेबर","हेनरी","टेस्ला","फैराड"],"ans":1},
{"q":"AC परिपथ में Z = ?","opts":["R+XL+XC","√(R²+(XL-XC)²)","R·XL","XL-XC"],"ans":1},
{"q":"Power factor = ?","opts":["R/Z","Z/R","XL/Z","XC/R"],"ans":0},
{"q":"AC का rms मान = ?","opts":["I₀","I₀/2","I₀/√2","√2·I₀"],"ans":2},
{"q":"EM तरंगों की खोज:","opts":["फैराडे","मैक्सवेल","हर्ट्ज","न्यूटन"],"ans":1},
{"q":"सबसे कम तरंगदैर्ध्य:","opts":["रेडियो","X-Ray","दृश्य","गामा"],"ans":3},
{"q":"स्नेल का नियम:","opts":["n₁sinθ₁=n₂sinθ₂","n₁cosθ₁=n₂cosθ₂","n₁θ₁=n₂θ₂","n₁/sinθ₁=n₂"],"ans":0},
{"q":"दर्पण सूत्र:","opts":["1/v+1/u=1/f","1/f=1/v-1/u","v+u=f","f=u·v"],"ans":0},
{"q":"पूर्ण आंतरिक परावर्तन:","opts":["θ<θc","θ>θc","θ=0","n₁<n₂"],"ans":1},
{"q":"मानव नेत्र निकट दृष्टि दूरी:","opts":["10cm","25cm","50cm","100cm"],"ans":1},
{"q":"यंग में β = ?","opts":["λD/d","λd/D","Dd/λ","D/λd"],"ans":0},
{"q":"KEmax = ?","opts":["hν+φ","hν-φ","hν/φ","φ-hν"],"ans":1},
{"q":"डी-ब्रॉयली: λ = ?","opts":["h/mv","mv/h","h·mv","m/hv"],"ans":0},
{"q":"बोर: कोणीय संवेग = ?","opts":["nh/2π","h/2πn","2πn/h","nh"],"ans":0},
{"q":"H आयनन ऊर्जा:","opts":["13.6eV","3.4eV","1.51eV","0.85eV"],"ans":0},
{"q":"बाल्मर श्रेणी:","opts":["पराबैंगनी","दृश्य","अवरक्त","X-ray"],"ans":1},
{"q":"T₁/₂ = ?","opts":["λ/0.693","0.693/λ","0.693·λ","1/λ"],"ans":1},
{"q":"p-n अग्र अभिनति में धारा:","opts":["शून्य","अत्यल्प","अधिक","असीमित"],"ans":2},
{"q":"n-type डोपेंट:","opts":["त्रिसंयोजी","पंचसंयोजी","द्विसंयोजी","शून्य"],"ans":1},
{"q":"NAND = AND + ?","opts":["OR","NOT","NOR","XOR"],"ans":1},
{"q":"OR Boolean: Y = ?","opts":["A·B","A+B","Ā","A⊕B"],"ans":1},
{"q":"1 eV = ?","opts":["1.6×10⁻¹⁹J","1.6×10⁻¹⁰J","9.1×10⁻³¹J","6.67×10⁻¹¹J"],"ans":0},
{"q":"प्रकाश चाल = ?","opts":["3×10⁸m/s","3×10⁶m/s","3×10¹⁰m/s","3×10⁴m/s"],"ans":0},
{"q":"1C में इलेक्ट्रॉन = ?","opts":["6.25×10¹⁸","1.6×10¹⁹","6.25×10¹⁹","1.6×10⁻¹⁹"],"ans":0},
{"q":"∮E·dA = ?","opts":["q/ε₀","qε₀","q²/ε₀","ε₀/q"],"ans":0},
{"q":"समान्तर प्लेट C = ?","opts":["ε₀A/d","ε₀d/A","A/ε₀d","d/ε₀A"],"ans":0},
{"q":"किर्चहॉफ II नियम आधार:","opts":["ऊर्जा संरक्षण","आवेश","संवेग","द्रव्यमान"],"ans":0},
{"q":"मीटर सेतु तार:","opts":["मैंगनिन","ताँबा","लोहा","चाँदी"],"ans":0},
{"q":"चुम्बकीय क्षेत्र रेखाएँ:","opts":["बन्द वक्र","खुली","सीधी","परवलय"],"ans":0},
{"q":"चुम्बकीय बल F = ?","opts":["qvB sinθ","qvB","qE","qvB cosθ"],"ans":0},
{"q":"लेंज नियम आधार:","opts":["ऊर्जा संरक्षण","आवेश","संवेग","द्रव्यमान"],"ans":0},
{"q":"प्रिज्म न्यूनतम विचलन:","opts":["(μ-1)A","(μ+1)A","μA","A/μ"],"ans":0},
{"q":"दूरदर्शी आवर्धन:","opts":["f₀/fₑ","fₑ/f₀","f₀+fₑ","f₀-fₑ"],"ans":0},
{"q":"LED पूर्ण रूप:","opts":["Light Emitting Diode","Low Energy Diode","Long Electric","Light Energy"],"ans":0},
{"q":"जेनर डायोड:","opts":["पश्च अभिनति में","अग्र में","दोनों","किसी में नहीं"],"ans":0},
{"q":"ट्रांसफार्मर:","opts":["केवल AC","केवल DC","दोनों","किसी पर नहीं"],"ans":0},
{"q":"LCR अनुनाद पर Z:","opts":["न्यूनतम=R","अधिकतम","शून्य","अनंत"],"ans":0},
{"q":"निरोधी विभव V₀ = ?","opts":["KEmax/e","e/KEmax","hν/e","e/hν"],"ans":0},
{"q":"ΔxΔp ≥ ?","opts":["h/4π","h/2π","h/π","h"],"ans":0},
{"q":"नाभिकीय बल:","opts":["आवेश स्वतंत्र+प्रबल+लघु परास","आवेश निर्भर","दुर्बल","दीर्घ परास"],"ans":0},
{"q":"AND Boolean: Y = ?","opts":["A·B","A+B","Ā","A⊕B"],"ans":0},
{"q":"NOT: Y = ?","opts":["Ā","A·B","A+B","A⊕B"],"ans":0},
{"q":"सौर सेल:","opts":["प्रकाश→विद्युत","विद्युत→प्रकाश","ताप→विद्युत","यांत्रिक→विद्युत"],"ans":0},
{"q":"फोटोडायोड उपयोग:","opts":["प्रकाश संसूचक","उत्सर्जक","प्रवर्धक","दोलक"],"ans":0},
{"q":"β = ?","opts":["Ic/Ib","Ib/Ic","Ie/Ic","Ic/Ie"],"ans":0},
{"q":"IC पूर्ण रूप:","opts":["Integrated Circuit","Internal Circuit","Inductive Circuit","Inverse Circuit"],"ans":0},
{"q":"NAND सार्वत्रिक क्यों?","opts":["सभी गेट बनते हैं","केवल AND","केवल OR","कोई नहीं"],"ans":0},
{"q":"EM तरंगें:","opts":["अनुप्रस्थ","अनुदैर्ध्य","दोनों","कोई नहीं"],"ans":0},
{"q":"मैलस नियम: I = ?","opts":["I₀cos²θ","I₀sin²θ","I₀cosθ","I₀/2"],"ans":0},
{"q":"प्रकाशिक तन्तु सिद्धान्त:","opts":["पूर्ण आन्तरिक परावर्तन","परावर्तन","अपवर्तन","विवर्तन"],"ans":0},
{"q":"p = ?","opts":["q×2a","q×a","2q×a","q²×a"],"ans":0},
{"q":"समविभव पृष्ठ और E रेखाएँ:","opts":["लम्बवत","समान्तर","कोण","विपरीत"],"ans":0},
{"q":"J = ?","opts":["I/A","IA","I/A²","A/I"],"ans":0},
{"q":"प्रतिरोधकता मात्रक:","opts":["Ω·m","Ω/m","m/Ω","Ω"],"ans":0},
{"q":"श्रेणी संधारित्र: 1/C = ?","opts":["1/C₁+1/C₂","C₁+C₂","C₁C₂/(C₁+C₂)","C₁-C₂"],"ans":0},
{"q":"समान्तर संधारित्र: C = ?","opts":["C₁+C₂","1/C₁+1/C₂","C₁C₂/(C₁+C₂)","C₁-C₂"],"ans":0},
{"q":"XOR: Y = ?","opts":["A⊕B","A·B","A+B","(A·B)'"],"ans":0},
{"q":"चालक गोले की C = ?","opts":["4πε₀R","ε₀A/d","2πε₀R","πε₀R"],"ans":0},
{"q":"द्विध्रुव U = ?","opts":["-pEcosθ","pEsinθ","pEcosθ","-pEsinθ"],"ans":0},
{"q":"एम्पियर परिभाषा आधार:","opts":["दो समान्तर धारावाही चालक","चुम्बकीय क्षेत्र","विद्युत क्षेत्र","प्रेरण"],"ans":0},
{"q":"कार्बन डेटिंग:","opts":["C-14","C-12","C-13","C-11"],"ans":0},
{"q":"समस्थानिक में समान:","opts":["Z","A","न्यूट्रॉन","B और C"],"ans":0},
{"q":"नाभिकीय रिएक्टर मंदक:","opts":["भारी जल","साधारण जल","तेल","CO₂"],"ans":0},
{"q":"स्काई तरंग संचार:","opts":["आयनमंडल","क्षोभमंडल","मध्यमंडल","समतापमंडल"],"ans":0},
{"q":"AM में परिवर्तित:","opts":["आयाम","आवृत्ति","दोनों","कोई नहीं"],"ans":0},
{"q":"FM में परिवर्तित:","opts":["आवृत्ति","आयाम","दोनों","कोई नहीं"],"ans":0},
{"q":"लाइमन श्रेणी:","opts":["पराबैंगनी","दृश्य","अवरक्त","X-ray"],"ans":0},
{"q":"पूर्ण तरंग दिष्टकारी में डायोड:","opts":["2","1","3","4"],"ans":0},
{"q":"विद्युत शक्ति P = ?","opts":["I²R","V/I","IR","V-IR"],"ans":0},
{"q":"भू तरंग संचार:","opts":["कम आवृत्ति","उच्च","माइक्रोवेव","X-ray"],"ans":0},
{"q":"ध्रुवण सिद्ध करता है:","opts":["अनुप्रस्थ तरंग","अनुदैर्ध्य","यांत्रिक","ध्वनि"],"ans":0},
{"q":"एकल झिरी केंद्रीय उच्चिष्ठ:","opts":["2λ/a","λ/a","λ/2a","2a/λ"],"ans":0},
{"q":"N = ?","opts":["N₀e^(-λt)","N₀e^(λt)","N₀/λt","λN₀t"],"ans":0},
{"q":"पोजिट्रॉन खोज:","opts":["एंडर्सन","रदरफोर्ड","थॉमसन","चैडविक"],"ans":0},
{"q":"न्यूट्रॉन खोज:","opts":["चैडविक","रदरफोर्ड","थॉमसन","बोहर"],"ans":0},
{"q":"e/m मापा:","opts":["थॉमसन","रदरफोर्ड","मिलिकन","बोहर"],"ans":0},
{"q":"विद्युत चुम्बकीय प्रेरण नियम:","opts":["फैराडे","मैक्सवेल","हेनरी","लेंज"],"ans":0},
{"q":"किर्चहॉफ नियम दिए:","opts":["किर्चहॉफ","ओम","फैराडे","गाउस"],"ans":0},
{"q":"रदरफोर्ड का मॉडल:","opts":["नाभिकीय","प्लम पुडिंग","बोहर","क्वांटम"],"ans":0},
{"q":"बोहर मॉडल सफल:","opts":["H स्पेक्ट्रम","He स्पेक्ट्रम","Li","सभी"],"ans":0},
{"q":"β क्षय में निकलता है:","opts":["इलेक्ट्रॉन","प्रोटॉन","न्यूट्रॉन","α कण"],"ans":0},
{"q":"α कण है:","opts":["He नाभिक","H नाभिक","इलेक्ट्रॉन","फोटॉन"],"ans":0},
{"q":"γ किरण है:","opts":["विद्युत चुम्बकीय","आवेशित कण","α कण","β कण"],"ans":0},
]

CHE_OBJ = [
{"q":"NaCl संरचना:","opts":["Simple cubic","FCC","BCC","HCP"],"ans":1},
{"q":"FCC में परमाणु:","opts":["1","2","4","6"],"ans":2},
{"q":"BCC में परमाणु:","opts":["1","2","4","3"],"ans":1},
{"q":"FCC packing efficiency:","opts":["52%","68%","74%","26%"],"ans":2},
{"q":"ΔP/P° = ?","opts":["n₂/(n₁+n₂)","n₁/(n₁+n₂)","n₁·n₂","n₁/n₂"],"ans":0},
{"q":"π = ?","opts":["MRT","nRT/V","CRT","RT/C"],"ans":2},
{"q":"एनोड पर:","opts":["अपचयन","ऑक्सीकरण","कोई नहीं","दोनों"],"ans":1},
{"q":"m = ?","opts":["ZIt","ZI/t","It/Z","Z/It"],"ans":0},
{"q":"वेग r = ?","opts":["k[A]ⁿ","k/[A]ⁿ","k·t","[A]/k"],"ans":0},
{"q":"t₁/₂=0.693/k किस कोटि?","opts":["0","1st","2nd","3rd"],"ans":1},
{"q":"KMnO₄ में Mn:","opts":["+4","+6","+7","+2"],"ans":2},
{"q":"[Co(NH₃)₆]³⁺ में Co:","opts":["+1","+2","+3","+6"],"ans":2},
{"q":"SN2 में:","opts":["Retention","Racemisation","Walden Inversion","Elimination"],"ans":2},
{"q":"Fehling's positive:","opts":["दोनों","Aldehyde","Ketone","दोनों ऋणात्मक"],"ans":1},
{"q":"Tollens positive:","opts":["Ketone","Aldehyde","Alcohol","Ether"],"ans":1},
{"q":"Glucose:","opts":["C₆H₁₂O₆","C₁₂H₂₂O₁₁","C₆H₁₀O₅","C₅H₁₀O₅"],"ans":0},
{"q":"DNA में Thymine का जोड़ा:","opts":["Adenine","Guanine","Cytosine","Uracil"],"ans":0},
{"q":"Nylon-6,6:","opts":["Addition polymer","Condensation polymer","Elastomer","Plastic"],"ans":1},
{"q":"Aspirin:","opts":["Analgesic","Antiseptic","Antacid","Antibiotic"],"ans":0},
{"q":"Molarity मात्रक:","opts":["mol/kg","mol/L","g/L","mol/mol"],"ans":1},
{"q":"SN1 में मध्यवर्ती:","opts":["Carbocation","Carbanion","Radical","कोई नहीं"],"ans":0},
{"q":"विलियम्सन संश्लेषण:","opts":["ईथर","एस्टर","एल्डिहाइड","कीटोन"],"ans":0},
{"q":"मार्कोनीकोव नियम:","opts":["असममित एल्कीन","सममित","एल्काइन","सभी"],"ans":0},
{"q":"लैन्थेनाइड संकुचन कारण:","opts":["f-e⁻ दुर्बल परिरक्षण","d-e⁻","आकार वृद्धि","आवेश घटना"],"ans":0},
{"q":"K₄[Fe(CN)₆] में Fe:","opts":["+2","+3","+4","+6"],"ans":0},
{"q":"[Co(NH₃)₆]Cl₃ IUPAC:","opts":["हेक्साएम्मीनकोबाल्ट(III) क्लोराइड","ट्राईएम्मीन","कोबाल्ट हेक्सा","क्लोरो कोबाल्ट"],"ans":0},
{"q":"प्रबल क्षेत्र लिगैण्ड:","opts":["CN⁻","F⁻","Cl⁻","H₂O"],"ans":0},
{"q":"d-d संक्रमण से:","opts":["रंग","चालकता","अनुचुम्बकत्व","प्रतिचुम्बकत्व"],"ans":0},
{"q":"H-bond सबसे प्रबल:","opts":["HF","H₂O","NH₃","HCl"],"ans":0},
{"q":"फिटकरी:","opts":["K₂SO₄·Al₂(SO₄)₃·24H₂O","NaCl","KCl","CaCO₃"],"ans":0},
{"q":"ओजोन परत:","opts":["समताप मंडल","क्षोभ","मध्य","आयन"],"ans":0},
{"q":"हैबर विधि:","opts":["NH₃","HNO₃","H₂SO₄","HCl"],"ans":0},
{"q":"सम्पर्क विधि:","opts":["H₂SO₄","HNO₃","HCl","NaOH"],"ans":0},
{"q":"SHE विभव:","opts":["0V","1V","-0.76V","0.34V"],"ans":0},
{"q":"E = ?","opts":["E°-(RT/nF)lnQ","E°+(RT/nF)lnQ","E°lnQ","E°/lnQ"],"ans":0},
{"q":"कोलराऊश नियम:","opts":["अनन्त तनुता पर मोलर चालकता","प्रतिरोध","सेल स्थिरांक","विशिष्ट चालकता"],"ans":0},
{"q":"शून्य कोटि वेग:","opts":["k","k[A]","k[A]²","k/[A]"],"ans":0},
{"q":"आर्रेनियस: k = ?","opts":["A·e^(-Ea/RT)","A·e^(Ea/RT)","A·T·e^(-Ea)","A·R·T"],"ans":0},
{"q":"टिण्डल प्रभाव:","opts":["कोलॉइड","विलयन","निलंबन","शुद्ध द्रव"],"ans":0},
{"q":"हार्डी-शुल्ज:","opts":["स्कंदन","पेप्टीकरण","विद्युत अपोहन","टिण्डल"],"ans":0},
{"q":"विटामिन A कमी:","opts":["रतौंधी","स्कर्वी","बेरी-बेरी","रिकेट्स"],"ans":0},
{"q":"विटामिन C:","opts":["एस्कॉर्बिक अम्ल","साइट्रिक अम्ल","लैक्टिक अम्ल","एसीटिक अम्ल"],"ans":0},
{"q":"DNA में अनुपस्थित:","opts":["यूरैसिल","एडेनीन","ग्वानीन","साइटोसीन"],"ans":0},
{"q":"एन्जाइम मूलतः:","opts":["प्रोटीन","वसा","कार्बोहाइड्रेट","विटामिन"],"ans":0},
{"q":"प्रोटीन प्राथमिक संरचना:","opts":["एमीनो अम्लों का अनुक्रम","α-हेलिक्स","β-पत्रक","उप-इकाई"],"ans":0},
{"q":"न्यूक्लिक अम्ल में शर्करा:","opts":["राइबोज/डीऑक्सीराइबोज","ग्लूकोज","फ्रुक्टोज","सुक्रोज"],"ans":0},
{"q":"फेन प्लवन:","opts":["सल्फाइड","ऑक्साइड","कार्बोनेट","हैलाइड"],"ans":0},
{"q":"मोंड प्रक्रम:","opts":["निकेल","ताँबा","एलुमिनियम","लोहा"],"ans":0},
{"q":"हॉल-हेरॉल्ट:","opts":["एलुमिनियम","लोहा","ताँबा","जस्ता"],"ans":0},
{"q":"बेसेमरीकरण:","opts":["इस्पात","ताँबा","एलुमिनियम","सीसा"],"ans":0},
{"q":"पीतल:","opts":["Cu+Zn","Cu+Sn","Cu+Ni","Cu+Al"],"ans":0},
{"q":"NH₃ संकरण:","opts":["sp³","sp²","sp","dsp²"],"ans":0},
{"q":"PCl₅ आकृति:","opts":["त्रिकोणीय द्विपिरामिडी","चतुष्फलकीय","अष्टफलकीय","वर्ग समतलीय"],"ans":0},
{"q":"OF₂ में O:","opts":["+2","-2","-1","+1"],"ans":0},
{"q":"राइमर-टीमान उत्पाद:","opts":["सैलिसिलैल्डिहाइड","बेंजोइक अम्ल","एसीटोफीनोन","बेंजैल्डिहाइड"],"ans":0},
{"q":"एल्डोल संघनन:","opts":["α-H","β-H","γ-H","कोई नहीं"],"ans":0},
{"q":"एस्टरीकरण:","opts":["अम्ल+एल्कोहॉल","अम्ल+एमीन","एल्कोहॉल+कीटोन","एल्डिहाइड+एल्कोहॉल"],"ans":0},
{"q":"डाइएजोटीकरण:","opts":["1°एमीन+HNO₂","2°एमीन","3°एमीन","सभी"],"ans":0},
{"q":"कैनिजारो अभिक्रिया:","opts":["बेंजैल्डिहाइड","एसीटोन","फॉर्मेल्डिहाइड","दोनों A और C"],"ans":3},
{"q":"K₂Cr₂O₇ रंग:","opts":["नारंगी","हरा","नीला","पीला"],"ans":0},
{"q":"ग्रीन हाउस गैस:","opts":["CO₂","O₂","N₂","H₂"],"ans":0},
{"q":"ओस्टवाल्ड विधि:","opts":["HNO₃","H₂SO₄","NH₃","HCl"],"ans":0},
{"q":"VBT अष्टफलकीय संकरण:","opts":["d²sp³","sp³d²","दोनों","sp³"],"ans":2},
{"q":"कीलक प्रभाव:","opts":["स्थायित्व बढ़ता","घटता","अपरिवर्तित","कोई नहीं"],"ans":0},
{"q":"जीनॉन यौगिक:","opts":["XeF₂,XeF₄,XeF₆","NeF₂","ArF₄","KrO₃"],"ans":0},
{"q":"फॉस्फोरस अपररूप:","opts":["सफेद और लाल","हीरा-ग्रेफाइट","O₂-O₃","α-β"],"ans":0},
{"q":"H₂SO₄ उपयोग:","opts":["केवल उर्वरक","उर्वरक+प्रयोगशाला","केवल प्रयोगशाला","कोई नहीं"],"ans":1},
{"q":"प्रकाशिक समावयवता:","opts":["ध्रुवीकृत प्रकाश घूमता","रंग बदलता","अपघटन","कोई नहीं"],"ans":0},
{"q":"Van't Hoff i NaCl:","opts":["≈2","≈1","≈3","≈4"],"ans":0},
{"q":"ΔTb = ?","opts":["i·Kb·m","Kb·m","i·m","Kb/m"],"ans":0},
{"q":"Gabriel synthesis:","opts":["1°Amine","2°Amine","3°Amine","Amide"],"ans":0},
{"q":"DNA-RNA अंतर:","opts":["DNA-Thymine, RNA-Uracil","DNA-Uracil","समान","कोई नहीं"],"ans":0},
{"q":"Addition polymer:","opts":["PVC","Nylon","Dacron","Bakelite"],"ans":0},
{"q":"Condensation polymer:","opts":["Nylon-6,6","Teflon","Polythene","PVC"],"ans":0},
{"q":"एन्जाइम कार्य:","opts":["Lock and Key","Random","Linear","Circular"],"ans":0},
{"q":"Friedel-Crafts उत्प्रेरक:","opts":["AlCl₃","NaOH","H₂SO₄","HCl"],"ans":0},
{"q":"Hoffmann Bromamide:","opts":["1°Amine","2°Amine","Amide","Nitrile"],"ans":0},
{"q":"नाइट्रोबेंजीन अपचयन (अम्ल):","opts":["Aniline","Azobenzene","Azoxybenzene","Phenylhydroxylamine"],"ans":0},
{"q":"चालकता SI:","opts":["S m⁻¹","Ω","Ω m","S"],"ans":0},
{"q":"आण्विकता:","opts":["अभिकारक अणु संख्या","उत्पाद","Ea","वेग"],"ans":0},
{"q":"उत्प्रेरक Ea को:","opts":["घटाता","बढ़ाता","अपरिवर्तित","शून्य"],"ans":0},
{"q":"ब्राउनियन गति:","opts":["कोलॉइड कण","आयन","इलेक्ट्रॉन","अणु"],"ans":0},
{"q":"जैल:","opts":["ठोस में द्रव","द्रव में ठोस","गैस में ठोस","द्रव में गैस"],"ans":0},
{"q":"इमल्शन:","opts":["द्रव में द्रव","गैस में द्रव","ठोस में द्रव","गैस में ठोस"],"ans":0},
{"q":"CO विषैली क्यों?","opts":["Hb से दृढ़ बंध","O₂ छोड़ती","CO₂ बनाती","कोई नहीं"],"ans":0},
{"q":"Bakelite:","opts":["Phenol+Formaldehyde","Styrene","VinylChloride","Ethylene"],"ans":0},
{"q":"Teflon:","opts":["Tetrafluoroethylene","Ethylene","Propylene","Styrene"],"ans":0},
{"q":"Buna-S:","opts":["Butadiene+Styrene","Butadiene+Acrylonitrile","Isoprene","Chloroprene"],"ans":0},
{"q":"π = CRT किसका?","opts":["परासरण दाब","वाष्प दाब","क्वथनांक उन्नयन","हिमांक अवनमन"],"ans":0},
{"q":"प्रतिरोध श्रेणी: R = ?","opts":["R₁+R₂","1/R₁+1/R₂","R₁R₂/(R₁+R₂)","R₁-R₂"],"ans":0},
{"q":"Beckmann Rearrangement उत्पाद:","opts":["Amide","Amine","Alcohol","Ether"],"ans":0},
{"q":"नाइट्रीकरण:","opts":["Nitrobacter","Rhizobium","Azotobacter","Clostridium"],"ans":0},
{"q":"विद्युत अपघटन एनोड:","opts":["ऑक्सीकरण","अपचयन","दोनों","कोई नहीं"],"ans":0},
{"q":"हैलोजन:","opts":["F,Cl,Br,I","O,S,Se","N,P,As","He,Ne,Ar"],"ans":0},
{"q":"मानक इलेक्ट्रोड विभव:","opts":["SHE से तुलना","किसी से","pH पर","ताप पर"],"ans":0},
{"q":"Raoult नियम किस पर?","opts":["आदर्श विलयन","अनादर्श","सभी","केवल द्रव"],"ans":0},
{"q":"मोललता मात्रक:","opts":["mol/kg","mol/L","g/L","mol/mol"],"ans":0},
{"q":"हेनरी नियम:","opts":["गैस घुलनशीलता दाब पर","ताप पर","दोनों","कोई नहीं"],"ans":0},
{"q":"अपवर्तनांक μ = ?","opts":["c/v","v/c","λ/λ₀","λ₀/λ"],"ans":0},
{"q":"अम्लीय माध्यम में KMnO₄:","opts":["MnSO₄","MnO₂","Mn₂O₃","KMnO₄"],"ans":0},
]

BIO_OBJ = [
{"q":"द्विनिषेचन में:","opts":["केवल भ्रूण","केवल भ्रूणपोष","भ्रूण+भ्रूणपोष","बीज"],"ans":2},
{"q":"आर्तव चक्र:","opts":["14 दिन","21 दिन","28 दिन","35 दिन"],"ans":2},
{"q":"मेंडल पृथक्करण नियम:","opts":["स्वतंत्र अपव्यूहन","प्रभाविता","पृथक्करण","युग्मन"],"ans":2},
{"q":"DNA में Thymine जोड़ा:","opts":["Adenine","Guanine","Cytosine","Uracil"],"ans":0},
{"q":"AUG कोडॉन:","opts":["Leucine","Methionine(Start)","Stop","Alanine"],"ans":1},
{"q":"PCR पूरा नाम:","opts":["Protein Chain","Polymerase Chain Reaction","Polymer Code","None"],"ans":1},
{"q":"Bt toxin मारता है:","opts":["Fungi","Bacteria","Lepidopteran larvae","Virus"],"ans":2},
{"q":"Autosomes:","opts":["23 जोड़े","22 जोड़े","46","44"],"ans":1},
{"q":"Down's syndrome:","opts":["45","46","47","48"],"ans":2},
{"q":"10% नियम:","opts":["10% ऊर्जा अगले को","20%","50%","100%"],"ans":0},
{"q":"In-situ conservation:","opts":["Zoo","National Park","Seed Bank","Botanical Garden"],"ans":1},
{"q":"Light Reaction:","opts":["Stroma","Thylakoid membrane","Mitochondria","Cytoplasm"],"ans":1},
{"q":"Auxin मुख्य कार्य:","opts":["पत्ती रंग","Cell elongation","फूल","Dormancy"],"ans":1},
{"q":"Human heart chambers:","opts":["2","3","4","5"],"ans":2},
{"q":"AIDS कारण:","opts":["Bacteria","HIV(Retrovirus)","Fungi","Protozoa"],"ans":1},
{"q":"p²+2pq+q² = ?","opts":["0","1","2","p+q"],"ans":1},
{"q":"Miller-Urey में बने:","opts":["DNA","Amino acids","RNA","Proteins"],"ans":1},
{"q":"t-RNA काम:","opts":["DNA पढ़ना","Amino acid ribosome तक","mRNA बनाना","DNA copy"],"ans":1},
{"q":"Golden Rice:","opts":["Vitamin C","Vitamin A(β-carotene)","Iron","Protein"],"ans":1},
{"q":"Adaptive radiation:","opts":["Darwin's Finches","Bacteria","Virus","Fungi"],"ans":0},
{"q":"Turner's syndrome:","opts":["45,XO","47,XXY","47,XY","46,XX"],"ans":0},
{"q":"Klinefelter's:","opts":["45,XO","47,XXY","47,XY","46,XY"],"ans":1},
{"q":"DNA replication:","opts":["S-phase","G1-phase","G2-phase","M-phase"],"ans":0},
{"q":"Human genome में जीन:","opts":["20,000-25,000","1,000","10,00,000","50,000"],"ans":0},
{"q":"Restriction enzyme:","opts":["DNA specific site पर काटना","जोड़ना","Protein","RNA"],"ans":0},
{"q":"DNA ligase:","opts":["जोड़ना","काटना","Copy","Digest"],"ans":0},
{"q":"Plasmid:","opts":["Extrachromosomal DNA","Protein","RNA","Enzyme"],"ans":0},
{"q":"Lac operon inducer:","opts":["Lactose","Glucose","Tryptophan","Galactose"],"ans":0},
{"q":"Dolly भेड़:","opts":["पहला clone स्तनधारी","पहला GM","पहला clone पक्षी","पहला clone कीट"],"ans":0},
{"q":"Mycorrhiza:","opts":["कवक-पादप जड़ सहजीवन","जीवाणु","विषाणु","परजीवी"],"ans":0},
{"q":"Hardy-Weinberg शर्त नहीं:","opts":["बड़ी जनसंख्या","यादृच्छिक","उत्परिवर्तन","चयन का अभाव"],"ans":2},
{"q":"Oogenesis:","opts":["1 Egg+3 Polar bodies","4 Eggs","2 Eggs","1 Egg only"],"ans":0},
{"q":"स्वतंत्र अपव्यूहन:","opts":["भिन्न गुणसूत्रों पर","एक ही पर","सहलग्न","लिंग गुणसूत्र"],"ans":0},
{"q":"Crossing over:","opts":["Prophase-I","Metaphase-I","Anaphase-I","Telophase-I"],"ans":0},
{"q":"हीमोफीलिया:","opts":["X-linked recessive","X-linked dominant","Autosomal recessive","Autosomal dominant"],"ans":0},
{"q":"वर्णान्धता:","opts":["X-linked recessive","Y-linked","Autosomal dominant","Autosomal recessive"],"ans":0},
{"q":"Ecosystem ऊर्जा प्रवाह:","opts":["एकदिशीय","द्विदिशीय","चक्रीय","कोई नहीं"],"ans":0},
{"q":"Primary productivity मापी:","opts":["g/m²/year","g/m³","g/L","mol/L"],"ans":0},
{"q":"जैव विविधता हॉटस्पॉट भारत:","opts":["पश्चिमी घाट","थार","गंगा का मैदान","विंध्याचल"],"ans":0},
{"q":"Critically Endangered:","opts":["विलुप्ति के कगार पर","संकटग्रस्त","सुभेद्य","कम चिंता"],"ans":0},
{"q":"Biomagnification:","opts":["DDT की सांद्रता बढ़ना","O₂","CO₂","जल"],"ans":0},
{"q":"Greenhouse effect:","opts":["Global warming","cooling","Ozone वृद्धि","UV घटती"],"ans":0},
{"q":"CFC से:","opts":["Ozone क्षरण","वृद्धि","CO₂","N₂"],"ans":0},
{"q":"Chipko movement:","opts":["वन संरक्षण","जल","मृदा","वायु"],"ans":0},
{"q":"Biogas मुख्य घटक:","opts":["Methane","CO₂","H₂","N₂"],"ans":0},
{"q":"Ex-situ conservation:","opts":["Botanical Garden","National Park","Wildlife Sanctuary","Biosphere Reserve"],"ans":0},
{"q":"Vector:","opts":["Plasmid","Restriction enzyme","Ligase","Polymerase"],"ans":0},
{"q":"Host:","opts":["E. coli","Virus","Fungi","Human cell"],"ans":0},
{"q":"Bt cotton gene:","opts":["Bacillus thuringiensis","Agrobacterium","Rhizobium","E. coli"],"ans":0},
{"q":"Insulin vector:","opts":["Plasmid","Chromosome","Ribosome","Mitochondria"],"ans":0},
{"q":"DNA fingerprinting:","opts":["VNTR","PCR","Gel electrophoresis","सभी"],"ans":3},
{"q":"Codon:","opts":["3 nucleotide","2","4","1"],"ans":0},
{"q":"70S ribosome:","opts":["Prokaryotes","Eukaryotes","दोनों","किसी में नहीं"],"ans":0},
{"q":"Transcription में:","opts":["mRNA","Protein","DNA","tRNA"],"ans":0},
{"q":"HGP में chromosomes:","opts":["23 जोड़े","24 जोड़े","46","22"],"ans":0},
{"q":"Apiculture:","opts":["मधुमक्खी","रेशम","मत्स्य","मुर्गी"],"ans":0},
{"q":"Sericulture:","opts":["रेशम कीट","मधुमक्खी","मत्स्य","मुर्गी"],"ans":0},
{"q":"IVF:","opts":["In Vitro Fertilization","In Vivo","In Vitro Formation","None"],"ans":0},
{"q":"MOET:","opts":["बहु अण्डोत्सर्ग+भ्रूण स्थानांतरण","IVF","AI","cloning"],"ans":0},
{"q":"Green Revolution:","opts":["अधिक उपज फसलें","दुग्ध","मत्स्य","रेशम"],"ans":0},
{"q":"White Revolution:","opts":["दुग्ध","अनाज","मत्स्य","रेशम"],"ans":0},
{"q":"Nitrogen fixation:","opts":["Rhizobium","Nitrosomonas","Nitrobacter","E. coli"],"ans":0},
{"q":"Food chain ऊर्जा:","opts":["10% आगे","50%","90%","100%"],"ans":0},
{"q":"Energy pyramid:","opts":["सदा सीधा","उल्टा","दोनों","स्थिति अनुसार"],"ans":0},
{"q":"Biomass pyramid उल्टा:","opts":["Aquatic में","Terrestrial में","सभी में","किसी में नहीं"],"ans":0},
{"q":"Mutualism उदाहरण:","opts":["Lichens","Parasite-Host","Predator-Prey","Competition"],"ans":0},
{"q":"Commensalism:","opts":["एक लाभ-दूसरे को न लाभ न हानि","दोनों लाभ","दोनों हानि","एक हानि"],"ans":0},
{"q":"Darwin प्राकृतिक चयन आधार:","opts":["Variation","Mutation","Recombination","Gene flow"],"ans":0},
{"q":"Industrial Melanism:","opts":["Biston betularia","Darwin's Finches","Galapagos turtle","Sea horse"],"ans":0},
{"q":"Analogous organs:","opts":["पक्षी पंख+तितली पंख","मनुष्य हाथ+चमगादड़","व्हेल flipper","घोड़े पैर"],"ans":0},
{"q":"Homologous organs:","opts":["मनुष्य हाथ+चमगादड़ पंख","पक्षी+तितली","मछली fin","सभी"],"ans":0},
{"q":"Vestigial organ:","opts":["Appendix","Heart","Kidney","Liver"],"ans":0},
{"q":"Meiosis में:","opts":["4 haploid cells","2 diploid","4 diploid","2 haploid"],"ans":0},
{"q":"Mitosis में:","opts":["2 diploid cells","4 haploid","4 diploid","2 haploid"],"ans":0},
{"q":"Spermatogenesis:","opts":["4 sperms","1","2","3"],"ans":0},
{"q":"Totipotency:","opts":["Plant cells","Animal cells","केवल stem cells","कोई नहीं"],"ans":0},
{"q":"Somatic hybridization:","opts":["Protoplast fusion","DNA injection","Agrobacterium","PCR"],"ans":0},
{"q":"Test tube baby:","opts":["IVF+ET","AI","MOET","Cloning"],"ans":0},
{"q":"Bioremediation:","opts":["Microorganisms","Chemicals","Physical","Radiation"],"ans":0},
{"q":"CRISPR-Cas9:","opts":["Gene editing","DNA sequencing","Protein synthesis","Cell division"],"ans":0},
{"q":"Stem cells:","opts":["Self-renewal+Differentiation","केवल division","केवल diff","कोई नहीं"],"ans":0},
{"q":"Probiotic:","opts":["Lactobacillus","E. coli","Salmonella","Vibrio"],"ans":0},
{"q":"Biowar:","opts":["Anthrax","Penicillin","Insulin","Vaccine"],"ans":0},
{"q":"Aquaculture:","opts":["मत्स्य","मधुमक्खी","रेशम","मुर्गी"],"ans":0},
{"q":"Biofortification:","opts":["पोषक तत्व बढ़ाना","उपज","रोग","कीट"],"ans":0},
{"q":"SCP:","opts":["Spirulina","Rice","Wheat","Maize"],"ans":0},
{"q":"Biopesticide:","opts":["Bacillus thuringiensis","DDT","Malathion","Endrin"],"ans":0},
{"q":"Biofuel:","opts":["Ethanol from sugarcane","Petrol","Diesel","Coal"],"ans":0},
{"q":"Transgenic crop:","opts":["Bt cotton","Normal cotton","Organic cotton","Wild cotton"],"ans":0},
{"q":"Gene therapy:","opts":["Defective gene correct","Surgery","Medicine","Radiation"],"ans":0},
{"q":"Molecular clock:","opts":["DNA mutation rate","Protein structure","Cell division","Fossil record"],"ans":0},
{"q":"Blue Revolution:","opts":["मत्स्य उत्पादन","दुग्ध","कृषि","रेशम"],"ans":0},
{"q":"Yellow Revolution:","opts":["तिलहन","दुग्ध","मत्स्य","फल"],"ans":0},
]

HIN_OBJ = [
{"q":"सूरदास की भाषा:","opts":["ब्रज","अवधी","मैथिली","खड़ीबोली"],"ans":0},
{"q":"'कैदी और कोकिला' रचयिता:","opts":["माखनलाल चतुर्वेदी","पंत","महादेवी","निराला"],"ans":0},
{"q":"महादेवी वर्मा युग:","opts":["भारतेन्दु","द्विवेदी","छायावाद","प्रगतिवाद"],"ans":2},
{"q":"'उत्साह' में बादल प्रतीक:","opts":["विनाश","क्रान्ति","सृजन","शान्ति"],"ans":1},
{"q":"'अट नहीं रही है' ऋतु:","opts":["वसन्त","वर्षा","ग्रीष्म","शीत"],"ans":0},
{"q":"'रति' किस रस में:","opts":["शृंगार","वीर","करुण","हास्य"],"ans":0},
{"q":"भारतेन्दु युग प्रवर्तक:","opts":["भारतेन्दु हरिश्चन्द्र","द्विवेदी","अयोध्या सिंह","प्रेमचन्द"],"ans":0},
{"q":"अनुप्रास का सम्बन्ध:","opts":["अर्थ","शब्द","भाव","रस"],"ans":1},
{"q":"दोहा विषम चरण मात्राएँ:","opts":["11","13","16","24"],"ans":1},
{"q":"'बाजार दर्शन' लेखक:","opts":["जैनेन्द्र","हजारी प्रसाद","अज्ञेय","धर्मवीर"],"ans":0},
{"q":"'बहादुर' लेखक:","opts":["प्रेमचन्द","रेणु","अमरकान्त","भीष्म साहनी"],"ans":2},
{"q":"कर्ता कारक:","opts":["को","से","ने","के लिए"],"ans":2},
{"q":"'विद्यालय' में संधि:","opts":["यण","गुण","वृद्धि","दीर्घ"],"ans":1},
{"q":"'अग्नि' पर्यायवाची:","opts":["पावक","अनल","आग","सभी"],"ans":3},
{"q":"'आम के आम...' अर्थ:","opts":["दोहरा लाभ","हानि","कठोर श्रम","व्यर्थ"],"ans":0},
{"q":"निबन्ध अंग:","opts":["भूमिका,विषय-विस्तार,उपसंहार","केवल प्रस्तावना","केवल निष्कर्ष","तर्क"],"ans":0},
{"q":"'आँसू' विधा:","opts":["खण्डकाव्य","महाकाव्य","गीतिकाव्य","मुक्तक"],"ans":2},
{"q":"रामचरितमानस भाषा:","opts":["संस्कृत","ब्रज","अवधी","हिंदी"],"ans":2},
{"q":"उपसर्ग जुड़ता है:","opts":["अन्त में","बीच में","आरम्भ में","कहीं भी"],"ans":2},
{"q":"'कामायनी' रचनाकार:","opts":["निराला","जयशंकर प्रसाद","महादेवी","पंत"],"ans":1},
{"q":"हिंदी 'स्वर्ण युग':","opts":["आदिकाल","भक्तिकाल","रीतिकाल","आधुनिककाल"],"ans":1},
{"q":"'गोदान' लेखक:","opts":["प्रेमचंद","जैनेंद्र","यशपाल","भगवतीचरण"],"ans":0},
{"q":"वीर रस स्थायी भाव:","opts":["भय","उत्साह","रति","क्रोध"],"ans":1},
{"q":"करुण रस स्थायी भाव:","opts":["शोक","हास","रति","विस्मय"],"ans":0},
{"q":"'मधुशाला' रचयिता:","opts":["पंत","बच्चन","महादेवी","निराला"],"ans":1},
{"q":"छायावाद में नहीं:","opts":["प्रसाद","निराला","पंत","भारतेंदु"],"ans":3},
{"q":"'आँखें चुराना' अर्थ:","opts":["आँख छिपाना","सामने न आना","शर्माना","झूठ बोलना"],"ans":1},
{"q":"हिंदी दिवस:","opts":["14 सितंबर","14 अक्टूबर","26 जनवरी","15 अगस्त"],"ans":0},
{"q":"संधि भेद:","opts":["2","3","4","5"],"ans":1},
{"q":"रामचंद्र शुक्ल:","opts":["हिंदी साहित्य का इतिहास","कविता क्या है","चिंतामणि","रस मीमांसा"],"ans":0},
{"q":"'तारसप्तक' संपादन:","opts":["निराला","अज्ञेय","पंत","बच्चन"],"ans":1},
{"q":"पृथ्वीराज रासो:","opts":["जयदेव","चंदबरदाई","विद्यापति","खुसरो"],"ans":1},
{"q":"आदिकाल दूसरा नाम:","opts":["भक्तिकाल","वीरगाथाकाल","रीतिकाल","छायावाद"],"ans":1},
{"q":"कबीर शाखा:","opts":["सगुण भक्ति","निर्गुण ज्ञानमार्गी","प्रेममार्गी","रीति"],"ans":1},
{"q":"'पद्मावत' रचयिता:","opts":["कबीर","तुलसी","जायसी","सूरदास"],"ans":2},
{"q":"प्रेमचंद मूल नाम:","opts":["धनपत राय","श्रीपत राय","नवाब राय","मुंशीलाल"],"ans":0},
{"q":"'साकेत' रचयिता:","opts":["प्रसाद","मैथिलीशरण गुप्त","दिनकर","पंत"],"ans":1},
{"q":"रीतिकाल प्रमुख कवि:","opts":["कबीर","सूरदास","बिहारी","तुलसी"],"ans":2},
{"q":"द्वंद्व समास:","opts":["राम-कृष्ण","राजपुत्र","नीलकमल","पंचवटी"],"ans":0},
{"q":"बहुव्रीहि समास:","opts":["चतुर्भुज","राजमहल","पीतांबर","यथाशक्ति"],"ans":2},
{"q":"हिंदी प्रथम उपन्यास:","opts":["गोदान","परीक्षागुरु","चंद्रकांता","भाग्यवती"],"ans":1},
{"q":"कारक भेद:","opts":["6","7","8","9"],"ans":2},
{"q":"मुक्त छंद प्रवर्तक:","opts":["तुलसी","कबीर","निराला","प्रसाद"],"ans":2},
{"q":"श्लेष अलंकार:","opts":["एक अर्थ","एक शब्द दो अर्थ","उपमा","रूपक"],"ans":1},
{"q":"'हालावाद' प्रवर्तक:","opts":["निराला","बच्चन","पंत","प्रसाद"],"ans":1},
{"q":"संप्रदान कारक विभक्ति:","opts":["को/के लिए","से","में","पर"],"ans":0},
{"q":"प्रेमचंद का उपन्यास नहीं:","opts":["रंगभूमि","सेवासदन","निर्मला","शेखर"],"ans":3},
{"q":"हिंदी भाषा:","opts":["बोली","भाषा","उपभाषा","विभाषा"],"ans":1},
{"q":"'कफन' लेखक:","opts":["प्रसाद","प्रेमचंद","अज्ञेय","मोहन राकेश"],"ans":1},
{"q":"सूरदास भाषा:","opts":["अवधी","ब्रजभाषा","खड़ीबोली","संस्कृत"],"ans":1},
{"q":"अव्ययीभाव समास:","opts":["यथाशक्ति","राजपुत्र","नीलकमल","पंचवटी"],"ans":0},
{"q":"तत्पुरुष समास:","opts":["राजमहल","नीलकमल","पंचवटी","यथाशक्ति"],"ans":0},
{"q":"वाच्य भेद:","opts":["2","3","4","5"],"ans":1},
{"q":"उपमा अलंकार:","opts":["जैसे,सा,सी,सम","मानो","रूपक","श्लेष"],"ans":0},
{"q":"रूपक अलंकार:","opts":["उपमेय पर उपमान का आरोप","तुलना","विरोधाभास","श्लेष"],"ans":0},
{"q":"'आधुनिक मीरा':","opts":["वेदना काव्य","भक्ति","कृष्ण भक्ति","प्रकृति"],"ans":0},
{"q":"'नौ-दो ग्यारह' अर्थ:","opts":["गणित","भाग जाना","लड़ाई","समझाना"],"ans":1},
{"q":"हिंदी स्वर:","opts":["11","13","14","16"],"ans":0},
{"q":"देवनागरी दिशा:","opts":["दाएँ से बाएँ","बाएँ से दाएँ","ऊपर से नीचे","नीचे से ऊपर"],"ans":1},
{"q":"प्रयोगवाद प्रवर्तक:","opts":["निराला","पंत","अज्ञेय","दिनकर"],"ans":2},
{"q":"भक्तिकाल समय:","opts":["1000-1375","1375-1700","1700-1900","1900 के बाद"],"ans":1},
{"q":"आधुनिक हिंदी गद्य जनक:","opts":["प्रेमचंद","भारतेंदु","शुक्ल","द्विवेदी"],"ans":1},
{"q":"8वीं अनुसूची भाषाएँ:","opts":["18","20","22","24"],"ans":2},
{"q":"रेणु शैली:","opts":["शुद्ध हिंदी","आंचलिक","संस्कृत","अंग्रेजी"],"ans":1},
{"q":"गांधी जी सच्चा सुख:","opts":["उपभोग","त्याग","संग्रह","भोग"],"ans":1},
{"q":"द्विगु समास पहला पद:","opts":["संज्ञा","संख्यावाचक","विशेषण","क्रिया"],"ans":1},
{"q":"हिंदी पहली पत्रिका:","opts":["सरस्वती","उदंत मार्तंड","माधुरी","हंस"],"ans":1},
{"q":"रस के अंग:","opts":["2","3","4","5"],"ans":2},
{"q":"'अंधे की लाठी' अर्थ:","opts":["एकमात्र सहारा","कमजोर","बेकार","अंधकार"],"ans":0},
{"q":"'उर्वशी' ज्ञानपीठ:","opts":["प्रसाद","दिनकर","पंत","निराला"],"ans":1},
{"q":"'यामा' ज्ञानपीठ:","opts":["महादेवी","सुभद्रा","मीराबाई","अमृता"],"ans":0},
{"q":"संज्ञा भेद:","opts":["3","4","5","6"],"ans":2},
{"q":"हिंदी उत्पत्ति:","opts":["पाली","प्राकृत","अपभ्रंश","संस्कृत"],"ans":2},
{"q":"काव्य प्रमुख भेद:","opts":["प्रबंध और मुक्तक","खंड और महा","गद्य और पद्य","सगुण-निर्गुण"],"ans":0},
{"q":"तुलसी भक्ति:","opts":["सगुण राम भक्ति","निर्गुण","कृष्ण","शक्ति"],"ans":0},
{"q":"'कमीज' किस भाषा से:","opts":["अरबी","फारसी","पुर्तगाली","अंग्रेजी"],"ans":2},
{"q":"प्रत्यय:","opts":["आगे","पीछे","बीच","कहीं"],"ans":1},
{"q":"'राम की शक्तिपूजा':","opts":["तुलसी","निराला","प्रसाद","पंत"],"ans":1},
{"q":"छायावाद समय:","opts":["1900-1918","1918-1936","1936-1950","1950 के बाद"],"ans":1},
{"q":"द्विवेदी पत्रिका:","opts":["हंस","सरस्वती","माधुरी","मतवाला"],"ans":1},
{"q":"राजभाषा अनुच्छेद:","opts":["340","343","370","356"],"ans":1},
{"q":"निराला पूरा नाम:","opts":["सूर्यकांत त्रिपाठी","रामकुमार वर्मा","भारतेंदु","हजारीप्रसाद"],"ans":0},
{"q":"बिहारी सतसई दोहे:","opts":["500","600","700","800"],"ans":2},
{"q":"तद्भव अर्थ:","opts":["संस्कृत से सीधे","संस्कृत से बदलकर","विदेशी","देशज"],"ans":1},
{"q":"हिंदी पहली कहानी:","opts":["उसने कहा था","इंदुमती","परीक्षा गुरु","कफन"],"ans":1},
{"q":"'कमल' पर्याय:","opts":["पद्म","कुमुद","नीरज","सभी"],"ans":3},
{"q":"'सुगम' विलोम:","opts":["दुर्गम","सरल","कठिन","विकट"],"ans":0},
{"q":"शब्द-शक्ति भेद:","opts":["2","3","4","5"],"ans":1},
{"q":"'भारत-दुर्दशा' लेखक:","opts":["प्रेमचंद","भारतेंदु","बालकृष्ण भट्ट","प्रतापनारायण"],"ans":1},
{"q":"'पंच परमेश्वर' पात्र:","opts":["जुम्मन शेख","अलगू चौधरी","हामिद","दोनों A और B"],"ans":3},
{"q":"सर्वनाम भेद:","opts":["4","5","6","7"],"ans":2},
{"q":"क्रिया भेद:","opts":["2","3","4","5"],"ans":0},
{"q":"'आनंदमठ' भाषा:","opts":["हिंदी","बांग्ला","संस्कृत","उर्दू"],"ans":1},
{"q":"निबन्ध प्रकार:","opts":["2","3","4","5"],"ans":1},
{"q":"'नमक का दारोगा' लेखक:","opts":["प्रसाद","प्रेमचंद","यशपाल","जैनेंद्र"],"ans":1},
{"q":"रामचरितमानस काण्ड:","opts":["5","6","7","8"],"ans":2},
{"q":"आत्मकथा में:","opts":["दूसरे की कथा","अपनी कथा","काल्पनिक","ऐतिहासिक"],"ans":1},
{"q":"'तारसप्तक' वर्ष:","opts":["1940","1943","1950","1955"],"ans":1},
{"q":"'चंद्रकांता' लेखक:","opts":["प्रेमचंद","देवकीनंदन खत्री","भगवतीचरण","यशपाल"],"ans":1},
]

ENG_OBJ = [
{"q":"'The Last Lesson' writer:","opts":["Alphonse Daudet","Anees Jung","William Douglas","Selma Lagerlof"],"ans":0},
{"q":"'Lost Spring' theme:","opts":["Poverty/exploitation","Education","Sports","Science"],"ans":0},
{"q":"'Deep Water' fear of:","opts":["Water","Fire","Heights","Darkness"],"ans":0},
{"q":"'Indigo' author:","opts":["Louis Fischer","Gandhi","Nehru","Tagore"],"ans":0},
{"q":"'My Mother at Sixty-Six' writer:","opts":["Kamala Das","Neruda","Keats","Frost"],"ans":0},
{"q":"'Keeping Quiet' poet:","opts":["Pablo Neruda","Kamala Das","Frost","Keats"],"ans":0},
{"q":"'A Thing of Beauty' gives:","opts":["Joy forever","Sadness","Pain","Wealth"],"ans":0},
{"q":"Aunt Jennifer's tigers are:","opts":["embroidered","real","painted","carved"],"ans":0},
{"q":"He ____ to school daily.","opts":["goes","go","going","gone"],"ans":0},
{"q":"Passive: 'She writes a letter':","opts":["A letter is written by her","A letter was written","She is written","A letter writes her"],"ans":0},
{"q":"Synonym of 'happy':","opts":["joyful","sad","angry","tired"],"ans":0},
{"q":"Antonym of 'brave':","opts":["coward","bold","courageous","fearless"],"ans":0},
{"q":"Indirect: 'I am ill.':","opts":["He said that he was ill","he said I am ill","He says he is ill","He told he was ill"],"ans":0},
{"q":"'Life is a dream':","opts":["Metaphor","Simile","Personification","Hyperbole"],"ans":0},
{"q":"Plural of 'child':","opts":["children","childs","childes","childrens"],"ans":0},
{"q":"'The Tiger King' protagonist:","opts":["Maharaja of Pratibandapuram","Sir James","astrologer","British officer"],"ans":0},
{"q":"'The Third Level' led to:","opts":["Galesburg 1894","New York","London","Paris"],"ans":0},
{"q":"___ European country:","opts":["A","An","The","No article"],"ans":0},
{"q":"Superlative of 'good':","opts":["gooder","better","best","most good"],"ans":2},
{"q":"Modal for 'possibility':","opts":["must","shall","may","will"],"ans":2},
{"q":"I have ___ there:","opts":["went","gone","go","going"],"ans":1},
{"q":"'Under the weather':","opts":["outside in rain","feeling ill","very happy","working hard"],"ans":1},
{"q":"Biography by oneself:","opts":["Biography","Autobiography","Memoir","Diary"],"ans":1},
{"q":"'Like' or 'as' figure of speech:","opts":["Metaphor","Simile","Personification","Hyperbole"],"ans":1},
{"q":"Gerund in 'Swimming is good':","opts":["is","good","Swimming","health"],"ans":2},
{"q":"Correct sentence:","opts":["He is more taller","He is tallest","He is taller","He is most tallest"],"ans":2},
{"q":"'Yours faithfully' when:","opts":["You know person","You don't know","Friend","Always"],"ans":1},
{"q":"Compound sentence:","opts":["She sings.","She sings and dances.","She sings because happy.","The girl who sings."],"ans":1},
{"q":"Conjunction: 'tired, but I studied':","opts":["was","tired","but","studied"],"ans":2},
{"q":"The news __ good:","opts":["are","is","were","have been"],"ans":1},
{"q":"She ____ for two hours:","opts":["has been studying","is studying","studied","studies"],"ans":0},
{"q":"Shakespeare's period:","opts":["Victorian","Romantic","Elizabethan","Modern"],"ans":2},
{"q":"'Ode to a Nightingale' by:","opts":["Wordsworth","Keats","Shelley","Byron"],"ans":1},
{"q":"Correct conditional:","opts":["If it rains, I will stay","If it will rain, I stay","If it rained, I will stay","If it rain, I stay"],"ans":0},
{"q":"Correct spelling:","opts":["accomodation","accommodation","accomadation","acomodation"],"ans":1},
{"q":"'Brevity is soul of wit':","opts":["Hamlet","Polonius","Othello","Macbeth"],"ans":1},
{"q":"'Break the ice':","opts":["break something","end awkwardness","cool down","make friends"],"ans":1},
{"q":"Interjection: 'Wow, what a painting!':","opts":["what","beautiful","painting","Wow"],"ans":3},
{"q":"NOT a tense:","opts":["Present Perfect","Past Continuous","Future Definite","Simple Past"],"ans":2},
{"q":"Word modifying verb:","opts":["Adjective","Adverb","Noun","Pronoun"],"ans":1},
{"q":"'A Roadside Stand' about:","opts":["rural-urban divide","nature","love","travel"],"ans":0},
{"q":"Homophone of 'right':","opts":["write","rite","wright","all of these"],"ans":3},
{"q":"Collective noun:","opts":["dog","flock","run","beautiful"],"ans":1},
{"q":"Good __ mathematics:","opts":["in","at","on","for"],"ans":1},
{"q":"'Will you please help me?'","opts":["Declarative","Interrogative","Imperative","Exclamatory"],"ans":2},
{"q":"CV full form:","opts":["Career Vision","Curriculum Vitae","Creative Vision","Career Value"],"ans":1},
{"q":"Alliteration:","opts":["She sells seashells","As brave as lion","Life is journey","He ran quickly"],"ans":0},
{"q":"Opposite of 'optimist':","opts":["realist","pessimist","idealist","socialist"],"ans":1},
{"q":"Looking forward to __ you:","opts":["meet","meeting","met","meets"],"ans":1},
{"q":"Proper noun:","opts":["city","river","Ganga","mountain"],"ans":2},
{"q":"Tag for 'She is smart':","opts":["is she?","isn't she?","doesn't she?","wasn't she?"],"ans":1},
{"q":"'un-'+'happy':","opts":["inhappy","unhappy","dishappy","mishappy"],"ans":1},
{"q":"Linking verb:","opts":["run","sing","seem","jump"],"ans":2},
{"q":"Correct spelling:","opts":["grammer","grammar","gramer","gramar"],"ans":1},
{"q":"'We' objective case:","opts":["our","ours","us","ourselves"],"ans":2},
{"q":"'Protagonist':","opts":["villain","main character","narrator","minor character"],"ans":1},
{"q":"ABAB rhyme:","opts":["1,2 rhyme;3,4","1,3 rhyme;2,4","all rhyme","no rhyme"],"ans":1},
{"q":"Study of meaning:","opts":["Phonology","Syntax","Semantics","Morphology"],"ans":2},
{"q":"Neither __ present:","opts":["are","is","were","have been"],"ans":1},
{"q":"Prefix 'against':","opts":["pro-","anti-","pre-","post-"],"ans":1},
{"q":"'Catch-22':","opts":["easy solution","no-win situation","lucky","difficult"],"ans":1},
{"q":"'A letter was written by him':","opts":["He writes","He wrote","He is writing","He will write"],"ans":1},
{"q":"Haiku:","opts":["14-line","Japanese 3-line 5-7-5","8-line","Rhyming couplet"],"ans":1},
{"q":"Direct: She said she was tired:","opts":["'I am tired.'","'She is tired.'","'I was tired.'","'You are tired.'"],"ans":0},
{"q":"Obligation modal:","opts":["can","may","must","might"],"ans":2},
{"q":"'mis-' means:","opts":["again","wrongly","not","before"],"ans":1},
{"q":"There __ many students:","opts":["is","are","was","has been"],"ans":1},
{"q":"NOT type of essay:","opts":["Descriptive","Argumentative","Persuasive","Imaginative"],"ans":3},
{"q":"Infinitive: 'She wants to dance':","opts":["She","wants","to dance","dance"],"ans":2},
{"q":"By next year, she __ degree:","opts":["completes","will complete","will have completed","completed"],"ans":2},
{"q":"'The Road Not Taken' theme:","opts":["War","Nature","Individual choice","Death"],"ans":2},
{"q":"'Verbose':","opts":["silent","too many words","brief","poetic"],"ans":1},
{"q":"Subject: 'Running keeps fit':","opts":["every day","keeps","Running every day","you"],"ans":2},
{"q":"He is __ his father:","opts":["alike","like","likely","likewise"],"ans":1},
{"q":"First person uses:","opts":["he/she","I/we","you","they"],"ans":1},
{"q":"She ____ here since 2020:","opts":["works","worked","has been working","is working"],"ans":2},
{"q":"NOT a mood:","opts":["Indicative","Subjunctive","Imperative","Descriptive"],"ans":3},
{"q":"'Empathy':","opts":["lack of feeling","understanding feelings","sympathy","apathy"],"ans":1},
{"q":"'The Enemy' writer:","opts":["Pearl S. Buck","John Updike","Jack Finney","Kalki"],"ans":0},
{"q":"'Going Places' author:","opts":["A.R. Barton","Susan Hill","Jack Finney","John Updike"],"ans":0},
{"q":"Dr. Sadao was:","opts":["Japanese surgeon","American doctor","British officer","Chinese scientist"],"ans":0},
{"q":"'Poets and Pancakes' about:","opts":["Gemini Studios","Hollywood","bakery","school"],"ans":0},
{"q":"Tiger king died because:","opts":["wooden toy tiger","real tiger","disease","war"],"ans":0},
{"q":"The peddler stole:","opts":["thirty kronor","watch","jewellery","food"],"ans":0},
{"q":"'The Last Lesson' set in:","opts":["Alsace","Paris","Berlin","London"],"ans":0},
{"q":"Dangling modifier:","opts":["Running fast, he caught bus","Running fast, the bus was caught","He ran to catch bus","Bus was caught"],"ans":1},
{"q":"'Actions speak louder':","opts":["Talk more","Actions important","Both equal","Words matter"],"ans":1},
{"q":"Exclamatory:","opts":["She is smart.","Is she smart?","Aha! I found it!","Be quiet."],"ans":2},
{"q":"Conjunction:","opts":["beautiful","although","quickly","table"],"ans":1},
{"q":"'Animal Farm' writer:","opts":["Aldous Huxley","George Orwell","H.G. Wells","Thomas Hardy"],"ans":1},
{"q":"Sonnet lines:","opts":["12","14","16","18"],"ans":1},
{"q":"Personification gives:","opts":["color","shape","human qualities","sound"],"ans":2},
{"q":"'I enjoy reading':","opts":["infinitive","gerund","participle","verb"],"ans":1},
{"q":"Concrete noun:","opts":["love","happiness","table","anger"],"ans":2},
{"q":"'A stitch in time' is:","opts":["Metaphor","Idiom","Proverb","Simile"],"ans":2},
{"q":"'Photograph' syllables:","opts":["2","3","4","5"],"ans":1},
{"q":"I saw him __ (correct):","opts":["I have seen him yesterday","I saw him yesterday","I had seen him yesterday","I see him yesterday"],"ans":1},
]

MAT_OBJ = [
{"q":"f(x)=x²+1, f(-1)=","opts":["2","1","0","-1"],"ans":0},
{"q":"sin⁻¹(1/2)=","opts":["π/6","π/3","π/4","π/2"],"ans":0},
{"q":"|[[1,2],[3,4]]|=","opts":["-2","2","10","-10"],"ans":0},
{"q":"d/dx(sinx)=","opts":["cosx","-cosx","sinx","-sinx"],"ans":0},
{"q":"∫x dx=","opts":["x²/2+C","x²+C","2x²+C","x³/3+C"],"ans":0},
{"q":"∫₀¹x²dx=","opts":["1/3","1/2","1","2"],"ans":0},
{"q":"f(x)=x² निम्नतम:","opts":["x=0","x=1","x=-1","x=2"],"ans":0},
{"q":"d/dx(eˣ)=","opts":["eˣ","xeˣ","eˣ/x","1/x"],"ans":0},
{"q":"d/dx(logx)=","opts":["1/x","x","eˣ","logx"],"ans":0},
{"q":"∫cosx dx=","opts":["sinx+C","-sinx+C","cosx+C","-cosx+C"],"ans":0},
{"q":"î·ĵ=","opts":["0","1","-1","k̂"],"ans":0},
{"q":"î×ĵ=","opts":["k̂","0","1","-k̂"],"ans":0},
{"q":"चित की प्रायिकता:","opts":["1/2","1/3","1/4","1"],"ans":0},
{"q":"सम संख्या प्रायिकता:","opts":["1/2","1/3","1/6","2/3"],"ans":0},
{"q":"P(A|B)=","opts":["P(A∩B)/P(B)","P(A∩B)","P(A)","P(B)/P(A∩B)"],"ans":0},
{"q":"sin²θ+cos²θ=","opts":["0","1","2","-1"],"ans":1},
{"q":"d/dx(xⁿ)=","opts":["nxⁿ","nx^(n-1)","x^(n-1)/n","(n-1)xⁿ"],"ans":1},
{"q":"e⁰=","opts":["0","1","e","∞"],"ans":1},
{"q":"f(x)=x², f'(x)=","opts":["x","2x","x²","2x²"],"ans":1},
{"q":"P(A∪B)=0.4+0.5-0.2=","opts":["0.7","0.9","0.1","0.3"],"ans":0},
{"q":"nC₀=","opts":["n","0","1","n!"],"ans":2},
{"q":"nPr=","opts":["n!/(n-r)!","n!/r!","n!/(r!(n-r)!)","r!/n!"],"ans":0},
{"q":"AP का n वाँ पद:","opts":["a+(n-1)d","a+nd","a-(n-1)d","nd"],"ans":0},
{"q":"GP योग |r|<1:","opts":["a/(1-r)","a/(1+r)","a(1-r)","ar"],"ans":0},
{"q":"y=mx+c का ढाल:","opts":["c","m","x","y"],"ans":1},
{"q":"lim(x→0)sinx/x=","opts":["0","1","∞","-1"],"ans":1},
{"q":"3×2 आव्यूह में तत्त्व:","opts":["3","2","5","6"],"ans":3},
{"q":"∫1/x dx=","opts":["x+C","log|x|+C","1/x²+C","-1/x+C"],"ans":1},
{"q":"d/dx(tanx)=","opts":["secx","sec²x","cosec²x","-cosec²x"],"ans":1},
{"q":"A⁻¹ तब:","opts":["|A|=0","|A|≠0","A=I","A=0"],"ans":1},
{"q":"A·(B×C) समतलीय:","opts":["1","|A||B||C|","0","∞"],"ans":2},
{"q":"लम्बवत् डॉट:","opts":["|A||B|","0","1","-1"],"ans":1},
{"q":"LPP इष्टतम:","opts":["किसी भी","मूल","कोने के","मध्य"],"ans":2},
{"q":"f''(c)>0 तो:","opts":["उच्चतम","निम्नतम","विभक्ति","अपरिभाषित"],"ans":1},
{"q":"द्विपद माध्य:","opts":["np","npq","√(npq)","p/n"],"ans":0},
{"q":"∫sec²x dx=","opts":["secx+C","tanx+C","-cotx+C","secxtanx+C"],"ans":1},
{"q":"∫tanx dx=","opts":["sec²x+C","log|cosx|+C","-log|cosx|+C","log|secx|+C"],"ans":2},
{"q":"cos(A+B)=","opts":["cosAcosB+sinAsinB","cosAcosB-sinAsinB","sinAcosB+cosAsinB","sinAcosB-cosAsinB"],"ans":1},
{"q":"0!=","opts":["0","1","अपरिभाषित","∞"],"ans":1},
{"q":"sin(-θ)=","opts":["sinθ","-sinθ","cosθ","-cosθ"],"ans":1},
{"q":"d/dx(sin⁻¹x)=","opts":["1/√(1-x²)","-1/√(1-x²)","1/(1+x²)","-1/(1+x²)"],"ans":0},
{"q":"d/dx(tan⁻¹x)=","opts":["1/√(1-x²)","1/(1+x²)","-1/(1+x²)","1/√(1+x²)"],"ans":1},
{"q":"|3 2;1 4|=","opts":["10","14","11","12"],"ans":0},
{"q":"x-अक्ष समीकरण:","opts":["x=0","y=0","z=0","x=y"],"ans":1},
{"q":"सममित आव्यूह:","opts":["aᵢⱼ=aⱼᵢ","aᵢⱼ=-aⱼᵢ","aᵢⱼ=0","aᵢⱼ=1"],"ans":0},
{"q":"MVT में f'(c)=","opts":["f(b)-f(a)","f(b)+f(a)","[f(b)-f(a)]/(b-a)","f(a)/f(b)"],"ans":2},
{"q":"∫₀^π sinx dx=","opts":["0","1","2","π"],"ans":2},
{"q":"dy/dx=y हल:","opts":["y=x+C","y=Ceˣ","y=eˣ+C","y=Cx"],"ans":1},
{"q":"अभिलम्ब ax+by+cz+d=0:","opts":["(d,0,0)","(a,b,c)","(b,c,d)","(a,b,d)"],"ans":1},
{"q":"l²+m²+n²=","opts":["0","1","2","3"],"ans":1},
{"q":"A×A=","opts":["|A|²","A²","0","2A"],"ans":2},
{"q":"f'(x)>0 तो f:","opts":["वर्धमान","ह्रासमान","स्थिर","अपरिभाषित"],"ans":0},
{"q":"y²=4ax फोकस:","opts":["(0,a)","(a,0)","(-a,0)","(0,-a)"],"ans":1},
{"q":"वृत्त e=","opts":["0","1",">1","<1"],"ans":0},
{"q":"दीर्घवृत्त e=","opts":["0","1","0<e<1","e>1"],"ans":2},
{"q":"अतिपरवलय e=","opts":["0","1","0<e<1","e>1"],"ans":3},
{"q":"√x का प्रान्त:","opts":["R","R-{0}","[0,∞)","(0,∞)"],"ans":2},
{"q":"sinx का परिसर:","opts":["R","[0,1]","[-1,1]","(0,1)"],"ans":2},
{"q":"सहखण्डज [a b;c d]:","opts":["[d -b;-c a]","[a c;b d]","[d b;c a]","[-d b;c -a]"],"ans":0},
{"q":"श्रृंखला नियम:","opts":["f'(x)·g'(x)","f'(g(x))·g'(x)","f(g'(x))","f'(x)/g'(x)"],"ans":1},
{"q":"f'(c)=0,f''(c)<0:","opts":["निम्नतम","उच्चतम","विभक्ति","अपरिभाषित"],"ans":1},
{"q":"0≤P(E)≤","opts":["0","0.5","1","∞"],"ans":2},
{"q":"n वस्तु व्यवस्था:","opts":["n","n²","n!","(n-1)!"],"ans":2},
{"q":"A.M. of a,b:","opts":["a+b","(a+b)/2","√(ab)","2ab/(a+b)"],"ans":1},
{"q":"G.M. of a,b:","opts":["(a+b)/2","√(ab)","2ab/(a+b)","a+b"],"ans":1},
{"q":"स्वतंत्र P(A∩B)=","opts":["P(A)+P(B)","P(A)-P(B)","P(A)·P(B)","P(A)/P(B)"],"ans":2},
{"q":"विषम-सममित:","opts":["aᵢⱼ=aⱼᵢ","aᵢⱼ=-aⱼᵢ","A=Aᵀ","A=I"],"ans":1},
{"q":"∫dx/(1+x²)=","opts":["sin⁻¹x+C","tan⁻¹x+C","cos⁻¹x+C","sec⁻¹x+C"],"ans":1},
{"q":"∫dx/√(1-x²)=","opts":["sin⁻¹x+C","tan⁻¹x+C","cos⁻¹x+C","-cos⁻¹x+C"],"ans":0},
{"q":"IF of dy/dx+Py=Q:","opts":["e^P","e^∫Pdx","e^Q","P/Q"],"ans":1},
{"q":"बेज सम्बन्धित:","opts":["योग","सप्रतिबंध","गुणन","स्वतंत्र"],"ans":1},
{"q":"σ=","opts":["σ²","√variance","Σxi/n","Σfi·xi"],"ans":1},
{"q":"sin30°=","opts":["√3/2","1/2","1/√2","1"],"ans":1},
{"q":"cos60°=","opts":["√3/2","1/2","1/√2","0"],"ans":1},
{"q":"tan45°=","opts":["0","1/√2","1","√3"],"ans":2},
{"q":"sin90°=","opts":["0","1/2","√3/2","1"],"ans":3},
{"q":"cos(2θ)=","opts":["2sinθcosθ","cos²θ-sin²θ","1-2sin²θ","(B)और(C)दोनों"],"ans":3},
{"q":"A×B=0 जब:","opts":["लम्बवत्","समान्तर","इकाई","शून्य"],"ans":1},
{"q":"दो बिंदु दूरी:","opts":["x₂-x₁+y₂-y₁","√[(x₂-x₁)²+(y₂-y₁)²]","(x₂-x₁)²+(y₂-y₁)²","√(x₂²+y₂²)"],"ans":1},
{"q":"x^x अवकलन:","opts":["x^x","x^(x-1)","x^x(1+logx)","x·x^(x-1)"],"ans":2},
{"q":"रोले: f'(c)=","opts":["1","0","f(a)","f(b)"],"ans":1},
{"q":"(a+b)^n व्यापक पद:","opts":["nCr·a^r·b^(n-r)","nCr·a^(n-r)·b^r","nCr·a^n·b^n","nCr·a^n/b^r"],"ans":1},
{"q":"समरेखता:","opts":["|A|=0","|A|≠0","|A|=1","|A|=-1"],"ans":0},
{"q":"f(x)=|x|, x=0 पर:","opts":["अवकलनीय","नहीं","केवल दाईं","केवल बाईं"],"ans":1},
{"q":"sinx अधिकतम:","opts":["0","π/2","1","∞"],"ans":2},
{"q":"क्षेत्रफल:","opts":["∫f(x)dx","∫ₐᵇf(x)dx","f(b)-f(a)","f'(x)"],"ans":1},
{"q":"nC₀=","opts":["0","1","n","n!"],"ans":1},
{"q":"अवकलनीय→संतत:","opts":["हाँ","नहीं","कभी-कभी","अपरिभाषित"],"ans":0},
{"q":"|I|=","opts":["0","1","-1","n"],"ans":1},
{"q":"समान्तर रेखा दिशा:","opts":["लम्बवत्","समान","अलग","विपरीत"],"ans":1},
{"q":"|2î+3ĵ+4k̂|=","opts":["√29","29","√20","9"],"ans":0},
{"q":"∫₀^(π/2)sinx dx=","opts":["0","1","2","π/2"],"ans":1},
{"q":"d/dx(cosx)=","opts":["sinx","-sinx","cosx","-cosx"],"ans":1},
]

# ─── SUBJECTIVE (2-Mark Short & 5-Mark Long Answers) ─────
PHY_S2 = [
    {"q": "1. कूलॉम के नियम का सदिश रूप लिखिए।", "a": "F = k q1 q2 / r² * r̂"},
    {"q": "2. विद्युत क्षेत्र रेखाओं के गुणधर्म लिखिए।", "a": "धन से ऋण की ओर, कभी बंद वक्र नहीं, एक-दूसरे को नहीं काटतीं।"},
    {"q": "3. गॉस के नियम का उपयोग कर गोलीय कोश के कारण विद्युत क्षेत्र ज्ञात कीजिए।", "a": "E = 0 (r < R), E = Q/(4πε₀r²) (r > R)"},
    {"q": "4. विद्युत द्विध्रुव के कारण अक्षीय स्थिति में विद्युत क्षेत्र का सूत्र लिखें।", "a": "E = (1/4πε₀) * 2p / r³"},
    {"q": "5. ओम के नियम की सीमाएँ क्या हैं?", "a": "ताप, चुम्बकीय क्षेत्र, अर्धचालकों में लागू नहीं।"},
    {"q": "6. वैद्युत वाहक बल एवं विभवान्तर में अन्तर लिखें।", "a": "EMF: खुले परिपथ का विभवान्तर; विभवान्तर: बंद परिपथ का।"},
    {"q": "7. हीटस्टोन सेतु का सिद्धान्त समझाइए।", "a": "संतुलन अवस्था में P/Q = R/S, धारामापी में शून्य विक्षेप।"},
    {"q": "8. बायो-सेवार्ट नियम लिखें एवं समझाएँ।", "a": "dB = (μ₀/4π)(Idl sinθ / r²)"},
    {"q": "9. एम्पियर का परिपथीय नियम लिखें।", "a": "∮B.dl = μ₀I"},
    {"q": "10. लेंज का नियम लिखें।", "a": "प्रेरित धारा सदैव कारण का विरोध करती है।"},
    {"q": "11. फैराडे का विद्युत चुम्बकीय प्रेरण का नियम लिखें।", "a": "ε = -dΦ/dt"},
    {"q": "12. प्रत्यावर्ती धारा एवं दिष्ट धारा में अन्तर लिखें।", "a": "AC परिमाण बदलता है, DC एक दिशा में बहती है।"},
    {"q": "13. प्रकाश के परावर्तन के नियम लिखें।", "a": "आपतन कोण = परावर्तन कोण, आपतित किरण, अभिलम्ब, परावर्तित किरण एक तल में।"},
    {"q": "14. लेंस मेकर सूत्र लिखें।", "a": "1/f = (μ-1)(1/R₁ - 1/R₂)"},
    {"q": "15. प्रकाश का पूर्ण आन्तरिक परावर्तन समझाएँ।", "a": "सघन→विरल, आपतन कोण > क्रान्तिक कोण।"},
    {"q": "16. व्यतिकरण एवं विवर्तन में अन्तर लिखें।", "a": "व्यतिकरण: दो तरंग स्रोतों से; विवर्तन: एक ही तरंगाग्र के विभिन्न भागों से।"},
    {"q": "17. यंग का द्विझिरी प्रयोग समझाइए।", "a": "फ्रिंज चौड़ाई β = λD/d"},
    {"q": "18. प्रकाश विद्युत प्रभाव क्या है?", "a": "धातु पर प्रकाश पड़ने से इलेक्ट्रॉन उत्सर्जन।"},
    {"q": "19. डी-ब्रॉग्ली तरंगदैर्ध्य का सूत्र लिखें।", "a": "λ = h/mv"},
    {"q": "20. नाभिकीय संलयन एवं विखण्डन में अन्तर लिखें।", "a": "संलयन: हल्के नाभिक जुड़ते हैं; विखण्डन: भारी नाभिक टूटते हैं।"},
    {"q": "21. द्रव्यमान क्षति एवं बन्धन ऊर्जा को समझाइए।", "a": "बन्धन ऊर्जा = Δm c²"},
    {"q": "22. N-type एवं P-type अर्धचालकों में अन्तर लिखें।", "a": "N: इलेक्ट्रॉन बहुल; P: होल बहुल।"},
    {"q": "23. P-N सन्धि डायोड का अग्र अभिनति में कार्यविधि समझाएँ।", "a": "अग्र अभिनति में धारा प्रवाहित होती है, अवक्षय परत पतली।"},
    {"q": "24. NOT गेट का प्रतीक एवं सत्यता सारणी बनाएँ।", "a": "प्रतीक: ▷○ ; सत्य सारणी: 0→1, 1→0"},
    {"q": "25. ट्रांजिस्टर के उपयोग लिखें।", "a": "प्रवर्धक, स्विच के रूप में।"},
    {"q": "26. मॉडुलन किसे कहते हैं? इसकी आवश्यकता बताएँ।", "a": "कम आवृत्ति संकेत को उच्च आवृत्ति पर ले जाना; संचरण हेतु।"},
    {"q": "27. पृथ्वी के चुम्बकीय क्षेत्र के अवयवों के नाम लिखें।", "a": "दिक्पात, नति, क्षैतिज तीव्रता।"},
    {"q": "28. विद्युत अनुनाद किसे कहते हैं?", "a": "L-C परिपथ में प्रतिबाधा न्यूनतम, धारा अधिकतम।"},
    {"q": "29. संधारित्र की प्रतिघात का सूत्र लिखें।", "a": "Xc = 1/ωC"},
    {"q": "30. शक्ति गुणांक किसे कहते हैं?", "a": "cos φ = R/Z, AC परिपथ में वास्तविक शक्ति और आभासी शक्ति का अनुपात।"},
]

PHY_S5 = [
    {"q": "1. गॉस के नियम का उपयोग कर अनन्त लम्बाई के सीधे आवेशित तार के कारण विद्युत क्षेत्र का व्यंजक प्राप्त करें।", "a": "E = λ/(2πε₀r)"},
    {"q": "2. समान्तर प्लेट संधारित्र की धारिता का सूत्र प्राप्त करें। सिद्ध करें कि आवेशित संधारित्र में संचित ऊर्जा = ½CV² होती है।", "a": "C = ε₀A/d, U = ½CV²"},
    {"q": "3. किरचॉफ के नियमों की सहायता से हीटस्टोन सेतु का सिद्धान्त स्थापित करें।", "a": "P/Q = R/S (संतुलन)"},
    {"q": "4. बायो-सेवार्ट नियम का उपयोग कर धारावाही वृत्ताकार पाश के अक्ष पर चुम्बकीय क्षेत्र का व्यंजक प्राप्त करें।", "a": "B = (μ₀IR²) / [2(R² + x²)^(3/2)]"},
    {"q": "5. प्रत्यावर्ती धारा परिपथ में श्रेणीक्रम L-C-R परिपथ के लिए प्रतिबाधा एवं शक्ति गुणांक का व्यंजक ज्ञात करें।", "a": "Z = √(R²+(X_L-X_C)²), cosφ = R/Z"},
    {"q": "6. ट्रांसफार्मर की संरचना, कार्यविधि एवं सिद्धान्त का विस्तृत वर्णन करें।", "a": "Vp/Vs = Np/Ns, अन्योन्य प्रेरण"},
    {"q": "7. प्रकाश के व्यतिकरण के लिए आवश्यक शर्तें लिखते हुए यंग के द्विझिरी प्रयोग में फ्रिंज चौड़ाई का सूत्र प्राप्त करें।", "a": "β = λD/d"},
    {"q": "8. सरल सूक्ष्मदर्शी एवं संयुक्त सूक्ष्मदर्शी की संरचना, कार्यविधि एवं आवर्धन क्षमता का सूत्र प्राप्त करें।", "a": "सरल: m = 1 + D/f ; संयुक्त: m = L/f₀ × D/fₑ"},
    {"q": "9. प्रकाश विद्युत प्रभाव के आधार पर आइंस्टीन का प्रकाश विद्युत समीकरण प्राप्त करें एवं प्रायोगिक निष्कर्षों की व्याख्या करें।", "a": "hν = φ + K_max"},
    {"q": "10. P-N सन्धि डायोड की कार्यप्रणाली का विस्तृत वर्णन करते हुए अर्द्ध तरंग दिष्टकारी का परिपथ चित्र बनाकर समझाइए।", "a": "अग्र: धारा; उत्क्रम: अल्प धारा; अर्द्ध तरंग दिष्टकारी परिपथ"},
    {"q": "11. दो समान्तर धारावाही चालकों के बीच बल का सूत्र प्राप्त करें एवं एक एम्पियर की परिभाषा दें।", "a": "F = (μ₀ I₁ I₂ l) / (2πd)"},
    {"q": "12. समतल अपवर्तक पृष्ठ पर अपवर्तन का सूत्र स्थापित करें एवं वास्तविक तथा आभासी गहराई में सम्बन्ध ज्ञात करें।", "a": "μ = वास्तविक गहराई / आभासी गहराई"},
    {"q": "13. नाभिकीय विखण्डन एवं संलयन में अन्तर स्पष्ट करते हुए नाभिकीय रिएक्टर का सिद्धान्त समझाइए।", "a": "विखण्डन: श्रृंखला अभिक्रिया; संलयन: उच्च ताप"},
    {"q": "14. द्रव्यमान क्षति तथा बन्धन ऊर्जा के आधार पर नाभिक के स्थायित्व की व्याख्या कीजिए।", "a": "अधिक बन्धन ऊर्जा प्रति न्यूक्लिऑन = अधिक स्थायित्व"},
    {"q": "15. एक P-N सन्धि का अग्र एवं उत्क्रम अभिनति में व्यवहार समझाइए तथा धारा-वोल्टता अभिलक्षण खींचिए।", "a": "अग्र: धारा; उत्क्रम: अल्प धारा; V-I ग्राफ"},
]

CHE_S2 = [
    {"q": "1. राउल्ट का नियम लिखें एवं इसकी सीमाएँ बताएँ।", "a": "p = p°x; केवल आदर्श विलयनों के लिए।"},
    {"q": "2. मोलरता एवं मोललता में अन्तर लिखें।", "a": "मोलरता (M) = mol/L; मोललता (m) = mol/kg।"},
    {"q": "3. हेनरी का नियम लिखें एवं इसके अनुप्रयोग बताएँ।", "a": "p = K_H x; सोडा बोतल, डीकम्प्रेशन सिकनेस।"},
    {"q": "4. अणुसंख्य गुणधर्म किन्हें कहते हैं? उदाहरण दें।", "a": "वाष्प दाब अवनमन, क्वथनांक उन्नयन, हिमांक अवनमन, परासरण दाब।"},
    {"q": "5. वान्ट हॉफ गुणांक क्या है?", "a": "i = (प्रेक्षित सान्द्रता) / (सामान्य सान्द्रता)।"},
    {"q": "6. फैराडे के विद्युत अपघटन के नियम लिखें।", "a": "W = ZQ; समान आवेश, तुल्यांकी भार समान।"},
    {"q": "7. मानक हाइड्रोजन इलेक्ट्रोड का नामांकित चित्र बनाएँ।", "a": "Pt | H₂ (g, 1 bar) | H⁺ (1 M), विभव 0 V।"},
    {"q": "8. अभिक्रिया की कोटि एवं आण्विकता में अन्तर लिखें।", "a": "कोटि प्रायोगिक, आण्विकता सैद्धान्तिक; कोटि भिन्नात्मक हो सकती है।"},
    {"q": "9. प्रथम कोटि की अभिक्रिया का वेग स्थिरांक का सूत्र लिखें।", "a": "k = (2.303/t) log([A]₀/[A])"},
    {"q": "10. सक्रियण ऊर्जा क्या है? आर्रेनियस समीकरण दें।", "a": "अभिकारक से सक्रिय संकुल बनने में न्यूनतम ऊर्जा; k = A e^(-Ea/RT)"},
    {"q": "11. लैन्थेनाइड संकुचन क्या है?", "a": "4f इलेक्ट्रॉनों के दुर्बल परिरक्षण के कारण आकार में कमी।"},
    {"q": "12. लैन्थेनाइड एवं एक्टिनाइड में अन्तर लिखें।", "a": "लैन्थेनाइड अरेडियोएक्टिव नहीं, एक्टिनाइड रेडियोएक्टिव।"},
    {"q": "13. वर्नर का सिद्धान्त लिखें।", "a": "प्राथमिक संयोजकता (आयनिक) और द्वितीयक संयोजकता (उपसहसंयोजन)।"},
    {"q": "14. प्रभावी परमाणु क्रमांक (EAN) किसे कहते हैं?", "a": "धातु आयन का कुल इलेक्ट्रॉनों की संख्या (धातु + लिगैण्ड)।"},
    {"q": "15. VSEPR सिद्धान्त के आधार पर NH₃ की आकृति समझाएँ।", "a": "sp³ संकरण, पिरामिडी आकृति, एकाकी इलेक्ट्रॉन युग्म।"},
    {"q": "16. sp³ एवं dsp² संकरण में अन्तर लिखें।", "a": "sp³: चतुष्फलकीय; dsp²: वर्ग समतलीय।"},
    {"q": "17. प्रेरक प्रभाव किसे कहते हैं?", "a": "आबन्ध पर इलेक्ट्रॉन घनत्व का स्थायी विस्थापन।"},
    {"q": "18. अनुनाद प्रभाव समझाइए।", "a": "पाई इलेक्ट्रॉनों का विस्थानीकरण, स्थायित्व बढ़ाता है।"},
    {"q": "19. SN1 एवं SN2 अभिक्रिया में अन्तर लिखें।", "a": "SN1: प्रथम कोटि, कार्बोकैटायन मध्यवर्ती; SN2: द्वितीय कोटि, संक्रमण अवस्था।"},
    {"q": "20. मार्कोनीकोव नियम लिखें एवं उदाहरण दें।", "a": "असममित एल्कीन में H जुड़कर अधिक H वाला कार्बन बनता है।"},
    {"q": "21. एल्कोहॉल एवं फिनोल में अन्तर लिखें।", "a": "एल्कोहॉल उदासीन; फिनोल अम्लीय।"},
    {"q": "22. राइमर-टीमान अभिक्रिया का रासायनिक समीकरण लिखें।", "a": "फिनोल + CHCl₃ + KOH → सैलिसिलैल्डिहाइड"},
    {"q": "23. एल्डोल संघनन समझाइए।", "a": "α-हाइड्रोजन वाले एल्डिहाइड/कीटोन क्षार द्वारा संघनित।"},
    {"q": "24. कैनिजारो अभिक्रिया का एक उदाहरण दीजिए।", "a": "2 HCHO → CH₃OH + HCOONa"},
    {"q": "25. एस्टरीकरण अभिक्रिया लिखें।", "a": "RCOOH + R'OH ⇌ RCOOR' + H₂O (अम्ल उत्प्रेरक)"},
    {"q": "26. डाइएजोटीकरण अभिक्रिया लिखें।", "a": "ArNH₂ + NaNO₂ + HCl → ArN₂⁺Cl⁻ (0‑5°C)"},
    {"q": "27. ग्लूकोस की खुली श्रृंखला संरचना बनाएँ।", "a": "CHO-(CHOH)₄-CH₂OH"},
    {"q": "28. वसा एवं तेल में अन्तर लिखें।", "a": "वसा: संतृप्त, ठोस; तेल: असंतृप्त, द्रव।"},
    {"q": "29. साबुन एवं अपमार्जक की क्रियाविधि समझाइए।", "a": "मिसेल बनाकर सफाई।"},
    {"q": "30. विटामिन A तथा C की कमी से होने वाले रोग लिखें।", "a": "A: रतौंधी; C: स्कर्वी।"},
]

CHE_S5 = [
    {"q": "1. मोलरता, मोललता, नॉर्मलता एवं मोल-अंश को परिभाषित करते हुए इनमें पारस्परिक सम्बन्ध स्थापित करें।", "a": "परिभाषाएँ और सूत्र।"},
    {"q": "2. वैद्युत रसायन सेलों का विस्तृत वर्णन करते हुए नेर्न्स्ट समीकरण प्राप्त करें।", "a": "E = E° - (RT/nF)lnQ"},
    {"q": "3. अभिक्रिया की कोटि ज्ञात करने की विधियों का विस्तृत वर्णन करें।", "a": "समाकलन, अर्द्ध आयु, आरेखीय विधियाँ।"},
    {"q": "4. संक्रमण तत्त्वों के सामान्य गुणधर्मों का विस्तृत वर्णन करें।", "a": "परिवर्ती ऑक्सीकरण अवस्था, रंग, उत्प्रेरकीय गुण।"},
    {"q": "5. लैन्थेनाइड श्रेणी के तत्त्वों के रसायन का विस्तृत वर्णन करें।", "a": "संकुचन, ऑक्सीकरण अवस्था, चुम्बकीय गुण।"},
    {"q": "6. संयोजकता आबन्ध सिद्धान्त (VBT) के आधार पर संकुल यौगिकों में आबन्धन का विस्तृत वर्णन करें।", "a": "संकरण, समावयवता।"},
    {"q": "7. प्रेरक प्रभाव, अनुनाद प्रभाव एवं अतिसंयुग्मन प्रभाव का विस्तृत वर्णन करें।", "a": "परिभाषाएँ और अनुप्रयोग।"},
    {"q": "8. एल्कोहॉल बनाने की विधियों एवं रासायनिक गुणों का विस्तृत वर्णन करें।", "a": "हाइड्रोबोरेशन, अपचयन; लुकास परीक्षण।"},
    {"q": "9. एल्डिहाइड एवं कीटोन के रासायनिक गुणों का विस्तृत वर्णन करें।", "a": "न्यूक्लियोफिलिक योग, ऑक्सीकरण, विभेद।"},
    {"q": "10. एमीन के रासायनिक गुणों एवं पृथक्करण की विधियों का विस्तृत वर्णन करें।", "a": "क्षारीयता, हाइन्सबर्ग परीक्षण।"},
    {"q": "11. विलयनों के अणुसंख्य गुणधर्मों का विस्तृत वर्णन करते हुए परासरण दाब ज्ञात करने की विधि समझाइए।", "a": "π = CRT, विधि।"},
    {"q": "12. रासायनिक बलगतिकी – आर्रेनियस समीकरण से सक्रियण ऊर्जा ज्ञात करने की विधि एवं उत्प्रेरक की भूमिका समझाइए।", "a": "log k vs 1/T, उत्प्रेरक Ea घटाता है।"},
    {"q": "13. d-ब्लॉक के तत्त्वों के इलेक्ट्रॉनिक विन्यास, ऑक्सीकरण अवस्थाएँ तथा उत्प्रेरकीय गुणों पर प्रकाश डालिए।", "a": "Cr, Mn, Fe के उदाहरण।"},
    {"q": "14. उपसहसंयोजन यौगिकों में समावयवता के प्रकारों का वर्णन करें।", "a": "ज्यामितीय, प्रकाशिक।"},
    {"q": "15. हैलोएल्केन की नाभिकस्नेही प्रतिस्थापन अभिक्रिया (SN1/SN2) की क्रियाविधि को समझाइए।", "a": "कार्बोकैटायन, संक्रमण अवस्था, प्रतिलोम।"},
]

BIO_S2 = [
    {"q": "1. समसूत्री एवं अर्द्धसूत्री विभाजन में अन्तर लिखें।", "a": "समसूत्री: गुणसूत्र संख्या समान; अर्द्धसूत्री: आधी।"},
    {"q": "2. परागण की परिभाषा एवं प्रकार लिखें।", "a": "परागकणों का वर्तिकाग्र पर स्थानांतरण; स्वपरागण, परपरागण।"},
    {"q": "3. बीजाण्ड की संरचना का नामांकित चित्र बनाएँ।", "a": "बाह्य/अन्तः त्वचा, भ्रूणकोष, बीजाण्डद्वार।"},
    {"q": "4. निषेचन किसे कहते हैं? इसके प्रकार लिखें।", "a": "नर और मादा युग्मक का संलयन; बाह्य, आन्तरिक।"},
    {"q": "5. मानव वृषण की संरचना समझाइए।", "a": "शुक्रजनक नलिकाएँ, अन्तराली कोशिकाएँ।"},
    {"q": "6. मानव अण्डाशय की संरचना लिखें।", "a": "पुटिकाएँ, कॉर्पस ल्यूटियम।"},
    {"q": "7. आर्तव चक्र को समझाइए।", "a": "28 दिन, मासिक स्राव, अण्डोत्सर्ग।"},
    {"q": "8. गर्भ निरोधक विधियों के नाम लिखें।", "a": "कॉपर-टी, कंडोम, गर्भनिरोधक गोलियाँ।"},
    {"q": "9. मेण्डल का प्रभाविता का नियम लिखें।", "a": "F1 पीढ़ी में केवल प्रभावी लक्षण दिखता है।"},
    {"q": "10. मेण्डल का पृथक्करण का नियम लिखें।", "a": "युग्मक बनते समय युग्म विकल्पी पृथक होते हैं।"},
    {"q": "11. सहप्रभाविता किसे कहते हैं? उदाहरण दें।", "a": "दोनों एलील अभिव्यक्त, AB रुधिर वर्ग।"},
    {"q": "12. बहुएलीलता किसे कहते हैं? ABO रुधिर वर्ग को समझाइए।", "a": "एक से अधिक एलील; Iᴬ, Iᴮ, i."},
    {"q": "13. DNA एवं RNA में अन्तर लिखें।", "a": "DNA: डीऑक्सीराइबोज, थाइमिन; RNA: राइबोज, यूरैसिल।"},
    {"q": "14. DNA प्रतिकृति की विधि संक्षेप में लिखें।", "a": "अर्द्धसंरक्षी, डीएनए पॉलीमरेज, लीडिंग-लैगिंग स्ट्रैंड।"},
    {"q": "15. अनुलेखन (Transcription) किसे कहते हैं?", "a": "DNA से mRNA का निर्माण।"},
    {"q": "16. जीन अभिव्यक्ति का नियमन समझाइए।", "a": "ओपेरॉन मॉडल, प्रेरक, दमनकारी।"},
    {"q": "17. जैव विकास के प्रमाणों का संक्षिप्त वर्णन करें।", "a": "जीवाश्म, तुलनात्मक शरीर रचना, भ्रूण विज्ञान।"},
    {"q": "18. डार्विन का प्राकृतिक चयन सिद्धान्त लिखें।", "a": "उपयुक्ततम की उत्तरजीविता।"},
    {"q": "19. पारिस्थितिक पिरामिड किसे कहते हैं?", "a": "संख्या, जैवभार, ऊर्जा का पिरामिड।"},
    {"q": "20. खाद्य जाल को समझाइए।", "a": "अनेक खाद्य श्रृंखलाओं का जाल।"},
    {"q": "21. जैव-विविधता की परिभाषा एवं प्रकार लिखें।", "a": "आनुवंशिक, जातीय, पारितंत्रीय विविधता।"},
    {"q": "22. जैव-प्रौद्योगिकी की परिभाषा एवं उपयोग लिखें।", "a": "जीवों का उपयोग; इंसुलिन, टीका, फसल सुधार।"},
    {"q": "23. पुनर्योगज DNA तकनीक के चरण लिखें।", "a": "डीएनए पृथक्करण, काटना, जोड़ना, कोशिका में प्रवेश।"},
    {"q": "24. प्लास्मिड किसे कहते हैं?", "a": "जीवाणुओं में अतिरिक्त गुणसूत्रीय DNA।"},
    {"q": "25. PCR की कार्यविधि लिखें।", "a": "विकृतीकरण, प्राइमर संलयन, विस्तारण (चक्र)।"},
    {"q": "26. प्रतिरक्षा तन्त्र की परिभाषा लिखें।", "a": "रोगजनकों से रक्षा करने वाली प्रणाली।"},
    {"q": "27. एण्टीबायोटिक प्रतिरोध क्या है?", "a": "जीवाणु द्वारा एण्टीबायोटिक के प्रति सहनशीलता।"},
    {"q": "28. ऊतक संवर्धन तकनीक का सिद्धान्त लिखें।", "a": "पोषक माध्यम में पादप ऊतक से पूर्ण पादप।"},
    {"q": "29. जैव उर्वरक एवं जैव कीटनाशकों का महत्त्व लिखें।", "a": "रासायनिक के स्थान पर पर्यावरण हितैषी।"},
    {"q": "30. जैव आवर्धन (Biomagnification) किसे कहते हैं?", "a": "खाद्य श्रृंखला में विषाक्त पदार्थों की सान्द्रता बढ़ना।"},
]

BIO_S5 = [
    {"q": "1. पुष्पी पादपों में लैंगिक जनन का विस्तृत वर्णन करते हुए निषेचन क्रियाविधि समझाइए।", "a": "परागण, पराग नलिका, दोहरा निषेचन।"},
    {"q": "2. मानव नर जनन तन्त्र की संरचना एवं कार्यों का विस्तृत वर्णन करें।", "a": "वृषण, शुक्रवाहिका, शुक्राणु निर्माण।"},
    {"q": "3. मानव मादा जनन तन्त्र की संरचना एवं कार्यों का विस्तृत वर्णन करें।", "a": "अण्डाशय, डिम्बवाहिनी, गर्भाशय।"},
    {"q": "4. गर्भावस्था एवं प्रसव की प्रक्रिया का विस्तृत वर्णन करें।", "a": "भ्रूण विकास, अपरा, प्रसव के चरण।"},
    {"q": "5. मेण्डल के प्रयोगों का विस्तृत वर्णन करते हुए स्वतन्त्र अपव्यूहन नियम की व्याख्या करें।", "a": "द्विसंकर क्रॉस, 9:3:3:1।"},
    {"q": "6. वंशागति के गुणसूत्रीय सिद्धान्त का विस्तृत वर्णन करें।", "a": "मॉर्गन का प्रयोग, सहलग्नता, जीन विनिमय।"},
    {"q": "7. DNA की संरचना एवं प्रतिकृति की क्रियाविधि का विस्तृत वर्णन करें।", "a": "द्विकुण्डली, पॉलीमरेज, अग्रगामी/पश्चगामी स्ट्रैंड।"},
    {"q": "8. प्रोटीन संश्लेषण (अनुलेखन एवं अनुवादन) की प्रक्रिया का विस्तृत वर्णन करें।", "a": "प्रतिलिपि, mRNA, tRNA, राइबोसोम।"},
    {"q": "9. पारिस्थितिक तन्त्र में ऊर्जा प्रवाह का विस्तृत वर्णन करें।", "a": "एकदिशीय, 10% नियम, खाद्य श्रृंखला।"},
    {"q": "10. जैव-प्रौद्योगिकी के सिद्धान्त एवं उपयोग का विस्तृत वर्णन करें।", "a": "पुनर्योगज DNA, इंसुलिन, ट्रांसजेनिक फसलें।"},
    {"q": "11. दोहरे निषेचन की क्रियाविधि का वर्णन करें तथा भ्रूणकोष का नामांकित चित्र बनाइए।", "a": "नर युग्मक + अण्ड = भ्रूण; नर युग्मक + द्वितीयक केन्द्रक = एण्डोस्पर्म।"},
    {"q": "12. सहलग्नता एवं जीन विनिमय की क्रियाविधि को समझाइए।", "a": "एक ही गुणसूत्र पर जीन, क्रॉसिंग ओवर।"},
    {"q": "13. जीन अभिव्यक्ति का नियमन – लैक्टोज ओपेरॉन मॉडल का विस्तृत वर्णन करें।", "a": "प्रेरक, दमनकारी, प्रतिलिपि।"},
    {"q": "14. मलेरिया रोग के लक्षण, रोगकारक एवं नियन्त्रण का वर्णन करें।", "a": "प्लास्मोडियम, मच्छर, कुनैन।"},
    {"q": "15. कैंसर के प्रकार, कारण एवं उपचार की विधियाँ समझाइए।", "a": "अर्बुद, कार्सिनोजन, कीमोथेरेपी, रेडियोथेरेपी।"},
]

HIN_S2 = [
    {"q": "1. सूरदास के पदों का प्रतिपाद्य लिखिए।", "a": "सूरदास के पदों में कृष्ण की बाल लीलाएँ और वात्सल्य भाव है।\nभाषा: ब्रजभाषा\nविशेषताएँ:\n(1) वात्सल्य और शृंगार रस\n(2) मधुर संगीतात्मकता\n(3) प्रकृति चित्रण\n(4) विरह का मार्मिक वर्णन"},
    {"q": "2. रस की परिभाषा एवं 9 भेद।", "a": "रस: काव्य से मिलने वाला आनन्द।\n9 रस:\n1.शृंगार(रति) 2.हास्य(हास) 3.करुण(शोक)\n4.रौद्र(क्रोध) 5.वीर(उत्साह) 6.भयानक(भय)\n7.बीभत्स(जुगुप्सा) 8.अद्भुत(विस्मय) 9.शांत(निर्वेद)"},
    {"q": "3. अलंकार की परिभाषा उदाहरण सहित।", "a": "काव्य की शोभा बढ़ाने वाले तत्त्व अलंकार हैं।\nशब्दालंकार: अनुप्रास, यमक, श्लेष\nअर्थालंकार: उपमा, रूपक, उत्प्रेक्षा\nउदा:\nअनुप्रास: 'चारु चंद्र की चंचल किरणें'\nउपमा: 'सागर सा गंभीर'"},
    {"q": "4. रेणु की भाषा-शैली की विशेषताएँ।", "a": "(1) आंचलिक भाषा का प्रयोग\n(2) भोजपुरी, मैथिली शब्द\n(3) लोकगीतों का समावेश\n(4) जीवंत संवाद\n(5) ग्रामीण जीवन का सजीव चित्रण"},
    {"q": "5. प्रेमचन्द की साहित्यिक विशेषताएँ।", "a": "(1) यथार्थवादी लेखन\n(2) किसान, दलित, नारी समस्या\n(3) सरल भाषा\n(4) आदर्शोन्मुखी कथाएँ\n(5) 'गोदान', 'कफन' जैसी कालजयी रचनाएँ"},
    {"q": "6. निबन्ध और कहानी में अन्तर।", "a": "निबन्ध: विचारात्मक गद्य\nलेखक के विचार प्रधान\nकहानी: कथातत्त्व प्रधान\nपात्र, संवाद, कथावस्तु प्रधान"},
    {"q": "7. मुहावरे और लोकोक्ति में अन्तर।", "a": "मुहावरा: वाक्यांश, विशेष अर्थ\n'आँखें चुराना' = सामने न आना\nलोकोक्ति: पूर्ण कथन, अनुभव आधारित\n'अब पछताए होत क्या...'\nमुहावरा वाक्य का अंग; लोकोक्ति स्वतंत्र।"},
    {"q": "8. उपसर्ग और प्रत्यय में अन्तर।", "a": "उपसर्ग: शब्द के आगे\nप्र+गति=प्रगति, अ+सत्य=असत्य\nप्रत्यय: शब्द के पीछे\nमनुष्य+ता=मनुष्यता\nदोनों शब्द का अर्थ बदलते हैं।"},
    {"q": "9. तत्सम, तद्भव और देशज में अन्तर।", "a": "तत्सम: संस्कृत से सीधे — अग्नि, क्षेत्र\nतद्भव: बदलकर — आग, खेत\nदेशज: स्थानीय — खिड़की, लोटा\nविदेशज: अन्य भाषा — कमीज, कैंची"},
    {"q": "10. कारक की परिभाषा और 8 कारक।", "a": "संज्ञा/सर्वनाम का क्रिया से सम्बन्ध।\n8 कारक:\nकर्ता(ने), कर्म(को), करण(से)\nसम्प्रदान(के लिए), अपादान(से अलग)\nसम्बन्ध(का/के/की), अधिकरण(में/पर)\nसम्बोधन(हे!)"},
    {"q": "11. छायावाद की 5 प्रमुख विशेषताएँ।", "a": "(1) व्यक्तिवाद\n(2) प्रकृति का मानवीकरण\n(3) प्रेम और सौंदर्य\n(4) रहस्यवाद\n(5) नई शैली\nकवि: प्रसाद, निराला, पंत, महादेवी"},
    {"q": "12. पत्र लेखन के दो प्रकार।", "a": "(1) औपचारिक: सरकारी, व्यापारिक\nभाषा: शिष्ट, मानक\n(2) अनौपचारिक: मित्र, परिवार\nभाषा: सरल, भावनात्मक\nBSEB: प्रधानाचार्य को = औपचारिक"},
    {"q": "13. संक्षेपण की परिभाषा एवं नियम।", "a": "(1) मूल का 1/3 भाग\n(2) मुख्य बातें\n(3) अपने शब्दों में\n(4) तृतीय पुरुष\n(5) एक अनुच्छेद\n(6) उचित शीर्षक"},
    {"q": "14. रामचरितमानस की भाषाई विशेषताएँ।", "a": "भाषा: अवधी\nशैली: दोहा-चौपाई\n(1) तत्सम शब्द\n(2) मधुर और लयात्मक\n(3) अलंकारों का प्रयोग\n(4) भक्ति और दर्शन का समन्वय"},
    {"q": "15. आत्मकथा और जीवनी में अन्तर।", "a": "आत्मकथा: स्वयं अपनी कथा, प्रथम पुरुष\nजीवनी: किसी अन्य की, तृतीय पुरुष\nदोनों जीवन आधारित रचनाएँ।"},
    {"q": "16. वाक्य शुद्धि के नियम।", "a": "(1) कर्ता-क्रिया में वचन-लिंग साम्य\n(2) उचित कारक चिह्न\n(3) सही शब्द प्रयोग\nअशुद्ध: मैंने खाना खाई\nशुद्ध: मैंने खाना खाया"},
    {"q": "17. सूचना लेखन का प्रारूप।", "a": "──────────\nसूचना\n[संस्था]\n[दिनांक]\n[शीर्षक]\n[विषय: क्या, कब, कहाँ, क्यों]\n[नाम, पद]\n──────────"},
    {"q": "18. निराला की कविता की विशेषताएँ।", "a": "(1) मुक्त छंद के प्रवर्तक\n(2) क्रांतिकारी विचार\n(3) राष्ट्रीय चेतना\n(4) शोषित वर्ग की आवाज\n(5) 'राम की शक्तिपूजा' प्रमुख रचना"},
    {"q": "19. हिंदी साहित्य के काल विभाजन।", "a": "आदिकाल (700-1400): चंदबरदाई\nभक्तिकाल (1400-1700): कबीर, तुलसी\nरीतिकाल (1700-1900): बिहारी\nआधुनिककाल (1900-): प्रेमचंद, निराला"},
    {"q": "20. 'बाजार दर्शन' का सारांश।", "a": "लेखक: जैनेन्द्र कुमार\nमुख्य विचार: बाजार की शक्ति मन की कमजोरी है।\nगांधी: सच्चा सुख त्याग में।\nसंदेश: जरूरत के अनुसार खरीदें, दिखावे के लिए नहीं।"},
    {"q": "21. 'गोदान' उपन्यास की मुख्य थीम।", "a": "किसान जीवन की त्रासदी।\nपात्र: होरी, धनिया\n(1) कर्ज का बोझ\n(2) जमींदारी शोषण\n(3) ग्रामीण-शहरी अंतर\n(4) नारी की दुर्दशा"},
    {"q": "22. महादेवी वर्मा की काव्य विशेषताएँ।", "a": "(1) वेदना और करुणा\n(2) रहस्यवादी भावना\n(3) प्रकृति से तादात्म्य\n(4) नारी पीड़ा\n(5) संगीतात्मक भाषा\nरचनाएँ: नीहार, रश्मि, नीरजा, यामा"},
    {"q": "23. औपचारिक पत्र का प्रारूप।", "a": "सेवा में,\nप्रधानाचार्य महोदय,\n[विद्यालय, पता]\nविषय: [कारण]\nमहोदय,\n[मुख्य बात]\nधन्यवाद।\nआपका शिष्य,\n[नाम, कक्षा, दिनांक]"},
    {"q": "24. संधि और समास में अन्तर।", "a": "संधि: दो वर्णों का मेल\nराम+ईश्वर = रामेश्वर\nसमास: दो शब्दों का संक्षिप्त रूप\nराजपुत्र = राजा का पुत्र\nसंधि में ध्वनि परिवर्तन; समास में अर्थ संक्षेप।"},
    {"q": "25. हिंदी में प्रयोगवाद की विशेषताएँ।", "a": "(1) नए भाषाई प्रयोग\n(2) अज्ञेय का 'तारसप्तक' (1943)\n(3) व्यक्तिवाद\n(4) आत्मसंघर्ष\n(5) यथार्थवाद"},
    {"q": "26. 'कफन' कहानी का सारांश।", "a": "लेखक: प्रेमचंद\nपात्र: घीसू, माधव, बुधिया\nकथावस्तु: मरती पत्नी का कफन न खरीदकर शराब पीना।\nशैली: व्यंग्यात्मक यथार्थवाद"},
    {"q": "27. यात्रा-वृत्तान्त की विशेषताएँ।", "a": "(1) स्थान का सजीव वर्णन\n(2) व्यक्तिगत अनुभव\n(3) सांस्कृतिक जानकारी\n(4) रोचक शैली\n(5) उत्सुकता जगाना"},
    {"q": "28. रिपोर्ताज किसे कहते हैं?", "a": "किसी घटना का आँखों देखा वर्णन।\nविशेषताएँ:\n(1) तात्कालिकता\n(2) आँखों देखा विवरण\n(3) भावात्मक और तथ्यात्मक\n(4) पत्रकारिता और साहित्य का मिश्रण"},
    {"q": "29. जनसंचार माध्यमों के प्रकार।", "a": "1. मुद्रण: समाचार पत्र, पत्रिका\n2. इलेक्ट्रॉनिक: रेडियो, TV\n3. डिजिटल: इंटरनेट, सोशल मीडिया\nसभी जन-जागृति में सहायक।"},
    {"q": "30. प्रयोजनमूलक हिंदी के प्रकार।", "a": "(1) राजभाषा — सरकारी\n(2) व्यावसायिक — व्यापार\n(3) मीडिया — समाचार\n(4) तकनीकी — विज्ञान"},
]

HIN_S5 = [
    {"q": "1. सूरदास की भक्ति-भावना और काव्य विशेषताएँ।", "a": "सूरदास (1478-1583)\nभाषा: ब्रजभाषा, रचना: सूरसागर\nविशेषताएँ:\n(1) वात्सल्य रस: कृष्ण की बाल-लीलाएँ\n(2) शृंगार: राधा-कृष्ण प्रेम\n(3) सगुण कृष्ण भक्ति\n(4) मधुर संगीत\nभक्ति: सख्य और वात्सल्य भाव\nभाषा: ब्रजभाषा का सौंदर्य, लोक-तत्त्व"},
    {"q": "2. प्रसाद जी के काव्य की विशेषताएँ।", "a": "जयशंकर प्रसाद (1889-1937)\nरचनाएँ: कामायनी, आँसू, लहर\nविशेषताएँ:\n(1) छायावाद के प्रवर्तक\n(2) रहस्यवाद और दर्शन\n(3) प्रकृति का मानवीकरण\n(4) राष्ट्रीय चेतना\nकामायनी: 14 सर्ग, मनु-श्रद्धा\nभाषा: संस्कृतनिष्ठ, अलंकृत"},
    {"q": "3. महादेवी वर्मा की काव्यगत विशेषताएँ।", "a": "रचनाएँ: नीहार, रश्मि, नीरजा, यामा\nविशेषताएँ:\n(1) वेदना और करुणा\n(2) रहस्यवादी भावना\n(3) प्रकृति से तादात्म्य\n(4) नारी-पीड़ा\n(5) संगीतात्मक भाषा\nपुरस्कार: ज्ञानपीठ (यामा)\n'आधुनिक मीरा' की उपाधि"},
    {"q": "4. हिन्दी उपन्यास के विकास का इतिहास।", "a": "परीक्षागुरु (1882) — पहला उपन्यास\nप्रेमचंद युग (1900-1936):\nगोदान, सेवासदन — यथार्थवाद\nप्रेमचंदोत्तर: जैनेंद्र, अज्ञेय\nमनोवैज्ञानिक उपन्यास\nआधुनिक: रेणु — आंचलिक\nमहत्त्व: सामाजिक चेतना का दर्पण"},
    {"q": "5. 'स्वच्छ भारत अभियान' पर निबन्ध।", "a": "प्रस्तावना: 2 अक्टूबर 2014 को शुरू\nउद्देश्य:\n(1) खुले में शौच मुक्ति\n(2) ठोस अपशिष्ट प्रबंधन\n(3) हर घर शौचालय\nउपलब्धियाँ:\n(1) 10 करोड़+ शौचालय\n(2) 600+ जिले ODF\nउपसंहार: स्वच्छता जीवनशैली बने।"},
    {"q": "6. 'जनसंख्या वृद्धि: समस्या और समाधान' पर निबन्ध।", "a": "प्रस्तावना: भारत — 140 करोड़, विश्व में प्रथम\nकारण:\n(1) अशिक्षा\n(2) बाल विवाह\n(3) गरीबी\nप्रभाव:\n(1) बेरोजगारी\n(2) संसाधन दबाव\nसमाधान:\n(1) शिक्षा\n(2) परिवार नियोजन\n(3) महिला सशक्तीकरण"},
    {"q": "7. शिकायती पत्र — नगर निगम को।", "a": "सेवा में,\nनगर निगम अध्यक्ष,\n[पता]\nविषय: सफाई व्यवस्था हेतु शिकायत।\nमहोदय,\nवार्ड में सफाई नहीं, कूड़े का ढेर, बीमारी का खतरा।\nनिवेदन:\n(1) नियमित सफाई\n(2) कूड़ेदान\nआपका,\n[नाम, पता, दिनांक]"},
    {"q": "8. सूरदास और तुलसीदास की तुलना।", "a": "सूरदास: कृष्ण भक्त, वात्सल्य-शृंगार, ब्रजभाषा, सूरसागर\nतुलसीदास: राम भक्त, दास्य-समन्वयवाद, अवधी, रामचरितमानस\nसमानता: दोनों सगुण भक्त, भक्तिकाल, समाज सुधार\nअंतर: सूर=कृष्ण/वात्सल्य; तुलसी=राम/मर्यादा"},
    {"q": "9. छायावाद की प्रमुख विशेषताएँ।", "a": "समय: 1918-1936\nविशेषताएँ:\n(1) व्यक्तिवाद\n(2) प्रकृति मानवीकरण\n(3) प्रेम और सौंदर्य\n(4) रहस्यवाद\n(5) राष्ट्रीयता\nकवि:\nप्रसाद: कामायनी\nनिराला: मुक्त छंद\nपंत: प्रकृति सौंदर्य\nमहादेवी: वेदना"},
    {"q": "10. हिन्दी व्याकरण — रस का विस्तृत वर्णन।", "a": "'विभावानुभावव्यभिचारिसंयोगाद्रसनिष्पत्ति'\n9 रस:\nशृंगार(रति), हास्य(हास), करुण(शोक)\nरौद्र(क्रोध), वीर(उत्साह), भयानक(भय)\nबीभत्स(जुगुप्सा), अद्भुत(विस्मय), शांत(निर्वेद)\n4 अंग: स्थायी भाव, विभाव, अनुभाव, संचारी भाव\nउदा: शृंगार: 'बतरस लालच लाल की...'"},
]

ENG_S2 = [
    {"q": "1. Why did William Douglas develop fear of water? (Deep Water)", "a": "As a child, a big boy threw Douglas into YMCA pool. He nearly drowned — sinking to bottom repeatedly. This traumatic experience created lifelong fear of water. He overcame it through professional swimming lessons and determination."},
    {"q": "2. Condition of bangle makers in Firozabad? (Lost Spring)", "a": "Bangle makers worked in dark, dingy rooms near furnaces. Children worked instead of going to school. Risk of blindness due to glass dust. Trapped in debt and poverty — a vicious cycle of exploitation."},
    {"q": "3. Why did peddler sign as Captain von Stahle? (The Rattrap)", "a": "Edla treated him with kindness, believing he was a Captain. Her goodness transformed him — he felt ashamed of theft. He returned stolen money, signing as 'Captain von Stahle' to honor her trust. Shows inner transformation through compassion."},
    {"q": "4. What did Gandhi do for Champaran sharecroppers? (Indigo)", "a": "Gandhi organized civil disobedience. He investigated grievances, collected evidence, negotiated with British. Won 25% refund for farmers. Established schools in villages. India's first successful civil disobedience movement."},
    {"q": "5. Poet's mother's appearance in 'My Mother at Sixty-Six'.", "a": "Mother's face: ashen like corpse, pale as late winter's moon. Mouth open, eyes closed. The familiar childhood fear of losing mother returned to the poet. Reflects aging and fear of separation."},
    {"q": "6. What does poet ask in 'Keeping Quiet'?", "a": "Pablo Neruda asks everyone to stop all activity for one moment. Not speak any language. Not move arms so much. Purpose: create stillness and mutual understanding. Message: silence prevents war and harm."},
    {"q": "7. Why is a thing of beauty joy forever? (A Thing of Beauty)", "a": "According to Keats, beauty never fades from memory. It removes sadness and gives hope. Examples: sun, moon, trees, flowers, rivers. Beauty uplifts the human spirit — hence 'a joy forever'."},
    {"q": "8. What are Aunt Jennifer's tigers doing?", "a": "Tigers are prancing across embroidered screen. Bright topaz, fearless, not afraid of men. Moving with ease under trees. Symbolism: represent freedom Aunt Jennifer desires but cannot have due to oppressive marriage."},
    {"q": "9. Format of report writing.", "a": "1. Headline — catchy\n2. Byline — By [Reporter]\n3. Place, Date\n4. Opening — 5W1H\n5. Body — details\n6. Conclusion\nLanguage: Third person, Past tense, Factual"},
    {"q": "10. Theme of 'The Third Level'.", "a": "Theme: Escape from stress. Third level represents wish to return to simpler past (1894). Charley uses imagination as escape. Story explores thin line between reality and fantasy."},
    {"q": "11. Change voice: 'The boy is flying a kite.'", "a": "Active: The boy is flying a kite.\nPassive: A kite is being flown by the boy.\nFormula: Object + is/am/are + being + V3 + by + Subject"},
    {"q": "12. Write letter to editor about stray dogs.", "a": "To,\nThe Editor,\n[Newspaper]\nSir,\nI wish to draw attention to menace of stray dogs. Several people bitten recently.\nI urge municipal authorities for immediate action.\nYours faithfully,\n[Name]"},
    {"q": "13. Explain: 'Actions speak louder than words.'", "a": "Meaning: What we do is more important than what we say.\nAnyone can make promises. True character shown by actions. A helpful deed is better than kind words."},
    {"q": "14. Types of sentences with examples.", "a": "Simple: She sings.\nCompound: She sings and dances.\nComplex: She sings because she is happy.\nDeclarative, Interrogative, Imperative, Exclamatory."},
    {"q": "15. Conditional sentences with types.", "a": "Type 0: If you heat ice, it melts.\nType 1: If it rains, I will stay.\nType 2: If I were rich, I would help.\nType 3: If I had studied, I would have passed."},
    {"q": "16. What is Precis Writing?", "a": "Summary in 1/3 length. Read twice, identify main ideas, write in own words, third person, give title. No direct speech."},
    {"q": "17. Use of Modals.", "a": "Can: ability, Could: past ability\nMay: permission, Might: possibility\nMust: obligation, Should: advice\nWould: conditional, Shall: formal future"},
    {"q": "18. Character of rattrap peddler.", "a": "Poor, homeless, philosophical (sees world as rattrap). Initially dishonest — steals from crofter. Transformed by Edla's kindness. Returns money, signs as Captain. Theme: goodness transforms people."},
    {"q": "19. Draft notice for blood donation camp.", "a": "NOTICE\nXYZ School | [Date]\nBLOOD DONATION CAMP\nAll students above 18 invited. Date: [date], School Hall, 10AM-2PM.\n[Name]\nHead Boy/Girl"},
    {"q": "20. Message of 'The Last Lesson'.", "a": "Never take language and culture for granted. M. Hamel shows value of mother tongue. Patriotism and cultural pride. 'Language is the key to prison of enslaved people.'"},
    {"q": "21. 'The Road Not Taken' by Robert Frost.", "a": "Theme: Individual choices in life. Speaker chooses less-traveled road. Symbolism: roads = life choices. Message: our choices define future. Have courage to be different."},
    {"q": "22. Gerunds and Infinitives.", "a": "Gerund (V+ing): Swimming is healthy. I enjoy reading.\nInfinitive (to+V1): I go to study. Happy to help.\nVerbs+gerund: enjoy, avoid. Verbs+infinitive: want, decide."},
    {"q": "23. Degrees of Comparison.", "a": "Positive: tall. Comparative: taller. Superlative: tallest.\nIrregular: good-better-best, bad-worse-worst.\n1 syllable: -er/-est. 2+ syllables: more/most."},
    {"q": "24. Write formal email format.", "a": "To: [email]\nSubject: [specific]\nDear Sir/Madam,\nI am writing to [purpose].\n[Content]\nYours sincerely,\n[Name, Designation]"},
    {"q": "25. Stream of consciousness.", "a": "Literary technique depicting continuous flow of thoughts. Features: inner monologue, non-linear, psychological realism. Authors: Virginia Woolf (Mrs. Dalloway), James Joyce (Ulysses)."},
    {"q": "26. Subject-Verb Agreement.", "a": "Singular subject → singular verb: The dog barks.\nPlural → plural: The dogs bark.\nCollective: usually singular. Either/Neither: singular.\nNews/Furniture: singular."},
    {"q": "27. Direct and Indirect Speech.", "a": "Direct: He said, 'I am happy.'\nIndirect: He said that he was happy.\nRules: Remove quotes, add 'that', change pronouns and tenses."},
    {"q": "28. Character of Dr. Sadao in 'The Enemy'.", "a": "Dedicated doctor, patriotic but humane. Saves American soldier despite risk. Conflict: duty vs medical oath. Message: humanity transcends nationalism."},
    {"q": "29. Speech on 'Clean India, Green India'.", "a": "Respected audience,\nSwachh Bharat Abhiyan launched 2014. Actions: avoid plastic, plant trees, proper waste disposal. Gandhi: 'Cleanliness is next to Godliness.' Let us make India clean and green!\nThank you!"},
    {"q": "30. Active and Passive Voice rules.", "a": "Active: Subject does action — She writes.\nPassive: Object becomes subject — A letter is written.\nFormulas:\nSimple Present: is/am/are + V3\nSimple Past: was/were + V3\nFuture: will + be + V3"},
]

ENG_S5 = [
    {"q": "1. Describe Douglas's experience in 'Deep Water' and how he overcame fear.", "a": "Young Douglas thrown into YMCA pool by big boy. Nearly drowned — sinking repeatedly. Traumatized for years.\nOvercoming: Hired professional instructor. Practiced gradually — legs, arms, breathing. Tested in rivers. Conquered fear through determination.\nMessage: Fear can be overcome through courage. 'In death there is life.'"},
    {"q": "2. Analyse 'Lost Spring' — poverty and exploitation.", "a": "Saheb: ragpicker from Bangladesh — lost spring (fields). Works at tea stall — loses freedom. Dream: play tennis.\nMukesh: bangle maker — hazardous conditions, blindness risk. Dream: mechanic.\nExploitation: child labor, debt trap, sahukars, police.\nTheme: Spring = hope lost to poverty. Must break chain of exploitation."},
    {"q": "3. Character sketch of rattrap peddler.", "a": "Shabby, poor, philosophical — sees world as rattrap.\nMoral weakness: steals 30 kronors. Gets lost = trapped like rat!\nTransformation: Edla's kindness and dignity changes him. Returns money, signs as 'Captain von Stahle'.\nTheme: Compassion can transform even morally fallen person."},
    {"q": "4. Theme of 'Keeping Quiet' and relevance today.", "a": "Theme: Peace through stillness.\nPoet asks: stop all activity, no language, no movement, no engines.\nResult: understanding, end to wars, harmony with nature.\nRelevance: Wars, terrorism, environmental destruction. Social media noise — we need silence and reflection.\nConclusion: Pause, reflect, find peace within."},
    {"q": "5. Essay: 'Importance of Education in Modern India'.", "a": "Nelson Mandela: 'Education is most powerful weapon.'\nNEP 2020 — revolutionary reforms. 77% literacy.\nImportance: Development, social change, critical thinking, women empowerment.\nChallenges: Rural-urban divide, drop-out rates.\nSolutions: Digital classrooms, skill-based education.\nConclusion: Quality education for every child must be India's mission."},
    {"q": "6. Report on 'Science Exhibition in Your School'.", "a": "ANNUAL SCIENCE EXHIBITION\nXYZ School | [Date]\nOver 200 students with 85 projects. First prize: solar water purifier (Class 12). Earthquake predictor amazed visitors. AI applications demonstrated.\nChief Guest praised creativity. Principal congratulated participants.\nConclusion: Indian students ready to lead world in science."},
    {"q": "7. Discuss 'Aunt Jennifer's Tigers' — plight of women.", "a": "Surface: Aunt Jennifer embroiders tigers while in difficult marriage.\nTigers: bright, fearless, free — represent her desired freedom.\nAunt Jennifer: fingers fluttering, 'weight of wedding band' — oppressed.\nIrony: Tigers free; Aunt Jennifer trapped. Even after death, 'ringed with ordeals'.\nTheme: Patriarchal oppression. Women must express themselves freely."},
    {"q": "8. Letter to Municipal Commissioner about poor drainage.", "a": "To,\nMunicipal Commissioner,\n[Address]\nSubject: Poor Drainage in [Area]\nRespected Sir,\nWater logging occurs every rainfall. Mosquitoes, impassable roads, unhygienic conditions.\nRequests: Desilting, proper drainage construction, regular maintenance.\nYours faithfully,\n[Name, Address]"},
    {"q": "9. Explain poetic devices in 'My Mother at Sixty-Six'.", "a": "Simile: 'face ashen like corpse', 'pale as winter moon'\nImagery: 'young trees sprinting', 'merry children spilling'\nTransferred Epithet: 'familiar ache'\nRepetition: 'smile and smile and smile' — masked grief\nSymbolism: winter moon = decline; young trees = hope\nTheme: Fear of losing aging mother. Love and separation."},
    {"q": "10. Article: 'Role of Youth in Nation Building'.", "a": "India: 65% below 35 — our greatest asset.\nContributions:\n1. Education: develop skills and values\n2. Innovation: startups, research\n3. Social responsibility: vote, volunteer\n4. Character: integrity, hard work\n5. Environment: fight climate change\nMandela: 'Education is most powerful weapon.'\nConclusion: Pledge to be responsible citizens!"},
]

MAT_S2 = [
    {"q": "1. एकैकी एवं आच्छादक फलनों में अन्तर।", "a": "एकैकी: f(x₁)=f(x₂) → x₁=x₂\nआच्छादक: codomain का हर element image है\nBijective = दोनों\nउदा: f(x)=2x+1 bijective है R→R पर"},
    {"q": "2. आव्यूह A=[[2,3],[1,2]] का व्युत्क्रम।", "a": "|A|=2×2-3×1=1\nadj(A)=[[2,-3],[-1,2]]\nA⁻¹=[[2,-3],[-1,2]]\nजाँच: A·A⁻¹=I ✓"},
    {"q": "3. गुणनफल नियम सिद्ध कीजिए।", "a": "d/dx[fg]=f'g+fg'\nसिद्धान्त: lim से\n= f(x)g'(x)+g(x)f'(x)\nउदा: d/dx[x²sinx]=2x sinx+x²cosx"},
    {"q": "4. f(x)=x³-3x के चरम बिन्दु।", "a": "f'(x)=3x²-3=3(x-1)(x+1)\nx=1,-1\nf''(1)=6>0 → निम्नतम, f(1)=-2\nf''(-1)=-6<0 → उच्चतम, f(-1)=2"},
    {"q": "5. ∫x sinx dx का मान।", "a": "u=x, v=sinx\n∫x sinx dx = x(-cosx)-∫(-cosx)dx\n=-x cosx + sinx + C"},
    {"q": "6. रोले एवं मध्यमान प्रमेय।", "a": "रोले: f(a)=f(b) → ∃c: f'(c)=0\nMVT: ∃c: f'(c)=[f(b)-f(a)]/(b-a)\nज्यामितीय: जीवा का ढाल = स्पर्श रेखा का ढाल"},
    {"q": "7. सारणिक के गुणधर्म।", "a": "(1)|Aᵀ|=|A| (2)समान पंक्ति→0\n(3)k गुणा→k|A| (4)पंक्ति बदलने पर चिह्न\n(5)|AB|=|A||B| (6)पंक्ति जोड़→|A| same"},
    {"q": "8. प्रायिकता का योग प्रमेय।", "a": "P(A∪B)=P(A)+P(B)-P(A∩B)\nपरस्पर अपवर्जी: P(A∩B)=0\nउदा: 0.3+0.4-0.1=0.6"},
    {"q": "9. ∫₁² x dx =", "a": "[x²/2]₁² = 4/2-1/2 = 3/2 = 1.5"},
    {"q": "10. बेज प्रमेय।", "a": "P(Aᵢ|B)=P(Aᵢ)·P(B|Aᵢ)/Σ P(Aⱼ)·P(B|Aⱼ)\nउदा: Box I: 3R,4W; Box II: 4R,3W\nP(I|R)=(1/2×3/7)/(1/2×3/7+1/2×4/7)=3/7"},
    {"q": "11. LPP के घटक और विधि।", "a": "घटक: चर, उद्देश्य फलन Z=ax+by, अवरोध, x,y≥0\nविधि: सुसंगत क्षेत्र → कोने के बिंदु → Z का मान → इष्टतम"},
    {"q": "12. ∫eˣ sinx dx =", "a": "I = eˣsinx - ∫eˣcosx dx\n= eˣsinx - eˣcosx - I\n2I = eˣ(sinx-cosx)\nI = eˣ(sinx-cosx)/2 + C"},
    {"q": "13. अवकल समीकरण का क्रम और घात।", "a": "क्रम: उच्चतम अवकलज का क्रम\nघात: उच्चतम अवकलज की घात\ndy/dx=y → क्रम=1, घात=1, हल: y=Ceˣ"},
    {"q": "14. स्थिति सदिश और एकांक सदिश।", "a": "स्थिति सदिश: →OP=xî+yĵ+zk̂, |OP|=√(x²+y²+z²)\nएकांक सदिश: â=→a/|→a|, परिमाण=1\nî,ĵ,k̂ एकांक सदिश"},
    {"q": "15. क्रमचय और संचय में अंतर।", "a": "क्रमचय nPr: क्रम मायने, n!/(n-r)!\nसंचय nCr: क्रम नहीं, n!/[r!(n-r)!]\nnPr = r! × nCr\nउदा: 5P3=60, 5C3=10"},
    {"q": "16. द्वितीय अवकलज परीक्षण।", "a": "f'(x)=0 → क्रांतिक बिंदु c\nf''(c)>0 → निम्नतम\nf''(c)<0 → उच्चतम\nf''(c)=0 → अनिर्णायक"},
    {"q": "17. निश्चित समाकलन के गुणधर्म।", "a": "(1)∫ₐᵇ=-∫ᵦᵃ (2)∫ₐᵃ=0\n(3)∫ₐᵇ=∫ₐᶜ+∫ᶜᵇ\n(4)∫ₐᵇf(x)=∫ₐᵇf(a+b-x)\n(5)सम फलन: ∫₋ₐᵃ=2∫₀ᵃ"},
    {"q": "18. समतल का समीकरण।", "a": "सामान्य: ax+by+cz+d=0\nसदिश: →r·→n=d\nअन्तःखण्ड: x/a+y/b+z/c=1\nदूरी: |ax₁+by₁+cz₁+d|/√(a²+b²+c²)"},
    {"q": "19. द्विपद बंटन।", "a": "P(X=r)=nCr·pʳ·(1-p)^(n-r)\nमाध्य=np\nप्रसरण=npq\nउदा: n=10,p=0.5 → μ=5, σ²=2.5"},
    {"q": "20. वर्धमान और ह्रासमान फलन।", "a": "वर्धमान: f'(x)>0\nह्रासमान: f'(x)<0\nf(x)=x²: x>0 पर वर्धमान, x<0 पर ह्रासमान"},
    {"q": "21. प्रथम कोटि रैखिक अवकल समीकरण।", "a": "dy/dx+Py=Q\nIF=e^∫P dx\nd/dx[y·IF]=Q·IF\ny·IF=∫Q·IF dx+C\nउदा: dy/dx+y=eˣ → IF=eˣ → y=eˣ/2+Ce⁻ˣ"},
    {"q": "22. सप्रतिबंध प्रायिकता।", "a": "P(A|B)=P(A∩B)/P(B)\nगुणन: P(A∩B)=P(B)·P(A|B)\nस्वतंत्र: P(A|B)=P(A)\nP(A∩B)=P(A)·P(B)"},
    {"q": "23. x^x का अवकलन।", "a": "y=x^x → log y=x log x\n(1/y)dy/dx=1+log x\ndy/dx=x^x(1+log x)"},
    {"q": "24. दो रेखाओं में न्यूनतम दूरी।", "a": "समान्तर: d=|(→a₂-→a₁)×→b|/|→b|\nविकर्ण: d=|(→a₂-→a₁)·(→b₁×→b₂)|/|→b₁×→b₂|"},
    {"q": "25. क्रेमर नियम।", "a": "D=|A|, D₁,D₂ = आव्यूह\nx=D₁/D, y=D₂/D (D≠0)\nD=0,D₁=D₂=0 → अनंत हल\nD=0, कोई Dᵢ≠0 → हल नहीं"},
    {"q": "26. समाकलन से क्षेत्रफल: y=x², 0 से 3।", "a": "A=∫₀³x² dx=[x³/3]₀³=27/3=9 वर्ग इकाई\nसूत्र: A=|∫ₐᵇf(x)dx|"},
    {"q": "27. तुल्यता संबंध।", "a": "तुल्यता: स्वतुल्य+सममित+संक्रामक\nउदा: 'समान आयु' — तीनों शर्तें ✓"},
    {"q": "28. मानक विचलन।", "a": "σ=√[Σ(xᵢ-x̄)²/n]\nप्रसरण=σ²\nउदा: 2,4,6 → x̄=4, σ²=8/3"},
    {"q": "29. sin⁻¹x+cos⁻¹x=π/2 सिद्ध।", "a": "sin⁻¹x=θ → x=sinθ\ncos⁻¹x=π/2-θ (क्योंकि sin(π/2-θ)=x)\n∴ sin⁻¹x+cos⁻¹x=θ+(π/2-θ)=π/2 ✓"},
    {"q": "30. रेखा का सदिश और कार्तीय समीकरण।", "a": "बिंदु(x₁,y₁,z₁), दिशा(a,b,c):\nसदिश: →r=→a+λ→b\nकार्तीय: (x-x₁)/a=(y-y₁)/b=(z-z₁)/c"},
]

MAT_S5 = [
    {"q": "1. sinx का प्रथम सिद्धान्त से अवकलज।", "a": "f'(x)=lim[sin(x+h)-sinx]/h\n=lim[2cos(x+h/2)sin(h/2)]/h\n=cos(x+h/2)·[sin(h/2)/(h/2)]\nh→0: cosx·1 = cosx ✓"},
    {"q": "2. आव्यूह विधि से 2x+3y=5, x+2y=3 हल।", "a": "A=[[2,3],[1,2]], B=[[5],[3]]\n|A|=1, A⁻¹=[[2,-3],[-1,2]]\nX=A⁻¹B=[[1],[1]]\nx=1, y=1 ✓"},
    {"q": "3. f(x)=x³-6x²+9x+15 के उच्चतम/निम्नतम।", "a": "f'(x)=3x²-12x+9=3(x-1)(x-3)\nx=1: f''(1)=-6<0 → उच्चतम, f(1)=19\nx=3: f''(3)=6>0 → निम्नतम, f(3)=15"},
    {"q": "4. dy/dx+2y=e^(-x) हल।", "a": "IF=e^(2x)\nd/dx[y·e^(2x)]=eˣ\ny·e^(2x)=eˣ+C\ny=e^(-x)+Ce^(-2x) ✓"},
    {"q": "5. बेज प्रमेय — सिद्धान्त और उदाहरण।", "a": "P(Aᵢ|B)=P(Aᵢ)P(B|Aᵢ)/ΣP(Aⱼ)P(B|Aⱼ)\nI:3R,4W; II:4R,3W; P(I)=P(II)=1/2\nP(I|R)=(3/14)/(3/14+4/14)=3/7"},
    {"q": "6. LPP — कुर्सी और मेज समस्या।", "a": "Z=100x+300y (max)\n2x+y≤40, x+3y≤45, x,y≥0\nकोने: O(0,0)=0, A(20,0)=2000\nB(15,10)=4500, C(0,15)=4500\nZ_max=₹4500"},
    {"q": "7. अवकलन नियम।", "a": "श्रृंखला: d/dx[f(g(x))]=f'(g(x))·g'(x)\nगुणनफल: d/dx[fg]=f'g+fg'\nभागफल: d/dx[f/g]=(f'g-fg')/g²"},
    {"q": "8. ∫₀^(π/2) log(sinx) dx।", "a": "I=∫₀^(π/2) log(sinx)dx\nगुणधर्म: I=∫₀^(π/2) log(cosx)dx\n2I=∫log(sin2x/2)dx\nI=-(π/2)log2"},
    {"q": "9. 3D ज्यामिति — रेखा और समतल।", "a": "रेखा: →r=→a+λ→b, (x-x₁)/a=(y-y₁)/b=(z-z₁)/c\nसमतल: ax+by+cz+d=0\nकोण (रेखा-समतल): sinθ=|→b·→n|/|→b||→n|\nकोण (दो समतल): cosθ=|→n₁·→n₂|/|→n₁||→n₂|"},
    {"q": "10. वृत्त x²+y²=a² का क्षेत्रफल।", "a": "A=4∫₀ᵃ√(a²-x²)dx\n=[x√(a²-x²)/2+a²/2·sin⁻¹(x/a)]₀ᵃ·4\n=4×πa²/4=πa² ✓"},
]

SUBJECTS={
    "phy":{"name":"⚛️ Physics","obj":PHY_OBJ,"s2":PHY_S2,"s5":PHY_S5},
    "che":{"name":"🧪 Chemistry","obj":CHE_OBJ,"s2":CHE_S2,"s5":CHE_S5},
    "bio":{"name":"🧬 Biology","obj":BIO_OBJ,"s2":BIO_S2,"s5":BIO_S5},
    "hin":{"name":"📚 Hindi","obj":HIN_OBJ,"s2":HIN_S2,"s5":HIN_S5},
    "eng":{"name":"🔤 English","obj":ENG_OBJ,"s2":ENG_S2,"s5":ENG_S5},
    "mat":{"name":"📐 Maths","obj":MAT_OBJ,"s2":MAT_S2,"s5":MAT_S5},
}

def load():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE,'r') as f: return json.load(f)
    except: pass
    return {}

def save(d):
    try:
        with open(DATA_FILE,'w') as f: json.dump(d,f)
    except: pass

def getU(data,uid):
    uid=str(uid)
    if uid not in data: data[uid]={"correct":0,"wrong":0,"skip":0}
    return data[uid]

def main_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⚛️ Physics",callback_data="s_phy"),InlineKeyboardButton("🧪 Chemistry",callback_data="s_che")],
        [InlineKeyboardButton("🧬 Biology",callback_data="s_bio"),InlineKeyboardButton("📚 Hindi",callback_data="s_hin")],
        [InlineKeyboardButton("🔤 English",callback_data="s_eng"),InlineKeyboardButton("📐 Maths",callback_data="s_mat")],
        [InlineKeyboardButton("📊 Score",callback_data="score"),InlineKeyboardButton("❓ Help",callback_data="help")],
    ])

def subj_kb(s):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 Objective (1 से शुरू)",callback_data=f"m_{s}_obj_1")],
        [InlineKeyboardButton("📝 किस नंबर से? (Resume)",callback_data=f"ask_{s}_obj")],
        [InlineKeyboardButton("✏️ 2-Mark Short Answer",callback_data=f"m_{s}_s2_1")],
        [InlineKeyboardButton("📖 5-Mark Long Answer",callback_data=f"m_{s}_s5_1")],
        [InlineKeyboardButton("🔀 Random Mix",callback_data=f"m_{s}_mix_1")],
        [InlineKeyboardButton("🏠 Menu",callback_data="home")],
    ])

def resume_kb(s,mode):
    rows=[]
    for start in range(1,101,10):
        row=[InlineKeyboardButton(str(n),callback_data=f"m_{s}_{mode}_{n}") for n in range(start,min(start+10,101))]
        rows.append(row)
    rows.append([InlineKeyboardButton("🔙 Back",callback_data=f"s_{s}")])
    return InlineKeyboardMarkup(rows)

def opts_kb(opts,s,mode,idx):
    L=["🅐","🅑","🅒","🅓"]
    rows=[[InlineKeyboardButton(f"{L[i]} {o}",callback_data=f"a_{s}_{mode}_{idx}_{i}")] for i,o in enumerate(opts)]
    rows.append([InlineKeyboardButton("⏭ Skip",callback_data=f"sk_{s}_{mode}_{idx}"),InlineKeyboardButton("🏠",callback_data="home")])
    return InlineKeyboardMarkup(rows)

def next_kb(s,mode,idx):
    return InlineKeyboardMarkup([[InlineKeyboardButton("➡️ Next",callback_data=f"nx_{s}_{mode}_{idx}"),InlineKeyboardButton("📊",callback_data="score"),InlineKeyboardButton("🏠",callback_data="home")]])

def sa_kb(s,mode,idx):
    return InlineKeyboardMarkup([[InlineKeyboardButton("➡️ Next",callback_data=f"nx_{s}_{mode}_{idx}"),InlineKeyboardButton("🏠",callback_data="home")]])

async def cmd_start(update:Update,ctx:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌟 *BSEB 2027 Quiz Bot*\n📚 PDF BY DEV\n\n"
        "6 Subjects | 100 Objective each\n"
        "✨ Resume Feature: किसी भी Q से start करो!\n\nSubject चुनो 👇",
        parse_mode="Markdown",reply_markup=main_kb())

async def btn(update:Update,ctx:ContextTypes.DEFAULT_TYPE):
    q=update.callback_query
    await q.answer()
    d=q.data; uid=q.from_user.id
    data=load(); ud=getU(data,uid)

    if d=="home":
        await q.edit_message_text("🌟 *BSEB 2027*\nSubject चुनो 👇",parse_mode="Markdown",reply_markup=main_kb()); return
    if d=="help":
        await q.edit_message_text("❓ *Help:*\n1️⃣ Subject चुनो\n2️⃣ 'किस नंबर से?' से resume करो\n3️⃣ ✅सही=हरा, ❌गलत=लाल\n📊Score से देखो accuracy",parse_mode="Markdown",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠",callback_data="home")]])); return
    if d=="score":
        c=ud.get("correct",0);w=ud.get("wrong",0);sk=ud.get("skip",0);t=c+w+sk
        pct=round(c/t*100) if t>0 else 0
        await q.edit_message_text(f"📊 *Score*\n✅{c} ❌{w} ⏭{sk}\n📝{t} 🎯{pct}%\n{'🏆' if pct>=80 else '💪'}",parse_mode="Markdown",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠",callback_data="home")]])); return
    if d.startswith("s_"):
        s=d[2:]
        if s not in SUBJECTS: return
        info=SUBJECTS[s]
        await q.edit_message_text(f"{info['name']}\n📝 Obj:{len(info['obj'])} ✏️ 2M:{len(info['s2'])} 📖 5M:{len(info['s5'])}\nMode 👇",parse_mode="Markdown",reply_markup=subj_kb(s)); return
    if d.startswith("ask_"):
        parts=d.split("_");s=parts[1];mode=parts[2]
        await q.edit_message_text(f"*किस Q से start करना है?*\n(1-100 में से चुनो) 👇",parse_mode="Markdown",reply_markup=resume_kb(s,mode)); return
    if d.startswith("m_"):
        parts=d.split("_");s=parts[1];mode=parts[2];idx=int(parts[3])-1
        await send_q(q,uid,s,mode,idx,data,ud); return
    if d.startswith("a_"):
        parts=d.split("_");s=parts[1];mode=parts[2];idx=int(parts[3]);chosen=int(parts[4])
        qs=get_qs(s,mode,ud); item=qs[idx]; correct=item["ans"]
        L=["🅐","🅑","🅒","🅓"]
        if chosen==correct:
            ud["correct"]=ud.get("correct",0)+1; res=f"✅ *सही!*\n{L[correct]} {item['opts'][correct]}"
        else:
            ud["wrong"]=ud.get("wrong",0)+1; res=f"❌ *गलत!*\nतुमने: {L[chosen]} {item['opts'][chosen]}\n✅ सही: {L[correct]} {item['opts'][correct]}"
        save(data)
        await q.edit_message_text(f"*Q{idx+1}.* {item['q']}\n\n{res}\n\n📊✅{ud.get('correct',0)} ❌{ud.get('wrong',0)}",parse_mode="Markdown",reply_markup=next_kb(s,mode,idx)); return
    if d.startswith("sk_"):
        parts=d.split("_");s=parts[1];mode=parts[2];idx=int(parts[3])
        ud["skip"]=ud.get("skip",0)+1; save(data)
        await send_q(q,uid,s,mode,idx+1,data,ud); return
    if d.startswith("nx_"):
        parts=d.split("_");s=parts[1];mode=parts[2];idx=int(parts[3])
        await send_q(q,uid,s,mode,idx+1,data,ud); return

def get_qs(s,mode,ud):
    info=SUBJECTS[s]
    if mode=="obj": return info["obj"]
    if mode=="s2": return info["s2"]
    if mode=="s5": return info["s5"]
    if mode=="mix":
        if "mq" not in ud or ud.get("ms")!=s:
            m=info["obj"].copy(); random.shuffle(m); ud["mq"]=m; ud["ms"]=s
        return ud["mq"]
    return info["obj"]

async def send_q(q,uid,s,mode,idx,data,ud):
    info=SUBJECTS[s]; qs=get_qs(s,mode,ud); save(data)
    if idx>=len(qs):
        c=ud.get("correct",0);w=ud.get("wrong",0)
        pct=round(c/(c+w)*100) if c+w>0 else 0
        await q.edit_message_text(f"🏁 *Quiz Complete!*\n✅{c} ❌{w} 🎯{pct}%\n{'🌟 Excellent!' if pct>=80 else '💪 Keep practicing!'}",parse_mode="Markdown",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 Again",callback_data=f"m_{s}_{mode}_1")],[InlineKeyboardButton("🏠 Menu",callback_data="home")]]))
        return
    item=qs[idx]; total=len(qs)
    if mode in ("obj","mix"):
        await q.edit_message_text(f"{info['name']}\n━━━━━━━━━━━━━━━\n*Q{idx+1}/{total}*\n\n❓ {item['q']}",parse_mode="Markdown",reply_markup=opts_kb(item["opts"],s,mode,idx))
    elif mode=="s2":
        await q.edit_message_text(f"{info['name']} ✏️ *2M* | *{idx+1}/{total}*\n\n📌 {item['q']}\n\n📝 *उत्तर:*\n{item['a']}",parse_mode="Markdown",reply_markup=sa_kb(s,mode,idx))
    elif mode=="s5":
        await q.edit_message_text(f"{info['name']} 📖 *5M* | *{idx+1}/{total}*\n\n📌 {item['q']}\n\n📖 *उत्तर:*\n{item['a']}",parse_mode="Markdown",reply_markup=sa_kb(s,mode,idx))

async def ai_chat(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    if not user_text:
        return
    if not gemini_model:
        await update.message.reply_text(
            "⚠️ AI feature अभी सेटअप नहीं है।\n"
            "Railway पर GEMINI_API_KEY environment variable add करें।"
        )
        return
    await ctx.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    try:
        # Gemini expects a prompt. We'll use a system-like instruction in the first turn.
        response = gemini_model.generate_content(
            f"तुम BSEB Class 12 student की मदद करने वाले एक हिंदी/English AI सहायक हो। किसी भी सवाल का सही, साफ और संक्षिप्त जवाब दो — चाहे वह पढ़ाई से जुड़ा हो या कुछ भी और।\n\nप्रश्न: {user_text}"
        )
        answer = response.text.strip()
        if not answer:
            answer = "माफ़ करना, मुझे जवाब नहीं मिल पाया। दोबारा पूछो।"
    except Exception as e:
        answer = f"⚠️ AI error: {e}"
    for i in range(0, len(answer), 4000):
        await update.message.reply_text(answer[i:i+4000])

def main():
    print("🌟 BSEB Bot starting with Google Gemini...")
    app=Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start",cmd_start))
    app.add_handler(CommandHandler("help",cmd_start))
    app.add_handler(CallbackQueryHandler(btn))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_chat))
    print("✅ Running!")
    app.run_polling(drop_pending_updates=True)

if __name__=="__main__":
    main()
