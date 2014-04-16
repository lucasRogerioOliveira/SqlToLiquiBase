#para usar domínios você deve criar o mesmo antes.
s = '''
CREATE TABLE ADMINISTRADORA (
    FIELD_1      INTEGER NOT NULL,
    FIELD_2      VARCHAR(45) NOT NULL,
    FIELD_3      CHAR(1) DEFAULT 'N' NOT NULL,
    FIELD_4      SOME_DOMAIN, 
    FIELD_5      VARCHAR(45)
);
'''
file = open('create table.sql','r')
s = ''.join(file.readlines())
DIRETORIO = 'C:\\bella\\DB\\liquibase\\changelog\\1.0\\create table\\'
USUARIO = 'lucas'
incluir_tabelas = '';
tabelas = s.split(');\n')
for tabela in tabelas:
    if tabela != '':
        nome_tabela = tabela[tabela.find('TABLE ')+6:tabela.find(' (')]
        print(nome_tabela)
        arq = open(DIRETORIO + nome_tabela.lower() + '.xml','w')
        arq.write('<?xml version="1.0" encoding="UTF-8"?>')
        arq.write('\n')
        arq.write('\n<databaseChangeLog')
        arq.write('\n  xmlns="http://www.liquibase.org/xml/ns/dbchangelog"')
        arq.write('\n  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
        arq.write('\n  xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog')
        arq.write('\n       http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-3.1.xsd">')
        arq.write('\n');
        arq.write('\n\t<changeSet id="1" author="lucas">')
        arq.write('\n\t\t<createTable tableName="' + nome_tabela + '">')
        colunas = tabela[tabela.find('(\n')+3:tabela.find(');\n')].split('\n')
        for coluna in colunas:
            coluna_str = '';
            palavras = coluna.split(' ')
            while palavras.count('') > 0:
                palavras.remove('')
                
            campo = palavras[0]
            if palavras[1].upper() == 'DOUBLE':
                tipo = palavras[1] + ' ' + palavras[2]
                print('\n==================\nTipo:',tipo)
                del palavras[2]
            elif palavras[1].upper() == 'BLOB':
                tipo = palavras[1] + ' ' + palavras[2] + ' ' + palavras[3] + ' ' + palavras[4] + ' ' + palavras[5] + ' ' + palavras[6]
                del palavras[2:7]
            else:
                tipo = palavras[1]
            if tipo[-1] == ',':
                tipo = tipo[:-1]
            if nome_tabela == 'AGENCIADORES':
                print("====TIPO:", tipo );
                print(palavras)
            valor_default = '';
            default = False;
            notNull = False;
            if len(palavras) >= 3:
                if palavras[2].upper() == 'DEFAULT':
                    print('campo' + campo + 'tp: ' + tipo + ' 2: ' + palavras[2] + ' 3: ' + palavras[3])
                    if tipo.upper().find('CHAR') > -1 or tipo.upper().find('DATE') > -1:
                        palavra = ''
                        comma = 0
                        i = 1
                        if palavras[3] != 'NULL' and palavras[3] != 'NULL,' and palavras[3].find("''") == -1:
                            while comma < 2:
                                if tipo.upper().find('DATE') > -1:
                                    if comma >= 1:
                                        palavra += ' ' + palavras[2+i]
                                    else:
                                        palavra += palavras[2+1]
                                else:
                                    palavra += palavras[2+i]
                                comma += palavra.replace('"',"'").count("'")
                                i += 1                            
                            print("palavras 2+i:", palavra)
                        elif palavras[3] == "''":
                            palavra += "''"
                            i += 1;
                        else:
                            palavra += '"NULL"'
                            i += 1;
                        print(i)
                        print(palavras)
                        del palavras[2:2+i]
                        print(palavras)
                        if tipo[-1] != '"':
                            tipo += '"'
                        default = True
                        valor_default = ' defaultValue=' + palavra.replace("'",'"').replace(',','').replace('.','')
                if len(palavras) > 2:
                    print('p2: ',palavras[2])
                    if palavras[2].upper() == 'NOT':
                        del palavras[2:4]
                        notNull = True
                else:
                    print("menor")
            if notNull:
                print("imprimindo valor_default")
                print(valor_default)
                if valor_default != '' and valor_default[-1] == '"':
                    arq.write('\n\t\t\t<column name="' + campo +'" type="' + tipo + valor_default + '>')
                else:
                    arq.write('\n\t\t\t<column name="' + campo +'" type="' + tipo + valor_default.replace("'",'"') + '">')
                arq.write('\n\t\t\t\t<constraints nullable="false"/>')
                arq.write('\n\t\t\t</column>')
            else:
                if valor_default != '' and valor_default[-1] == '"':
                    arq.write('\n\t\t\t<column name="' + campo +'" type="' + tipo + valor_default + '/>')
                else:
                    arq.write('\n\t\t\t<column name="' + campo +'" type="' + tipo + valor_default.replace("'",'"') + '"/>')
        arq.write('\n\t\t</createTable>')
        arq.write('\n\t\t<rollback>')
        arq.write('\n\t\t\t<dropTable tableName="' + nome_tabela + '"/>')
        arq.write('\n\t\t</rollback>')
        arq.write('\n\t</changeSet>')
        arq.write('\n</databaseChangeLog>');
        arq.close();
        incluir_tabelas += '<include file="' + DIRETORIO + nome_tabela + '.xml"/>\n'
    else:
        print('vazio');
print('\n----------------------------------------\n' + incluir_tabelas.lower())
