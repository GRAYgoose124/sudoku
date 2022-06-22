nonets = [(1,1),(1,4),(1,7),(4,1),(4,4),(4,7),(7,1),(7,4),(7,7)]
neighbors = [(-1, -1),  (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]


def get_nonet_idx(pos):
    idxs = list(map(lambda n: ((n[0]-pos[0])**2 + (n[1]-pos[1])**2)**0.5, nonets))
    return idxs.index(min(idxs))


def get_nonet(board, pos):
    bucket = []
    idx = get_nonet_idx(pos)
    for n in neighbors:
        k = nonets[idx] 
        bucket.append(board[n[0] + k[0]][n[1] + k[1]])

    return bucket


def is_filled(board):
    for r in board:
        if 0 in r:
            return False
    
    return True