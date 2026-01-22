"""
Application.Database.connection
Handles PostgreSQL database connection using psycopg2
"""

import psycopg2
from psycopg2 import pool
import logging

logger = logging.getLogger(__name__)


class DatabaseConnection:
    """Class to manage database connection pool"""
    
    _connection_pool = None
    
    @classmethod
    def initialize_pool(cls, database, user, password, host="localhost", port="5432", minconn=1, maxconn=10, **kwargs):
        """
        Initialize the connection pool
        """
        try:

            if 'sslmode' not in kwargs:
                kwargs['sslmode'] = 'require'
                
            cls._connection_pool = psycopg2.pool.SimpleConnectionPool(
                minconn,
                maxconn,
                database=database,
                user=user,
                password=password,
                host=host,
                port=port,
                **kwargs
            )
            logger.info("Database connection pool created successfully")
        except Exception as e:
            logger.error(f"Error creating connection pool: {e}")
            raise
    
    @classmethod
    def get_connection(cls):
        """
        Get a connection from the pool
        
        Returns:
            connection: psycopg2 connection object
        """
        if cls._connection_pool is None:
            raise Exception("Connection pool is not initialized. Call initialize_pool() first.")
        
        try:
            connection = cls._connection_pool.getconn()
            logger.debug("Connection retrieved from pool")
            return connection
        except Exception as e:
            logger.error(f"Error getting connection: {e}")
            raise
    
    @classmethod
    def return_connection(cls, connection):
        """
        Return a connection to the pool
        
        Args:
            connection: psycopg2 connection object to return
        """
        if cls._connection_pool is None:
            return
        
        try:
            cls._connection_pool.putconn(connection)
            logger.debug("Connection returned to pool")
        except Exception as e:
            logger.error(f"Error returning connection: {e}")
    
    @classmethod
    def close_all_connections(cls):
        """Close all connections in the pool"""
        if cls._connection_pool is not None:
            cls._connection_pool.closeall()
            logger.info("All database connections closed")


def execute_query(query, params=None, fetch=False):
    """
    Execute a SQL query with connection management
    
    Args:
        query (str): SQL query string
        params (tuple): Query parameters (default: None)
        fetch (bool): Whether to fetch results (default: False)
    
    Returns:
        list: Query results if fetch=True, else None
    """
    connection = None
    cursor = None
    
    try:
        connection = DatabaseConnection.get_connection()
        cursor = connection.cursor()
        
        cursor.execute(query, params or ())
        
        if fetch:
            result = cursor.fetchall()
            connection.commit()
            return result
        else:
            connection.commit()
            return None
            
    except Exception as e:
        if connection:
            connection.rollback()
        logger.error(f"Database error: {e}")
        raise
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            DatabaseConnection.return_connection(connection)