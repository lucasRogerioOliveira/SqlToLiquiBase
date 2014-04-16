#CREATE GENERATOR SEGURANCA_SEGUR_ID_GEN; SET GENERATOR SEGURANCA_SEGUR_ID_GEN TO 0;
#CREATE SEQUENCE CONTADOR_2 START WITH 5 INCREMENT BY 2 MINVALUE 10 MAXVALUE 1000 ORDER CYCLE;
file = open('create sequence.sql','r')
s = ''.join(file.readlines())
DIRETORIO = 'C:\\bella\\DB\\liquibase\\changelog\\1.0\\create sequence\\'
USUARIO = 'lucas'
insertSequence = ''
schema = 'lb'
schemaName = 'public'
sequences = s.split(';\n')
for sequence in sequences:
    if sequence != '':
        if sequence.find('CREATE GENERATOR ') > -1:
            pos = sequence.find('CREATE GENERATOR ')+17
            if sequence.find(';',pos) > -1:
                sequenceName = sequence[pos:sequence.find(';')].lower()
            else:
                sequenceName = sequence[pos:len(sequence)].lower()
            print(sequenceName)
            arq = open(DIRETORIO + sequenceName.lower() + '.xml','w')
            arq.write('<!--ORIGINAL SQL: ' + sequence.replace('\n','') +'-->')
            arq.write('\n<databaseChangeLog')
            arq.write('\n  xmlns="http://www.liquibase.org/xml/ns/dbchangelog"')
            arq.write('\n  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
            arq.write('\n  xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog')
            arq.write('\n       http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-3.1.xsd">')
            arq.write('\n')
            arq.write('\n\t<changeSet id="1-' + sequenceName + '" author="' + USUARIO + '">')
            arq.write('\n\t\t<createSequence catalogName="' + schema + '"')
            arq.write('\n\t\t\tschemaName="' + schemaName + '"')
            arq.write('\n\t\t\tsequenceName="' + sequenceName + '"')
            setGenerator = sequence.find('SET GENERATOR ')
            if setGenerator > -1:
                arq.write('/>')
                arq.write('\n\t\t<sql>')
                arq.write('\n\t\t\t' + sequence[setGenerator:])
                arq.write('\n\t\t</sql>')
            else:
                arq.write('/>')
            arq.write('\n\t\t<rollback>')
            arq.write('\n\t\t\t<dropSequence catalogName="' + schema + '"')
            arq.write('\n\t\t\tschemaName="' + schemaName + '"')
            arq.write('\n\t\t\tsequenceName="' + sequenceName + '"/>')
            arq.write('\n\t\t</rollback>')
            arq.write('\n\t</changeSet>')
            arq.write('\n</databaseChangeLog>');            
            arq.close();
            print(sequence[sequence.find(' TO ',setGenerator)+4:])
        elif sequence.find('CREATE SEQUENCE ') > -1:
            pos = sequence.upper().find(' SEQUENCE ')+10
            sequenceName = sequence[pos:sequence.find(' ',pos)]
            print(sequenceName)
            arq = open(DIRETORIO + sequenceName.lower() + '.xml','w')            
            arq.write('<!--ORIGINAL SQL: ' + sequence.strip('\n') +'-->')
            arq.write('\n<databaseChangeLog')
            arq.write('\n  xmlns="http://www.liquibase.org/xml/ns/dbchangelog"')
            arq.write('\n  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
            arq.write('\n  xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog')
            arq.write('\n       http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-3.1.xsd">')
            arq.write('\n')
            arq.write('\n\t<changeSet id="1-' + sequenceName + '" author="' + USUARIO + '">')
            arq.write('\n\t\t<createSequence catalogName="' + schema + '"')
            arq.write('\n\t\t\tschemaName="' + schemaName + '"')
            arq.write('\n\t\t\tsequenceName="' + sequenceName + '"')
            pos = sequence.find(' START WITH ')
            if pos > -1:
                arq.write('\n\t\t\tstartValue="' + sequence[sequence.find(' '):pos+12] + '"/>')
            pos = sequence.find(' INCREMENT BY ')
            if pos > -1:
                arq.write('\n\t\t\tincrementBy="' + sequence[sequence.find(' '):pos+14] + '"/>')
            pos = sequence.find(' MINVALUE ')
            if pos > -1:
                arq.write('\n\t\t\tminValue="' + sequence[sequence.find(' '):pos+10] + '"/>')
            pos = sequence.find(' MAXVALUE ')
            if pos > -1:
                arq.write('\n\t\t\tminValue="' + sequence[sequence.find(' '):pos+10] + '"/>')
            if sequence.find(' ORDER ') > -1:
                arq.write('\n\t\t\tordered="true"')
            if sequence.find(' CYCLE ') > -1:
                arq.write('\n\t\t\tcycle="true"')
            arq.write('/>')
            arq.write('\n\t\t<rollback>')
            arq.write('\n\t\t\t<dropSequence catalogName="' + schema + '"')
            arq.write('\n\t\t\tschemaName="' + schemaName + '"')
            arq.write('\n\t\t\tsequenceName="' + sequenceName + '"/>')
            arq.write('\n\t\t</rollback>')
            arq.write('\n\t</changeSet>')
            arq.write('\n</databaseChangeLog>');                        
            arq.close();            
        insertSequence += '<include file="' + DIRETORIO + sequenceName + '.xml"/>\n'
    else:
        print('vazio');
print('\n----------------------------------------\n' + insertSequence.lower())
