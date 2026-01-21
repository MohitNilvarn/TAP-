import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

async def test_connection():
    uri = os.getenv("MONGODB_URI")
    print(f"Testing connection to: {uri.split('@')[1]}") # Hide password
    
    try:
        client = AsyncIOMotorClient(uri)
        await client.admin.command('ping')
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())
