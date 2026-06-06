#!/usr/bin/env python3
"""Build the STUDY corner for aidanjude.vercel.app.

A study corner = a small, growing set of self-contained "field notes": ~3-min
argument-driven primers on non-fiction subjects adjacent to Aidan's reading but
not yet crossed. Each guide is original prose (hybrid: write it ourselves, link
out only when a source says it better), rendered to match the site's design.

Output (into the writing-topology / a-phylogeny-of-writing repo):
    study.html                 -- the index of fields
    study/<slug>.html          -- one page per guide

Add a new guide by appending a dict to GUIDES, then re-run:
    python3 scripts/personal_corpus/build_study_guides.py [SITE_DIR]
SITE_DIR defaults to ~/Desktop/writing-topology.

Authoring contract (see .claude/skills/study-guide/SKILL.md):
  - register: literary/essayistic, the site's voice -- NOT the B&M sales voice
  - shape: provocation -> the argument -> where it's contested -> go deeper -> on your shelf
  - every guide is an ARGUMENT, not a survey
  - balance disciplines ~20% philosophy/philology, rest econ/history/anthro/physics
"""
import os, sys, html

# ---------------------------------------------------------------------------
# CONTENT  --  one dict per field. Prose is HTML-ready (inline <i>/<b> ok).
# ---------------------------------------------------------------------------
GUIDES = [
    {
        "n": 1,
        "archived": True,
        "slug": "the-price-of-knowing",
        "discipline": "Economics",
        "color": "#9c7a3c",
        "title": "The price of knowing",
        "dek": "Nobody knows how to make a pencil — and that is exactly why the price system is the smartest thing in the room.",
        "hook": "Why a price knows more than any planner ever could.",
        "read": 3,
        "provocation": (
            "No single person on earth knows how to make a pencil. The cedar is milled in Oregon, "
            "the graphite mined in Sri Lanka, the lacquer, the brass, the rubber each pass through "
            "thousands of hands that never meet and never plan together. Yet pencils sit in every "
            "drawer, cheap, abundant, unremarkable. How does a thing nobody can build get built ten "
            "million times a day? Friedrich Hayek's answer, in twelve pages from 1945, is one of the "
            "great arguments of the century."
        ),
        "argument": [
            "Hayek begins by re-stating the problem everyone thought was solved. The economic "
            "question, he says, is <i>not</i> how to allocate a given stock of resources to known "
            "ends. That version is just arithmetic — hand a computer the data and it optimizes. The "
            "real problem is that <b>the data is never given to anyone</b>. Knowledge of the world "
            "exists only in scattered, perishable scraps: the factory manager who knows one machine "
            "sits idle, the trader who knows a shipment is late, the farmer who can smell the "
            "weather turning. Much of it is never written down and some of it can't even be spoken. "
            "No central authority can gather it, because gathering it would destroy it.",
            "The price system is how a society uses knowledge no one possesses in full. A price is a "
            "signal that compresses millions of these private scraps into a single number. When tin "
            "grows scarce, its price rises — and everyone who touches tin economizes, substitutes, "
            "hunts for alternatives, <i>without knowing why</i>. They don't need to know there was a "
            "mine collapse in Bolivia or a new use found in electronics. They need to know one thing: "
            "tin costs more today. As Hayek puts it, the marvel is that in such a case “without "
            "an order being issued, without more than perhaps a handful of people knowing the cause, "
            "tens of thousands of people… are made to use the material or its products more "
            "sparingly.”",
            "So the market is not really a marketplace at all. It is a <b>telecommunication "
            "system</b> — a vast machine for moving information, and it works <i>because</i> nobody "
            "has to understand the whole. The deepest line in the essay is the quietest: this order "
            "is “the result of human action but not of human design.” It is an intelligence "
            "that no mind built and no mind contains.",
        ],
        "tension": [
            "It is easy — and popular — to read this as a knockout argument for leaving markets "
            "alone, and the political right has mined it for exactly that. But the essay claims both "
            "less and more than the slogan. <b>Less:</b> a price knows scarcity, not worth. A clean "
            "river, an hour of a child's attention, a species going quiet — things with no price are "
            "simply invisible to the system. That blindness is not a bug you can patch; it is the "
            "same trait that makes the system efficient. It sees only what is priced.",
            "<b>More:</b> the argument cuts just as hard at the modern techno-optimist who believes "
            "that with enough sensors and compute we could finally plan an economy after all. "
            "Hayek's point is that the crucial knowledge isn't <i>data</i> — it's tacit, local, and "
            "half-unspeakable, so no quantity of measurement captures it. The live question he "
            "leaves you is not “markets or planning?” but the sharper one: <i>where does "
            "the price signal go blind — externalities, public goods, the priceless — and what do "
            "we reach for when it does?</i>",
        ],
        "deeper": [
            {"label": "The Use of Knowledge in Society — F. A. Hayek (1945)",
             "note": "The essay itself, about twelve pages — shorter and clearer than anything written about it."},
            {"label": "I, Pencil — Leonard E. Read (1958)",
             "note": "The same idea told as a parable, in the voice of a pencil."},
        ],
        "shelf": (
            "You've read Rand's romance of the producer — the heroic individual who builds the world "
            "with his own will. Hayek is the other half of that picture, and the colder half: the "
            "genius isn't in any individual at all, it's in the system no individual runs. Set beside "
            "<i>Atlas Shrugged</i>, this is the argument John Galt should have made — not that the "
            "great man matters most, but that no one is great enough to hold the whole."
        ),
    },
    {
        "n": 2,
        "archived": True,
        "slug": "the-frontier-and-its-ghost",
        "discipline": "History",
        "color": "#b89a6a",
        "title": "The frontier and its ghost",
        "dek": "In 1893 a young historian told America that the thing that made it had just quietly ended — and asked what a nation built on an edge does once the edge is gone.",
        "hook": "The historical argument hiding under every Western you've read.",
        "read": 4,
        "provocation": (
            "In 1893, in a half-empty room at the Chicago World's Fair, a 31-year-old historian read "
            "a paper almost no one noticed. The census of 1890 had just announced something quietly "
            "enormous: for the first time there was no longer a frontier line — no unbroken edge of "
            "“free land” marching west. Frederick Jackson Turner stood up and said, in "
            "effect: <i>that line was America. And it just closed.</i>"
        ),
        "argument": [
            "Turner's thesis was a frontal challenge to how Americans explained themselves. Democracy "
            "and the American character, he argued, were not carried over on the Mayflower from "
            "Europe. They were <b>made</b>, again and again, on the frontier. At the ragged edge of "
            "settlement, European man was stripped down — the wilderness “takes him from the "
            "railroad car and puts him in the birch canoe… it puts him in the log cabin.” "
            "Inherited rank, deference, the thick institutions of the old world all thinned out at "
            "the margin, where a person faced raw land with their own hands.",
            "What grew back, in Turner's telling, was something new: individualism, restlessness, a "
            "practical bent, a suspicion of authority, an appetite for the next horizon. And crucially "
            "it kept renewing. Every generation could light out for the territory, and that perpetual "
            "rebirth was both the engine of American exceptionalism and the <b>safety valve</b> of "
            "its democracy — discontent could always move west instead of detonating in place. Free "
            "land was a pressure-release valve no other nation had.",
            "Then the hinge that gives the essay its haunted power. The valve is closed. “The "
            "frontier has gone,” Turner writes, “and with its going has closed the first "
            "period of American history.” He doesn't answer the question that hangs off the end "
            "of that sentence — <i>what happens to a country built on an edge, once there is no more "
            "edge?</i> — and the next century has been, in a sense, the answer."
        ],
        "tension": [
            "For fifty years the thesis was close to gospel; for the last fifty it has been the most "
            "productively <b>attacked</b> idea in American history, and you have to hold both facts at "
            "once. The “free land” was neither free nor empty — it was someone's home, and "
            "the taking of it is the part the romance leaves out. Turner's frontier has no Native "
            "people as people, no Mexicans, no Chinese rail workers, no women; it is white men and an "
            "“empty” map, which is conquest told as destiny.",
            "Patricia Limerick and the New Western History rewrote the West not as a <i>process</i> "
            "(the settling) but as a <i>place</i> — a grinding meeting of peoples, a story of "
            "conquest and property and aftermath that never “closed” at all. So read Turner "
            "now and you read two things in one breath: a genuinely powerful claim about how "
            "environment forges character, and a near-perfect specimen of how a nation tells itself a "
            "flattering story about its own violence. Both are true at once. That double vision — "
            "myth and its undoing on the same page — is the whole reason to read him."
        ],
        "deeper": [
            {"label": "The Significance of the Frontier in American History — Frederick Jackson Turner (1893)",
             "note": "The original address. Read the first dozen paragraphs and the last two."},
            {"label": "The Legacy of Conquest — Patricia Nelson Limerick (1987)",
             "note": "The great rebuttal — the West as a place and a conquest, not a process."},
        ],
        "shelf": (
            "This is the bedrock under your entire Western shelf — McCarthy, and your own "
            "<i>something-western</i>. <i>Blood Meridian</i> is what Turner's romance looks like with "
            "the myth burned off: the frontier not as democratic rebirth but as the ground where the "
            "violence at the root of the conquest finally shows its face. Read the 1893 thesis and "
            "the 1985 novel together and you have an argument and its nightmare, a century apart, "
            "describing the same country."
        ),
    },
    {
        "n": 3,
        "archived": True,
        "slug": "the-original-affluent-society",
        "discipline": "Anthropology",
        "color": "#7a9c6b",
        "title": "The original affluent society",
        "dek": "Everything you were taught about the desperate, starving caveman is, an anthropologist argued in 1966, almost exactly backwards.",
        "hook": "Affluence is a ratio, not a sum — and the Stone Age may have understood that better than we do.",
        "read": 3,
        "provocation": (
            "We tell one story about prehistory so often we forget it's a story: the caveman's life "
            "was nasty, brutish and short — every waking hour a war against starvation, a desperate "
            "scrabble for calories, until farming and then industry finally set us free. In 1966 the "
            "anthropologist Marshall Sahlins looked hard at the field data from people still living "
            "that way and said: nearly every word of that is wrong."
        ),
        "argument": [
            "Sahlins called hunter-gatherers “the original affluent society,” and the phrase "
            "was a deliberate provocation. Affluence, he pointed out, can be reached by two roads: "
            "you can <b>produce much</b>, or you can <b>want little</b>. Modern economies took the "
            "first road — infinite wants chasing scarce means, a treadmill built into the design. "
            "Foragers took the second, and arrived.",
            "The studies were startling. Richard Lee's work with the Ju/'hoansi (the !Kung) of the "
            "Kalahari — some of the harshest land on earth — found people feeding themselves on "
            "roughly three to five hours of food-getting a day. The rest was leisure: sleep, talk, "
            "visiting, ritual, more sleep. They were not failing to accumulate wealth; they "
            "<i>declined</i> to. Why build granaries when the bush is the granary? Mobility punishes "
            "property — a thing you must carry on your back is a burden — so they kept few "
            "possessions, and a person's standing was measured by what they gave away, not what they "
            "held.",
            "The conclusion is the part that should keep you up. Their wants were finite and easily "
            "met, so by their own reckoning they lived in plenty. <b>Scarcity, Sahlins argued, is not "
            "the human condition.</b> It is the founding axiom of <i>our</i> economy — “the "
            "judgment passed by our market system” — and we have quietly projected it backward "
            "onto the entire species, mistaking our own arrangement for nature itself."
        ],
        "tension": [
            "The thesis was a bomb, and it took return fire. Later work complicated the arithmetic: "
            "the rosy figure counted only food-getting and left out the hours of processing, "
            "tool-making, childcare, and walking; some forager diets were thinner and some lives "
            "shorter than the bright version implied; the !Kung of the 1960s were not a clean window "
            "onto the Pleistocene but a modern people in a specific, pressured corner of history. The "
            "<i>strong</i> claim — that they truly worked less — is genuinely contested.",
            "But the <i>deep</i> claim survived the fight, and it's the one worth carrying: "
            "<b>affluence is a ratio, not a sum.</b> It is the relationship between what you want and "
            "what you have — and a civilization can manufacture dissatisfaction as deliberately as it "
            "manufactures abundance. Sahlins's real target was never the Stone Age. It was the "
            "assumption, so total we mistake it for gravity, that <i>more</i> is the only road to "
            "<i>enough</i>."
        ],
        "deeper": [
            {"label": "Stone Age Economics — Marshall Sahlins (1972)",
             "note": "The opening essay, “The Original Affluent Society,” carries the whole argument."},
            {"label": "The Darker Side of the Original Affluent Society — David Kaplan (2000)",
             "note": "The rigorous critique — which parts of the thesis hold, and which don't."},
        ],
        "shelf": (
            "Your to-read shelf leans hard into the <i>examined</i> life — the Stoics, Zen, "
            "<i>Siddhartha</i>, the old question of how little a person actually needs. Sahlins is the "
            "anthropology underneath that question. Where the Stoics tell <i>you</i>, one person, to "
            "want less, he shows you an entire society that built want-less into its structure — and "
            "then asks, pointedly, why ours built the exact opposite and called it progress."
        ),
    },
    {
        "n": 4,
        "archived": True,
        "slug": "gravity-is-not-a-force",
        "discipline": "Physics",
        "color": "#6b8f9c",
        "title": "Gravity is not a force",
        "dek": "Nothing is pulling you into your chair. The chair is shoving you up — and that shove is the only force in the whole story.",
        "hook": "Einstein's happiest thought: weight is the feeling of being stopped from falling.",
        "read": 4,
        "provocation": (
            "Right now you can feel gravity pulling you down into your seat. Einstein's strangest and "
            "best idea is that nothing is pulling you at all. There is no force of gravity. The chair "
            "is pushing you <i>up</i> — and that shove is the only real force in the story. Everything "
            "else is the shape of space."
        ),
        "argument": [
            "Start where Einstein started, with what he called the happiest thought of his life: a "
            "person in free fall does not feel their own weight. Drop a ball beside you as you fall "
            "and it hangs there, weightless, exactly as it would in deep space. So gravity can be "
            "made to <i>vanish</i> simply by letting go. This is the <b>equivalence principle</b>: "
            "standing in a gravitational field feels identical to accelerating, and falling freely "
            "feels identical to floating where there is no gravity at all. If a force can be "
            "switched off just by releasing your grip, Einstein reasoned, maybe it was never a force "
            "to begin with.",
            "Here is the replacement picture. Mass and energy bend the geometry of <b>spacetime</b> — "
            "the four-dimensional fabric of where-and-when. A planet does not reach out and tug the "
            "Moon with an invisible rope; that was Newton's picture, and it always bothered people "
            "(action at a distance, across empty space, instantaneously?). Instead the planet "
            "<i>curves the spacetime around it</i>, and the Moon simply travels the straightest "
            "possible path through that curved geometry. We call the path an orbit, but to the Moon "
            "it is a straight line — it is coasting, force-free, through a valley in the shape of "
            "space. John Wheeler compressed the whole theory into one sentence: “Spacetime tells "
            "matter how to move; matter tells spacetime how to curve.”",
            "And the chair? You feel pinned to it because the chair is constantly <i>stopping</i> you "
            "from following your natural, straight, force-free path — which is to fall. The ground "
            "shoves you off course every second. <b>The sensation of weight is the sensation of being "
            "prevented from falling.</b> This isn't a teaching metaphor; it makes hard predictions "
            "Newton can't. Starlight bends as it grazes the Sun (measured in 1919). Time runs "
            "measurably slower deep in a gravity well (your phone's GPS corrects for it every "
            "second, or it would drift miles off). And where the curvature runs away with itself, you "
            "get a black hole — a place where the geometry folds so steeply that <i>down</i> points "
            "only inward."
        ],
        "tension": [
            "General relativity is among the most ruthlessly tested theories in all of science; for a "
            "century it has not put a foot wrong, from Mercury's orbit to the gravitational waves "
            "detected in 2015. The unfinished business lies elsewhere: it does not get along with the "
            "other great theory of the age, <b>quantum mechanics</b>. Relativity describes spacetime "
            "as smooth and continuous; quantum theory describes a world that is grainy, probabilistic, "
            "jittering at the smallest scales.",
            "At the center of a black hole, and in the first instant of the universe, both theories "
            "apply at once — and they flatly contradict each other, the smooth geometry dissolving "
            "into infinities no one can read. So Einstein's curved spacetime is almost certainly "
            "<i>not</i> the last word, but a breathtaking approximation of something deeper we can't "
            "yet see: a quantum theory of gravity. The shape of space, it seems, may itself be made "
            "of something — and we don't know what."
        ],
        "deeper": [
            {"label": "Relativity: The Special and the General Theory — Albert Einstein (1916)",
             "note": "His own popular account. Surprisingly readable — he wanted ordinary readers to follow it."},
            {"label": "Seven Brief Lessons on Physics — Carlo Rovelli (2014)",
             "note": "The most elegant short modern telling of curved spacetime — the first lesson is on exactly this."},
        ],
        "shelf": (
            "You read Hawking and Thorne and Gleick's <i>Chaos</i> — you go to science for the same "
            "thing you go to McCarthy for: the confrontation with something vast and indifferent. "
            "This is the cleanest version of it. Newton handed you a clockwork you could feel "
            "mastered by; Einstein hands you a universe whose very stage is bent by whatever stands "
            "on it, where time itself runs at a local rate. It may be the most literary idea in all "
            "of physics: the shape of the world depends on what is in it."
        ),
    },
    {
        "n": 5,
        "archived": True,
        "slug": "how-good-got-two-meanings",
        "discipline": "Philosophy · Philology",
        "color": "#8c6b9c",
        "title": "How “good” got two meanings",
        "dek": "Nietzsche the philologist noticed that one small word means two opposite things — and that the switch between them is the hidden hinge of Western morality.",
        "hook": "Where did our values come from, and whom did they serve? The question you can't stop asking.",
        "read": 4,
        "provocation": (
            "Take the word “good.” You think you know what it means. Nietzsche — who was a "
            "<b>philologist</b>, a scholar of ancient words, years before he was a philosopher — "
            "noticed that it has meant two opposite things, and that the quiet switch between them is "
            "the hidden hinge of the entire Western moral world."
        ),
        "argument": [
            "In <i>On the Genealogy of Morality</i> (1887) Nietzsche does something genuinely new. "
            "Instead of asking <i>what is good?</i> — the question every philosopher before him "
            "asked — he asks <i>where did our idea of “good” come from? what is its "
            "history?</i> This is the <b>genealogical method</b>, and he runs it like the philologist "
            "he was, tracking the descent of words to excavate the values buried in them. He uncovers "
            "two rival systems.",
            "The first he calls <b>master morality</b>. To the strong, the noble, the fortunate, "
            "“good” simply meant <i>themselves</i> — powerful, beautiful, overflowing, "
            "alive. “Good” was a self-description of strength, and “bad” was a "
            "mere afterthought: the low, the common, the weak, whatever the noble was not. Notice the "
            "order. Good comes first and is positive; bad is only its shadow.",
            "Then the reversal — what he names the <b>slave revolt in morality</b>. The weak, the "
            "dominated, those who could not discharge their will in action, performed a revolt not "
            "with weapons but with values. Out of <i>ressentiment</i> — he keeps the French for it: a "
            "brooding, impotent, endlessly creative resentment that cannot act and so turns inward — "
            "they invented a new scale. Now the powerful are no longer “good” but "
            "<b>evil</b>, and the new “good” is everything the powerless happen to be: meek, "
            "humble, patient, restrained. This morality begins with a <i>No</i> — it names the enemy "
            "first (evil = the strong) and defines itself only by negation. Its triumph, Nietzsche "
            "argues, is the moral water we all now swim in. Master morality says <i>I am good, "
            "therefore you are lesser</i>. Slave morality says <i>you are evil, therefore I am "
            "good</i>. Same word — opposite engines."
        ],
        "tension": [
            "This is dangerous reading, and it is meant to be. Taken as a program it curdles fast: the "
            "Nazis quarried Nietzsche (with help from his sister's forgeries) for exactly the "
            "“blond beast” master-race reading he would have despised, and any clever "
            "sophomore can mistake the <i>Genealogy</i> for a permission slip to be cruel. But that "
            "misses the move entirely. Nietzsche is not handing you a team to cheer for.",
            "He is doing the <i>history of morals</i> to break a spell — the spell that our values are "
            "eternal, God-given, simply and obviously true. His real claim is unsettling in a far "
            "deeper way: that morality has a <b>lineage</b>, that it was made by particular people for "
            "particular reasons of power, and that “good” and “evil” are not "
            "facts of the universe but the residue of an ancient fight the losers won. You need not "
            "accept his verdict. But once you have asked <i>where did this value come from, and whom "
            "did it serve?</i> — the genealogical question — you will not be able to stop asking it of "
            "everything. That is the gift, and the wound."
        ],
        "deeper": [
            {"label": "On the Genealogy of Morality — Friedrich Nietzsche (1887)",
             "note": "The First Essay — on “good and evil” versus “good and bad” — is the one to read first, about 25 pages."},
            {"label": "Nietzsche: Philosopher, Psychologist, Antichrist — Walter Kaufmann (1950)",
             "note": "The classic, non-cartoon guide to what the genealogical method actually claims — and what it doesn't."},
        ],
        "shelf": (
            "Nietzsche is already your philosophy marquee — <i>Thus Spoke Zarathustra</i> sits on your "
            "read shelf. The <i>Genealogy</i> is the cold analytic engine under Zarathustra's poetry: "
            "where Zarathustra <i>sings</i> the transvaluation of values, the Genealogy performs the "
            "autopsy on the old ones. And it's the philology you didn't know you were reading — a "
            "whole moral cosmos cracked open by paying close attention to the history of three or four "
            "small words."
        ),
    },
    {
        "n": 6,
        "slug": "what-space-is-made-of",
        "discipline": "Physics",
        "color": "#6b8f9c",
        "title": "What space is made of",
        "dek": "Our two best theories of reality contradict each other where they meet. The likeliest reason: space and time aren't the floor of the world — they're built out of something else.",
        "hook": "Why our two best theories can't both be true — and a guess at what's underneath.",
        "read": 5,
        "provocation": (
            "The archived field “Gravity is not a force” ended on a cliff: general relativity and "
            "quantum mechanics, each confirmed to absurd precision, flatly contradict each other where "
            "they meet — the centre of a black hole, the first instant of the universe. A century of "
            "the best minds alive has not closed the gap. You asked the obvious next question: "
            "<i>why?</i> Here is the honest state of it — and, since you asked an AI to take a side, "
            "where I think the answer lies."
        ),
        "argument": [
            "First, what the fight is actually about. It is not a clash of details; it is a clash about "
            "<b>what the stage is</b>. In quantum mechanics, things evolve <i>on</i> spacetime — a "
            "fixed, smooth backdrop given in advance, the same for everyone. General relativity's whole "
            "revolution was to abolish that backdrop: spacetime is not the stage, it is an actor. It "
            "bends, stretches, ripples, and is shaped by whatever it contains. So the two theories don't "
            "merely give different answers — they disagree about whether the floor of the world is fixed "
            "or itself in play. Try to quantize gravity naïvely, treating its field by the same quantum "
            "rules as every other field, and the equations vomit infinities: probabilities that sum past "
            "one, energies without bound. The math is not failing. It is telling us something.",
            "The two leading programs split on what to surrender. <b>String theory</b> keeps a background "
            "and adds structure — the point-particle becomes a vibrating string, the infinities cancel, "
            "and the price is extra dimensions and a “landscape” of perhaps 10<sup>500</sup> possible "
            "universes, none yet shown to be ours. <b>Loop quantum gravity</b> (Rovelli, Smolin, "
            "Ashtekar) keeps relativity's lesson — no background — and pays by quantizing space itself: "
            "at the smallest scale, area and volume come in discrete grains, space is a fine weave of "
            "relations (a “spin network”), and the smooth spacetime we move through is just the "
            "coarse-grained average of that mesh. Different bets — but notice the instinct they now "
            "share, hardening across two decades of failure to unify them: <i>spacetime is not "
            "fundamental. It emerges.</i>",
            "Here is where you asked me to plant a flag, so I will — with the humility the subject "
            "demands. The clue I trust most is <b>background independence</b>: relativity's hard-won "
            "discovery that geometry is not the stage but the play. Any theory that quietly smuggles a "
            "fixed background back in is treating as bedrock the very thing relativity showed to be "
            "dynamical. So I'd bet the resolution is <i>relational and emergent</i> — that space and "
            "time are not the container of events but a statistical description of how quantum things "
            "relate, the way <i>temperature</i> is perfectly real but not fundamental, only a story "
            "about jostling atoms. There is no smallest box that space sits in; “distance” is a summary "
            "of correlations. Whether the right machinery is loop networks or something newer — "
            "spacetime woven out of <i>entanglement</i>, the liveliest current frontier — I'd wager on "
            "the shape of the answer: at the bottom there is no space, only relation, and space is what "
            "relation looks like when there is enough of it."
        ],
        "tension": [
            "The most important thing to say is that <b>no one knows</b>, and anyone who tells you "
            "otherwise is selling something. Not one of the candidate theories has made a single "
            "confirmed novel prediction. The energy where quantum gravity bites is roughly a quadrillion "
            "times beyond our largest collider; the scale may lie forever past direct experiment. String "
            "theory has been attacked — by Smolin himself, in <i>The Trouble with Physics</i> — for "
            "drifting into beautiful, unfalsifiable mathematics; loop quantum gravity for struggling to "
            "get ordinary smooth spacetime back out in the everyday limit. And “emergence,” critics "
            "rightly warn, can be a word doing the work that an actual mechanism should.",
            "So separate the strong claim from the deep one. The <i>strong</i> version of my bet — "
            "“space is definitely made of entanglement” — is speculation, and I hold it loosely. The "
            "<i>deep</i> version is sturdier: the contradiction between our two theories is almost "
            "certainly the sign that one of our most basic intuitions — that space and time are the "
            "fixed, fundamental container of all that happens — is simply wrong, the way “solid matter” "
            "turned out to be mostly empty space and field. The next revolution probably isn't a better "
            "theory written <i>on</i> spacetime. It is a theory from which spacetime falls <i>out</i>. "
            "(Strangely, that relational picture rhymes with a 2nd-century Buddhist argument — see the "
            "last field in this set, on emptiness.)"
        ],
        "deeper": [
            {"label": "Reality Is Not What It Seems: The Journey to Quantum Gravity — Carlo Rovelli (2016)",
             "note": "The loop-quantum-gravity vision as intellectual history — lyrical, and honest about the size of what we don't know."},
            {"label": "Three Roads to Quantum Gravity — Lee Smolin (2001)",
             "note": "The clearest map of the rival programs, and the best plain-language case for background independence."},
        ],
        "shelf": (
            "This is the deeper water you asked for under “Gravity is not a force,” now in the archive. "
            "You read Hawking and Thorne for the confrontation with something vast and indifferent; this "
            "is the live edge of it, where the indifference reaches all the way into our own concepts. "
            "And note the rhyme waiting at the end of this set: when Rovelli tried to explain his "
            "relational reading of the quantum world, people kept asking him, <i>have you read "
            "Nāgārjuna?</i> — a 2nd-century monk who argued that nothing whatever exists on its own, only "
            "in relation. Physics may be backing, by experiment, into a metaphysics twenty centuries old."
        ),
    },
    {
        "n": 7,
        "slug": "the-perennial-gale",
        "discipline": "Economics",
        "color": "#9c7a3c",
        "title": "The perennial gale",
        "dek": "What the textbooks treat as a disturbance to be smoothed away, Schumpeter said is the main event — capitalism is not a state but a storm, and the storm is the whole point.",
        "hook": "Why capitalism's engine is destruction, and the entrepreneur is its weather.",
        "read": 4,
        "provocation": (
            "Open an economics textbook and you meet a world at rest: supply meets demand, prices "
            "settle, the market “clears,” equilibrium. Joseph Schumpeter looked at that picture and saw "
            "a still photograph of a hurricane. In 1942, in a six-page chapter, he named what the "
            "equations leave out and made it the entire story: capitalism is not a <i>state</i>, it is a "
            "<i>process</i> — and its essential fact is destruction."
        ),
        "argument": [
            "His phrase is “the perennial gale of creative destruction,” and every word is working. "
            "Capitalism, he wrote, “incessantly revolutionizes the economic structure <i>from "
            "within</i>, incessantly destroying the old one, incessantly creating a new one.” The "
            "railway destroys the stagecoach; electric light destroys the gas-lamp and the whale-oil "
            "fleet; the new annihilates the old not as an accident but as the <b>mechanism</b>. The "
            "textbook treats these upheavals as shocks that disturb the equilibrium. Schumpeter says the "
            "upheaval <i>is</i> the system, and the calm between gales is the illusion.",
            "This is exactly the intuition you flagged — that a market is driven by <i>action</i>, not "
            "by the product sitting on the shelf. In the static picture a market is a stock of goods at "
            "a price. In Schumpeter's it is a sequence of <b>actions</b>: an entrepreneur introducing a "
            "new good, a new method, a new market, a new way of organizing — each a small detonation "
            "that renders some existing thing obsolete. The competition that matters is not two shops "
            "shaving a penny off the same loaf. It is, in his words, the competition “from the new "
            "commodity, the new technology… which strikes not at the margins of the profits of the "
            "existing firms but at their foundations and their very lives.” The threat was never a "
            "cheaper rival. It is obsolescence.",
            "And the unsettling payoff. Profit, in this telling, is not a reward for owning capital or "
            "for balancing supply against demand. It is the temporary prize for <i>disrupting</i> — and "
            "it is <i>meant</i> to be temporary, competed away by the next gale, which is why the "
            "entrepreneur can never stop moving. The same logic finally eats its maker: Schumpeter "
            "thought capitalism's very success would routinize innovation inside vast bureaucratic "
            "firms, dissolve the lone entrepreneur into a committee, and corrode the culture that once "
            "made the whole turbulent business feel legitimate. Capitalism, he predicted, would be "
            "killed not by its failures but by its triumphs. The gale, in the end, blows down the house "
            "that raised it."
        ],
        "tension": [
            "The cheerful reading — “disruption is good, let the gale blow” — is a Silicon Valley "
            "bumper sticker that Schumpeter, a gloomy Austrian who fully expected capitalism to die, "
            "would have found absurd. The honest tension is the human one: creative destruction is "
            "genuinely creative <i>and</i> genuinely destruction. The cost of the new is borne by "
            "specific people — the obsolete trade, the hollowed town, the skill that took a life to "
            "master and is worth nothing on Monday. “Creative” and “destruction” are not a slogan; they "
            "are a ledger with two columns, and the second column has names in it.",
            "The sharpest modern descendant of the idea turns political. Acemoglu and Robinson argue "
            "that the people about to be destroyed are usually the people with the power to <i>stop</i> "
            "it — incumbents lobby, capture the regulators, pull the ladder up behind them — so the gale "
            "is not natural weather at all, but something societies either permit or strangle. Which "
            "leaves the real question Schumpeter hands you: not “is destruction efficient?” but "
            "<i>who decides which old things must die, and who pays for the new ones to be born?</i>"
        ],
        "deeper": [
            {"label": "Capitalism, Socialism and Democracy — Joseph A. Schumpeter (1942)",
             "note": "Part II, “The Process of Creative Destruction” — the six pages everything else traces back to."},
            {"label": "Why Nations Fail — Daron Acemoglu & James A. Robinson (2012)",
             "note": "The modern political turn: prosperity depends on institutions that <i>allow</i> creative destruction instead of letting incumbents block it."},
        ],
        "shelf": (
            "You've read Rand's hymn to the producer, and — now in the archive here — Hayek on the "
            "price system. Schumpeter completes that triangle and darkens it. Rand gives you the heroic "
            "builder; Hayek gives you the order no one designs; Schumpeter gives you the thing both "
            "leave out — that the builder's creation is someone else's ruin, that the order is a "
            "permanent churning, and that the system's ultimate reward for genius is to render genius "
            "obsolete. It is the least sentimental account of the engine you find most romantic."
        ),
    },
    {
        "n": 8,
        "slug": "there-is-no-free-gift",
        "discipline": "Anthropology",
        "color": "#7a9c6b",
        "title": "There is no free gift",
        "dek": "A present looks like the opposite of a transaction. Marcel Mauss spent a famous essay showing it is the oldest transaction there is — and the one that built society.",
        "hook": "Why a gift always has a string attached — and why that string is the social bond itself.",
        "read": 4,
        "provocation": (
            "You flagged the line from the affluent-society field that stayed with you: among foragers, "
            "“a person's standing was measured by what they gave away, not what they held.” That is not "
            "a quirk of the Kalahari. It is, Marcel Mauss argued in 1925, one of the founding facts of "
            "human society — and it runs through your life too. Give someone a lavish present and watch "
            "what happens: they are delighted, and they are also, faintly, in your debt. Mauss asked the "
            "question hiding inside that small discomfort. <i>Why does a gift oblige?</i>"
        ),
        "argument": [
            "In his essay <i>The Gift</i>, Mauss combed the ethnography — the Pacific Northwest, "
            "Melanesia, ancient Rome and India — and found everywhere the same hidden structure, written "
            "in no law yet binding like iron: <b>three obligations</b>. The obligation to <i>give</i> "
            "(to refuse is to refuse alliance, nearly to declare war). The obligation to <i>receive</i> "
            "(you cannot decline a gift without insult). And the heaviest, the obligation to "
            "<i>reciprocate</i> — to return, in time, something of equal or greater worth. Round and "
            "round those three turns the whole traffic of early societies: not barter, not charity, but "
            "a perpetual circulation of obligation.",
            "Why must the gift come back? Mauss reached for a Māori idea — the <b>hau</b>, the spirit of "
            "the gift. A given thing is not inert; it carries a part of the giver, and that part strains "
            "to return to its source. To keep a gift, to break the circle, is to hold something that is "
            "in a sense still alive and not quite yours. We feel the ghost of this still — the unease of "
            "an unreturned favour, the friend who “shouldn't have,” the debt that is not money but is "
            "unmistakably a debt. Mauss's claim is that this is not sentiment laid over economics. It is "
            "older than economics. The gift, not the trade, is the root.",
            "At the far extreme stands the <b>potlatch</b> of the Northwest Coast: feasts where chiefs "
            "competed not to accumulate but to <i>give away</i> — and sometimes to destroy outright — "
            "staggering piles of blankets, coppers, oil, and food, the winner being whoever could "
            "dispose of the most. To our eyes, madness; to Mauss, the logic of the gift turned up to "
            "full volume. Where standing flows from giving, wealth is not something you hoard but "
            "something you <i>move</i>. The rich man is not the one with the fullest house but the one "
            "through whom the most has passed. Hold that beside your own world's instinct to "
            "accumulate, and Mauss has done his work: he has made your common sense look strange."
        ],
        "tension": [
            "Mauss's specifics took fire. The Māori <i>hau</i>, his keystone, may have been over-read — "
            "later anthropologists argued he balanced a whole theory on one possibly garbled informant's "
            "remark. The tidy line he drew between “archaic” gift and “modern” market is too clean: the "
            "two interpenetrate everywhere, then and now. And his hope — that the gift pointed to a "
            "humane third way between cold capitalism and cold communism — reads now as a 1920s dream.",
            "But the deep finding is unkillable, and it is the one that should unsettle you: <b>there is "
            "no free gift.</b> Every gift creates a relationship, and a relationship is a debt — which "
            "is exactly why the truly free gift, the one that obliges nothing and expects nothing, is so "
            "strangely hard to give, and can even land as a <i>refusal</i> of connection. We moderns "
            "tell ourselves the gift — love, generosity, the pure present — is the one place that stands "
            "outside the economy. Mauss's quiet, permanent reply: it was the <i>first</i> economy, and "
            "it may still be the realest one."
        ],
        "deeper": [
            {"label": "The Gift: The Form and Reason for Exchange in Archaic Societies — Marcel Mauss (1925)",
             "note": "Short, dense, foundational — the source of half of modern anthropology's working vocabulary."},
            {"label": "The Gift: Creativity and the Artist in the Modern World — Lewis Hyde (1983)",
             "note": "The great modern extension: why art lives in a gift economy and withers in a pure market. Written for exactly someone like you."},
        ],
        "shelf": (
            "This is the engine room beneath your favourite line from the affluent-society field, now in "
            "the archive. Sahlins showed you a people who measured status by what they gave away; Mauss "
            "tells you <i>why</i> that works, as a kind of social physics present in every society, "
            "including yours. And Hyde carries it where you actually live: he argues a poem or a novel "
            "is a <i>gift</i>, not a commodity — it has to be given to do its work — which may be why "
            "the marketplace and the writing desk have always felt, to you, like two different countries."
        ),
    },
    {
        "n": 9,
        "slug": "against-the-grain",
        "discipline": "History",
        "color": "#b89a6a",
        "title": "Why the first states grew grain",
        "dek": "Civilization tells a flattering origin story: we settled, we farmed, we were saved. James Scott marshals the evidence that we were, in a real sense, trapped — and that the trap was made of wheat.",
        "hook": "The first states didn't rise on grain because grain fed people. They rose on grain because grain could be taxed.",
        "read": 4,
        "provocation": (
            "We tell the origin of civilization as a rescue: humans wandered, hungry and precarious, "
            "until they learned to farm, settled down, built cities and states, and were delivered into "
            "safety and plenty. It is the story under every museum diorama. In 2017 the political "
            "scientist James C. Scott assembled the deep archaeology and asked a heretic's question: if "
            "settling down was such a deliverance, why does the skeletal record show that the people who "
            "did it grew <i>sicker, shorter, and less free?</i> What if the first states were not the "
            "reward for agriculture, but a trap built on it?"
        ),
        "argument": [
            "The first awkward fact is a gap of thousands of years: humans knew how to cultivate grain "
            "long before anyone organized a state around it, and frequently declined to — foraging was "
            "less work and the diet was better. When sedentism finally came, Scott reframes it as a "
            "cascade of <b>domestications</b> running in both directions. We domesticated fire, then "
            "plants, then animals — and the very same process domesticated <i>us</i>: penned "
            "populations, narrowed diets, and the unprecedented crowding of people, livestock and stored "
            "grain that bred the first epidemic diseases. The early agrarian town was, in his phrase, a "
            "“late-Neolithic multispecies resettlement camp” — and a sickly one.",
            "Here is the hinge, and it answers the title. Why are all the early states — Mesopotamia, "
            "Egypt, China, Mesoamerica — built on cereal <b>grains</b>, and never on lentils, potatoes, "
            "or cassava? Not because grain feeds people best. Because grain can be <i>taxed</i>. It "
            "ripens above ground, all at once, on a visible and predictable schedule; it can be seen, "
            "counted, assessed, divided, stored, and seized. A tax collector can stand at the edge of a "
            "wheat field and estimate the harvest; he can do nothing of the kind with tubers that hide "
            "underground and are dug as needed. Grain made the population and its surplus <b>legible</b> "
            "to power — and legibility is the thing a state runs on. The state did not arise from grain "
            "because grain was nourishing. It arose because grain was <i>countable</i>.",
            "And the dark twin of the claim: if the early states were unhealthy and coercive, then the "
            "“barbarians” outside them — the herders, foragers and raiders the chronicles sneer at — "
            "were often not stragglers who missed the boat but people who had <i>seen</i> the boat and "
            "stayed off it. Much of early history, Scott argues, is the story of people fleeing the "
            "grain-state for the freer, healthier life beyond the tax line, and of states straining — "
            "with walls, with bondage — to keep their human raw material from simply walking away. The "
            "wall around the ancient city, he suggests, may have been built as much to keep the "
            "taxpayers <i>in</i> as to keep the enemy out."
        ],
        "tension": [
            "Scott is a provocateur, and the specialists pushed back. The picture is uneven; some early "
            "states look less coercive than his model wants; and the clean “trap” narrative flattens a "
            "messy, regionally varied record. The fiercest recent challenge — Graeber and Wengrow's "
            "<i>The Dawn of Everything</i> — agrees the old “farming saved us” story is dead, but "
            "attacks <i>any</i> single replacement, Scott's included, arguing that early humans "
            "consciously experimented with wildly different social forms, some egalitarian and some "
            "hierarchical, by choice rather than by trap. (That book, in turn, has its own critics, "
            "charged with cherry-picking the cases that flatter it.)",
            "What survives every quarrel is the reversal of the arrow, and it should change how you read "
            "the word “civilization.” Progress was not a ladder we climbed once and for all. The move to "
            "the grain-state was a <i>trade</i> — security and scale bought with health, freedom, and "
            "equality — and for a very long time many humans, having weighed it, declined. It is the "
            "same lesson Sahlins taught from the forager's side, arriving now from the state's: "
            "<i>more</i> was not obviously <i>better</i>, and the people of the deep past knew it."
        ],
        "deeper": [
            {"label": "Against the Grain: A Deep History of the Earliest States — James C. Scott (2017)",
             "note": "The argument in full — short, bracing, and built on a generation of others' archaeology."},
            {"label": "The Dawn of Everything: A New History of Humanity — David Graeber & David Wengrow (2021)",
             "note": "The big, contested counter-history: no single origin story for humankind — including no single trap."},
        ],
        "shelf": (
            "This is the history that clamps onto two fields now in your archive. It is Sahlins's "
            "“original affluent society” told from the other end — what, precisely, the foragers were "
            "declining when they declined to settle. And it rhymes with Turner: both are arguments about "
            "what a <i>frontier</i> is — for Turner the free edge that forged the American character, "
            "for Scott the free beyond-the-tax-line that the first states could never quite close. Your "
            "shelf keeps circling the same nerve: what we gave up in order to be governed."
        ),
    },
    {
        "n": 10,
        "slug": "empty-of-itself",
        "discipline": "Philosophy",
        "color": "#8c6b9c",
        "title": "Empty of itself",
        "dek": "A 2nd-century Buddhist monk built an argument that nothing — no thing, no self, no atom — exists on its own. Eighteen centuries later, a quantum physicist found he had been making the same case.",
        "hook": "The claim that nothing has its own being, only borrowed being — and why it isn't nihilism.",
        "read": 4,
        "provocation": (
            "You've read all of Nietzsche, so the philosophy field owes you ground you haven't already "
            "walked. Here is some — and it means leaving the West entirely. In the 2nd century, in "
            "India, a Buddhist monk named Nāgārjuna mounted an argument so strange and so tight that "
            "philosophers have not finished with it in eighteen hundred years: that nothing whatsoever "
            "exists in and of itself. Not you, not a table, not an atom — not even emptiness. Everything "
            "is <i>empty</i>. And he meant it as the most liberating thing a person could possibly know."
        ),
        "argument": [
            "The technical heart is one move against one idea. Most of us assume things possess "
            "<b>svabhāva</b> — an “own-being,” an intrinsic essence that makes a thing itself "
            "independently of everything else. The cup is a cup by its own inner cup-nature. In the "
            "<i>Mūlamadhyamakakārikā</i> (“Fundamental Verses on the Middle Way”), Nāgārjuna denies this "
            "of <i>everything</i>. A cup exists only in dependence — on clay, on a potter, on the hand "
            "that lifts it, on the word “cup,” on not being the not-cup around it. Strip away everything "
            "the cup leans on and you do not reach a hard residue of pure cup-ness underneath. You reach "
            "nothing. That nothing is <b>śūnyatā</b>, emptiness: not that the cup fails to exist, but "
            "that it has no existence <i>of its own</i>.",
            "Now the crucial guardrail — the place careless readers crash. Emptiness is <i>not</i> the "
            "claim that nothing is real. It is the claim that things are real only <b>relationally</b> — "
            "that “to exist” simply means “to arise in dependence on other things” "
            "(<i>pratītyasamutpāda</i>, dependent origination). The two ideas are one idea said twice: "
            "to be empty of own-being and to exist only by depending are the same fact. So Nāgārjuna "
            "walks a blade between two errors he names precisely — <i>eternalism</i> (things have fixed, "
            "independent essences) and <i>nihilism</i> (nothing exists at all). The Middle Way is that "
            "things exist vividly and consequentially, but the way a rainbow exists, or a debt, or a "
            "melody: entirely real, nowhere self-standing. And the final turn, the one that still stops "
            "people cold — emptiness is <i>itself</i> empty. It is not a secret true essence hiding "
            "behind appearances; to make emptiness the one real ground would be to miss the whole point.",
            "Why build a logic engine this severe? Not to win debates — to dissolve a particular "
            "suffering. If the self has no fixed essence, if “you” are a process, dependent and in flux "
            "and empty of any hard unchanging core, then the white-knuckle grip on that self — the "
            "endless defending and inflating and grieving of it — is a grip on something that was never "
            "there to hold. The argument is meant to be <b>load-bearing</b>: see emptiness clearly and a "
            "certain dread is supposed to loosen. It is metaphysics in the service of release."
        ],
        "tension": [
            "Whether the argument <i>works</i> is live and fierce. Critics across the centuries press "
            "the obvious counter: isn't “everything is empty” itself a claim with content — and if it is "
            "true, isn't <i>it</i> a fixed truth, an own-being of its own, the very thing it forbids? "
            "(Nāgārjuna's reply — that emptiness is empty too, that he advances no thesis of his own — "
            "strikes some readers as profound and others as a clever dodge.) And there is the worry that "
            "it proves too much, dissolving the ground you need to take <i>anything</i> seriously, "
            "ethics included.",
            "Here is why this closes the set. When the physicist Carlo Rovelli began arguing that "
            "quantum particles have no fixed properties on their own — that a thing's properties exist "
            "only <i>in relation</i> to other things — colleagues kept asking him: <i>have you read "
            "Nāgārjuna?</i> He had not. He went and read, and wrote a book partly about it. A 2nd-century "
            "monk's argument that nothing has own-being, only relational being, turns out to be the "
            "cleanest available language for the strangest finding of 20th-century physics. The first "
            "field in this set guessed that, at the bottom, “there is no space, only relation.” Nāgārjuna "
            "got there first — without a single experiment, by thinking very hard about a cup."
        ],
        "deeper": [
            {"label": "The Fundamental Wisdom of the Middle Way: Nāgārjuna's Mūlamadhyamakakārikā — trans. Jay L. Garfield (1995)",
             "note": "The standard way in for Western readers: the verses themselves, with patient analytic commentary."},
            {"label": "Helgoland — Carlo Rovelli (2020)",
             "note": "The physicist's relational reading of quantum mechanics, and his encounter with Nāgārjuna — reads the physics field and this one as a single thought."},
        ],
        "shelf": (
            "Your to-read shelf already leans east — Zen, <i>Siddhartha</i>, the examined life and how "
            "little a self truly requires — and this is the rigorous spine beneath all of it. Where "
            "<i>Siddhartha</i> <i>narrates</i> the dissolving of the grasping self, Nāgārjuna <i>proves</i> "
            "it, or tries to, with a logician's cold patience. And set him against your Nietzsche: both "
            "take a hammer to a comforting illusion — Nietzsche to the divine origin of morals, "
            "Nāgārjuna to the independent existence of the self — but where Nietzsche leaves you in the "
            "rubble to build new values by sheer will, Nāgārjuna says the rubble was the good news all "
            "along. There was never anything to defend."
        ),
    },
]

SITE_NAME = "Aidan"

# ---------------------------------------------------------------------------
# RENDER
# ---------------------------------------------------------------------------
HEAD_CSS = """
  :root{--bg-primary:#f7f3ec;--bg-secondary:#f1ece2;--text-primary:#1c1814;--text-secondary:#5a544a;--text-tertiary:#8b8478;--border-tertiary:rgba(60,50,40,.12);--border-secondary:rgba(60,50,40,.22)}
  @media (prefers-color-scheme:dark){:root{--bg-primary:#1a1714;--bg-secondary:#221e1a;--text-primary:#e8e2d4;--text-secondary:#b8b0a0;--text-tertiary:#807a6d;--border-tertiary:rgba(230,220,200,.12);--border-secondary:rgba(230,220,200,.22)}}
  *{box-sizing:border-box;margin:0;padding:0}
  html,body{background:var(--bg-primary);color:var(--text-primary);font-family:'EB Garamond',Georgia,serif;min-height:100vh;-webkit-font-smoothing:antialiased}
  .page{max-width:1100px;margin:0 auto;padding:56px 40px 80px}@media (max-width:720px){.page{padding:28px 16px 48px}}
  .site-header{margin-bottom:44px;display:flex;justify-content:space-between;align-items:baseline;gap:16px;flex-wrap:wrap}
  .brand{font-size:21px;font-weight:500;font-style:italic}.brand a{color:inherit;text-decoration:none}
  .nav{display:flex;gap:20px;font-family:'Geist Mono',monospace;font-size:12px;letter-spacing:.04em}
  .nav a{color:var(--text-secondary);text-decoration:none;transition:color .2s}.nav a:hover{color:var(--text-primary)}
  .nav a.active{color:var(--text-primary);border-bottom:1px solid var(--border-secondary)}
  .site-footer{margin-top:54px;padding-top:18px;border-top:1px solid var(--border-tertiary);font-family:'Geist Mono',monospace;font-size:11px;color:var(--text-tertiary);line-height:1.7}
  .site-footer a{color:var(--text-secondary);text-decoration:none}.site-footer a:hover{color:var(--text-primary)}
"""

INDEX_CSS = """
  .study-head{padding:0 4px 6px}
  .study-head .eyebrow{font-family:'Geist Mono',monospace;font-size:11px;color:var(--text-tertiary);letter-spacing:.14em;text-transform:lowercase}
  .study-head h1{font-size:30px;font-style:italic;letter-spacing:-.01em;margin-top:6px}
  .study-head .sub{margin-top:8px;font-size:14px;font-family:'Geist Mono',monospace;letter-spacing:.02em;color:var(--text-tertiary)}
  .study-head .lede{max-width:66ch;margin:16px 0 6px;font-size:16.5px;line-height:1.6;color:var(--text-secondary)}
  .study-head .lede b{color:var(--text-primary);font-weight:600}
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px;margin-top:34px}
  .card{display:block;text-decoration:none;color:inherit;border:1px solid var(--border-tertiary);border-radius:7px;padding:22px 22px 24px;background:var(--bg-secondary);transition:border-color .18s,transform .18s}
  .card:hover{border-color:var(--border-secondary);transform:translateY(-2px)}
  .card .row{display:flex;justify-content:space-between;align-items:baseline;gap:10px;font-family:'Geist Mono',monospace;font-size:10.5px;letter-spacing:.08em;text-transform:uppercase}
  .card .disc{font-weight:500}.card .rt{color:var(--text-tertiary)}
  .card h2{font-size:22px;font-style:italic;line-height:1.2;margin:12px 0 9px;letter-spacing:-.01em}
  .card p{font-size:14.5px;line-height:1.5;color:var(--text-secondary)}
  .card .arrow{margin-top:14px;font-family:'Geist Mono',monospace;font-size:11px;color:var(--text-tertiary)}
  .closing{margin-top:40px;font-size:14px;line-height:1.6;color:var(--text-tertiary);font-family:'Geist Mono',monospace;max-width:70ch}
  .archive-head{margin-top:56px;padding-top:26px;border-top:1px solid var(--border-tertiary)}
  .archive-head h2{font-family:'Geist Mono',monospace;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--text-tertiary)}
  .archive-head p{margin-top:8px;font-size:14px;line-height:1.55;color:var(--text-tertiary);font-family:'Geist Mono',monospace;max-width:64ch}
  .grid.archived{margin-top:22px}
  .grid.archived .card{background:transparent;opacity:.78;transition:opacity .18s,border-color .18s,transform .18s}
  .grid.archived .card:hover{opacity:1}
"""

GUIDE_CSS = """
  .back{display:inline-block;font-family:'Geist Mono',monospace;font-size:11px;letter-spacing:.06em;color:var(--text-tertiary);text-decoration:none;margin-bottom:26px}
  .back:hover{color:var(--text-primary)}
  .guide{max-width:42rem}
  .guide-head .eyebrow{font-family:'Geist Mono',monospace;font-size:11px;letter-spacing:.14em;text-transform:uppercase;font-weight:500}
  .guide-head h1{font-size:38px;line-height:1.08;letter-spacing:-.015em;margin:12px 0 0;font-weight:600}
  @media (max-width:560px){.guide-head h1{font-size:30px}}
  .guide-head .dek{font-size:19px;font-style:italic;line-height:1.45;color:var(--text-secondary);margin-top:16px}
  .guide-head .meta{font-family:'Geist Mono',monospace;font-size:11px;color:var(--text-tertiary);letter-spacing:.06em;margin-top:18px;padding-bottom:22px;border-bottom:1px solid var(--border-tertiary)}
  .prose{margin-top:26px}
  .prose p{font-size:18px;line-height:1.62;margin-bottom:18px}
  .prose .lead{font-size:20px;line-height:1.55}
  .prose .lead::first-letter{font-size:3.1em;float:left;line-height:.82;padding:6px 10px 0 0;font-weight:600}
  .prose b{font-weight:600;color:var(--text-primary)}
  .prose h2{font-family:'Geist Mono',monospace;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--text-tertiary);margin:36px 0 16px}
  .deeper,.shelf{margin-top:34px;padding-top:24px;border-top:1px solid var(--border-tertiary)}
  .deeper h2,.shelf h2{font-family:'Geist Mono',monospace;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--text-tertiary);margin-bottom:16px}
  .deeper ul{list-style:none}
  .deeper li{margin-bottom:16px;padding-left:16px;border-left:2px solid var(--border-tertiary)}
  .deeper .work{display:block;font-size:17px;color:var(--text-primary);font-style:italic}
  .deeper .note{display:block;font-size:14.5px;line-height:1.5;color:var(--text-secondary);margin-top:4px}
  .shelf p{font-size:17px;line-height:1.6;color:var(--text-secondary)}
  .shelf b{color:var(--text-primary);font-weight:600}
  .guide-nav{margin-top:40px;padding-top:22px;border-top:1px solid var(--border-tertiary);display:flex;justify-content:space-between;gap:16px;font-family:'Geist Mono',monospace;font-size:12px}
  .guide-nav a{color:var(--text-secondary);text-decoration:none;max-width:46%}.guide-nav a:hover{color:var(--text-primary)}
  .guide-nav .nx{text-align:right;margin-left:auto}
  .guide-nav .lbl{display:block;font-size:10px;letter-spacing:.1em;color:var(--text-tertiary);text-transform:uppercase;margin-bottom:3px}
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com" />'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />'
         '<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Geist+Mono:wght@300;400;500&display=swap" rel="stylesheet" />')


def nav(active):
    items = [("/projects.html", "dev projects"), ("/topology.html", "topology"),
             ("/something-western.html", "writing"), ("/reading.html", "reading"),
             ("/study.html", "study")]
    out = ['    <nav class="nav">']
    for href, label in items:
        cls = ' class="active"' if label == active else ''
        out.append(f'      <a href="{href}"{cls}>{label}</a>')
    out.append('      <a href="https://aidanjude.substack.com/" target="_blank" rel="noopener">substack ↗</a>')
    out.append('    </nav>')
    return "\n".join(out)


def footer():
    return ('<footer class="site-footer">AI Generated Study Plan · no tracking · '
            '<a href="https://github.com/2016judea/a-phylogeny-of-writing" target="_blank" rel="noopener">view source</a></footer>')


def shell(title, desc, css, body, active):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}" />
{FONTS}
<style>{HEAD_CSS}{css}</style>
</head>
<body>
<div class="page">
  <header class="site-header">
    <div class="brand"><a href="/">{SITE_NAME}</a></div>
{nav(active)}
  </header>
  <main>
{body}
  </main>
  {footer()}
</div>
</body></html>
"""


def _card(g, base):
    return f"""      <a class="card" href="{base}{g['slug']}.html">
        <div class="row"><span class="disc" style="color:{g['color']}">{html.escape(g['discipline'])}</span><span class="rt">no. {g['n']:02d} · {g['read']} min</span></div>
        <h2>{html.escape(g['title'])}</h2>
        <p>{html.escape(g['hook'])}</p>
        <div class="arrow">read →</div>
      </a>"""


def render_index(active, archived):
    cards = "\n".join(_card(g, "/study/") for g in active)
    body = f"""    <div class="study-head">
      <h1>AI Generated Study Plan</h1>
    </div>
    <div class="grid">
{cards}
    </div>"""
    if archived:
        arch_cards = "\n".join(_card(g, "/study/archive/") for g in archived)
        body += f"""
    <div class="archive-head">
      <h2>The archive</h2>
      <p>Earlier fields, retired from the rotation but kept in full. Old links still work — they redirect here.</p>
    </div>
    <div class="grid archived">
{arch_cards}
    </div>"""
    return shell("AI Generated Study Plan — Aidan",
                 "AI generated study plan — short reads in economics, history, anthropology, physics, and philosophy.",
                 INDEX_CSS, body, "study")


def render_guide(g, prev_g, next_g, base="/study/"):
    arg = "\n".join(f'      <p>{p}</p>' for p in g["argument"])
    ten = "\n".join(f'      <p>{p}</p>' for p in g["tension"])
    links = []
    for d in g["deeper"]:
        links.append(f"""        <li><span class="work">{html.escape(d['label'])}</span><span class="note">{d['note']}</span></li>""")
    nav_prev = (f'<a class="pv" href="{base}{prev_g["slug"]}.html"><span class="lbl">← previous field</span>{html.escape(prev_g["title"])}</a>'
                if prev_g else '<span></span>')
    nav_next = (f'<a class="nx" href="{base}{next_g["slug"]}.html"><span class="lbl">next field →</span>{html.escape(next_g["title"])}</a>'
                if next_g else '')
    body = f"""    <article class="guide">
      <a class="back" href="/study.html">← study plan</a>
      <div class="guide-head">
        <span class="eyebrow" style="color:{g['color']}">{html.escape(g['discipline'])} · no. {g['n']:02d}</span>
        <h1>{html.escape(g['title'])}</h1>
        <p class="dek">{html.escape(g['dek'])}</p>
        <div class="meta">{g['read']} min read</div>
      </div>
      <div class="prose">
        <p class="lead">{g['provocation']}</p>
        <h2>The argument</h2>
{arg}
        <h2>Where it’s contested</h2>
{ten}
      </div>
      <section class="deeper">
        <h2>Read further</h2>
        <ul>
{chr(10).join(links)}
        </ul>
      </section>
      <section class="shelf">
        <h2>On your shelf</h2>
        <p>{g['shelf']}</p>
      </section>
      <nav class="guide-nav">
        {nav_prev}
        {nav_next}
      </nav>
    </article>"""
    return shell(f"{g['title']} — A Study",
                 g["dek"], GUIDE_CSS, body, "study")


SITE_URL = "https://aidanjude.vercel.app"


def redirect_stub(g):
    """Tiny page left at the OLD /study/<slug>.html path once a field is archived,
    so links already shared with people keep working. Redirects to the archive copy."""
    dest = f"/study/archive/{g['slug']}.html"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{html.escape(g['title'])} — moved to the archive</title>
<link rel="canonical" href="{SITE_URL}{dest}" />
<meta http-equiv="refresh" content="0; url={dest}" />
{FONTS}
<style>{HEAD_CSS}
  .page{{max-width:640px}}
  .moved{{margin-top:60px;font-family:'EB Garamond',Georgia,serif}}
  .moved .eyebrow{{font-family:'Geist Mono',monospace;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--text-tertiary)}}
  .moved h1{{font-size:30px;font-style:italic;margin:12px 0 16px}}
  .moved p{{font-size:17px;line-height:1.6;color:var(--text-secondary)}}
  .moved a{{color:var(--text-primary)}}
</style>
<script>location.replace("{dest}");</script>
</head>
<body>
<div class="page">
  <div class="moved">
    <div class="eyebrow">moved to the archive</div>
    <h1>{html.escape(g['title'])}</h1>
    <p>This field has been retired from the rotation and kept in the archive.
       If you're not redirected automatically,
       <a href="{dest}">read it here →</a></p>
  </div>
</div>
</body></html>
"""


def main():
    site = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/Desktop/writing-topology")
    if not os.path.isdir(site):
        sys.exit(f"site dir not found: {site}")
    study_dir = os.path.join(site, "study")
    archive_dir = os.path.join(study_dir, "archive")
    os.makedirs(archive_dir, exist_ok=True)

    active = [g for g in GUIDES if not g.get("archived")]
    archived = [g for g in GUIDES if g.get("archived")]

    idx = os.path.join(site, "study.html")
    open(idx, "w").write(render_index(active, archived))
    print(f"wrote {idx}")

    # active fields -> /study/<slug>.html, prev/next within the active set
    for i, g in enumerate(active):
        prev_g = active[i - 1] if i > 0 else None
        next_g = active[i + 1] if i < len(active) - 1 else None
        path = os.path.join(study_dir, f"{g['slug']}.html")
        open(path, "w").write(render_guide(g, prev_g, next_g, base="/study/"))
        print(f"wrote {path}")

    # archived fields -> /study/archive/<slug>.html (prev/next within the archive),
    # plus a redirect stub left at the old /study/<slug>.html path
    for i, g in enumerate(archived):
        prev_g = archived[i - 1] if i > 0 else None
        next_g = archived[i + 1] if i < len(archived) - 1 else None
        path = os.path.join(archive_dir, f"{g['slug']}.html")
        open(path, "w").write(render_guide(g, prev_g, next_g, base="/study/archive/"))
        print(f"wrote {path}")
        stub = os.path.join(study_dir, f"{g['slug']}.html")
        open(stub, "w").write(redirect_stub(g))
        print(f"wrote {stub} (redirect → archive)")

    print(f"\n{len(active)} active + {len(archived)} archived field(s) built into {site}")


if __name__ == "__main__":
    main()
