# app/tests/test_notes.py

import pytest

# ----------------------------
# Test cases for Notes API
# ----------------------------

def test_create_note(client):
    """Test creating a new note"""
    response = client.post(
        "/api/v1/notes/",
        json={"title": "Test Note", "content": "This is a test"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Note"
    assert data["content"] == "This is a test"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

def test_get_notes(client):
    """Test retrieving all notes"""
    # Create a note first
    client.post("/api/v1/notes/", json={"title": "Note 1", "content": "Content 1"})
    client.post("/api/v1/notes/", json={"title": "Note 2", "content": "Content 2"})

    response = client.get("/api/v1/notes/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2  # At least the 2 notes we created

def test_get_single_note(client):
    """Test retrieving a single note by ID"""
    # Create a note first
    response = client.post("/api/v1/notes/", json={"title": "Single Note", "content": "Single Content"})
    note_id = response.json()["id"]

    response = client.get(f"/api/v1/notes/{note_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == note_id
    assert data["title"] == "Single Note"
    assert data["content"] == "Single Content"

def test_update_note(client):
    """Test updating an existing note"""
    # Create a note first
    response = client.post("/api/v1/notes/", json={"title": "Old", "content": "Old content"})
    note_id = response.json()["id"]

    # Update it
    response = client.put(f"/api/v1/notes/{note_id}", json={"title": "Updated", "content": "Updated content"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated"
    assert data["content"] == "Updated content"

def test_delete_note(client):
    """Test deleting a note"""
    # Create a note first
    response = client.post("/api/v1/notes/", json={"title": "To Delete", "content": "Delete me"})
    note_id = response.json()["id"]

    # Delete it
    response = client.delete(f"/api/v1/notes/{note_id}")
    assert response.status_code == 200
    assert response.json() == {"ok": True}

    # Check that it's gone
    response = client.get(f"/api/v1/notes/{note_id}")
    assert response.status_code == 404