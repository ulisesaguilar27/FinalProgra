import scrapper as s
import pandas as pd
from mysql.connector import connect, Error

class DataBase:
    def __init__(self):
        self.connection = connect(
            host="localhost",
            user="root",
            password="12345678",
            database="OFERTAS_MERCADOLIBRE",
        )
        self.cursor = self.connection.cursor()


    def create_table(self):
        crear_tabla_query = """
        CREATE TABLE IF NOT EXISTS ofertas_mercado (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Nombre VARCHAR(255),
            Precio DECIMAL(10, 2),
            Descuento VARCHAR(50),
            Tipo VARCHAR(50),
            Envio VARCHAR(50)
        );
        """
        self.cursor.execute(crear_tabla_query)
        self.connection.commit()

    def __enter__(self):
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()

    def insert_data(self, archivo_csv):
        try:
            df = pd.read_csv(archivo_csv, index_col=0)

            # Manejar valores nulos en el DataFrame
            df.fillna('', inplace=True)

            for index, row in df.iterrows():
                insertar_query = """
                INSERT INTO ofertas_mercado(Nombre, Precio, Descuento, Tipo, Envio)
                VALUES (%s, %s, %s, %s, %s)
                """
                values = (
                    str(row['Nombre']),
                    float(row['Precio'].replace(',', '')),
                    str(row['Descuento']),
                    str(row['Tipo']),
                    str(row['Envio'])
                )
                self.cursor.execute(insertar_query, values)

            self.connection.commit()
            print("Datos insertados correctamente en la tabla.")
        except Error as e:
            print(f"Error al insertar datos: {e}")
            raise

    def obtener_datos(self):
        query = "SELECT * FROM ofertas_mercado"
        db = DataBase()
        result = pd.read_sql_query(query, db.connection)
        return result

    def obtener_datos_vista_descuento(self):
        query = "SELECT * FROM vista_descuento;"
        result = pd.read_sql_query(query, self.connection)
        return result

    def obtener_datos_vista_baratos(self):
        query = "SELECT * FROM vista_baratos;"
        result = pd.read_sql_query(query, self.connection)
        return result

    def obtener_datos_vista_productos(self):
        query = "SELECT * FROM productosxtipo;"
        result = pd.read_sql_query(query,self.connection)
        return result

    def obtener_datos_descuento2(self):
        query = 'SELECT rango_descuento, Envio, cantidad_productos FROM vista_descuentos2;'
        result = pd.read_sql(query, self.connection)
        return result

    def obtenerPreciosDesc(self):
        query = 'SELECT Nombre, Precio, Descuento FROM ofertas_mercado;'
        result = pd.read_sql(query, self.connection)
        return result

    def top5Desc(self):
        query = 'SELECT Nombre, Precio, Descuento, Tipo FROM ofertas_mercado ORDER BY CAST(Descuento AS DECIMAL(5,2)) DESC LIMIT 10;'
        result = pd.read_sql(query, self.connection)
        return result

    def countEnvios(self):
        query = 'SELECT Envio, COUNT(*) as Cantidad_Productos FROM ofertas_mercado GROUP BY Envio;'
        result = pd.read_sql_query(query, self.connection)
        return result

    def top10Asc(self):
        query = 'SELECT Nombre, Precio, Descuento, Tipo FROM ofertas_mercado ORDER BY CAST(Descuento AS DECIMAL(5,2)) ASC LIMIT 10;'
        result = pd.read_sql_query(query, self.connection)
        return result

    def descAsc(self):
        query = 'SELECT Descuento, COUNT(*) as Cantidad_Productos FROM vista_ofertas_descuento GROUP BY Descuento ORDER BY CAST(Descuento AS DECIMAL(5,2)) ASC LIMIT 10;'
        result = pd.read_sql(query, self.connection)
        return result


    def cerrar_conexion(self):
        self.cursor.close()
        self.connection.close()

if __name__ == "__main__":
    base = s.scrapper_ofertas()
    # Crear una instancia de la clase DataBase
    db = DataBase()

    try:
        # Crear la tabla (si no existe)
        db.create_table()

        # Insertar datos desde un archivo CSV
        archivo_csv = "datasets/mercado.csv"
        db.insert_data(archivo_csv)

    finally:
        # Cerrar la conexión
        db.cerrar_conexion()