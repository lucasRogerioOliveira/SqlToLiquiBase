#exemple
'''
ALTER TABLE TABLE_1 ADD CONSTRAINT NAME UNIQUE (FIELD_1, FIELD_2);
ALTER TABLE TABLE_1 ADD CONSTRAINT NAME KEY (FIELD);
ALTER TABLE TABLE_1 ADD CONSTRAINT NAME FOREIGN KEY (FIELD) REFERENCES TABLE_REFERENCE (FIELD_REFERENCE);
'''
file = open('alter table.sql','r')
s = ''.join(file.readlines())
INDEX_DIR = 'C:\\bella\\DB\\liquibase\\changelog\\1.0\\create index\\'
USUARIO = 'lucas'
insertIndex = ''
schemaName = 'public'
schema = 'lb'
tables = s.split(';\n')
for table in tables:
    if table != '':
        head =  '<!--ORIGINAL SQL: ' + table.replace('\n','') +'-->'
        head += '''\n<databaseChangeLog
xmlns="http://www.liquibase.org/xml/ns/dbchangelog"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog
\thttp://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-3.1.xsd">
'''
        pos = table.find('TABLE ')+6
        table_name = table[pos:table.find(' ',pos)]        
        pos = table.find(' ',pos)+1
        action = table[pos:table.find(' ',pos)]
        pos = table.find(' ',pos)+1
        item = table[pos:table.find(' ',pos)]
        pos = table.find(' ',pos)+1
        if action == 'ADD':
            if item == 'CONSTRAINT':                
                index = table[pos:table.find(' ',pos)]
                arq = open(INDEX_DIR + index.lower() + '.xml','w')
                head += '\n\t<changeSet id="1-' + index.lower() + '" author="lucas">'
                pos = table.find(' ',pos)+1
                key = table[pos:table.find(' ',pos)]
                pos = table.find(' ',pos)+1                
                if key == 'UNIQUE':
                    arq.write(head)
                    fields = index[index.upper().find(' (')+2:index.upper().find(')')].split(',')
                    arq.write('\n\t\t<createIndex catalogName="' + schema + '"')
                    arq.write('\n\t\t\tindexName="' + index + '"')
                    if schema != '':
                        arq.write('\n\t\t\tschemaName="' + schemaName.lower() + '"')
                    arq.write('\n\t\t\ttableName="' + table_name.lower() + '"')
                    arq.write('\n\t\t\tunique="true">')
                    fields = table[table.find(' (')+2:table.find(');')].split(',')
                    for field in fields:
                        arq.write('\n\t\t<column name="' + field.replace(' ','') + '"/>')
                    arq.write('\n\t\t</createIndex>')
                    arq.write('\n\t\t<rollback>')
                    arq.write('\n\t\t\t<dropIndex catalogName="' + schema.lower() + '"')
                    arq.write('\n\t\t\t\tindexName="' + index.lower() + '"')
                    arq.write('\n\t\t\t\tschemaName="' + schemaName.lower() + '"')
                    arq.write('\n\t\t\t\ttableName="' + table.lower() + '"/>')
                    arq.write('\n\t\t</rollback>')
                    insertIndex += '<include file="' + INDEX_DIR + index.lower() + '.xml"/>\n'
                    arq.write('\n\t</changeSet>')
                    arq.write('\n</databaseChangeLog>')
                    arq.close()
                elif key == 'FOREIGN':
                    arq.write(head)
                    fields = table[table.upper().find('KEY (')+5:table.find(')')]
                    arq.write('\n\t\t<addForeignKeyConstraint baseColumnNames="' + fields.lower() + '"')
                    arq.write('\n\t\t\tbaseTableName="' + table_name.lower() +'"')
                    arq.write('\n\t\t\tconstraintName="' + index.lower() + '"')
                    #arq.write('\n\t\t\tdeferrable="' + true + '"');
                    #arq.write('\n\t\t\tinitiallyDeferred="' + true + '"');
                    pos = table.find('REFERENCES ')+11;
                    referenceTableName = table[pos:table.find(' ',pos)]
                    fields = table[table.upper().find(' (',pos)+2:table.upper().find(')',pos)]                    
                    if table.find('ON ',pos) > -1:
                        onDelete = table.upper().find('ON DELETE ',pos)+10
                        if onDelete > 10:
                            if table.find(' ',onDelete) > -1:
                                arq.write('\n\t\t\tonDelete="' + table[onDelete:table.find(' ',onDelete)] + '"')
                            else:
                                arq.write('\n\t\t\tonDelete="' + table[onDelete:len(table)] + '"')
                        onUpdate = table.upper().find('ON UPDATE ',pos)+10
                        if onUpdate > 10:
                            if table.find(' ',onUpdate) > -1:
                                arq.write('\n\t\t\tonUpdate="' + table[onUpdate:table.find(' ',onUpdate)] + '"')
                            else:
                                arq.write('\n\t\t\tonUpdate="' + table[onUpdate:len(table)] + '"')
                    arq.write('\n\t\t\treferencedColumnNames="' + fields.lower() + '"')
                    arq.write('\n\t\t\treferencedTableName="' + referenceTableName.lower() + '"/>')
                    arq.write('\n\t\t<rollback>')
                    arq.write('\n\t\t\t<dropForeignKeyConstraint baseTableName="' + table_name + '" constraintName="' + index + '"/>')
                    arq.write('\n\t\t</rollback>')
                    insertIndex += '<include file="' + INDEX_DIR + index.lower() + '.xml"/>\n'
                    arq.write('\n\t</changeSet>')
                    arq.write('\n</databaseChangeLog>')
                    arq.close()
                elif table.find(' PRIMARY KEY ') > -1:                
                    primaryKey =  table[table.find('(')+1:table.find(')')].lower()                    
                    arq = open(INDEX_DIR + index.lower() + '.xml','w')
                    arq.write(head)
                    arq.write('\n\t\t<addPrimaryKey ')
                    if schema != '':
                        arq.write('catalogName="' + schema + '"')
                    arq.write('\n\t\t\tcolumnNames="' + primaryKey + '"')
                    arq.write('\n\t\t\tconstraintName="' + index.lower() + '"')
                    arq.write('\n\t\t\tschemaName="'+ schemaName.lower() + '"')
                    arq.write('\n\t\t\ttableName="' + table_name.lower() + '"/>')
                    arq.write('\n\t\t<rollback>')
                    arq.write('\n\t\t\t<dropPrimaryKey catalogName="' + schema.lower() + '"')
                    arq.write('\n\t\t\tconstraintName="' + index.lower() + '"')
                    arq.write('\n\t\t\tschemaName="' + schemaName.lower() + '"')
                    arq.write('\n\t\t\ttableName="' + table_name.lower() + '"/>')
                    arq.write('\n\t\t</rollback>')                    
                    #arq.write('tablespace="A String"/>')
                    arq.write('\n\t</changeSet>')
                    arq.write('\n</databaseChangeLog>')                    
                    arq.close()
                    insertIndex += '<include file="' + INDEX_DIR + index.lower() + '.xml"/>\n'
            elif item == 'PRIMARY':
                arq = open(INDEX_DIR + 'pk_' + table_name.lower() + '.xml','w')
                head += '\n\t<changeSet id="1-pk_' + table_name.lower() + '" author="lucas">'
                arq.write(head)
                arq.write('\n\t\t<addPrimaryKey ')
                if schema != '':
                    arq.write('catalogName="' + schema + '"')
                primaryKey = table[table.find('(')+1:table.find(')')].lower()
                arq.write('\n\t\t\tcolumnNames="' + primaryKey + '"')
                arq.write('\n\t\t\tconstraintName="pk_' + table_name.lower() + '"')
                arq.write('\n\t\t\tschemaName="'+ schemaName.lower() + '"')
                arq.write('\n\t\t\ttableName="' + table_name.lower() + '"/>')
                arq.write('\n\t\t<rollback>')
                arq.write('\n\t\t\t<dropPrimaryKey catalogName="' + schema.lower() + '"')
                arq.write('\n\t\t\tconstraintName="pk_' + table_name.lower() + '"')
                arq.write('\n\t\t\tschemaName="' + schemaName.lower() + '"')
                arq.write('\n\t\t\ttableName="' + table_name.lower() + '"/>')
                arq.write('\n\t\t</rollback>')
                insertIndex += '<include file="' + INDEX_DIR + 'pk_' + table_name.lower() + '.xml"/>\n'
                #arq.write('tablespace="A String"/>')
                arq.write('\n\t</changeSet>')
                arq.write('\n</databaseChangeLog>')
                arq.close()
print('\n----------------------------------------\n' + insertIndex.lower())
