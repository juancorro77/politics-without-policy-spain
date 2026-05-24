# Politics without Policy? Measuring Agenda Shift and Executive Evasion in the Spanish Congress of Deputies (2019-2026)

**Author:** Juan Corro  
**Affiliation:** Independent Researcher / Computational Social Science Group  
**Target Journal:** *Research & Politics* (SAGE)  
**Replication Repository:** [https://github.com/juancorro77/politics-without-policy-spain](https://github.com/juancorro77/politics-without-policy-spain)

---

## Abstract
Do weekly parliamentary control sessions function as a mechanism for executive accountability, or do they serve as a performative stage for partisan conflict? Using a hybrid computational approach that combines dictionary-based text parsing and Large Language Model (LLM) classification (Gemini API), this paper audits **2,275 oral Q&A segments** from the Spanish Congress of Deputies during the **XIV (2019-2023)** and **XV (2023-Present)** Legislatures. We operationalize two metrics: the *Agenda Shift Rate* (ASR) to measure the displacement of substantive policy topics by partisan politics, and the *Evasion Rate* (ER) to measure ministerial non-replies. The empirical findings reveal a systemic crowding out of policy: 83.8% of oral questions are registered directly on *politics*. For the remaining 16.2% of questions registered on *policy* (e.g., housing, energy, health), **over 69% (XIV) and 71% (XV)** of the actual debate turns are shifted to partisan confrontation. Furthermore, ministers evade technical inquiries by dedicating **69.8% (XIV) and 68.9% (XV)** of their response turns to partisan counterattacks. We discuss the implications of these findings for deliberative quality and legislative oversight in polarized democracies.

**Keywords:** Legislative Control, Parliamentary Questions, Agenda Shift, Evasion Rate, Computational Social Science, Spanish Congress.

---

## 1. Introduction
In representative democracies, parliamentary oversight is crucial for maintaining the balance of power. Weekly control sessions (such as the British *Question Time* or the Spanish *Sesiones de Control al Gobierno*) are theoretically designed to force the executive to justify its administrative decisions, explain policy designs, and account for public expenditure (Martin, 2011). In practice, however, these sessions are highly visible media events, leading to a tension between technical accountability (*policy*) and strategic partisan competition (*politics*).

This tension is particularly acute in Southern European democracies, such as Spain, characterized by high polarization, closed-list electoral systems, and strict party discipline (Field & Botti, 2021). Under these institutional constraints, members of parliament (MPs) and government ministers face strong incentives to treat oral questions not as informational tools, but as performative opportunities to score tactical victories (Maurer, 2008). While actual policy negotiations are relegated to invisible committee work, the plenary floor is transformed into a closed-circuit arena for partisan gesticulation.

This paper provides a large-scale, quantitative audit of this phenomenon in the Spanish Congress of Deputies (*Congreso de los Diputados*). We analyze all oral questions (*Preguntas Orales en Pleno*) across the **XIV (2019-2023)** and **XV (2023-Present)** Legislatures—a period marked by unprecedented political fragmentation and polarization. To scale this analysis, we deploy a hybrid computational pipeline that tokenizes and classifies **2,275 unique Q&A debates** containing tens of thousands of individual speech units. 

We operationalize two key metrics:
1.  **Agenda Shift Rate (ASR)**: The extent to which a debate formally registered on a *policy* topic is shifted by the participants into the realm of *politics* (e.g., corruption allegations, territorial legitimacy, or pacts).
2.  **Evasion Rate (ER)**: The proportion of the government minister's response turn spent on partisan rhetoric rather than answering the technical inquiry.

Our results demonstrate a systematic and rising "crowding out" of policy substance. Not only are the vast majority of questions registered directly on political battles, but even the small fraction of questions registered on critical citizen issues (housing, water scarcity, energy, transportation) are systematically hijacked on the floor. By evading substantive policy details (costs, trade-offs, and compromises), both the opposition and the government degrade the deliberative quality of the parliament, undermining its role as a watchdog of public administration.

---

## 2. Theoretical Framework and Hypotheses
The study of parliamentary questions divides their utility into two functions: the **informational function** (where MPs seek data on public services and local issues) and the **behavioral or symbolic function** (where MPs seek media coverage, party cohesion, and government embarrassment) (Wiberg, 1995).

### Politics vs. Policy in Parliamentary Scrutiny
Following Bara, Weale, and Bicquelet (2007), we distinguish between **policy** (technical, administrative, and fiscal aspects of public programs) and **politics** (partisan competition, ideological battles, and legitimacy struggles). In an ideal deliberative setting, parliamentary control should maintain a high proportion of policy-focused content, allowing for scrutiny of government efficacy (Habermas, 1996). However, in highly polarized environments, the opposition uses questions strategically to "set the agenda" with conflictual frames (Green-Pedersen, 2010). Under closed lists, MPs are selected by party elites, meaning their career incentives align with partisan warfare rather than policy specialization (Sánchez de Dios, 1999). Therefore, we expect a severe displacement of policy topics during live debates.
> **Hypothesis 1 (H1 - Agenda Shift)**: Live parliamentary debates initiated under a policy-manifest question will be dominated by politics-focused speech units, resulting in high Agenda Shift Rates (ASR).

### Ministerial Evasion and Blame Avoidance
Ministers face asymmetric information risks. Answering a technical policy question directly can expose administrative failures, budgetary overruns, or policy gaps. Consequently, executives utilize strategies of **blame avoidance** (Hood, 2011). In his seminal work on political interviews, Bull (2003) cataloged how politicians evade direct questions by reframing the topic, attacking the questioner, or deflecting blame to past administrations. Rasiah (2010) adapted this framework to *Question Time*, defining *agenda shift* as a covert evasion strategy where the minister ignores the MP’s question and establishes a counter-agenda. 
In the Spanish context, the Executive frequently deflects local policy questions by attacking the opposition's national alliances or pointing to autonomous regional governments.
> **Hypothesis 2 (H2 - Executive Evasion)**: Ministers responding to policy-focused questions will dedicate the majority of their speech turns to politics-focused units, exhibiting high Evasion Rates (ER).

### The Impact of Polarization and Fragmentation
Spain's party system has transitioned from a stable imperfect two-party system to a fragmented and highly polarized landscape (Orriols & Cordero, 2016). The XIV Legislature (2019-2023) featured Spain’s first coalition government since the transition to democracy, supported by a fragile legislative majority. The XV Legislature (2023-Present) has seen even higher polarization due to controversial legislative pacts (such as the amnesty law). Higher polarization raises the stakes of partisan survival, forcing both sides to prioritize ideological warfare over technical governance.
> **Hypothesis 3 (H3 - Temporal Escalation)**: The Agenda Shift Rate (ASR) will be significantly higher in the XV Legislature compared to the XIV Legislature.

---

## 3. Data and Methodology

### Data Collection
The dataset was gathered by scraping the Open Data portal of the Spanish Congress of Deputies (*Congreso de los Diputados*). Due to Liferay portal limitations which restrict bulk exports to 1,000 items, we developed a custom scraping pipeline:
1.  **Initiative Scraping**: A headless Playwright script crawled the advanced search portal, extracting all initiatives of type *"Pregunta oral en Pleno"* for the XIV and XV legislatures. This yielded a master list of **2,558 initiatives**.
2.  **Transcript Extraction**: For each initiative, we parsed the matching publication ID and extracted the raw text transcript of the debate segment from the official journal of sessions (*Diario de Sesiones*). After excluding withdrawn or postponed initiatives, we compiled a final dataset of **2,275 completed Q&A debates**.

### The Hybrid Classification Pipeline
To analyze the transcripts, we segment each Q&A debate into **Speech Units (UD)** (typically corresponding to individual sentences). Each UD is classified dicotómicamente as either `policy` or `politics`. 

To scale the coding of tens of thousands of sentences without compromising accuracy, we designed a hybrid classifier:
1.  **Rule-based Dictionary**: A localized Spanish dictionary containing highly specific regex patterns was applied. Words like *vivienda, precio, ferrocarril, sanidad, embalse* automatically routed the sentence to `policy`. Words like *amnistía, cgpj, dictadura, bulo, corrupción* routed it to `politics`.
2.  **LLM Refinement (Gemini API)**: Ambiguous sentences matching both or neither dictionary category were analyzed using `gemini-1.5-flash` with a strict zero-shot classification prompt. This hybrid approach combines the speed and determinism of dictionaries with the semantic understanding of generative models.

### Operationalization of Variables
For each Q&A debate $i$ formally registered under a `policy` topic:
*   **Agenda Shift Rate ($ASR_i$)**: The percentage of politics-focused units in the entire exchange:
    $$ASR_i = \frac{UD_{\text{politics}, i}}{UD_{\text{politics}, i} + UD_{\text{policy}, i}} \times 100$$
*   **Evasion Rate ($ER_i$)**: The percentage of politics-focused units specifically within the minister's response turns:
    $$ER_i = \frac{UD_{\text{politics, minister}, i}}{UD_{\text{politics, minister}, i} + UD_{\text{policy, minister}, i}} \times 100$$

---

## 4. Empirical Results

### Consolidated Analysis: XIV vs. XV Legislatures
The analysis of **2,275 Q&A debates** reveals that policy discussions are structurally marginalized on the floor of the Spanish Congress. First, the majority of questions are registered directly on political battles (1,083 in XIV; 965 in XV). Substantive policy questions comprise only **16.2%** of the total questions (254 in XIV; 142 in XV). 

For this small subset of policy-focused questions, the live debate on the floor systematically shifts away from the technical topic, as detailed in Table 1:

#### Table 1: Consolidated Scrutiny Metrics
| Metric | XIV Legislature (2019-2023) | XV Legislature (2023-Present) | Trend |
| :--- | :---: | :---: | :---: |
| Registered Policy Questions | 254 (19.0%) | 142 (12.8%) | - |
| Registered Politics Questions | 1,083 (81.0%) | 965 (87.2%) | - |
| **Mean Agenda Shift Rate (ASR)** | **69.0%** | **71.2%** | ▲ Increase (+2.2%) |
| **Mean Minister Evasion Rate (ER)** | **69.8%** | **68.9%** | ▼ Slight Decrease |

The data strongly support **Hypothesis 1 (H1)** and **Hypothesis 2 (H2)**:
*   **ASR is consistently above 69%**: Out of every ten sentences spoken in a debate meant to address a public service (housing, infrastructure, water), approximately seven are spent arguing over partisan corruption, territorial agreements, or political legitimacy.
*   **ER is close to 70%**: Ministers evade accountability by dedicating the vast majority of their time to counter-attacking the opposition or deflecting blame, leaving only 30% of their speech units for the substantive question.

Furthermore, the data support **Hypothesis 3 (H3)**: ASR rose from 69.0% to 71.2% in the XV Legislature, reflecting the growing polarization of the current legislative term.

---

### Group-Level Analysis
The strategic use of parliamentary questions varies significantly across parliamentary groups. Table 2 details the ASR and ER provoked by the primary political parties when they register questions on policy topics.

#### Table 2: Metrics by Initiating Parliamentary Group
| Parliamentary Group | Initiatives Evaluadas | Mean ASR (%) | Mean ER Provoked (%) |
| :--- | :---: | :---: | :---: |
| **GP (PP)** | 160 | 75.5% | 76.0% |
| **GVOX (Vox)** | 31 | 74.7% | 72.5% |
| **GSUMAR (Sumar)** | 4 | 72.9% | 75.7% |
| **GCs (Ciudadanos - XIV)** | 18 | 72.2% | 74.1% |
| **GR (ERC)** | 30 | 71.8% | 67.7% |
| **GJxCAT (Junts)** | 10 | 69.6% | 64.2% |
| **GPlu (Plural / BNG / Compromís)** | 22 | 60.6% | 60.9% |

The two main opposition groups—GP (Partido Popular) and GVOX—provoke the highest Agenda Shift and Evasion Rates. Their questions, even when registered under technical policy titles, are heavily loaded with partisan frames, which in turn triggers highly defensive, politics-focused responses from the ministers (with ER reaching 76.0% and 72.5% respectively). Conversely, minority regionalist groups (such as GPlu) exhibit lower ASR (60.6%) and ER (60.9%), indicating a more localized, policy-focused approach to executive control.

---

### Case Studies
To illustrate how these dynamics play out in live debates, we examine two transcripts classified by our pipeline.

#### Case A: Drought and Water Scarcity in Catalonia (Initiative 180/001290 - XIV)
*   **Manifest Topic**: Water infrastructure and support for farmers during the drought in Catalonia.
*   **Opposition Turn (Pilar Calvo Gómez - GPlu)**:
    > "...pagesos i ramaders, projects that are now dying... Once again we are paying a high price for Catalonia's lack of independence."
*   **Government Turn (Minister Teresa Ribera)**:
    > "...you must have forgotten who was heading the Government when they stopped building the hydraulic infrastructures..."
*   **Analysis**: While the question begins with agricultural drought, the MP quickly shifts the topic to Catalan independence (*politics*). The minister responds by deflecting blame to the previous administration's infrastructure record (*politics / blame avoidance*). **ASR = 76.5%**, **ER = 81.2%**.

#### Case B: Youth and Pension Sustainability (Initiative 180/001289 - XIV)
*   **Manifest Topic**: Viability of public pensions and intergenerational justice.
*   **Opposition Turn (Edmundo Bal - GCs)**:
    > "...and do not forget the electoral promises of Ferraz made from Moncloa, lest the President of the Government scold you for stealing his spotlight..."
*   **Analysis**: The MP utilizes the pension debate to mock the internal power dynamics and electoral strategies of the ruling party. The discussion of actuarial balance and youth employment is completely lost. **ASR = 83.2%**, **ER = 78.4%**.

---

## 5. Discussion: The Degradation of Good Governance
Why does this high rate of agenda shift matter? From a democratic theory perspective, parliamentary control is not merely a symbolic ritual; it is a mechanism for policy evaluation. When politics crowds out policy, the quality of governance is degraded in three fundamental ways:

1.  **Evading Costs and Feasibility**: There is no discussion on the fiscal feasibility or budgetary allocation of public programs.
2.  **Masking Design Alternatives**: By focusing on moral attacks or pacts, the chamber fails to deliberate on alternative ways to solve public problems (e.g., comparing tax incentives versus direct regulation in housing).
3.  **Ignoring Trade-offs**: Complex public policies always involve trade-offs (e.g., balancing environmental protection with agricultural water needs). Partisan confrontation reduces these trade-offs to binary, moralistic arguments, preventing pragmatic compromises.

To restore deliberative quality, structural reforms to the parliamentary rules (*Reglamento del Congreso*) should be considered. These could include shifting the weekly oral questions format toward a more committee-style system, where questions are answered by technical experts, or empowering the Speaker (*Presidente del Congreso*) to enforce strict thematic relevance rules, subtracting time from speakers who engage in blatant thematic deviation.

---

## References
*   Bara, J., Weale, A., & Bicquelet, A. (2007). Analyzing parliamentary debate: How and why? *Quality & Quantity*, 41, 577-597.
*   Bull, P. (2003). *The Microanalysis of Political Communication: Claptrap and Equivocation*. Psychology Press.
*   Bull, P., & Mayer, K. (1993). How Winston Churchill and Margaret Thatcher evade questions in political interviews. *Journal of Language and Social Psychology*, 12(4), 270-288.
*   Field, B. N., & Botti, A. (Eds.). (2021). *Politics and Society in Contemporary Spain*. Palgrave Macmillan.
*   Green-Pedersen, C. (2010). Who sets the agenda in parliamentary government? Defining the role of opposition and government in parliamentary questions. *European Journal of Political Research*, 49(3), 347-369.
*   Habermas, J. (1996). *Between Facts and Norms: Contributions to a Discourse Theory of Law and Democracy*. MIT Press.
*   Hood, C. (2011). *The Blame Game: Spin, Bureaucracy, and Self-Preservation in Government*. Princeton University Press.
*   Martin, S. (2011). Parliamentary Questions. In *The Oxford Handbook of Legislative Studies*. Oxford University Press.
*   Maurer, L. M. (2008). *El poder de control del Parlamento: Las preguntas al Gobierno en el Congreso de los Diputados*. Centro de Investigaciones Sociológicas (CIS).
*   Orriols, L., & Cordero, G. (2016). The Great Recession and the rise of new parties in Spain. *South European Society and Politics*, 21(4), 455-472.
*   Rasiah, R. (2010). A framework for the systematic coding of evasion in parliamentary question time. *Journal of Pragmatics*, 42(3), 664-680.
*   Wiberg, M. (1995). Parliamentary Questioning: Control, Information and Publicity. In *Dilemmas of Representative Democracy*. Dartmouth.
