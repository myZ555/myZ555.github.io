---
name: disease-summary
description: Build concise disease summary tables from an existing Disease Index and the relevant chapters in the user's medical notes. Use when the user asks to summarize or consolidate one or more diseases from the Index.
---

# Disease Summary

1. **Parse the requested specialty and disease/topic.**
   Respect the user's requested scope.

2. **Locate the relevant Disease Index.**
   Use the Index to identify the requested disease and its associated categories/subcategories.
   Treat the Index as the authoritative definition of what diseases/topics belong to the requested scope.

3. **Map Index entries to source chapters.**
   Search the corresponding specialty's `Summary` and `PocketBook` materials for the relevant disease names, synonyms, and associated topics.
   Do not scan unrelated chapters unnecessarily.

4. **Collect and synthesize the relevant material.**
   Extract clinically important information from the identified chapters.
   Summarize rather than reproduce the source text.

5. **Prioritize high-yield clinical information.**
   Include, when applicable:
   - Definition / classification
   - Etiology / risk factors
   - Clinical features
   - Diagnosis / diagnostic criteria
   - Differential diagnosis
   - Investigations
   - Management
   - Complications
   - Important clinical distinctions / pearls

   Adapt the fields to the disease. Do not force irrelevant categories into the table.

6. **Produce a concise Markdown summary table.**
   Prefer a high-density table suitable for quick review.
   Use multiple tables when a single table would become excessively wide.

7. **Preserve source fidelity.**
   Do not invent information or silently supplement missing information with external knowledge.
   If an important item is not found in the available materials, mark it as `未提及` when appropriate.

8. **Handle conflicting information explicitly.**
   If relevant source chapters disagree, briefly flag the discrepancy rather than silently choosing one version.

9. **Keep the output concise.**
   The result should function as a quick-reference clinical summary, not a rewritten textbook chapter.

10. **Save only when requested.**
    Follow the user's requested output location and filename. Do not overwrite existing files unless explicitly instructed.