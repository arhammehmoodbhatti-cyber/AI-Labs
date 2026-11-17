This folder contains the tokenization, chunking and text-retrieval tasks for Lab 6. The policy and support documents are synthetic examples written for this exercise.

## Files
- `task1_tokens.py`: compares whitespace and Unicode word-like tokens and checks the optional model tokenizer.
- `task2_chunks.py`: creates fixed windows and sentence-aware chunks with source offsets.
- `task3_retrieval.py`: compares three chunking strategies with TF-IDF and the sentence-embedding backend when its package is available.
- `lab6_search.py`: shared retrieval class.
- `guided_chatbot.py`, `guided_suggestions.py`, `guided_tokens.py`, `guided_embeddings.py`, `guided_chunks.py`, `guided_limits.py`, `guided_metrics.py`: guided examples.
- `scenario1_handbook.py` to `scenario5_equipment.py`: five retrieval scenarios.
- `document_chatbot.py`: interactive source-evidence demonstration.
- `corpus.json`, `queries.json`: synthetic source documents and labeled queries.
- `retrieval_log.csv`: actual retrieval output. Rows marked `not_run_model_unavailable` are not embedding results.
- `Lab6_Report.docx`: methods, observed results and limitations.

## Setup
Use Python 3.10 or newer. Install the packages with:

```bash
python -m pip install -r requirements.txt
```

The first embedding run downloads `sentence-transformers/all-MiniLM-L6-v2` and may need internet access. The default TF-IDF examples do not need model weights.

## Run

```bash
python task1_tokens.py
python guided_chatbot.py
python guided_suggestions.py
python task2_chunks.py
python guided_chunks.py
python guided_embeddings.py
python guided_limits.py
python guided_metrics.py
python task3_retrieval.py
python document_chatbot.py
```

Run any scenario separately, for example `python scenario1_handbook.py`. The retrieval script keeps the four development queries separate from the four held-out test queries. It does not treat results for unanswerable queries as relevant evidence.
