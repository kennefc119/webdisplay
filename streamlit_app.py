import pandas as pd
from pathlib import Path
import streamlit as st
from datetime import datetime
import time

st.image("graphics/banner.jpg", use_container_width=True)

st.markdown("""
<div style='text-align: center;'>
    <h1 style='font-size:36px;'>❤️ Kandz代購 Secret Promotion Site❤️</h1>
    <h4 style='font-size:24px;'>For exclusive Hong Kong clients only!!!</h4>
</div>
""", unsafe_allow_html=True)

st.markdown("""
Kandz 已經踏入第9年，一直為大家努力搜羅全球不同嘅名牌手袋、首飾及服裝，致力將最優質嘅時尚單品帶到您嘅身邊。我們專注於代購服務，確保每一件商品都經過嚴格把關，讓您足不出戶即可擁有心儀嘅國際精品。

憑藉多年嘅經驗與專業團隊，我們承諾貨品一般兩星期內到貨，讓您享受快速又安心嘅購物體驗。無論係經典款手袋、限量版首飾，還是潮流服飾，Kandz 都致力為您提供最優惠嘅價格與最貼心嘅服務。選擇 Kandz，讓您嘅時尚之旅更加輕鬆、便捷，盡顯獨特品味與魅力。

""")
df = pd.read_excel("excel/products.xlsx")
now = datetime.now()
base_image_url = "https://kandz.streamlit.app/images/"

###################################################################################################

valid_offers = df[df['expiry_date'].apply(lambda x: datetime.strptime(str(x), "%Y%m%d")) > now]
st.markdown(f"### 🎁 今日 Secret Promotion Offer 數量：<span style='color:red; font-weight:bold;'>{len(valid_offers)}</span>", unsafe_allow_html=True)
cols = st.columns(3)

###################################################################################################
for idx, row in df.iterrows():
    expiry_date = datetime.strptime(str(row['expiry_date']), "%Y%m%d")
    expiry_datetime = datetime.combine(expiry_date.date(), datetime.min.time())
    if expiry_datetime > now:
        remaining = expiry_datetime - now
        total_seconds = int(remaining.total_seconds())
        days = total_seconds // 86400
        hours = (total_seconds % 86400) // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        col = cols[idx % 3]
        with col:
            
            image_filename = str(row['image_filename'])
            image_path = Path("images") / (image_filename + ".jpeg")
            pay_url = row['payment_url']
            if not pay_url.startswith("http"):
                pay_url = "https://" + pay_url
            st.image(image_path, use_container_width=True)
            st.markdown(f"**{row['name']}**")
            st.caption(row['description'])
            st.markdown(f"⏳ Promotion expires in<br><b>{days} D {hours} Hr {minutes} min {seconds} sec</b>", unsafe_allow_html=True)

            message = f"你好，我想查詢 {row['name']} 幾錢?"
            whatsapp_url = f"https://wa.me/447418333672?text={message}"
            ask_button = f"<a href='{whatsapp_url}' target='_blank' style='display:inline-block; margin-right:10px;'><button style='background-color:#e0e0e0;color:black;padding:8px 16px;border:none;border-radius:5px;font-size:16px;'>Ask</button></a>"
            pay_button = f"""<a href="{pay_url}" target="_blank" rel="noopener noreferrer" style="display:inline-block;">
                <button style="background-color:#FFA500;color:white;padding:8px 16px;border:none;border-radius:5px;font-size:16px;cursor:pointer;">
                    Pay
                </button>
            </a>"""            
            st.markdown(ask_button + pay_button, unsafe_allow_html=True)