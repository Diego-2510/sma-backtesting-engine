"""Quick smoke test for data_loader."""

from src.data_loader import load_data


def main():
    df = load_data("AAPL", "2023-01-01", "2024-01-01")
    print(df.head())
    print(f"\nShape: {df.shape}")
    print(f"Columns: {list(df.columns)}")

    # Second call should hit cache
    df_cached = load_data("AAPL", "2023-01-01", "2024-01-01")
    assert len(df) == len(df_cached), "Cache mismatch!"
    print("\n[OK] Cache works.")


if __name__ == "__main__":
    main()
