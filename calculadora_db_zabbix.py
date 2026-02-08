import customtkinter as ctk
from fpdf import FPDF
from datetime import datetime
import tkinter.messagebox as messagebox
from tkinter import filedialog

class ZabbixExpertCalc(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurações Iniciais
        self.title("Calculadora Zabbix feita por Elison®")
        self.geometry("600x850")
        ctk.set_appearance_mode("dark") 
        ctk.set_default_color_theme("blue")

        # Variáveis de cálculo
        self.last_gb = 0
        self.last_iops = 0
        self.last_nvps = 0

        # --- Cabeçalho e Alternador de Tema ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(pady=10, padx=20, fill="x")

        self.label_title = ctk.CTkLabel(self.header_frame, text="Zabbix DB Capacity", font=("Roboto", 22, "bold"))
        self.label_title.pack(side="left", pady=10)

        # Botão de Tema (Sol/Lua)
        self.theme_btn = ctk.CTkButton(
            self.header_frame, 
            text="🌙", 
            width=40, 
            height=40,
            corner_radius=20,
            fg_color=("gray75", "gray25"),
            text_color=("black", "white"),
            hover_color=("gray70", "gray30"),
            command=self.toggle_theme
        )
        self.theme_btn.pack(side="right", pady=10)

        # --- Container de Inputs ---
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(pady=10, padx=30, fill="x")

        self.vars = {}
        fields = [
            ("Número Total de Itens", "items", "1000"),
            ("Refresh Rate Médio (seg)", "refresh", "60"),
            ("Retenção Histórico (dias)", "h_days", "90"),
            ("Retenção Trends (dias)", "t_days", "365"),
            ("Eventos por Segundo", "events", "1")
        ]

        for label_text, attr, default in fields:
            lbl = ctk.CTkLabel(self.input_frame, text=label_text)
            lbl.pack(pady=(10, 0))
            var = ctk.StringVar(value=default)
            var.trace_add("write", lambda *args: self.calculate())
            entry = ctk.CTkEntry(self.input_frame, textvariable=var, width=250, justify="center")
            entry.pack(pady=(0, 5))
            self.vars[attr] = var

        # --- Resultados ---
        self.res_frame = ctk.CTkFrame(self)
        self.res_frame.pack(pady=20, padx=30, fill="both", expand=True)

        self.lbl_gb = ctk.CTkLabel(self.res_frame, text="Espaço: 0.00 GB", font=("Roboto", 18, "bold"), text_color="#3498db")
        self.lbl_gb.pack(pady=5)

        self.lbl_nvps = ctk.CTkLabel(self.res_frame, text="NVPS: 0.00", font=("Roboto", 14))
        self.lbl_nvps.pack(pady=2)

        self.lbl_iops = ctk.CTkLabel(self.res_frame, text="IOPS Mínimo: 0", font=("Roboto", 16, "bold"), text_color="#e67e22")
        self.lbl_iops.pack(pady=5)

        self.btn_pdf = ctk.CTkButton(self, text="Gerar Relatório Técnico Completo", command=self.export_pdf, 
                                     fg_color="#27ae60", hover_color="#219150")
        self.btn_pdf.pack(pady=20)

        self.calculate()

    def toggle_theme(self):
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("light")
            self.theme_btn.configure(text="☀️")
        else:
            ctk.set_appearance_mode("dark")
            self.theme_btn.configure(text="🌙")

    def calculate(self):
        try:
            # Documentação Zabbix: History ~90 bytes, Trends ~90 bytes, Eventos ~170 bytes
            B_HISTORY, B_TREND, B_EVENT = 90, 90, 170
            items = float(self.vars['items'].get() or 0)
            refresh = float(self.vars['refresh'].get() or 1)
            h_days = float(self.vars['h_days'].get() or 0)
            t_days = float(self.vars['t_days'].get() or 0)
            events_sec = float(self.vars['events'].get() or 0)

            # NVPS (New Values Per Second)
            nvps = items / refresh
            self.last_nvps = nvps

            # Espaço por categoria
            h_total = nvps * 86400 * h_days * B_HISTORY
            t_total = items * 24 * t_days * B_TREND
            e_total = events_sec * 86400 * 365 * B_EVENT

            self.last_gb = (h_total + t_total + e_total) / (1024**3)
            self.last_iops = (nvps * 1.5) + (events_sec * 10) 

            self.lbl_gb.configure(text=f"Espaço Total: {self.last_gb:.2f} GB")
            self.lbl_nvps.configure(text=f"NVPS: {nvps:.2f}")
            self.lbl_iops.configure(text=f"IOPS Mínimo: {int(self.last_iops)} req/s")
        except Exception:
            pass

    def export_pdf(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Arquivos PDF", "*.pdf")],
            initialfile=f"Capacity_Planning_Zabbix_{datetime.now().strftime('%Y%m%d')}.pdf"
        )
        
        if filename:
            try:
                pdf = FPDF()
                pdf.add_page()
                
                # --- CABEÇALHO ---
                pdf.set_font("Arial", 'B', 16)
                pdf.cell(190, 10, "Relatorio Tecnico de Capacity Planning - Zabbix", ln=True, align='C')
                pdf.set_font("Arial", size=10)
                pdf.cell(190, 10, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align='C')
                pdf.ln(10)

                # --- RESULTADOS RESUMIDOS ---
                pdf.set_font("Arial", 'B', 13)
                pdf.set_fill_color(230, 230, 230)
                pdf.cell(0, 10, "1. Resumo de Recursos", ln=True, fill=True)
                pdf.set_font("Arial", size=11)
                pdf.ln(2)
                pdf.cell(0, 7, f"- Espaco Estimado em Disco: {self.last_gb:.2f} GB", ln=True)
                pdf.cell(0, 7, f"- Performance de I/O (IOPS): {int(self.last_iops)} req/s", ln=True)
                pdf.cell(0, 7, f"- Carga de Dados (NVPS): {self.last_nvps:.2f}", ln=True)
                pdf.ln(8)

                # --- DETALHAMENTO TÉCNICO ---
                pdf.set_font("Arial", 'B', 13)
                pdf.cell(0, 10, "2. Analise de Expansao de Dados", ln=True, fill=True)
                pdf.ln(2)

                # History
                pdf.set_font("Arial", 'B', 11)
                pdf.cell(0, 7, "2.1 Tabelas de Historico (History)", ln=True)
                pdf.set_font("Arial", size=10)
                pdf.multi_cell(0, 5, "O historico armazena cada valor coletado individualmente. O crescimento e agressivo e depende do NVPS. "
                                     "Em ambientes de TI de infraestrutura, um alto volume de dados brutos e crucial para analise de incidentes em tempo real, "
                                     "mas exige storages com baixa latencia (SSD/NVMe).")
                pdf.ln(3)

                # Trends
                pdf.set_font("Arial", 'B', 11)
                pdf.cell(0, 7, "2.2 Tabelas de Tendencias (Trends)", ln=True)
                pdf.set_font("Arial", size=10)
                pdf.multi_cell(0, 5, "As trends sao agregacoes horarias. Mesmo com milhares de itens, o banco cresce de forma controlada "
                                     "nas tabelas de tendencias, pois cada item gera apenas 24 registros por dia. E o que permite manter dados por 1 ano ou mais "
                                     "para relatorios de disponibilidade e SLA.")
                pdf.ln(3)

                # IOPS
                pdf.set_font("Arial", 'B', 11)
                pdf.cell(0, 7, "2.3 Impacto em I/O e Housekeeper", ln=True)
                pdf.set_font("Arial", size=10)
                pdf.multi_cell(0, 5, "O IOPS sugerido considera a escrita constante dos itens e o processo de limpeza (Housekeeper). "
                                     "Em ambientes Azure ou On-premise, um disco sobrecarregado causara 'Zabbix queue' alta. "
                                     "Este calculo previne gargalos de escrita que impactariam a observabilidade.")

                pdf.ln(10)
                pdf.set_font("Arial", 'I', 8)
                pdf.multi_cell(0, 5, "Nota: Calculos baseados nas premissas oficiais da documentacao Zabbix para banco de dados. "
                                     "A utilizacao real pode variar conforme a compactacao do filesystem e engine do DB.")

                pdf.output(filename)
                messagebox.showinfo("Sucesso", f"Relatorio salvo em:\n{filename}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao gerar PDF: {e}")

if __name__ == "__main__":
    app = ZabbixExpertCalc()
    app.mainloop()
