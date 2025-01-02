import time


class Block:
    def __init__(self, idx: int, size: int, file_id: int | None = None):
        self.idx = idx
        self.size = size
        self.file_id = file_id

    @property
    def idx_range(self) -> tuple[int, int]:
        return self.idx, self.idx + self.size - 1

    @property
    def is_file(self) -> bool:
        return self.file_id is not None

    @property
    def checksum(self) -> int:
        if not self.is_file:
            return 0
        return sum([i * self.file_id for i in range(self.idx, self.idx + self.size)])

    @property
    def display(self):
        return self.size * (str(self.file_id) if self.is_file else ".")

    def __repr__(self):
        block_type = "File" if self.is_file else "Free"
        return f"{block_type}({self.idx}, {self.idx + self.size - 1})"


class Disk:
    def __init__(self):
        self.blocks_by_idx_range: dict[tuple[int, int], Block] = {}
        self.file_id_to_block: dict[int, Block] = {}
        self.free_space_blocks: list[Block] = []
        self.pointer = 0

    def add_blocks(self, size: int, file_id: int | None = None):
        block = Block(self.pointer, size, file_id)

        self.blocks_by_idx_range[block.idx_range] = block
        self.pointer += size

        if file_id is not None:
            self.file_id_to_block[file_id] = block
        else:
            self.free_space_blocks.append(block)

    def get_first_free_space_block(self, size: int) -> Block | None:
        return next((b for b in self.free_space_blocks if b.size >= size), None)

    def compact(self) -> int:
        file_ids = list(self.file_id_to_block.keys())
        file_ids.reverse()

        for file_id in file_ids:

            file_block = self.file_id_to_block[file_id]
            free_block = self.get_first_free_space_block(file_block.size)

            if free_block and free_block.idx < file_block.idx:
                file_block.idx, free_block.idx = free_block.idx, file_block.idx
                self.blocks_by_idx_range[file_block.idx_range] = file_block
                self.blocks_by_idx_range[free_block.idx_range] = free_block

                remaining_free_space = free_block.size - file_block.size
                if remaining_free_space:
                    new_free_block = Block(file_block.idx + file_block.size, remaining_free_space)
                    self.free_space_blocks.append(new_free_block)
                    self.blocks_by_idx_range[new_free_block.idx_range] = new_free_block

                self.free_space_blocks.sort(key=lambda b: b.idx)

        return self._get_checksum()

    def _get_checksum(self) -> int:
        return sum([b.checksum for b in self.file_id_to_block.values()])

    def __repr__(self):
        ordered_blocks = list(self.blocks_by_idx_range.values())
        ordered_blocks.sort(key=lambda b: b.idx)
        return ", ".join([str(block) for block in ordered_blocks])

    @property
    def display(self) -> str:
        return "".join([b.display for b in self.blocks_by_idx_range.values()])


def main():

    disk = Disk()
    with open("../inputs/day09_input.txt", encoding="utf-8") as f:

        file_id = 0
        for idx, block_size in enumerate(f.read()):
            block_size = int(block_size)

            # file block
            if idx % 2 == 0:
                disk.add_blocks(block_size, file_id)
                file_id += 1

            # free space block
            elif block_size:
                disk.add_blocks(block_size)

    checksum = disk.compact()
    print(checksum)


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Runtime: {round(time.time() - start, 3)} seconds")
