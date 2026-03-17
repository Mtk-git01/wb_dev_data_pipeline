import pandas as pd

from src.transform_trade import transform_trade_long, latest_trade_snapshot


def test_transform_trade_long_basic():
    raw = pd.DataFrame({
        "requested_reporter_iso3": ["GHA"],
        "requested_reporter_name": ["Ghana"],
        "requested_hs_code": ["1801"],
        "requested_hs_label": ["Cocoa beans"],
        "requested_flow_code": ["X"],
        "requested_flow_name": ["Export"],
        "period": [2023],
        "partnerCode": ["0"],
        "partnerDesc": ["World"],
        "primaryValue": [1107356000],
        "netWgt": [433288041],
    })

    result = transform_trade_long(raw)

    assert result["reporter_name"].iloc[0] == "Ghana"
    assert result["reporter_iso3"].iloc[0] == "GHA"
    assert int(result["year"].iloc[0]) == 2023
    assert result["hs_code"].iloc[0] == "1801"
    assert result["flow_code"].iloc[0] == "X"
    assert float(result["trade_value_usd"].iloc[0]) == 1107356000
    assert float(result["net_weight_kg"].iloc[0]) == 433288041


def test_latest_trade_snapshot_picks_latest():
    df = pd.DataFrame({
        "reporter_name": ["Ghana", "Ghana"],
        "reporter_iso3": ["GHA", "GHA"],
        "year": [2022, 2023],
        "hs_code": ["1801", "1801"],
        "hs_label": ["Cocoa beans", "Cocoa beans"],
        "flow_code": ["X", "X"],
        "flow_name": ["Export", "Export"],
        "partner_code": ["0", "0"],
        "partner_name": ["World", "World"],
        "trade_value_usd": [100, 120],
        "net_weight_kg": [10, 12],
        "source_name": ["UN Comtrade", "UN Comtrade"],
        "load_timestamp": [pd.Timestamp("2026-01-01"), pd.Timestamp("2026-01-01")],
    })

    latest = latest_trade_snapshot(df)

    assert len(latest) == 1
    assert latest["year"].iloc[0] == 2023
    assert latest["trade_value_usd"].iloc[0] == 120
    assert latest["net_weight_kg"].iloc[0] == 12