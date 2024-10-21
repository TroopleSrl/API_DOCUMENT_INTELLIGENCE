from chunkers.chunker import Chunker
import re
import numpy as np
from google.generativeai import embed_content_async

class SemanticChunker(Chunker):
    def __init__(self, chunk_size = 1):
        self.buffer_size = chunk_size
        self.model = 'models/embedding-001'

    @staticmethod
    def create_sentences(text: str):
        single_sentences_list = re.split(r'(?<=[.?!])\s+', text)
        sentences = [{'sentence': x, 'index' : i} for i, x in enumerate(single_sentences_list)]
        return sentences
    
    def cosine_similariity(self, a, b):
        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        return dot_product / (norm_a * norm_b)
    
    def calculate_cosine_distances(self, sentences):
        distances = []
        for i in range(len(sentences) - 1):
            embedding_current = sentences[i]['combined_sentence_embedding']
            embedding_next = sentences[i + 1]['combined_sentence_embedding']
            
            # Calculate cosine similarity
            similarity = self.cosine_similarity(embedding_current, embedding_next)
            
            # Convert to cosine distance
            distance = 1 - similarity

            # Append cosine distance to the list
            distances.append(distance)

            # Store distance in the dictionary
            sentences[i]['distance_to_next'] = distance

        # Optionally handle the last sentence
        # sentences[-1]['distance_to_next'] = None  # or a default value

        return distances, sentences

    def combine_sentences(self, sentences, buffer_size):
        # Go through each sentence dict
        for i in range(len(sentences)):

            # Create a string that will hold the sentences which are joined
            combined_sentence = ''

            # Add sentences before the current one, based on the buffer size.
            for j in range(i - buffer_size, i):
                # Check if the index j is not negative (to avoid index out of range like on the first one)
                if j >= 0:
                    # Add the sentence at index j to the combined_sentence string
                    combined_sentence += sentences[j]['sentence'] + ' '

            # Add the current sentence
            combined_sentence += sentences[i]['sentence']

            # Add sentences after the current one, based on the buffer size
            for j in range(i + 1, i + 1 + buffer_size):
                # Check if the index j is within the range of the sentences list
                if j < len(sentences):
                    # Add the sentence at index j to the combined_sentence string
                    combined_sentence += ' ' + sentences[j]['sentence']

            # Then add the whole thing to your dict
            # Store the combined sentence in the current sentence dict
            sentences[i]['combined_sentence'] = combined_sentence

        return sentences

    def create_chunks(self, sentences, distances, breakpoint_percentile_threshold = 70):
        breakpoint_distance_threshold = np.percentile(distances, breakpoint_percentile_threshold)

        indices_above_thresh = [i for i, x in enumerate(distances) if x > breakpoint_distance_threshold] # The indices of those breakpoints on your list

        # Initialize the start index
        start_index = 0

        # Create a list to hold the grouped sentences
        chunks = []

        # Iterate through the breakpoints to slice the sentences
        for index in indices_above_thresh:
            # The end index is the current breakpoint
            end_index = index

            # Slice the sentence_dicts from the current start index to the end index
            group = sentences[start_index:end_index + 1]
            combined_text = ' '.join([d['sentence'] for d in group])
            chunks.append(combined_text)
            
            # Update the start index for the next group
            start_index = index + 1

        # The last group, if any sentences remain
        if start_index < len(sentences):
            combined_text = ' '.join([d['sentence'] for d in sentences[start_index:]])
            chunks.append(combined_text)

        return chunks\
        
    async def chunk(self, text: str):
        sentences = self.create_sentences(text)
        sentences = self.combine_sentences(sentences, self.buffer_size)

        # Collect all combined sentences
        combined_sentences = [x['combined_sentence'] for x in sentences]
        
        # Generate embeddings for all sentences in a single call
        try:
            embeddings = []
            for sentence in combined_sentences:
                # Get the embedding and check its structure
                result = await embed_content_async(model=self.model, content=sentence, task_type="SEMANTIC_SIMILARITY")
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
