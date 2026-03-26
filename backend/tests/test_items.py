import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestCreateItem:
    async def test_create_item_success(self, client: AsyncClient, sample_item_data: dict):
        response = await client.post("/items/", json=sample_item_data)

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == sample_item_data["title"]
        assert data["description"] == sample_item_data["description"]
        assert data["is_active"] is True
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    async def test_create_item_minimal(self, client: AsyncClient):
        response = await client.post("/items/", json={"title": "Minimal Item"})

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Minimal Item"
        assert data["description"] is None
        assert data["is_active"] is True

    async def test_create_item_without_title(self, client: AsyncClient):
        response = await client.post("/items/", json={"description": "No title"})

        assert response.status_code == 422


class TestGetItems:
    async def test_get_items_empty(self, client: AsyncClient):
        response = await client.get("/items/")

        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0
        assert data["page"] == 1
        assert data["page_size"] == 10

    async def test_get_items_with_data(self, client: AsyncClient, sample_item_data: dict):
        await client.post("/items/", json=sample_item_data)
        await client.post("/items/", json={"title": "Second Item"})

        response = await client.get("/items/")

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert data["total"] == 2

    async def test_get_items_pagination(self, client: AsyncClient):
        for i in range(15):
            await client.post("/items/", json={"title": f"Item {i}"})

        response = await client.get("/items/?page=2&page_size=10")

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 5
        assert data["page"] == 2
        assert data["total"] == 15

    async def test_get_items_filter_active(self, client: AsyncClient):
        await client.post("/items/", json={"title": "Active Item", "is_active": True})
        await client.post("/items/", json={"title": "Inactive Item", "is_active": False})

        response = await client.get("/items/?active_only=true")

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["is_active"] is True


class TestGetItemById:
    async def test_get_item_by_id_success(self, client: AsyncClient, sample_item_data: dict):
        create_response = await client.post("/items/", json=sample_item_data)
        item_id = create_response.json()["id"]

        response = await client.get(f"/items/{item_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == item_id
        assert data["title"] == sample_item_data["title"]

    async def test_get_item_by_id_not_found(self, client: AsyncClient):
        response = await client.get("/items/999")

        assert response.status_code == 404


class TestUpdateItem:
    async def test_update_item_success(self, client: AsyncClient, sample_item_data: dict):
        create_response = await client.post("/items/", json=sample_item_data)
        item_id = create_response.json()["id"]

        update_data = {"title": "Updated Title", "description": "Updated description"}
        response = await client.patch(f"/items/{item_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["description"] == "Updated description"

    async def test_update_item_partial(self, client: AsyncClient, sample_item_data: dict):
        create_response = await client.post("/items/", json=sample_item_data)
        item_id = create_response.json()["id"]

        response = await client.patch(f"/items/{item_id}", json={"is_active": False})

        assert response.status_code == 200
        data = response.json()
        assert data["is_active"] is False
        assert data["title"] == sample_item_data["title"]

    async def test_update_item_not_found(self, client: AsyncClient):
        response = await client.patch("/items/999", json={"title": "New Title"})

        assert response.status_code == 404


class TestDeleteItem:
    async def test_delete_item_success(self, client: AsyncClient, sample_item_data: dict):
        create_response = await client.post("/items/", json=sample_item_data)
        item_id = create_response.json()["id"]

        response = await client.delete(f"/items/{item_id}")

        assert response.status_code == 204

        get_response = await client.get("/items/")
        assert get_response.json()["total"] == 0

    async def test_delete_item_not_found(self, client: AsyncClient):
        response = await client.delete("/items/999")

        assert response.status_code == 404


class TestHealthEndpoint:
    async def test_health_check(self, client: AsyncClient):
        response = await client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "environment" in data


class TestRootEndpoint:
    async def test_root(self, client: AsyncClient):
        response = await client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert "docs" in data