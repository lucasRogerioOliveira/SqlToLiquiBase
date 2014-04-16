from unicodedata import normalize 
def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII','ignore').decode('ASCII')


file = open('create procedure.sql','r')
s = ''.join(file.readlines())
DIRETORIO = 'C:\\bella\\DB\\liquibase\\changelog\\1.0\\create procedure\\'
USUARIO = 'lucas'
insertProcedure = ''
schema = 'lb'
schemaName = 'public'
procedures = s.split('^\n\n\n')
for procedure in procedures:
    if procedure != '':        
        pos = procedure.upper().find(' PROCEDURE ')+11
        print(procedure)
        posSpace = procedure.find(' ',pos)
        posAs = procedure.upper().find('AS\n',pos)
        posReturn = procedure.upper().find('RETURNS',pos)
        posBreakLine = procedure.find('\n',pos)
        if (posSpace < posAs and posSpace < posReturn) or (posSpace < posAs and posReturn == -1):
            print('1')
            procedureName = procedure[pos:procedure.find(' ',pos)].lower().strip('\n')
        elif (posAs < posReturn and posReturn > -1) or (posAs > -1 and posReturn == -1):
            print('2')
            procedureName = procedure[pos:procedure.upper().find('AS\n',pos)].lower().strip('\n')
        elif posReturn < posBreakLine:
            print('3')
            procedureName = procedure[pos:procedure.upper().find('RETURNS\n',pos)].lower().strip('\n')
        else:
            print('4')
            print('posSpace ', posSpace, ' posAs ', posAs, ' posReturn ', posReturn, ' posBreakLine ', posBreakLine)
            procedureName = procedure[pos:procedure.find('\n',pos)].lower().strip('\n')
        print('*******')
        print(procedureName)
        print('*******')
        arq = open(DIRETORIO + procedureName.lower() + '.xml','w')
        #arq.write('<!--ORIGINAL SQL: ' + remover_acentos(procedure.replace('--','')) +'-->')
        arq.write('\n<databaseChangeLog')
        arq.write('\n  xmlns="http://www.liquibase.org/xml/ns/dbchangelog"')
        arq.write('\n  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
        arq.write('\n  xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog')
        arq.write('\n       http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-3.1.xsd">')
        arq.write('\n')
        arq.write('\n\t<changeSet id="1-' + procedureName + '" author="' + USUARIO + '">')
        arq.write('\n\t\t<createProcedure catalogName="' + schema + '"')
        arq.write('\n\t\t\tpath="' + DIRETORIO + procedureName.lower() + '.sql"')
        arq.write('\n\t\t\tschemaName="' + schemaName + '">')
        #arq.write('\n\t\t\tencoding="ISO-8859-1">')
        #substitui por ' porque no firebird deeixar com " dava erro.        
        procedure = procedure.replace('"',"'")
        posComment = procedure.find('--')
        procedure = remover_acentos(procedure).replace(' <> ','!=')
        #while posComment > -1:            
        #    procedure = procedure[:posComment] + procedure[posComment:].replace('--','/*',1)
        #    #vendo se jah não termina com '*/' pois se não da erro... a final de contas se eu abrir vários /* é necessário apenas um */ para fechar todos eles
        #    if procedure[posComment:procedure.find('\n',posComment)][-2:] != '*/': 
        #        procedure = procedure[:posComment] + procedure[posComment:].replace('\n','*/\n',1)
        #    posComment = procedure.find('--')
        arq2 = open(DIRETORIO + procedureName.lower() + '.sql','w')
        arq2.write(procedure)
        arq2.close()
        arq.write('\n\t\t</createProcedure>')
        arq.write('\n\t\t<rollback>')
        arq.write('\n\t\t\t<dropProcedure catalogName="' + schema + '"')
        arq.write('\n\t\t\tschemaName="' + schemaName + '"')
        arq.write('\n\t\t\tprocedureName="' + procedureName + '"/>')
        arq.write('\n\t\t</rollback>')
        arq.write('\n\t</changeSet>')
        arq.write('\n</databaseChangeLog>')
        arq.close()
        insertProcedure += '<include file="' + DIRETORIO + procedureName + '.xml"/>\n'
    else:
        print('vazio')
print('\n----------------------------------------\n' + insertProcedure.lower())
