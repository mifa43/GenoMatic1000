from pathlib import Path
from typing import Any
import json
import pandas as pd

# Unutar raw_parser.py promeni ovo:
from parser.helpers.detect_file_type import detect_file_type


class RawParser:
    def __init__(self, file_path: str | Path):
        self.file_path = Path(file_path)

    def read(self) -> pd.DataFrame:
        file_extension = detect_file_type(self.file_path)

        if file_extension is None:
            raise ValueError(f"Unsupported file type: {self.file_path}")

        if file_extension == ".csv":
            return self._read_csv()

        if file_extension == ".tsv":
            return self._read_tsv()

        if file_extension == ".bed":
            return self._read_bed()

        if file_extension == ".json":
            return self._read_json()

        if file_extension == ".txt":
            return self._read_txt()

        if file_extension == ".vcf":
            return self._read_vcf()

        raise ValueError(f"No reader implemented for: {file_extension}")

    def _read_csv(self) -> pd.DataFrame:
        return pd.read_csv(self.file_path)

    def _read_tsv(self) -> pd.DataFrame:
        return pd.read_csv(self.file_path, sep="\t")

    def _read_json(self) -> pd.DataFrame:
        """
        Robust JSON reader for Ensembl/NCBI style JSON.

        Handles:
        - list[dict]
        - dict
        - dict with nested list fields
        - dict with nested metadata
        """

        with open(self.file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Case 1: JSON is already a list of records
        if isinstance(data, list):
            return pd.json_normalize(data)

        # Case 2: JSON is a dict
        if isinstance(data, dict):
            # Prefer common biological record containers if present
            candidate_keys = [
                "features",
                "genes",
                "transcripts",
                "mappings",
                "overlap",
                "records",
                "results",
                "data",
            ]

            for key in candidate_keys:
                value = data.get(key)

                if isinstance(value, list):
                    df = pd.json_normalize(value)
                    df.attrs["json_metadata"] = {
                        k: v for k, v in data.items() if k != key
                    }
                    df.attrs["json_record_key"] = key
                    return df

            # Case 3: dict without obvious record list
            # Flatten as a single-row DataFrame
            return pd.json_normalize(data)

        # Case 4: scalar JSON, rare but valid
        return pd.DataFrame({"value": [data]})

    def _read_txt(self) -> pd.DataFrame:
        with open(self.file_path, "r", encoding="utf-8") as file:
            lines = [line.rstrip("\n") for line in file]

        return pd.DataFrame(
            {
                "line_number": range(1, len(lines) + 1),
                "content": lines,
            }
        )

    def _read_bed(self) -> pd.DataFrame:
        """
        BED trap:
        BED files usually do not have a header.
        Minimal BED columns are:
        chrom, chromStart, chromEnd

        BED coordinates are 0-based, half-open.
        VCF coordinates are usually 1-based.
        """

        bed_columns = [
            "chrom",
            "start_0based",
            "end_0based",
            "name",
            "score",
            "strand",
        ]

        df = pd.read_csv(
            self.file_path,
            sep="\t",
            header=None,
            comment="#",
        )

        df.columns = bed_columns[: len(df.columns)]

        if "start_0based" in df.columns:
            df["start_1based"] = df["start_0based"] + 1

        return df

    def _read_vcf(self) -> pd.DataFrame:
        """
        VCF trap:
        - Lines starting with ## are metadata.
        - The line starting with #CHROM is the real table header.
        - Do not use comment='#' directly, because it removes the header.
        """

        metadata_lines: list[str] = []
        header: list[str] | None = None
        records: list[list[str]] = []

        with open(self.file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.rstrip("\n")

                if not line:
                    continue

                if line.startswith("##"):
                    metadata_lines.append(line)
                    continue

                if line.startswith("#CHROM"):
                    header = line.lstrip("#").split("\t")
                    continue

                records.append(line.split("\t"))

        if header is None:
            raise ValueError(f"VCF header line '#CHROM' not found in: {self.file_path}")

        df = pd.DataFrame(records, columns=header)

        df.attrs["vcf_metadata"] = metadata_lines

        df = self._normalize_vcf_columns(df)

        return df

    def _normalize_vcf_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Converts basic VCF columns into useful typed columns.
        Keeps raw INFO but also expands common SV/CNV fields.
        """

        rename_map = {
            "CHROM": "chrom",
            "POS": "pos",
            "ID": "id",
            "REF": "ref",
            "ALT": "alt",
            "QUAL": "qual",
            "FILTER": "filter",
            "INFO": "info",
        }

        df = df.rename(columns=rename_map)

        if "pos" in df.columns:
            df["pos"] = pd.to_numeric(df["pos"], errors="coerce").astype("Int64")

        if "qual" in df.columns:
            df["qual"] = pd.to_numeric(df["qual"], errors="coerce")

        if "info" in df.columns:
            info_df = df["info"].apply(self._parse_vcf_info).apply(pd.Series)
            df = pd.concat([df, info_df], axis=1)

        # Common structural variant fields
        for col in ["END", "SVLEN", "CN"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

        # Project-friendly aliases
        if "END" in df.columns:
            df["end"] = df["END"]

        if "SVTYPE" in df.columns:
            df["variant_class"] = df["SVTYPE"]

        if "CN" in df.columns:
            df["copy_number"] = df["CN"]

        if "SVLEN" in df.columns:
            df["svlen"] = df["SVLEN"]

        return df

    @staticmethod
    def _parse_vcf_info(info_value: Any) -> dict[str, Any]:
        """
        Parses INFO field like:
        SVTYPE=DUP;END=15272292;SVLEN=42519;CN=3

        Also supports flags without '='.
        """

        if pd.isna(info_value):
            return {}

        result: dict[str, Any] = {}

        for item in str(info_value).split(";"):
            if not item:
                continue

            if "=" in item:
                key, value = item.split("=", 1)
                result[key] = value
            else:
                result[item] = True

        return result