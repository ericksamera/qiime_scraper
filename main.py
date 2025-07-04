# main.py

import argparse
from dataclasses import dataclass
from pathlib import Path

from modules import io_utils, iterators, logger, qiime_wrapper

@dataclass
class Args:
    fastq_dir: Path
    dry_run: bool = False

def get_args() -> Args:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--fastq-dir",
        type=Path,
        required=True,
        help="Directory containing .fastq.gz files.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print commands without executing")
    
    args = parser.parse_args()
    return Args(**vars(args))

def main() -> None:

    args = get_args()

    log = logger.setup_logger()

    project_fastq_dir: Path = args.fastq_dir.resolve()

    io_utils.generate_manifest(project_fastq_dir)

    qiime_wrapper.import_data(
        input_path=project_fastq_dir.joinpath('fastq.manifest'),
        output_path=project_fastq_dir.joinpath('output.qza'),
        dry_run=False
    )

    f, r = iterators.get_optimal_trimming(imported_qza=project_fastq_dir.joinpath('output.qza'))

    iterators.get_optimal_classifier(
        imported_qza=project_fastq_dir / ".work" / ".optimal_trimming" / f"{f}-{r}_output_rep_seqs.qza",
        classifiers_dir=Path('/home/erick/qiime'))

if __name__ == "__main__":
    main()
# ---