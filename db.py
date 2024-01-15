import asyncpg

from config import Config

db_params = {
    'database': Config.DB_NAME,
    'user': Config.DB_USERNAME,
    'password': Config.DB_PASSWORD,
    'host': Config.DB_HOST,
    'port': Config.DB_PORT
}


async def get_food_titles():
    connection = await asyncpg.connect(**db_params)

    try:
        query = "SELECT id, title FROM food_protocols"
        food_data = await connection.fetch(query)

        food_dict = {data['id']: data['title'] for data in food_data}
        return food_dict

    except (Exception, asyncpg.PostgresError) as error:
        print("Ошибка при работе с PostgreSQL", error)

    finally:
        if connection:
            await connection.close()


async def get_recommendations(title_name):
    connection = await asyncpg.connect(**db_params)

    try:
        query = "SELECT title, id, name FROM recommendations WHERE title = $1"
        rows = await connection.fetch(query, title_name)

        result_dict = {}

        for row in rows:
            title = row['title']
            id = row['id']
            name = row['name']

            if title not in result_dict:
                result_dict[title] = []

            result_dict[title].append({'id': id, 'name': name})

        for key in result_dict:
            result_dict[key] = sorted(result_dict[key], key=lambda x: x['id'])

        return result_dict
    except (Exception, asyncpg.PostgresError) as error:
        print("Ошибка при работе с PostgreSQL", error)

    finally:
        if connection:
            await connection.close()


async def get_protocol_by_id(id):
    connection = await asyncpg.connect(**db_params)

    try:
        query = "SELECT title FROM food_protocols WHERE id = $1"
        food_title = await connection.fetchval(query, id)
        return food_title

    except (Exception, asyncpg.PostgresError) as error:
        print("Ошибка при работе с PostgreSQL", error)

    finally:
        if connection:
            await connection.close()


async def get_recommendations_by_ids(ids):
    connection = await asyncpg.connect(**db_params)

    try:
        placeholders = ', '.join(['${}'.format(i + 1) for i in range(len(ids))])
        query = "SELECT name FROM recommendations WHERE id IN ({})".format(placeholders)
        recommendation_names = await connection.fetch(query, *ids)
        recommendation_names = [name['name'] for name in recommendation_names]
        return recommendation_names

    except (Exception, asyncpg.PostgresError) as error:
        print("Ошибка при работе с PostgreSQL", error)

    finally:
        if connection:
            await connection.close()


async def save_new_client(name, email, food_protocol_id, food_protocol_name, allergic, recommendations,
                          recommendations_ids):
    connection = await asyncpg.connect(**db_params)

    try:
        query = "SELECT * FROM clients WHERE full_name = $1"
        existing_client = await connection.fetchrow(query, name)

        if existing_client:
            update_query = """
                    UPDATE clients
                    SET food_protocol_id = $1, food_protocol_name = $2, allergic = $3, recommendations = $4, recommendations_ids = $5, email = $6
                    WHERE full_name = $7
                    """
            await connection.execute(update_query, food_protocol_id, food_protocol_name, str(allergic), recommendations,
                                     recommendations_ids, str(email), name)
        else:
            insert_query = """
                    INSERT INTO clients (full_name, email, food_protocol_id, food_protocol_name, allergic, recommendations, recommendations_ids)
                    VALUES ($1, $2, $3, $4, $5, $6, $7)
                    """
            await connection.execute(insert_query, name, str(email), food_protocol_id, food_protocol_name,
                                     str(allergic), recommendations, recommendations_ids)

    except (Exception, asyncpg.PostgresError) as error:
        print("Error while connecting to PostgreSQL", error)

    finally:
        if connection:
            await connection.close()


async def get_clients_data():
    connection = await asyncpg.connect(**db_params)

    try:
        query = "SELECT * FROM clients"
        rows = await connection.fetch(query)

        list_of_dicts = [dict(row) for row in rows]
        return list_of_dicts

    except (Exception, asyncpg.PostgresError) as error:
        print("Ошибка при работе с PostgreSQL", error)

    finally:
        if connection:
            await connection.close()


async def get_client_by_id(id):
    connection = await asyncpg.connect(**db_params)

    try:
        query = "SELECT * FROM clients WHERE id = $1"
        client_data = await connection.fetchrow(query, id)

        if client_data:
            client_dict = dict(client_data.items())
            return client_dict
        else:
            return None

    except (Exception, asyncpg.PostgresError) as error:
        print("Ошибка при работе с PostgreSQL", error)

    finally:
        if connection:
            await connection.close()


async def get_client_by_name(name):
    connection = await asyncpg.connect(**db_params)

    try:
        query = "SELECT * FROM clients WHERE full_name = $1"
        client_data = await connection.fetchrow(query, name)

        if client_data:
            client_dict = dict(client_data.items())
            return client_dict
        else:
            return None

    except (Exception, asyncpg.PostgresError) as error:
        print("Ошибка при работе с PostgreSQL", error)

    finally:
        if connection:
            await connection.close()


async def delete_client_by_id(id):
    connection = await asyncpg.connect(**db_params)

    try:
        query = "DELETE FROM clients WHERE id = $1"
        await connection.execute(query, id)

    except (Exception, asyncpg.PostgresError) as error:
        print("Ошибка при работе с PostgreSQL", error)

    finally:
        if connection:
            await connection.close()


async def update_user_recommendations(user_id, recommendations_ids, recommendations):
    connection = await asyncpg.connect(**db_params)

    try:
        sql = """
            UPDATE clients
            SET recommendations_ids = $1, recommendations = $2
            WHERE id = $3
        """
        await connection.execute(sql, recommendations_ids, recommendations, user_id)

    except (Exception, asyncpg.PostgresError) as error:
        print("Ошибка при работе с PostgreSQL", error)

    finally:
        if connection:
            await connection.close()


async def update_client_by_id(client_data):
    connection = await asyncpg.connect(**db_params)

    try:
        sql_query = """
            UPDATE clients
            SET
                full_name = $1,
                email = $2,
                food_protocol_id = $3,
                allergic = $4,
                recommendations = $5,
                food_protocol_name = $6,
                recommendations_ids = $7
            WHERE id = $8
        """
        await connection.execute(
            sql_query,
            client_data['full_name'],
            client_data['email'],
            client_data['food_protocol_id'],
            client_data['allergic'],
            client_data['recommendations'],
            client_data['food_protocol_name'],
            client_data['recommendations_ids'],
            client_data['id']
        )

    except (Exception, asyncpg.PostgresError) as error:
        print("Ошибка при работе с PostgreSQL", error)

    finally:
        if connection:
            await connection.close()


async def get_food_protocols_by_id(food_id):
    connection = await asyncpg.connect(**db_params)

    try:
        query = "SELECT allowed, not_allowed FROM food_protocols WHERE id = $1"

        result = await connection.fetchrow(query, food_id)
        result_dict = dict(result)
        return result_dict

    except (Exception, asyncpg.PostgresError) as error:
        print("Ошибка при работе с PostgreSQL", error)

    finally:
        if connection:
            await connection.close()


async def setup_rec_data(names):
    connection = await asyncpg.connect(**db_params)

    try:
        query = "SELECT name, title FROM recommendations WHERE name = ANY($1)"

        results = await connection.fetch(query, names)

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
    except (Exception, asyncpg.PostgresError) as error:
        print("Ошибка при работе с PostgreSQL", error)

    finally:
        if connection:
            await connection.close()
