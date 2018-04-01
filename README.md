# reditus

## atualização de banco de dados
 - '''source env/bin/activate'''
 ### metadados dos processos
   - 'python manage.py metadatarebase'
    - comando que limpa os metadados com base nos arquivos em 'static/data/elastic_data/'
 ### metadados dos processos
   - 'python manage.py similarsrebase'
    - comando que limpa as referencias aos arquivos similares com base nos arquivos em 'static/data/similar_data/similares_const/'
    - recomenda-se manter o arquivo compactado em 'static/data/similar_data/' e os arquivos descompactados em 'static/data/similar_data/similares_const/' para bom funcionamento do comando.

## atualizações de codigo
 - https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04
 - 'sudo systemctl daemon-reload'
 - 'sudo systemctl restart gunicorn'
 - 'sudo nginx -t && sudo systemctl restart nginx'

### comandos para configuração em caso de pull request
 - 'virtualenv env'
 - 'source env/bin/activate'
 - 'pip install -r requirements.txt'

 - no diretório do projeto
    - 'python manage.py makemigrations'
    - 'python manage.py migrate'

### comandos para execução local
 - 'python manage.py runserver'
