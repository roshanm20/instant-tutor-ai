# AI EdTech MVP - Video Content Processing Pipeline
# Complete implementation for extracting knowledge from course videos

import os
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import asyncio
from pathlib import Path

# Video processing imports
try:
    import cv2
    import moviepy.editor as mp
    from moviepy.video.io.VideoFileClip import VideoFileClip
    import speech_recognition as sr
    import whisper
    VIDEO_PROCESSING_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Video processing dependencies not available: {e}")
    VIDEO_PROCESSING_AVAILABLE = False
    # Create dummy classes for demo mode
    class VideoFileClip:
        def __init__(self, *args, **kwargs):
            pass
        def close(self):
            pass
        @property
        def duration(self):
            return 300  # 5 minutes demo
        @property
        def audio(self):
            return None

# Text processing imports
try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.document_loaders import TextLoader
    LANGCHAIN_AVAILABLE = True
except ImportError:
    print("Warning: LangChain not available, using simple text splitter")
    LANGCHAIN_AVAILABLE = False
    # Simple text splitter fallback
    class RecursiveCharacterTextSplitter:
        def __init__(self, chunk_size=1000, chunk_overlap=200, **kwargs):
            self.chunk_size = chunk_size
            self.chunk_overlap = chunk_overlap
        def split_text(self, text):
            chunks = []
            for i in range(0, len(text), self.chunk_size - self.chunk_overlap):
                chunks.append(text[i:i + self.chunk_size])
            return chunks

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    print("Warning: Sentence Transformers not available")
    SENTENCE_TRANSFORMERS_AVAILABLE = False

try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    print("Warning: Tiktoken not available")
    TIKTOKEN_AVAILABLE = False

# Vector database imports
try:
    import pinecone
    PINECONE_AVAILABLE = True
except Exception as e:
    print(f"Warning: Pinecone not available: {e}")
    PINECONE_AVAILABLE = False

try:
    import weaviate
    WEAVIATE_AVAILABLE = True
except ImportError:
    print("Warning: Weaviate not available")
    WEAVIATE_AVAILABLE = False

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    print("Warning: OpenAI not available")
    OPENAI_AVAILABLE = False

# Utilities
import pandas as pd
import numpy as np
from tqdm import tqdm
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class VideoSegment:
    """Represents a processed video segment with metadata"""
    id: str
    start_time: float
    end_time: float
    transcript: str
    visual_features: Optional[List[float]] = None
    embedding: Optional[List[float]] = None
    metadata: Optional[Dict[str, Any]] = None

class VideoProcessor:
    """Handles video processing, transcript extraction, and visual analysis"""
    
    def __init__(self, whisper_model: str = "base"):
        """Initialize video processor with Whisper model for transcription"""
        if VIDEO_PROCESSING_AVAILABLE:
            self.whisper_model = whisper.load_model(whisper_model)
            self.recognizer = sr.Recognizer()
        else:
            self.whisper_model = None
            self.recognizer = None
        
    def extract_audio(self, video_path: str, audio_path: str) -> bool:
        """Extract audio from video file"""
        if not VIDEO_PROCESSING_AVAILABLE:
            logger.info("Video processing not available, returning demo mode")
            return True
        try:
            video = VideoFileClip(video_path)
            audio = video.audio
            audio.write_audiofile(audio_path, verbose=False, logger=None)
            video.close()
            audio.close()
            return True
        except Exception as e:
            logger.error(f"Error extracting audio: {e}")
            return False
    
    def transcribe_audio(self, audio_path: str) -> Dict[str, Any]:
        """Transcribe audio using Whisper with timestamps"""
        if not VIDEO_PROCESSING_AVAILABLE or not self.whisper_model:
            logger.info("Whisper not available, returning demo transcript")
            return {
                "text": "This is a demo transcript for testing purposes.",
                "segments": [
                    {"start": 0, "end": 60, "text": "Demo segment 1"},
                    {"start": 60, "end": 120, "text": "Demo segment 2"}
                ]
            }
        try:
            result = self.whisper_model.transcribe(
                audio_path,
                word_timestamps=True,
                verbose=False
            )
            return result
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            return {}
    
    def extract_key_frames(self, video_path: str, interval: int = 30) -> List[np.ndarray]:
        """Extract key frames from video at specified intervals"""
        if not VIDEO_PROCESSING_AVAILABLE:
            logger.info("OpenCV not available, returning empty frames list")
            return []
        try:
            cap = cv2.VideoCapture(video_path)
            frames = []
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            frame_interval = int(fps * interval)  # Extract frame every 'interval' seconds
            frame_count = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                    
                if frame_count % frame_interval == 0:
                    # Convert BGR to RGB
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frames.append(frame_rgb)
                
                frame_count += 1
            
            cap.release()
            return frames
        except Exception as e:
            logger.error(f"Error extracting key frames: {e}")
            return []
    
    def segment_video(self, video_path: str, segment_duration: int = 300) -> List[VideoSegment]:
        """Process video into segments with transcripts and visual features"""
        logger.info(f"Processing video: {video_path}")
        
        # Extract audio
        audio_path = video_path.replace('.mp4', '_audio.wav')
        if not self.extract_audio(video_path, audio_path):
            logger.error("Failed to extract audio")
            return []
        
        # Transcribe audio
        transcription = self.transcribe_audio(audio_path)
        if not transcription:
            logger.error("Failed to transcribe audio")
            return []
        
        # Extract key frames
        key_frames = self.extract_key_frames(video_path)
        
        # Create segments
        segments = []
        video = VideoFileClip(video_path)
        total_duration = video.duration
        
        for i in range(0, int(total_duration), segment_duration):
            start_time = i
            end_time = min(i + segment_duration, total_duration)
            
            # Extract transcript for this segment
            segment_transcript = self._extract_segment_transcript(
                transcription, start_time, end_time
            )
            
            segment = VideoSegment(
                id=f"{Path(video_path).stem}_segment_{i//segment_duration}",
                start_time=start_time,
                end_time=end_time,
                transcript=segment_transcript,
                metadata={
                    "video_path": video_path,
                    "duration": end_time - start_time,
                    "key_frames_count": len(key_frames)
                }
            )
            segments.append(segment)
        
        video.close()
        
        # Clean up audio file
        os.remove(audio_path)
        
        logger.info(f"Created {len(segments)} segments from video")
        return segments
    
    def _extract_segment_transcript(self, transcription: Dict, start_time: float, end_time: float) -> str:
        """Extract transcript text for a specific time segment"""
        segment_text = ""
        
        if 'segments' in transcription:
            for segment in transcription['segments']:
                segment_start = segment.get('start', 0)
                segment_end = segment.get('end', 0)
                
                # Check if segment overlaps with our time range
                if segment_start < end_time and segment_end > start_time:
                    segment_text += segment.get('text', '') + " "
        
        return segment_text.strip()

class TextChunker:
    """Handles intelligent text chunking for optimal embedding generation"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """Initialize text chunker with specified parameters"""
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", "! ", "? ", " ", ""]
        )
    
    def chunk_transcript(self, transcript: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Split transcript into optimally sized chunks for embedding"""
        if not transcript.strip():
            return []
        
        chunks = self.text_splitter.split_text(transcript)
        
        chunked_docs = []
        for i, chunk in enumerate(chunks):
            if len(chunk.strip()) < 50:  # Skip very small chunks
                continue
                
            chunk_metadata = metadata.copy()
            chunk_metadata.update({
                'chunk_id': i,
                'chunk_length': len(chunk),
                'total_chunks': len(chunks)
            })
            
            chunked_docs.append({
                'text': chunk,
                'metadata': chunk_metadata
            })
        
        return chunked_docs

class EmbeddingGenerator:
    """Generates embeddings for text content using various models"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", openai_api_key: Optional[str] = None):
        """Initialize embedding generator with specified model"""
        self.model_name = model_name
        self.openai_api_key = openai_api_key
        
        if "openai" in model_name.lower() and openai_api_key and OPENAI_AVAILABLE:
            openai.api_key = openai_api_key
            self.model = None
        elif SENTENCE_TRANSFORMERS_AVAILABLE:
            # Use Sentence Transformers for local embeddings
            self.model = SentenceTransformer(model_name)
        else:
            print("Warning: No embedding models available, using demo mode")
            self.model = None
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts"""
        if not self.model and not self.openai_api_key:
            # Demo mode - return random embeddings
            logger.info("No embedding model available, returning demo embeddings")
            return [[0.1] * 384 for _ in texts]  # 384-dimensional demo embeddings
        
        if self.openai_api_key and "openai" in self.model_name.lower() and OPENAI_AVAILABLE:
            return self._generate_openai_embeddings(texts)
        elif self.model:
            return self._generate_local_embeddings(texts)
        else:
            # Fallback to demo embeddings
            logger.info("No embedding model available, returning demo embeddings")
            return [[0.1] * 384 for _ in texts]
    
    def _generate_openai_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using OpenAI API"""
        embeddings = []
        batch_size = 100  # OpenAI batch limit
        
        for i in tqdm(range(0, len(texts), batch_size), desc="Generating OpenAI embeddings"):
            batch = texts[i:i + batch_size]
            
            try:
                response = openai.Embedding.create(
                    input=batch,
                    model="text-embedding-ada-002"
                )
                
                batch_embeddings = [item['embedding'] for item in response['data']]
                embeddings.extend(batch_embeddings)
                
            except Exception as e:
                logger.error(f"Error generating OpenAI embeddings: {e}")
                # Fallback to zero embeddings for failed batch
                embeddings.extend([[0.0] * 1536] * len(batch))
        
        return embeddings
    
    def _generate_local_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using local Sentence Transformers model"""
        try:
            embeddings = self.model.encode(texts, show_progress_bar=True)
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Error generating local embeddings: {e}")
            return []

class PineconeVectorDB:
    """Pinecone vector database implementation for course content"""
    
    def __init__(self, api_key: str, environment: str = "gcp-starter"):
        """Initialize Pinecone connection"""
        if not PINECONE_AVAILABLE:
            logger.warning("Pinecone not available, running in demo mode")
            self.api_key = None
            self.environment = None
            return
        self.api_key = api_key
        self.environment = environment
        pinecone.init(api_key=api_key, environment=environment)
    
    def create_index(self, index_name: str, dimension: int = 384, metric: str = "cosine") -> bool:
        """Create a new Pinecone index"""
        if not PINECONE_AVAILABLE:
            logger.info(f"Demo mode: Would create index {index_name}")
            return True
        try:
            if index_name not in pinecone.list_indexes():
                pinecone.create_index(
                    name=index_name,
                    dimension=dimension,
                    metric=metric,
                    pods=1,
                    replicas=1,
                    pod_type="p1.x1"
                )
                logger.info(f"Created Pinecone index: {index_name}")
            else:
                logger.info(f"Index {index_name} already exists")
            return True
        except Exception as e:
            logger.error(f"Error creating Pinecone index: {e}")
            return False
    
    def upsert_vectors(self, index_name: str, vectors: List[Dict[str, Any]]) -> bool:
        """Upload vectors to Pinecone index"""
        if not PINECONE_AVAILABLE:
            logger.info(f"Demo mode: Would upsert {len(vectors)} vectors to {index_name}")
            return True
        try:
            index = pinecone.Index(index_name)
            
            # Batch upsert for efficiency
            batch_size = 100
            for i in tqdm(range(0, len(vectors), batch_size), desc="Upserting to Pinecone"):
                batch = vectors[i:i + batch_size]
                index.upsert(batch)
            
            logger.info(f"Upserted {len(vectors)} vectors to {index_name}")
            return True
        except Exception as e:
            logger.error(f"Error upserting vectors: {e}")
            return False
    
    def search_similar(self, index_name: str, query_vector: List[float], 
                      top_k: int = 10, filter_dict: Optional[Dict] = None) -> List[Dict]:
        """Search for similar vectors in Pinecone"""
        if not PINECONE_AVAILABLE:
            logger.info(f"Demo mode: Would search {index_name} for {top_k} results")
            return []
        try:
            index = pinecone.Index(index_name)
            
            results = index.query(
                vector=query_vector,
                top_k=top_k,
                filter=filter_dict,
                include_metadata=True
            )
            
            return results.matches
        except Exception as e:
            logger.error(f"Error searching vectors: {e}")
            return []

class WeaviateVectorDB:
    """Weaviate vector database implementation for course content"""
    
    def __init__(self, url: str = "http://localhost:8080", api_key: Optional[str] = None):
        """Initialize Weaviate connection"""
        auth_config = None
        if api_key:
            auth_config = weaviate.AuthApiKey(api_key=api_key)
        
        self.client = weaviate.Client(
            url=url,
            auth_client_secret=auth_config
        )
    
    def create_schema(self, class_name: str = "CourseContent") -> bool:
        """Create Weaviate schema for course content"""
        schema = {
            "class": class_name,
            "description": "Educational course content with video segments",
            "properties": [
                {
                    "name": "content",
                    "dataType": ["text"],
                    "description": "The main content text"
                },
                {
                    "name": "videoPath",
                    "dataType": ["string"],
                    "description": "Path to the source video"
                },
                {
                    "name": "startTime",
                    "dataType": ["number"],
                    "description": "Segment start time in seconds"
                },
                {
                    "name": "endTime",
                    "dataType": ["number"],
                    "description": "Segment end time in seconds"
                },
                {
                    "name": "chunkId",
                    "dataType": ["int"],
                    "description": "Chunk identifier within segment"
                },
                {
                    "name": "courseId",
                    "dataType": ["string"],
                    "description": "Course identifier"
                }
            ],
            "vectorizer": "text2vec-transformers"
        }
        
        try:
            self.client.schema.create_class(schema)
            logger.info(f"Created Weaviate schema for {class_name}")
            return True
        except Exception as e:
            if "already exists" in str(e):
                logger.info(f"Schema {class_name} already exists")
                return True
            logger.error(f"Error creating schema: {e}")
            return False
    
    def add_data(self, class_name: str, data_objects: List[Dict[str, Any]]) -> bool:
        """Add data objects to Weaviate"""
        try:
            with self.client.batch as batch:
                batch.batch_size = 100
                
                for obj in tqdm(data_objects, desc="Adding to Weaviate"):
                    batch.add_data_object(
                        data_object=obj,
                        class_name=class_name
                    )
            
            logger.info(f"Added {len(data_objects)} objects to Weaviate")
            return True
        except Exception as e:
            logger.error(f"Error adding data to Weaviate: {e}")
            return False
    
    def search_semantic(self, class_name: str, query: str, limit: int = 10) -> List[Dict]:
        """Perform semantic search in Weaviate"""
        try:
            result = (
                self.client.query
                .get(class_name, ["content", "videoPath", "startTime", "endTime", "courseId"])
                .with_near_text({"concepts": [query]})
                .with_limit(limit)
                .with_additional(["certainty", "distance"])
                .do()
            )
            
            return result["data"]["Get"][class_name]
        except Exception as e:
            logger.error(f"Error performing semantic search: {e}")
            return []

class CourseContentProcessor:
    """Main class orchestrating the entire course content processing pipeline"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize with configuration parameters"""
        self.config = config
        self.video_processor = VideoProcessor(config.get("whisper_model", "base"))
        self.text_chunker = TextChunker(
            chunk_size=config.get("chunk_size", 1000),
            chunk_overlap=config.get("chunk_overlap", 200)
        )
        self.embedding_generator = EmbeddingGenerator(
            model_name=config.get("embedding_model", "all-MiniLM-L6-v2"),
            openai_api_key=config.get("openai_api_key")
        )
        
        # Initialize vector database based on config
        if config.get("vector_db") == "pinecone":
            self.vector_db = PineconeVectorDB(
                api_key=config["pinecone_api_key"],
                environment=config.get("pinecone_environment", "gcp-starter")
            )
        else:
            self.vector_db = WeaviateVectorDB(
                url=config.get("weaviate_url", "http://localhost:8080"),
                api_key=config.get("weaviate_api_key")
            )
    
    async def process_course_videos(self, video_paths: List[str], course_id: str) -> bool:
        """Process multiple course videos and store in vector database"""
        logger.info(f"Processing {len(video_paths)} videos for course {course_id}")
        
        all_vectors = []
        all_data_objects = []
        
        for video_path in video_paths:
            logger.info(f"Processing video: {video_path}")
            
            # Extract video segments
            segments = self.video_processor.segment_video(video_path)
            
            for segment in segments:
                if not segment.transcript:
                    continue
                
                # Chunk the transcript
                chunks = self.text_chunker.chunk_transcript(
                    segment.transcript,
                    {
                        "video_path": video_path,
                        "start_time": segment.start_time,
                        "end_time": segment.end_time,
                        "segment_id": segment.id,
                        "course_id": course_id
                    }
                )
                
                # Generate embeddings
                texts = [chunk["text"] for chunk in chunks]
                if texts:
                    embeddings = self.embedding_generator.generate_embeddings(texts)
                    
                    # Prepare data for vector database
                    for chunk, embedding in zip(chunks, embeddings):
                        if self.config.get("vector_db") == "pinecone":
                            vector_data = {
                                "id": f"{segment.id}_chunk_{chunk['metadata']['chunk_id']}",
                                "values": embedding,
                                "metadata": {
                                    **chunk["metadata"],
                                    "content": chunk["text"]
                                }
                            }
                            all_vectors.append(vector_data)
                        else:
                            # Weaviate format
                            data_object = {
                                "content": chunk["text"],
                                "videoPath": video_path,
                                "startTime": segment.start_time,
                                "endTime": segment.end_time,
                                "chunkId": chunk["metadata"]["chunk_id"],
                                "courseId": course_id
                            }
                            all_data_objects.append(data_object)
        
        # Store in vector database
        if self.config.get("vector_db") == "pinecone":
            index_name = f"course-{course_id}".lower().replace("_", "-")
            self.vector_db.create_index(index_name, dimension=len(all_vectors[0]["values"]))
            return self.vector_db.upsert_vectors(index_name, all_vectors)
        else:
            self.vector_db.create_schema("CourseContent")
            return self.vector_db.add_data("CourseContent", all_data_objects)
    
    def search_course_content(self, query: str, course_id: str, top_k: int = 10) -> List[Dict]:
        """Search for relevant content based on query"""
        if self.config.get("vector_db") == "pinecone":
            # Generate query embedding
            query_embedding = self.embedding_generator.generate_embeddings([query])[0]
            
            index_name = f"course-{course_id}".lower().replace("_", "-")
            return self.vector_db.search_similar(
                index_name, 
                query_embedding, 
                top_k=top_k,
                filter_dict={"course_id": course_id}
            )
        else:
            return self.vector_db.search_semantic("CourseContent", query, limit=top_k)

# Example usage and configuration
def main():
    """Example implementation of the course content processing pipeline"""
    
    # Configuration
    config = {
        "vector_db": "weaviate",  # or "pinecone"
        "whisper_model": "base",
        "embedding_model": "all-MiniLM-L6-v2",
        "chunk_size": 1000,
        "chunk_overlap": 200,
        "weaviate_url": "http://localhost:8080",
        # "pinecone_api_key": "your-pinecone-api-key",
        # "openai_api_key": "your-openai-api-key"
    }
    
    # Initialize processor
    processor = CourseContentProcessor(config)
    
    # Example course videos
    video_paths = [
        "course_videos/lecture_01.mp4",
        "course_videos/lecture_02.mp4",
        "course_videos/lecture_03.mp4"
    ]
    
    course_id = "math_101"
    
    # Process videos (run this once to set up the knowledge base)
    # asyncio.run(processor.process_course_videos(video_paths, course_id))
    
    # Example search queries
    sample_queries = [
        "What is the derivative of x squared?",
        "Explain integration by parts",
        "How to solve linear equations?",
        "What are the properties of logarithms?"
    ]
    
    print("=== Sample Search Results ===")
    for query in sample_queries:
        print(f"\nQuery: {query}")
        results = processor.search_course_content(query, course_id, top_k=3)
        
        for i, result in enumerate(results[:3]):
            if config.get("vector_db") == "pinecone":
                content = result.metadata.get("content", "")[:200]
                score = result.score
                print(f"  {i+1}. Score: {score:.3f} - {content}...")
            else:
                content = result.get("content", "")[:200]
                certainty = result.get("_additional", {}).get("certainty", 0)
                print(f"  {i+1}. Certainty: {certainty:.3f} - {content}...")

if __name__ == "__main__":
    main()