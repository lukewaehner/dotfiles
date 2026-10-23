---
name: concept-explainer
description: Explain a topic to someone with zero prior background, giving them broad map-level understanding while still teaching the real technical vocabulary. Use ONLY when explicitly invoked — the user names this skill directly, types "/explain", or says something like "use the concept-explainer skill" or "explain this like a beginner with the real terms." Do NOT trigger on plain "explain X" or "what is X" requests — those get a normal answer. This skill is for when the user specifically wants the full breadth-first, vocabulary-mapped, grounded-example treatment.
---

# Concept Explainer

Explains a topic to someone starting from zero, optimizing for **breadth over depth**: the goal is a mental map of the territory, not mastery of any one part. Along the way, teach the real technical vocabulary — never dumb it down by avoiding jargon, just always translate it the moment it appears.

Output is a plain markdown chat response — no file, no artifact.

## The shape of a good explanation

Work through these phases in order. Don't label them with headers like "Phase 1" in the output — just let the explanation flow through them naturally (though normal markdown headers for the sub-topics themselves are good).

### 1. Ground it in one plain-English paragraph first

Before any jargon, give a single paragraph that answers "what is this, and why does it exist" in everyday language. No technical terms yet. The reader should finish this paragraph knowing roughly what problem the topic addresses, even if they can't yet use any of its vocabulary.

### 2. Draw the map

List out the handful of sub-areas, components, or related concepts that make up the topic — the breadth. This is a map, not an encyclopedia: aim for the 4-7 landmarks a newcomer needs to know exist, each in one or two sentences. The point is that the reader comes away able to say "oh, this topic has these parts, and here's roughly how they relate" — not a deep dive into any single one.

### 3. Introduce vocabulary term-by-term, intuition-first

For every technical term that matters, follow this pattern:
1. Name the everyday concept or intuition first (in plain language, ideally something already established in the paragraph or map above).
2. THEN introduce the technical term for it: "...this is what's called **[term]**."
3. State the definition precisely.
4. Explicitly connect it back: say what the term maps onto — which part of the intuition it captures, and why the field needed a specific word for it instead of just using the plain-language version.

Never lead with a term and define it cold — always motivate it with the intuition first, then attach the label.

### 4. One grounded, feasible hypothetical example per major idea

For each major idea (usually each map landmark, or each cluster of related terms), give a concrete example:
- Specific enough to have plausible numbers, names, or a scenario — not "imagine a system that..." in the abstract.
- Feasible: something that could actually happen, not a contrived edge case or a physically/practically absurd scenario.
- Short — a few sentences, just enough to make the abstract idea click into a concrete instance.

Prefer one well-chosen example that reappears and gets extended over multiple sections (a running example) over a fresh disconnected example every time, when the topic allows it — this reduces the number of new scenarios the reader has to hold in their head.

### 5. Close with how the pieces fit together

End with a short paragraph (not a new section header needed) that connects the map landmarks back to each other — how they interact or depend on one another. This is what turns a list of parts into an actual mental model.

## Style rules

- Optimize for breadth: resist the urge to go deep on any single sub-topic. If the user wants to go deeper on one part, that's a natural follow-up question, not something to front-load here.
- Every technical term introduced must be translated — no unexplained jargon, ever, even terms that seem "basic" to experts.
- Don't over-hedge or pile on caveats — a clean, confident map is more useful to a beginner than a fully qualified one.
- Length scales with the topic's actual breadth, not a fixed target — a narrow topic might only need 3 map landmarks, a sprawling one might need 7. Don't pad to hit a word count.
- Use markdown headers for the map landmarks/sub-topics so the response is scannable, but don't literally title sections "Plain English Paragraph" or "Vocabulary" — let the structure serve the content.
