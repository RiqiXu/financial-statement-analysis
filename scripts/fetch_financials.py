"""获取一家公司的原始报表。默认只获取利润表，--all 获取三张表。"""
import argparse
import json
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path

import akshare as ak


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stock", default="sh600519", help="新浪接口代码，包含 sh/sz 前缀")
    parser.add_argument("--all", action="store_true", help="获取三张财务报表")
    args = parser.parse_args()

    project = Path(__file__).resolve().parents[1]
    now = datetime.now(timezone.utc)
    output = project / "data" / "raw" / f"{args.stock}_{now.strftime('%Y%m%dT%H%M%S%fZ')}"
    output.mkdir(parents=True)
    tables = [("利润表", "profit.csv")]
    if args.all:
        tables += [("资产负债表", "balance.csv"), ("现金流量表", "cashflow.csv")]
    metadata = {
        "stock": args.stock,
        "fetched_at_utc": now.isoformat(),
        "source": "AKShare / Sina stock_financial_report_sina",
        "akshare_version": version("akshare"),
        "pandas_version": version("pandas"),
        "note": "原始历史报表；抓取时间、报告日、更新日期均不能直接当作首次公告日。",
        "tables": [],
    }
    try:
        for name, filename in tables:
            print(f"正在获取：{args.stock} / {name}", flush=True)
            df = ak.stock_financial_report_sina(stock=args.stock, symbol=name)
            if df.empty:
                raise ValueError(f"{name} 返回空表，请检查接口和股票代码")
            if "报告日" not in df.columns:
                raise ValueError(f"{name} 缺少报告日字段，请核对最新接口文档")
            path = output / filename
            df.to_csv(path, index=False, encoding="utf-8-sig")
            metadata["tables"].append({
                "name": name, "file": filename, "rows": len(df),
                "columns": list(df.columns),
            })
            print(f"已保存：{path}\n行数：{len(df)}，列数：{len(df.columns)}")
            print(df.iloc[:3, :5].to_string(index=False))
    except Exception as exc:
        metadata["error"] = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        (output / "metadata.json").write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8"
        )


if __name__ == "__main__":
    main()
