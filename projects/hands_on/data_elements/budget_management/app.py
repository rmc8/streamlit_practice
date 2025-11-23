from datetime import date
from dataclasses import dataclass

import pandas as pd
import streamlit as st

# ページ設定
st.set_page_config(page_title="家計簿アプリ", page_icon="💰", layout="wide")

# タイトル
st.title("💰 家計簿アプリ")

# 定数定義
MONTHLY_BUDGET = 200000  # 月間予算20万円
CATEGORIES = ["食費", "交通費", "通信費", "その他費用"]


# サンプルデータの作成
def create_sample_data():
    """サンプル支出データを作成"""
    sample_data = [
        {"日付": date(2024, 1, 10), "カテゴリ": "食費", "金額": 1500, "メモ": "昼食"},
        {
            "日付": date(2024, 1, 12),
            "カテゴリ": "交通費",
            "金額": 500,
            "メモ": "電車代",
        },
        {
            "日付": date(2024, 1, 15),
            "カテゴリ": "通信費",
            "金額": 8000,
            "メモ": "携帯電話料金",
        },
        {
            "日付": date(2024, 1, 18),
            "カテゴリ": "その他費用",
            "金額": 3000,
            "メモ": "本の購入",
        },
    ]
    return pd.DataFrame(sample_data)


# カラム設定の定義
def get_column_config():
    """カラム設定を定義"""
    return {
        "日付": st.column_config.DateColumn(
            "日付",
            required=True,
            format="YYYY-MM-DD",
            help="支出した日付を選択してください",
        ),
        "カテゴリ": st.column_config.SelectboxColumn(
            "カテゴリ",
            required=True,
            options=CATEGORIES,
            help="支出のカテゴリを選択してください",
        ),
        "金額": st.column_config.NumberColumn(
            "金額",
            required=True,
            min_value=1,
            format="¥%d",
            help="1円以上の金額を入力してください",
        ),
        "メモ": st.column_config.TextColumn(
            "メモ",
            max_chars=100,
            help="支出についてのメモを入力してください（100文字以内）",
        ),
    }


# メトリクスの計算
@dataclass
class Metrics:
    total_expenses: int
    remaining_budget: int
    budget_usage_rate: float

def calculate_metrics(expenses_df):
    """支出データからメトリクスを計算"""
    total_expenses = expenses_df["金額"].sum()
    remaining_budget = MONTHLY_BUDGET - total_expenses
    budget_usage_rate = (total_expenses / MONTHLY_BUDGET) * 100

    return Metrics(total_expenses, remaining_budget, budget_usage_rate)

# メイン処理
def main():
    # サイドバーでサンプルデータの読み込み
    st.sidebar.header("設定")
    if st.sidebar.button("サンプルデータを読み込む"):
        st.session_state.expenses_df = create_sample_data()
        st.rerun()

    if st.sidebar.button("データをクリア"):
        if "expenses_df" in st.session_state:
            del st.session_state.expenses_df
        st.rerun()

    # 支出データの初期化
    if "expenses_df" not in st.session_state:
        st.session_state.expenses_df = pd.DataFrame(
            columns=["日付", "カテゴリ", "金額", "メモ"]
        )

    # 支出入力セクション
    st.header("📝 支出入力")
    st.write(
        "表をクリックして支出を入力・編集してください。新しい行を追加するには表の下のセルをクリックします。"
    )

    # データエディターの表示
    edited_df = st.data_editor(
        st.session_state.expenses_df,
        column_config=get_column_config(),
        num_rows="dynamic",
        key="expenses_editor",
        use_container_width=True,
    )

    # 編集されたデータを保存
    st.session_state.expenses_df = edited_df

    # メトリクス表示セクション
    st.header("📊 予算サマリー")

    # メトリクスの計算
    metrics = calculate_metrics(edited_df)

    # メトリクスの表示
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="予算", value=f"¥{MONTHLY_BUDGET:,}", help="月間の予算額")

    with col2:
        # 残高の色を設定（マイナスの場合は赤色）
        delta_color = "normal"
        if metrics.remaining_budget < 0:
            delta_color = "inverse"

        st.metric(
            label="残高",
            value=f"¥{metrics.remaining_budget:,}",
            delta=f"¥{metrics.total_expenses:,}",
            delta_color=delta_color,
            help="予算から支出を引いた残額",
        )

    with col3:
        # 予算消化率の色を設定（80%以上で警告色）
        usage_rate_color = "normal"
        if metrics.budget_usage_rate >= 80:
            usage_rate_color = "off"
        if metrics.budget_usage_rate >= 100:
            usage_rate_color = "inverse"

        st.metric(
            label="予算消化率",
            value=f"{metrics.budget_usage_rate:.1f}%",
            delta_color=usage_rate_color,
            help="予算に対する支出の割合",
        )

    # カテゴリ別集計の表示
    if not edited_df.empty:
        st.header("📈 カテゴリ別集計")

        # カテゴリ別の合計金額を計算
        category_totals = edited_df.groupby("カテゴリ")["金額"].sum().reset_index()
        category_totals = category_totals.rename(columns={"金額": "合計金額"})
        category_totals["合計金額"] = category_totals["合計金額"].apply(
            lambda x: f"¥{x:,}"
        )

        # 集計結果を表示
        st.dataframe(category_totals, use_container_width=True, hide_index=True)

    # 使い方ガイド
    with st.expander("💡 使い方ガイド"):
        st.markdown("""
        ### 基本的な使い方
        
        1. **支出の入力**: 表をクリックして直接入力
        2. **新しい行の追加**: 表の下の空のセルをクリック
        3. **行の削除**: 行を選択してDeleteキーを押す
        
        ### 入力ルール
        
        - **日付**: 必須項目、カレンダーから選択
        - **カテゴリ**: 必須項目、リストから選択
        - **金額**: 必須項目、1円以上の整数
        - **メモ**: 任意項目
        
        ### 表示される情報
        
        - **予算**: 設定された月間予算（20万円）
        - **残高**: 予算から支出を引いた金額
        - **予算消化率**: 予算に対する支出の割合
        """)


if __name__ == "__main__":
    main()
