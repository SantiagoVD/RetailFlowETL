"""DimDate builder."""

import pandas as pd


class DimDateBuilder:
    def build(self, frame: pd.DataFrame, date_column: str = "sale_date") -> pd.DataFrame:
        dates = pd.to_datetime(frame[date_column]).drop_duplicates().sort_values()
        result = pd.DataFrame({"date": dates.dt.strftime("%Y-%m-%d")})
        parsed = pd.to_datetime(result["date"])
        result["date_key"] = parsed.dt.strftime("%Y%m%d").astype(int)
        result["day"] = parsed.dt.day
        result["day_of_week"] = parsed.dt.dayofweek + 1
        result["week"] = parsed.dt.isocalendar().week.astype(int)
        result["month"] = parsed.dt.month
        result["month_name"] = parsed.dt.month_name()
        result["quarter"] = parsed.dt.quarter
        result["year"] = parsed.dt.year
        return result[["date_key", "date", "day", "day_of_week", "week", "month", "month_name", "quarter", "year"]]
