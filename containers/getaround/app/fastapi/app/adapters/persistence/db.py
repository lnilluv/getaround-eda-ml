import asyncpg


class AsyncpgUserGateway:
    def __init__(self, db_url: str) -> None:
        self._db_url = db_url
        self._pool: asyncpg.Pool | None = None

    async def connect(self) -> None:
        if self._pool is None:
            self._pool = await asyncpg.create_pool(self._db_url)

    async def disconnect(self) -> None:
        if self._pool is not None:
            await self._pool.close()
            self._pool = None

    async def create_schema(self) -> None:
        if self._pool is None:
            raise RuntimeError("Database pool is not initialized")
        async with self._pool.acquire() as connection:
            await connection.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    email VARCHAR(128) UNIQUE NOT NULL,
                    active BOOLEAN NOT NULL DEFAULT TRUE
                );
                """
            )

    async def seed_default_user(self) -> None:
        if self._pool is None:
            raise RuntimeError("Database pool is not initialized")
        async with self._pool.acquire() as connection:
            await connection.execute(
                """
                INSERT INTO users (email, active)
                VALUES ('contact@pryda.dev', TRUE)
                ON CONFLICT (email) DO NOTHING;
                """
            )

    async def list_users(self) -> list[dict]:
        if self._pool is None:
            raise RuntimeError("Database pool is not initialized")
        async with self._pool.acquire() as connection:
            rows = await connection.fetch(
                "SELECT id, email, active FROM users ORDER BY id ASC;"
            )
            return [dict(row) for row in rows]
