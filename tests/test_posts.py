import pytest
from app import schemas

def test_get_all_posts(authorized_client, test_post):
    res = authorized_client.get("/posts/")
    
    def validate(post):
        return schemas.PostOut(**post)
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)
    
    assert len(res.json()) == len(test_post)
    assert res.status_code == 200

def test_unauthorized_user_get_all_posts(client, test_post):
    res = client.get("/posts/")
    assert res.status_code == 401
    
def test_unauthorized_user_get_one_post(client, test_post):
    res = client.get(f"/posts/{test_post[0].id}")
    assert res.status_code == 200
    
def test_get_one_post_not_exist(authorized_client, test_post):
    res = authorized_client.get(f"/posts/88888")
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_post):
    res = authorized_client.get(f"/posts/{test_post[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_post[0].id
    assert post.Post.content == test_post[0].content
    assert post.Post.title == test_post[0].title

@pytest.mark.parametrize("title, content, published", [
    ("How I built my first API", "A quick look into FastAPI basics", True),
    ("Best coding snacks", "Why I think pizza wins every time", False),
    ("Deploying to the cloud", "Lessons from my first CI/CD pipeline", True),
])
def test_create_post(authorized_client, test_user, test_post, title, content, published):
    res = authorized_client.post(
        "/posts/", 
        json={"title": title, "content": content, "published": published}
    )

    created_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.user_id == test_user['id']

def test_create_post_default_published_true(authorized_client, test_user, test_post):
    res = authorized_client.post("/posts/", 
        json={"title": "My journey with pytest", "content": "Simple tips to get started"})

    created_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == "My journey with pytest"
    assert created_post.content == "Simple tips to get started"
    assert created_post.published == True
    assert created_post.user_id == test_user['id']

def test_unauthorized_user_create_post(client, test_post):
    res = client.post("/posts/", 
        json={"title": "My journey with pytest", "content": "Simple tips to get started"})
    
def test_unauthorized_user_delete_post(client,test_user, test_post):
    res = client.delete(f"/posts/{test_post[0].id}")
    assert res.status_code == 401
    
def test_delete_post_success(authorized_client, test_user, test_post):
    res = authorized_client.delete(f"/posts/{test_post[0].id}")
    assert res.status_code == 204
    
def test_delete_post_not_exist(authorized_client, test_user, test_post):
    res = authorized_client.delete(f"/posts/100000")
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_user, test_post):
    res = authorized_client.delete(f"/posts/{test_post[3].id}")
    assert res.status_code == 403
    
def test_update_post(authorized_client, test_user, test_post):
    data = {
        "title": "updt title",
        "content": "updt content",
        "id": test_post[0].id
    }
    res = authorized_client.put(f"/posts/{test_post[0].id}", json=data)
    updated_post = schemas.PostResponse(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']
    
def test_update_other_user_post(authorized_client, test_user, test_user2, test_post):
    data = {
        "title": "updt title",
        "content": "updt content",
        "id": test_post[3].id
    }
    res = authorized_client.put(f"/posts/{test_post[3].id}", json=data)
    assert res.status_code == 403

def test_unauthorized_user_update_post(client,test_user, test_post):
    res = client.put(f"/posts/{test_post[0].id}")
    assert res.status_code == 401
    
def test_update_post_not_exist(authorized_client, test_user, test_post):
    data = {
        "title": "updt title",
        "content": "updt content",
        "id": test_post[3].id
    }
    res = authorized_client.put(f"/posts/100000", json=data)
    assert res.status_code == 404