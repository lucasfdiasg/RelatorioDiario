import datetime
import os
import platform 

# --- 1. FUNÇÕES-ASSISTENTES (Utilitários) ---

def limpar_tela():
    """Limpa o console do terminal (funciona em Windows, Mac e Linux)."""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def mostrar_dashboard(data, a_fazer, em_execucao, concluidas, prorrogadas): # (MUDANÇA)
    """
    Mostra o painel principal com todas as 4 listas e emojis.
    """
    limpar_tela()
    print(f"--- GERADOR DE RELATÓRIOS --- Dia: {data} ---")
    
    # (MUDANÇA: Emoji ⏲️)
    print("\n[ A FAZER ⏲️  ]:")
    if not a_fazer:
        print("- Vazio")
    else:
        for i, tarefa in enumerate(a_fazer, start=1):
            print(f"  [{i}] {tarefa}")
            
    # (MUDANÇA: Emoji ✨)
    print("\n[ EM EXECUÇÃO ✨  ]:")
    if not em_execucao:
        print("- Vazio")
    else:
        for i, tarefa in enumerate(em_execucao, start=1):
            print(f"  [{i}] {tarefa}")

    # (NOVA LISTA: Emoji ➡️)
    print("\n[ PRORROGADAS (para amanhã) ➡️  ]:")
    if not prorrogadas:
        print("- Vazio")
    else:
        for i, tarefa in enumerate(prorrogadas, start=1):
            print(f"  [{i}] {tarefa}")

    # (MUDANÇA: Emoji ✅)
    print("\n[ CONCLUÍDAS ✅ ]:")
    if not concluidas:
        print("- Vazio")
    else:
        for tarefa in concluidas:
            print(f"  [✓] {tarefa}")
    
    print("-" * 40) # Separador

def mostrar_menu():
    """Imprime o novo menu de opções com 6 itens."""
    print("MENU DE OPÇÕES:")
    print("[1] Adicionar nova tarefa (em 'A Fazer')")
    print("[2] Ativar tarefa (Mover de 'A Fazer' -> 'Em Execução')")
    print("[3] Concluir tarefa (Mover de 'Em Execução' -> 'Concluídas')")
    # (NOVA OPÇÃO)
    print("[4] Prorrogar tarefa (Mover de 'A Fazer' -> 'Prorrogadas')")
    # (RENUMERADO)
    print("[5] Salvar Relatório Final (em .txt)")
    print("[6] Sair")

# --- 2. FUNÇÕES DE LÓGICA (Ações) ---

def adicionar_nova_tarefa(lista_a_fazer):
    """Pede ao usuário e adiciona uma tarefa na lista 'A Fazer'."""
    print("--- Adicionar Nova Tarefa ---")
    tarefa = input("Descreva a nova tarefa: ")
    if tarefa:
        lista_a_fazer.append(tarefa)
        print("Tarefa adicionada com sucesso!")
    else:
        print("Nenhuma tarefa adicionada.")
    input("Pressione Enter para continuar...")

def ativar_tarefa(lista_a_fazer, lista_em_execucao):
    """Move uma tarefa da lista 'A Fazer' para 'Em Execução'."""
    print("--- Ativar Tarefa (Mover para 'Em Execução') ---")
    if not lista_a_fazer:
        print("Não há tarefas 'A Fazer' para ativar.")
        input("Pressione Enter para continuar...")
        return
    try:
        idx_str = input("Digite o NÚMERO da tarefa 'A Fazer' que deseja ativar: ")
        idx = int(idx_str) - 1 
        if idx < 0: raise IndexError
        tarefa_movida = lista_a_fazer.pop(idx)
        lista_em_execucao.append(tarefa_movida)
        print(f"Tarefa '{tarefa_movida}' movida para 'Em Execução'!")
    except (ValueError, IndexError):
        print("ERRO: Número inválido. Nenhuma tarefa foi movida.")
    input("Pressione Enter para continuar...")

def concluir_tarefa(lista_em_execucao, lista_concluidas):
    """Move uma tarefa de 'Em Execução' para 'Concluídas'."""
    print("--- Concluir Tarefa ---")
    if not lista_em_execucao:
        print("Não há tarefas 'Em Execução' para concluir.")
        input("Pressione Enter para continuar...")
        return
    try:
        idx_str = input("Digite o NÚMERO da tarefa 'Em Execução' que deseja concluir: ")
        idx = int(idx_str) - 1 
        if idx < 0: raise IndexError
        tarefa_movida = lista_em_execucao.pop(idx)
        lista_concluidas.append(tarefa_movida)
        print(f"Tarefa '{tarefa_movida}' marcada como 'Concluída'!")
    except (ValueError, IndexError):
        print("ERRO: Número inválido. Nenhuma tarefa foi movida.")
    input("Pressione Enter para continuar...")

# (NOVA FUNÇÃO)
def prorrogar_tarefa(lista_a_fazer, lista_prorrogadas):
    """Move uma tarefa de 'A Fazer' para 'Prorrogadas'."""
    print("--- Prorrogar Tarefa (Mover para 'Prorrogadas') ---")
    if not lista_a_fazer:
        print("Não há tarefas 'A Fazer' para prorrogar.")
        input("Pressione Enter para continuar...")
        return
    try:
        idx_str = input("Digite o NÚMERO da tarefa 'A Fazer' que deseja prorrogar: ")
        idx = int(idx_str) - 1 
        if idx < 0: raise IndexError
        tarefa_movida = lista_a_fazer.pop(idx)
        lista_prorrogadas.append(tarefa_movida)
        print(f"Tarefa '{tarefa_movida}' movida para 'Prorrogadas'!")
    except (ValueError, IndexError):
        print("ERRO: Número inválido. Nenhuma tarefa foi movida.")
    input("Pressione Enter para continuar...")


def salvar_relatorio_arquivo(data, a_fazer, em_execucao, concluidas, prorrogadas): # (MUDANÇA)
    """
    Pega todos os dados das 4 listas e salva em um arquivo de texto.
    """
    limpar_tela()
    print("--- Salvando Relatório Final ---")
    nome_arquivo = f"Relatorio_{data.replace('/', '-')}.txt"
    
    # (MUDANÇA)
    total_tarefas = len(a_fazer) + len(em_execucao) + len(concluidas) + len(prorrogadas)

    try:
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(f"--- RELATÓRIO FINAL DE TAREFAS --- \n")
            f.write(f"Data: {data}\n")
            f.write(f"Total de Tarefas Gerenciadas: {total_tarefas}\n")
            f.write("=" * 40 + "\n")
            
            f.write("\n[ ✅ TAREFAS CONCLUÍDAS ]\n")
            if not concluidas: f.write("- Nenhuma\n")
            else:
                for tarefa in concluidas: f.write(f"- {tarefa}\n")
            
            f.write("\n[ ✨ TAREFAS EM EXECUÇÃO ]\n")
            if not em_execucao: f.write("- Nenhuma\n")
            else:
                for tarefa in em_execucao: f.write(f"- {tarefa}\n")
                    
            f.write("\n[ ⏲️ TAREFAS A FAZER ]\n")
            if not a_fazer: f.write("- Nenhuma\n")
            else:
                for tarefa in a_fazer: f.write(f"- {tarefa}\n")
            
            # (NOVA SEÇÃO NO RELATÓRIO)
            f.write("\n[ ➡️ TAREFAS PRORROGADAS (para o dia seguinte) ]\n")
            if not prorrogadas: f.write("- Nenhuma\n")
            else:
                for tarefa in prorrogadas: f.write(f"- {tarefa}\n")
            
            f.write("\n--- Fim do Relatório ---")
        
        print(f"\nSucesso! Relatório salvo como: {nome_arquivo}")
    except Exception as e:
        print(f"\nERRO: Não foi possível salvar o arquivo. Detalhe: {e}")

    input("\nPressione Enter para voltar ao menu...")


# --- 3. FUNÇÃO PRINCIPAL (A Orquestradora) ---

def main():
    hoje_formatado = datetime.datetime.now().strftime("%d/%m/%Y")

    # (NOVA LISTA)
    tarefas_a_fazer = []
    tarefas_em_execucao = []
    tarefas_concluidas = []
    tarefas_prorrogadas = []

    while True:
        # (MUDANÇA) Passa a nova lista para o dashboard
        mostrar_dashboard(hoje_formatado, tarefas_a_fazer, tarefas_em_execucao, tarefas_concluidas, tarefas_prorrogadas)
        mostrar_menu()
        
        # (MUDANÇA)
        escolha = input("Escolha uma opção (1-6): ")
        print()

        if escolha == '1':
            adicionar_nova_tarefa(tarefas_a_fazer)
        
        elif escolha == '2':
            ativar_tarefa(tarefas_a_fazer, tarefas_em_execucao)

        elif escolha == '3':
            concluir_tarefa(tarefas_em_execucao, tarefas_concluidas)
        
        # (NOVA OPÇÃO)
        elif escolha == '4':
            prorrogar_tarefa(tarefas_a_fazer, tarefas_prorrogadas)
        
        # (RENUMERADO)
        elif escolha == '5':
            salvar_relatorio_arquivo(hoje_formatado, tarefas_a_fazer, tarefas_em_execucao, tarefas_concluidas, tarefas_prorrogadas)
        
        # (RENUMERADO)
        elif escolha == '6':
            print("Saindo do Gerador de Relatórios...")
            break
        
        else:
            print("ERRO: Opção inválida.")
            input("Pressione Enter para tentar novamente...")

    print("Programa finalizado.")

# --- 4. PONTO DE ENTRADA ---
if __name__ == "__main__":
    main()