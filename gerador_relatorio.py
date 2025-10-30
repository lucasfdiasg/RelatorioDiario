import datetime

# --- 1. FUNÇÕES-ASSISTENTES (Definidas no nível principal) ---
# Agora a 'main' e qualquer outra função podem "enxergar" e usar estas.

def adicionar_tarefa(lista_pendentes):
    """Pede ao usuário e adiciona uma tarefa na lista de pendentes."""
    print("--- ADICIONAR TAREFA PENDENTE ---")
    tarefa = input("Descreva a tarefa pendente: ")
    lista_pendentes.append(tarefa)
    print("Tarefa pendente adicionada com sucesso!")

def adicionar_tarefa_concluida(lista_concluidas):
    """Pede ao usuário e adiciona uma tarefa na lista de concluídas."""
    print("--- ADICIONAR TAREFA CONCLUÍDA ---")
    tarefa = input("Descreva a tarefa concluída: ")
    lista_concluidas.append(tarefa)
    print("Tarefa concluída adicionada com sucesso!")

def mostrar_relatorio(data, concluidas, pendentes, total):
    """Imprime o relatório formatado no console."""
    # Renomeei seu 'mostrar_relatorio' para ser mais claro
    print(f"\n--- PRÉVIA DO RELATÓRIO - {data} ---")
    print(f"Total de Tarefas: {total}")

    print ("\nTarefas Concluídas:")
    if not concluidas:
        print("- Nenhuma tarefa concluída.")
    else:
        for tarefa in concluidas:
            print(f"- {tarefa}")
    
    print("\nTarefas Pendentes:")
    if not pendentes:
        print("- Nenhuma tarefa pendente.")
    else:
        for tarefa in pendentes:
            print(f"- {tarefa}")
    
    print("\n(Fim da prévia do relatório)")

def menu():
    """Apenas imprime as opções do menu."""
    print("\nMENU DE OPÇÕES:")
    print("[1] - Adicionar Tarefa Pendente")
    print("[2] - Adicionar Tarefa Concluída")
    print("[3] - Gerar Relatório (no console)")
    print("[4] - Sair")

# --- 2. FUNÇÃO PRINCIPAL (A Orquestradora) ---
# Esta é a ÚNICA função 'main'. Ela 'orquestra' as outras.

def main():

    # -- CONFIGURAÇÕES INICIAIS --
    hoje_formatado = datetime.datetime.now().strftime("%d/%m/%Y")
    print("Gerador de Relatórios - Iniciado em", hoje_formatado)

    tarefas_concluidas = []
    tarefas_pendentes = []
    # Removemos o 'total_tarefas = 0' daqui, 
    # pois é melhor calcular o total na hora (como você fez na opção 3).

    while True:
        menu() # Chama a função-assistente 'menu'
        escolha = input("Escolha uma opção: ")
        print()

        if escolha == "1":
            # Chama a função-assistente de adicionar
            adicionar_tarefa(tarefas_pendentes)

        elif escolha == "2":
            adicionar_tarefa_concluida(tarefas_concluidas)
        
        elif escolha == "3":
            # Calcula o total na hora
            total_tarefas = len(tarefas_concluidas) + len(tarefas_pendentes)
            # Chama a função-assistente de mostrar relatório
            mostrar_relatorio(hoje_formatado, tarefas_concluidas, tarefas_pendentes, total_tarefas)
        
        elif escolha == "4":
            print("Encerrando o Gerador de Relatórios. Até mais!")
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")
        
        print("-" * 20) # Separador

    print("\nGerador de Relatórios - Finalizado.")

# --- 3. PONTO DE ENTRADA (O "Botão de Ligar") ---
# Fica no nível principal, chamando a 'main' orquestradora.
if __name__ == "__main__":
    main()