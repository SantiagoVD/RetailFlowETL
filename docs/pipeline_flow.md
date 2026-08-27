# Pipeline flow

1. Parse and URL-decode the first S3 notification record.
2. Validate `input/<dataset>/` and select CSV, JSON or XLSX reader.
3. Read bytes, calculate SHA-256 and check processed metadata.
4. Extract a dataframe and write Bronze Parquet with source/run columns.
5. Apply configured null, duplicate, datatype, range, date and business rules.
6. Write rejected rows plus error codes/messages to Quarantine.
7. Normalize valid rows into Silver and write Parquet.
8. Build Gold facts/dimensions and write Parquet.
9. Persist run metadata and mark the checksum successful only after all stages complete.
