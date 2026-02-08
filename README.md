# Zabbix DB Capacity & Planning Calc

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Zabbix](https://img.shields.io/badge/zabbix-%23CC2932.svg?style=for-the-badge&logo=zabbix&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-blue?style=for-the-badge)


Uma ferramenta de desktop desenvolvida para Engenheiros de Monitoramento e Administradores de Redes realizarem o **Capacity Planning** de bancos de dados Zabbix de forma rápida e precisa.


## Funcionalidades

- **Cálculo em Tempo Real:** Resultados de NVPS, Armazenamento (GB) e IOPS atualizados instantaneamente.
- **Previsão de Armazenamento:** Baseado em métricas de retenção de Histórico e Trends (Tendências).
- **Estimativa de Performance:** Cálculo de IOPS mínimo sugerido para evitar filas (queues) no banco de dados.
- **Relatório Técnico (PDF):** Gera um documento detalhado pronto para ser enviado a gestores ou clientes, justificando investimentos em infraestrutura.
- **Interface Moderna:** Suporte a Dark Mode e Light Mode para melhor conforto visual.

## Lógica de Cálculo

O aplicativo utiliza as premissas oficiais da documentação Zabbix para estimativa de banco de dados:
- **Histórico:** ~90 bytes por valor.
- **Trends:** ~90 bytes por registro.
- **Eventos:** ~170 bytes por evento.

## Tecnologias Utilizadas

- **Python 3.x**
- **CustomTkinter:** Interface gráfica de alta performance.
- **FPDF:** Engine para geração de documentos PDF.
- **Tkinter Messagebox:** Tratamento de erros e notificações ao usuário.

## Como usar

1. Certifique-se de ter o Python instalado.
2. Instale as dependências:
   ```bash
   pip install customtkinter fpdf
