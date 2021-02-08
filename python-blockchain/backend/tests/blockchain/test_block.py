import time
from backend.blockchain.block import Block, GENESIS_DATA
from backend.util.hex_to_binary import hex_to_binary
from backend.config import MINE_RATE, SECONDS


def test_mine_block():
    last_block = Block.genesis()
    data = "test-data"
    block = Block.mine_block(last_block, data)
    assert isinstance(block, Block)
    assert block.data == data
    assert block.last_hash == last_block.hash
    assert hex_to_binary(block.hash)[
        0:block.difficulty] == '0' * block.difficulty


def test_genesis():
    genesis = Block.genesis() 
    assert isinstance(genesis, Block)
    for key, value in GENESIS_DATA.items():
        assert(getattr(genesis, key) == value)


def test_quickly_mined_block():
    genesis = Block.genesis() # expect difficulty = 3
    assert genesis.difficulty == 3
    last_block = Block.mine_block(genesis, 'foo') ## expect have difficulty 4
    assert last_block.difficulty == 4
    mined_block = Block.mine_block(last_block, 'bar') # expect difficulty 5 actually a 4. Not anymore-- fixed 
    assert mined_block.difficulty == last_block.difficulty + 1 # expect 5 = 4 + 1 
    second_mined_block = Block.mine_block(mined_block, 'bear')
    assert second_mined_block.difficulty == mined_block.difficulty + 1 # expect 5 = 4 + 1 
    

def test_slowly_mined_block(): # system can only start working on 4th block because it compares third with second. First is corrupt with magic number
    first_block = Block.genesis()
    second_block = Block.mine_block(first_block, 'foo')
    time.sleep(MINE_RATE / SECONDS) # Should trigger a decrease based on timestamp. Has to be between 2nd and third
    third_block = Block.mine_block(second_block, 'fee')
    fourth_block = Block.mine_block(third_block, 'bar')
    assert fourth_block.difficulty == third_block.difficulty - 1


#Takes a long time, better to turn off when not using
# def test_mined_block_difficulty_limits_at_1(): ## need to walk back from 5 to 0 so 5 sleeps. 
#     first_block = Block.genesis() # 3 as magic number
#     second_block = Block.mine_block(first_block, 'foo') # 4 as magic number 
#     time.sleep(MINE_RATE / SECONDS) # Sleep 1
#     third_block = Block.mine_block(second_block, 'fee') # 5 as magic number
#     time.sleep(MINE_RATE / SECONDS) # Sleep 2
#     fourth_block = Block.mine_block(third_block, 'bar') # First computation, comparing 3 and 2. Walk back from 5 due to sleep 1 => 4
#     time.sleep(MINE_RATE / SECONDS) # Sleep 3
#     fifth_block = Block.mine_block(fourth_block, 'bb') # Second computation, comparing 4 and 3. Walk back from 4 to 3
#     time.sleep(MINE_RATE / SECONDS) # Sleep 4
#     sixth_block = Block.mine_block(fifth_block, 'boy') # Third computation, comparing 5 and 4. Walk back from 3 to 2
#     time.sleep(MINE_RATE / SECONDS) # Sleep 5
#     seventh_block = Block.mine_block(sixth_block, 'bit') # fourth computation, comparing 6 and 5. Walk back from 2 to 1
#     eighth_block = Block.mine_block(seventh_block, 'byte') # fifth computation, comparing 7 and 6. Walk back from 1 to 0 but prevented from hitting 0
#     assert eighth_block.difficulty == 1
