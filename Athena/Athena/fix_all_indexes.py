# Arquivo: fix_all_indexes.py
import psycopg2

# Conectar ao banco
conn = psycopg2.connect(
    host="aws-0-sa-east-1.pooler.supabase.com",
    port=6543,
    database="postgres",
    user="postgres.vcmafdafcmtlrvcxpxlz",
    password="wN5vJ&A6Aq3E6he"
)

cursor = conn.cursor()

# Lista de índices problemáticos
indexes_to_drop = [
    'pages_person_usuario_id_e082e59c',
    'pages_company_usuario_id_f5dbd8d2',
    'pages_contract_person_id_idx',
    'pages_contract_company_id_idx',
    'pages_contract_usuario_id_idx',
]

print("🧹 Limpando índices duplicados...")

for index_name in indexes_to_drop:
    try:
        cursor.execute(f"DROP INDEX IF EXISTS {index_name}")
        print(f"✅ Índice {index_name} removido")
    except Exception as e:
        print(f"⚠️ Erro ao remover {index_name}: {e}")

conn.commit()
cursor.close()
conn.close()

print("\n✅ Limpeza concluída!")