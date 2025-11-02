import datetime
import os
import platform 


class Tarefa:
    def __init__(self, titulo, descricao=""):

        self.titulo = titulo
        self.descricao = descricao
        self.subtarefas = []

    def adicionar_subtarefa(self, sub_titulo):
        if sub_titulo:
            self.subtarefas.append(sub_titulo)
    
    def __str__(self):
        return self.titulo
    
def limpar_tela():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def mostrar_dashboard(data, a_fazer, em_execucao, concluidas, prorrogadas):
    limpar_tela()
    print(f"--- GERADOR DE RELATÓRIOS --- Dia: {data} ---")
    print("\n[ ⏲️ - A FAZER ]:")
    if not a_fazer:
        print("- Vazio")
    else:
        for i, tarefa_obj in enumerate(a_fazer, start=1):
            print(f"\n  [{i}] {tarefa_obj.titulo}")
            
            if tarefa_obj.descricao:
                print(f"      Descrição: {tarefa_obj.descricao}")
                
            if tarefa_obj.subtarefas:
                print(f"      Sub-tarefas:")
                for sub in tarefa_obj.subtarefas:
                    print(f"        - {sub}")
    print("\n[ ✨ - EM EXECUÇÃO ]:")
    if not em_execucao:
        print("- Vazio")
    else:
        for i, tarefa_obj in enumerate(em_execucao, start=1):
            print(f"\n  [{i}] {tarefa_obj.titulo}")
            if tarefa_obj.descricao:
                print(f"      Descrição: {tarefa_obj.descricao}")
            if tarefa_obj.subtarefas:
                print(f"      Sub-tarefas:")
                for sub in tarefa_obj.subtarefas:
                    print(f"        - {sub}")
    print("\n[ ➡️ - PRORROGADAS (para amanhã) ]:")
    if not prorrogadas:
        print("- Vazio")
    else:
        for i, tarefa_obj in enumerate(prorrogadas, start=1):
            print(f"\n  [{i}] {tarefa_obj.titulo}")
            if tarefa_obj.descricao:
                print(f"      Descrição: {tarefa_obj.descricao}")
    print("\n[ ✅ - CONCLUÍDAS ]:")
    if not concluidas:
        print("- Vazio")
    else:
        for tarefa_obj in concluidas:
            print(f"  [✓] {tarefa_obj.titulo}")
    
    print("\n" + "-" * 40)

def mostrar_menu():
    """Imprime o menu de opções (sem mudanças aqui)."""
    print("MENU DE OPÇÕES:")
    print("[1] Adicionar nova tarefa (em 'A Fazer')")
    print("[2] Ativar tarefa (Mover de 'A Fazer' -> 'Em Execução')")
    print("[3] Concluir tarefa (Mover de 'Em Execução' -> 'Concluídas')")
    print("[4] Prorrogar tarefa (Mover de 'A Fazer' -> 'Prorrogadas')")
    print("[5] Excluir Tarefa")
    print("[6] Salvar Relatório Final (em .txt)")
    print("[7] Sair")

def adicionar_nova_tarefa(lista_a_fazer):
    print("--- Adicionar Nova Tarefa ---")
    titulo = input("Qual o TÍTULO da tarefa? (Obrigatório): ")
    if not titulo:
        print("ERRO: O título não pode ser vazio.")
        input("Pressione Enter para continuar...")
        return

    descricao = input("Adicione uma DESCRIÇÃO (Opcional, tecle Enter para pular): ")
    
    nova_tarefa = Tarefa(titulo, descricao)
    
    print("\nAdicione SUB-TAREFAS (Opcional, tecle Enter para pular):")
    print("(Deixe em branco e tecle Enter quando terminar de adicionar)")
    
    contador_sub = 1
    while True:
        sub_titulo = input(f"  Sub-tarefa {contador_sub}: ")
        if not sub_titulo:
            break 
            
        nova_tarefa.adicionar_subtarefa(sub_titulo)
        contador_sub += 1
    lista_a_fazer.append(nova_tarefa)
    print(f"\nTarefa '{nova_tarefa.titulo}' e suas sub-tarefas foram adicionadas!")
    input("Pressione Enter para continuar...")

def ativar_tarefa(lista_a_fazer, lista_em_execucao):

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
        
        print(f"Tarefa '{tarefa_movida.titulo}' movida para 'Em Execução'!")
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
        if idx < 0: raise IndexError
        
        tarefa_movida = lista_em_execucao.pop(idx)
        lista_concluidas.append(tarefa_movida)
        
        # (MUDANÇA)
        print(f"Tarefa '{tarefa_movida.titulo}' marcada como 'Concluída'!")
    except (ValueError, IndexError):
        print("ERRO: Número inválido. Nenhuma tarefa foi movida.")
    input("Pressione Enter para continuar...")

def prorrogar_tarefa(lista_a_fazer, lista_prorrogadas):
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
        
        print(f"Tarefa '{tarefa_movida.titulo}' movida para 'Prorrogadas'!")
    except (ValueError, IndexError):
        print("ERRO: Número inválido. Nenhuma tarefa foi movida.")
    input("Pressione Enter para continuar...")

def excluir_tarefa(a_fazer, em_execucao, prorrogadas):
    """(MUDANÇA PEQUENA) Só muda a mensagem de print."""
    print("--- Excluir Tarefa Permanentemente ---")
    print("De qual lista você deseja excluir?")
    print("[1] ⏲️ - A Fazer")
    print("[2] ✨ - Em Execução")
    print("[3] ➡️ - Prorrogadas")
    print("[C] Cancelar")
    
    escolha_lista = input("Escolha a lista (1, 2, 3 ou C): ").strip().lower()
    lista_alvo, nome_lista = None, ""

    if escolha_lista == '1': lista_alvo, nome_lista = a_fazer, "A Fazer"
    elif escolha_lista == '2': lista_alvo, nome_lista = em_execucao, "Em Execução"
    elif escolha_lista == '3': lista_alvo, nome_lista = prorrogadas, "Prorrogadas"
    elif escolha_lista == 'c':
        print("Operação cancelada.")
        input("Pressione Enter para continuar...")
        return
    else:
        print("ERRO: Lista inválida.")
        input("Pressione Enter para continuar...")
        return
    
    if not lista_alvo:
        print(f"A lista '[{nome_lista}]' já está vazia. Nada para excluir.")
        input("Pressione Enter para continuar...")
        return
        
    try:
        idx_str = input(f"Digite o NÚMERO da tarefa na lista '[{nome_lista}]' que deseja EXCLUIR: ")
        idx = int(idx_str) - 1
        if idx < 0: raise IndexError
        
        tarefa_excluida = lista_alvo.pop(idx)
        print(f"\nSucesso! Tarefa '{tarefa_excluida.titulo}' foi EXCLUÍDA permanentemente.")
        
    except (ValueError, IndexError):
        print("ERRO: Número inválido. Nenhuma tarefa foi excluída.")
    
    input("Pressione Enter para continuar...")


def salvar_relatorio_arquivo(data, a_fazer, em_execucao, concluidas, prorrogadas):
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
                for tarefa_obj in concluidas: 
                    f.write(f"- {tarefa_obj.titulo}\n")
            
            f.write("\n[ ✨ TAREFAS EM EXECUÇÃO ]\n")
            if not em_execucao: f.write("- Nenhuma\n")
            else:
                for tarefa_obj in em_execucao: 
                    f.write(f"\n- {tarefa_obj.titulo}\n")
                    if tarefa_obj.descricao: f.write(f"  Descrição: {tarefa_obj.descricao}\n")
                    if tarefa_obj.subtarefas:
                        f.write(f"  Sub-tarefas:\n")
                        for sub in tarefa_obj.subtarefas: f.write(f"    - {sub}\n")
            
            f.write("\n[ ⏲️ TAREFAS A FAZER ]\n")
            if not a_fazer: f.write("- Nenhuma\n")
            else:
                for tarefa_obj in a_fazer: 
                    f.write(f"\n- {tarefa_obj.titulo}\n")
                    if tarefa_obj.descricao: f.write(f"  Descrição: {tarefa_obj.descricao}\n")
                    if tarefa_obj.subtarefas:
                        f.write(f"  Sub-tarefas:\n")
                        for sub in tarefa_obj.subtarefas: f.write(f"    - {sub}\n")
            
            f.write("\n[ ➡️ TAREFAS PRORROGADAS (para o dia seguinte) ]\n")
            if not prorrogadas: f.write("- Nenhuma\n")
            else:
                for tarefa_obj in prorrogadas: 
                    f.write(f"\n- {tarefa_obj.titulo}\n")
                    if tarefa_obj.descricao: f.write(f"  Descrição: {tarefa_obj.descricao}\n")
            
            f.write("\n\n--- Fim do Relatório ---")
        
        print(f"\nSucesso! Relatório salvo como: {nome_arquivo}")
    except Exception as e:
        print(f"\nERRO: Não foi possível salvar o arquivo. Detalhe: {e}")

    input("\nPressione Enter para voltar ao menu...")


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
        elif escolha == '7Am':
            print("Saindo do Gerador de Relatórios...")
            break
        else:
            print("ERRO: Opção inválida.")
            input("Pressione Enter para tentar novamente...")

    print("Programa finalizado.")

if __name__ == "__main__":
    main()