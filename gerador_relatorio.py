
import datetime

def main():
    """
    Função principal do nosso aplicativo.
    Toda a lógica do menu e das tarefas acontece aqui dentro.
    """
    
    # -- CONFIGURAÇÕES INICIAIS --
    hoje_formatado = datetime.datetime.now().strftime("%d/%m/%Y")

    print("Gerador de Relatórios - Iniciado em", hoje_formatado)

    tarefas_concluidas = []
    tarefas_pendentes = []
    total_tarefas = 0

    while True:
        print("\nMENU DE OPÇÕES:")
        print("[1] - Adicionar Tarefa Pendente")
        print("[2] - Adicionar Tarefa Concluída")
        print("[3] - Gerar Relatório (no console)")
        print("[4] - Sair")

        escolha = input("Escolha uma opção: ")
        print()

        if escolha == "1":
            print("--- ADICIONAR TAREFA PENDENTE ---")
            tarefa = input("Descreva a tarefa pendente: ")
            
        
            tarefas_pendentes.append(tarefa) 
            total_tarefas += 1
            print("Tarefa pendente adicionada com sucesso!")
        
        elif escolha == "2":
            print("--- ADICIONAR TAREFA CONCLUÍDA ---")
            tarefa = input("Descreva a tarefa concluída: ")
            
            tarefas_concluidas.append(tarefa)
            total_tarefas += 1
            print("Tarefa concluída adicionada com sucesso!")
        
        elif escolha == "3":
            print("--- GERAR RELATÓRIO (Prévia) ---")
            print(f"\nRELATÓRIO DE TAREFAS - {hoje_formatado}")
            print(f"Total de Tarefas: {total_tarefas}")
            
       
            print("\nTarefas Concluídas:")
            if not tarefas_concluidas:
                print("- Nenhuma tarefa concluída.")
            else:
                for tarefa in tarefas_concluidas:
                    print(f"- {tarefa}")
            
            print("\nTarefas Pendentes:")
            if not tarefas_pendentes:
                print("- Nenhuma tarefa pendente.")
            else:
                for tarefa in tarefas_pendentes:
                    print(f"- {tarefa}")
            
            print("\n(Fim da prévia do relatório)")

        elif escolha == "4":
            print("Saindo do gerador de relatórios. Até mais!")
            break

        else:
            print("ERRO: Opção inválida. Por favor, digite 1, 2, 3 ou 4.")
        
        print("-" * 20)


    # --- FIM DO PROGRAMA ---
  
    print("\nPrograma encerrado.")


if __name__ == "__main__":
    main()