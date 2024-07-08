################################################ INSTALAÇÕES ################################################

## Instalar e Ativar o ambiente 

poetry install 
poetry shell 

## Instalar as dependencias e bibliotecas

poetry add --group dev pytest pytest-cov 
poetry add fastapi --version "^0.111.0"
poetry add pandas --version "^2.2.2"
poetry add pandera --version "^0.20.1"
poetry add pymongo --version "^4.8.0"
poetry add psycopg2-binary --version "^2.9.9"
poetry add sqlalchemy --version "^2.0.31"
poetry add motor --version "^3.5.0"
poetry add loguru --version "^0.7.2"
poetry add git-lfs --version "^1.6"
poetry add --group dev ruff 
poetry add --group dev taskipy 

** CONSULTAR AS DEPENDENCIAS **
poetry show --tree
poetry env list

################################################ VERSIONAMENTO GIT ################################################

** GITIGNORE **

ignr -p python > .gitignore 
ignr -p visualstudio > .gitignore 
ignr -p ruff > .gitignore 
ignr -p data > .gitignore 


##################################################################
** PRIMEIRO COMMIT ** 

git init .
git add .
git commit -m "mensagem"
git push -u origin main 


##################################################################
** criar uma branch(branch de trabalho) **

git checkout -b nome_da_nova_branch (cria uma branch de trabalho) 
git commit -m "mensagem"
git push origin nome_da_nova_branch(branch de trabalho)

##################################################################
** sair da branch_nova **

git checkout main (branch de trabalho) 
** git merge nome_da_nova_branch** (obs: pega todos os codigos da branch de trabalho e coloca na branch principal(main))






