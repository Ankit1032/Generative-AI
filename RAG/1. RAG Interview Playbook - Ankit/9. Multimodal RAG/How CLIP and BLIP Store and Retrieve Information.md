# How CLIP and BLIP Store and Retrieve Information

### How Information is Stored (Embedding)
The models use a specialized **image encoder** (like a Vision Transformer or ResNet) to process the image.

*   **Decomposition**: The image is broken down into small patches (e.g., $32 \times 32$ pixels).
*   **Transformation**: These patches are converted into a single high-dimensional vector (often 512 numbers) that captures the "essence" of the image—such as objects, colors, and textures—rather than just individual pixels.
*   **Shared Space**: During training, these models are taught to place images and their corresponding text descriptions very close to each other in a shared **latent space**. If an image and text are related (e.g., a photo of a dog and the phrase "a fluffy dog"), their vectors will point in nearly the same direction.

### How Information is Retrieved (Querying)
When you enter a search query, the system follows these steps:

1.  **Text Encoding**: Your query is passed through a **text encoder**, which converts it into a vector in the same 512-dimensional space as the images.
2.  **Similarity Matching**: The system calculates the **cosine similarity** (the mathematical angle) between your query vector and all the stored image vectors in its database.
3.  **Ranking**: Images with vectors closest to your query's vector are ranked highest and returned as results.

### Key Differences Between CLIP and BLIP
*   **CLIP**: Focuses primarily on "global" matching (the whole image vs. the whole text). It is excellent for fast, broad searches but can sometimes struggle with complex logic like "a man *not* wearing a hat".
*   **BLIP**: Adds a **cross-attention mechanism**, allowing the text and image parts of the model to "talk" to each other more deeply during the encoding process. This makes it better at detailed tasks like **image captioning** or answering specific questions about an image (VQA).
