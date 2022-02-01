import psycopg2


def make_connection(command):
    connector = None
    try:
        connector = psycopg2.connect(dbname='amm', user='nadezhda')

        cur = connector.cursor()

        cur.execute(command)
        connector.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connector is not None:
            connector.close()


def create_table():
    """" creates a table in the database """
    command = 'CREATE TABLE  IF NOT EXISTS Amm (id serial primary key, text varchar(50), questions text, answer varchar(100) );'
    return command


def insert_row(text, questions, answer):
    values = (text, questions, answer)
    query = 'INSERT INTO Amm(text, questions, answer) VALUES(%s, %s, %s);' % values
    return query


def find_answer(content):
    command = 'SELECT answer FROM Amm WHERE questions=%s'
    connector = None
    answer = ''
    try:
        connector = psycopg2.connect(dbname='amm', user='nadezhda')

        cur = connector.cursor()

        cur.execute(command % content)
        answer = cur.fetchone()
        #connector.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connector is not None:
            connector.close()

    return answer

if __name__ == '__main__':
    make_connection(create_table())
    # make_connection(insert_row("'имя декана'", "'как зовут декана'", "'ваня'"))
    # make_connection(insert_row("'фамилия декана'", "'какая фамилия у декана'", "'шашкин'"))
