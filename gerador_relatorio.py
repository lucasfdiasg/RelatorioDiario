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

def mostrar_dashboard(data, a_fazer, em_execucao, concluidas, prorrogadas):
    """Mostra o painel principal com todas as 4 listas e emojis."""
    limpar_tela()
    print(f"--- GERADOR DE RELATÓRIOS --- Dia: {data} ---")
    
    print("\n[ ⏲️ A FAZER ]:")
    if not a_fazer:
        print("- Vazio")
    else:
        for i, tarefa in enumerate(a_fazer, start=1):
            print(f"  [{i}] {tarefa}")
            
    print("\n[ ✨ EM EXECUÇÃO ]:")
    if not em_execucao:
        print("- Vazio")
    else:
        for i, tarefa in enumerate(em_execucao, start=1):
            print(f"  [{i}] {tarefa}")

    print("\n[ ➡️ PRORROGADAS (para amanhã) ]:")
    if not prorrogadas:
        print("- Vazio")
    else:
        for i, tarefa in enumerate(prorrogadas, start=1):
            print(f"  [{i}] {tarefa}")

    print("\n[ ✅ CONCLUÍDAS ]:")
    if not concluidas:
        print("- Vazio")
    else:
        for tarefa in concluidas:
            print(f"  [✓] {tarefa}") # Note: Sem índice numérico
    
    print("-" * 40)

def mostrar_menu():
    """Imprime o novo menu de opções com 7 itens."""
    print("MENU DE OPÇÕES:")
    print("[1] Adicionar nova tarefa (em 'A Fazer')")
    print("[2] Ativar tarefa (Mover de 'A Fazer' -> 'Em Execução')")
    print("[3] Concluir tarefa (Mover de 'Em Execução' -> 'Concluídas')")
    print("[4] Prorrogar tarefa (Mover de 'A Fazer' -> 'Prorrogadas')")
    # (NOVA OPÇÃO)
    print("[5] Excluir Tarefa")
    # (RENUMERADO)
    print("[6] Salvar Relatório Final (em .txt)")
    print("[7] Sair")

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

def excluir_tarefa(a_fazer, em_execucao, prorrogadas):
    """
    (NOVO) Pergunta ao usuário qual lista e qual item ele deseja excluir.
    """
    print("--- Excluir Tarefa Permanentemente ---")
    print("De qual lista você deseja excluir?")
    print("[1] ⏲️ A Fazer")
    print("[2] ✨ Em Execução")
    print("[3] ➡️ Prorrogadas")
    print("[C] Cancelar")
    
    escolha_lista = input("Escolha a lista (1, 2, 3 ou C): ").strip().lower()

    lista_alvo = None
    nome_lista = ""

    if escolha_lista == '1':
        lista_alvo = a_fazer
        nome_lista = "A Fazer"
    elif escolha_lista == '2':
        lista_alvo = em_execucao
        nome_lista = "Em Execução"
    elif escolha_lista == '3':
        lista_alvo = prorrogadas
        nome_lista = "Prorrogadas"
    elif escolha_lista == 'c':
        print("Operação cancelada.")
        input("Pressione Enter para continuar...")
        return
    else:
        print("ERRO: Lista inválida.")
        input("Pressione Enter para continuar...")
        return
    
    # Verifica se a lista escolhida está vazia
    if not lista_alvo:
        print(f"A lista '[{nome_lista}]' já está vazia. Nada para excluir.")
        input("Pressione Enter para continuar...")
        return
        
    # Se a lista não estiver vazia, pede o índice
    try:
        idx_str = input(f"Digite o NÚMERO da tarefa na lista '[{nome_lista}]' que deseja EXCLUIR: ")
        idx = int(idx_str) - 1
        if idx < 0: raise IndexError
        
        # O '.pop()' remove o item e o retorna,
        # permitindo-nos mostrar qual tarefa foi removida.
        tarefa_excluida = lista_alvo.pop(idx)
        print(f"\nSucesso! Tarefa '{tarefa_excluida}' foi EXCLUÍDA permanentemente.")
        
    except (ValueError, IndexError):
        print("ERRO: Número inválido. Nenhuma tarefa foi excluída.")
    
    input("Pressione Enter para continuar...")


def salvar_relatorio_arquivo(data, a_fazer, em_execucao, concluidas, prorrogadas):
    """Pega todos os dados das 4 listas e salva em um arquivo de texto."""
    limpar_tela()
    print("--- Salvando Relatório Final ---")
    nome_arquivo = f"Relatorio_{data.replace('/', '-')}.txt"
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

    tarefas_a_fazer = []
    tarefas_em_execucao = []
    tarefas_concluidas = []
    tarefas_prorrogadas = []

    while True:
        mostrar_dashboard(hoje_formatado, tarefas_a_fazer, tarefas_em_execucao, tarefas_concluidas, tarefas_prorrogadas)
        mostrar_menu()
        
        escolha = input("Escolha uma opção (1-7): ")
        print()

        if escolha == '1':
            adicionar_nova_tarefa(tarefas_a_fazer)
        
        elif escolha == '2':
            ativar_tarefa(tarefas_a_fazer, tarefas_em_execucao)

        elif escolha == '3':
            concluir_tarefa(tarefas_em_execucao, tarefas_concluidas)
        
        elif escolha == '4':
            prorrogar_tarefa(tarefas_a_fazer, tarefas_prorrogadas)
        
        elif escolha == '5':
            
            excluir_tarefa(tarefas_a_fazer, tarefas_em_execucao, tarefas_prorrogadas)
        
        elif escolha == '6':
            salvar_relatorio_arquivo(hoje_formatado, tarefas_a_fazer, tarefas_em_execucao, tarefas_concluidas, tarefas_prorrogadas)
    
        elif escolha == '7':
            print("Saindo do Gerador de Relatórios...")
            break
        
        else:
            print("ERRO: Opção inválida.")
            input("Pressione Enter para tentar novamente...")

    print("Programa finalizado.")

# --- 4. PONTO DE ENTRADA ---
if __name__ == "__main__":
    main()