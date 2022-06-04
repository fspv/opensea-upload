import argparse
import json
import os
from dataclasses import asdict, dataclass, field
from typing import Iterator, List, Union


@dataclass
class Property:
    pass


@dataclass
class Level:
    pass


@dataclass
class Stat:
    pass


# pylint: disable=too-many-instance-attributes
@dataclass
class NFT:
    file_path: str
    nft_name: str
    external_link: str = ""
    description: str = ""
    collection: str = ""
    properties: List[Property] = field(default_factory=list)
    levels: List[Level] = field(default_factory=list)
    stats: List[Stat] = field(default_factory=list)
    unlockable_content: List[Union[str, bool]] = field(default_factory=list)
    explicit_and_sensitive_content: bool = False
    supply: int = 0
    blockchain: str = ""


@dataclass
class Result:
    nft: List[NFT] = field(default_factory=list)


@dataclass
class ImageFile:
    file_path: str
    description: str


def _get_image_files(directory: str) -> Iterator[ImageFile]:
    files: List[str] = sorted(map(lambda file: directory + file, os.listdir(directory)))

    for file in files:
        if file.endswith(".jpg"):
            description_path = file + "_description.txt"
            if os.path.exists(description_path):
                with open(
                    file + "_description.txt", encoding="utf-8"
                ) as description_file:
                    description = description_file.read()
            else:
                description = ""

            yield ImageFile(file, description)


def _get_nfts(
    image_files: List[ImageFile],
    collection: str = "",
    start: int = 0,
    stop: int = 2**64,
) -> Iterator[NFT]:
    for pos, image_file in enumerate(list(image_files[start:stop])):
        yield NFT(
            file_path=image_file.file_path,
            nft_name=f"Mem #{pos + start}",
            collection=collection,
            description=image_file.description,
        )


def _parse_args() -> argparse.Namespace:
    """
    Parse command line arguments for the script
    """
    parser = argparse.ArgumentParser(
        description="Generate json to feed to opensea uploader"
    )
    parser.add_argument(
        "--start", type=int, help="Start generation from this image", default=0
    )
    parser.add_argument(
        "--stop", type=int, help="Stop generation on this image", default=2**64
    )
    parser.add_argument(
        "--collection", type=str, help="Collection the NFT belongs to", default=""
    )
    parser.add_argument(
        "--output",
        type=str,
        help="File to write the resulting json to",
        required=True,
    )
    parser.add_argument(
        "--source-dir",
        type=str,
        help="Directory with the source images",
        required=True,
    )

    args = parser.parse_args()

    return args


def main() -> None:
    args = _parse_args()

    result = Result(
        list(
            _get_nfts(
                list(_get_image_files(args.source_dir)),
                args.collection,
                args.start,
                args.stop,
            )
        )
    )

    with open(args.output, "w", encoding="utf-8") as file:
        file.write(json.dumps(asdict(result)))


if __name__ == "__main__":
    main()
