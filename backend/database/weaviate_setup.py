# AI EdTech MVP - Weaviate Vector Database Setup
# Complete implementation guide for Weaviate integration

import weaviate
from weaviate.classes.config import Configure, Property, DataType
from typing import List, Dict, Any, Optional
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WeaviateSetup:
    """Complete Weaviate setup and management for AI EdTech MVP"""
    
    def __init__(self, url: str = "http://localhost:8080", api_key: Optional[str] = None):
        """Initialize Weaviate connection"""
        try:
            if api_key:
                # For Weaviate Cloud Services (WCS)
                self.client = weaviate.connect_to_wcs(
                    cluster_url=url,
                    auth_credentials=weaviate.AuthApiKey(api_key)
                )
            else:
                # For local Weaviate instance
                self.client = weaviate.connect_to_local(host=url)
            
            logger.info("Successfully connected to Weaviate")
        except Exception as e:
            logger.error(f"Failed to connect to Weaviate: {e}")
            raise
    
    def create_course_schema(self, collection_name: str = "CourseContent") -> bool:
        """Create Weaviate collection schema for course content"""
        try:
            # Check if collection already exists
            if self.client.collections.exists(collection_name):
                logger.info(f"Collection '{collection_name}' already exists")
                return True
            
            # Create collection with properties
            collection = self.client.collections.create(
                name=collection_name,
                description="Educational course content with video segments and transcripts",
                properties=[
                    Property(
                        name="content",
                        data_type=DataType.TEXT,
                        description="The main content text from video transcript"
                    ),
                    Property(
                        name="courseId",
                        data_type=DataType.TEXT,
                        description="Unique identifier for the course"
                    ),
                    Property(
                        name="videoPath",
                        data_type=DataType.TEXT,
                        description="Path to the source video file"
                    ),
                    Property(
                        name="startTime",
                        data_type=DataType.NUMBER,
                        description="Segment start time in seconds"
                    ),
                    Property(
                        name="endTime",
                        data_type=DataType.NUMBER,
                        description="Segment end time in seconds"
                    ),
                    Property(
                        name="chunkId",
                        data_type=DataType.INT,
                        description="Chunk identifier within video segment"
                    ),
                    Property(
                        name="difficulty",
                        data_type=DataType.TEXT,
                        description="Content difficulty level (beginner, intermediate, advanced)"
                    ),
                    Property(
                        name="topic",
                        data_type=DataType.TEXT,
                        description="Main topic or subject covered"
                    ),
                    Property(
                        name="language",
                        data_type=DataType.TEXT,
                        description="Language of the content (English, Malayalam, etc.)"
                    )
                ],
                # Configure automatic vectorization
                vector_config=Configure.Vectors.text2vec_transformers(
                    source_properties=["content"]
                )
            )
            
            logger.info(f"Successfully created collection: {collection_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating collection: {e}")
            return False
    
    def add_course_data(self, collection_name: str, course_data: List[Dict[str, Any]]) -> bool:
        """Add course content data to Weaviate collection"""
        try:
            collection = self.client.collections.get(collection_name)
            
            # Prepare data objects
            data_objects = []
            for item in course_data:
                data_object = {
                    "content": item.get("content", ""),
                    "courseId": item.get("course_id", ""),
                    "videoPath": item.get("video_path", ""),
                    "startTime": float(item.get("start_time", 0)),
                    "endTime": float(item.get("end_time", 0)),
                    "chunkId": int(item.get("chunk_id", 0)),
                    "difficulty": item.get("difficulty", "intermediate"),
                    "topic": item.get("topic", "general"),
                    "language": item.get("language", "english")
                }
                data_objects.append(data_object)
            
            # Batch insert data
            with collection.batch.dynamic() as batch:
                for obj in data_objects:
                    batch.add_object(obj)
            
            logger.info(f"Successfully added {len(data_objects)} objects to {collection_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding data: {e}")
            return False
    
    def search_course_content(self, collection_name: str, query: str, 
                            course_filter: str = None, limit: int = 10) -> List[Dict]:
        """Search for relevant course content using semantic search"""
        try:
            collection = self.client.collections.get(collection_name)
            
            # Build search query
            search = collection.query.near_text(
                query=query,
                limit=limit,
                return_properties=["content", "courseId", "videoPath", "startTime", "endTime", "topic", "difficulty"],
                return_metadata=["certainty", "distance"]
            )
            
            # Apply course filter if specified
            if course_filter:
                search = search.where(
                    weaviate.classes.query.Filter.by_property("courseId").equal(course_filter)
                )
            
            # Execute search
            results = search.objects
            
            # Process results
            processed_results = []
            for result in results:
                processed_result = {
                    "content": result.properties.get("content", ""),
                    "course_id": result.properties.get("courseId", ""),
                    "video_path": result.properties.get("videoPath", ""),
                    "start_time": result.properties.get("startTime", 0),
                    "end_time": result.properties.get("endTime", 0),
                    "topic": result.properties.get("topic", ""),
                    "difficulty": result.properties.get("difficulty", ""),
                    "certainty": result.metadata.certainty if result.metadata else 0.0,
                    "distance": result.metadata.distance if result.metadata else 1.0
                }
                processed_results.append(processed_result)
            
            return processed_results
            
        except Exception as e:
            logger.error(f"Error searching content: {e}")
            return []
    
    def hybrid_search(self, collection_name: str, query: str, alpha: float = 0.75, 
                     course_filter: str = None, limit: int = 10) -> List[Dict]:
        """Perform hybrid search combining semantic and keyword search"""
        try:
            collection = self.client.collections.get(collection_name)
            
            # Build hybrid search query
            search = collection.query.hybrid(
                query=query,
                alpha=alpha,  # 0.0 = pure keyword, 1.0 = pure semantic
                limit=limit,
                return_properties=["content", "courseId", "videoPath", "startTime", "endTime", "topic"],
                return_metadata=["score"]
            )
            
            # Apply course filter if specified
            if course_filter:
                search = search.where(
                    weaviate.classes.query.Filter.by_property("courseId").equal(course_filter)
                )
            
            # Execute search
            results = search.objects
            
            # Process results
            processed_results = []
            for result in results:
                processed_result = {
                    "content": result.properties.get("content", ""),
                    "course_id": result.properties.get("courseId", ""),
                    "video_path": result.properties.get("videoPath", ""),
                    "start_time": result.properties.get("startTime", 0),
                    "end_time": result.properties.get("endTime", 0),
                    "topic": result.properties.get("topic", ""),
                    "score": result.metadata.score if result.metadata else 0.0
                }
                processed_results.append(processed_result)
            
            return processed_results
            
        except Exception as e:
            logger.error(f"Error performing hybrid search: {e}")
            return []
    
    def get_collection_stats(self, collection_name: str) -> Dict[str, Any]:
        """Get statistics about the collection"""
        try:
            collection = self.client.collections.get(collection_name)
            
            # Get total object count
            total_objects = len(collection.query.fetch_objects().objects)
            
            # Get collection configuration
            config = collection.config.get()
            
            return {
                "total_objects": total_objects,
                "collection_name": config.name,
                "description": config.description,
                "properties_count": len(config.properties),
                "vectorizer": config.vector_config
            }
            
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            return {}
    
    def close_connection(self):
        """Close Weaviate connection"""
        try:
            self.client.close()
            logger.info("Weaviate connection closed")
        except Exception as e:
            logger.error(f"Error closing connection: {e}")

# Docker Compose setup for local Weaviate
def create_docker_compose():
    """Create docker-compose.yml for local Weaviate setup"""
    
    docker_compose_content = """
version: '3.4'
services:
  weaviate:
    command:
    - --host
    - 0.0.0.0
    - --port
    - '8080'
    - --scheme
    - http
    image: cr.weaviate.io/semitechnologies/weaviate:1.25.5
    ports:
    - "8080:8080"
    - "50051:50051"
    environment:
      QUERY_DEFAULTS_LIMIT: 25
      AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: 'true'
      PERSISTENCE_DATA_PATH: '/var/lib/weaviate'
      DEFAULT_VECTORIZER_MODULE: 'text2vec-transformers'
      ENABLE_MODULES: 'text2vec-transformers,generative-openai'
      TRANSFORMERS_INFERENCE_API: 'http://t2v-transformers:8080'
      CLUSTER_HOSTNAME: 'node1'
    volumes:
      - weaviate_data:/var/lib/weaviate

  t2v-transformers:
    image: cr.weaviate.io/semitechnologies/transformers-inference:sentence-transformers-multi-qa-MiniLM-L6-cos-v1
    environment:
      ENABLE_CUDA: '0'
      
volumes:
  weaviate_data:
"""
    
    with open("docker-compose.yml", "w") as f:
        f.write(docker_compose_content)
    
    print("Created docker-compose.yml for Weaviate")
    print("To start Weaviate:")
    print("1. docker-compose up -d")
    print("2. Wait for services to be ready")
    print("3. Access Weaviate at http://localhost:8080")

# Step-by-step setup guide
def setup_weaviate_guide():
    """Complete setup guide for Weaviate in AI EdTech MVP"""
    
    print("=== Weaviate Setup Guide for AI EdTech MVP ===")
    print()
    
    # Step 1: Installation options
    print("STEP 1: Choose Installation Method")
    print("Option A: Local Docker Setup (Recommended for MVP)")
    print("  1. Install Docker and Docker Compose")
    print("  2. Run: create_docker_compose() to generate docker-compose.yml")
    print("  3. Run: docker-compose up -d")
    print("  4. Weaviate available at http://localhost:8080")
    print()
    print("Option B: Weaviate Cloud Services (WCS)")
    print("  1. Sign up at https://console.weaviate.cloud/")
    print("  2. Create cluster and get endpoint URL")
    print("  3. Generate API key")
    print()
    
    # Step 2: Install Python client
    print("STEP 2: Install Python Client")
    print("pip install weaviate-client")
    print()
    
    # Step 3: Connection setup
    print("STEP 3: Connect to Weaviate")
    print("```python")
    print("import weaviate")
    print("")
    print("# Local connection")
    print("client = weaviate.connect_to_local()")
    print("")
    print("# Or WCS connection")
    print("client = weaviate.connect_to_wcs(")
    print("    cluster_url='your-cluster-url.weaviate.cloud',")
    print("    auth_credentials=weaviate.AuthApiKey('your-api-key')")
    print(")")
    print("```")
    print()
    
    # Step 4: Schema creation
    print("STEP 4: Create Collection Schema")
    print("```python")
    print("from weaviate.classes.config import Configure, Property, DataType")
    print("")
    print("collection = client.collections.create(")
    print("    name='CourseContent',")
    print("    properties=[")
    print("        Property(name='content', data_type=DataType.TEXT),")
    print("        Property(name='courseId', data_type=DataType.TEXT),")
    print("        Property(name='videoPath', data_type=DataType.TEXT),")
    print("        Property(name='startTime', data_type=DataType.NUMBER)")
    print("    ],")
    print("    vector_config=Configure.Vectors.text2vec_transformers()")
    print(")")
    print("```")
    print()
    
    # Step 5: Data ingestion
    print("STEP 5: Add Course Data")
    print("```python")
    print("collection = client.collections.get('CourseContent')")
    print("")
    print("with collection.batch.dynamic() as batch:")
    print("    batch.add_object({")
    print("        'content': 'Mathematics lecture content...',")
    print("        'courseId': 'math_101',")
    print("        'videoPath': 'lectures/lecture1.mp4',")
    print("        'startTime': 120.5")
    print("    })")
    print("```")
    print()
    
    # Step 6: Search functionality
    print("STEP 6: Search Course Content")
    print("```python")
    print("# Semantic search")
    print("results = collection.query.near_text(")
    print("    query='What is calculus?',")
    print("    limit=5")
    print(").objects")
    print("")
    print("# Hybrid search (semantic + keyword)")
    print("results = collection.query.hybrid(")
    print("    query='integration by parts',")
    print("    alpha=0.75,")
    print("    limit=5")
    print(").objects")
    print("```")
    print()

# Cost comparison for Kerala market
def weaviate_cost_analysis():
    """Compare Weaviate costs for Kerala edtech market"""
    
    print("=== Weaviate Cost Analysis for Kerala EdTech ===")
    print()
    
    options = {
        "Local Deployment": {
            "monthly_cost": "₹2,000-5,000",
            "infrastructure": "Self-managed server/cloud",
            "scalability": "Manual scaling required",
            "suitable_for": "MVP, small scale deployment",
            "pros": ["Full control", "No vendor lock-in", "Cost effective"],
            "cons": ["Requires DevOps expertise", "Maintenance overhead"]
        },
        "Weaviate Cloud (Sandbox)": {
            "monthly_cost": "$0",
            "infrastructure": "Managed cloud service",
            "scalability": "Limited resources",
            "suitable_for": "Testing and prototyping",
            "pros": ["Free tier", "Zero setup", "Managed service"],
            "cons": ["Limited resources", "Not for production"]
        },
        "Weaviate Cloud (Standard)": {
            "monthly_cost": "$25-100+ USD",
            "infrastructure": "Fully managed",
            "scalability": "Auto-scaling available",
            "suitable_for": "Production deployment",
            "pros": ["Fully managed", "Auto-scaling", "High availability"],
            "cons": ["Higher cost", "Vendor dependency"]
        }
    }
    
    for option, details in options.items():
        print(f"{option}:")
        for key, value in details.items():
            if isinstance(value, list):
                print(f"  {key.replace('_', ' ').title()}: {', '.join(value)}")
            else:
                print(f"  {key.replace('_', ' ').title()}: {value}")
        print()
    
    print("Recommendation for Kerala Market:")
    print("• Start with Local Deployment for MVP (₹2,000-5,000/month)")
    print("• Use WCS Sandbox for development and testing")
    print("• Scale to WCS Standard when reaching 1000+ concurrent users")
    print("• Consider hybrid approach: Local primary + WCS backup")
    print()

if __name__ == "__main__":
    setup_weaviate_guide()
    create_docker_compose()
    weaviate_cost_analysis()