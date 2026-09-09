class GPUWarpDivergence:
    """
    SIMT Warp Execution Simulator (32 threads).
    Tracks active thread masks during branch divergence and reconvergence.
    Implements warp vote primitives (__all_sync, __any_sync, __ballot_sync).
    """
    WARP_SIZE = 32

    def __init__(self):
        self.full_mask = (1 << self.WARP_SIZE) - 1

    def ballot_sync(self, active_mask, predicate_per_thread):
        ballot = 0
        for tid in range(self.WARP_SIZE):
            if (active_mask & (1 << tid)) and predicate_per_thread[tid]:
                ballot |= (1 << tid)
        return ballot

    def all_sync(self, active_mask, predicate_per_thread):
        return (self.ballot_sync(active_mask, predicate_per_thread) & active_mask) == active_mask

    def any_sync(self, active_mask, predicate_per_thread):
        return (self.ballot_sync(active_mask, predicate_per_thread) & active_mask) != 0

    def execute_branch(self, active_mask, condition_fn):
        then_mask = 0
        else_mask = 0
        for tid in range(self.WARP_SIZE):
            if active_mask & (1 << tid):
                if condition_fn(tid):
                    then_mask |= (1 << tid)
                else:
                    else_mask |= (1 << tid)
        return then_mask, else_mask
