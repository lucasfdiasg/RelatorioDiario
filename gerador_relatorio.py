import datetime
import os      # Para comandos do sistema (limpar tela)
import platform 

# --- 1. FUNÇÕES-ASSISTENTES (Utilitários) ---

def limpar_tela():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def mostrar_dashboard(data, a_fazer, em_execucao, concluidas):
    """Imprime o painel principal com as listas de tarefas."""
    limpar_tela()
    print(f"--- GERADOR DE RELATÓRIOS --- Dia: {data} ---")
    
    print("\n[ A FAZER ]:")
    if not a_fazer:
        print("- Vazio")
    else:
        for i, tarefa in enumerate(a_fazer, start=1):
            print(f"  [{i}] {tarefa}")
            
    print("\n[ EM EXECUÇÃO ]:")
    if not em_execucao:
        print("- Vazio")
    else:
        for i, tarefa in enumerate(em_execucao, start=1):
            print(f"  [{i}] {tarefa}")

    print("\n[ CONCLUÍDAS ]:")
    if not concluidas:
        print("- Vazio")
    else:
        for tarefa in concluidas:
            print(f"  [✓] {tarefa}")
    
    print("-" * 40)
def mostrar_menu():
    """Imprime o novo menu de opções."""
    print("MENU DE OPÇÕES:")
    print("[1] Adicionar nova tarefa (em 'A Fazer')")
    print("[2] Ativar tarefa (Mover de 'A Fazer' -> 'Em Execução')")
    print("[3] Concluir tarefa (Mover de 'Em Execução' -> 'Concluídas')")
    print("[4] Gerar Relatório (prévia)")
    print("[5] Sair")

# --- 2. FUNÇÕES DE LÓGICA (Ações) ---

def adicionar_nova_tarefa(lista_a_fazer):
    """Pede ao usuário e adiciona uma tarefa na lista 'A Fazer'."""
    print("--- Adicionar Nova Tarefa ---")
    tarefa = input("Descreva a nova tarefa: ")
    if tarefa: # Garante que o usuário digitou algo
        lista_a_fazer.append(tarefa)
        print("Tarefa adicionada com sucesso!")
    else:
        print("Nenhuma tarefa adicionada.")

def ativar_tarefa(lista_a_fazer, lista_em_execucao):
    print("--- Ativar Tarefa (Mover para 'Em Execução') ---")
    if not lista_a_fazer:
        print("Não há tarefas 'A Fazer' para ativar.")
        input("Pressione Enter para continuar...")
        return

    try:
        idx_str = input("Digite o NÚMERO da tarefa 'A Fazer' que deseja ativar: ")
        idx = int(idx_str) - 1
        
        tarefa_movida = lista_a_fazer.pop(idx)
        
        lista_em_execucao.append(tarefa_movida)
        print(f"Tarefa '{tarefa_movida}' movida para 'Em Execução'!")
        
    except (ValueError, IndexError):
        print("ERRO: Número inválido. Nenhuma tarefa foi movida.")
    
    input("Pressione Enter para continuar...")

def concluir_tarefa(lista_em_execucao, lista_concluidas):
    print("--- Concluir Tarefa ---")
    if not lista_em_execucao:
        print("Não há tarefas 'Em Execução' para concluir.")
        input("Pressione Enter para continuar...")
        return

    try:
        idx_str = input("Digite o NÚMERO da tarefa 'Em Execução' que deseja concluir: ")
        idx = int(idx_str) - 1 
        
        tarefa_movida = lista_em_execucao.pop(idx)
        lista_concluidas.append(tarefa_movida)
        print(f"Tarefa '{tarefa_movida}' marcada como 'Concluída'!")
        
    except (ValueError, IndexError):
        print("ERRO: Número inválido. Nenhuma tarefa foi movida.")
    
    input("Pressione Enter para continuar...")

def mostrar_relatorio_console(data, a_fazer, em_execucao, concluidas):
    """Imprime o relatório final (similar ao antigo)."""
    limpar_tela()
    total_tarefas = len(a_fazer) + len(em_execucao) + len(concluidas)
    
    print(f"--- RELATÓRIO FINAL - {data} ---")
    print(f"Total de Tarefas Gerenciadas: {total_tarefas}")

    print("\n[ CONCLUÍDAS ]:")
    if not concluidas: print("- Nenhuma")
    for tarefa in concluidas: print(f"- {tarefa}")
        
    print("\n[ EM EXECUÇÃO ]:")
    if not em_execucao: print("- Nenhuma")
    for tarefa in em_execucao: print(f"- {tarefa}")
            
    print("\n[ A FAZER ]:")
    if not a_fazer: print("- Nenhuma")
    for tarefa in a_fazer: print(f"- {tarefa}")
    
    print("\n(Fim do Relatório)")
    input("\nPressione Enter para voltar ao menu...")

# --- 3. FUNÇÃO PRINCIPAL (A Orquestradora) ---

def main():
    hoje_formatado = datetime.datetime.now().strftime("%d/%m/%Y")
    tarefas_a_fazer = []
    tarefas_em_execucao = []
    tarefas_concluidas = []

    while True:
        mostrar_dashboard(hoje_formatado, tarefas_a_fazer, tarefas_em_execucao, tarefas_concluidas)
        mostrar_menu()
        
        escolha = input("Escolha uma opção (1-5): ")
        print()

        if escolha == '1':
            adicionar_nova_tarefa(tarefas_a_fazer)
        
        elif escolha == '2':
            ativar_tarefa(tarefas_a_fazer, tarefas_em_execucao)

        elif escolha == '3':
            concluir_tarefa(tarefas_em_execucao, tarefas_concluidas)
        
        elif escolha == '4':
            mostrar_relatorio_console(hoje_formatado, tarefas_a_fazer, tarefas_em_execucao, tarefas_concluidas)
        
        elif escolha == '5':
            print("Saindo do Gerador de Relatórios...")
            break
        
        else:
            print("ERRO: Opção inválida.")
            input("Pressione Enter para tentar novamente...")

    print("Programa finalizado.")

# --- 4. PONTO DE ENTRADA ---
if __name__ == "__main__":
    main()