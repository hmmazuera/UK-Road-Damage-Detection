import streamlit as st
from PIL import Image


st.set_page_config(
    page_title="AI Road Infrastructure Inspector",
    page_icon="🛣️",
    layout="wide"
)


@st.cache_resource
def load_model():
    from ultralytics import YOLO
    return YOLO("models/best.pt")


recommendations = {
    "Pothole": "Inspect the pothole and assess patching requirements.",
    "Alligator Crack": "Inspect pavement deterioration and assess repair requirements.",
    "Lateral Crack": "Inspect the crack and assess sealing requirements.",
    "Longitudinal Crack": "Inspect the crack and assess sealing requirements."
}

st.markdown(
    """
    <div style="background-color:#0E1117;padding:25px;
                border-radius:12px;margin-bottom:25px">
        <h1 style="color:white;margin-bottom:5px;">
            🛣️ AI Road Infrastructure Inspector
        </h1>
        <p style="color:#D3D3D3;font-size:18px;">
            Computer Vision application for detecting road surface
            damage using a YOLOv8 object detection model.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Upload a road surface image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")

    original_column, result_column = st.columns(2)

    with original_column:
        st.subheader("📷 Original Image")
        st.image(image, width="stretch")

    if st.button("Detect Road Damage"):
        model = load_model()
        result = model.predict(image, conf=0.25, device="cpu")[0]

        with result_column:
            st.subheader("🎯 Detection Result")
            st.image(
                result.plot(),
                channels="BGR",
                width="stretch"
            )

        detections = []

        for box in result.boxes:
            name = result.names[int(box.cls.item())]

            detections.append({
                "Damage Type": name,
                "Confidence": round(box.conf.item(), 3),
                "Recommended Action": recommendations[name]
            })

        st.markdown("---")
        st.subheader("📊 Detection Summary")

        if detections:
            st.dataframe(
                detections,
                width="stretch",
                hide_index=True
            )

            detected_classes = {
                detection["Damage Type"] for detection in detections
            }

            if "Pothole" in detected_classes:
                priority = "High Priority"
                message = (
                    "Potholes were detected. Road inspection and repair "
                    "are recommended as soon as possible."
                )
                color = "#8B0000"
                icon = "🔴"

            elif "Alligator Crack" in detected_classes:
                priority = "Medium-High Priority"
                message = (
                    "Alligator cracking was detected. This may indicate "
                    "structural pavement deterioration."
                )
                color = "#FF8C00"
                icon = "🟠"

            else:
                priority = "Inspection Recommended"
                message = (
                    "Cracks were detected. Monitoring and preventive "
                    "maintenance are recommended."
                )
                color = "#2E8B57"
                icon = "🟢"

            st.markdown(
                f"""
                <div style="background-color:{color};padding:22px;
                            border-radius:12px;margin-top:20px">
                    <h2 style="color:white;margin-bottom:5px;">
                        {icon} {priority}
                    </h2>
                    <p style="color:white;font-size:17px;">
                        {message}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

        else:
            st.info(
                "No road damage detected with the current confidence "
                "threshold. This does not confirm that the road is damage-free."
            )

else:
    st.info("Upload a road image to start the inspection.")

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center;color:gray">
        AI Road Infrastructure Inspector · Computer Vision · YOLOv8 · Streamlit
    </div>
    """,
    unsafe_allow_html=True
)