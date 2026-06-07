import asyncio
import random
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes
)

BOT_TOKEN = "8792779625:AAEyyDTvoO1jTqgvha6GKvO2u64AwJGPFBw"

PHY_OBJ = [
    {"q": "विद्युत क्षेत्र की SI इकाई है:", "opts": ["N/C", "C/N", "V·m", "J/C"], "ans": 0},
    {"q": "कूलॉम के नियम में बल किसके व्युत्क्रमानुपाती है?", "opts": ["r", "r²", "r³", "√r"], "ans": 1},
    {"q": "गाउस नियम: ΦE = ?", "opts": ["q/ε₀", "ε₀/q", "q·ε₀", "q²/ε₀"], "ans": 0},
    {"q": "विद्युत विभव V = ?", "opts": ["kq/r²", "kq/r", "kq·r", "k/qr"], "ans": 1},
    {"q": "समविभव पृष्ठ पर कार्य होता है:", "opts": ["अधिकतम", "न्यूनतम", "शून्य", "अनंत"], "ans": 2},
    {"q": "संधारित्र की ऊर्जा U = ?", "opts": ["CV", "CV²", "½CV²", "2CV"], "ans": 2},
    {"q": "ε₀ = ?", "opts": ["8.85×10⁻¹²", "9×10⁹", "6.67×10⁻¹¹", "1.6×10⁻¹⁹"], "ans": 0},
    {"q": "ओम नियम में R किस पर निर्भर नहीं?", "opts": ["तापमान", "V और I दोनों पर", "लंबाई", "क्षेत्रफल"], "ans": 1},
    {"q": "विद्युत शक्ति P = ?", "opts": ["VI", "V/I", "I/V", "V+I"], "ans": 0},
    {"q": "किर्चहॉफ प्रथम नियम का आधार:", "opts": ["ऊर्जा संरक्षण", "आवेश संरक्षण", "संवेग", "द्रव्यमान"], "ans": 1},
    {"q": "व्हीटस्टोन ब्रिज: P/Q = ?", "opts": ["R/S", "S/R", "P·Q", "P+Q"], "ans": 0},
    {"q": "लॉरेन्ज बल F = ?", "opts": ["qE", "q(v×B)", "qvB", "q(E+v×B)"], "ans": 3},
    {"q": "साइक्लोट्रॉन में आवृत्ति किस पर निर्भर नहीं?", "opts": ["आवेश q", "द्रव्यमान m", "वेग v", "चुंबकीय क्षेत्र B"], "ans": 2},
    {"q": "∮B·dl = ?", "opts": ["μ₀I", "μ₀/I", "I/μ₀", "μ₀I²"], "ans": 0},
    {"q": "वृत्ताकार लूप के केंद्र पर B = ?", "opts": ["μ₀I/2R", "μ₀I/R", "μ₀I/4πR", "2μ₀I/R"], "ans": 0},
    {"q": "चुंबकीय फ्लक्स का SI मात्रक:", "opts": ["टेस्ला", "हेनरी", "वेबर", "एम्पियर"], "ans": 2},
    {"q": "फैराडे नियम: ε = ?", "opts": ["dΦ/dt", "-dΦ/dt", "Φ/t", "-Φ·t"], "ans": 1},
    {"q": "स्व-प्रेरकत्व SI मात्रक:", "opts": ["वेबर", "हेनरी", "टेस्ला", "फैराड"], "ans": 1},
    {"q": "AC परिपथ में Z = ?", "opts": ["R+XL+XC", "√(R²+(XL-XC)²)", "R·XL", "XL-XC"], "ans": 1},
    {"q": "Power factor = ?", "opts": ["R/Z", "Z/R", "XL/Z", "XC/R"], "ans": 0},
    {"q": "AC का rms मान = ?", "opts": ["I₀", "I₀/2", "I₀/√2", "√2·I₀"], "ans": 2},
    {"q": "EM तरंगों की खोज किसने की?", "opts": ["फैराडे", "मैक्सवेल", "हर्ट्ज", "न्यूटन"], "ans": 1},
    {"q": "सबसे कम तरंगदैर्ध्य किसकी?", "opts": ["रेडियो", "X-Ray", "दृश्य", "गामा किरण"], "ans": 3},
    {"q": "स्नेल का नियम:", "opts": ["n₁sinθ₁=n₂sinθ₂", "n₁cosθ₁=n₂cosθ₂", "n₁θ₁=n₂θ₂", "n₁/sinθ₁=n₂"], "ans": 0},
    {"q": "दर्पण सूत्र:", "opts": ["1/v+1/u=1/f", "1/f=1/v-1/u", "v+u=f", "f=u·v"], "ans": 0},
    {"q": "पूर्ण आंतरिक परावर्तन:", "opts": ["θ < θc", "θ > θc", "θ = 0", "n₁ < n₂"], "ans": 1},
    {"q": "मानव नेत्र की निकट दृष्टि दूरी:", "opts": ["10cm", "25cm", "50cm", "100cm"], "ans": 1},
    {"q": "यंग के प्रयोग में β = ?", "opts": ["λD/d", "λd/D", "Dd/λ", "D/λd"], "ans": 0},
    {"q": "प्रकाश विद्युत प्रभाव: KEmax = ?", "opts": ["hν + φ", "hν - φ", "hν/φ", "φ - hν"], "ans": 1},
    {"q": "डी-ब्रॉयली: λ = ?", "opts": ["h/mv", "mv/h", "h·mv", "m/hv"], "ans": 0},
    {"q": "बोर मॉडल: कोणीय संवेग = ?", "opts": ["nh/2π", "h/2πn", "2πn/h", "nh"], "ans": 0},
    {"q": "हाइड्रोजन की आयनन ऊर्जा:", "opts": ["13.6eV", "3.4eV", "1.51eV", "0.85eV"], "ans": 0},
    {"q": "बाल्मर श्रेणी किस क्षेत्र में?", "opts": ["पराबैंगनी", "दृश्य", "अवरक्त", "X-ray"], "ans": 1},
    {"q": "अर्ध-आयु T₁/₂ = ?", "opts": ["λ/0.693", "0.693/λ", "0.693·λ", "1/λ"], "ans": 1},
    {"q": "p-n जंक्शन अग्र अभिनति में धारा:", "opts": ["शून्य", "अत्यल्प", "अधिक", "असीमित"], "ans": 2},
    {"q": "n-type में डोपेंट:", "opts": ["त्रिसंयोजी", "पंचसंयोजी", "द्विसंयोजी", "शून्यसंयोजी"], "ans": 1},
    {"q": "NAND गेट = AND + ?", "opts": ["OR", "NOT", "NOR", "XOR"], "ans": 1},
    {"q": "OR गेट का Boolean: Y = ?", "opts": ["A·B", "A+B", "Ā", "A⊕B"], "ans": 1},
    {"q": "1 eV = ?", "opts": ["1.6×10⁻¹⁹ J", "1.6×10⁻¹⁰ J", "9.1×10⁻³¹ J", "6.67×10⁻¹¹ J"], "ans": 0},
    {"q": "प्रकाश की चाल = ?", "opts": ["3×10⁸ m/s", "3×10⁶ m/s", "3×10¹⁰ m/s", "3×10⁴ m/s"], "ans": 0},
]

PHY_S2 = [
    {"q": "1. कूलॉम के नियम को लिखिए। k का मान बताइए।", "a": "F = kq₁q₂/r² जहाँ k = 9×10⁹ N·m²/C²\nयह बल दोनों आवेशों के गुणनफल के समानुपाती और दूरी के वर्ग के व्युत्क्रमानुपाती होता है।"},
    {"q": "2. समविभव पृष्ठ किसे कहते हैं? दो गुण लिखिए।", "a": "वह पृष्ठ जिस पर सभी बिंदुओं का विभव समान हो।\n(1) इस पर कार्य शून्य होता है।\n(2) क्षेत्र रेखाएँ इसके लंबवत होती हैं।"},
    {"q": "3. ओम का नियम लिखिए और दो सीमाएँ बताइए।", "a": "V = IR — स्थिर ताप पर धारा विभवांतर के समानुपाती।\nसीमाएँ:\n(1) अर्धचालकों में लागू नहीं।\n(2) गैसों में लागू नहीं।"},
    {"q": "4. किर्चहॉफ के दोनों नियम लिखिए।", "a": "(1) KCL: किसी जंक्शन पर ΣI = 0\n(2) KVL: किसी बंद पाश में ΣV = 0"},
    {"q": "5. लेंज का नियम लिखिए।", "a": "प्रेरित धारा की दिशा उस कारण का विरोध करती है जिससे वह उत्पन्न हुई।\nयह ऊर्जा संरक्षण पर आधारित है।"},
    {"q": "6. AC और DC में दो अंतर लिखिए।", "a": "(1) AC की दिशा बदलती है; DC स्थिर।\n(2) AC को ट्रांसफॉर्मर से घटाया-बढ़ाया जा सकता है।"},
    {"q": "7. पूर्ण आंतरिक परावर्तन की शर्तें।", "a": "(1) प्रकाश सघन से विरल माध्यम में जाए।\n(2) आपतन कोण क्रांतिक कोण से अधिक हो।"},
    {"q": "8. प्रकाश विद्युत प्रभाव — आइंस्टीन का समीकरण।", "a": "KEmax = hν - φ = h(ν - ν₀)\nजब धातु पर उचित आवृत्ति का प्रकाश पड़े तो इलेक्ट्रॉन निकलते हैं।"},
    {"q": "9. बोर के परमाणु मॉडल की दो अभिधारणाएँ।", "a": "(1) इलेक्ट्रॉन निश्चित कक्षाओं में घूमते हैं।\n(2) L = nh/2π का गुणज होता है।"},
    {"q": "10. p-n जंक्शन में अग्र और पश्च अभिनति।", "a": "अग्र: p को + और n को − → अधिक धारा।\nपश्च: विपरीत → धारा नहीं बहती।"},
]

PHY_S5 = [
    {"q": "1. गाउस का नियम — अनंत आवेशित तार के लिए E ज्ञात कीजिए।", "a": "गाउस नियम: ΦE = q/ε₀\nE × 2πrl = λl/ε₀\n∴ E = λ/(2πε₀r)\nदिशा: तार से त्रिज्य दिशा में।"},
    {"q": "2. बायो-सावर्ट नियम — वृत्ताकार लूप के केंद्र पर B।", "a": "dB = μ₀Idl sinθ/(4πr²)\nθ=90°, r=R → B = μ₀I/(2R)\nN फेरों के लिए: B = μ₀NI/(2R)"},
    {"q": "3. LCR श्रेणी परिपथ की अनुनाद आवृत्ति।", "a": "Z = √[R²+(XL-XC)²]\nअनुनाद: XL=XC → ω₀=1/√LC\nf₀ = 1/(2π√LC)\nअनुनाद पर Z=R (न्यूनतम), I अधिकतम।"},
    {"q": "4. लेंस निर्माता समीकरण व्युत्पन्न कीजिए।", "a": "n₂/v - n₁/u = (n₂-n₁)/R\nदोनों पृष्ठ जोड़ने पर:\n1/f = (n-1)(1/R₁ - 1/R₂)"},
    {"q": "5. फोटोइलेक्ट्रिक प्रभाव और बोर मॉडल से Eₙ = -13.6/n²।", "a": "KEmax = hν - φ\nबोर: mvr=nh/2π, mv²/r=ke²/r²\nहल: Eₙ = -13.6/n² eV\nn=1: -13.6 eV, n=∞: 0"},
    {"q": "6. p-n जंक्शन पूर्ण-तरंग दिष्टकारी।", "a": "दो डायोड + केंद्र-नल ट्रांसफॉर्मर।\nधनात्मक चक्र: D₁ → R_L में धारा\nऋणात्मक चक्र: D₂ → R_L में धारा (same direction)\nदक्षता = 81.2%"},
]

CHE_OBJ = [
    {"q": "NaCl की संरचना है:", "opts": ["Simple cubic", "FCC", "BCC", "HCP"], "ans": 1},
    {"q": "FCC में परमाणुओं की संख्या:", "opts": ["1", "2", "4", "6"], "ans": 2},
    {"q": "BCC में परमाणुओं की संख्या:", "opts": ["1", "2", "4", "3"], "ans": 1},
    {"q": "FCC packing efficiency:", "opts": ["52%", "68%", "74%", "26%"], "ans": 2},
    {"q": "राउल्ट नियम: ΔP/P° = ?", "opts": ["n₂/(n₁+n₂)", "n₁/(n₁+n₂)", "n₁·n₂", "n₁/n₂"], "ans": 0},
    {"q": "परासरण दाब π = ?", "opts": ["MRT", "nRT/V", "CRT", "RT/C"], "ans": 2},
    {"q": "एनोड पर होती है:", "opts": ["अपचयन", "ऑक्सीकरण", "कोई नहीं", "दोनों"], "ans": 1},
    {"q": "फैराडे I नियम: m = ?", "opts": ["ZIt", "ZI/t", "It/Z", "Z/It"], "ans": 0},
    {"q": "अभिक्रिया वेग r = ?", "opts": ["k[A]ⁿ", "k/[A]ⁿ", "k·t", "[A]/k"], "ans": 0},
    {"q": "t₁/₂ = 0.693/k — किस कोटि?", "opts": ["0", "1st", "2nd", "3rd"], "ans": 1},
    {"q": "KMnO₄ में Mn की ऑक्सीकरण अवस्था:", "opts": ["+4", "+6", "+7", "+2"], "ans": 2},
    {"q": "[Co(NH₃)₆]³⁺ में Co की ऑक्सीकरण अवस्था:", "opts": ["+1", "+2", "+3", "+6"], "ans": 2},
    {"q": "SN2 में होता है:", "opts": ["Retention", "Racemisation", "Walden Inversion", "Elimination"], "ans": 2},
    {"q": "Fehling's test: positive किसके लिए?", "opts": ["दोनों", "Aldehyde", "Ketone", "दोनों ऋणात्मक"], "ans": 1},
    {"q": "Tollens test: positive किसके लिए?", "opts": ["Ketone", "Aldehyde", "Alcohol", "Ether"], "ans": 1},
    {"q": "Glucose का अणुसूत्र:", "opts": ["C₆H₁₂O₆", "C₁₂H₂₂O₁₁", "C₆H₁₀O₅", "C₅H₁₀O₅"], "ans": 0},
    {"q": "DNA में Thymine का जोड़ा:", "opts": ["Adenine", "Guanine", "Cytosine", "Uracil"], "ans": 0},
    {"q": "Nylon-6,6 है:", "opts": ["Addition polymer", "Condensation polymer", "Elastomer", "Plastic"], "ans": 1},
    {"q": "Aspirin है:", "opts": ["Analgesic", "Antiseptic", "Antacid", "Antibiotic"], "ans": 0},
    {"q": "Molarity का मात्रक:", "opts": ["mol/kg", "mol/L", "g/L", "mol/mol"], "ans": 1},
]

CHE_S2 = [
    {"q": "1. राउल्ट के नियम और परासरण दाब का सूत्र।", "a": "राउल्ट: P = x_solvent × P°\nΔP/P° = n₂/(n₁+n₂)\nπ = CRT"},
    {"q": "2. प्रथम कोटि अभिक्रिया की अर्ध-आयु।", "a": "t₁/₂ = 0.693/k\nk पर निर्भर, [A] पर नहीं।\nk = Ae^(-Ea/RT)"},
    {"q": "3. नेर्न्स्ट समीकरण।", "a": "E = E° - (RT/nF)·lnQ\n298K: E = E° - (0.0592/n)·logQ"},
    {"q": "4. d-ब्लॉक में रंगीन आयन क्यों?", "a": "अपूर्ण d-कक्षक → d-d transition\nदृश्य प्रकाश अवशोषण → रंग दिखता है।"},
    {"q": "5. SN1 और SN2 में अंतर।", "a": "SN1: 2 चरण, carbocation, 3°>2°>1°\nSN2: 1 चरण, Walden Inversion, 1°>2°>3°"},
    {"q": "6. Fehling's और Tollens test।", "a": "Fehling's: Aldehyde → ईंट-लाल Cu₂O\nTollens: Aldehyde → चाँदी का दर्पण"},
    {"q": "7. Van't Hoff गुणांक i।", "a": "NaCl → Na⁺+Cl⁻, i≈2\nΔTb = i·Kb·m\nπ = i·CRT"},
    {"q": "8. Gabriel synthesis।", "a": "Phthalimide से शुद्ध 1° amine बनती है।\n2° और 3° amine नहीं बनते।"},
    {"q": "9. DNA और RNA में अंतर।", "a": "DNA: Deoxyribose, Thymine, Double helix\nRNA: Ribose, Uracil, Single strand"},
    {"q": "10. Addition और Condensation polymer।", "a": "Addition: PVC, Teflon — उप-उत्पाद नहीं।\nCondensation: Nylon — H₂O निकलती है।"},
]

CHE_S5 = [
    {"q": "1. फैराडे के नियम और विद्युत रासायनिक श्रेणी।", "a": "m=ZIt, Z=E/96500\nE°cell = E°cathode - E°anode\nΔG° = -nFE°cell"},
    {"q": "2. उत्प्रेरण के प्रकार और एंजाइम।", "a": "समांगी: एक प्रावस्था\nविषमांगी: अलग प्रावस्था\nएंजाइम: Lock-and-key model, 37°C पर अधिकतम"},
    {"q": "3. Crystal Field Theory — Octahedral complex।", "a": "eg: dx²-y², dz² (+0.6Δo)\nt2g: dxy,dyz,dxz (-0.4Δo)\nStrong field → low spin, Weak field → high spin"},
    {"q": "4. बहुलकीकरण और जैव-निम्नीकरणीय polymer।", "a": "Addition: PE, PVC\nCondensation: Nylon, PET\nJaiv: PHBV — सूक्ष्मजीव तोड़ सकते हैं"},
    {"q": "5. अमीनो अम्ल और Zwitter ion।", "a": "H₂N-CHR-COOH\nZwitter: H₃N⁺-CHR-COO⁻\nIsoelectric point पर अधिकतम"},
    {"q": "6. p-Block Group 15 हाइड्राइड।", "a": "क्षारीयता: NH₃>PH₃>AsH₃\nस्थायित्व: NH₃>PH₃>AsH₃\nNH₃ में H-bond → उच्च क्वथनांक"},
]

BIO_OBJ = [
    {"q": "द्विनिषेचन में बनता है:", "opts": ["केवल भ्रूण", "केवल भ्रूणपोष", "भ्रूण + भ्रूणपोष", "बीज"], "ans": 2},
    {"q": "आर्तव चक्र लगभग:", "opts": ["14 दिन", "21 दिन", "28 दिन", "35 दिन"], "ans": 2},
    {"q": "मेंडल का पृथक्करण नियम:", "opts": ["स्वतंत्र अपव्यूहन", "प्रभाविता", "पृथक्करण", "युग्मन"], "ans": 2},
    {"q": "DNA में Thymine का जोड़ा:", "opts": ["Adenine", "Guanine", "Cytosine", "Uracil"], "ans": 0},
    {"q": "AUG कोडॉन:", "opts": ["Leucine", "Methionine (Start)", "Stop", "Alanine"], "ans": 1},
    {"q": "PCR पूरा नाम:", "opts": ["Protein Chain Reaction", "Polymerase Chain Reaction", "Polymer Code", "None"], "ans": 1},
    {"q": "Bt toxin मारता है:", "opts": ["Fungi", "Bacteria", "Lepidopteran larvae", "Virus"], "ans": 2},
    {"q": "मनुष्य में Autosomes:", "opts": ["23 जोड़े", "22 जोड़े", "46", "44"], "ans": 1},
    {"q": "Down's syndrome में chromosomes:", "opts": ["45", "46", "47", "48"], "ans": 2},
    {"q": "10% नियम:", "opts": ["10% ऊर्जा अगले level को", "20%", "50%", "100%"], "ans": 0},
    {"q": "In-situ conservation:", "opts": ["Zoo", "National Park", "Seed Bank", "Botanical Garden"], "ans": 1},
    {"q": "Light Reaction कहाँ?", "opts": ["Stroma", "Thylakoid membrane", "Mitochondria", "Cytoplasm"], "ans": 1},
    {"q": "Auxin मुख्य कार्य:", "opts": ["पत्ती रंग", "Cell elongation", "फूल खिलना", "Seed dormancy"], "ans": 1},
    {"q": "Human heart में chambers:", "opts": ["2", "3", "4", "5"], "ans": 2},
    {"q": "AIDS कारण:", "opts": ["Bacteria", "HIV (Retrovirus)", "Fungi", "Protozoa"], "ans": 1},
    {"q": "Hardy-Weinberg: p²+2pq+q² = ?", "opts": ["0", "1", "2", "p+q"], "ans": 1},
    {"q": "Miller-Urey प्रयोग में बने:", "opts": ["DNA", "Amino acids", "RNA", "Proteins"], "ans": 1},
    {"q": "t-RNA का काम:", "opts": ["DNA पढ़ना", "Amino acid ribosome तक ले जाना", "mRNA बनाना", "DNA copy"], "ans": 1},
    {"q": "Golden Rice में अधिकता:", "opts": ["Vitamin C", "Vitamin A (β-carotene)", "Iron", "Protein"], "ans": 1},
    {"q": "Adaptive radiation उदाहरण:", "opts": ["Darwin's Finches", "Bacteria", "Virus", "Fungi"], "ans": 0},
]

BIO_S2 = [
    {"q": "1. द्विनिषेचन क्या है?", "a": "(1) नर युग्मक 1 + अंडकोशिका → भ्रूण (2n)\n(2) नर युग्मक 2 + द्वितीयक नाभिक → भ्रूणपोष (3n)\nकेवल Angiosperms में।"},
    {"q": "2. मेंडल का पृथक्करण नियम।", "a": "Tt×Tt → TT:Tt:tt = 1:2:1\nलंबा:बौना = 3:1\nयुग्मकजनन में alleles अलग होते हैं।"},
    {"q": "3. lac operon क्या है?", "a": "E. coli में lactose उपस्थित → Repressor निष्क्रिय\nβ-galactosidase बनती है। Inducible operon।"},
    {"q": "4. PCR के तीन चरण।", "a": "(1) Denaturation 93-96°C\n(2) Annealing 50-65°C\n(3) Extension 72°C — Taq polymerase"},
    {"q": "5. Bt cotton कैसे कार्य करता है?", "a": "Bacillus thuringiensis का cry gene डाला।\nBollworm खाता है → आँत नष्ट → मरता है।"},
    {"q": "6. Down's Turner's Klinefelter's।", "a": "Down's: 47 (Trisomy 21)\nTurner's: 45,XO — बाँझ females\nKlinefelter's: 47,XXY — बाँझ male"},
    {"q": "7. Hardy-Weinberg की शर्तें।", "a": "(1) बड़ी जनसंख्या (2) यादृच्छिक मैथुन\n(3) कोई उत्परिवर्तन नहीं (4) कोई प्रवासन नहीं\n(5) कोई चयन नहीं"},
    {"q": "8. Auxin और Gibberellin में अंतर।", "a": "Auxin: Cell elongation, apical dominance\nGibberellin: Stem elongation, seed germination"},
    {"q": "9. Active और Passive immunity।", "a": "Active: Body antibody बनाता है — टीकाकरण\nPassive: Ready antibody दी जाती है — antivenom"},
    {"q": "10. Miller-Urey प्रयोग।", "a": "CH₄+NH₃+H₂+H₂O + विद्युत स्पार्क → Amino acids\nनिष्कर्ष: जीवन के घटक अजैविक परिस्थितियों में बन सकते हैं।"},
]

BIO_S5 = [
    {"q": "1. द्विनिषेचन की पूरी प्रक्रिया।", "a": "परागण → पराग नलिका → बीजांडद्वार\nनर युग्मक 1 + अंड → युग्मनज (2n) → भ्रूण\nनर युग्मक 2 + ध्रुवीय नाभिक → भ्रूणपोष (3n)\nकेवल Angiosperms में।"},
    {"q": "2. Dihybrid Cross में 9:3:3:1।", "a": "RRYY × rryy → F1: RrYy\nF1×F1: 9 R_Y_ : 3 R_yy : 3 rrY_ : 1 rryy\n9:3:3:1 अनुपात।"},
    {"q": "3. Recombinant DNA Technology।", "a": "Restriction Enzyme → काटना\nLigation → जोड़ना\nTransformation → Host में डालना\nSelection → Antibiotic में उगाना"},
    {"q": "4. Darwin का Natural Selection।", "a": "अत्यधिक प्रजनन + संसाधन सीमित → संघर्ष\nउपयुक्त जीवित → वंशानुगति\nIndustrial Melanism: Biston betularia उदाहरण।"},
    {"q": "5. मानव प्रतिरक्षा और AIDS।", "a": "HIV → CD4⁺ T-cells नष्ट\nCD4 <200/μL → AIDS\nART से नियंत्रण\nAntibody (B-cells) और Cytotoxic (T-cells)।"},
    {"q": "6. पारितंत्र ऊर्जा प्रवाह।", "a": "10% नियम: 10000J→1000J→100J→10J\nएकदिशीय प्रवाह\nशेष 90% श्वसन+उष्मा\nऊर्जा पिरामिड: हमेशा सीधा।"},
]

SUBJECTS = {
    "physics":   {"name": "⚛️ Physics",   "emoji": "⚛️", "obj": PHY_OBJ, "s2": PHY_S2, "s5": PHY_S5},
    "chemistry": {"name": "🧪 Chemistry", "emoji": "🧪", "obj": CHE_OBJ, "s2": CHE_S2, "s5": CHE_S5},
    "biology":   {"name": "🧬 Biology",   "emoji": "🧬", "obj": BIO_OBJ, "s2": BIO_S2, "s5": BIO_S5},
}

user_state = {}

def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⚛️ Physics", callback_data="subj_physics"),
         InlineKeyboardButton("🧪 Chemistry", callback_data="subj_chemistry")],
        [InlineKeyboardButton("🧬 Biology", callback_data="subj_biology")],
        [InlineKeyboardButton("📊 My Score", callback_data="score"),
         InlineKeyboardButton("ℹ️ Help", callback_data="help")],
    ])

def subject_menu_keyboard(subj):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 Objective Quiz", callback_data=f"mode_{subj}_obj")],
        [InlineKeyboardButton("✏️ 2-Mark Short Answer", callback_data=f"mode_{subj}_s2")],
        [InlineKeyboardButton("📖 5-Mark Long Answer", callback_data=f"mode_{subj}_s5")],
        [InlineKeyboardButton("🔀 Random Mix Quiz", callback_data=f"mode_{subj}_mix")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="home")],
    ])

def options_keyboard(opts, subj, q_idx):
    keys = ["🅐", "🅑", "🅒", "🅓"]
    keyboard = [[InlineKeyboardButton(f"{keys[i]} {opt}", callback_data=f"ans_{subj}_{q_idx}_{i}")] for i, opt in enumerate(opts)]
    keyboard.append([InlineKeyboardButton("⏭ Skip", callback_data=f"skip_{subj}_{q_idx}")])
    keyboard.append([InlineKeyboardButton("🏠 Menu", callback_data="home")])
    return InlineKeyboardMarkup(keyboard)

def next_keyboard(subj, mode, q_idx):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➡️ Next Question", callback_data=f"next_{subj}_{mode}_{q_idx}")],
        [InlineKeyboardButton("📊 Score", callback_data="score"), InlineKeyboardButton("🏠 Menu", callback_data="home")],
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = (
        f"🌿 *PDF BY DEV — BSEB 2027 Quiz Bot*\n\n"
        f"नमस्ते {user.first_name}! 🙏\n\n"
        f"*Subjects:*\n"
        f"⚛️ Physics | 🧪 Chemistry | 🧬 Biology\n\n"
        f"*Modes:*\n"
        f"📝 Objective | ✏️ 2-Mark | 📖 5-Mark | 🔀 Mix\n\n"
        f"Subject चुनो 👇"
    )
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=main_menu_keyboard())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id

    if data == "home":
        await query.edit_message_text("🌿 *PDF BY DEV — BSEB 2027*\n\nSubject चुनो 👇", parse_mode="Markdown", reply_markup=main_menu_keyboard())
        return

    if data == "help":
        text = ("ℹ️ *Bot कैसे use करें:*\n\n"
                "1️⃣ Subject चुनो\n2️⃣ Mode चुनो\n"
                "3️⃣ Objective में ✅ सही = हरा, ❌ गलत = लाल + सही answer\n"
                "📊 My Score — अपना score देखो")
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Menu", callback_data="home")]]))
        return

    if data == "score":
        s = user_state.get(user_id, {})
        c = s.get("total_correct", 0)
        w = s.get("total_wrong", 0)
        sk = s.get("total_skip", 0)
        t = c + w + sk
        pct = round(c/t*100) if t > 0 else 0
        text = f"📊 *आपका Score*\n\n✅ सही: {c}\n❌ गलत: {w}\n⏭ Skip: {sk}\n📝 कुल: {t}\n🎯 Accuracy: {pct}%\n\n{'🏆 शानदार!' if pct >= 80 else '💪 और practice करो!'}"
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Menu", callback_data="home")]]))
        return

    if data.startswith("subj_"):
        subj = data.split("_")[1]
        info = SUBJECTS[subj]
        text = f"{info['name']} — *BSEB 2027*\n\n📝 Objective: {len(info['obj'])}\n✏️ 2-Mark: {len(info['s2'])}\n📖 5-Mark: {len(info['s5'])}\n\nMode चुनो 👇"
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=subject_menu_keyboard(subj))
        return

    if data.startswith("mode_"):
        parts = data.split("_")
        subj, mode = parts[1], parts[2]
        if user_id not in user_state: user_state[user_id] = {}
        user_state[user_id].update({"subject": subj, "mode": mode, "q_index": 0, "session_correct": 0, "session_wrong": 0})
        if mode == "mix":
            mixed = SUBJECTS[subj]["obj"].copy()
            random.shuffle(mixed)
            user_state[user_id]["mix_questions"] = mixed
        await send_question(query, user_id, subj, mode, 0)
        return

    if data.startswith("ans_"):
        parts = data.split("_")
        subj, q_idx, chosen = parts[1], int(parts[2]), int(parts[3])
        mode = user_state.get(user_id, {}).get("mode", "obj")
        questions = user_state.get(user_id, {}).get("mix_questions", SUBJECTS[subj]["obj"]) if mode == "mix" else SUBJECTS[subj]["obj"]
        if q_idx >= len(questions): return
        q = questions[q_idx]
        correct = q["ans"]
        keys = ["🅐", "🅑", "🅒", "🅓"]
        if user_id not in user_state: user_state[user_id] = {}
        if chosen == correct:
            result = f"✅ *बिल्कुल सही!* 🎉\n\n*{keys[correct]} {q['opts'][correct]}*"
            user_state[user_id]["total_correct"] = user_state[user_id].get("total_correct", 0) + 1
            user_state[user_id]["session_correct"] = user_state[user_id].get("session_correct", 0) + 1
        else:
            result = f"❌ *गलत!*\n\nतुमने चुना: {keys[chosen]} {q['opts'][chosen]}\n\n✅ *सही: {keys[correct]} {q['opts'][correct]}*"
            user_state[user_id]["total_wrong"] = user_state[user_id].get("total_wrong", 0) + 1
            user_state[user_id]["session_wrong"] = user_state[user_id].get("session_wrong", 0) + 1
        sc = user_state[user_id].get("session_correct", 0)
        sw = user_state[user_id].get("session_wrong", 0)
        text = f"*Q{q_idx+1}.* {q['q']}\n\n{result}\n\n📊 Session: ✅{sc} ❌{sw}"
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=next_keyboard(subj, mode, q_idx))
        return

    if data.startswith("skip_"):
        parts = data.split("_")
        subj, q_idx = parts[1], int(parts[2])
        mode = user_state.get(user_id, {}).get("mode", "obj")
        if user_id not in user_state: user_state[user_id] = {}
        user_state[user_id]["total_skip"] = user_state[user_id].get("total_skip", 0) + 1
        await send_question(query, user_id, subj, mode, q_idx + 1)
        return

    if data.startswith("next_"):
        parts = data.split("_")
        subj, mode, q_idx = parts[1], parts[2], int(parts[3])
        await send_question(query, user_id, subj, mode, q_idx + 1)
        return

async def send_question(query, user_id, subj, mode, q_idx):
    info = SUBJECTS[subj]
    if mode in ("obj", "mix"):
        questions = user_state.get(user_id, {}).get("mix_questions", info["obj"]) if mode == "mix" else info["obj"]
        if q_idx >= len(questions):
            sc = user_state.get(user_id, {}).get("session_correct", 0)
            sw = user_state.get(user_id, {}).get("session_wrong", 0)
            t = sc + sw
            pct = round(sc/t*100) if t > 0 else 0
            text = f"🏆 *Quiz Complete!*\n\n✅ सही: {sc}\n❌ गलत: {sw}\n🎯 Score: {pct}%\n\n{'🌟 Outstanding!' if pct >= 90 else '💪 Keep practicing!'}"
            await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 Again", callback_data=f"mode_{subj}_{mode}")], [InlineKeyboardButton("🏠 Menu", callback_data="home")]]))
            return
        q = questions[q_idx]
        text = f"{info['emoji']} *{info['name']}*\n━━━━━━━━━━━━━━━━━\n*Q{q_idx+1}/{len(questions)}*\n\n❓ {q['q']}"
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=options_keyboard(q["opts"], subj, q_idx))
    elif mode in ("s2", "s5"):
        questions = info[mode]
        if q_idx >= len(questions):
            await query.edit_message_text("✅ सभी questions देख लिए! 👏", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Menu", callback_data="home")]]))
            return
        q = questions[q_idx]
        mark = "2 Mark" if mode == "s2" else "5 Mark"
        text = f"{info['emoji']} *{info['name']} — {mark}*\n━━━━━━━━━━━━━━━━━\n*{q['q']}*\n\n📝 *उत्तर:*\n{q['a']}"
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("➡️ Next", callback_data=f"next_{subj}_{mode}_{q_idx}"), InlineKeyboardButton("🏠 Menu", callback_data="home")]]))

def main():
    print("🌿 BSEB 2027 Bot Starting...")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("✅ Bot Running!")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
