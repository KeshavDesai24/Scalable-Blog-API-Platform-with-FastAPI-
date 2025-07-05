import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db
from app import models
from alembic import command
from app.oauth2 import create_access_token

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    # run our code before we return our test
    # models.Base.metadata.create_all(bind=engine)
    # command.upgrade("head")
    yield TestClient(app)
    # command.downgrade("base")
    # run our code after our test finishes
    # models.Base.metadata.drop_all(bind=engine)
    
@pytest.fixture
def test_user2(client):
    user_data = {"email": "testing123@gmail.com", "password": "testing123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user(client):
    user_data = {"email": "testing@gmail.com", "password": "testing"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_post(test_user, session, test_user2):
    posts_data = [{
    "title": "Why FastAPI is Awesome",
    "content": "A quick look at why FastAPI makes building APIs so efficient.",
    "user_id": test_user['id']
    }, {
    "title": "Tips for Debugging",
    "content": "Simple strategies to make debugging less painful and more productive.",
    "user_id": test_user['id']
    }, {
    "title": "Docker Basics",
    "content": "Understand containers, images, and why Docker is loved by developers.",
    "user_id": test_user['id']
    }, {
    "title": "Git Basics",
    "content": "Study git add, commit, push, pull etc",
    "user_id": test_user2['id']
    }]
    
    def create_post_model(post):
        return models.Post(**post)
        
    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    
    session.add_all(posts)
    
    # session.add_all([models.Post(tiitle="Why FastAPI is Awesome", content="A quick look at why FastAPI makes building APIs so efficient.", owner_id= test_user['id']),
                                        
    # models.Post(tiitle="Tips for Debugging", content="Simple strategies to make debugging less painful and more productive.", owner_id=test_user['id']),
    
    # models.Post(tiitle="Docker Basics", content="Understand containers, images, and why Docker is loved by developers.", owner_id=test_user['id'])])
    
    session.commit()
    posts = session.query(models.Post).all()
    return posts
