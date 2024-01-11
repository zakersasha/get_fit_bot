import psycopg2

from config import Config

db_params = {
    'dbname': Config.DB_NAME,
    'user': Config.DB_USERNAME,
    'password': Config.DB_PASSWORD,
    'host': Config.DB_HOST,
    'port': Config.DB_PORT
}


def get_food_titles():
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT id, title FROM food_protocols")
        food_data = cursor.fetchall()
        food_dict = {data[0]: data[1] for data in food_data}

        return food_dict

    except (Exception, psycopg2.Error) as error:
        print("Ошибка при работе с PostgreSQL", error)

    finally:
        if connection:
            cursor.close()
            connection.close()


def get_recommendations(title_name):
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT title, id, name FROM recommendations WHERE title = %s", (title_name,))

        rows = cursor.fetchall()

        result_dict = {}

        for row in rows:
            title = row[0]
            id = row[1]
            name = row[2]

            if title not in result_dict:
                result_dict[title] = []

            result_dict[title].append({'id': id, 'name': name})

        for key in result_dict:
            result_dict[key] = sorted(result_dict[key], key=lambda x: x['id'])
        return result_dict
    except (Exception, psycopg2.Error) as error:
        print("Ошибка при работе с PostgreSQL", error)

    finally:
        if connection:
            cursor.close()
            connection.close()


def get_protocol_by_id(id):
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT title FROM food_protocols WHERE id = %s", (id,))
        food_title = cursor.fetchone()
        if food_title is not None:
            return food_title[0]
        else:
            return None

    except (Exception, psycopg2.Error) as error:
        print("Ошибка при работе с PostgreSQL", error)

    finally:
        if connection:
            cursor.close()
            connection.close()


def get_recommendations_by_ids(ids):
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    try:
        placeholders = ', '.join(['%s'] * len(ids))
        query = "SELECT name FROM recommendations WHERE id IN ({})".format(placeholders)

        cursor.execute(query, ids)

        recommendation_names = cursor.fetchall()

        recommendation_names = [name[0] for name in recommendation_names]

        return recommendation_names

    except (Exception, psycopg2.Error) as error:
        print("Ошибка при работе с PostgreSQL", error)

    finally:
        if connection:
            cursor.close()
            connection.close()


def save_new_client(name, email, food_protocol_id, food_protocol_name, allergic, recommendations, recommendations_ids):
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()
    try:

        query = "SELECT * FROM clients WHERE full_name = %s"
        cursor.execute(query, (name,))
        existing_client = cursor.fetchone()

        if existing_client:
            query = """
                    UPDATE clients
                    SET food_protocol_id = %s, food_protocol_name = %s, allergic = %s, recommendations = %s, recommendations_ids = %s, email = %s
                    WHERE full_name = %s
                    """
            cursor.execute(query, (
                food_protocol_id, food_protocol_name, str(allergic), recommendations, recommendations_ids,
                str(email), name))
        else:
            query = """
                    INSERT INTO clients (full_name, email, food_protocol_id, food_protocol_name, allergic, recommendations, recommendations_ids)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
            cursor.execute(query, (
                name, str(email), food_protocol_id, food_protocol_name, str(allergic), recommendations,
                recommendations_ids))

        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

    finally:
        if connection:
            cursor.close()
            connection.close()


def get_clients_data():
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM clients")

        rows = cursor.fetchall()

        columns = [col[0] for col in cursor.description]

        list_of_dicts = []
        for row in rows:
            dict_row = dict(zip(columns, row))
            list_of_dicts.append(dict_row)

        return list_of_dicts

    except (Exception, psycopg2.Error) as error:
        print("Ошибка при работе с PostgreSQL", error)

    finally:
        if connection:
            cursor.close()
            connection.close()


def get_client_by_id(id):
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM clients WHERE id = %s", (id,))
        client_data = cursor.fetchone()
        columns = [desc[0] for desc in cursor.description]
        client_dict = {columns[i]: client_data[i] for i in range(len(columns))}
        return client_dict


    except (Exception, psycopg2.Error) as error:
        print("Ошибка при работе с PostgreSQL", error)

    finally:
        if connection:
            cursor.close()
            connection.close()


def delete_client_by_id(id):
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    try:
        cur = connection.cursor()

        cur.execute("""
                DELETE FROM clients
                WHERE id = %s
            """, (id,))

        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Ошибка при работе с PostgreSQL", error)

    finally:
        if connection:
            cursor.close()
            connection.close()


def update_user_recommendations(user_id, recommendations_ids, recommendations):
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    try:
        sql = """
                UPDATE clients
                SET recommendations_ids = %s, recommendations = %s
                WHERE id = %s
            """
        cursor.execute(sql, (recommendations_ids, recommendations, user_id))
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Ошибка при работе с PostgreSQL", error)

    finally:
        if connection:
            cursor.close()
            connection.close()


def get_food_protocols_by_id(food_id):
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()
    try:
        query = "SELECT allowed, not_allowed FROM food_protocols WHERE id = %s"

        cursor.execute(query, (food_id,))
        result = cursor.fetchone()
        columns = ('allowed', 'not_allowed')
        result_dict = dict(zip(columns, result))
        return result_dict

    except (Exception, psycopg2.Error) as error:
        print("Ошибка при работе с PostgreSQL", error)

    finally:
        if connection:
            cursor.close()
            connection.close()


def setup_rec_data(names):
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()
    try:
        query = "SELECT name, title FROM recommendations WHERE name IN %s"

        cursor.execute(query, (tuple(names),))

        results = cursor.fetchall()

        formatted_string = ""
        headers_set = set()

        for item in results:
            header, content = item
            if content in headers_set:
                formatted_string += f"\n- {header}"
            else:
                formatted_string += f"\n<b>{content}</b>\n- {header}"
                headers_set.add(content)

        return formatted_string
    except (Exception, psycopg2.Error) as error:
        print("Ошибка при работе с PostgreSQL", error)

    finally:
        if connection:
            cursor.close()
            connection.close()
