import os

from datetime import datetime

import pandas as pd

import streamlit as st

# Thư viện tạo PDF

from reportlab.lib.pagesizes import mm

from reportlab.pdfgen import canvas

from reportlab.pdfbase import pdfmetrics

from reportlab.pdfbase.ttfonts import TTFont

# ============================================================

# CẤU HÌNH TRANG

# ============================================================

st.set_page_config(

    page_title="Order Nhà Hàng - Mr. Út Cưng",

    layout="wide"

)

# Logo

if os.path.exists("0F8389B5-950C-4E02-9293-460BEA0D62E0.png"):

    st.image(

        "0F8389B5-950C-4E02-9293-460BEA0D62E0.png",

        width=180

    )

# ============================================================

# ĐƯỜNG DẪN DỮ LIỆU

# ============================================================

CSV_FILE = "history.csv"

# Thư mục lưu hóa đơn

BILL_FOLDER = "bills"

os.makedirs(BILL_FOLDER, exist_ok=True)

# ============================================================

# THỰC ĐƠN

# ============================================================

menu = {

    "Đồ ăn": {

        "Pizza Hải Sản": 150000,

        "Pizza cá": 500000,

        "Mì Ý Bò Bằm": 95000,

        "Burger Gà": 35000,

        "Salad Trộn": 50000,

        "Bít tết Bò Mỹ": 250000,

        "Sườn nướng BBQ": 180000,

        "Cánh gà chiên mắm": 75000,

        "Lẩu cá diêu hồng": 200000,

        "Lẩu Thái hải sản": 300000,

        "Lẩu Cá Đuối": 290000,

    },

    "Thức uống": {

        "Coca Cola": 20000,

        "Trà sữa SV": 70000,

        "Trà Đào Cam Sả": 35000,

        "Cà Phê Sữa": 25000,

        "Nước Suối": 10000,

        "Sinh tố Bơ": 45000,

        "Nước ép cam": 40000,

        "Mojito chanh dây": 55000,

        "Bia Heineken": 30000,

        "Bia Tiger bạc": 22000,

    },

}

# ============================================================

# FONT TIẾNG VIỆT CHO BILL

# ============================================================

FONT_NAME = "Helvetica"

FONT_PATH = "DejaVuSans.ttf"

if os.path.exists(FONT_PATH):

    try:

        pdfmetrics.registerFont(

            TTFont("DejaVu", FONT_PATH)

        )

        FONT_NAME = "DejaVu"

    except Exception:

        FONT_NAME = "Helvetica"

# ============================================================

# HÀM TẠO BILL PDF

# ============================================================

def tao_bill(

    order_dict,

    table_number,

    tam_tinh,

    giam_gia,

    tong_thanh_toan

):

    now = datetime.now()

    # Tên file bill

    bill_name = (

        f"bill_{now.strftime('%Y%m%d_%H%M%S')}.pdf"

    )

    bill_path = os.path.join(

        BILL_FOLDER,

        bill_name

    )

    # Khổ giấy máy in bill 80mm

    width = 80 * mm

    # Chiều cao tùy theo số món

    height = (

        115 + len(order_dict) * 17

    ) * mm

    # Tạo PDF

    c = canvas.Canvas(

        bill_path,

        pagesize=(width, height)

    )

    y = height - 10 * mm

    # ========================================================

    # TIÊU ĐỀ

    # ========================================================

    c.setFont(

        FONT_NAME,

        13

    )

    c.drawCentredString(

        width / 2,

        y,

        "NHA HANG MR. UT CUNG"

    )

    y -= 6 * mm

    c.setFont(

        FONT_NAME,

        8

    )

    c.drawCentredString(

        width / 2,

        y,

        "HOA DON THANH TOAN"

    )

    y -= 5 * mm

    c.line(

        5 * mm,

        y,

        width - 5 * mm,

        y

    )

    y -= 6 * mm

    # ========================================================

    # THÔNG TIN HÓA ĐƠN

    # ========================================================

    c.setFont(

        FONT_NAME,

        8

    )

    c.drawString(

        5 * mm,

        y,

        f"Ban: {table_number}"

    )

    y -= 5 * mm

    c.drawString(

        5 * mm,

        y,

        f"Ngay: {now.strftime('%d/%m/%Y')}"

    )

    y -= 5 * mm

    c.drawString(

        5 * mm,

        y,

        f"Gio: {now.strftime('%H:%M:%S')}"

    )

    y -= 6 * mm

    c.line(

        5 * mm,

        y,

        width - 5 * mm,

        y

    )

    y -= 5 * mm

    # ========================================================

    # DANH SÁCH MÓN

    # ========================================================

    for row in order_dict.values():

        ten_mon = row["Tên món"]

        so_luong = row["Số lượng"]

        don_gia = row["Đơn giá"]

        thanh_tien = row["Thành tiền"]

        c.setFont(

            FONT_NAME,

            8

        )

        # Tên món

        if len(ten_mon) > 28:

            c.drawString(

                5 * mm,

                y,

                ten_mon[:28]

            )

            y -= 4 * mm

        else:

            c.drawString(

                5 * mm,

                y,

                ten_mon

            )

            y -= 4 * mm

        # Số lượng x đơn giá

        c.drawString(

            5 * mm,

            y,

            f"{so_luong} x {don_gia:,.0f}"

        )

        # Thành tiền

        c.drawRightString(

            width - 5 * mm,

            y,

            f"{thanh_tien:,.0f}"

        )

        y -= 7 * mm

    # ========================================================

    # TỔNG TIỀN

    # ========================================================

    c.line(

        5 * mm,

        y,

        width - 5 * mm,

        y

    )

    y -= 6 * mm

    c.setFont(

        FONT_NAME,

        8

    )

    c.drawString(

        5 * mm,

        y,

        "Tam tinh:"

    )

    c.drawRightString(

        width - 5 * mm,

        y,

        f"{tam_tinh:,.0f} VND"

    )

    # Giảm giá

    if giam_gia > 0:

        y -= 5 * mm

        c.drawString(

            5 * mm,

            y,

            "Giam gia 5%:"

        )

        c.drawRightString(

            width - 5 * mm,

            y,

            f"-{giam_gia:,.0f} VND"

        )

    # Tổng thanh toán

    y -= 8 * mm

    c.setFont(

        FONT_NAME,

        10

    )

    c.drawString(

        5 * mm,

        y,

        "TONG THANH TOAN:"

    )

    c.drawRightString(

        width - 5 * mm,

        y,

        f"{tong_thanh_toan:,.0f} VND"

    )

    # ========================================================

    # LỜI CẢM ƠN

    # ========================================================

    y -= 10 * mm

    c.setFont(

        FONT_NAME,

        8

    )

    c.drawCentredString(

        width / 2,

        y,

        "Cam on quy khach!"

    )

    y -= 5 * mm

    c.drawCentredString(

        width / 2,

        y,

        "Hen gap lai quy khach."

    )

    # Lưu PDF

    c.save()

    return bill_path

# ============================================================

# SESSION STATE

# ============================================================

if "order_dict" not in st.session_state:

    st.session_state.order_dict = {}

if "history" not in st.session_state:

    if os.path.exists(CSV_FILE):

        try:

            df_loaded = pd.read_csv(

                CSV_FILE

            )

            st.session_state.history = (

                df_loaded.to_dict(

                    orient="records"

                )

            )

        except Exception:

            st.session_state.history = []

    else:

        st.session_state.history = []

if "admin_logged_in" not in st.session_state:

    st.session_state.admin_logged_in = False

# Bill vừa tạo

if "last_bill" not in st.session_state:

    st.session_state.last_bill = None

# ============================================================

# THANH ĐIỀU HƯỚNG

# ============================================================

page = st.sidebar.radio(

    "📋 Chọn trang hệ thống",

    [

        "🍽️ Order",

        "🔑 Admin"

    ]

)

# ============================================================

# TRANG ORDER

# ============================================================

if page == "🍽️ Order":

    st.title(

        "🍽️ Hệ thống Order Nhà Hàng_Mr. Út Cưng"

    )

    st.caption(

        "Ghi nhận order nhanh chóng và chính xác theo thời gian thực"

    )

    col1, col2 = st.columns(

        [1, 1.3]

    )

    # ========================================================

    # CỘT CHỌN MÓN

    # ========================================================

    with col1:

        st.subheader(

            "🍽️ Chọn Món"

        )

        table_number = st.selectbox(

            "🪑 Chọn số bàn",

            [

                f"Bàn {i}"

                for i in range(1, 21)

            ]

        )

        category = st.selectbox(

            "Chọn loại:",

            list(menu.keys())

        )

        item = st.selectbox(

            "Chọn món:",

            list(menu[category].keys())

        )

        quantity = st.number_input(

            "Số lượng:",

            min_value=1,

            step=1,

            value=1

        )

        # ====================================================

        # THÊM VÀO GIỎ

        # ====================================================

        if st.button(

            "➕ Thêm vào giỏ",

            use_container_width=True

        ):

            price = menu[category][item]

            if item in st.session_state.order_dict:

                st.session_state.order_dict[item][

                    "Số lượng"

                ] += quantity

                st.session_state.order_dict[item][

                    "Thành tiền"

                ] = (

                    st.session_state.order_dict[item][

                        "Số lượng"

                    ] * price

                )

                st.session_state.order_dict[item][

                    "Bàn"

                ] = table_number

            else:

                st.session_state.order_dict[item] = {

                    "Bàn": table_number,

                    "Tên món": item,

                    "Đơn giá": price,

                    "Số lượng": quantity,

                    "Thành tiền":

                        price * quantity,

                }

            st.success(

                f"Đã thêm {item} vào giỏ!"

            )

            st.rerun()

    # ========================================================

    # CỘT GIỎ HÀNG

    # ========================================================

    with col2:

        st.subheader(

            "🛒 Giỏ hàng hiện tại"

        )

        if st.session_state.order_dict:

            df = pd.DataFrame.from_dict(

                st.session_state.order_dict,

                orient="index"

            )

            st.dataframe(

                df[

                    [

                        "Bàn",

                        "Tên món",

                        "Đơn giá",

                        "Số lượng",

                        "Thành tiền"

                    ]

                ],

                use_container_width=True,

                hide_index=True

            )

            # =================================================

            # TÍNH TIỀN

            # =================================================

            tam_tinh = df[

                "Thành tiền"

            ].sum()

            # Giảm 5% nếu trên 1 triệu

            giam_gia = (

                tam_tinh * 0.05

                if tam_tinh > 1000000

                else 0

            )

            tong_thanh_toan = (

                tam_tinh - giam_gia

            )

            st.write(

                f"**Tạm tính:** "

                f"{tam_tinh:,.0f} VNĐ"

            )

            if giam_gia > 0:

                st.write(

                    f"**Giảm giá 5% (> 1M):** "

                    f"-{giam_gia:,.0f} VNĐ"

                )

            st.metric(

                "💰 Tổng thanh toán",

                f"{tong_thanh_toan:,.0f} VNĐ"

            )

            col_btn1, col_btn2 = st.columns(2)

            # =================================================

            # THANH TOÁN

            # =================================================

            with col_btn1:

                if st.button(

                    "💳 Thanh toán",

                    use_container_width=True

                ):

                    now_str = datetime.now().strftime(

                        "%Y-%m-%d %H:%M:%S"

                    )

                    # =========================================

                    # TẠO BILL

                    # =========================================

                    bill_path = tao_bill(

                        st.session_state.order_dict,

                        table_number,

                        tam_tinh,

                        giam_gia,

                        tong_thanh_toan

                    )

                    # =========================================

                    # LƯU LỊCH SỬ

                    # =========================================

                    for row in (

                        st.session_state

                        .order_dict

                        .values()

                    ):

                        st.session_state.history.append(

                            {

                                "Thời gian":

                                    now_str,

                                "Bàn":

                                    row["Bàn"],

                                "Tên món":

                                    row["Tên món"],

                                "Số lượng":

                                    row["Số lượng"],

                                "Thành tiền":

                                    row["Thành tiền"],

                            }

                        )

                    # =========================================

                    # LƯU CSV

                    # =========================================

                    try:

                        df_history = pd.DataFrame(

                            st.session_state.history

                        )

                        df_history.to_csv(

                            CSV_FILE,

                            index=False,

                            encoding="utf-8-sig"

                        )

                    except Exception as e:

                        st.error(

                            f"Lỗi ghi dữ liệu: {e}"

                        )

                    # =========================================

                    # LƯU BILL VỪA TẠO

                    # =========================================

                    st.session_state.last_bill = (

                        bill_path

                    )

                    # Xóa giỏ

                    st.session_state.order_dict = {}

                    st.success(

                        "✅ Thanh toán thành công!"

                    )

                    st.info(

                        "🧾 Bill đã được tạo. "

                        "Bạn có thể tải xuống và in ngay bên dưới."

                    )

            # =================================================

            # XÓA GIỎ

            # =================================================

            with col_btn2:

                if st.button(

                    "🗑️ Xóa toàn bộ giỏ",

                    use_container_width=True

                ):

                    st.session_state.order_dict = {}

                    st.rerun()

        else:

            st.info(

                "🛒 Giỏ hàng đang trống. "

                "Hãy chọn món bên trái để lên đơn."

            )

    # ========================================================

    # BILL VỪA THANH TOÁN

    # ========================================================

    if st.session_state.last_bill:

        bill_path = (

            st.session_state.last_bill

        )

        if os.path.exists(bill_path):

            st.markdown("---")

            st.subheader(

                "🧾 HÓA ĐƠN VỪA THANH TOÁN"

            )

            st.success(

                f"Bill: {os.path.basename(bill_path)}"

            )

            # Đọc file PDF

            with open(

                bill_path,

                "rb"

            ) as f:

                bill_data = f.read()

            # Nút tải / in

            st.download_button(

                label="🖨️ TẢI BILL ĐỂ IN",

                data=bill_data,

                file_name=os.path.basename(

                    bill_path

                ),

                mime="application/pdf",

                use_container_width=True

            )

            st.caption(

                "Sau khi tải bill PDF, mở file và chọn "

                "Print/In để in ra máy in bill."

            )

# ============================================================

# TRANG ADMIN

# ============================================================

elif page == "🔑 Admin":

    st.title(

        "🔑 Trang Quản Trị & Phân Tích Doanh Thu"

    )

    # ========================================================

    # ĐĂNG NHẬP

    # ========================================================

    if not st.session_state.admin_logged_in:

        with st.form(

            "admin_login_form"

        ):

            password = st.text_input(

                "Nhập mật khẩu quản trị",

                type="password"

            )

            login_submitted = (

                st.form_submit_button(

                    "🔑 Đăng nhập"

                )

            )

            if login_submitted:

                if password == "123456":

                    st.session_state.admin_logged_in = True

                    st.success(

                        "Đăng nhập thành công!"

                    )

                    st.rerun()

                else:

                    st.error(

                        "Mật khẩu không chính xác!"

                    )

        st.warning(

            "Vui lòng nhập mật khẩu và bấm đăng nhập "

            "để xem dữ liệu kinh doanh."

        )

        st.stop()

    # ========================================================

    # ADMIN ĐÃ ĐĂNG NHẬP

    # ========================================================

    col_header_title, col_header_btn = st.columns(

        [4, 1]

    )

    with col_header_title:

        st.success(

            "Xác thực quyền Quản trị viên thành công!"

        )

    with col_header_btn:

        if st.button(

            "🔒 Đăng xuất"

        ):

            st.session_state.admin_logged_in = False

            st.rerun()

    # ========================================================

    # TABS ADMIN

    # ========================================================

    tab1, tab2, tab3 = st.tabs(

        [

            "📋 Danh sách thực đơn",

            "💰 Doanh thu & Nhật ký giao dịch",

            "📊 Thống kê & Phân tích bán hàng REAL-TIME"

        ]

    )

    # ========================================================

    # TAB 1 - MENU

    # ========================================================

    with tab1:

        st.subheader(

            "Menu hiện hành của nhà hàng"

        )

        data = []

        for category in menu:

            for item, price in menu[category].items():

                data.append(

                    [

                        category,

                        item,

                        price

                    ]

                )

        df_menu = pd.DataFrame(

            data,

            columns=[

                "Phân loại",

                "Tên món",

                "Đơn giá (VNĐ)"

            ]

        )

        st.dataframe(

            df_menu,

            use_container_width=True,

            hide_index=True

        )

    # ========================================================

    # TAB 2 - DOANH THU

    # ========================================================

    with tab2:

        st.subheader(

            "💰 Doanh thu & Hóa đơn thực tế"

        )

        if os.path.exists(CSV_FILE):

            try:

                df_history = pd.read_csv(

                    CSV_FILE

                )

            except Exception:

                df_history = pd.DataFrame()

        else:

            df_history = pd.DataFrame()

        if not df_history.empty:

            # Tổng doanh thu

            tong_doanh_thu = (

                df_history["Thành tiền"].sum()

            )

            col_met1, col_met2 = st.columns(2)

            col_met1.metric(

                "💰 Tổng doanh thu tích lũy",

                f"{tong_doanh_thu:,.0f} VNĐ"

            )

            col_met2.metric(

                "🍽️ Số lượng món đã phục vụ",

                f"{df_history['Số lượng'].sum()} phần"

            )

            st.markdown("---")

            # =================================================

            # DOANH THU THEO NGÀY

            # =================================================

            st.subheader(

                "📅 Thống kê doanh thu theo Ngày"

            )

            df_history["Ngày"] = pd.to_datetime(

                df_history["Thời gian"]

            ).dt.date

            df_daily_revenue = (

                df_history

                .groupby("Ngày")["Thành tiền"]

                .sum()

                .reset_index()

            )

            df_daily_revenue.columns = [

                "Ngày",

                "Doanh thu (VNĐ)"

            ]

            col_chart_day, col_table_day = st.columns(

                [1.5, 1]

            )

            with col_chart_day:

                st.write(

                    "**📊 Biểu đồ doanh thu hàng ngày:**"

                )

                st.bar_chart(

                    df_daily_revenue

                    .set_index("Ngày")

                    ["Doanh thu (VNĐ)"]

                )

            with col_table_day:

                st.write(

                    "**📋 Bảng kê doanh thu theo ngày:**"

                )

                st.dataframe(

                    df_daily_revenue,

                    use_container_width=True,

                    hide_index=True

                )

            st.markdown("---")

            # =================================================

            # LỊCH SỬ THANH TOÁN

            # =================================================

            st.subheader(

                "🧾 Chi tiết lịch sử thanh toán"

            )

            st.dataframe(

                df_history[

                    [

                        "Thời gian",

                        "Bàn",

                        "Tên món",

                        "Số lượng",

                        "Thành tiền"

                    ]

                ],

                use_container_width=True,

                hide_index=True

            )

        else:

            st.info(

                "Hệ thống chưa ghi nhận giao dịch thanh toán nào."

            )

    # ========================================================

    # TAB 3 - PHÂN TÍCH

    # ========================================================

    with tab3:

        st.subheader(

            "📊 Phân tích số liệu và Khung giờ vàng"

        )

        if os.path.exists(CSV_FILE):

            try:

                df_anal = pd.read_csv(

                    CSV_FILE

                )

            except Exception:

                df_anal = pd.DataFrame()

        else:

            df_anal = pd.DataFrame()

        if not df_anal.empty:

            df_anal["Thời gian"] = pd.to_datetime(

                df_anal["Thời gian"]

            )

            df_anal["Giờ"] = (

                df_anal["Thời gian"].dt.hour

            )

            df_anal["Tháng-Năm"] = (

                df_anal["Thời gian"]

                .dt.strftime("%m/%Y")

            )

            # =================================================

            # MÓN BÁN CHẠY

            # =================================================

            best_seller = (

                df_anal

                .groupby("Tên món")["Số lượng"]

                .sum()

                .idxmax()

            )

            best_seller_qty = (

                df_anal

                .groupby("Tên món")["Số lượng"]

                .sum()

                .max()

            )

            # =================================================

            # KHUNG GIỜ

            # =================================================

            hourly_sales = (

                df_anal

                .groupby("Giờ")["Số lượng"]

                .sum()

            )

            best_hour = (

                hourly_sales.idxmax()

            )

            best_hour_qty = (

                hourly_sales.max()

            )

            # =================================================

            # THÁNG DOANH THU CAO

            # =================================================

            best_month = (

                df_anal

                .groupby("Tháng-Năm")["Thành tiền"]

                .sum()

                .idxmax()

            )

            best_month_rev = (

                df_anal

                .groupby("Tháng-Năm")["Thành tiền"]

                .sum()

                .max()

            )

            # =================================================

            # KPI

            # =================================================

            col_kpi1, col_kpi2, col_kpi3 = st.columns(3)

            with col_kpi1:

                st.info(

                    "🏆 MÓN BÁN CHẠY NHẤT"

                )

                st.metric(

                    label=best_seller,

                    value=f"{best_seller_qty} phần"

                )

            with col_kpi2:

                st.warning(

                    "⚡ KHUNG GIỜ BÁN CHẠY"

                )

                st.metric(

                    label=(

                        f"{best_hour:02d}:00 - "

                        f"{(best_hour + 1):02d}:00"

                    ),

                    value=f"{best_hour_qty} phần"

                )

            with col_kpi3:

                st.success(

                    "📅 THÁNG DOANH THU CAO"

                )

                st.metric(

                    label=f"Tháng {best_month}",

                    value=f"{best_month_rev:,.0f} VNĐ"

                )

            st.markdown("---")

            # =================================================

            # PHÂN TÍCH TỪNG MÓN

            # =================================================

            st.write(

                "### 🍔 Doanh thu & Số lượng tiêu thụ từng món"

            )

            summary_mon = (

                df_anal

                .groupby("Tên món")

                .agg(

                    Số_lượng_bán=(

                        "Số lượng",

                        "sum"

                    ),

                    Doanh_thu=(

                        "Thành tiền",

                        "sum"

                    )

                )

                .reset_index()

            )

            summary_mon = summary_mon.sort_values(

                by="Số_lượng_bán",

                ascending=False

            )

            col_chart1, col_table1 = st.columns(

                [1.5, 1]

            )

            with col_chart1:

                st.bar_chart(

                    summary_mon

                    .set_index("Tên món")

                    ["Số_lượng_bán"]

                )

            with col_table1:

                st.dataframe(

                    summary_mon,

                    use_container_width=True,

                    hide_index=True

                )

            st.markdown("---")

            # =================================================

            # KHUNG GIỜ

            # =================================================

            st.write(

                "### ⏰ Thống kê lượng khách đặt theo khung giờ"

            )

            summary_gio = (

                df_anal

                .groupby("Giờ")

                .agg(

                    Số_lượng_món=(

                        "Số lượng",

                        "sum"

                    ),

                    Doanh_thu=(

                        "Thành tiền",

                        "sum"

                    )

                )

                .reset_index()

            )

            all_hours = pd.DataFrame(

                {

                    "Giờ": range(24)

                }

            )

            summary_gio = pd.merge(

                all_hours,

                summary_gio,

                on="Giờ",

                how="left"

            ).fillna(0)

            col_chart2, col_info2 = st.columns(

                [1.5, 1]

            )

            with col_chart2:

                st.bar_chart(

                    summary_gio

                    .set_index("Giờ")

                    ["Số_lượng_món"]

                )

            with col_info2:

                st.write(

                    "**⏰ Thời điểm bán chạy nhất:**"

                )

                st.markdown(

                    f"""

                    Khung giờ bán nhiều nhất hiện tại:

                    **{best_hour:02d}:00 - {(best_hour + 1):02d}:00**

                    Tổng cộng:

                    **{best_hour_qty} phần**

                    """

                )

                st.dataframe(

                    summary_gio[

                        summary_gio[

                            "Số_lượng_món"

                        ] > 0

                    ],

                    use_container_width=True,

                    hide_index=True

                )

            st.markdown("---")

            # =================================================

            # DOANH THU THEO THÁNG

            # =================================================

            st.write(

                "### 📅 Doanh thu bán hàng theo Tháng"

            )

            df_anal["Tháng_Số"] = (

                df_anal["Thời gian"].dt.month

            )

            summary_thang = (

                df_anal

                .groupby(

                    [

                        "Tháng_Số",

                        "Tháng-Năm"

                    ]

                )

                .agg(

                    Số_lượng_bán=(

                        "Số lượng",

                        "sum"

                    ),

                    Doanh_thu=(

                        "Thành tiền",

                        "sum"

                    )

                )

                .reset_index()

                .sort_values(

                    "Tháng_Số"

                )

            )

            col_chart3, col_table3 = st.columns(

                [1.5, 1]

            )

            with col_chart3:

                st.bar_chart(

                    summary_thang

                    .set_index("Tháng-Năm")

                    ["Doanh_thu"]

                )

            with col_table3:

                st.dataframe(

                    summary_thang[

                        [

                            "Tháng-Năm",

                            "Số_lượng_bán",

                            "Doanh_thu"

                        ]

                    ],

                    use_container_width=True,

                    hide_index=True

                )

        else:

            st.info(

                "Chưa có dữ liệu giao dịch để thống kê. "

                "Hãy tiến hành thanh toán một vài đơn hàng trước."

            )
