from chunkers.chunker import Chunker
import re
import numpy as np
from google.generativeai import embed_content

class SemanticChunker(Chunker):
    def __init__(self, chunk_size=1):
        self.buffer_size = chunk_size
        self.model = 'models/embedding-001'

    @staticmethod
    def create_sentences(text: str):
        """Splits the text into sentences."""
        single_sentences_list = re.split(r'(?<=[.?!])\s+', text)
        sentences = [{'sentence': x, 'index': i} for i, x in enumerate(single_sentences_list)]
        return sentences

    def cosine_similarity(self, a, b):
        """Calculates cosine similarity between two vectors."""
        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        return dot_product / (norm_a * norm_b)

    def calculate_cosine_distances(self, sentences):
        """Calculates the cosine distances between sentence embeddings."""
        distances = []
        for i in range(len(sentences) - 1):
            embedding_current = sentences[i]['combined_sentence_embedding']
            embedding_next = sentences[i + 1]['combined_sentence_embedding']

            # Calculate cosine similarity
            similarity = self.cosine_similarity(embedding_current, embedding_next)

            # Convert to cosine distance
            distance = 1 - similarity
            distances.append(distance)

            # Store distance in the dictionary
            sentences[i]['distance_to_next'] = distance

        return distances, sentences

    def combine_sentences(self, sentences, buffer_size):
        """Combines adjacent sentences based on the buffer size."""
        for i in range(len(sentences)):
            combined_sentence = ''

            # Add previous sentences
            for j in range(i - buffer_size, i):
                if j >= 0:
                    combined_sentence += sentences[j]['sentence'] + ' '

            # Add current sentence
            combined_sentence += sentences[i]['sentence']

            # Add following sentences
            for j in range(i + 1, i + 1 + buffer_size):
                if j < len(sentences):
                    combined_sentence += ' ' + sentences[j]['sentence']

            sentences[i]['combined_sentence'] = combined_sentence

        return sentences

    def create_chunks(self, sentences, distances, breakpoint_percentile_threshold=70):
        """Creates text chunks based on the cosine distances."""
        breakpoint_distance_threshold = np.percentile(distances, breakpoint_percentile_threshold)
        indices_above_thresh = [i for i, x in enumerate(distances) if x > breakpoint_distance_threshold]

        start_index = 0
        chunks = []

        # Iterate through the breakpoints to slice the sentences
        for index in indices_above_thresh:
            end_index = index
            group = sentences[start_index:end_index + 1]
            combined_text = ' '.join([d['sentence'] for d in group])
            chunks.append(combined_text)

            # Update start index for next group
            start_index = index + 1

        # Handle the last group if any sentences remain
        if start_index < len(sentences):
            combined_text = ' '.join([d['sentence'] for d in sentences[start_index:]])
            chunks.append(combined_text)

        return chunks

    def chunk(self, text: str):
        """Main function to chunk text based on semantic similarity."""
        sentences = self.create_sentences(text)
        sentences = self.combine_sentences(sentences, self.buffer_size)

        # Collect combined sentences for embedding generation
        combined_sentences = [x['combined_sentence'] for x in sentences]

        try:
            # Generate embeddings (synchronous)
            embeddings = []
            for sentence in combined_sentences:
                result = embed_content(model=self.model, content=sentence, task_type="SEMANTIC_SIMILARITY")
                if 'embedding' in result:
                    embeddings.append(result['embedding'])
                else:
                    raise ValueError(f"Embedding not found in API response for sentence: {sentence}")

            if len(embeddings) != len(sentences):
                raise ValueError("Mismatch between number of embeddings and sentences.")

            # Assign embeddings to sentences
            for i, sentence in enumerate(sentences):
                sentence['combined_sentence_embedding'] = embeddings[i]

            # Calculate distances and create chunks
            distances, sentences = self.calculate_cosine_distances(sentences)
            return self.create_chunks(sentences, distances)

        except Exception as e:
            import traceback
            print("Failed to generate embeddings or chunk the text")
            print(traceback.format_exc())
            return []
