import streamlit as st

# ============================================================
# LASRA — Ovine Drum Salting Simulator
# Practitioner learning resource
# ============================================================

st.set_page_config(
    page_title="LASRA | Ovine Drum Salting Simulator",
    page_icon="🐑",
    layout="wide",
)

# ---------- Styling ----------
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1250px;
    }

    .lasra-kicker {
        font-size: 0.82rem;
        letter-spacing: 0.12em;
        font-weight: 700;
        color: #64748b;
        margin-bottom: 0.25rem;
    }

    .scenario-box {
        background: #f8fafc;
        border: 1px solid #dbe4ee;
        border-left: 7px solid #244a68;
        border-radius: 10px;
        padding: 1.1rem 1.25rem;
        margin: 0.5rem 0 1.2rem 0;
    }

    .result-good {
        background: #f4f8f5;
        border: 1px solid #cad9cd;
        border-left: 8px solid #4d7358;
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1rem;
    }

    .result-watch {
        background: #fbf8ef;
        border: 1px solid #e5dcc1;
        border-left: 8px solid #a37a28;
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1rem;
    }

    .result-poor {
        background: #fbf3f2;
        border: 1px solid #e5cdca;
        border-left: 8px solid #9a5149;
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1rem;
    }

    .principle-box {
        background: #f7f9fb;
        border-radius: 10px;
        padding: 1rem 1.15rem;
        border: 1px solid #e2e8f0;
        height: 100%;
    }

    .small-note {
        color: #64748b;
        font-size: 0.9rem;
    }

    div.stButton > button {
        width: 100%;
        min-height: 3rem;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)


# ---------- Header ----------
st.markdown('<div class="lasra-kicker">LASRA | PRACTITIONER LEARNING</div>', unsafe_allow_html=True)
st.title("Ovine Drum Salting Simulator")
st.write(
    "Work through a realistic preservation run. There is no quiz score: "
    "make production decisions, see the likely consequences, and use the feedback to try again."
)

st.info(
    "Training model only — plant recipes, approved chemicals, safety controls and operating "
    "procedures always take precedence."
)


# ============================================================
# Scenario
# ============================================================

st.subheader("Your production brief")

scenario = st.selectbox(
    "Choose a starting situation",
    [
        "Routine fresh load",
        "Warm skins after a production delay",
        "Poorly prepared / fleshy skins",
        "A difficult load: warm, delayed and fleshy",
    ],
)

scenarios = {
    "Routine fresh load": {
        "delay": 0.5,
        "temp": 18,
        "flesh": "Well prepared",
        "contam": "Low",
        "description": (
            "The skins have arrived promptly and are in generally good condition. "
            "Your job is to preserve that value."
        ),
    },
    "Warm skins after a production delay": {
        "delay": 3.0,
        "temp": 28,
        "flesh": "Well prepared",
        "contam": "Moderate",
        "description": (
            "Production has been interrupted. The skins have remained warm and wet for several hours. "
            "They still look reasonably normal."
        ),
    },
    "Poorly prepared / fleshy skins": {
        "delay": 1.0,
        "temp": 20,
        "flesh": "Excess flesh present",
        "contam": "Moderate",
        "description": (
            "The load arrived reasonably promptly, but a noticeable proportion of skins retain excess flesh. "
            "This may interfere with preservative contact."
        ),
    },
    "A difficult load: warm, delayed and fleshy": {
        "delay": 4.0,
        "temp": 30,
        "flesh": "Excess flesh present",
        "contam": "High",
        "description": (
            "This is a poor starting position: a long warm delay, significant contamination and excess flesh. "
            "Good drum salting cannot reverse damage that has already occurred."
        ),
    },
}

s = scenarios[scenario]

st.markdown(
    f"""
    <div class="scenario-box">
        <strong>{scenario}</strong><br><br>
        {s["description"]}<br><br>
        <strong>Time since removal:</strong> {s["delay"]} h &nbsp; | &nbsp;
        <strong>Skin temperature:</strong> {s["temp"]} °C &nbsp; | &nbsp;
        <strong>Preparation:</strong> {s["flesh"]} &nbsp; | &nbsp;
        <strong>Contamination:</strong> {s["contam"]}
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Decisions
# ============================================================

st.subheader("Make your production decisions")

c1, c2 = st.columns(2)

with c1:
    st.markdown("#### 1. Before the drum")

    receipt_action = st.radio(
        "What will you do with the load on receipt?",
        [
            "Proceed directly to preservation",
            "Inspect and improve preparation before preservation",
            "Cool / hold while the production issue is addressed",
        ],
        index=1,
    )

    excess_flesh_action = st.selectbox(
        "How will you deal with excess flesh?",
        [
            "Remove obstructive excess flesh before salting",
            "Leave it — the drum and salt should compensate",
        ],
    )

    salt_level = st.select_slider(
        "Salt application relative to the approved plant recipe",
        options=["50%", "75%", "100%", "125%"],
        value="100%",
        help="This simulator uses the approved plant recipe as the reference point; it does not prescribe a universal salt recipe.",
    )

    biocide = st.selectbox(
        "Biocide / preservative treatment",
        [
            "Approved plant dose",
            "Reduced dose",
            "None",
        ],
    )

with c2:
    st.markdown("#### 2. Drum and drainage")

    mix_quality = st.selectbox(
        "Salt / preservative preparation",
        [
            "Accurately measured and evenly mixed",
            "Roughly measured / unevenly mixed",
        ],
    )

    drum_time = st.slider(
        "Drum time (minutes)",
        min_value=10,
        max_value=90,
        value=50,
        step=5,
    )

    drum_speed = st.slider(
        "Drum speed (rpm)",
        min_value=1.0,
        max_value=8.0,
        value=3.0,
        step=0.5,
    )

    drainage = st.slider(
        "Drainage time before packing (hours)",
        min_value=0,
        max_value=72,
        value=36,
        step=6,
    )


# ============================================================
# Simulation engine
# ============================================================

def add_issue(issues, severity, title, explanation, consequence):
    issues.append({
        "severity": severity,
        "title": title,
        "explanation": explanation,
        "consequence": consequence,
    })


if st.button("Run the preservation simulation", type="primary"):

    issues = []
    strengths = []

    # ---- Starting condition: time / temperature / moisture ----
    biological_risk = 0

    if s["delay"] >= 4 and s["temp"] >= 25:
        biological_risk = 3
        add_issue(
            issues,
            3,
            "High pre-preservation deterioration risk",
            "Warm, wet skins have remained unpreserved for a prolonged period. "
            "Temperature, moisture and time act together to favour bacterial activity.",
            "Some deterioration may already have occurred even if the skins still look acceptable. "
            "Later signs can include wool slip, grain weakening or loss of raw-material value.",
        )
    elif s["delay"] >= 2 and s["temp"] >= 24:
        biological_risk = 2
        add_issue(
            issues,
            2,
            "The clock has been running",
            "The warm delay has increased the opportunity for bacteria to multiply before preservation.",
            "Prompt and effective preservation is now especially important, but salting cannot reverse damage already done.",
        )
    else:
        strengths.append(
            "The load reached preservation reasonably promptly, limiting the time available for early bacterial deterioration."
        )

    # Receipt decision
    if receipt_action == "Cool / hold while the production issue is addressed":
        if biological_risk >= 2:
            strengths.append(
                "Cooling helps slow further bacterial activity while the production problem is addressed."
            )
        else:
            add_issue(
                issues,
                1,
                "Unnecessary delay",
                "Cooling can slow bacterial activity, but this load was already suitable for prompt preservation.",
                "Holding the load adds time without an obvious preservation benefit unless there is another plant reason to do so.",
            )

    if receipt_action == "Inspect and improve preparation before preservation":
        strengths.append(
            "Inspection before salting gives you a chance to identify physical damage, contamination and barriers to good flesh-side contact."
        )

    # Excess flesh
    fleshy = s["flesh"] == "Excess flesh present"

    if fleshy and excess_flesh_action.startswith("Leave"):
        add_issue(
            issues,
            3,
            "Poor preservative contact",
            "Excess flesh can shield areas of the skin from effective contact with the salt and preservative mixture.",
            "The batch may appear salted overall while local areas remain poorly preserved.",
        )
    elif fleshy:
        strengths.append(
            "Removing obstructive excess flesh improves the chance of even flesh-side contact with the preservative system."
        )
    else:
        strengths.append(
            "Skin preparation is already suitable for effective flesh-side preservative contact."
        )

    # Salt
    salt_pct = int(salt_level.replace("%", ""))

    if salt_pct == 50:
        add_issue(
            issues,
            3,
            "Salt application well below the plant recipe",
            "Salt protects by drawing water from the skin and forming concentrated brine, reducing water readily available to microorganisms.",
            "Insufficient salt can leave preservation unreliable, particularly where distribution is uneven.",
        )
    elif salt_pct == 75:
        add_issue(
            issues,
            2,
            "Salt application below the plant recipe",
            "Reducing salt changes the preservation conditions on which the approved process is based.",
            "The safety margin for reliable preservation is reduced.",
        )
    elif salt_pct == 125:
        add_issue(
            issues,
            1,
            "More is not automatically better",
            "The approved plant recipe should be the reference point. Adding extra salt is not a substitute for good preparation, mixing, coverage and drainage.",
            "Extra chemical use may add cost and waste without correcting the real cause of poor preservation.",
        )
    else:
        strengths.append(
            "Salt application matches the approved plant recipe."
        )

    # Biocide
    if biocide == "None":
        add_issue(
            issues,
            2,
            "Additional microbial control has been removed",
            "Salt and biocide perform different but complementary roles. Salt reduces available water; an approved biocide suppresses microbial activity.",
            "The process is relying on salt alone rather than the approved combined preservation system.",
        )
    elif biocide == "Reduced dose":
        add_issue(
            issues,
            1,
            "Biocide dose below the approved recipe",
            "Changing preservative concentration can reduce microbial control.",
            "Follow the approved plant formulation rather than assuming a lower dose will perform equivalently.",
        )
    else:
        strengths.append(
            "The approved biocide dose provides additional microbial control alongside salting."
        )

    # Mixing
    if mix_quality.startswith("Roughly"):
        add_issue(
            issues,
            3,
            "Uneven preservative preparation",
            "Accurate measurement and even mixing matter because the drum can only distribute the mixture that has been prepared.",
            "Some skins or areas may receive too little preservative even if the average batch addition appears correct.",
        )
    else:
        strengths.append(
            "Accurate measurement and mixing support consistent preservative distribution."
        )

    # Drum time
    if drum_time < 30:
        add_issue(
            issues,
            3,
            "Drum time is probably too short",
            "The LASRA industry example uses roughly 45–60 minutes to achieve good flesh-side coverage.",
            "A short run increases the risk of incomplete or uneven distribution.",
        )
    elif drum_time < 45:
        add_issue(
            issues,
            1,
            "Shorter than the typical example",
            "This may be adequate under a validated plant process, but it is below the 45–60 minute example used in the learning material.",
            "Check whether even coverage has actually been achieved rather than relying on time alone.",
        )
    elif drum_time <= 60:
        strengths.append(
            "Drum time sits within the 45–60 minute example used in the LASRA learning material."
        )
    else:
        add_issue(
            issues,
            1,
            "Long drum time",
            "Longer tumbling is not automatically better once good distribution has been achieved.",
            "Unnecessary mechanical action adds processing time and may increase the risk of wool or raw-material damage.",
        )

    # Drum speed
    if drum_speed < 2:
        add_issue(
            issues,
            2,
            "Mechanical action may be too low",
            "The drum needs enough movement to distribute the salt and preservative mixture across the load.",
            "Too little movement may contribute to uneven coverage.",
        )
    elif drum_speed <= 4:
        strengths.append(
            "Drum speed is within the low-speed 2–4 rpm example used to promote distribution without excessive mechanical action."
        )
    elif drum_speed <= 5:
        add_issue(
            issues,
            1,
            "Drum speed is above the typical low-speed range",
            "More movement does not necessarily improve preservation once distribution is adequate.",
            "Watch for unnecessary mechanical action and follow the validated plant procedure.",
        )
    else:
        add_issue(
            issues,
            2,
            "Excessive mechanical action",
            "The learning material uses low-speed operation, around 2–4 rpm, to distribute preservative without excessive movement.",
            "High speed may increase the risk of wool felting or physical damage.",
        )

    # Drainage
    if drainage < 12:
        add_issue(
            issues,
            3,
            "Packed too soon after the drum",
            "Preservation does not finish when the drum stops. Brine needs time to drain from the skins.",
            "Packing too early retains unnecessary moisture and brine and can compromise handling and storage.",
        )
    elif drainage < 24:
        add_issue(
            issues,
            2,
            "Drainage period is short",
            "The LASRA industry example uses about 24–48 hours of drainage after drum salting.",
            "Allow enough time for brine to drain before packing, according to the plant procedure.",
        )
    elif drainage <= 48:
        strengths.append(
            "Drainage time is within the 24–48 hour example used in the LASRA learning material."
        )
    else:
        strengths.append(
            "The skins have been given an extended drainage period before packing."
        )

    # ========================================================
    # Overall outcome — consequence based, not a quiz score
    # ========================================================

    severity_total = sum(i["severity"] for i in issues)
    critical_count = sum(1 for i in issues if i["severity"] >= 3)

    if critical_count >= 2 or severity_total >= 10:
        outcome = "HIGH RISK OF POOR OR UNEVEN PRESERVATION"
        css_class = "result-poor"
        summary = (
            "Several decisions have combined to weaken the preservation chain. "
            "The important point is not a numerical score: identify where control was lost, "
            "change those decisions and run the batch again."
        )
    elif critical_count >= 1 or severity_total >= 5:
        outcome = "PRESERVATION AT RISK"
        css_class = "result-watch"
        summary = (
            "Much of the process is reasonable, but one or more decisions could compromise preservation. "
            "Read the technical feedback below and decide what you would change."
        )
    else:
        outcome = "PRESERVATION CHAIN UNDER GOOD CONTROL"
        css_class = "result-good"
        summary = (
            "Your decisions support prompt, even preservation and appropriate drainage. "
            "Remember that a good process protects the condition of the raw material; it cannot repair damage that happened earlier."
        )

    st.markdown("---")
    st.subheader("Likely production outcome")

    st.markdown(
        f"""
        <div class="{css_class}">
            <strong>{outcome}</strong><br><br>
            {summary}
        </div>
        """,
        unsafe_allow_html=True,
    )

    r1, r2, r3 = st.columns(3)

    with r1:
        st.metric("Technical issues to review", len(issues))

    with r2:
        st.metric("Good decisions identified", len(strengths))

    with r3:
        if critical_count:
            st.metric("Major control failures", critical_count)
        else:
            st.metric("Major control failures", 0)

    # Strengths
    if strengths:
        st.markdown("### What you controlled well")
        for strength in strengths:
            st.success(strength)

    # Technical feedback
    if issues:
        st.markdown("### What needs another look")

        severity_names = {
            1: "Worth reviewing",
            2: "Important",
            3: "Major control issue",
        }

        for n, issue in enumerate(
            sorted(issues, key=lambda x: x["severity"], reverse=True), start=1
        ):
            with st.expander(
                f"{n}. {severity_names[issue['severity']]} — {issue['title']}",
                expanded=(n <= 2),
            ):
                st.markdown(f"**Why it matters**  \n{issue['explanation']}")
                st.markdown(f"**Likely consequence**  \n{issue['consequence']}")

    # Reflection rather than interrogation
    st.markdown("### Before you run it again")
    st.write(
        "Look at the outcome and choose the **one or two decisions** that had the greatest effect. "
        "Change them above and rerun the same load. The aim is to understand the process, not to achieve a quiz score."
    )

    # Practitioner transfer
    with st.expander("Take it back to the plant"):
        st.write(
            "Think of a real load you have handled. Where was the greatest preservation risk: "
            "time before salting, temperature, skin preparation, chemical preparation, distribution in the drum, "
            "or drainage afterwards? What evidence would tell you the process was under control?"
        )


# ============================================================
# Learning principles
# ============================================================

st.markdown("---")
st.subheader("The preservation chain")

p1, p2, p3 = st.columns(3)

with p1:
    st.markdown(
        """
        <div class="principle-box">
        <strong>1. Control deterioration early</strong><br><br>
        Fresh skins are warm, wet and biologically active. Temperature, moisture and time work together.
        </div>
        """,
        unsafe_allow_html=True,
    )

with p2:
    st.markdown(
        """
        <div class="principle-box">
        <strong>2. Make preservation work everywhere</strong><br><br>
        Accurate preparation, flesh-side contact, correct chemical addition and controlled drum movement all matter.
        </div>
        """,
        unsafe_allow_html=True,
    )

with p3:
    st.markdown(
        """
        <div class="principle-box">
        <strong>3. Protect the result</strong><br><br>
        Preservation continues after the drum. Drainage, packing, storage and transport remain part of the chain.
        </div>
        """,
        unsafe_allow_html=True,
    )

st.caption(
    "LASRA | Ovine Drum Salting — practitioner learning simulator. "
    "Typical times and speeds shown are examples from the LASRA learning material, not universal plant specifications."
)
