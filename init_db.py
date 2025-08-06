from server.storage import Base, engine

Base.metadata.create_all(engine)
print("Table created successfully.")