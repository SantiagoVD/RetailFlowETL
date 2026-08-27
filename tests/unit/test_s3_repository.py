from retailflow_etl.storage.s3_repository import InMemoryS3Repository


def test_in_memory_repository_supports_objects_and_json():
    repository = InMemoryS3Repository()
    repository.put_object("input/test.csv", b"a,b\n1,2\n")
    repository.write_json("metadata/run.json", {"status": "SUCCESS"})
    assert repository.object_exists("input/test.csv")
    assert repository.get_object("input/test.csv").startswith(b"a,b")
    assert repository.read_json("metadata/run.json")["status"] == "SUCCESS"
