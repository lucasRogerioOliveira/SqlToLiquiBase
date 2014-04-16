#CREATE UNIQUE INDEX NAME ON TABLE (FIELD_1, FIELD_2);
#CREATE INDEX PRODUTOS_IDX6 ON SCHEMA.TABLE (FIELD_1);
file = open('create index.sql','r')
s = ''.join(file.readlines())
DIRETORIO = 'C:\\bella\\DB\\liquibase\\changelog\\1.0\\create index\\'
USUARIO = 'lucas'
incluir_indice = ''
schemaName = 'public'
indices = s.split(';\n')
for indice in indices:
    if indice != '':
        nome_indice = indice[indice.find('INDEX ')+6:indice.find(' ON')]
        print(nome_indice)
        arq = open(DIRETORIO + nome_indice.lower() + '.xml','w')
        arq.write('<!--ORIGINAL SQL: ' + indice.replace('\n','') +'-->')
        arq.write('\n<databaseChangeLog')
        arq.write('\n  xmlns="http://www.liquibase.org/xml/ns/dbchangelog"')
        arq.write('\n  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
        arq.write('\n  xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog')
        arq.write('\n       http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-3.1.xsd">')
        arq.write('\n');
        arq.write('\n\t<changeSet id="1-' + nome_indice + '" author="lucas">')        
        
        unique = indice.upper().find('UNIQUE') > -1
        schema = indice[indice.upper().find('ON ')+3:indice.upper().find('.')]
        table = indice[indice.upper().find('.')+1:indice.upper().find(' (')]
        fields = indice[indice.upper().find(' (')+2:indice.upper().find(')')].split(',')
        arq.write('\n\t\t<createIndex catalogName="' + schema + '"')
        arq.write('\n\t\t\tindexName="' + nome_indice + '"')
        arq.write('\n\t\t\tschemaName="' + schemaName + '"')
        arq.write('\n\t\t\ttableName="' + table + '"')
        arq.write('\n\t\t\tunique="' + str(unique).lower() + '">')
        for field in fields:
            arq.write('\n\t\t<column name="' + field.replace(' ','') + '"/>')
        arq.write('\n\t\t</createIndex>')
        arq.write('\n\t\t<rollback>')
        arq.write('\n\t\t\t<dropIndex catalogName="' + schema + '"')
        arq.write('\n\t\t\t\tindexName="' + nome_indice + '"')
        arq.write('\n\t\t\t\tschemaName="' + schemaName + '"')
        arq.write('\n\t\t\t\ttableName="' + table + '"/>')
        arq.write('\n\t\t</rollback>')
        arq.write('\n\t</changeSet>')
        arq.write('\n</databaseChangeLog>');
        arq.close();
        incluir_indice += '<include file="' + DIRETORIO + nome_indice + '.xml"/>\n'
    else:
        print('vazio');
print('\n----------------------------------------\n' + incluir_indice.lower())
