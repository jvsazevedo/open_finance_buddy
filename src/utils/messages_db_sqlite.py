import sqlite3
from langchain.vectorstores import SQLiteVSS
from langchain.embeddings import OpenAIEmbeddings
from langchain_core.documents import Document

conn = sqlite3.connect("messages_history.db")
cursor = conn.cursor()

embeddings = OpenAIEmbeddings()
vectorstore = SQLiteVSS.from_params(
    embedding=embeddings,
    db_file="messages_vectors.db",
    table_name="embeddings",
    content_column="content",
    metadata_columns=["message_id", "topic_summary", "user_id"]
)

def create_conversations_table():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY,
        user_id TEXT,
        role TEXT,
        content TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        topic_summary TEXT
    )
    ''')
    conn.commit()

def add_message_with_embedding(user_id: int, role: str, content: str, topic_summary: str):
    cursor.execute(
        "INSERT INTO conversations (user_id, role, content, topic_summary) VALUES (?, ?, ?, ?)", 
        (user_id, role, content, topic_summary)
    )
    message_id = cursor.lastrowid
    conn.commit()
    
    vectorstore.add_documents([
        Document(
            page_content=content,
            metadata={"message_id": message_id, "user_id": user_id, "topic_summary": topic_summary}
        )
    ])
    
    return message_id

def get_recent_conversations(user_id, limit=10):
    """
    Recupera as conversas mais recentes de um usuário específico, 
    ordenadas por message_id decrescente.
    
    Args:
        user_id: ID do usuário
        limit: Número máximo de conversas a retornar (padrão: 10)
    
    Returns:
        Lista de tuplas representando as conversas
    """
    cursor.execute(
        """
        SELECT * FROM conversations 
        WHERE user_id = ? 
        ORDER BY id DESC 
        LIMIT ?
        """,
        (user_id, limit)
    )
    return cursor.fetchall()

def find_similar_messages_for_user(query, user_id, limit=5):
    """
    Busca mensagens similares à query, filtrando apenas para um usuário específico.
    
    Args:
        query: Texto para busca de similaridade
        user_id: ID do usuário para filtrar os resultados
        limit: Número máximo de resultados (padrão: 5)
    
    Returns:
        Lista de tuplas representando as conversas similares do usuário
    """
    results = vectorstore.similarity_search(
        query, 
        k=limit,
        filter={"user_id": user_id}  # Filtrar por user_id
    )
    
    message_ids = [doc.metadata["message_id"] for doc in results]
    
    if message_ids:
        placeholders = ','.join(['?'] * len(message_ids))
        cursor.execute(
            f"SELECT * FROM conversations WHERE id IN ({placeholders})",
            message_ids
        )
        return cursor.fetchall()
    return []

def find_recent_similar_messages(query, user_id, limit=5, time_limit_days=7):
    """
    Busca mensagens similares à query entre as conversas recentes de um usuário.
    
    Args:
        query: Texto para busca de similaridade
        user_id: ID do usuário para filtrar os resultados
        limit: Número máximo de resultados (padrão: 5)
        time_limit_days: Número de dias atrás para considerar (padrão: 7)
    
    Returns:
        Lista de tuplas representando as conversas similares recentes do usuário
    """
    # Calcular a data limite
    import datetime
    date_limit = datetime.datetime.now() - datetime.timedelta(days=time_limit_days)
    date_limit_str = date_limit.strftime('%Y-%m-%d %H:%M:%S')
    
    results = vectorstore.similarity_search(
        query, 
        k=limit*2,  # Buscar mais resultados para depois filtrar por data
        filter={"user_id": user_id}
    )
    
    message_ids = [doc.metadata["message_id"] for doc in results]
    
    if message_ids:
        placeholders = ','.join(['?'] * len(message_ids))
        cursor.execute(
            f"""
            SELECT * FROM conversations 
            WHERE id IN ({placeholders})
            AND user_id = ?
            AND created_at > ?
            ORDER BY id DESC
            LIMIT ?
            """,
            message_ids + [user_id, date_limit_str, limit]
        )
        return cursor.fetchall()
    return []

def find_similar_messages_by_topic(query, topic_keywords, user_id=None, limit=5):
    """
    Busca mensagens similares à query que contenham determinadas palavras-chave no resumo do tópico.
    
    Args:
        query: Texto para busca de similaridade
        topic_keywords: Lista de palavras-chave para filtrar por tópico
        user_id: ID do usuário para filtrar os resultados (opcional)
        limit: Número máximo de resultados (padrão: 5)
    
    Returns:
        Lista de tuplas representando as conversas similares por tópico
    """
    # Preparar filtro de metadata
    metadata_filter = {}
    if user_id:
        metadata_filter["user_id"] = user_id
    
    results = vectorstore.similarity_search(
        query, 
        k=limit*3,  # Buscar mais resultados para depois filtrar por tópico
        filter=metadata_filter if metadata_filter else None
    )
    
    filtered_results = []
    for doc in results:
        topic_summary = doc.metadata.get("topic_summary", "").lower()
        if any(keyword.lower() in topic_summary for keyword in topic_keywords):
            filtered_results.append(doc)
        
        if len(filtered_results) >= limit:
            break
    
    message_ids = [doc.metadata["message_id"] for doc in filtered_results[:limit]]
    
    if message_ids:
        placeholders = ','.join(['?'] * len(message_ids))
        cursor.execute(
            f"SELECT * FROM conversations WHERE id IN ({placeholders})",
            message_ids
        )
        return cursor.fetchall()
    return []