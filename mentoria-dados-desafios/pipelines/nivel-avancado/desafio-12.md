/*
=========================================================
DESAFIO 12: Orquestrar com Mage (DAG)
=========================================================
Nivel: Avancado

Objetivo:
Criar um pipeline de 3 etapas (extract, transform, load)
utilizando o Mage AI ou um orquestrador Python sequencial.

Requisitos:
- Implementar funcao extract_orders que le a tabela orders.
- Implementar funcao transform_aggregate que agrupa e soma.
- Implementar funcao load_star_schema que persiste os dados.
- Utilizar decorator @pipeline para registrar as etapas.
- A ordem de execucao deve ser: extract -> transform -> load.

Dica Tecnica:
O decorator @pipeline pode ser implementado com functools.wraps
para manter metadados da funcao. Use um dicionario de contexto
para passar dados entre etapas.
*/
