from pathlib import Path
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="KBO 야구 대시보드",
    page_icon='⚾',
    layout="centered",
)

TARGET_DIR = "data"
TARGET_CSV = "data1.csv"

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / TARGET_DIR / TARGET_CSV

df = pd.read_csv(DATA_PATH)

st.title("KBO 야구 대시보드")

with st.sidebar:

    st.header("조회 조건")

    team = st.selectbox(
        '팀 선택',
        ['전체', 'KT위즈', '삼성라이온즈', 'LG트윈스', 'KIA타이거즈', '두산베어스'])

min_rank = int(df["Rank"].min())
max_rank = int(df["Rank"].max())

rank_range = st.slider(
        "순위 범위",
        min_value=min_rank,
        max_value=max_rank,
        value=(min_rank, max_rank)
    )

filtered = df[
    df["Rank"].between(
        rank_range[0],
        rank_range[1]
    )
].copy()

if team != "전체":

    filtered = filtered[
        filtered["Team"] == team
    ]

total_teams = len(filtered)


if total_teams > 0:

 # 평균 승률
 average_win_rate = filtered["WinRate"].mean()

 # 총 승리 수
 total_wins = filtered["Wins"].sum()

 # 평균 타율
 average_avg = filtered["AVG"].mean()

else:

    average_win_rate = 0
    total_wins = 0
    average_avg = 0

col1, col2, col3, col4 = st.columns(4)

# 1. 조회팀 수
with col1:
    st.metric(
        label='조회팀 수',
        value=f'{total_teams:,}팀',
        border=True,

    )

# 2. 평균 승률
with col2:
    st.metric(
        label='평균 승률',
        value=f'{average_win_rate:.3f}',
        border=True,

    )

# 3. 총 승리
with col3:
    st.metric(
        label='총 승리',
        value=f'{total_wins:,}승',
        border=True,
    )

# 4. 평균 타율
with col4:
    st.metric(
        label='평균 타율',
        value=f'{average_avg:.3f}',
        border=True,
    )

st.divider()
if filtered.empty:
    st.warning('조건에 맞는 팀이 없습니다.')
else:
    left, right = st.columns([2,1])
    with left:
        st.subheader('팀별 승률')

        chart_data = filtered.sort_values(
            "Rank"
        )

        st.bar_chart(
            chart_data,
            x="Team",
            y="WinRate"
        )

    with right:
        st.subheader('구단 데이터')

        st.dataframe(
            filtered,
            hide_index=True,
            column_config={
                'Team': st.column_config.TextColumn(
                    '팀'
                ),

                'Rank': st.column_config.NumberColumn(
                    '순위', format='%d위'
                ),

                'WinRate': st.column_config.NumberColumn(
                    '승률', format='%.3f'
                ),

                'GB': st.column_config.NumberColumn(
                    '게임차', format='%.1f'
                ),

                'AVG': st.column_config.NumberColumn(
                    '타율', format='%.3f'
                )
            }
        )







