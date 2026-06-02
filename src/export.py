from pathlib import Path


def save_summary(
    summary,
    filename
):

    output_dir = Path(
        "outputs"
    )

    output_dir.mkdir(
        exist_ok=True
    )

    file_path = (
        output_dir /
        filename
    )

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(summary)

    return str(file_path)