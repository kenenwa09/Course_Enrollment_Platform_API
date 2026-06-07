import pytest

@pytest.mark.asyncio
async def test_enroll_success(client, student_token, sample_course):
    res = await client.post("/api/v1/enrollment/", json={"course_id": sample_course["id"]},
        headers={"Authorization": f"Bearer {student_token}"}
    )
    assert res.status_code == 201
    assert res.json()["course_id"] == sample_course["id"]

@pytest.mark.asyncio
async def test_enroll_duplicate(client, student_token, sample_course):
    await client.post("/api/v1/enrollment/", json={"course_id": sample_course["id"]},
        headers={"Authorization": f"Bearer {student_token}"})
    res = await client.post("/api/v1/enrollment/", json={"course_id": sample_course["id"]},
        headers={"Authorization": f"Bearer {student_token}"})
    assert res.status_code == 400
    assert "already enrolled" in res.json()["detail"]

@pytest.mark.asyncio
async def test_enroll_full_course(client, admin_token, student_token):
    course_res = await client.post("/api/v1/course/", json={
        "title": "Tiny Course", "code": "TINY1", "capacity": 1
    }, headers={"Authorization": f"Bearer {admin_token}"})
    course_id = course_res.json()["id"]

    
    await client.post("/api/v1/auth/register", json={
        "name": "Student2", "email": "s2@test.com", "password": "pass1234", "role": "student"
    })
    res2 = await client.post("/api/v1/auth/login", json={"email": "s2@test.com", "password": "pass1234"})
    token2 = res2.json()["access_token"]

    await client.post("/api/v1/enrollment/", json={"course_id": course_id},
        headers={"Authorization": f"Bearer {token2}"})

    
    res = await client.post("/api/v1/enrollment/", json={"course_id": course_id},
        headers={"Authorization": f"Bearer {student_token}"})
    assert res.status_code == 400
    assert "capacity" in res.json()["detail"]

@pytest.mark.asyncio
async def test_enroll_inactive_course(client, admin_token, student_token):
    course_res = await client.post("/api/v1/course/", json={
        "title": "Old Course", "code": "OLD01", "capacity": 10
    }, headers={"Authorization": f"Bearer {admin_token}"})
    course_id = course_res.json()["id"]
    await client.patch(f"/api/v1/course/{course_id}", json={"is_active": False},
        headers={"Authorization": f"Bearer {admin_token}"})

    res = await client.post("/api/v1/enrollment/", json={"course_id": course_id},
        headers={"Authorization": f"Bearer {student_token}"})
    assert res.status_code == 400
    assert "inactive" in res.json()["detail"]

@pytest.mark.asyncio
async def test_admin_cannot_enroll(client, admin_token, sample_course):
    res = await client.post("/api/v1/enrollment/", json={"course_id": sample_course["id"]},
        headers={"Authorization": f"Bearer {admin_token}"})
    assert res.status_code == 403

@pytest.mark.asyncio
async def test_unenroll(client, student_token, sample_course):
    enroll_res = await client.post("/api/v1/enrollment/", json={"course_id": sample_course["id"]},
        headers={"Authorization": f"Bearer {student_token}"})
    enrollment_id = enroll_res.json()["id"]
    res = await client.delete(f"/api/v1/enrollment/{enrollment_id}",
        headers={"Authorization": f"Bearer {student_token}"})
    assert res.status_code == 204

@pytest.mark.asyncio
async def test_my_enrollments(client, student_token, sample_course):
    await client.post("/api/v1/enrollment/", json={"course_id": sample_course["id"]},
        headers={"Authorization": f"Bearer {student_token}"})
    res = await client.get("/api/v1/enrollment/me",
        headers={"Authorization": f"Bearer {student_token}"})
    assert res.status_code == 200
    assert len(res.json()) == 1

@pytest.mark.asyncio
async def test_admin_view_all_enrollments(client, admin_token, student_token, sample_course):
    await client.post("/api/v1/enrollment/", json={"course_id": sample_course["id"]},
        headers={"Authorization": f"Bearer {student_token}"})
    res = await client.get("/api/v1/enrollment/",
        headers={"Authorization": f"Bearer {admin_token}"})
    assert res.status_code == 200

@pytest.mark.asyncio
async def test_student_cannot_view_all_enrollments(client, student_token):
    res = await client.get("/api/v1/enrollment/",
        headers={"Authorization": f"Bearer {student_token}"})
    assert res.status_code == 403