# 💰 Meu Controle Financeiro Pessoal

Um sistema interativo feito com **Python + Streamlit** para organizar receitas e despesas mês a mês, com dashboards e exportação compatível com Excel.

---

## 📌 Funcionalidades

- ✅ Cadastro e edição de receitas e despesas
- 📊 Dashboard anual com gráficos interativos (Plotly)
- 💾 Salvamento automático em arquivo `.csv`
- ⬇️ Exportação direta com acentuação e colunas corretas
- 🧮 Cálculo de saldo mensal e anual

---

## ▶️ Como Executar

1. Instale as dependências:

```bash
pip install streamlit pandas plotly
Execute o app:

bash
Copiar
Editar
streamlit run main.py
📁 Arquivo de Dados
Os dados são salvos no arquivo meus_dados.csv

Codificação: UTF-8 com BOM (utf-8-sig)

Separador: ; (ponto e vírgula), compatível com Excel no Brasil

📥 Como abrir no Excel sem erro de acento
✅ Método Recomendado (abrir direto):
Basta dar duplo clique no arquivo .csv — o Excel abrirá corretamente com colunas separadas e acentos visíveis.

🔄 Método Alternativo:
Excel > Dados > Obter Dados > De Texto/CSV

Origem do arquivo: 65001: Unicode (UTF-8)

Delimitador: Ponto e vírgula (;)

Clique em "Carregar"

🧾 Estrutura do CSV
csv
Copiar
Editar
Data;Descrição;Valor;Categoria
2025-05-02;Posto;-12.00;Transporte
2025-05-03;Mercado;-150.00;Alimentação
...
📸 Exemplo de Tela
![Image](https://github.com/user-attachments/assets/2d2976ae-7d2c-4117-8314-20a938dc9681)

![Image](https://github.com/user-attachments/assets/17019fd7-8edc-4832-bdfb-91e3c576d514)

![Image](https://github.com/user-attachments/assets/86dcfa7b-b1e8-43bb-97cf-849a2baccb3d)
📄 Licença
Este projeto é livre para uso pessoal.

yaml
Copiar
Editar

---
