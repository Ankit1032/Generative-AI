# Cohen’s Kappa in RAG Evaluation

Cohen’s Kappa (κ) is a statistical metric that measures inter-rater agreement for categorical labels while correcting for agreement that might occur by random chance.

In the context of Retrieval-Augmented Generation (RAG), it is primarily used to validate the reliability of your evaluation process — either comparing human raters to each other, comparing a human to an AI "judge," or comparing two different AI models.

## How Cohen's Kappa Works

Unlike simple accuracy, which only looks at the percentage of identical ratings, Kappa adjusts for "lucky" matches.

### Formula

- **Po**: Observed agreement (actual percentage of times raters agreed).
- **Pe**: Expected agreement (the probability they would agree by pure chance based on the distribution of their ratings).

### Scale

Scores range from **-1 to 1**:

- **1**: Perfect agreement.
- **0**: Agreement is no better than random guessing.
- **< 0**: Disagreement is worse than random chance.

## How to Use It in RAG Evaluation

RAG pipelines are complex, and metrics like Ragas (Context Precision, Faithfulness) often use LLMs as judges. Cohen's Kappa helps you trust those judges.

1. **Validate AI Judges (LLM-as-a-Judge)**:  
   Before trusting an LLM to score your RAG output (e.g., "Is this answer faithful to the context?"), have a human rater and the LLM score the same 100 samples. Calculate the Kappa between them. A high score (e.g., >0.8) indicates the LLM is a reliable proxy for the human.

2. **Ensure Ground Truth Quality**:  
   If you have two humans creating your "golden dataset" (ground truth), use Kappa to ensure they agree on what constitutes a "correct" or "relevant" answer. If agreement is low (<0.4), your guidelines for human labelers need to be more specific.

3. **A/B Testing Models**:  
   When swapping a powerful model (GPT-4o) for a cheaper one (Llama-3), run both on the same dataset. A high Kappa suggests the cheaper model can successfully replace the expensive one without changing the system's "judgment".

## General Interpretation Benchmarks

While context matters, common guidelines (Landis & Koch) include:

- **0.81 – 1.00**: Almost perfect agreement  
- **0.61 – 0.80**: Substantial agreement  
- **0.41 – 0.60**: Moderate agreement  
- **< 0.40**: Fair to poor agreement
