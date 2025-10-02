# Criar arquivo: create_contract_table.py
import psycopg2

conn = psycopg2.connect(
    host="aws-0-sa-east-1.pooler.supabase.com",
    port=6543,
    database="postgres",
    user="postgres.vcmafdafcmtlrvcxpxlz",
    password="wN5vJ&A6Aq3E6he"
)

cursor = conn.cursor()

# Verificar se tabela existe
cursor.execute("""
    SELECT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_name = 'pages_contract'
    );
""")

table_exists = cursor.fetchone()[0]

if table_exists:
    print("✅ Tabela pages_contract já existe!")
    
    # Listar colunas existentes
    cursor.execute("""
        SELECT column_name FROM information_schema.columns 
        WHERE table_name = 'pages_contract'
        ORDER BY ordinal_position
    """)
    
    print("\n📋 Colunas da tabela:")
    for row in cursor.fetchall():
        print(f"  - {row[0]}")
else:
    print("❌ Tabela pages_contract NÃO existe!")
    print("🔧 Você precisa aplicar a migration 0004 que cria essa tabela")

cursor.close()
conn.close()