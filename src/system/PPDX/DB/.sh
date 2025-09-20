```bash
mkdir D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\DB\neo4j-data\data
mkdir D:\GIT\ResearchProject_Memory-AugmentedAIAgents\GraduationProject\src\system\PPDX\DB\neo4j-data\logs
mkdir D:\GIT\ResearchProject_Memory-AugmentedAIAgents\GraduationProject\src\system\PPDX\DB\neo4j-data\import
mkdir D:\GIT\ResearchProject_Memory-AugmentedAIAgents\GraduationProject\src\system\PPDX\DB\neo4j-data\conf
```

# Cách run này mình check thử thì ko thấy log rất lạ. 
```bash
docker run `
    --name my-neo4j-graphrag `
    -p 7474:7474 `
    -p 7687:7687 `
    -v D:/GIT/ResearchProject_Memory-AugmentedAIAgents/GraduationProject/src/system/PPDX/DB/neo4j-data/data:/data `
    -v D:/GIT/ResearchProject_Memory-AugmentedAIAgents/GraduationProject/src/system/PPDX/DB/neo4j-data/logs:/logs `
    -v D:/GIT/ResearchProject_Memory-AugmentedAIAgents/GraduationProject/src/system/PPDX/DB/neo4j-data/import:/var/lib/neo4j/import `
    -v D:/GIT/ResearchProject_Memory-AugmentedAIAgents/GraduationProject/src/system/PPDX/DB/neo4j-data/conf:/var/lib/neo4j/conf `
    -e NEO4J_AUTH=neo4j/your_super_secret_password `
    --env NEO4J_ACCEPT_LICENSE_AGREEMENT=yes `
    -d neo4j:latest
```

# Cách run chuẩn docker compose và logs rõ ràng 
```bash
docker compose up -d
```
# Vào http://localhost:7474/
# Check : Sau khi đăng nhập vào Neo4j Browser (qua cổng 7474),
#  bạn sẽ thấy một giao diện có ô nhập lệnh ở phía trên cùng.
#  Hãy nhập các lệnh Cypher sau để tạo một vài nút và mối quan hệ 
# để bạn có thể thấy dữ liệu:

```Cypher
CREATE (p:Person {name: 'Alice', age: 30})
CREATE (m:Movie {title: 'The Matrix', released: 1999})
CREATE (d:Director {name: 'Lana Wachowski'})
RETURN p, m, d
```


---

# cách reset lại cả v
docker compose down -v