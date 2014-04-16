from unicodedata import normalize 
def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII','ignore').decode('ASCII')

#example
'''/* CREATE TRIGGER  FOR CARTOES
ACTIVE BEFORE INSERT OR UPDATE POSITION 0
AS
begin
end
^


'''
file = open('create trigger.sql','r')
s = ''.join(file.readlines())
DIRETORIO = 'C:\\bella\\DB\\liquibase\\changelog\\1.0\\create trigger\\'
USUARIO = 'lucas'
insertTrigger = ''
schema = 'lb'
schemaName = 'public'
triggers = s.split('^\n\n\n') #delimitador
for trigger in triggers:
    if trigger != '':        
        pos = trigger.upper().find('CREATE TRIGGER ')+15
        triggerName = trigger[pos:trigger.find(' ',pos)]
        print(triggerName)
        arq = open(DIRETORIO + triggerName.lower() + '.xml','w')
        arq.write('\n<databaseChangeLog')
        arq.write('\n  xmlns="http://www.liquibase.org/xml/ns/dbchangelog"')
        arq.write('\n  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
        arq.write('\n  xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog')
        arq.write('\n       http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-3.1.xsd">')
        arq.write('\n')
        arq.write('\n\t<changeSet id="1-' + triggerName + '" author="' + USUARIO + '">')
        arq.write('\n\t\t<sqlFile endDelimiter="^" splitStatements="true" path="' + DIRETORIO + triggerName.lower() + '.sql"/>')
        trigger = trigger.replace('"',"'")
        posComment = trigger.find('--')
        trigger = remover_acentos(trigger).replace(' <> ','!=')
        arq2 = open(DIRETORIO + triggerName.lower() + '.sql','w')
        arq2.write(trigger)
        arq2.close()        
        arq.write('\n\t\t<rollback>')
        arq.write('\n\t\t\t<sql>')
        arq.write('\n\t\t\t\tDROP TRIGGER ' + triggerName)
        arq.write('\n\t\t\t</sql>')
        arq.write('\n\t\t</rollback>')
        arq.write('\n\t</changeSet>')
        arq.write('\n</databaseChangeLog>')
        arq.close()
        insertTrigger += '<include file="' + DIRETORIO + triggerName + '.xml"/>\n'
    else:
        print('vazio')
print('\n----------------------------------------\n' + insertTrigger.lower())
