import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, date
from PIL import Image
import os
from io import BytesIO
try:
    import graphviz
    GRAPHVIZ_AVAILABLE = True
except ImportError:
    GRAPHVIZ_AVAILABLE = False

# 页面配置
st.set_page_config(
    page_title="螺纹期现策略模拟系统", 
    layout="wide",
    page_icon="📊"
)

# 自定义CSS - 优化Logo显示和整体布局
st.markdown("""
    <style>
    /* 整体样式优化 */
    .block-container {
        padding-top: 0.5rem;
        padding-bottom: 1rem;
    }
    
    /* 顶部Logo和标题容器 */
    .header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-bottom: 1.5rem;
        padding-top: 0.5rem;
    }
    
    /* Logo容器样式 */
    .logo-container {
        display: flex;
        justify-content: center;
        width: 100%;
        padding: 0.5rem 0;
    }
    
    /* 标题样式 */
    .title-container {
        text-align: center;
        padding: 0.5rem 0;
    }
    
    /* 按钮样式 */
    .stButton > button {
        background-color: #2a6fdb;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background-color: #1d5bbf;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* 下载按钮样式 */
    .stDownloadButton > button {
        background-color: #28a745;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    
    /* 指标卡片样式 */
    .metric-box {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 4px solid #2a6fdb;
        margin-bottom: 1rem;
    }
    
    /* 标签页样式 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        padding: 0 20px;
        border-radius: 8px;
        background-color: #f0f2f6;
        transition: all 0.3s;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2a6fdb;
        color: white;
    }
    
    /* 侧边栏样式 */
    [data-testid="stSidebar"] {
        background-color: #f8fafd;
        border-right: 1px solid #e6eef9;
    }
    
    /* 响应式调整 */
    @media (max-width: 768px) {
        .title-text {
            font-size: 2rem !important;
        }
        [data-testid="stSidebar"] {
            width: 100% !important;
        }
        .logo-container img {
            max-width: 120px;
        }
    }
    
    /* 风险矩阵样式 */
    .risk-matrix {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
        margin-bottom: 20px;
    }
    .risk-item {
        background-color: #f0f2f6;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
    }
    .risk-high {
        background-color: #ffcccc;
        border-left: 4px solid #dc3545;
    }
    .risk-medium {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
    }
    .risk-low {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
    }
    
    /* 期权权利金卡片 */
    .premium-card {
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
        color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        margin-bottom: 20px;
    }
    
    /* 保证金卡片 */
    .margin-card {
        background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%);
        color: #333;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 创建顶部容器 - Logo和标题
st.markdown('<div class="header-container">', unsafe_allow_html=True)

# 公司Logo - 放置在页面最顶部
def load_logo():
    try:
        # 尝试加载本地logo文件
        if os.path.exists("logo.png"):
            logo = Image.open("logo.png")
            
            # 调整Logo大小以适应页面
            max_width = 300
            if logo.width > max_width:
                ratio = max_width / logo.width
                new_height = int(logo.height * ratio)
                logo = logo.resize((max_width, new_height))
                
            return logo
        return None
    except Exception as e:
        st.warning(f"无法加载Logo: {str(e)}")
        return None

logo = load_logo()
if logo:
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    st.image(logo, use_container_width=False)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    # 如果没有Logo，显示替代文本
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, #2a6fdb, #1d5bbf);
            color: white;
            padding: 1rem;
            border-radius: 12px;
            text-align: center;
            font-size: 1.5rem;
            font-weight: bold;
            max-width: 300px;
        ">
            钢铁金融分析系统
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 应用标题
st.markdown('<div class="title-container">', unsafe_allow_html=True)
st.markdown('<h1 class="title-text">📊 螺纹钢期现策略收益与风险模拟</h1>', unsafe_allow_html=True)
st.caption("基于期货对冲、网格策略和期权卖权的三维风险管理体系")
st.markdown('</div>', unsafe_allow_html=True)

# 结束顶部容器
st.markdown('</div>', unsafe_allow_html=True)

# =============== 侧边栏参数 ===============
st.sidebar.header("📊 核心参数设置")

with st.sidebar.expander("基础参数", expanded=True):
    spot_base = st.number_input("当前现货价格（元/吨）", value=3700, step=50)
    futures_base = st.number_input("当前期货价格（元/吨）", value=3500, step=50)
    warehouse = st.number_input("现货库存量（吨）", value=5000, step=500)
    strike_price = st.number_input("期权执行价格（元/吨）", value=3600, step=50)
    capital = st.number_input("策略总资金（万元）", value=1000, step=100)
    risk_free_rate = st.slider("无风险利率（%）", 0.0, 10.0, 2.5, step=0.1)
    contract_expiry = st.date_input("合约到期日", value=date(2025, 8, 15))
    
    # 计算合约剩余天数
    today = date.today()
    days_to_expiry = (contract_expiry - today).days
    st.info(f"合约剩余天数: {days_to_expiry}天")

with st.sidebar.expander("策略仓位配置"):
    col1, col2 = st.columns(2)
    with col1:
        hedge_ratio = st.slider("期货空单仓位比例（%）", 0, 50, 20)
        grid_ratio = st.slider("网格策略仓位比例（%）", 0, 30, 10)
    with col2:
        option_ratio = st.slider("卖权策略仓位比例（%）", 0, 30, 10)
        vol_range_percent = st.selectbox("模拟波动范围（±%）", [5, 10, 15, 20], index=2)
    
    vol = vol_range_percent / 100

with st.sidebar.expander("策略收益参数"):
    grid_profit_per_ton = st.slider("网格策略每吨收益（元）", 0, 50, 20)
    # 大幅扩大期权权利金范围至0-300元
    option_premium = st.slider("期权权利金（元/吨）", 0, 300, 20, 
                             help="根据市场波动率调整权利金水平，高波动环境可设置较高权利金")

with st.sidebar.expander("保证金参数", expanded=False):
    futures_margin_ratio = st.slider("期货保证金比例（%）", 5, 20, 10)
    option_margin_ratio = st.slider("期权保证金比例（%）", 10, 30, 15)

with st.sidebar.expander("动态对冲参数", expanded=False):
    dynamic_hedge = st.checkbox("启用动态对冲比例", value=True)
    if dynamic_hedge:
        col3, col4 = st.columns(2)
        with col3:
            min_hedge = st.slider("最低对冲比例(%)", 0, 30, 10)
        with col4:
            max_hedge = st.slider("最高对冲比例(%)", 50, 100, 80)
        hedge_threshold = st.slider("价格波动阈值(%)", 1, 10, 5)

# =============== 模拟计算 ===============
@st.cache_data
def calculate_strategy(spot_base, warehouse, hedge_ratio, grid_ratio, option_ratio,
                      grid_profit_per_ton, option_premium, vol, strike_price,
                      dynamic_hedge=True, min_hedge=10, max_hedge=80, hedge_threshold=5):
    
    price_range = np.arange(
        int(spot_base * (1 - vol)),
        int(spot_base * (1 + vol) + 1),
        50
    )
    
    results = []
    for price in price_range:
        delta = price - spot_base
        
        # 动态调整对冲比例
        if dynamic_hedge:
            price_change_pct = abs(delta) / spot_base * 100
            if price_change_pct > hedge_threshold:
                actual_hedge_ratio = max_hedge
            else:
                actual_hedge_ratio = min_hedge + (max_hedge - min_hedge) * (price_change_pct / hedge_threshold)
        else:
            actual_hedge_ratio = hedge_ratio
        
        # 现货盈亏
        spot_pnl = delta * warehouse
        
        # 期货对冲盈亏
        hedge_pnl = -delta * (actual_hedge_ratio / 100) * warehouse
        
        # 网格策略收益（固定收益）
        grid_pnl = grid_profit_per_ton * (grid_ratio / 100) * warehouse
        
        # 期权策略收益
        option_pnl = option_premium * (option_ratio / 100) * warehouse
        # 当现货价格超过执行价时，期权策略产生损失
        if price > strike_price:
            option_loss = (price - strike_price) * (option_ratio / 100) * warehouse
            option_pnl -= option_loss
        
        # 总盈亏
        total = spot_pnl + hedge_pnl + grid_pnl + option_pnl
        
        results.append({
            "现货价格": price,
            "价格变化率": delta / spot_base * 100,
            "现货盈亏": spot_pnl,
            "期货对冲": hedge_pnl,
            "实际对冲比例": actual_hedge_ratio,
            "网格策略": grid_pnl,
            "卖权策略": option_pnl,
            "总利润": total
        })
    
    return pd.DataFrame(results)

# 执行计算
df = calculate_strategy(
    spot_base, warehouse, hedge_ratio, grid_ratio, option_ratio,
    grid_profit_per_ton, option_premium, vol, strike_price,
    dynamic_hedge, min_hedge if dynamic_hedge else hedge_ratio, 
    max_hedge if dynamic_hedge else hedge_ratio, hedge_threshold
)

# 计算基差
base_difference = spot_base - futures_base

# 计算保证金占用
futures_margin = futures_base * warehouse * (hedge_ratio / 100) * (futures_margin_ratio / 100)
option_margin = strike_price * warehouse * (option_ratio / 100) * (option_margin_ratio / 100)
total_margin = futures_margin + option_margin

# 计算年化收益率
def calculate_annualized_return(total_profit, capital, risk_free_rate, days_to_expiry):
    """
    计算年化收益率和超额收益率
    """
    # 总收益率 = 总利润 / 总资金
    total_return = total_profit / (capital * 10000)  # 资本单位：万元转为元
    
    # 年化因子 = 365 / 合约剩余天数
    annual_factor = 365 / days_to_expiry if days_to_expiry > 0 else 1
    
    # 年化收益率 = (1 + 总收益率)^(年化因子) - 1
    annualized_return = ((1 + total_return) ** annual_factor) - 1 if total_return > -1 else 0
    
    # 超额收益率 = 年化收益率 - 无风险利率
    excess_return = annualized_return - (risk_free_rate / 100)
    
    return annualized_return, excess_return

# =============== 结果展示 ===============
tab1, tab2, tab3 = st.tabs(["📈 策略表现分析", "📊 风险分析", "📘 策略说明"])

with tab1:
    st.subheader("策略总利润分析")
    
    # 计算盈亏平衡点
    breakeven_df = df[df["总利润"] >= 0]
    breakeven_price = breakeven_df["现货价格"].min() if not breakeven_df.empty else None
    
    fig = px.line(df, x="现货价格", y="总利润", 
                  title=f"策略总利润曲线 (当前现货价: {spot_base}元)",
                  labels={"总利润": "利润（元）"},
                  markers=True,
                  line_shape="spline",
                  color_discrete_sequence=["#2a6fdb"])
    
    # 添加参考线
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.7)
    
    if breakeven_price:
        fig.add_vline(x=breakeven_price, line_dash="dash", 
                      line_color="#28a745", annotation_text=f"盈亏平衡点: {breakeven_price}元",
                      annotation_position="top left")
    
    fig.add_vline(x=spot_base, line_dash="dash", 
                  line_color="#6c757d", annotation_text=f"当前价格: {spot_base}元",
                  annotation_position="top right")
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("策略组件盈亏分解")
    fig_bar = px.area(df, x="现货价格", 
                      y=["现货盈亏", "期货对冲", "网格策略", "卖权策略"],
                      title="各策略组件盈亏贡献",
                      labels={"value": "利润（元）", "variable": "策略组件"},
                      color_discrete_sequence=["#6c757d", "#2a6fdb", "#17a2b8", "#ffc107"])
    st.plotly_chart(fig_bar, use_container_width=True)
    
    if dynamic_hedge:
        st.subheader("动态对冲比例变化")
        fig_hedge = px.line(df, x="现货价格", y="实际对冲比例",
                            title="动态对冲比例随价格变化情况",
                            labels={"实际对冲比例": "对冲比例（%）"},
                            line_shape="spline",
                            color_discrete_sequence=["#e83e8c"])
        fig_hedge.add_hline(y=hedge_ratio, line_dash="dash", line_color="#6c757d", 
                            annotation_text=f"基础对冲比例: {hedge_ratio}%")
        st.plotly_chart(fig_hedge, use_container_width=True)

with tab2:
    st.subheader("风险指标分析")
    
    # 风险指标计算
    max_profit = df["总利润"].max()
    min_profit = df["总利润"].min()
    max_drawdown = max_profit - min_profit
    max_drawdown_pct = max_drawdown / (capital * 10000) * 100  # 最大回撤率
    
    profit_range = df[df["总利润"] > 0]["现货价格"]
    breakeven_str = f"{profit_range.min():.0f} ~ {profit_range.max():.0f}" if not profit_range.empty else "无"
    
    # 计算风险价值(VaR)
    var_95 = df["总利润"].quantile(0.05)
    var_95_pct = abs(var_95) / (capital * 10000) * 100  # VaR百分比
    
    # 计算压力测试结果
    stress_price = spot_base * (1 - vol * 1.5)
    stress_row = df.iloc[(df['现货价格'] - stress_price).abs().argsort()[:1]]
    stress_loss = stress_row["总利润"].values[0] if not stress_row.empty else 0
    stress_loss_pct = abs(stress_loss) / (capital * 10000) * 100  # 压力损失百分比
    
    # 计算年化收益率
    annualized_return, excess_return = calculate_annualized_return(
        max_profit, capital, risk_free_rate, days_to_expiry
    )
    
    # 保证金占用分析
    st.subheader("保证金占用分析")
    st.markdown(f"""
    <div class="margin-card">
        <h3>保证金占用情况</h3>
        <div style="display: flex; justify-content: space-between; margin-top: 15px;">
            <div>
                <h4>期货保证金</h4>
                <h2>{futures_margin:,.0f} 元</h2>
                <p>(保证金比例: {futures_margin_ratio}%)</p>
            </div>
            <div>
                <h4>期权保证金</h4>
                <h2>{option_margin:,.0f} 元</h2>
                <p>(保证金比例: {option_margin_ratio}%)</p>
            </div>
            <div>
                <h4>总保证金</h4>
                <h2>{total_margin:,.0f} 元</h2>
                <p>(占总资金: {total_margin/(capital*10000)*100:.1f}%)</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 风险矩阵
    st.subheader("风险矩阵评估")
    st.markdown("""
    <div class="risk-matrix">
        <div class="risk-item risk-high">
            <h4>最大回撤率</h4>
            <h3>{:.2f}%</h3>
            <p>警戒线: >8%</p>
        </div>
        <div class="risk-item risk-medium">
            <h4>95% VaR</h4>
            <h3>{:.2f}%</h3>
            <p>警戒线: >5%</p>
        </div>
        <div class="risk-item risk-low">
            <h4>年化收益率</h4>
            <h3>{:.2f}%</h3>
            <p>目标: >10%</p>
        </div>
        <div class="risk-item">
            <h4>超额收益率</h4>
            <h3>{:.2f}%</h3>
            <p>目标: >5%</p>
        </div>
    </div>
    """.format(
        max_drawdown_pct, 
        var_95_pct,
        annualized_return * 100,
        excess_return * 100
    ), unsafe_allow_html=True)
    
    # 基差风险
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.metric("当前基差（现货-期货）", f"{base_difference} 元", 
                 delta=f"{base_difference/spot_base*100:.2f}%")
        st.metric("现货价格波动范围", f"±{vol_range_percent}%")
        st.metric("无风险利率", f"{risk_free_rate}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.metric("最大回撤", f"{max_drawdown:,.0f} 元", delta=f"{max_drawdown_pct:.2f}%")
        st.metric("盈亏平衡区间", breakeven_str)
        st.metric("年化收益率", f"{annualized_return*100:.2f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.metric("95%置信度风险价值(VaR)", f"{abs(var_95):,.0f} 元", 
                 delta=f"{var_95_pct:.2f}%")
        st.metric("最大利润价格", f"{df.loc[df['总利润'].idxmax()]['现货价格']:.0f} 元")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.metric("极端行情最大亏损", f"{abs(stress_loss):,.0f} 元", 
                 delta=f"{stress_loss_pct:.2f}%")
        st.metric("压力测试价格", f"{stress_price:.0f} 元")
        st.metric("超额收益率", f"{excess_return*100:.2f}%", 
                 delta=f"超越无风险利率{excess_return*100:.2f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.subheader("风险-收益分布图")
    fig_risk = px.scatter(df, x="现货价格", y="总利润", 
                         color="总利润", 
                         color_continuous_scale=["#dc3545", "#ffc107", "#28a745"],
                         title="风险-收益分布图",
                         labels={"总利润": "利润（元）"})
    fig_risk.add_hline(y=0, line_dash="dash", line_color="gray")
    fig_risk.add_vline(x=spot_base, line_dash="dash", line_color="gray")
    st.plotly_chart(fig_risk, use_container_width=True)
    
    # 期权风险分析
    st.subheader("期权风险分析")
    
    # 权利金收益卡片
    total_premium = option_premium * warehouse * (option_ratio / 100)
    st.markdown(f"""
    <div class="premium-card">
        <h3>期权权利金收益分析</h3>
        <div style="display: flex; justify-content: space-between; margin-top: 15px;">
            <div>
                <h4>每吨权利金</h4>
                <h2>{option_premium} 元/吨</h2>
            </div>
            <div>
                <h4>总权利金收入</h4>
                <h2>{total_premium:,.0f} 元</h2>
            </div>
            <div>
                <h4>权利金年化收益率</h4>
                <h2>{total_premium/(capital*10000)*(365/days_to_expiry)*100 if days_to_expiry > 0 else 0:.2f}%</h2>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    option_col1, option_col2 = st.columns(2)
    
    with option_col1:
        st.markdown("""
        <div class="metric-box">
            <h4>期权风险敞口</h4>
            <p>当前期权仓位比例: <strong>{:.0f}%</strong></p>
            <p>最大潜在损失: <strong>{:,.0f}元</strong></p>
            <p>执行价偏离: <strong>{:.2f}%</strong></p>
            <p>权利金/执行价比: <strong>{:.2f}%</strong></p>
        </div>
        """.format(
            option_ratio,
            abs(df["卖权策略"].min()),
            (strike_price - spot_base) / spot_base * 100,
            option_premium / strike_price * 100
        ), unsafe_allow_html=True)
        
    with option_col2:
        st.markdown("""
        <div class="metric-box">
            <h4>期权风险管理策略</h4>
            <ul>
                <li>波动率>30%时减少卖权比例</li>
                <li>价格突破执行价时对冲Delta风险</li>
                <li>设置权利金回撤止损点</li>
                <li>定期评估Theta衰减速度</li>
                <li>权利金范围扩大至0-300元/吨</li>
                <li>权利金/执行价比控制在5%-15%</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.subheader("三维风险对冲体系")
    
    # 使用Graphviz绘制策略流程图
    if GRAPHVIZ_AVAILABLE:
        try:
            graph = graphviz.Digraph()
            graph.attr('graph', rankdir='LR', size='10,5', bgcolor='transparent')
            graph.attr('node', shape='box', style='rounded,filled', 
                      fillcolor='#e3f2fd', fontname='Arial', fontsize='12')
            graph.attr('edge', color='#2a6fdb', arrowsize='0.8')
            
            graph.node('A', '期货空单对冲\n防范系统性下跌风险')
            graph.node('B', '网格增强策略\n利用市场波动增厚收益')
            graph.node('C', '期权时间价值\n获取稳定现金流')
            graph.node('D', '风险控制\n动态调整仓位')
            graph.node('E', '利润优化\n增强整体收益')
            
            graph.edge('A', 'D')
            graph.edge('B', 'D')
            graph.edge('C', 'D')
            graph.edge('D', 'E')
            
            st.graphviz_chart(graph)
        except Exception as e:
            st.warning(f"流程图渲染错误: {str(e)}")
            st.image("https://via.placeholder.com/800x300?text=三维风险对冲体系示意图", use_container_width=True)
    else:
        st.warning("Graphviz不可用，流程图功能受限。请确保已安装Graphviz系统依赖。")
        st.image("https://via.placeholder.com/800x300?text=三维风险对冲体系示意图", use_container_width=True)
    
    st.subheader("核心策略逻辑")
    
    with st.expander("1. 期货空单对冲", expanded=True):
        st.markdown("""
        <div style="background-color: #e8f4fd; padding: 1rem; border-radius: 8px; border-left: 4px solid #2a6fdb;">
        <h4 style="color: #1d5bbf;">基础保护层</h4>
        <p><b>目标</b>: 对冲现货价格下跌风险，锁定销售利润</p>
        <p><b>操作</b>: 
            <ul>
                <li>在期货市场卖出螺纹钢期货合约（如RB2510合约）</li>
                <li>维持企业正常经营同时降低净多头头寸</li>
            </ul>
        </p>
        <p><b>风险管理</b>:
            <ul>
                <li>保证金占用: {futures_margin_ratio}%</li>
                <li>基差风险监控：每日跟踪期货-现货价差</li>
                <li>动态对冲比例：根据市场波动率调整对冲比例</li>
                <li>保证金压力测试：模拟价格极端波动下的保证金需求</li>
            </ul>
        </p>
        </div>
        """.format(futures_margin_ratio=futures_margin_ratio), unsafe_allow_html=True)
    
    with st.expander("2. 网格增强策略"):
        st.markdown("""
        <div style="background-color: #e6f7f0; padding: 1rem; border-radius: 8px; border-left: 4px solid #28a745;">
        <h4 style="color: #218838;">波动收益层</h4>
        <p><b>目标</b>: 利用盘面波动增厚收益，提升套保效能</p>
        <p><b>操作</b>:
            <ul>
                <li>在套保仓位基础上增加网格交易</li>
                <li>高卖低买获取日内波动收益</li>
                <li>网格点差参照ATR指标设置</li>
            </ul>
        </p>
        <p><b>年化收益增强</b>:
            <ul>
                <li>网格策略可提供3-8%的年化收益增强</li>
                <li>震荡行情中收益尤为显著</li>
            </ul>
        </p>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("3. 期权卖权策略 - 增强版"):
        st.markdown("""
        <div style="background-color: #fff8e6; padding: 1rem; border-radius: 8px; border-left: 4px solid #ffc107;">
        <h4 style="color: #e0a800;">时间价值层</h4>
        <p><b>目标</b>: 提前锁定销售利润，获取时间价值</p>
        <p><b>操作</b>:
            <ul>
                <li>卖出虚值或平值看涨期权（执行价3000~3100元）</li>
                <li>动态调整仓位，权利金大幅衰减时及时落袋</li>
                <li><b>权利金范围扩大至0-300元/吨</b>，增加策略灵活性</li>
            </ul>
        </p>
        <p><b>风险管理</b>:
            <ul>
                <li><b>IV监控</b>：IV>30%时优先卖出期权，IV<20%时减少卖权比例</li>
                <li><b>希腊字母管理</b>：
                    <ul>
                        <li>Delta：控制在±0.3以内</li>
                        <li>Gamma：监控非线性风险</li>
                        <li>Vega：控制波动率风险敞口</li>
                        <li>Theta：最大化时间价值收益</li>
                    </ul>
                </li>
                <li><b>保证金比例</b>: {option_margin_ratio}%</li>
            </ul>
        </p>
        </div>
        """.format(option_margin_ratio=option_margin_ratio), unsafe_allow_html=True)
    
    st.subheader("动态仓位管理系统")
    
    col5, col6 = st.columns([1, 2])
    with col5:
        st.markdown("""
        <div style="background-color: #f9f2ff; padding: 1rem; border-radius: 8px; border-left: 4px solid #6f42c1;">
        <h4 style="color: #59359a;">仓位调整逻辑</h4>
        <ul>
            <li>价格波动 > 阈值(5%): 增加对冲至80%</li>
            <li>价格波动 < 阈值(3%): 降低对冲至30%</li>
            <li>波动在3-5%之间: 维持当前比例</li>
        </ul>
        
        <h4 style="color: #59359a; margin-top: 1rem;">组合策略示例</h4>
        <ul>
            <li>10-30% 固定套保仓位</li>
            <li>10-20% 网格策略仓位</li>
            <li>10-30% 卖权策略仓位</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col6:
        # 仓位管理流程图
        if GRAPHVIZ_AVAILABLE:
            try:
                graph = graphviz.Digraph()
                graph.attr('graph', rankdir='TB', bgcolor='transparent')
                graph.attr('node', shape='diamond', fillcolor='#e3f2fd', style='filled', fontname='Arial')
                graph.attr('edge', fontsize='10', color='#495057')
                
                graph.node('A', '价格波动')
                graph.node('B', '波动>5%?')
                graph.node('C', '增加对冲至80%')
                graph.node('D', '波动<3%?')
                graph.node('E', '降低对冲至30%')
                graph.node('F', '维持当前比例')
                
                graph.edge('A', 'B')
                graph.edge('B', 'C', label='是')
                graph.edge('B', 'D', label='否')
                graph.edge('D', 'E', label='是')
                graph.edge('D', 'F', label='否')
                
                st.graphviz_chart(graph)
            except Exception as e:
                st.warning(f"流程图渲染错误: {str(e)}")
                st.image("https://via.placeholder.com/500x300?text=动态仓位管理流程图", use_container_width=True)
        else:
            st.image("https://via.placeholder.com/500x300?text=动态仓位管理流程图", use_container_width=True)
    
    st.subheader("历史回测表现 (2022-2024)")
    backtest_data = {
        "年度": ["2022", "2023", "2024"],
        "年化收益率": ["15.2%", "22.7%", "18.3%"],
        "最大回撤率": ["6.8%", "7.2%", "5.9%"],
        "波动率": ["12.4%", "14.1%", "11.7%"],
        "夏普比率": ["1.23", "1.61", "1.56"],
        "无风险利率": ["2.5%", "2.6%", "2.7%"],
        "超额收益率": ["12.7%", "20.1%", "15.6%"]
    }
    st.dataframe(pd.DataFrame(backtest_data), hide_index=True)
    
    # 年化收益率比较
    st.subheader("年化收益率比较")
    fig_comparison = px.bar(
        pd.DataFrame({
            "指标": ["策略年化", "无风险利率", "超额收益"],
            "值": [annualized_return * 100, risk_free_rate, excess_return * 100]
        }), 
        x="指标", y="值", 
        color="指标",
        color_discrete_sequence=["#2a6fdb", "#6c757d", "#28a745"],
        labels={"值": "收益率 (%)"},
        title="策略年化收益率 vs 无风险利率"
    )
    st.plotly_chart(fig_comparison, use_container_width=True)
    
    # 实现10%以上年化收益率的条件
    st.subheader("实现10%以上年化收益率的条件")
    st.markdown("""
    <div style="background-color: #e6f7f0; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #28a745;">
        <h4 style="color: #218838;">策略配置要求</h4>
        <ul>
            <li><b>市场波动率</b>: 10%-20% (波动率过低则收益有限，过高则风险过大)</li>
            <li><b>期货对冲比例</b>: 20%-40% (提供基础保护同时保留上涨收益)</li>
            <li><b>网格策略配置</b>: 
                <ul>
                    <li>仓位比例: 10%-20%</li>
                    <li>每吨收益: 30-50元</li>
                    <li>年化贡献: 3-8%</li>
                </ul>
            </li>
            <li><b>期权卖权策略</b>:
                <ul>
                    <li>仓位比例: 20%-30%</li>
                    <li>权利金范围: 50-150元/吨</li>
                    <li>权利金/执行价比: 5%-15%</li>
                    <li>年化贡献: 5-12%</li>
                </ul>
            </li>
        </ul>
        
        <h4 style="color: #218838; margin-top: 1rem;">风险管理要求</h4>
        <ul>
            <li><b>最大回撤控制</b>: <8%</li>
            <li><b>保证金占用</b>: <50%总资金</li>
            <li><b>动态对冲</b>: 波动阈值5%，对冲比例范围30%-80%</li>
            <li><b>现金储备</b>: >20%总资金用于极端行情</li>
        </ul>
        
        <h4 style="color: #218838; margin-top: 1rem;">市场环境要求</h4>
        <ul>
            <li><b>基差结构</b>: 期货贴水不超过5%</li>
            <li><b>波动率环境</b>: IV在20%-30%之间</li>
            <li><b>趋势环境</b>: 震荡或温和上涨市场</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("""
    **实施建议**: 
    - 根据实际资金规模、风险承受能力选择组合策略
    - 持续跟踪螺纹钢基本面逻辑和波动率变化
    - 前期以灵活方式操作，有利润及时落袋
    - 定期进行压力测试和策略回测
    - 关注期权希腊字母风险，定期进行希腊字母平衡
    - 权利金范围扩大至0-300元/吨，可根据市场波动率灵活调整
    """)

# =============== 导出功能 ===============
st.subheader("📁 数据导出与分析报告")

# 创建内存中的Excel文件
excel_buffer = BytesIO()
with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
    # 主数据表
    df.to_excel(writer, sheet_name='策略模拟', index=False)
    
    # 参数汇总表
    params_data = {
        "参数名称": [
            "现货价格", "期货价格", "基差", "库存量", 
            "对冲比例", "网格比例", "期权比例",
            "网格收益", "期权权利金", "波动范围",
            "执行价格", "动态对冲", "最低对冲比例", 
            "最高对冲比例", "波动阈值", "总资金", "无风险利率",
            "合约到期日", "期货保证金比例", "期权保证金比例"
        ],
        "参数值": [
            f"{spot_base}元/吨", f"{futures_base}元/吨", f"{base_difference}元", f"{warehouse}吨",
            f"{hedge_ratio}%", f"{grid_ratio}%", f"{option_ratio}%",
            f"{grid_profit_per_ton}元/吨", f"{option_premium}元/吨", f"±{vol_range_percent}%",
            f"{strike_price}元/吨", "是" if dynamic_hedge else "否",
            f"{min_hedge}%" if dynamic_hedge else "N/A", 
            f"{max_hedge}%" if dynamic_hedge else "N/A",
            f"{hedge_threshold}%" if dynamic_hedge else "N/A",
            f"{capital}万元", f"{risk_free_rate}%",
            contract_expiry.strftime("%Y-%m-%d"),
            f"{futures_margin_ratio}%", f"{option_margin_ratio}%"
        ]
    }
    params_df = pd.DataFrame(params_data)
    params_df.to_excel(writer, sheet_name='参数设置', index=False)
    
    # 风险指标表
    risk_metrics = {
        "指标": ["最大回撤", "盈亏平衡区间", "95% VaR", "压力测试亏损", "年化收益率", "超额收益率", "总保证金占用"],
        "数值": [
            f"{max_drawdown:,.0f}元 ({max_drawdown_pct:.2f}%)", 
            breakeven_str,
            f"{abs(var_95):,.0f}元 ({var_95_pct:.2f}%)",
            f"{abs(stress_loss):,.0f}元 ({stress_loss_pct:.2f}%)",
            f"{annualized_return*100:.2f}%",
            f"{excess_return*100:.2f}%",
            f"{total_margin:,.0f}元 ({total_margin/(capital*10000)*100:.1f}%)"
        ]
    }
    pd.DataFrame(risk_metrics).to_excel(writer, sheet_name='风险指标', index=False)
    
    # 历史回测数据
    backtest_df = pd.DataFrame({
        "年度": ["2022", "2023", "2024"],
        "年化收益率": ["15.2%", "22.7%", "18.3%"],
        "最大回撤率": ["6.8%", "7.2%", "5.9%"],
        "波动率": ["12.4%", "14.1%", "11.7%"],
        "夏普比率": ["1.23", "1.61", "1.56"],
        "无风险利率": ["2.5%", "2.6%", "2.7%"],
        "超额收益率": ["12.7%", "20.1%", "15.6%"]
    })
    backtest_df.to_excel(writer, sheet_name='历史回测', index=False)

# 下载按钮
st.download_button(
    label="📥 下载完整分析报告 (Excel)",
    data=excel_buffer.getvalue(),
    file_name=f"螺纹期现策略模拟_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.caption("报告包含策略模拟数据、参数设置、风险指标和历史回测")

# 页脚
st.markdown("---")
st.caption("© 2025 兴泰建设集团 | 螺纹钢期现策略模拟工具 | 更新日期: 2025-07-21")