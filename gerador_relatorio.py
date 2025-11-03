import datetime
import os
import platform 
import json
import time

class Tarefa:

    def __init__(self, titulo, descricao="", subtarefas=None, periodo=None):
        self.titulo = titulo
        self.descricao = descricao
        self.subtarefas = subtarefas if subtarefas is not None else []
        self.periodo = periodo

    def adicionar_subtarefa(self, sub_titulo):
        if sub_titulo:
            self.subtarefas.append(sub_titulo)
    
    def __str__(self):
        return self.titulo 
        
    def to_dict(self):
        return {
            "titulo": self.titulo,
            "descricao": self.descricao,
            "subtarefas": self.subtarefas,
            "periodo": self.periodo
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            titulo=data.get("titulo", "Sem Título"),
            descricao=data.get("descricao", ""),
            subtarefas=data.get("subtarefas", []),
            periodo=data.get("periodo", None)
        )

NOME_ARQUIVO_PLANEJAMENTO = "planejamento_store.json"

def carregar_planejamento(data_hoje_iso):
    print("Verificando planejamento anterior...")
    try:
        with open(NOME_ARQUIVO_PLANEJAMENTO, "r", encoding="utf-8") as f:
            dados = json.load(f)
            
        data_salva = dados.get("data_salva")
        
        if data_salva == data_hoje_iso:
            print("Planejamento de hoje já está carregado. (App reaberto)")
            pass 
        else:
            print(f"Carregando planejamento salvo de {data_salva}...")
        
        tarefas_carregadas = [Tarefa.from_dict(t) for t in dados.get("planejamento", [])]
        
        if data_salva != data_hoje_iso:
            for t in tarefas_carregadas:
                t.periodo = None 
        
        return tarefas_carregadas

    except FileNotFoundError:
        print("Nenhum arquivo de planejamento encontrado. Começando um novo dia.")
        return []
    except Exception as e:
        print(f"Erro ao carregar planejamento: {e}")
        return []

def salvar_planejamento(lista_a_fazer, data_hoje_iso):
    print("Salvando planejamento...")
    try:
        dados_planejamento = [tarefa.to_dict() for tarefa in lista_a_fazer]
        
        dados_para_salvar = {
            "data_salva": data_hoje_iso,
            "planejamento": dados_planejamento
        }
        
        with open(NOME_ARQUIVO_PLANEJAMENTO, "w", encoding="utf-8") as f:
            json.dump(dados_para_salvar, f, indent=4, ensure_ascii=False)
            
        print(f"Planejamento salvo em {NOME_ARQUIVO_PLANEJAMENTO}.")
        
    except Exception as e:
        print(f"ERRO ao salvar planejamento: {e}")

def limpar_tela():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def mostrar_dashboard(data, a_fazer, em_execucao, concluidas):
    limpar_tela()
    print(f"--- GERADOR DE RELATÓRIOS --- Dia: {data} ---")
    
    print("\n[ ⏲️  - A FAZER (Planejamento) ]:")
    if not a_fazer:
        print("- Vazio")
    else:
        for i, tarefa_obj in enumerate(a_fazer, start=1):
            print(f"\n  [{i}] {tarefa_obj.titulo}")
            if tarefa_obj.descricao: print(f"      Descrição: {tarefa_obj.descricao}")
            if tarefa_obj.subtarefas:
                print(f"      Sub-tarefas:")
                for sub in tarefa_obj.subtarefas: print(f"        - {sub}")
            
    print("\n[ ✨ - EM EXECUÇÃO ]:")
    if not em_execucao: print("- Vazio")
    else:
        for i, tarefa_obj in enumerate(em_execucao, start=1):
            periodo_str = f"({tarefa_obj.periodo})" if tarefa_obj.periodo else ""
            print(f"\n  [{i}] {tarefa_obj.titulo} {periodo_str}")

    print("\n[ ✅ - CONCLUÍDAS ]:")
    if not concluidas: print("- Vazio")
    else:
        for tarefa_obj in concluidas:
            periodo_str = f"({tarefa_obj.periodo})" if tarefa_obj.periodo else ""
            print(f"  [✓] {tarefa_obj.titulo} {periodo_str}")
    
    print("\n" + "-" * 40)

def mostrar_menu():
    print("MENU DE OPÇÕES:")
    print("[1] Adicionar nova tarefa (em 'A Fazer')")
    print("[2] Ativar tarefa (Mover de 'A Fazer' -> 'Em Execução')")
    print("[3] Concluir tarefa (Mover de 'Em Execução' -> 'Concluídas')")
    print("[4] Excluir Tarefa")
    print("[5] Gerar Relatório do Dia e Salvar Planejamento")
    print("[6] Sair (sem salvar relatório)")

def adicionar_nova_tarefa(lista_a_fazer):
    print("--- Adicionar Nova Tarefa ---")
    titulo = input("Qual o TÍTULO da tarefa? (Obrigatório): ")
    if not titulo:
        print("ERRO: O título não pode ser vazio."); time.sleep(1); return
    descricao = input("Adicione uma DESCRIÇÃO (Opcional): ")
    nova_tarefa = Tarefa(titulo, descricao)
    
    print("\nAdicione SUB-TAREFAS (Opcional, deixe em branco para parar):")
    contador_sub = 1
    while True:
        sub_titulo = input(f"  Sub-tarefa {contador_sub}: ")
        if not sub_titulo: break
        nova_tarefa.adicionar_subtarefa(sub_titulo)
        contador_sub += 1
        
    lista_a_fazer.append(nova_tarefa)
    print(f"\nTarefa '{nova_tarefa.titulo}' adicionada ao Planejamento (A Fazer)!")
    time.sleep(1)

def perguntar_periodo():
    while True:
        periodo = input("Período: [M]anhã ou [T]arde? ").strip().upper()
        if periodo in ['M', 'T']:
            return periodo
        print("Opção inválida. Digite 'M' ou 'T'.")

def ativar_tarefa(lista_a_fazer, lista_em_execucao):
    print("--- Ativar Tarefa (Mover para 'Em Execução') ---")
    if not lista_a_fazer:
        print("Não há tarefas 'A Fazer' para ativar."); time.sleep(1); return
    try:
        idx_str = input("Digite o NÚMERO da tarefa 'A Fazer' que deseja ativar: ")
        idx = int(idx_str) - 1 
        if idx < 0: raise IndexError

        periodo = perguntar_periodo()
        
        tarefa_movida = lista_a_fazer.pop(idx) 
        tarefa_movida.periodo = periodo 
        lista_em_execucao.append(tarefa_movida)
        
        print(f"Tarefa '{tarefa_movida.titulo}' movida para 'Em Execução' ({periodo})!")
    except (ValueError, IndexError):
        print("ERRO: Número inválido.")
    time.sleep(1)

def concluir_tarefa(lista_em_execucao, lista_concluidas):
    print("--- Concluir Tarefa ---")
    if not lista_em_execucao:
        print("Não há tarefas 'Em Execução' para concluir."); time.sleep(1); return
    try:
        idx_str = input("Digite o NÚMERO da tarefa 'Em Execução' que deseja concluir: ")
        idx = int(idx_str) - 1 
        if idx < 0: raise IndexError
        
        periodo = perguntar_periodo()
        
        tarefa_movida = lista_em_execucao.pop(idx)
        tarefa_movida.periodo = periodo 
        lista_concluidas.append(tarefa_movida)
        print(f"Tarefa '{tarefa_movida.titulo}' marcada como 'Concluída' ({periodo})!")
    except (ValueError, IndexError):
        print("ERRO: Número inválido.")
    time.sleep(1)

def excluir_tarefa(a_fazer, em_execucao):
    print("--- Excluir Tarefa Permanentemente ---")
    print("De qual lista você deseja excluir?")
    print("[1] ⏲️ A Fazer")
    print("[2] ✨ Em Execução")
    print("[C] Cancelar")
    
    escolha_lista = input("Escolha a lista (1, 2 ou C): ").strip().lower()
    lista_alvo, nome_lista = None, ""

    if escolha_lista == '1': lista_alvo, nome_lista = a_fazer, "A Fazer"
    elif escolha_lista == '2': lista_alvo, nome_lista = em_execucao, "Em Execução"
    elif escolha_lista == 'c': print("Operação cancelada."); time.sleep(1); return
    else: print("ERRO: Lista inválida."); time.sleep(1); return
    
    if not lista_alvo:
        print(f"A lista '[{nome_lista}]' já está vazia."); time.sleep(1); return
        
    try:
        idx_str = input(f"Digite o NÚMERO da tarefa na lista '[{nome_lista}]' que deseja EXCLUIR: ")
        idx = int(idx_str) - 1
        if idx < 0: raise IndexError
        tarefa_excluida = lista_alvo.pop(idx)
        print(f"\nSucesso! Tarefa '{tarefa_excluida.titulo}' foi EXCLUÍDA.")
    except (ValueError, IndexError):
        print("ERRO: Número inválido.")
    time.sleep(1)

def gerar_relatorio_e_salvar_SIMPLES(data, a_fazer, em_execucao, concluidas, data_hoje_iso):
    limpar_tela()
    print("--- Gerando Relatório do Dia e Salvando Planejamento ---")
    nome_arquivo_relatorio = f"Relatorio_{data.replace('/', '-')}.txt"

    concluidas_manha = [t for t in concluidas if t.periodo == 'M']
    concluidas_tarde = [t for t in concluidas if t.periodo == 'T']
    execucao_manha = [t for t in em_execucao if t.periodo == 'M']
    execucao_tarde = [t for t in em_execucao if t.periodo == 'T']
    
    try:
        with open(nome_arquivo_relatorio, "w", encoding="utf-8") as f:
            f.write(f"*RELATÓRIO {data}*\n\n")
            f.write("+++++++\n|| MANHÃ ||\n=======\n\n")
            
            f.write("[ ✅ CONCLUÍDAS - MANHÃ ]\n")
            for t in concluidas_manha:
                f.write(f"+ {t.titulo}\n")
                if t.descricao: f.write(f"\t> {t.descricao}\n")
                for s in t.subtarefas: f.write(f"\t\t- {s}\n")
            
            f.write("\n[ ✨ EM EXECUÇÃO - MANHã ]\n")
            for t in execucao_manha:
                f.write(f"+ {t.titulo}\n")
                if t.descricao: f.write(f"\t> {t.descricao}\n")
                for s in t.subtarefas: f.write(f"\t\t- {s}\n")
            
            f.write("\n\n+++++++\n|| TARDE ||\n=======\n\n")
            
            f.write("[ ✅ CONCLUÍDAS - TARDE ]\n")
            for t in concluidas_tarde:
                f.write(f"+ {t.titulo}\n")
                if t.descricao: f.write(f"\t> {t.descricao}\n")
                for s in t.subtarefas: f.write(f"\t\t- {s}\n")

            f.write("\n[ ✨ EM EXECUÇÃO - TARDE ]\n")
            for t in execucao_tarde:
                f.write(f"+ {t.titulo}\n")
                if t.descricao: f.write(f"\t> {t.descricao}\n")
                for s in t.subtarefas: f.write(f"\t\t- {s}\n")

            f.write("\n\n=====================\nPLANEJAMENTO\n=====================\n\n")
            
            if not a_fazer: f.write("- Nada planejado.\n")
            else:
                for t in a_fazer:
                    f.write(f"+ {t.titulo}\n")
                    if t.descricao: f.write(f"\t> {t.descricao}\n")
                    for s in t.subtarefas: f.write(f"\t\t- {s}\n")
            
        print(f"\nSucesso! Relatório do dia salvo como: {nome_arquivo_relatorio}")

        salvar_planejamento(a_fazer, data_hoje_iso)
        
        a_fazer.clear()
        em_execucao.clear()
        concluidas.clear()
        
        print("\nRelatório gerado e planejamento salvo. O dia foi encerrado.")
        print("As listas foram limpas.")

    except Exception as e:
        print(f"\nERRO: Não foi possível gerar o relatório. Detalhe: {e}")

    input("\nPressione Enter para voltar ao menu...")


def main():
    hoje_formatado_app = datetime.datetime.now().strftime("%d/%m/%Y")
    hoje_formatado_iso = datetime.date.today().isoformat() 
    
    print("Iniciando o Gerador de Relatórios...")
    tarefas_a_fazer = carregar_planejamento(hoje_formatado_iso)
    tarefas_em_execucao = []
    tarefas_concluidas = []  
    
    if tarefas_a_fazer:
        salvar_planejamento(tarefas_a_fazer, hoje_formatado_iso)

    time.sleep(1)

    while True:
        mostrar_dashboard(hoje_formatado_app, tarefas_a_fazer, tarefas_em_execucao, tarefas_concluidas)
        mostrar_menu()
        
        escolha = input("Escolha uma opção (1-6): ")
        print()

        if escolha == '1':
            adicionar_nova_tarefa(tarefas_a_fazer)
            salvar_planejamento(tarefas_a_fazer, hoje_formatado_iso)
        
        elif escolha == '2':
            ativar_tarefa(tarefas_a_fazer, tarefas_em_execucao)
            salvar_planejamento(tarefas_a_fazer, hoje_formatado_iso)

        elif escolha == '3':
            concluir_tarefa(tarefas_em_execucao, tarefas_concluidas)
        
        elif escolha == '4':
            excluir_tarefa(tarefas_a_fazer, tarefas_em_execucao)
            salvar_planejamento(tarefas_a_fazer, hoje_formatado_iso)
        
        elif escolha == '5':
            gerar_relatorio_e_salvar_SIMPLES(hoje_formatado_app, tarefas_a_fazer, tarefas_em_execucao, tarefas_concluidas, hoje_formatado_iso)
        
        elif escolha == '6':
            print("Saindo do Gerador de Relatórios...")
            salvar_planejamento(tarefas_a_fazer, hoje_formatado_iso)
            print("Planejamento atual salvo. Até mais!")
            break
        
        else:
            print("ERRO: Opção inválida.")
            time.sleep(1)

    print("Programa finalizado.")

if __name__ == "__main__":
    main()