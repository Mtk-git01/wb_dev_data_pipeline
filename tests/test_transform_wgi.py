import pandas as pd
import pandas as pd
from src.transform_wgi import transform_wgi, latest_non_null

def test_transform_wgi_basic():
    raw_df = pd.DataFrame({
        "Economy (name)": ["Japan", "Japan", "Azerbaijan", "Azerbaijan"],
        "Economy (code)": ["JPN", "JPN", "AZE", "AZE"],
        "Year": [2024, 2024, 2024, 2024],
        "Governance dimension": ["ge", "rq", "ge", "rq"],
        "Governance estimate (approx. -2.5 to +2.5)": [1.6, 1.5, -0.1, -0.3],
    })

    out = transform_wgi(raw_df)

    assert "government_effectiveness" in out.columns
    assert "regulatory_quality" in out.columns
    assert len(out) == 2