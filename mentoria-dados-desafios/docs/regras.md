# Regras da Mentoria

Para manter o ambiente organizado e garantir a melhor experiência para todos os mentorados, pedimos que sigam as regras abaixo:

## 1. Integridade do Repositório Main
- **Não** faça commits diretamente na branch `main`.
- Sempre trabalhe em sua própria branch (ex: `feature/joao-silva-sql-basico`).
- Use Pull Requests se a instrução for integrar o seu código ao repositório principal, mas geralmente recomendamos forks para portfólio pessoal.

## 2. Padrões de Código
- Escreva código SQL em caixa alta para palavras reservadas (`SELECT`, `FROM`, `WHERE`).
- Use nomes descritivos para variáveis e alias (evite `a`, `b`, `c`).
- Documente trechos complexos do seu código utilizando comentários (`--` em SQL ou `#` em Python).

## 3. Ambiente Local
- Não comite credenciais reais ou arquivos `.env` no repositório.
- A base de dados PostgreSQL e os containers são destruídos e recriados conforme necessidade. Não armazene dados críticos localmente.

## 4. Comunicação
- Dúvidas sobre desafios devem ser documentadas nas issues do GitHub, permitindo que outros mentorados aprendam com as mesmas dúvidas.
- Se o desafio pedir uma determinada arquitetura ou restrição, cumpra-a antes de tentar abordagens mais "fáceis". O objetivo é aprender o conceito.

## 5. Integridade Acadêmica
- É encorajado discutir soluções, mas não copie e cole queries sem entender o que elas fazem.
- Se utilizou IA ou fóruns (como StackOverflow) para chegar na resposta, adicione um comentário no seu código explicando o que aprendeu.
