from app import mongo_session
from pymongo.errors import PyMongoError, ConnectionFailure

def mongo_transaction_with_retry(func, *args, max_retry: int = 3):
    for _ in range(max_retry):
        try:
            with mongo_session.start_transaction():
                func(*args)
                mongo_session.commit_transaction()
                return
        except (PyMongoError, ConnectionFailure) as e:
            print(f"Error: {str(e)}. Retrying...")
        # if the exception is from function let it raise
   
    # if max retry reached raise Error
    mongo_session.abort_transaction()
    raise PyMongoError