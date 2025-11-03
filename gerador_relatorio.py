import datetime
import os
import platform 
import json
import time

class SubTarefa:
    def __init__(self, titulo, concluida=False):
        self.titulo = titulo
        self.concluida = concluida

    def to_dict(self):
        return {
            "titulo": self.titulo,
            "concluida": self.concluida
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            titulo=data.get("titulo", "Sem Título"),
            concluida=data.get("concluida", False)
        )
    
    def __str__(self):
        return self.titulo

class Tarefa:
    def __init__(self, titulo, subtarefas=None, periodo=None):
        self.titulo = titulo
        self.subtarefas = subtarefas if subtarefas is not None else []
        self.periodo = periodo

    def adicionar_subtarefa(self, sub_titulo):
        if sub_titulo:
            nova_subtarefa = SubTarefa(titulo=sub_titulo)
            self.subtarefas.append(nova_subtarefa)
    
    def __str__(self):
        return self.titulo 
        
    def to_dict(self):
        return {
            "titulo": self.titulo,
            "subtarefas": [s.to_dict() for s in self.subtarefas],
            "periodo": self.periodo
        }

    @classmethod
    def from_dict(cls, data):
        subtarefas_objs = [SubTarefa.from_dict(s) for s in data.get("subtarefas", [])]
        return cls(
            titulo=data.get("titulo", "Sem Título"),
            subtarefas=subtarefas_objs,
            periodo=data.get("periodo", None)
        )

NOME_ARQUIVO_PLANEJAMENTO = "planejamento_store.json"
NOME_ARQUIVO_REGRAS = "regras_recorrentes.json"

MAPA_DIAS_USUARIO_PARA_PYTHON = {
    2: 0, 3: 1, 4: 2, 5: 3, 6: 4, 7: 5, 1: 6  
}

MAPA_PYTHON_PARA_USUARIO_TEXTO = {
    0: "Seg (2)", 1: "Ter (3)", 2: "Qua (4)", 3: "Qui (5)", 4: "Sex (6)", 5: "Sab (7)", 6: "Dom (1)"
}

def carregar_regras():
    try:
        with open(NOME_ARQUIVO_REGRAS, "r", encoding="utf-8") as f:
            regras = json.load(f)
        return regras
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Erro ao carregar regras: {e}")
        return []

def salvar_regras(regras):
    try:
        with open(NOME_ARQUIVO_REGRAS, "w", encoding="utf-8") as f:
            json.dump(regras, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"ERRO ao salvar regras: {e}")

def carregar_planejamento(data_hoje_iso):
    print("Verificando planejamento anterior...")
    try:
        with open(NOME_ARQUIVO_PLANEJAMENTO, "r", encoding="utf-8") as f:
            dados = json.load(f)
        
        data_salva = dados.get("data_salva")
        
        tarefas_pendentes_carregadas = [Tarefa.from_dict(t) for t in dados.get("a_fazer", [])]
        tarefas_em_andamento_carregadas = [Tarefa.from_dict(t) for t in dados.get("em_execucao", [])]
        
        if data_salva == data_hoje_iso:
            print("Planejamento de hoje já está carregado. (App reaberto)")
            return tarefas_pendentes_carregadas, tarefas_em_andamento_carregadas, True
        else:
            print(f"Carregando planejamento salvo de {data_salva}...")
            if data_salva != data_hoje_iso:
                for t in tarefas_pendentes_carregadas + tarefas_em_andamento_carregadas:
                    t.periodo = None 
            return tarefas_pendentes_carregadas, tarefas_em_andamento_carregadas, False

    except FileNotFoundError:
        print("Nenhum arquivo de planejamento encontrado. Começando um novo dia.")
        return [], [], False
    except Exception as e:
        print(f"Erro ao carregar planejamento: {e}")
        return [], [], False

def salvar_planejamento(lista_pendentes, lista_em_andamento, data_hoje_iso):
    print("Salvando planejamento...")
    try:
        dados_a_fazer = [tarefa.to_dict() for tarefa in lista_pendentes]
        dados_em_execucao = [tarefa.to_dict() for tarefa in lista_em_andamento]
        
        dados_para_salvar = {
            "data_salva": data_hoje_iso,
            "a_fazer": dados_a_fazer,
            "em_execucao": dados_em_execucao
        }
        
        with open(NOME_ARQUIVO_PLANEJAMENTO, "w", encoding="utf-8") as f:
            json.dump(dados_para_salvar, f, indent=4, ensure_ascii=False)
            
        print(f"Planejamento salvo em {NOME_ARQUIVO_PLANEJAMENTO}.")
        
    except Exception as e:
        print(f"ERRO ao salvar planejamento: {e}")

def limpar_tela():
    if os.name == 'nt': os.system('cls')
    else: os.system('clear')

def mostrar_dashboard(data, pendentes, em_andamento, realizado):
    limpar_tela()
    print(f"--- GERADOR DE RELATÓRIOS --- Dia: {data} ---")
    
    print("\n[ ⏲️ PENDENTES (Planejamento) ]:")
    if not pendentes: print("- Vazio")
    else:
        for i, tarefa_obj in enumerate(pendentes, start=1):
            print(f"\n  [{i}] {tarefa_obj.titulo}")
            if tarefa_obj.subtarefas:
                print(f"      Sub-tarefas:")
                for j, sub in enumerate(tarefa_obj.subtarefas, start=1):
                    check = "✓" if sub.concluida else " "
                    print(f"        [{j}] [{check}] {sub.titulo}")
            
    print("\n[ ✨ EM ANDAMENTO ]:")
    if not em_andamento: print("- Vazio")
    else:
        for i, tarefa_obj in enumerate(em_andamento, start=1):
            periodo_str = f"({tarefa_obj.periodo})" if tarefa_obj.periodo else ""
            print(f"\n  [{i}] {tarefa_obj.titulo} {periodo_str}")
            if tarefa_obj.subtarefas:
                print(f"      Sub-tarefas:")
                for j, sub in enumerate(tarefa_obj.subtarefas, start=1):
                    check = "✓" if sub.concluida else " "
                    print(f"        [{j}] [{check}] {sub.titulo}")

    print("\n[ ✅ REALIZADO ]:")
    if not realizado: print("- Vazio")
    else:
        for tarefa_obj in realizado:
            periodo_str = f"({tarefa_obj.periodo})" if tarefa_obj.periodo else ""
            print(f"  [✓] {tarefa_obj.titulo} {periodo_str}")
    
    print("\n" + "-" * 40)

def mostrar_menu():
    print("MENU DE OPÇÕES:")
    print("[1] Adicionar nova tarefa")
    print("[2] Ativar tarefa (Mover de 'Pendentes' -> 'Em Andamento')")
    print("[3] Concluir tarefa (Mover de 'Em Andamento' -> 'Realizado')")
    print("[4] Gerenciar Sub-tarefas (Marcar/Desmarcar)")
    print("[5] Editar Tarefa (Título, Sub-tarefas)")
    print("[6] Tarefas Recorrentes")
    print("[7] Excluir Tarefa")
    print("[8] Gerar Relatório do Dia e Salvar Planejamento")
    print("[9] Sair (sem salvar relatório)")

def adicionar_nova_tarefa(lista_pendentes, lista_em_andamento, lista_realizado):
    print("--- Adicionar Nova Tarefa ---")
    titulo = input("Qual o TÍTULO da tarefa? (Obrigatório): ")
    if not titulo:
        print("ERRO: O título não pode ser vazio."); time.sleep(1); return
    
    nova_tarefa = Tarefa(titulo)
    
    print("\nAdicione SUB-TAREFAS (Opcional, deixe em branco para parar):")
    
    while True:
        sub_titulo = input("  > ")
        if not sub_titulo: break
        nova_tarefa.adicionar_subtarefa(sub_titulo)
    
    print("\n--- Onde adicionar esta tarefa? ---")
    print("[1] ⏲️ Pendentes (Planejamento)")
    print("[2] ✨ Em Andamento")
    print("[3] ✅ Realizado")
    print("[C] Cancelar Adição")
    
    escolha_lista = input("Escolha a lista (1, 2, 3 ou C): ").strip().lower()
    
    if escolha_lista == '1':
        lista_pendentes.append(nova_tarefa)
        print(f"\nTarefa '{nova_tarefa.titulo}' adicionada em 'Pendentes'!")
        
    elif escolha_lista == '2':
        periodo = perguntar_periodo()
        nova_tarefa.periodo = periodo
        lista_em_andamento.append(nova_tarefa)
        print(f"\nTarefa '{nova_tarefa.titulo}' adicionada em 'Em Andamento' ({periodo})!")
        
    elif escolha_lista == '3':
        periodo = perguntar_periodo()
        nova_tarefa.periodo = periodo
        lista_realizado.append(nova_tarefa)
        print(f"\nTarefa '{nova_tarefa.titulo}' adicionada em 'Realizado' ({periodo})!")
        
    elif escolha_lista == 'c':
        print("\nAdição de tarefa cancelada.")
        
    else:
        print("\nOpção inválida. A tarefa não foi adicionada.")
        
    time.sleep(1)


def perguntar_periodo():
    while True:
        periodo = input("Período: [M]anhã ou [T]arde? ").strip().upper()
        if periodo in ['M', 'T']:
            return periodo
        print("Opção inválida. Digite 'M' ou 'T'.")

def ativar_tarefa(lista_pendentes, lista_em_andamento):
    print("--- Ativar Tarefa (Mover para 'Em Andamento') ---")
    if not lista_pendentes:
        print("Não há tarefas 'Pendentes' para ativar."); time.sleep(1); return
    try:
        idx_str = input("Digite o NÚMERO da tarefa 'Pendentes' que deseja ativar: ")
        idx = int(idx_str) - 1 
        if idx < 0: raise IndexError

        periodo = perguntar_periodo()
        
        tarefa_movida = lista_pendentes.pop(idx) 
        tarefa_movida.periodo = periodo 
        lista_em_andamento.append(tarefa_movida)
        
        print(f"Tarefa '{tarefa_movida.titulo}' movida para 'Em Andamento' ({periodo})!")
    except (ValueError, IndexError):
        print("ERRO: Número inválido.")
    time.sleep(1)

def concluir_tarefa(lista_em_andamento, lista_realizado):
    print("--- Concluir Tarefa ---")
    if not lista_em_andamento:
        print("Não há tarefas 'Em Andamento' para concluir."); time.sleep(1); return
    try:
        idx_str = input("Digite o NÚMERO da tarefa 'Em Andamento' que deseja concluir: ")
        idx = int(idx_str) - 1 
        if idx < 0: raise IndexError
        
        periodo = perguntar_periodo()
        
        tarefa_movida = lista_em_andamento.pop(idx)
        tarefa_movida.periodo = periodo 
        lista_realizado.append(tarefa_movida)
        print(f"Tarefa '{tarefa_movida.titulo}' marcada como 'Realizado' ({periodo})!")
    except (ValueError, IndexError):
        print("ERRO: Número inválido.")
    time.sleep(1)

def excluir_tarefa(pendentes, em_andamento):
    print("--- Excluir Tarefa Permanentemente ---")
    print("De qual lista você deseja excluir?")
    print("[1] ⏲️ Pendentes")
    print("[2] ✨ Em Andamento")
    print("[C] Cancelar")
    
    escolha_lista = input("Escolha a lista (1, 2 ou C): ").strip().lower()
    lista_alvo, nome_lista = None, ""

    if escolha_lista == '1': lista_alvo, nome_lista = pendentes, "Pendentes"
    elif escolha_lista == '2': lista_alvo, nome_lista = em_andamento, "Em Andamento"
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

def gerenciar_subtarefas(pendentes, em_andamento, lista_realizado):
    print("--- Gerenciar Sub-tarefas (Marcar/Desmarcar) ---")
    print("De qual lista você quer gerenciar as sub-tarefas?")
    print("[1] ⏲️ Pendentes")
    print("[2] ✨ Em Andamento")
    print("[C] Cancelar")
    
    escolha_lista = input("Escolha a lista (1, 2 ou C): ").strip().lower()
    lista_alvo, nome_lista = None, ""

    if escolha_lista == '1': lista_alvo, nome_lista = pendentes, "Pendentes"
    elif escolha_lista == '2': lista_alvo, nome_lista = em_andamento, "Em Andamento"
    elif escolha_lista == 'c': print("Operação cancelada."); time.sleep(1); return
    else: print("ERRO: Lista inválida."); time.sleep(1); return

    if not lista_alvo:
        print(f"A lista '[{nome_lista}]' está vazia."); time.sleep(1); return

    try:
        idx_tarefa_str = input(f"Digite o NÚMERO da tarefa principal na lista '[{nome_lista}']: ")
        idx_tarefa = int(idx_tarefa_str) - 1
        if idx_tarefa < 0: raise IndexError
        
        tarefa_selecionada = lista_alvo[idx_tarefa]
        
        if not tarefa_selecionada.subtarefas:
            print(f"A tarefa '{tarefa_selecionada.titulo}' não possui sub-tarefas."); time.sleep(1); return

        print(f"\n--- Gerenciando sub-tarefas de: {tarefa_selecionada.titulo} ---")
        for i, sub in enumerate(tarefa_selecionada.subtarefas, start=1):
            check = "✓" if sub.concluida else " "
            print(f"  [{i}] [{check}] {sub.titulo}")
        
        idx_sub_str = input("Digite o NÚMERO da sub-tarefa para marcar/desmarcar (ou C para cancelar): ").strip().lower()
        if idx_sub_str == 'c':
            print("Operação cancelada."); time.sleep(1); return
            
        idx_sub = int(idx_sub_str) - 1
        if idx_sub < 0: raise IndexError
        
        sub_selecionada = tarefa_selecionada.subtarefas[idx_sub]
        
        sub_selecionada.concluida = not sub_selecionada.concluida
        status_str = "CONCLUÍDA" if sub_selecionada.concluida else "PENDENTE"
        print(f"\nSucesso! Sub-tarefa '{sub_selecionada.titulo}' marcada como {status_str}.")

        if all(s.concluida for s in tarefa_selecionada.subtarefas):
            print(f"\nAVISO: Todas as sub-tarefas de '{tarefa_selecionada.titulo}' estão concluídas.")
            time.sleep(1)
            resposta = input("Deseja mover a tarefa principal para '✅ Realizado'? [S/N]: ").strip().upper()
            if resposta == 'S':
                periodo = perguntar_periodo()
                tarefa_selecionada.periodo = periodo
                lista_realizado.append(tarefa_selecionada)
                lista_alvo.pop(idx_tarefa)
                print(f"Tarefa '{tarefa_selecionada.titulo}' movida para 'Realizado'!")

    except (ValueError, IndexError):
        print("ERRO: Número inválido.")
    
    time.sleep(1)

def editar_tarefa(pendentes, em_andamento):
    print("--- Editar Tarefa ---")
    print("De qual lista você deseja editar a tarefa?")
    print("[1] ⏲️ Pendentes")
    print("[2] ✨ Em Andamento")
    print("[C] Cancelar")
    
    escolha_lista = input("Escolha a lista (1, 2 ou C): ").strip().lower()
    lista_alvo, nome_lista = None, ""

    if escolha_lista == '1': lista_alvo, nome_lista = pendentes, "Pendentes"
    elif escolha_lista == '2': lista_alvo, nome_lista = em_andamento, "Em Andamento"
    elif escolha_lista == 'c': print("Operação cancelada."); time.sleep(1); return
    else: print("ERRO: Lista inválida."); time.sleep(1); return

    if not lista_alvo:
        print(f"A lista '[{nome_lista}]' está vazia."); time.sleep(1); return

    try:
        idx_tarefa_str = input(f"Digite o NÚMERO da tarefa principal na lista '[{nome_lista}']: ")
        idx_tarefa = int(idx_tarefa_str) - 1
        if idx_tarefa < 0: raise IndexError
        
        tarefa_selecionada = lista_alvo[idx_tarefa]

        while True:
            limpar_tela()
            print(f"--- Editando Tarefa: {tarefa_selecionada.titulo} ---")
            print(f"[1] Editar Título Principal ({tarefa_selecionada.titulo})")
            print("\nSub-tarefas:")
            if not tarefa_selecionada.subtarefas:
                print("- Nenhuma -")
            for i, sub in enumerate(tarefa_selecionada.subtarefas, start=1):
                check = "✓" if sub.concluida else " "
                print(f"  [{i}] [{check}] {sub.titulo}")
            
            print("\n[2] Adicionar nova Sub-tarefa")
            print("[3] Editar texto de uma Sub-tarefa")
            print("[4] Excluir uma Sub-tarefa")
            print("[V] Voltar ao menu principal")
            
            escolha_edicao = input("\nEscolha uma opção de edição: ").strip().lower()

            if escolha_edicao == '1':
                novo_titulo = input(f"Digite o novo TÍTULO (anterior: {tarefa_selecionada.titulo}): ")
                if novo_titulo:
                    tarefa_selecionada.titulo = novo_titulo
                    print("Título atualizado!")
                else:
                    print("Título não pode ser vazio. Nenhuma alteração feita.")
                time.sleep(1)
            
            elif escolha_edicao == '2':
                novo_sub_titulo = input("Digite a nova Sub-tarefa: ")
                if novo_sub_titulo:
                    tarefa_selecionada.adicionar_subtarefa(novo_sub_titulo)
                    print("Sub-tarefa adicionada!")
                time.sleep(1)

            elif escolha_edicao == '3':
                if not tarefa_selecionada.subtarefas:
                    print("Não há sub-tarefas para editar."); time.sleep(1); continue
                try:
                    idx_sub_str = input("Digite o NÚMERO da sub-tarefa para EDITAR: ")
                    idx_sub = int(idx_sub_str) - 1
                    sub_para_editar = tarefa_selecionada.subtarefas[idx_sub]
                    novo_sub_titulo = input(f"Digite o novo texto (anterior: {sub_para_editar.titulo}): ")
                    if novo_sub_titulo:
                        sub_para_editar.titulo = novo_sub_titulo
                        print("Sub-tarefa atualizada!")
                    else:
                        print("Texto não pode ser vazio. Nenhuma alteração feita.")
                except (ValueError, IndexError):
                    print("Número de sub-tarefa inválido.")
                time.sleep(1)

            elif escolha_edicao == '4':
                if not tarefa_selecionada.subtarefas:
                    print("Não há sub-tarefas para excluir."); time.sleep(1); continue
                try:
                    idx_sub_str = input("Digite o NÚMERO da sub-tarefa para EXCLUIR: ")
                    idx_sub = int(idx_sub_str) - 1
                    sub_excluida = tarefa_selecionada.subtarefas.pop(idx_sub)
                    print(f"Sub-tarefa '{sub_excluida.titulo}' excluída!")
                except (ValueError, IndexError):
                    print("Número de sub-tarefa inválido.")
                time.sleep(1)

            elif escolha_edicao == 'v':
                print("Saindo do modo de edição...")
                time.sleep(1)
                break
            
            else:
                print("Opção de edição inválida.")
                time.sleep(1)

    except (ValueError, IndexError):
        print("ERRO: Número da tarefa principal inválido.")
        time.sleep(1)

def gerenciar_regras_menu(regras):
    while True:
        limpar_tela()
        print("--- Tarefas Recorrentes ---")
        
        if not regras:
            print("\nNenhuma regra de recorrência cadastrada.")
        else:
            print("\nRegras Atuais:")
            for i, regra_info in enumerate(regras, start=1):
                titulo = regra_info['modelo']['titulo']
                regra = regra_info['regra']
                if regra['tipo'] == 'diaria':
                    print(f"  [{i}] '{titulo}' (Diária)")
                elif regra['tipo'] == 'semanal':
                    dia_texto = MAPA_PYTHON_PARA_USUARIO_TEXTO.get(regra['dia_semana'], "Inválido")
                    print(f"  [{i}] '{titulo}' (Semanal: toda {dia_texto})")
                elif regra['tipo'] == 'mensal':
                    print(f"  [{i}] '{titulo}' (Mensal: todo dia {regra['dia_mes']})")

        print("\n[1] Adicionar Nova Regra")
        print("[2] Editar Regra")
        print("[3] Excluir Regra")
        print("[V] Voltar ao Menu Principal")
        
        escolha = input("Escolha uma opção: ").strip().lower()

        if escolha == '1':
            adicionar_regra_recorrente(regras)
            salvar_regras(regras)
        elif escolha == '2':
            editar_regra_recorrente(regras)
            salvar_regras(regras)
        elif escolha == '3':
            excluir_regra_recorrente(regras)
            salvar_regras(regras)
        elif escolha == 'v':
            break
        else:
            print("Opção inválida.")
            time.sleep(1)

def adicionar_regra_recorrente(regras):
    print("\n--- Adicionar Nova Regra Recorrente ---")
    titulo = input("Qual o TÍTULO da tarefa modelo? (Obrigatório): ")
    if not titulo:
        print("ERRO: O título não pode ser vazio."); time.sleep(1); return

    modelo_tarefa = Tarefa(titulo)
    print("\nAdicione SUB-TAREFAS modelo (Opcional, deixe em branco para parar):")
    while True:
        sub_titulo = input("  > ")
        if not sub_titulo: break
        modelo_tarefa.adicionar_subtarefa(sub_titulo)

    nova_regra_dict = _perguntar_detalhes_regra()
    if nova_regra_dict is None:
        print("Criação de regra cancelada."); time.sleep(1); return

    regras.append({
        "modelo": modelo_tarefa.to_dict(),
        "regra": nova_regra_dict
    })
    print(f"\nRegra para '{titulo}' criada com sucesso!")
    time.sleep(1)

def _perguntar_detalhes_regra():
    print("\n--- Definir Regra de Recorrência ---")
    print("[1] Diária (Todo dia)")
    print("[2] Semanal (Um dia da semana)")
    print("[3] Mensal (Um dia do mês)")
    
    tipo_regra_str = input("Escolha o tipo (1, 2 ou 3): ").strip()
    
    if tipo_regra_str == '1':
        return {"tipo": "diaria"}
    elif tipo_regra_str == '2':
        try:
            dia_usuario = int(input("Digite o dia da semana (1=Dom, 2=Seg, 3=Ter, ..., 7=Sab): "))
            if dia_usuario in MAPA_DIAS_USUARIO_PARA_PYTHON:
                dia_semana_interno = MAPA_DIAS_USUARIO_PARA_PYTHON[dia_usuario]
                return {"tipo": "semanal", "dia_semana": dia_semana_interno}
            else:
                raise ValueError
        except ValueError:
            print("Dia da semana inválido."); return None
    elif tipo_regra_str == '3':
        try:
            dia_mes = int(input("Digite o dia do mês (1-31): "))
            if 1 <= dia_mes <= 31:
                return {"tipo": "mensal", "dia_mes": dia_mes}
            else:
                raise ValueError
        except ValueError:
            print("Dia do mês inválido."); return None
    else:
        print("Tipo de regra inválido."); return None

def editar_regra_recorrente(regras):
    if not regras:
        print("Não há regras para editar."); time.sleep(1); return

    print("\n--- Editar Regra Recorrente ---")
    try:
        idx_str = input("Digite o NÚMERO da regra que deseja EDITAR: ")
        idx = int(idx_str) - 1
        if not (0 <= idx < len(regras)):
            raise IndexError
        
        regra_selecionada = regras[idx]
        titulo_atual = regra_selecionada['modelo']['titulo']
        
        print(f"\n--- Editando Regra: {titulo_atual} ---")
        print("[1] Editar Título do Modelo")
        print("[2] Editar Regra de Recorrência (Tipo/Dia)")
        print("[V] Voltar")
        
        escolha = input("O que deseja editar? ").strip().lower()

        if escolha == '1':
            novo_titulo = input(f"Digite o novo TÍTULO (anterior: {titulo_atual}): ")
            if novo_titulo:
                regra_selecionada['modelo']['titulo'] = novo_titulo
                print("Título do modelo atualizado!")
            else:
                print("Título não pode ser vazio. Nenhuma alteração feita.")
        
        elif escolha == '2':
            print("Por favor, defina a NOVA regra de recorrência.")
            nova_regra_dict = _perguntar_detalhes_regra()
            if nova_regra_dict:
                regra_selecionada['regra'] = nova_regra_dict
                print("Regra de recorrência atualizada!")
            else:
                print("Edição da regra cancelada.")
                
        elif escolha == 'v':
            return
        
        else:
            print("Opção inválida.")
        
    except (ValueError, IndexError):
        print("ERRO: Número inválido.")
    
    time.sleep(1)


def excluir_regra_recorrente(regras):
    if not regras:
        print("Não há regras para excluir."); time.sleep(1); return
    
    print("\n--- Excluir Regra Recorrente ---")
    try:
        idx_str = input("Digite o NÚMERO da regra que deseja EXCLUIR: ")
        idx = int(idx_str) - 1
        if 0 <= idx < len(regras):
            regra_excluida = regras.pop(idx)
            print(f"Regra para '{regra_excluida['modelo']['titulo']}' foi excluída.")
        else:
            raise IndexError
    except (ValueError, IndexError):
        print("ERRO: Número inválido.")
    time.sleep(1)


def gerar_relatorio_e_salvar_SIMPLES(data, pendentes, em_andamento, realizado, data_hoje_iso):
    limpar_tela()
    print("--- Gerando Relatório do Dia e Salvando Planejamento ---")
    
    data_simples_arquivo = datetime.datetime.now().strftime("%d-%m-%Y")
    nome_arquivo_relatorio = f"Relatorio_{data_simples_arquivo}.txt"

    realizado_manha = [t for t in realizado if t.periodo == 'M']
    realizado_tarde = [t for t in realizado if t.periodo == 'T']
    em_andamento_manha = [t for t in em_andamento if t.periodo == 'M']
    em_andamento_tarde = [t for t in em_andamento if t.periodo == 'T']
    
    def formatar_subtarefa_relatorio(subtarefa):
        check = "✅" if subtarefa.concluida else ""
        return f"\t\t- {subtarefa.titulo} {check}\n"

    try:
        with open(nome_arquivo_relatorio, "w", encoding="utf-8") as f:
            f.write("📄- *RELATÓRIO GERADO* -📄\n")
            f.write(f"# *Dia: {data}* #\n\n")
            
            f.write("+++++++\n|| MANHÃ ||\n=======\n\n")
            
            f.write("[ ✅ REALIZADO - MANHÃ ]\n")
            if not realizado_manha: f.write("- Nenhuma\n")
            for t in realizado_manha:
                f.write(f"+ {t.titulo} ✅\n")
                for s in t.subtarefas: f.write(formatar_subtarefa_relatorio(s))
            
            f.write("\n[ ✨ TAREFAS EM ANDAMENTO - MANHÃ ]\n")
            if not em_andamento_manha: f.write("- Nenhuma\n")
            for t in em_andamento_manha:
                f.write(f"+ {t.titulo}\n")
                for s in t.subtarefas: f.write(formatar_subtarefa_relatorio(s))
            
            f.write("\n\n+++++++\n|| TARDE ||\n=======\n\n")
            
            f.write("[ ✅ REALIZADO - TARDE ]\n")
            if not realizado_tarde: f.write("- Nenhuma\n")
            for t in realizado_tarde:
                f.write(f"+ {t.titulo} ✅\n")
                for s in t.subtarefas: f.write(formatar_subtarefa_relatorio(s))

            f.write("\n[ ✨ TAREFAS EM ANDAMENTO - TARDE ]\n")
            if not em_andamento_tarde: f.write("- Nenhuma\n")
            for t in em_andamento_tarde:
                f.write(f"+ {t.titulo}\n")
                for s in t.subtarefas: f.write(formatar_subtarefa_relatorio(s))

            f.write("\n\n=====================\nPLANEJAMENTO (Próximo Dia)\n=====================\n\n")
            
            if not pendentes and not em_andamento: 
                f.write("- Nada planejado.\n")
            
            if pendentes:
                f.write("[ ⏲️ PENDENTES ]\n")
                for t in pendentes:
                    f.write(f"+ {t.titulo}\n")
                    for s in t.subtarefas: f.write(formatar_subtarefa_relatorio(s).replace("✅", ""))
            
            if em_andamento:
                f.write("\n[ ✨ EM ANDAMENTO (A Continuar) ]\n")
                for t in em_andamento:
                    f.write(f"+ {t.titulo}\n")
                    for s in t.subtarefas: f.write(formatar_subtarefa_relatorio(s).replace("✅", ""))
            
        print(f"\nSucesso! Relatório do dia salvo como: {nome_arquivo_relatorio}")

        salvar_planejamento(pendentes, em_andamento, data_hoje_iso)
        
        pendentes.clear()
        em_andamento.clear()
        realizado.clear()
        
        print("\nRelatório gerado e planejamento salvo. O dia foi encerrado.")
        print("As listas foram limpas.")

    except Exception as e:
        print(f"\nERRO: Não foi possível gerar o relatório. Detalhe: {e}")

    input("\nPressione Enter para voltar ao menu...")


def verificar_e_injetar_recorrentes(regras, tarefas_pendentes, tarefas_em_andamento, hoje_obj):
    print("Verificando tarefas recorrentes...")
    
    dia_semana_hoje = hoje_obj.weekday()
    dia_mes_hoje = hoje_obj.day
    novas_tarefas_injetadas = []

    titulos_existentes = {t.titulo for t in tarefas_pendentes} | {t.titulo for t in tarefas_em_andamento}

    for regra_info in regras:
        regra = regra_info['regra']
        modelo = regra_info['modelo']
        titulo_modelo = modelo['titulo']
        
        disparar = False
        if regra['tipo'] == 'diaria':
            disparar = True
        elif regra['tipo'] == 'semanal' and regra['dia_semana'] == dia_semana_hoje:
            disparar = True
        elif regra['tipo'] == 'mensal' and regra['dia_mes'] == dia_mes_hoje:
            disparar = True
        
        if disparar and (titulo_modelo not in titulos_existentes):
            nova_tarefa_recorrente = Tarefa.from_dict(modelo)
            novas_tarefas_injetadas.append(nova_tarefa_recorrente)
            print(f"Injetando tarefa recorrente: {titulo_modelo}")
            titulos_existentes.add(titulo_modelo)
            
    return novas_tarefas_injetadas + tarefas_pendentes


def main():
    hoje_obj = datetime.datetime.now()
    
    dias_semana_pt = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
    
    nome_dia_semana = dias_semana_pt[hoje_obj.weekday()]
    data_formatada_simples = hoje_obj.strftime("%d/%m/%Y")
    
    hoje_formatado_app = f"{nome_dia_semana}, {data_formatada_simples}"
    hoje_formatado_iso = hoje_obj.date().isoformat() 
    
    print("Iniciando o Gerador de Relatórios...")
    tarefas_pendentes, tarefas_em_andamento, mesmo_dia = carregar_planejamento(hoje_formatado_iso)
    tarefas_realizado = []
    
    if not mesmo_dia:
        regras = carregar_regras()
        tarefas_pendentes = verificar_e_injetar_recorrentes(regras, tarefas_pendentes, tarefas_em_andamento, hoje_obj)
    
    if tarefas_pendentes or tarefas_em_andamento:
        salvar_planejamento(tarefas_pendentes, tarefas_em_andamento, hoje_formatado_iso)

    time.sleep(1)

    while True:
        mostrar_dashboard(hoje_formatado_app, tarefas_pendentes, tarefas_em_andamento, tarefas_realizado)
        mostrar_menu()
        
        escolha = input("Escolha uma opção (1-9): ")
        print()

        if escolha == '1':
            adicionar_nova_tarefa(tarefas_pendentes, tarefas_em_andamento, tarefas_realizado)
            salvar_planejamento(tarefas_pendentes, tarefas_em_andamento, hoje_formatado_iso)
        
        elif escolha == '2':
            ativar_tarefa(tarefas_pendentes, tarefas_em_andamento)
            salvar_planejamento(tarefas_pendentes, tarefas_em_andamento, hoje_formatado_iso)

        elif escolha == '3':
            concluir_tarefa(tarefas_em_andamento, tarefas_realizado)
            salvar_planejamento(tarefas_pendentes, tarefas_em_andamento, hoje_formatado_iso)
        
        elif escolha == '4':
            gerenciar_subtarefas(tarefas_pendentes, tarefas_em_andamento, tarefas_realizado)
            salvar_planejamento(tarefas_pendentes, tarefas_em_andamento, hoje_formatado_iso)
        
        elif escolha == '5':
            editar_tarefa(tarefas_pendentes, tarefas_em_andamento)
            salvar_planejamento(tarefas_pendentes, tarefas_em_andamento, hoje_formatado_iso)

        elif escolha == '6':
            regras_atuais = carregar_regras()
            gerenciar_regras_menu(regras_atuais)
        
        elif escolha == '7':
            excluir_tarefa(tarefas_pendentes, tarefas_em_andamento)
            salvar_planejamento(tarefas_pendentes, tarefas_em_andamento, hoje_formatado_iso)
        
        elif escolha == '8':
            gerar_relatorio_e_salvar_SIMPLES(hoje_formatado_app, tarefas_pendentes, tarefas_em_andamento, tarefas_realizado, hoje_formatado_iso)
        
        elif escolha == '9':
            print("Saindo do Gerador de Relatórios...")
            salvar_planejamento(tarefas_pendentes, tarefas_em_andamento, hoje_formatado_iso)
            print("Planejamento atual salvo. Até mais!")
            break
        
        else:
            print("ERRO: Opção inválida.")
            time.sleep(1)

    print("Programa finalizado.")

if __name__ == "__main__":
    main()