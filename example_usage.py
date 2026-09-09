from client import GPUWarpDivergence

def main():
    print("=== Testing GPU Warp Divergence & Voting ===")
    gpu = GPUWarpDivergence()
    active = gpu.full_mask

    # Branch divergence condition: even vs odd thread IDs
    then_m, else_m = gpu.execute_branch(active, lambda tid: tid % 2 == 0)
    print(f"Full warp: 32 threads. Branch then_mask: {bin(then_m).count('1')} threads, else_mask: {bin(else_m).count('1')} threads")
    assert bin(then_m).count("1") == 16
    assert bin(else_m).count("1") == 16

    preds = [i >= 16 for i in range(32)]
    any_v = gpu.any_sync(active, preds)
    all_v = gpu.all_sync(active, preds)
    print(f"Warp vote: any_sync={any_v}, all_sync={all_v}")
    assert any_v is True and all_v is False
    print("=== All tests passed successfully! ===")

if __name__ == "__main__":
    main()
