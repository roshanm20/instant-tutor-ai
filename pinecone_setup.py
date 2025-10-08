# AI EdTech MVP - Pinecone Vector Database Setup
# Step-by-step implementation guide for Pinecone integration

import os
import pinecone
from pinecone import Pinecone, ServerlessSpec
from typing import List, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PineconeSetup:
    """Complete Pinecone setup and management for AI EdTech MVP"""
    
    def __init__(self, api_key: str):
        """Initialize Pinecone with API key"""
        self.api_key = api_key
        self.pc = Pinecone(api_key=api_key)
    
    def create_index(self, index_name: str, dimension: int = 1536, metric: str = "cosine") -> bool:
        """Create a new Pinecone index with serverless configuration"""
        try:
            # Check if index already exists
            existing_indexes = [index.name for index in self.pc.list_indexes()]
            
            if index_name in existing_indexes:
                logger.info(f"Index '{index_name}' already exists")
                return True
            
            # Create serverless index (recommended for MVP)
            self.pc.create_index(
                name=index_name,
                dimension=dimension,
                metric=metric,
                spec=ServerlessSpec(
                    cloud='aws',
                    region='us-east-1'  # Choose region closest to your users
                )
            )
            
            logger.info(f"Successfully created index: {index_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating index: {e}")
            return False
    
    def upsert_course_content(self, index_name: str, course_data: List[Dict[str, Any]]) -> bool:
        """Upload course content vectors to Pinecone index"""
        try:
            index = self.pc.Index(index_name)
            
            # Prepare vectors in Pinecone format
            vectors = []
            for item in course_data:
                vector_data = {
                    "id": item["id"],
                    "values": item["embedding"],
                    "metadata": {
                        "content": item["content"],
                        "course_id": item["course_id"],
                        "video_path": item.get("video_path", ""),
                        "start_time": item.get("start_time", 0),
                        "end_time": item.get("end_time", 0),
                        "chunk_id": item.get("chunk_id", 0)
                    }
                }
                vectors.append(vector_data)
            
            # Batch upsert (recommended batch size: 100)
            batch_size = 100
            for i in range(0, len(vectors), batch_size):
                batch = vectors[i:i + batch_size]
                index.upsert(vectors=batch)
                logger.info(f"Upserted batch {i//batch_size + 1}/{len(vectors)//batch_size + 1}")
            
            logger.info(f"Successfully upserted {len(vectors)} vectors to {index_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error upserting vectors: {e}")
            return False
    
    def search_course_content(self, index_name: str, query_vector: List[float], 
                            course_filter: str = None, top_k: int = 10) -> List[Dict]:
        """Search for similar content in the course knowledge base"""
        try:
            index = self.pc.Index(index_name)
            
            # Prepare filter if course_id is specified
            filter_dict = None
            if course_filter:
                filter_dict = {"course_id": {"$eq": course_filter}}
            
            # Perform similarity search
            results = index.query(
                vector=query_vector,
                top_k=top_k,
                filter=filter_dict,
                include_metadata=True
            )
            
            # Process and return results
            processed_results = []
            for match in results.matches:
                result = {
                    "id": match.id,
                    "score": match.score,
                    "content": match.metadata.get("content", ""),
                    "course_id": match.metadata.get("course_id", ""),
                    "video_path": match.metadata.get("video_path", ""),
                    "start_time": match.metadata.get("start_time", 0),
                    "end_time": match.metadata.get("end_time", 0)
                }
                processed_results.append(result)
            
            return processed_results
            
        except Exception as e:
            logger.error(f"Error searching vectors: {e}")
            return []
    
    def get_index_stats(self, index_name: str) -> Dict[str, Any]:
        """Get statistics about the index"""
        try:
            index = self.pc.Index(index_name)
            stats = index.describe_index_stats()
            return {
                "total_vectors": stats.total_vector_count,
                "dimension": stats.dimension,
                "index_fullness": stats.index_fullness,
                "namespaces": stats.namespaces
            }
        except Exception as e:
            logger.error(f"Error getting index stats: {e}")
            return {}

# Step-by-step implementation guide
def setup_pinecone_for_edtech():
    """Complete setup guide for Pinecone in AI EdTech MVP"""
    
    print("=== Pinecone Setup Guide for AI EdTech MVP ===")
    print()
    
    # Step 1: Environment Setup
    print("STEP 1: Environment Setup")
    print("1. Sign up for Pinecone account at https://app.pinecone.io/")
    print("2. Create API key from dashboard")
    print("3. Set environment variable: PINECONE_API_KEY=your_api_key")
    print("4. Install required packages: pip install pinecone-client")
    print()
    
    # Step 2: Initialize Pinecone
    print("STEP 2: Initialize Pinecone Connection")
    print("```python")
    print("import os")
    print("from pinecone import Pinecone")
    print("")
    print("api_key = os.getenv('PINECONE_API_KEY')")
    print("pc = Pinecone(api_key=api_key)")
    print("```")
    print()
    
    # Step 3: Create Index
    print("STEP 3: Create Vector Index")
    print("```python")
    print("# For OpenAI embeddings (dimension = 1536)")
    print("pc.create_index(")
    print("    name='edtech-course-content',")
    print("    dimension=1536,")
    print("    metric='cosine',")
    print("    spec=ServerlessSpec(cloud='aws', region='us-east-1')")
    print(")")
    print("```")
    print()
    
    # Step 4: Prepare Data
    print("STEP 4: Prepare Course Data")
    print("```python")
    print("course_data = [")
    print("    {")
    print("        'id': 'course1_segment1_chunk1',")
    print("        'embedding': [0.1, 0.2, ...],  # 1536 dimensions")
    print("        'content': 'Course content text...',")
    print("        'course_id': 'math_101',")
    print("        'video_path': 'lectures/lecture1.mp4',")
    print("        'start_time': 120.5,")
    print("        'end_time': 180.3")
    print("    }")
    print("]")
    print("```")
    print()
    
    # Step 5: Upload Data
    print("STEP 5: Upload Vectors")
    print("```python")
    print("index = pc.Index('edtech-course-content')")
    print("index.upsert(vectors=course_data)")
    print("```")
    print()
    
    # Step 6: Search
    print("STEP 6: Search for Relevant Content")
    print("```python")
    print("# Generate query embedding")
    print("query_embedding = generate_embedding('What is calculus?')")
    print("")
    print("# Search in Pinecone")
    print("results = index.query(")
    print("    vector=query_embedding,")
    print("    top_k=5,")
    print("    filter={'course_id': 'math_101'},")
    print("    include_metadata=True")
    print(")")
    print("```")
    print()

# Cost estimation for Kerala/Indian market
def estimate_pinecone_costs():
    """Estimate Pinecone costs for Kerala edtech startup"""
    
    print("=== Pinecone Cost Estimation for Kerala EdTech Startup ===")
    print()
    
    costs = {
        "Starter Plan": {
            "monthly_cost": "$0",
            "storage": "100K vectors",
            "queries": "10K/month",
            "suitable_for": "MVP, 1-2 courses"
        },
        "Standard Plan": {
            "monthly_cost": "$70",
            "storage": "5M vectors", 
            "queries": "10M/month",
            "suitable_for": "10-20 courses, 1000 students"
        },
        "Enterprise Plan": {
            "monthly_cost": "$600+",
            "storage": "100M+ vectors",
            "queries": "Unlimited",
            "suitable_for": "100+ courses, 10K+ students"
        }
    }
    
    for plan, details in costs.items():
        print(f"{plan}:")
        for key, value in details.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
        print()
    
    print("Recommendations for Kerala market:")
    print("• Start with Starter plan for MVP (Free)")
    print("• Scale to Standard plan when reaching 1000+ students")
    print("• Consider hybrid approach: Pinecone + local vector DB")
    print("• Budget ₹5,000-25,000/month for vector database costs")
    print()

if __name__ == "__main__":
    setup_pinecone_for_edtech()
    estimate_pinecone_costs()