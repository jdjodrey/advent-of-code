import time


class Block:
    def __init__(self, file_id: int | None = None):
        self.file_id = file_id

    @property
    def is_file(self):
        return self.file_id is not None

    def __repr__(self):
        return str(self.file_id) if self.is_file else "."


class Disk:
    def __init__(self):
        self.blocks: list[Block] = []
        self.first_free_space_idx: int = -1

    def add_blocks(self, blocks: list[Block]):
        self.blocks.extend(blocks)

    def compact(self) -> int:
        # note the first available free space
        self._update_first_free_space_idx()

        for idx in range(len(self.blocks) - 1, 0, -1):
            block = self.blocks[idx]
            if block.is_file:

                free_space_idx = self.first_free_space_idx

                # make sure the free space is to the left
                if free_space_idx < idx:
                    free_space_block = self.blocks.pop(free_space_idx)
                    self.blocks.insert(free_space_idx, block)
                    self.blocks[idx] = free_space_block

                    self._update_first_free_space_idx(free_space_idx)

        return self._get_checksum()

    def _update_first_free_space_idx(self, start: int = 0):
        for idx in range(start, len(self.blocks)):
            block = self.blocks[idx]
            if not block.is_file:
                self.first_free_space_idx = idx
                break

    def _get_checksum(self) -> int:
        checksum = 0
        for idx, block in enumerate(self.blocks):
            if not block.is_file:
                break

            checksum += idx * block.file_id

        return checksum

    def __repr__(self):
        return "".join([str(block) for block in self.blocks])


def main():

    disk = Disk()
    with open("../inputs/day09_input.txt", encoding="utf-8") as f:

        file_id = 0
        for idx, block_size in enumerate(f.read()):
            block_size = int(block_size)

            # file block
            if idx % 2 == 0:
                disk.add_blocks([Block(file_id) for _ in range(block_size)])
                file_id += 1

            # free space block
            elif block_size:
                disk.add_blocks([Block() for _ in range(block_size)])

    checksum = disk.compact()
    print(checksum)


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Runtime: {round(time.time() - start, 3)} seconds")
