"""从已下载的原始报表计算 2024 年的三个学习指标。"""
import argparse
from pathlib import Path

import pandas as pd


REQUIRED_FILES = ("profit.csv", "balance.csv", "cashflow.csv")


def find_data_dir(project: Path) -> Path:
    """选择最近一个包含三张报表的 sh600519 数据目录。"""
    candidates = sorted((project / "data" / "raw").glob("sh600519_*"), reverse=True)
    for candidate in candidates:
        if all((candidate / filename).is_file() for filename in REQUIRED_FILES):
            return candidate
    raise FileNotFoundError(
        "找不到包含 profit.csv、balance.csv 和 cashflow.csv 的 sh600519 数据目录；"
        "请先运行 scripts/fetch_financials.py --all。"
    )


def get_report_row(df: pd.DataFrame, report_date: str, table_name: str) -> pd.Series:
    """按报告日精确选择唯一一行，避免误用最新季度数据。"""
    dates = df["报告日"].astype(str).str.replace(r"\.0$", "", regex=True)
    rows = df.loc[dates == report_date]
    if len(rows) != 1:
        raise ValueError(
            f"{table_name} 中报告日 {report_date} 应恰有一行，实际找到 {len(rows)} 行。"
        )
    return rows.iloc[0]


def number(row: pd.Series, column: str, table_name: str) -> float:
    """读取并校验需要参与计算的数值字段。"""
    value = pd.to_numeric(row[column], errors="coerce")
    if pd.isna(value):
        raise ValueError(f"{table_name} 的字段“{column}”为空或不是数字。")
    return float(value)


def main() -> None:
    project = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=None,
        help="三张 CSV 所在目录；省略时自动选择最新的完整 sh600519 数据目录",
    )
    parser.add_argument("--year", default="2024", help="要计算的年度，默认 2024")
    args = parser.parse_args()

    data_dir = args.data_dir or find_data_dir(project)
    missing = [name for name in REQUIRED_FILES if not (data_dir / name).is_file()]
    if missing:
        raise FileNotFoundError(f"数据目录缺少文件：{', '.join(missing)}（{data_dir}）")

    profit = pd.read_csv(data_dir / "profit.csv", encoding="utf-8-sig")
    balance = pd.read_csv(data_dir / "balance.csv", encoding="utf-8-sig")
    cashflow = pd.read_csv(data_dir / "cashflow.csv", encoding="utf-8-sig")
    for name, df in (("利润表", profit), ("资产负债表", balance), ("现金流量表", cashflow)):
        if "报告日" not in df.columns:
            raise ValueError(f"{name} 缺少“报告日”列。")

    year_end = f"{args.year}1231"
    prior_year_end = f"{int(args.year) - 1}1231"
    profit_year = get_report_row(profit, year_end, "利润表")
    balance_year = get_report_row(balance, year_end, "资产负债表")
    balance_prior = get_report_row(balance, prior_year_end, "资产负债表")
    cashflow_year = get_report_row(cashflow, year_end, "现金流量表")

    revenue = number(profit_year, "营业收入", "利润表")
    net_profit = number(profit_year, "净利润", "利润表")
    parent_net_profit = number(profit_year, "归属于母公司所有者的净利润", "利润表")
    operating_cash_flow = number(cashflow_year, "经营活动产生的现金流量净额", "现金流量表")
    equity_end = number(balance_year, "归属于母公司股东权益合计", "资产负债表")
    equity_begin = number(balance_prior, "归属于母公司股东权益合计", "资产负债表")

    if revenue == 0:
        raise ValueError("营业收入为零，无法计算销售净利率。")
    if net_profit <= 0:
        raise ValueError("净利润为零或负数，现金流质量比率不适合直接解释；请单独分析。")
    average_equity = (equity_begin + equity_end) / 2
    if average_equity == 0:
        raise ValueError("平均归母净资产为零，无法计算简化 ROE。")

    print(f"数据目录：{data_dir}")
    print(f"年度：{args.year}（利润与现金流报告日 {year_end}；ROE 使用 {prior_year_end} 和 {year_end} 年末净资产）")
    print(f"销售净利率：{net_profit / revenue:.2%}（净利润 / 营业收入）")
    print(f"现金流质量：{operating_cash_flow / net_profit:.2%}（经营活动现金流量净额 / 净利润）")
    print(f"简化 ROE：{parent_net_profit / average_equity:.2%}（归母净利润 / 平均归母净资产；不等同于年报加权平均 ROE）")
    print("已按数据字典与年报核对数值、单位和合并报表口径；正式披露公告日期仍待核实。")


if __name__ == "__main__":
    main()