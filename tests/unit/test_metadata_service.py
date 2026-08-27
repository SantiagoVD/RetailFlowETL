from retailflow_etl.metadata.metadata_service import MetadataService
from retailflow_etl.storage.path_builder import PathBuilder
from retailflow_etl.storage.s3_repository import InMemoryS3Repository


def test_metadata_records_run_and_processed_checksum():
    repo = InMemoryS3Repository()
    service = MetadataService(repo, PathBuilder())
    run = service.new_run("sales", "sales.csv")
    service.finish(run, "SUCCESS")
    service.mark_processed(run, "abc")
    assert service.is_processed("sales", "abc")
    assert repo.read_json(f"metadata/runs/{run.run_id}.json")["status"] == "SUCCESS"
