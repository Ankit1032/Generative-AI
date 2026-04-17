# Prompt Regression Testing

Prompt regression testing is a quality assurance process used to ensure that changes to AI prompts, model versions, or configurations do not degrade the existing behavior, safety, or quality of an AI application. Unlike traditional code testing, it accounts for the **probabilistic nature** of LLMs by focusing on **semantic stability** rather than exact text matching.

## How to Do Prompt Regression Testing

1. **Establish a "Golden Dataset"**  
   - Curate **20–30** representative input-output pairs that define the "ground truth" or desired behavior for your application.  
   - Include high-priority user queries, complex edge cases, and past failure points (bugs) to ensure they remain fixed.

2. **Define Evaluation Metrics (The "Contract")**  
   - **Deterministic Checks**: Validate structural requirements such as valid JSON formatting, presence of mandatory keys, or character length limits.  
   - **Fuzzy/Semantic Checks**: Use semantic similarity (cosine similarity) to check if the new output's meaning matches the baseline.  
   - **Constraint Checks**: Ensure the absence of forbidden phrases or restricted topics (e.g., PII or competitor mentions).

3. **Implement "LLM-as-a-Judge"**  
   - Use a more capable model (e.g., GPT-4o) to grade the performance of your production model.  
   - Provide the "judge" with a specific rubric to score responses on a scale (e.g., 1–5) for tone, helpfulness, and accuracy.

4. **Establish Baseline & Compare**  
   - Run your current "stable" prompt through the test suite to get a baseline performance score.  
   - Apply your prompt changes and re-run the suite. A regression is detected if scores drop below a defined tolerance threshold (e.g., semantic similarity falls below **0.8**).

5. **Automate in CI/CD**  
   - Integrate tests into your deployment pipeline using tools like **promptfoo**, **LangSmith**, or **testRigor**.  
   - Configure release gates to automatically block deployments if critical tests fail or if the overall pass rate drops below a certain percentage (e.g., **90%**).
