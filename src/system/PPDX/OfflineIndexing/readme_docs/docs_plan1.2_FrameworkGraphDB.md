## 🏗️ **Framework & Database Options cho Knowledge Graph**

### **1. Graph Database Options**

#### **🥇 Neo4j (Recommended)**
```python
from neo4j import GraphDatabase
from py2neo import Graph, Node, Relationship

class Neo4jKnowledgeGraph:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="password"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.graph = Graph(uri, auth=(user, password))
    
    def create_phrase_node(self, phrase_id: str, text: str, embedding: list):
        query = """
        CREATE (p:Phrase {
            id: $phrase_id,
            text: $text,
            normalized_text: $normalized_text,
            embedding: $embedding
        })
        RETURN p
        """
        self.graph.run(query, 
                      phrase_id=phrase_id, 
                      text=text, 
                      normalized_text=text.lower(),
                      embedding=embedding)
    
    def create_passage_node(self, passage_id: str, text: str, source: str):
        query = """
        CREATE (p:Passage {
            id: $passage_id,
            text: $text,
            source: $source
        })
        RETURN p
        """
        self.graph.run(query, passage_id=passage_id, text=text, source=source)
    
    def create_relation_edge(self, subject_id: str, object_id: str, predicate: str, confidence: float):
        query = """
        MATCH (s:Phrase {id: $subject_id})
        MATCH (o:Phrase {id: $object_id})
        CREATE (s)-[:RELATION {
            predicate: $predicate,
            confidence: $confidence
        }]->(o)
        """
        self.graph.run(query, 
                      subject_id=subject_id, 
                      object_id=object_id,
                      predicate=predicate,
                      confidence=confidence)
```

**Neo4j Advantages:**
- ✅ **Mature ecosystem** với rich tooling
- ✅ **Cypher query language** - rất powerful cho graph queries
- ✅ **Built-in dashboard** (Neo4j Browser)
- ✅ **APOC procedures** cho advanced operations
- ✅ **Vector search support** (từ version 5.x)

#### **🥈 NebulaGraph (High Performance)**
```python
from nebula3.gclient.net import ConnectionPool
from nebula3.Config import Config

class NebulaKnowledgeGraph:
    def __init__(self):
        config = Config()
        self.pool = ConnectionPool()
        self.pool.init([('127.0.0.1', 9669)], config)
        
    def create_schema(self):
        session = self.pool.get_session('user', 'password')
        
        # Create space
        session.execute('CREATE SPACE IF NOT EXISTS knowledge_graph(vid_type=FIXED_STRING(32))')
        session.execute('USE knowledge_graph')
        
        # Create tags (node types)
        session.execute('''
        CREATE TAG IF NOT EXISTS Phrase(
            text string,
            normalized_text string,
            embedding string
        )
        ''')
        
        session.execute('''
        CREATE TAG IF NOT EXISTS Passage(
            text string,
            source string
        )
        ''')
        
        # Create edges
        session.execute('''
        CREATE EDGE IF NOT EXISTS RELATION(
            predicate string,
            confidence double
        )
        ''')
```

#### **🥉 Amazon Neptune (Cloud-native)**
```python
from gremlin_python.driver import client
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.anonymous_traversal import traversal

class NeptuneKnowledgeGraph:
    def __init__(self, endpoint):
        self.connection = DriverRemoteConnection(f'wss://{endpoint}:8182/gremlin', 'g')
        self.g = traversal().withRemote(self.connection)
    
    def add_phrase_vertex(self, phrase_id: str, text: str):
        self.g.addV('Phrase').property('id', phrase_id).property('text', text).next()
    
    def add_relation_edge(self, subject_id: str, object_id: str, predicate: str):
        self.g.V().has('id', subject_id).addE('RELATION').to(
            self.g.V().has('id', object_id)
        ).property('predicate', predicate).next()
```

---

### **2. Framework Implementation Comparison**

| Framework | Language | Strengths | Use Case |
|-----------|----------|-----------|----------|
| **Neo4j** | Cypher + Python | Ecosystem, tooling | Production-ready |
| **NebulaGraph** | nGQL + Python | Performance, scale | Large datasets |
| **Neptune** | Gremlin + Python | Managed, AWS integration | Cloud deployments |
| **NetworkX** | Python | Simplicity, prototyping | Development/testing |

---

### **3. Recommended Stack: Neo4j + Python**

#### **Complete Implementation:**

```python
from neo4j import GraphDatabase
import json
import numpy as np
from sentence_transformers import SentenceTransformer

class Neo4jRAGGraph:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="neo4j123"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.encoder = SentenceTransformer('sentence-transformers/multilingual-mpnet-base-v2')
        self._create_constraints()
    
    def _create_constraints(self):
        """Create unique constraints and indexes"""
        with self.driver.session() as session:
            # Unique constraints
            session.run("CREATE CONSTRAINT phrase_id IF NOT EXISTS FOR (p:Phrase) REQUIRE p.id IS UNIQUE")
            session.run("CREATE CONSTRAINT passage_id IF NOT EXISTS FOR (p:Passage) REQUIRE p.id IS UNIQUE")
            
            # Text search indexes
            session.run("CREATE FULLTEXT INDEX phrase_text IF NOT EXISTS FOR (p:Phrase) ON EACH [p.text, p.normalized_text]")
            session.run("CREATE FULLTEXT INDEX passage_text IF NOT EXISTS FOR (p:Passage) ON EACH [p.text]")
    
    def add_phrase(self, phrase_id: str, text: str, normalized_text: str = None):
        normalized = normalized_text or text.lower().strip()
        embedding = self.encoder.encode(text).tolist()
        
        with self.driver.session() as session:
            query = """
            MERGE (p:Phrase {id: $phrase_id})
            SET p.text = $text,
                p.normalized_text = $normalized_text,
                p.embedding = $embedding,
                p.updated_at = datetime()
            RETURN p
            """
            session.run(query, 
                       phrase_id=phrase_id,
                       text=text, 
                       normalized_text=normalized,
                       embedding=embedding)
    
    def add_passage(self, passage_id: str, text: str, source: str = ""):
        embedding = self.encoder.encode(text).tolist()
        
        with self.driver.session() as session:
            query = """
            CREATE (p:Passage {
                id: $passage_id,
                text: $text,
                source: $source,
                embedding: $embedding,
                created_at: datetime()
            })
            RETURN p
            """
            session.run(query,
                       passage_id=passage_id,
                       text=text,
                       source=source,
                       embedding=embedding)
    
    def add_relation(self, subject_id: str, object_id: str, predicate: str, confidence: float = 1.0):
        with self.driver.session() as session:
            query = """
            MATCH (s:Phrase {id: $subject_id})
            MATCH (o:Phrase {id: $object_id})
            CREATE (s)-[:RELATION {
                predicate: $predicate,
                confidence: $confidence,
                created_at: datetime()
            }]->(o)
            """
            session.run(query,
                       subject_id=subject_id,
                       object_id=object_id,
                       predicate=predicate,
                       confidence=confidence)
    
    def add_contains(self, passage_id: str, phrase_id: str):
        with self.driver.session() as session:
            query = """
            MATCH (passage:Passage {id: $passage_id})
            MATCH (phrase:Phrase {id: $phrase_id})
            CREATE (passage)-[:CONTAINS]->(phrase)
            """
            session.run(query, passage_id=passage_id, phrase_id=phrase_id)
    
    def multi_hop_search(self, start_entities: list, max_hops: int = 3):
        """Multi-hop graph traversal"""
        with self.driver.session() as session:
            query = f"""
            MATCH (start:Phrase)
            WHERE start.normalized_text IN $start_entities
            CALL apoc.path.expand(start, "RELATION|SYNONYM", "", 1, {max_hops}) 
            YIELD path
            RETURN DISTINCT nodes(path) as nodes, relationships(path) as rels
            """
            result = session.run(query, start_entities=start_entities)
            return [record for record in result]
    
    def vector_search_passages(self, query_embedding: list, limit: int = 50):
        """Vector similarity search for passages"""
        with self.driver.session() as session:
            # Note: Cần Neo4j 5.x+ cho vector search
            query = """
            MATCH (p:Passage)
            WITH p, gds.similarity.cosine(p.embedding, $query_embedding) AS similarity
            RETURN p.id as id, p.text as text, similarity
            ORDER BY similarity DESC
            LIMIT $limit
            """
            result = session.run(query, query_embedding=query_embedding, limit=limit)
            return [(record["id"], record["text"], record["similarity"]) for record in result]
    
    def close(self):
        self.driver.close()
```

---

### **4. Dashboard & Monitoring Solutions**

#### **🎯 Neo4j Browser (Built-in)**
```bash
# Access via browser: http://localhost:7474
# Cypher queries for exploration:

# View graph structure
MATCH (n) RETURN n LIMIT 100

# View passage-phrase relationships
MATCH (passage:Passage)-[:CONTAINS]->(phrase:Phrase)
RETURN passage, phrase LIMIT 50

# Multi-hop relationships
MATCH path = (start:Phrase)-[:RELATION*1..3]->(end:Phrase)
WHERE start.text CONTAINS "Einstein"
RETURN path LIMIT 20
```

#### **📊 Neo4j Bloom (Advanced Visualization)**
```python
# Neo4j Bloom subscription required
# Visual graph exploration with natural language queries
# Automatic perspective generation
# Beautiful graph visualizations
```

#### **🔧 Custom Dashboard với Streamlit**
```python
import streamlit as st
import plotly.graph_objects as go
import networkx as nx
from neo4j_rag_graph import Neo4jRAGGraph

def create_dashboard():
    st.title("Knowledge Graph Dashboard")
    
    kg = Neo4jRAGGraph()
    
    # Sidebar controls
    st.sidebar.header("Controls")
    query = st.sidebar.text_input("Search Query")
    max_hops = st.sidebar.slider("Max Hops", 1, 5, 3)
    
    if query:
        # Perform search
        results = kg.multi_hop_search([query.lower()], max_hops)
        
        # Create networkx graph for visualization
        G = nx.Graph()
        for record in results:
            nodes = record["nodes"]
            rels = record["rels"]
            
            for node in nodes:
                G.add_node(node["id"], label=node["text"][:30])
            
            for rel in rels:
                G.add_edge(rel.start_node["id"], rel.end_node["id"], 
                          label=rel["predicate"])
        
        # Plot with plotly
        pos = nx.spring_layout(G)
        
        edge_x, edge_y = [], []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        
        edge_trace = go.Scatter(x=edge_x, y=edge_y, mode='lines')
        
        node_x = [pos[node][0] for node in G.nodes()]
        node_y = [pos[node][1] for node in G.nodes()]
        node_text = [G.nodes[node]["label"] for node in G.nodes()]
        
        node_trace = go.Scatter(x=node_x, y=node_y, mode='markers+text',
                               text=node_text, textposition="middle center")
        
        fig = go.Figure(data=[edge_trace, node_trace])
        st.plotly_chart(fig)
    
    # Statistics
    st.header("Graph Statistics")
    with kg.driver.session() as session:
        stats = session.run("""
        MATCH (n) 
        RETURN labels(n)[0] as type, count(*) as count
        """)
        
        for record in stats:
            st.metric(record["type"], record["count"])

if __name__ == "__main__":
    create_dashboard()
```

---

### **5. Setup Instructions**

#### **Neo4j Installation & Setup:**
```bash
# 1. Install Neo4j Desktop hoặc Community Edition
wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
echo 'deb https://debian.neo4j.com stable 4.4' | sudo tee -a /etc/apt/sources.list.d/neo4j.list
sudo apt update
sudo apt install neo4j=1:4.4.12

# 2. Start Neo4j
sudo systemctl start neo4j
sudo systemctl enable neo4j

# 3. Install Python dependencies
pip install neo4j py2neo sentence-transformers streamlit plotly networkx

# 4. Configure Neo4j
# Edit /etc/neo4j/neo4j.conf:
dbms.default_listen_address=0.0.0.0
dbms.connector.bolt.listen_address=:7687
dbms.connector.http.listen_address=:7474
```

#### **Environment Setup:**
```python
# requirements.txt
neo4j>=5.0.0
py2neo>=2021.2.3
sentence-transformers>=2.2.0
streamlit>=1.25.0
plotly>=5.15.0
networkx>=3.1
pandas>=1.5.0
numpy>=1.24.0
```

---

### **6. Recommendation**

**🎯 Recommended Stack:**
```
Graph DB: Neo4j Community Edition
Framework: Python + py2neo/neo4j-driver
Dashboard: Neo4j Browser + Custom Streamlit
Hosting: Docker containers
Monitoring: Neo4j Metrics + Custom dashboards
```

**Lý do:**
- ✅ **Production-ready** với strong community
- ✅ **Rich ecosystem** (APOC, GDS, Bloom)
- ✅ **Built-in dashboard** cho development
- ✅ **Vector search support** (Neo4j 5.x+)
- ✅ **Easy deployment** với Docker

**→ Setup này sẽ cho bạn full-featured knowledge graph system với beautiful visualizations!** 🚀