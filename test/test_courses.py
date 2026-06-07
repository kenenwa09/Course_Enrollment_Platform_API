import pytest

@pytest.mark.asyncio
async def test_list_courses_public(client, sample_course):
    res = await client.get("/api/v1/course/")
    assert res.status_code == 200
    assert len(res.json()) >= 1

@pytest.mark.asyncio
async def test_get_course_by_id(client, sample_course):
    res = await client.get(f"/api/v1/course/{sample_course['id']}")
    assert res.status_code == 200
    assert res.json()["code"] == "PY101"

@pytest.mark.asyncio
async def test_create_course_as_admin(client, admin_token):
    res = await client.post("/api/v1/course/", json={
        "title": "Advanced Django", "code": "DJ301", "capacity": 20
    }, headers={"Authorization": f"Bearer {admin_token}"})
    assert res.status_code == 201
    assert res.json()["code"] == "DJ301"

@pytest.mark.asyncio
async def test_create_course_as_student_forbidden(client, student_token):
    res = await client.post("/api/v1/course/", json={
        "title": "Hacking Course", "code": "HCK01", "capacity": 5
    }, headers={"Authorization": f"Bearer {student_token}"})
    assert res.status_code == 403

@pytest.mark.asyncio
async def test_create_course_duplicate_code(client, admin_token, sample_course):
    res = await client.post("/api/v1/course/", json={
        "title": "Another Python", "code": "PY101", "capacity": 10
    }, headers={"Authorization": f"Bearer {admin_token}"})
    assert res.status_code == 400

@pytest.mark.asyncio
async def test_update_course(client, admin_token, sample_course):
    res = await client.patch(f"/api/v1/course/{sample_course['id']}",
        json={"capacity": 50},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert res.status_code == 200
    assert res.json()["capacity"] == 50

@pytest.mark.asyncio
async def test_delete_course(client, admin_token, sample_course):
    res = await client.delete(f"/api/v1/course/{sample_course['id']}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert res.status_code == 204

@pytest.mark.asyncio
async def test_get_nonexistent_course(client):
    res = await client.get("/api/v1/course/99999")
    assert res.status_code == 404