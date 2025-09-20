

### 1. Setup Database
```bash
cd src/DB
docker-compose up -d
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
pip install -r src/offline_indexing/offline_indexing_requirements.txt
```

### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env with your HuggingFace API key
```

### 4. Test Pipeline
```bash
cd src/offline_indexing/test
python test_offline_pipeline.py
python run_offline_pipeline.py --excel test/test_data.xlsx

```

### 5. Run với Real Data
```bash
cd src/offline_indexing
python run_offline_pipeline.py --excel vimqa_dev_300.xlsx
```


### 6. Verify Results

```bash
cd src/offline_indexing/test
python test_query_functions.py
```